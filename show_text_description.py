# -*- coding:utf-8 -*-
import os
import matplotlib.pyplot as plt


# Plot how many samples are computed
def plot_samples(data_dir, figure_dir):
    years = []
    for dirpath, dirnames, filenames in os.walk(data_dir):
        for f in filenames:
            year = int(f.split('.')[0])
            years.append(year)
    years.sort()
    uniq_years = set(years)
    uniq_years = list(uniq_years)
    uniq_years.sort()

    time_window = {}
    for year in years:
        time_window[year] = years.count(year)

    timestaps = list(time_window.keys())
    num_timestap = list(time_window.values())

    plt.rcParams['xtick.direction'] = 'in'
    plt.rcParams['ytick.direction'] = 'in'

    # 设置图片的尺寸
    plt.figure(figsize=(12, 8))

    plt.bar(timestaps, num_timestap, 0.8, color="blue")

    # 设置图片的边距
    plt.subplots_adjust(left=0.08, right=0.95, top=0.95, bottom=0.1)

    # 若要去掉标题，在下面一行代码前面加上#
    plt.title('Samples Description')

    plt.xlabel('Year')
    plt.ylabel('Number')

    plt.savefig('%s/text-description.png' % figure_dir)
    plt.show()


if __name__ == '__main__':
    data_dir = "./cleaned_data/final_out"
    result_dir = "./results"
    if not os.path.exists(result_dir):
        os.mkdir(result_dir)

    plot_samples(data_dir, result_dir)
