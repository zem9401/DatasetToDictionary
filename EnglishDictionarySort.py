import json
import os
import re
import nltk
import string
from collections import defaultdict
from nltk.tokenize import WordPunctTokenizer
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters



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
    punkt_param = PunktParameters()
    # 这里想对U.S缩略词进行处理，好像失败了
    abbreviation = ['U.S']
    punkt_param.abbrev_types = set(abbreviation)
    tokenizer = PunktSentenceTokenizer(punkt_param)
    pat_letter = re.compile(r'[^a-zA-Z \']+')
    # 对一些缩略词进行转换处理
    # to find the 's following the pronouns. re.I is refers to ignore case
    pat_is = re.compile("(it|he|she|that|this|there|here)(\'s)", re.I)
    # to find the 's following the letters
    pat_s = re.compile("(?<=[a-zA-Z])\'s")
    # to find the ' following the words ending by s
    pat_s2 = re.compile("(?<=s)\'s?")
    # to find the abbreviation of not
    pat_not = re.compile("(?<=[a-zA-Z])n\'t")
    # to find the abbreviation of would
    pat_would = re.compile("(?<=[a-zA-Z])\'d")
    # to find the abbreviation of will
    pat_will = re.compile("(?<=[a-zA-Z])\'ll")
    # to find the abbreviation of am
    pat_am = re.compile("(?<=[I|i])\'m")
    # to find the abbreviation of are
    pat_are = re.compile("(?<=[a-zA-Z])\'re")
    # to find the abbreviation of have
    pat_ve = re.compile("(?<=[a-zA-Z])\'ve")

    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, str) and (key == "id" or key == "is_impossible"):
                continue
            elif isinstance(value, int) and key == "answer_start":
                continue
            elif isinstance(value, str):
                #
                value = "".join(tokenizer.tokenize(value))
                # 通过正则去除标点，除'外
                value = pat_letter.sub(' ', value).strip().lower()
                value = pat_is.sub(r"\1 is", value)
                value = pat_s.sub("", value)
                value = pat_s2.sub("", value)
                value = pat_not.sub(" not", value)
                value = pat_would.sub(" would", value)
                value = pat_will.sub(" will", value)
                value = pat_am.sub(" am", value)
                value = pat_are.sub(" are", value)
                value = pat_ve.sub(" have", value)
                value = value.replace('\'', ' ')
                words.extend(WordPunctTokenizer().tokenize(value))
            else:
                data_to_words(value)
    elif isinstance(data, list):
        for i in data:
            if isinstance(i, str):
                i = "".join(tokenizer.tokenize(i))
                i = pat_letter.sub(' ', i).strip().lower()
                i = pat_is.sub(r"\1 is", i)
                i = pat_s.sub("", i)
                i = pat_s2.sub("", i)
                i = pat_not.sub(" not", i)
                i = pat_would.sub(" would", i)
                i = pat_will.sub(" will", i)
                i = pat_am.sub(" am", i)
                i = pat_are.sub(" are", i)
                i = pat_ve.sub(" have", i)
                i = i.replace('\'', ' ')
                words.extend(WordPunctTokenizer().tokenize(i))
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
    # dev_data_words = data_to_words(dev_data)
    train_data_words = data_to_words(train_data)
    vocab = sort_vocab(train_data_words)
    save_words_dictionary(vocab, '{}/vocab.txt'.format(BASE_DIR))