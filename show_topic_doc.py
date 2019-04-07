# -*- coding:utf-8 -*-
import os
import codecs
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties


# Show topic-documents matrix from DTM output
def show_topic_docs():
    gam_file_path = "%s/lda-seq/gam.dat" % dtm_dir
    dmap_file_path = "%s/cleaned_data.dmap" % db_dir
    out_file = "%s/topic_docs.csv" % db_dir

    num_topics, k_term = 0, 0
    with codecs.open(param_path, 'r', 'utf-8') as pfile:
        for line in pfile:
            if line.startswith("num_topics"):
                num_topics = int(line.strip().split('=')[1])
            elif line.startswith("num_docs"):
                k_term = int(line.strip().split('=')[1])
    doc_name = []
    with codecs.open(dmap_file_path, 'r', 'utf-8') as dfile:
        for line in dfile:
            doc_name.append(line.strip().split('\\')[1])

    gammas = pd.read_table(gam_file_path, header=None)
    gammas = np.array(gammas)
    gammas = gammas.reshape((-1, num_topics))
    results = []
    for t in range(num_topics):
        dw = gammas[:, t]/sum(gammas[:, t])
        sort_dw = sorted(dw, reverse=True)
        d = []
        for i in range(k_term):
            top_k = sort_dw[i]
            index = np.where(dw == top_k)
            index = int(index[0])
            dn = doc_name[index].strip()
            dn += " "+str(top_k)
            d.append(dn)
        results.append(d)
    # write results to csv
    df = pd.DataFrame(results)
    df_T = df.T
    df_T.columns = list(range(num_topics))
    df_T.to_csv(out_file, index=False, header=True, encoding='GBK')

    # visualizing topic-docs
    # 设置图例字体大小(主题数目<10时的情况)
    font = FontProperties(fname='C:\Windows\Fonts\msyh.ttc', size=10)

    # 设置坐标轴标签的字体大小，即修改'size'的值
    font2 = {'weight': 'normal', 'size': 10}

    for t in range(num_topics):
        data = df_T.ix[:, t]
        x_var = list(data.apply(lambda x: float(x.strip().split(" ")[1])))
        x_var.reverse()
        y_var = list(data.apply(lambda x: x.strip().split(" ")[0]))
        y_var.reverse()
        print("x_var\n", x_var)
        print("y_var\n", y_var)
        idx = np.arange(len(x_var))
        plt.rcParams['xtick.direction'] = 'in'
        plt.rcParams['ytick.direction'] = 'in'

        # 设置图片尺寸
        plt.figure(figsize=(12, 8))

        plt.barh(idx, x_var)
        plt.yticks(idx, y_var, fontproperties=font)
        plt.grid(axis='x')
        plt.xlabel("Weight")
        plt.ylabel("Document")

        # 设置图片的边距
        plt.subplots_adjust(left=0.2, right=0.95, top=0.95, bottom=0.1)

        # 设置坐标轴刻度值的字体大小，即修改labelsize的值
        plt.tick_params(labelsize=10)

        # 若不显示标题，则在下面这行代码前面加上#
        plt.title("Topic "+str(t))

        save_file = "%s/topic-%d-docs.png" % (result_dir, t)
        plt.savefig(save_file)
        plt.show()


if __name__ == '__main__':
    param_path = "./setting/model_params.txt"
    db_dir = "./models/db"
    dtm_dir = "./models/dtm"
    result_dir = "./results"
    if not os.path.exists(result_dir):
        os.mkdir(result_dir)

    show_topic_docs()