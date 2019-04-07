# -*- coding:utf-8 -*-
import os
import codecs


# generate time slice file
def set_time_window(param_path, data_dir, db_dir):
    # get parameters from setting file
    time_interval = 1
    with codecs.open(param_path, 'r', 'utf-8') as pfile:
        for line in pfile:
            if line.startswith("time"):
                time_interval = int(line.split('=')[1])
    years = []
    for dirpath, dirnames, filenames in os.walk(data_dir):
        for f in filenames:
            year = int(f.split('.')[0])
            years.append(year)
    years.sort()
    uniq_years = set(years)
    uniq_years = list(uniq_years)
    uniq_years.sort()

    time_out_filename = "%s/time-seq.txt" % db_dir
    with codecs.open(time_out_filename, 'w', 'utf-8') as tfile:
        for y in uniq_years:
            tfile.write(str(y) + '\n')

    time_window = {}
    if time_interval == 1:
        for year in years:
            time_window[year] = years.count(year)
    elif time_interval >= 2:
        start = years[0]
        end = years[-1]
        tstap = 1
        current = start
        if end-start < time_interval:
            time_window[tstap] = len(years)
        else:
            while current <= end:
                time_window[tstap] = 0
                for i in range(time_interval):
                    time_window[tstap] += years.count(current)
                    current += 1
                tstap += 1
    number_timestaps = len(time_window)
    # timestaps = time_window.keys()
    num_timestap = time_window.values()

    out_filename = "%s/cleaned_data-seq.dat" % db_dir
    with codecs.open(out_filename, 'w', 'utf-8') as out_file:
        out_file.write(str(number_timestaps) + '\n')
        for num in num_timestap:
            out_file.writelines(str(num) + '\n')


# Run Dynamic Topic Model(DTM)
def dtm_train(db_dir, param_path, output_dir):
    corpus_prefix = "%s/cleaned_data" % db_dir
    ntopics = 0
    # get parameters from setting file
    with codecs.open(param_path, 'r', 'utf-8') as pfile:
        for line in pfile:
            if line.startswith("num_topics"):
                ntopics = line.strip().split('=')[1]

    # call external C++ exe to run
    params = "--ntopics=%s --mode=fit --rng_seed=0 --initialize_lda=true --corpus_prefix=%s --outname=%s " \
             "--top_chain_var=0.005 --alpha=0.01 --lda_sequence_min_iter=6" \
             " --lda_sequence_max_iter=20 --lda_max_em_iter=6" % (ntopics, corpus_prefix, output_dir)
    os.system("dtm-win32.exe "+params)


if __name__ == '__main__':
    param_path = "./setting/model_params.txt"
    data_dir = "./cleaned_data/final_out"
    db_dir = "./models/db"
    output_dir = "./models/dtm"

    set_time_window(param_path, data_dir, db_dir)

    dtm_train(db_dir, param_path, output_dir)
