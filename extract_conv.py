import re
import sys
import pickle
import json
from tqdm import tqdm

import jieba
import jieba.posseg as pseg  # 词性标注
import jieba.analyse as anls  # 关键词提取


def make_split(line):
    if re.match(r'.*([，…?!\.,!？])$', ''.join(line)):
        return []
    return [', ']


def good_line(line):
    if len(re.findall(r'[a-zA-Z0-9]', ''.join(line))) > 0:
        return False
    return True


def regular(line):
    line = line.replace('- -', '')
    line = line.replace('  -', '')
    line = line.replace('\n', '')
    line = line.replace(',', '')
    line = line.replace('.', '')
    line = line.replace('?', '')
    line = line.replace('!', '')
    line = line.replace(' ', '')
    line = line.replace('，', '')
    line = line.replace('。', '')
    line = line.replace('？', '')
    line = line.replace('！', '')
    return line


def main(limit=20, x_limit=1, y_limit=1):
    from word_sequence import WordSequence

    print('extract lines')
    fp = open("data170.txt",
              'r', errors='ignore', encoding='utf-8')
    groups = []
    group = []

    # 分词保存
    for line in tqdm(fp):
        if line.startswith('- -') or line.startswith('  -'):
            group = jieba.lcut(regular(line))
            if group:
                groups.append(group)

    print(groups)
    print('extract group')
    print('')
    print('-------------')
    print('')

    x_data = []
    y_data = []

    for i in range((int)(len(groups) / 2)):
        x_line = None
        y_line = None
        if i >= 0:
            x_line = groups[i*2]
            y_line = groups[i*2+1]
            if good_line(x_line) and good_line(y_line):
                x_data.append(x_line)
                y_data.append(y_line)

    # for ask, answer in zip(x_data, y_data):
    #     print(''.join(ask))
    #     print(''.join(answer))
    #     print('-'*20)

    data = list(zip(x_data, y_data))

    data = [
        (x, y)
        for x, y in data
        if len(x) < limit
        and len(y) < limit
        and len(y) >= y_limit
        and len(x) >= x_limit
    ]
    x_data, y_data = zip(*data)
    # print(x_data + y_data)

    print('')
    print('fit word_sequence')
    print('')
    print('-------------')

    ws_input = WordSequence()
    ws_input.fit(x_data + y_data)

    print(ws_input.dict)
    with open('data170_vector.txt', 'w+', encoding='utf-8') as f :
        for key, value in ws_input.dict.items() :
            f.writelines(str(value) + ':  ' + key + '\n')
        print('write file')

    print('dump')

    pickle.dump(
        (x_data, y_data),
        open('data170.pkl', 'wb')
    )
    pickle.dump(ws_input, open('ws170.pkl', 'wb'))

    print('done')


if __name__ == '__main__':
    main()
