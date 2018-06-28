# -*- coding:utf-8 -*-
import os
import codecs
import shutil
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# Divide cleaned data into training data and test data
def divide_corpus():
    corpus_dir = "./cleaned_data/stage_4_out"
    lda_model_dir = "./models/lda"

    if not os.path.exists(lda_model_dir):
        os.mkdir(lda_model_dir)

    corpus =[]
    for root, dirs, files in os.walk(corpus_dir):
        for file in files:
            doc_path = os.path.join(root, file)
            doc = codecs.open(doc_path, 'r', 'utf-8').read()
            corpus.append(doc)
    print("Total documents: ", len(corpus))

    random.shuffle(corpus)
    p = int(len(corpus)*0.9)
    train = corpus[:p]
    test = corpus[p:]

    with codecs.open(lda_model_dir+"/"+"corpus_train.dat", 'w', 'utf-8') as datfile:
        datfile.write(str(len(train)) + '\n')
        for doc in train:
            datfile.write(doc + '\n')
    with codecs.open(lda_model_dir+"/"+"corpus_test.dat", 'w', 'utf-8') as testfile:
        testfile.write(str(len(test)) + '\n')
        for doc in test:
            testfile.write(doc + '\n')
    print("Train documents: ", len(train))
    print("Test documents: ", len(test))


# Run LDA model with Gibbs sampling
def lda_estimate():

    train_path = "./models/lda/corpus_train.dat"
    test_path = "./models/lda/corpus_test.dat"
    params_path = "./setting/model_params.txt"

    # get parameters from setting file
    with codecs.open(params_path, 'r', 'utf-8') as pfile:
        for line in pfile:
            if line.startswith("alpha"):
                alpha = line.split('=')[1].strip()
            elif line.startswith("beta"):
                beta = line.split('=')[1].strip()
            elif line.startswith('ntopics'):
                topic = line.split('=')[1].strip()
            elif line.startswith('niters'):
                niters = line.split('=')[1].strip()
            elif line.startswith('savestep'):
                savestep = line.split('=')[1].strip()
            elif line.startswith('twords'):
                twords = line.split('=')[1].strip()
    # create dirs for LDA model output
    tdir = "./models/lda/topic_" + str(topic)
    if not os.path.exists(tdir):
        os.mkdir(tdir)

    tfile = tdir + "/corpus_train.dat"
    testfile = tdir + "/corpus_test.dat"
    if not os.path.exists(tfile):
        shutil.copyfile(train_path, tfile)
    if not os.path.exists(testfile):
        shutil.copyfile(test_path, testfile)

    # call external C++ exe to run LDA topic model
    print("Training LDA model with", topic, "topics...")
    os.chdir("./lib/GibbsLDA++/bin")
    dfile = "../../../models/lda/corpus_train.dat"
    params = "-alpha " + str(alpha) + " -beta " + str(beta) + " -ntopics " + str(topic) \
             + " -niters " + str(niters) + " -savestep " + str(savestep) + " -twords " + str(twords) \
             + " -treval 1" + " -dfile " + str(dfile)
    os.system("lda.exe -est " + params)
    os.chdir("../../../")
    print("Training finished.")


# Using trained model to do inference on test set
def lda_inference():
    params_path = "./setting/model_params.txt"
    with codecs.open(params_path, 'r', 'utf-8') as pfile:
        for line in pfile:
            if line.startswith('ntopics'):
                topic = line.split('=')[1].strip()

    # call external C++ exe to run LDA inference
    print("Inference on test set with", topic, "topics...")
    os.chdir("./lib/GibbsLDA++/bin")
    dir_prefix = "../../../models/lda/topic_"
    tfile = "../../../models/lda/corpus_test.dat"
    dir = dir_prefix + str(topic) + '/'
    params = "-dir " + dir + " -model model-final -niters 20 -twords 50 -treval 1 -teval 1 -dfile " + tfile
    os.system("lda.exe -inf " + params)
    os.chdir("../../../")
    print("Inference finished.")


