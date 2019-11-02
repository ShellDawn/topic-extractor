# -*- coding:utf-8 -*-
import os
import codecs
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties


# Calculate word-time matrix from DTM output
def cal_word_times(topic_no, time_slice, k_term=8):
    topic_file_path = "%s/lda-seq/" % dtm_dir
    time_file_path = "%s/time-seq.txt" % db_dir
    vocab_file_path = "%s/data_cleaned.vocab" % db_dir

    if topic_no < 10:
        topic_file_name = "topic-00" + str(topic_no) + "-var-e-log-prob.dat"
    else:
        topic_file_name = "topic-0" + str(topic_no) + "-var-e-log-prob.dat"

    matrix = pd.read_table(topic_file_path + topic_file_name, header=None)
    matrix = np.array(matrix)
    matrix = matrix.reshape((-1, time_slice))
    matrix = np.exp(matrix)
    matrix = pd.DataFrame(matrix)
    vocab = pd.read_table(vocab_file_path, header=None, encoding='utf-8')

    # get date list from time seq file
    date_list = []
    with codecs.open(time_file_path, 'r', 'utf-8') as tfile:
        for line in tfile:
            date_list.append(int(line.strip()))

    # count total prob. of each term in all time slices
    matrix['sum'] = matrix.apply(lambda x: x.sum(), axis=1)
    top_k_term = sorted(np.array(matrix['sum']), reverse=True)
    y_vars = []
    var_names = []

    for i in range(k_term):
        top_k = top_k_term[i]
        index = np.where(matrix['sum'] == top_k)
        index = int(index[0])
        var = list(matrix.ix[index, :-1])
        var.insert(0, vocab.ix[index][0])
        y_vars.append(var)
        var_names.append(vocab.ix[index][0])
        print(vocab.ix[index][0])

    # set direction of X, Y axis
    plt.rcParams['xtick.direction'] = 'in'
    plt.rcParams['ytick.direction'] = 'in'

    # set font size
    if k_term <= 20:
        font = FontProperties(fname='C:\Windows\Fonts\msyh.ttc', size=10)
    elif k_term > 20:
        font = FontProperties(fname='C:\Windows\Fonts\msyh.ttc', size=8)

    colors = ["red", "blue", "black", "orange", "purple", "green", "magenta", "cyan", "yellow", "gray"]
    markers = ['+', '.', '*']
    color_index = 0
    marker_index = 0

    # set figure size
    fig, ax = plt.subplots(figsize=(12, 8))

    for i in range(k_term):
        legend_name = var_names[i]
        ax.plot(date_list, y_vars[i][1:], 'k--', marker=markers[marker_index],
                label=legend_name, color=colors[color_index], linewidth=1)
        color_index += 1
        color_index = color_index % 10
        if color_index == 0:
            marker_index = (marker_index + 1) % 3
    if k_term <= 10:
        ncol = 2
    elif k_term <= 15:
        ncol = 3
    elif k_term <= 20:
        ncol = 4
    elif k_term <= 25:
        ncol = 5
    else:
        ncol = 6
    ax.legend(prop=font, loc='best', ncol=ncol)

    df_data = []
    for i in range(k_term):
        df_data.append(y_vars[i][1:])
    df_data = pd.DataFrame(df_data, dtype=float)

    df_mean = df_data.apply(lambda x: np.mean(x), axis=0)
    df_std = df_data.apply(lambda x: np.std(x), axis=0)

    '''
    # show Mean line & Std. line
    
    right_axis = ax.twinx()
    right_axis.plot(date_list, df_mean, marker=".", linestyle="-", label="Mean", color="black", linewidth=1.5)
    right_axis.plot(date_list, df_std, marker="|", linestyle="-", label="Standard deviation", color="black", linewidth=1.5)
    right_axis.legend(prop=font, loc='upper center', bbox_to_anchor=(0.9, 0.8))
    right_axis.set_ylabel("Mean & Standard deviation", fontdict=font2)
    '''

    # set title
    plt.title("Topic%s" % str(topic_no))

    # set font size of labels on X, Y axis
    font2 = {'weight': 'normal', 'size': 10}
    ax.set_xlabel(xlabel="Year", fontdict=font2)
    ax.set_ylabel(ylabel="Probability", fontdict=font2)

    # set label size
    plt.tick_params(labelsize=10)

    # set margin
    fig.subplots_adjust(left=0.08, right=0.93, top=0.95, bottom=0.1)
    fig_fp = "%s/word-times_topic-%d.png" % (result_dir, topic_no)
    plt.savefig(fig_fp)
    print("Saved word-time figure to [%s]" % fig_fp)
    plt.show()

    # write results to csv
    y_vars = pd.DataFrame(y_vars)
    df_mean = list(df_mean)
    df_mean.insert(0, 0)
    df_mean = np.array(df_mean).reshape(1, -1)
    df_mean = pd.DataFrame(df_mean)
    df_std = list(df_std)
    df_std.insert(0, 0)
    df_std = np.array(df_std).reshape(1, -1)
    df_std = pd.DataFrame(df_std)
    y_res = pd.concat([y_vars, df_mean, df_std], axis=0)
    date_list.insert(0, 'Year')
    y_res.columns = date_list
    csv_fp = "%s/word-times_topic-%d.csv" % (db_dir, topic_no)
    y_res.to_csv(csv_fp, header=True, index=False, encoding='GBK')
    print("Saved to [%s]" % csv_fp)


# Visualize word-time from DTM output
def show_word_times():
    time_slice_path = "%s/data_cleaned-seq.dat" % db_dir
    time_slice = pd.read_table(time_slice_path)
    time_slice = np.asarray(time_slice)
    num_time_slice = len(time_slice)
    num_topics, k_term = 0, 0
    with codecs.open(param_path, 'r', 'utf-8') as pfile:
        for line in pfile:
            if line.startswith("num_topics"):
                num_topics = int(line.strip().split('=')[1])
            if line.startswith("num_words"):
                k_term = int(line.strip().split('=')[1])

    for t in range(num_topics):
        cal_word_times(t, num_time_slice, k_term=k_term)


if __name__ == '__main__':
    param_path = "./setting/model_params.txt"
    db_dir = "./models/db"
    dtm_dir = "./models/dtm"
    result_dir = "./results"
    if not os.path.exists(result_dir):
        os.mkdir(result_dir)

    show_word_times()
