# -*- coding:utf-8 -*-
import os
import codecs
import matplotlib.pyplot as plt


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
        print("topic", topic)
        trained_dir = lda_dir + '/topic-%s' % str(topic)
        px_path = trained_dir+"/corpus_test.dat.perplex.txt"
        px_list = codecs.open(px_path, 'r', 'utf-8').read()
        px_list = px_list.strip().split('\n')
        px = float(px_list[-1].strip())
        perplexity_list.append(px)
        print("perplexity:", px)
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
