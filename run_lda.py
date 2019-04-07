# -*- coding:utf-8 -*-
import os
import codecs
import shutil
import random
from text2ldac import gen_ldac_corpus


# Divide cleaned data into training data and test data
def divide_corpus(data_dir, lda_model_dir):
    if not os.path.exists(lda_model_dir):
        os.mkdir(lda_model_dir)

    corpus = []
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            doc_path = os.path.join(root, file)
            doc = codecs.open(doc_path, 'r', 'utf-8').read()
            corpus.append(doc)
    print("Total documents: ", len(corpus))

    random.shuffle(corpus)
    p = int(len(corpus)*0.9)
    train = corpus[:p]
    test = corpus[p:]

    with codecs.open(lda_model_dir+"/"+"corpus_train.dat", 'w', 'utf-8') as datfile:
        datfile.write(str(len(train)) + '\n')
        for doc in train:
            datfile.write(doc + '\n')
    with codecs.open(lda_model_dir+"/"+"corpus_test.dat", 'w', 'utf-8') as testfile:
        testfile.write(str(len(test)) + '\n')
        for doc in test:
            testfile.write(doc + '\n')
    print("Train documents: ", len(train))
    print("Test documents: ", len(test))


# Run LDA model with Gibbs sampling
def lda_train(lda_dir, params_path):
    # default settings
    alpha = 0.25
    beta = 0.1
    topic_list = []
    twords = 10
    # get parameters from setting file
    with codecs.open(params_path, 'r', 'utf-8') as pfile:
        for line in pfile:
            if line.startswith("alpha"):
                alpha = line.split('=')[1].strip()
            elif line.startswith("beta"):
                beta = line.split('=')[1].strip()
            elif line.startswith('ntopics'):
                topics = line.split('=')[1].strip()
                topic_list = topics.split()
            elif line.startswith('twords'):
                twords = line.split('=')[1].strip()

    for topic in topic_list:
        # create dirs for LDA model output
        model_dir = lda_dir + "/topic-" + str(topic)
        if not os.path.exists(model_dir):
            os.mkdir(model_dir)
        train_file = model_dir + "/corpus_train.dat"
        test_file = model_dir + "/corpus_test.dat"
        if not os.path.exists(train_file):
            shutil.copyfile(lda_dir + "/corpus_train.dat", train_file)
        if not os.path.exists(test_file):
            shutil.copyfile(lda_dir + "/corpus_test.dat", test_file)

        # call external C++ exe to run LDA topic model
        print("Training LDA model with %s topics..." % topic)
        params = "-alpha %s -beta %s -ntopics %s -niters 20 -savestep 20 -twords %s -treval 1 -dfile %s" % (
            alpha, beta, topic, twords, train_file)
        cmds = "lda.exe -est " + params
        print(cmds)
        os.system(cmds)
        print("Done.")

    print("All training finished.")


# Using trained model to do inference on test set
def lda_inference(lda_dir, params_path):
    # default settings
    topic_list = []
    twords = 10
    # get parameters from setting file
    with codecs.open(params_path, 'r', 'utf-8') as pfile:
        for line in pfile:
            if line.startswith('ntopics'):
                topics = line.split('=')[1].strip()
                topic_list = topics.split()
            elif line.startswith('twords'):
                twords = line.split('=')[1].strip()

    for topic in topic_list:
        # call external C++ exe to run LDA inference
        print("Inference on test set with %s topics..." % topic)
        model_dir = lda_dir + "/topic-" + str(topic)
        test_file = model_dir + "/corpus_test.dat"
        params = "-dir %s -model model-final -niters 20 -twords %s -treval 1 -teval 1 -dfile %s" % (
            model_dir, twords, test_file)
        os.system("lda.exe -inf " + params)

    print("Inference finished.")


if __name__ == '__main__':
    params_path = "./setting/model_params.txt"
    data_dir = "./cleaned_data/final_out"
    lda_dir = "./models/lda"
    db_dir = "./models/db"

    divide_corpus(data_dir, lda_dir)

    print("Generating train/test data for LDA training...")
    gen_ldac_corpus(data_dir, db_dir)

    lda_train(lda_dir, params_path)
    lda_inference(lda_dir, params_path)


