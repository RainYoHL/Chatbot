import numpy as np


class WordSequence(object):

    PAD_TAG = '<pad>'
    UNK_TAG = '<unk>'
    START_TAG = '<s>'
    END_TAG = '</s>'

    PAD = 0
    UNK = 1
    START = 2
    END = 3

    def __init__(self):
        # 初始化基本的字典dict
        self.dict = {
            WordSequence.PAD_TAG: WordSequence.PAD,
            WordSequence.UNK_TAG: WordSequence.UNK,
            WordSequence.START_TAG: WordSequence.START,
            WordSequence.END_TAG: WordSequence.END,
        }
        self.fited = False

    def to_index(self, word):
        assert self.fited, "WordSequence 尚未进行 fit 操作"
        if word in self.dict:
            return self.dict[word]
        return WordSequence.UNK

    def to_word(self, index):
        assert self.fited, "WordSequence 尚未进行 fit 操作"
        for k, v in self.dict.items():
            if v == index:
                return k
        return WordSequence.UNK_TAG

    def size(self):

        assert self.fited, "WordSequence 尚未进行 fit 操作"
        return len(self.dict) + 1

    def __len__(self):
        return self.size()

    def fit(self, sentences, min_count=1, max_count=None, max_features=None):

        assert not self.fited, 'WordSequence 只能fit一次'
        count = {}
        # print(sentences)

        for sentence in sentences:
            arr = sentence
            for word in arr:
                if word not in count:
                    count[word] = 0
                count[word] += 1
        if min_count is not None:
            count = {k: v for k, v in count.items() if v >= min_count}

        # if max_count is not None:
        #     count = {k: v for k, v in count.items() if v <= max_count}

        self.dict = {
            WordSequence.PAD_TAG: WordSequence.PAD,
            WordSequence.UNK_TAG: WordSequence.UNK,
            WordSequence.START_TAG: WordSequence.START,
            WordSequence.END_TAG: WordSequence.END,
        }

        if isinstance(max_features, int):
            print(1)
            count = sorted(list(count.items()), key=lambda x: x[1])

            if len(count) > max_features:
                count = count[-int(max_features):]
            for w, _ in count:
                self.dict[w] = len(self.dict)

        else:
            for w in sorted(count.keys()):
                self.dict[w] = len(self.dict)

        self.fited = True

    def transform(self, sentence, max_len=None):
        assert self.fited, "WordSequence 尚未进行 fit 操作"

        if max_len is not None:
            r = [self.PAD] * max_len

        else:
            r = [self.PAD] * len(sentence)

        for index, a in enumerate(sentence):
            if index >= len(r):
                break
            r[index] = self.to_index(a)
        return np.array(r)

    def inverse_transform(self, indices,
                          ignore_pad=False, ignore_unk=False,
                          ignore_start=False, igonre_end=False):
        ret = []
        for i in indices:
            word = self.to_word(i)
            if word == WordSequence.PAD_TAG and ignore_pad:
                continue
            if word == WordSequence.UNK_TAG and ignore_unk:
                continue
            if word == WordSequence.START_TAG and ignore_start:
                continue
            if word == WordSequence.END_TAG and igonre_end:
                continue
            ret.append(word)

        return ret


def test():

    ws = WordSequence()
    ws.fit((
        ['足球', '球', '蓝', '球', '球'],
        ['足', '蓝', '球'],
    ))

    indice = ws.transform(['蓝', '球'])
    print(indice)

    back = ws.inverse_transform(indice)
    print(back)


if __name__ == '__main__':
    test()
