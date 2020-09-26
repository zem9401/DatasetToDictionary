import json
import os
import jieba
from jieba import analyse
from collections import defaultdict, Counter


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
words = []
search_data_vocabs = []
zhidao_data_vocabs = []
title = []
paragraphs = []
answers = []
question = []
vocabs = []

# 读取数据，处理MemoryError问题，防止json文件过大读取不了,读取一行处理一行
def read_data(path_1, path_2):

    global search_data_vocabs
    global zhidao_data_vocabs
    # fin_1 = open(save_path_1, "w")
    # fin_2 = open(save_path_2, "w")
    with open(path_1, 'r', encoding="utf-8") as f1,\
            open(path_2, 'r', encoding="utf-8") as f2:
        # 尝试逐行读取数据,方法1
        # try:
        #     while True:
        #         line_1 = f1.readline()
        #         line_2 = f2.readline()
        #         if line_1 or line_2:
        #             data_1 = json.loads(line_1)
        #             data_2 = json.loads(line_2)
        #         else:
        #             break
        # except Exception as e:
        #     print(e)
        #     f1.close()
        #     f2.close()
        # 方法2

        for i, line in enumerate(f1):
            # print("这是data_1 i")
            # print(i)
            # print("这是line")
            # print(line)
            data_1 = json.loads(line)
            search_data_vocabs.extend(data_to_vocabs(data_1))
            # print("这里是search_data_vocabs")
            # print(search_data_vocabs)
            search_vocabs = sort_vocab(search_data_vocabs)

        for i, line in enumerate(f2):
            # print("这是data_2 i")
            # print(i)
            # print("这是line")
            # print(line)
            data_2 = json.loads(line)
            zhidao_data_vocabs.extend(data_to_vocabs(data_2))
            # print("这里是zhidao_data_vocabs")
            # print(zhidao_data_vocabs)
            zhidao_vocabs = sort_vocab(zhidao_data_vocabs)

    # print(data_1)
    return search_vocabs, zhidao_vocabs

# 通过递归遍历内部内容
# def data_to_vocabs(data):
#     global words
#     if isinstance(data, dict):
#         for key, value in data.items():
#             if key == "title":
#                 words.extend(seg_word(value))
#             elif key == "paragraphs":
#                 words.extend(seg_word(value))
#             elif key == "answers":
#                 words.extend(seg_word(value))
#             elif key == "question":
#                 words.extend(seg_word(value))
#             else:
#                 data_to_vocabs(value)
#     else:
#         pass
#     return words

# 使用字典结构特性获取元素,最后返回vocabs列表
def data_to_vocabs(data):
    global answers
    global question
    global title
    global paragraphs
    global vocabs

    for answer in data["answers"]:
        answers.extend(seg_word(answer))
    question.extend(seg_word(data["question"]))

    for doc in data["documents"]:
        title.extend(seg_word(doc["title"]))
        for para in doc["paragraphs"]:
            paragraphs.extend(seg_word(para))

    vocabs.extend(title)
    vocabs.extend(paragraphs)
    vocabs.extend(answers)
    vocabs.extend(question)

    return vocabs

def seg_word(text):
    text_temp = list(jieba.cut(text))
    return text_temp

# 整理词频
def sort_vocab(items):
    count_dict = defaultdict(lambda: 0)
    for item in items:
        count_dict[item] += 1
    return sorted(count_dict.items(), key=lambda x: x[1], reverse=True)

    # count_result = Counter(items)
    # return list(count_result.elements())


# 存储已经整理词频后的内容
def save_words_dictionary(vocab, save_path):
    with open(save_path, 'w', encoding='utf-8') as f:
        for line in vocab:
            w, i = line
            f.write("%s\t%d\n" % (w, i))


if __name__ == '__main__':
    datas = read_data("{}\DataSet\preprocessed\\trainset\search.train.json".format(BASE_DIR),
                      "{}\DataSet\preprocessed\\trainset\zhidao.train.json".format(BASE_DIR))
    search_vocabs, zhidao_vocabs = datas

    # search_data_vocabs = data_to_vocabs(search_data)
    # zhidao_data_vocabs = data_to_vocabs(zhidao_data)

    # search_vocabs = sort_vocab(search_data_vocabs)
    # zhidao_vocabs = sort_vocab(zhidao_data_vocabs)

    save_words_dictionary(search_vocabs, '{}/search_vocabs.txt'.format(BASE_DIR))
    save_words_dictionary(zhidao_vocabs, '{}/zhidao_vocabs.txt'.format(BASE_DIR))

    # print(search_data_vocabs)
    # print(zhidao_data_vocabs)
