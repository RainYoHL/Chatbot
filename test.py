import sys
import pickle

import numpy as np
import tensorflow as tf
# sys.path.append('E:/VSCode/Python/Chatbot/Chatbot_1/Chatbot_2')

from sequence_to_sequence import SequenceToSequence
from data_utils import batch_flow

import jieba


def test(params):
    x_data, _ = pickle.load(open('data170.pkl', 'rb'))
    ws = pickle.load(open('ws170.pkl', 'rb'))

    config = tf.ConfigProto(
        device_count={'CPU': 1, 'GPU': 0},
        allow_soft_placement=True,
        log_device_placement=False
    )

    save_path = './model/epoch_800_learn_rate_0.001_depth_4_hidden_units_128_data170/s2ss_chatbot.ckpt'

    tf.reset_default_graph()
    model_pred = SequenceToSequence(
        input_vocab_size=len(ws),
        target_vocab_size=len(ws),
        batch_size=1,
        mode='decode',
        beam_width=0,
        **params
    )
    init = tf.global_variables_initializer()

    with tf.Session(config=config) as sess:
        sess.run(init)
        model_pred.load(sess, save_path)
        with open('data170_question.txt', 'r', encoding='utf-8') as f:
            with open('result_800_data170.txt', 'w+', encoding='utf-8') as f_r:
                while True:
                    # user_text = f.readline()
                    # user_text = user_text.replace('\n', '')
                    # print('问: ' + user_text)
                    # f_r.write('问: ' + user_text + '\n')
                    user_text = input('问: ')
                    if user_text in ('exit', 'quit'):
                        exit(0)

                    x_test = []
                    x_test.append(jieba.lcut(user_text))

                    bar = batch_flow([x_test], ws, 1)
                    x, xl = next(bar)
                    x = np.flip(x, axis=1)

                    # print(x, xl)

                    pred = model_pred.predict(
                        sess,
                        np.array(x),
                        np.array(xl)
                    )
                    # print(pred)

                    # print(ws.inverse_transform(x[0]))

                    ans = ws.inverse_transform(pred[0])
                    print('答: ' + str(ans) + '\n')
                    print()
                    # f_r.write('答: ' + str(ans) + '\n')
                    # return ans


def chatbot():
    import json
    text = test(json.load(open('params.json')))
    return


if __name__ == '__main__':
    chatbot()
