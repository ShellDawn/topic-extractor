# -*- coding:utf-8 -*-
import os
import codecs
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# Calculate perplexity of LDA
def cal_perplex(topic_word_fp, doc_topic_fp, tassign_fp):
    topic_word = np.loadtxt(topic_word_fp)
    doc_topic = np.loadtxt(doc_topic_fp)
    topic_word = np.mat(np.asarray(topic_word))
    doc_topic = np.mat(np.asarray(doc_topic))

    doc_word = doc_topic * topic_word
    doc_word = pd.DataFrame(doc_word)
    log_pw = doc_word.apply(lambda x: np.log(x.sum()), axis=0)
    sum_log_pw = np.sum(log_pw)

    sum_t = 0
    with open(tassign_fp, 'r') as fr:
        for line in fr:
            doc_i = line.strip().split(' ')
            n_words = len(doc_i)
            sum_t += n_words

    perplexity = np.exp(-sum_log_pw/sum_t)
    return perplexity


# Plot "perplexity" to "number of topics" of LDA according to model results
def plot_perplexity(lda_dir, figure_dir, params_path):
    # default settings
    topic_list = []
    perplexity_list = []
    # get parameters from setting file
    with codecs.open(params_path, 'r', 'utf-8') as pfile:
        for line in pfile:
            if line.startswith('ntopics'):
                topics = line.split('=')[1].strip()
                topic_list = topics.split()

    for topic in topic_list:
        print("Calculating perplexity when topic = %s" % topic)
        model_dir = "%s/topic-%s" % (lda_dir, topic)
        topic2word_file = "%s/corpus_test.dat.phi" % model_dir
        doc2topic_file = "%s/corpus_test.dat.theta" % model_dir
        tassign_file = "%s/corpus_test.dat.tassign" % model_dir
        px = cal_perplex(topic2word_file, doc2topic_file, tassign_file)
        perplexity_list.append(px)
    figure_plot(topic_list, perplexity_list, figure_dir)


def figure_plot(topic, perplexity, figure_dir):

    x = topic
    y = perplexity
    plt.rcParams['xtick.direction'] = 'in'
    plt.rcParams['ytick.direction'] = 'in'

    # set size of the figure
    plt.figure(figsize=(12, 8))

    plt.plot(x, y, marker="*", color="red", linewidth=2)

    # set margin of the figure
    plt.subplots_adjust(left=0.08, right=0.95, top=0.95, bottom=0.1)

    plt.xlabel("Number of Topics")
    plt.ylabel("Perplexity")

    plt.savefig(figure_dir + '/perplexity.png')
    plt.show()


if __name__ == '__main__':
    params_path = "./setting/model_params.txt"
    lda_dir = "./models/lda"
    result_dir = "./results"
    if not os.path.exists(result_dir):
        os.mkdir(result_dir)
    plot_perplexity(lda_dir, result_dir, params_path)
