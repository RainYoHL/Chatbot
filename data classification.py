#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @File    :   1.py
# @Time    :   2019/08/11 01:12:21
# @Author  :   Atu
# @Version :   3.6.5

def regular(line):
    line = line.replace('-', '')
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

with open('data170.txt', 'r', encoding='utf-8') as f_all :
    with open('data170_question.txt', 'w+', encoding='utf-8') as f_q :
        with open('data170_answer.txt', 'w+', encoding='utf-8') as f_a :
            line = f_all.readline()
            while line :
                if line.startswith('- -'):
                    line = regular(line)
                    f_q.write(line)
                elif line.startswith('  -'):
                    line = regular(line)
                    f_a.write(line)
                line = f_all.readline()
            f_q.write('exit')