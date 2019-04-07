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
    vocab_file_path = "%s/cleaned_data.vocab" % db_dir
    outfile_prefix = "%s/word-times_topic-%d" % (db_dir, topic_no)
    figfile_prefix = "%s/word-times_topic-%d" % (result_dir, topic_no)

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

    # visualizing terms-times in topic "topic_no"
    date_list = []
    plt.rcParams['xtick.direction'] = 'in'
    plt.rcParams['ytick.direction'] = 'in'
    with codecs.open(time_file_path, 'r', 'utf-8') as tfile:
        for line in tfile:
            date_list.append(int(line.strip()))
    if k_term <= 20:
        # 设置图例字体大小(主题数目<=20时的情况)
        font = FontProperties(fname='C:\Windows\Fonts\msyh.ttc', size=10)
    elif k_term > 20:
        # 设置图例字体大小(主题数目>20时的情况)
        font = FontProperties(fname='C:\Windows\Fonts\msyh.ttc', size=8)

    colors = ["red", "blue", "black", "orange", "purple", "green", "magenta", "cyan", "yellow", "gray"]
    markers = ['+', '.', '*']
    color_index = 0
    marker_index = 0

    # 设置图片的尺寸
    fig, ax = plt.subplots(figsize=(12, 8))

    # 设置坐标轴标签的字体大小，即修改'size'的值
    font2 = {'weight': 'normal', 'size': 10}

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

    ###########################################################################
    # 若不显示均值线与标准差线，将下面这部分代码行前后分别用'''注释掉
    '''
    right_axis = ax.twinx()
    right_axis.plot(date_list, df_mean, marker=".", linestyle="-", label="Mean", color="black", linewidth=1.5)
    right_axis.plot(date_list, df_std, marker="|", linestyle="-", label="Standard deviation", color="black", linewidth=1.5)
    right_axis.legend(prop=font, loc='upper center', bbox_to_anchor=(0.9, 0.8))
    right_axis.set_ylabel("Mean & Standard deviation", fontdict=font2)
    '''
    ###########################################################################

    # 若不显示标题，则在下面这行代码前面加上#
    plt.title("Topic" + str(topic_no))

    # 设置坐标轴标签的字体大小，即修改'size'的值
    font2 = {'weight': 'normal', 'size': 10}
    ax.set_xlabel(xlabel="Year", fontdict=font2)
    ax.set_ylabel(ylabel="Probability", fontdict=font2)

    # 设置坐标轴刻度值的字体大小，即修改labelsize的值
    plt.tick_params(labelsize=10)

    # 设置图片的边距
    fig.subplots_adjust(left=0.08, right=0.93, top=0.95, bottom=0.1)

    plt.savefig(figfile_prefix + '.png')
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
    y_res.to_csv(outfile_prefix + '.csv', header=True, index=False, encoding='GBK')


# Visualize word-time from DTM output
def show_word_times():
    time_slice_path = "%s/cleaned_data-seq.dat" % db_dir
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
