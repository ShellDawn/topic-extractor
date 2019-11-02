# -*- coding:utf-8 -*-
import os
import codecs
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties


# Show topic-time matrix from DTM output
def show_topic_times(param_fp, db_dirs, dtm_dirs, result_dirs):
    timeslice_file_path = "%s/data_cleaned-seq.dat" % db_dirs
    time_file_path = "%s/time-seq.txt" % db_dirs
    gam_file_path = "%s/lda-seq/gam.dat" % dtm_dirs

    # get parameters from setting file
    num_topics = 0
    topics = dict()
    with codecs.open(param_fp, 'r', 'utf-8') as pfile:
        for line in pfile:
            if line.startswith("num_topics"):
                num_topics = int(line.strip().split('=')[1])
            elif line.startswith("topic"):
                topics[int(line.strip().split('=')[0][5:])] = line.strip().split('=')[1]

    # read gamma file
    gammas = pd.read_table(gam_file_path, header=None)
    gammas = np.array(gammas)
    gammas = gammas.reshape((-1, num_topics))
    gammas = pd.DataFrame(gammas)
    time_slice = pd.read_table(timeslice_file_path)
    time_slice = np.asarray(time_slice)
    num_time_slice = len(time_slice)

    # get date list from time seq file
    date_list = []
    with codecs.open(time_file_path, 'r', 'utf-8') as tfile:
        for line in tfile:
            date_list.append(int(line.strip()))

    # save topic-time matrix
    gam_sum = np.zeros((num_time_slice, num_topics))
    row_i = 0
    for i in range(num_time_slice):
        gam_year = gammas.iloc[row_i:row_i+time_slice[i][0]]
        gam_sum[i, :] = gam_year.apply(lambda x: x.sum(), axis=0)
        row_i = row_i + time_slice[i][0]
    gam_sum = pd.DataFrame(gam_sum)
    gam_sum['sum'] = gam_sum.apply(lambda x: x.sum(), axis=1)
    for i in range(num_time_slice):
        sum_value = gam_sum.ix[i][-1]
        gam_sum.ix[i, :-1] = gam_sum.ix[i, :-1].apply(lambda x: x/sum_value)
    result = gam_sum.ix[:, :-1]

    if len(topics) != len(result.ix[0, :]):
        print("There are totally %d topics need to be named! Please manually set each name of topic in [%s]!"
              % (len(result.ix[0, :]), param_fp))
        return

    # set direction of X, Y axis
    plt.rcParams['xtick.direction'] = 'in'
    plt.rcParams['ytick.direction'] = 'in'

    # set font size
    if num_topics < 10:
        font = FontProperties(fname='C:\Windows\Fonts\msyh.ttc', size=10)
    elif num_topics >= 10:
        font = FontProperties(fname='C:\Windows\Fonts\msyh.ttc', size=9)

    # set figure size
    fig, left_axis = plt.subplots(figsize=(12, 8))
    right_axis = left_axis.twinx()

    colors = ["red", "blue", "black", "orange", "purple", "green", "magenta", "cyan", "yellow", "gray"]
    markers = ['o', '*',  '.']
    color_index = 0
    marker_index = 0

    '''
    # draw box line diagram
    
    topic_time = result
    label = ["" for i in range(len(date_list))]
    for i in range(0, len(date_list), 5):
        label[i] = date_list[i]
    bp = right_axis.boxplot(topic_time, labels=label)
    print(bp['fliers'][0].get_ydata())
    '''

    print("Topics:")
    for (k, v) in topics.items():
        print(k, ":", v)
        legend_name = v
        left_axis.scatter(date_list, result.ix[:, k], marker=markers[marker_index],
                          label=legend_name, color=colors[color_index], linewidths=1)
        color_index += 1
        color_index = color_index % 10
        if color_index == 0:
            marker_index = (marker_index+1) % 3
    if num_topics <= 10:
        ncol = 1
    elif num_topics <= 20:
        ncol = 2
    else:
        ncol = 3

    # set font size of labels on X, Y axis
    font2 = {'weight': 'normal', 'size': 10}

    left_axis.legend(prop=font, bbox_to_anchor=(0.95, 0.85), ncol=ncol)
    left_axis.set_ylabel("Relative weight", fontdict=font2)
    left_axis.set_xlabel("Year", fontdict=font2)

    topic_time = result
    title = 'topic_'
    topic_time.columns = [title + str(i) for i in range(num_topics)]
    topic_time['mean'] = topic_time.apply(lambda x: np.mean(x), axis=1)
    topic_time['std'] = topic_time.apply(lambda x: np.std(x), axis=1)
    topic_time.index = date_list

    # show Mean line
    y2 = topic_time['mean']
    right_axis.plot(date_list, y2, linestyle="--", label="Mean", color="black", linewidth=1)

    # show Std. line
    y3 = topic_time['std']
    right_axis.plot(date_list, y3, marker="+", label="Standard deviation", color="black", linewidth=1)

    right_axis.legend(prop=font, bbox_to_anchor=(0.95, 0.95))
    right_axis.set_ylabel("Mean & Standard deviation", fontdict=font2)

    # set font size of X, Y axis
    plt.tick_params(labelsize=10)

    # set margin
    plt.subplots_adjust(left=0.08, right=0.92, top=0.92, bottom=0.08)

    # saved files and figs
    save_file = "%s/topic-time.png" % result_dirs
    out_file = "%s/topic_times.csv" % db_dirs
    topic_time.to_csv(out_file, header=True, index=True)
    plt.savefig(save_file)
    plt.show()
    print("Saved topic-time table in [%s]" % out_file)
    print("Saved topic-time figure in [%s]" % save_file)


if __name__ == '__main__':
    param_path = "./setting/model_params.txt"
    db_dir = "./models/db"
    dtm_dir = "./models/dtm"
    result_dir = "./results"
    if not os.path.exists(result_dir):
        os.mkdir(result_dir)

    show_topic_times(param_path, db_dir, dtm_dir, result_dir)
