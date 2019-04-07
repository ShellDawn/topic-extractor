# -*- coding:utf-8 -*-
import os
import codecs
import pandas as pd


# Run LDA model with Gibbs sampling
def lda_train_best():
    corpus = []
    docs = []
    for file in os.listdir(data_dir):
        docname = file.split('.txt')[0]
        docs.append(docname)
        doc_path = os.path.join(data_dir, file)
        doc = codecs.open(doc_path, 'r', 'utf-8').read()
        corpus.append(doc)
    print("Total documents: ", len(corpus))

    corpus_dat = "%s/corpus.dat" % lda_dir
    with codecs.open(corpus_dat, 'w', 'utf-8') as datfile:
        datfile.write(str(len(corpus)) + '\n')
        for doc in corpus:
            datfile.write(doc + '\n')

    # default settings
    alpha = 0.25
    beta = 0.1
    best_topic = 0
    twords = 10
    # get parameters from setting file
    with codecs.open(params_path, 'r', 'utf-8') as pfile:
        for line in pfile:
            if line.startswith("alpha"):
                alpha = line.split('=')[1].strip()
            elif line.startswith("beta"):
                beta = line.split('=')[1].strip()
            elif line.startswith('num_topics'):
                best_topic = line.split('=')[1].strip()
            elif line.startswith('twords'):
                twords = line.split('=')[1].strip()

    # call external C++ exe to run LDA topic model
    print("Training LDA model with %s topics..." % best_topic)
    params = "-alpha %s -beta %s -ntopics %s -niters 20 -savestep 20 -twords %s -treval 1 -dfile %s" % (
        alpha, beta, best_topic, twords, corpus_dat)
    cmds = "lda.exe -est " + params
    print(cmds)
    os.system(cmds)
    print("Done.")
    return best_topic, docs


def save_doc_topic(ntopic, docs):
    theta_path = '%s/model-final.theta' % lda_dir
    save_file = '%s/doc_topic.csv' % db_dir

    theta = pd.read_table(theta_path, delimiter=' ', header=None)
    theta = pd.DataFrame(theta)
    docs = pd.Series(docs)
    topics = []
    for i in range(int(ntopic)):
        t = 'topic-'+str(i)
        topics.append(t)
    topics.append('NAN')
    topics.insert(0, 'doc')

    doc_topic = pd.concat([docs, theta], axis=1)
    doc_topic.columns = topics
    doc_topic.drop(['NAN'], axis=1, inplace=True)
    doc_topic.to_csv(save_file, header=True, index=False, encoding='GBK')
    print("Doc-Topic is saved: ", save_file)


if __name__ == '__main__':
    params_path = "./setting/model_params.txt"
    data_dir = "./cleaned_data/final_out"
    lda_dir = "./models/lda"
    db_dir = "./models/db"

    num_topic, docs = lda_train_best()
    save_doc_topic(num_topic, docs)
