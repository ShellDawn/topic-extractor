# -*- coding:utf-8 -*-
import os
import codecs
import pandas as pd


def lda_train():
    corpus_dir = "./cleaned_data/stage_4_out"
    lda_model_dir = "./models/lda"
    param_path = "./setting/model_params.txt"

    if not os.path.exists(lda_model_dir):
        os.mkdir(lda_model_dir)

    corpus = []
    docs = []
    for file in os.listdir(corpus_dir):
        docname = file.split('.txt')[0]
        docs.append(docname)
        doc_path = os.path.join(corpus_dir, file)
        doc = codecs.open(doc_path, 'r', 'utf-8').read()
        corpus.append(doc)

    print("Total documents: ", len(corpus))
    with codecs.open(lda_model_dir + "/" + "corpus.dat", 'w', 'utf-8') as datfile:
        datfile.write(str(len(corpus)) + '\n')
        for doc in corpus:
            datfile.write(doc + '\n')

    # get parameters from setting file
    with codecs.open(param_path, 'r', 'utf-8') as pfile:
        for line in pfile:
            if line.startswith("alpha"):
                alpha = line.split('=')[1].strip()
            elif line.startswith("beta"):
                beta = line.split('=')[1].strip()
            elif line.startswith('topics'):
                topic = line.split('=')[1].strip()
            elif line.startswith('niters'):
                niters = line.split('=')[1].strip()
            elif line.startswith('twords'):
                twords = line.split('=')[1].strip()

    # call external C++ exe to run LDA topic model
    print("Training LDA model with", topic, "topics...")
    os.chdir("./lib/GibbsLDA++/bin")
    dfile = "../../../models/lda/corpus.dat"
    params = "-alpha " + str(alpha) + " -beta " + str(beta) + " -ntopics " + str(topic) \
             + " -niters " + str(niters) + " -savestep " + str(niters) + " -twords " + str(twords) \
             + " -treval 1" + " -dfile " + str(dfile)
    os.system("lda.exe -est " + params)
    os.chdir("../../../")
    print("Training finished.")

    return topic, docs


def save_doc_topic(ntopic, docs):
    theta_path = './models/lda/model-final.theta'
    save_file = './models/db/doc_topic.csv'

    theta = pd.read_table(theta_path, delimiter=' ', header=None)
    theta = pd.DataFrame(theta)
    docs = pd.Series(docs)
    topics = []
    for i in range(int(ntopic)):
        t = 'topic_'+str(i)
        topics.append(t)
    topics.append('NAN')
    topics.insert(0, 'doc')

    doc_topic = pd.concat([docs, theta], axis=1)
    doc_topic.columns = topics
    doc_topic.drop(['NAN'], axis=1, inplace=True)
    doc_topic.to_csv(save_file, header=True, index=False, encoding='GBK')
    print("Doc-Topic is saved:", save_file)


if __name__ == '__main__':
    ntopic, docs = lda_train()
    save_doc_topic(ntopic, docs)