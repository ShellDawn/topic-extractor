# -*- coding:utf-8 -*-
import codecs
import os

lh_words_path = "./setting/model_params.txt"


# Remove low-frequency and high-frequency words in global corpus
def remove_lh_words(input_dir, output_dir, dict_dir):
    word_set = set()
    tf_dict = dict()
    df_dict = dict()
    doc_num = 0

    lh_setting = codecs.open(lh_words_path, 'r', 'utf-8')
    lf_threshold = 0
    hf_threshold = 1
    for line in lh_setting:
        if line.startswith("low_frequency_threshold"):
            lf_threshold = float(line.split('=')[1])
        elif line.startswith("high_frequency_threshold"):
            hf_threshold = float(line.split('=')[1])

    # count term frequency & document frequency
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            doc_path = os.path.join(root, file)
            doc_num += 1
            doc_words = []
            with codecs.open(doc_path, 'r', 'utf-8') as doc:
                for line in doc:
                    for word in line.split():
                        doc_words.append(word)
                        if word not in word_set:
                            word_set.add(word)
                            tf_dict[word] = 1
                        else:
                            tf_dict[word] += 1
            doc_words = set(doc_words)
            for w in doc_words:
                if w not in df_dict.keys():
                    df_dict[w] = 1
                else:
                    df_dict[w] += 1

    print("Total documents: ", doc_num)
    print("Total unique words: ", len(word_set))

    with codecs.open("%s/vocab-tf.txt" % dict_dir, 'w', 'utf-8') as fw:
        for word in word_set:
            fw.write(word + '\t' + str(tf_dict[word]) + '\n')
    print("\nSaved term frequency (TF) of words to file [%s/vocab-tf.txt]" % dict_dir)
    with codecs.open("%s/vocab-df.txt" % dict_dir, 'w', 'utf-8') as fw:
        for word in word_set:
            fw.write(word + '\t' + str(df_dict[word]) + '\n')
    print("Saved document frequency (DF) of words to file [%s/vocab-df.txt]" % dict_dir)

    # remove low-frequency and high-frequency words
    lh_words = set()
    print("\nRemoving low-frequency words (DF < %.3f * total documents)" % lf_threshold)
    lc = 0
    for (k, v) in df_dict.items():
        if v < lf_threshold*doc_num:
            lh_words.add(k)
            lc += 1
            if lc <= 10:
                print(k)
    if lc > 10:
        print("...")
    print("Removed %d words." % lc)
    print("Removing high-frequency words (DF > %.3f * total documents)" % hf_threshold)
    hc = 0
    for (k, v) in df_dict.items():
        if v > hf_threshold * doc_num:
            lh_words.add(k)
            hc += 1
            if hc <= 10:
                print(k)
    if hc > 10:
        print("...\n...")
    print("Removed %d words." % hc)

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
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
    print("\nSaved files to [%s]\n" % output_dir)


if __name__ == '__main__':
    input_data_dir = "./data_cleaned/tokenize_out"
    output_data_dir = "./data_cleaned/final_out"
    out_dict_dir = "./data_cleaned"
    remove_lh_words(input_data_dir, output_data_dir, out_dict_dir)