def figure_plot(topic, perplexity):
    figure_dir = "./Figures"
    if not os.path.exists(figure_dir):
        os.mkdir(figure_dir)
    x = topic
    y = perplexity
    plt.rcParams['xtick.direction'] = 'in'
    plt.rcParams['ytick.direction'] = 'in'

    # 设置图片的尺寸
    plt.figure(figsize=(12, 8))

    plt.plot(x, y, marker="*", color="red", linewidth=2)

    # 设置图片的边距
    plt.subplots_adjust(left=0.08, right=0.95, top=0.95, bottom=0.1)

    plt.xlabel("Number of Topics")
    plt.ylabel("Perplexity")

    plt.savefig(figure_dir + '/' + 'perplexity.svg')
    plt.show()

'''
# Calculate perplexity of LDA
def cal_perplex(topic_word, doc_topic, tassign):

    topic_word = np.mat(np.asarray(topic_word))
    doc_topic = np.mat(np.asarray(doc_topic))
    doc_word = doc_topic * topic_word
    doc_word = pd.DataFrame(doc_word)
    print(doc_word.shape)

    log_pw = doc_word.apply(lambda x: np.log(x.sum()), axis=0)
    sum_log_pw = np.sum(log_pw)
    print("sum_log_pw:", sum_log_pw)

    sum_t = 0
    for i in range(len(tassign)):
        doc_i = tassign[i].strip().split(" ")
        sum_t += len(doc_i)
    print("sum_t:", sum_t)

    
    for i in range(len(tassign)):
        doc_i = tassign[i].strip().split(" ")
        print(len(doc_i))
        sum_t += len(doc_i)
        log_pw = 0.0
        for word in doc_i:
            pz = 0.0
            word_id = int(word.split(':')[0])
            for j in range(len(topic_word)):
                if word_id in range(topic_word.shape[1]):
                    p_tz = float(topic_word.ix[j][word_id])
                else:
                    p_tz = 0.0
                    #print("word id:", word_id)
                p_zd = float(doc_topic.ix[i][j])
                pz += p_tz*p_zd
            log_pw += np.log(pz+0.0001)
        sum_log_pw += log_pw
    

    perplexity = np.exp(-sum_log_pw/sum_t)
    print("perplex: ", perplexity)
    return perplexity
'''

# Plot "perplexity" to "number of topics" of LDA according to model results
def plot_perplexity():
    dir_prefix = "./models/lda/topic_"
    params_path = "./setting/model_params.txt"
    perplexity_list = []

    with codecs.open(params_path, 'r', 'utf-8') as pfile:
        for line in pfile:
            if line.startswith('topic_list'):
                line = line.split('=')[1]
                line = line[1:-3].split(',')
                topic_list = list(int(line[i]) for i in range(len(line)))
    for topic in topic_list:
        print("topic", topic)
        dir = dir_prefix + str(topic) + '/'
        px_path = dir+"corpus_test.dat.perplex.txt"
        px_list = codecs.open(px_path, 'r', 'utf-8').read()
        px_list = px_list.strip().split('\n')
        px = float(px_list[-1].strip())
        perplexity_list.append(px)
        print("px:", px)
    figure_plot(topic_list, perplexity_list)


# Save doc-topic matrix
def save_doc_topic():
    directory = "./cleaned_data/stage_4_out"
    gam_file_path = "./models/dtm/lda-seq/gam.dat"
    param_path = "./setting/model_params.txt"
    with codecs.open(param_path, 'r', 'utf-8') as pfile:
        for line in pfile:
            if line.startswith("topics"):
                num_topics = int(line.strip().split('=')[1])

    gammas = pd.read_table(gam_file_path, header=None)
    gammas = np.array(gammas)
    gammas = gammas.reshape((-1, num_topics))
    gammas = pd.DataFrame(gammas)


if __name__ == "__main__":
    print("Test functions in 'lda.py'.")
    #lda_estimate()
    #lda_inference()
    #plot_perplexity()