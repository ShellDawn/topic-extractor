# -*- coding:utf-8 -*-
import codecs
import os

lh_words_path = "./setting/model_params.txt"


# Remove low-frequency and high-frequency words in global corpus
def remove_lh_words(input_dir, output_dir, out_dict_file):
    word_set = set()
    freq_dict = dict()
    doc_num = 0

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    # record all unique words
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            doc_path = os.path.join(root, file)
            doc_num += 1
            with codecs.open(doc_path, 'r', 'utf-8') as doc:
                for line in doc:
                    for word in line.split():
                        if word not in word_set:
                            word_set.add(word)
                            freq_dict[word] = 0
                        else:
                            freq_dict[word] += 1

    lh_setting = codecs.open(lh_words_path, 'r', 'utf-8')
    lf_threshold = 0
    hf_threshold = 1
    for line in lh_setting:
        if line.startswith("low_frequency_threshold"):
            lf_threshold = float(line.split('=')[1])
        elif line.startswith("high_frequency_threshold"):
            hf_threshold = float(line.split('=')[1])
    print("Removing low-frequency words <", lf_threshold)
    print("Removing high-frequency words >", hf_threshold)

    for k, v in freq_dict.items():
        if v < lf_threshold*doc_num:
            word_set.remove(k)
        freq_dict[k] = 0

    print("Total unique words: ", len(word_set))
    print("Total documents: ", doc_num)

    for word in word_set:
        for root, dirs, files in os.walk(input_dir):
            for file in files:
                doc_path = os.path.join(root, file)
                doc = codecs.open(doc_path, 'r', 'utf-8').read()
                if word in doc:
                    freq_dict[word] += 1

    print("==================================")
    with codecs.open(out_dict_file, 'w', 'utf-8') as fw:
        for word in word_set:
            fw.write(word + '\t' + str(freq_dict[word]) + '\n')

    # remove low-frequency and high-frequency words
    lh_words = set()
    for (k, v) in freq_dict.items():
        if v < lf_threshold*doc_num or v > hf_threshold*doc_num:
            lh_words.add(k)
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            doc_path = os.path.join(root, file)
            out_file = output_dir+'/'+file
            fin = codecs.open(doc_path, 'r', 'utf-8')
            fout = codecs.open(out_file, 'w', 'utf-8')
            word_list = fin.read()
            store_words = []
            for word in word_list.split(" "):
                if not (word.strip() in lh_words) and len(word.strip()) > 1:
                    store_words.append(word)
            store_words = " ".join(store_words)
            fout.write(store_words)
    print("Finished.\n")


if __name__ == '__main__':
    input_dir = "./cleaned_data/tokenize_out"
    output_dir = "./cleaned_data/final_out"
    out_dict_file = "./cleaned_data/vocab.txt"
    remove_lh_words(input_dir, output_dir, out_dict_file)
