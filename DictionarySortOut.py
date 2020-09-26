import json
import os
from collections import defaultdict


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
words = []

# 将json文件中的数据读取出来
def read_data(path_1, path_2):
    with open(path_1, 'r', encoding='utf-8') as f1,\
            open(path_2, 'r', encoding='utf-8') as f2:
        data_1 = json.load(f1)
        data_2 = json.load(f2)

    return data_1["data"], data_2["data"]

# 进行递归遍历字典嵌套列表内容
def data_to_words(data):
    global words
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, str) and (key == "id" or key == "is_impossible"):
                continue
            elif isinstance(value, int) and key == "answer_start":
                continue
            elif isinstance(value, str):
                words += value.split(" ")
                # print("%s" %key)
                # print(value)
            else:
                data_to_words(value)
    elif isinstance(data, list):
        for i in data:
            if isinstance(i, str):
                words += i.split()
            else:
                data_to_words(i)
    else:
        # print("{}".format(data))
        pass
    return words


# 存储已经整理词频后的内容
def save_words_dictionary(vocab, save_path):
    with open(save_path, 'w', encoding='utf-8') as f:
        for line in vocab:
            w, i = line
            f.write("%s\t%d\n" % (w, i))

# 整理词频
def sort_vocab(items):
    count_dict = defaultdict(lambda: 0)
    for item in items:
        count_dict[item] += 1
    return sorted(count_dict.items(), key=lambda x: x[1], reverse=True)


if __name__ == '__main__':
    datas = read_data('{}\DataSet\dev-v2.0.json'.format(BASE_DIR),
                      '{}\DataSet\\train-v2.0.json'.format(BASE_DIR))
    dev_data, train_data = datas
    dev_data_words = data_to_words(dev_data)
    train_data_words = data_to_words(train_data)
    vocab = sort_vocab(train_data_words)
    save_words_dictionary(vocab, '{}/vocab.txt'.format(BASE_DIR))