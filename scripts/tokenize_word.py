# -*- coding:utf-8 -*-
import codecs
import os
import jieba

stopwords_path = "./setting/stop_words.txt"
synonyms_path = "./setting/synonyms_words.txt"
user_dicts = "./setting/user_defined_dicts.txt"


def is_instr(str):
    if "一" in str or \
                    "二" in str or \
                    "三" in str or \
                    "四" in str or \
                    "五" in str or \
                    "六" in str or \
                    "七" in str or \
                    "八" in str or \
                    "九" in str or \
                    "十" in str:
        return True
    else:
        return False


# Tokenize and remove stop words and merge synonyms
def tokenize(input_dir, output_dir):
    # load user-defined dicts
    jieba.load_userdict(user_dicts)

    # load synonyms
    combine_dict = {}
    for line in codecs.open(synonyms_path, 'r', 'utf-8'):
        seperate_word = line.strip().split('-')
        num = len(seperate_word)
        for i in range(1, num):
            # 将同义词表中后一个词全部映射到前一个词
            combine_dict[seperate_word[i]] = seperate_word[0]

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    # remove stop words and merge synonyms
    print("Tokenize and remove stop words...")
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            doc_path = os.path.join(root, file)
            out_file = output_dir+'/'+file
            fin = codecs.open(doc_path, 'r', 'utf-8')
            fout = codecs.open(out_file, 'w', 'utf-8')
            f_stop = codecs.open(stopwords_path, 'r', 'utf-8')

            texts = fin.read()
            stop_text = f_stop.read()
            word_list = []
            # 分词
            seg_list = jieba.cut(texts)
            seg_list = "/".join(seg_list)

            # 同义词替换
            seg_text = []
            for word in seg_list.split('/'):
                word = word.strip()
                if word in combine_dict.keys():
                    seg_text.append(combine_dict[word])
                else:
                    seg_text.append(word)

            # 去除停用词
            stop_seg_list = stop_text.split('\n')
            for word in seg_text:
                if (not (word in stop_seg_list)) and (not is_instr(word.strip())):
                    word_list.append(word)

            word_list = " ".join(word_list)
            fout.write(word_list)
    print("Saved files to [%s]\n" % output_dir)


if __name__ == '__main__':
    data_dir = "./data_cleaned/clean_text_out"
    out_dir = "./data_cleaned/tokenize_out"
    tokenize(data_dir, out_dir)
