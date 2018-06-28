#!/usr/bin/python
# -*- coding: utf-8 -*-
import text2ldac
import doc2lda
import preprocessing as pre
import lda
import dtm


# 'step' is set to run corresponding step
step = 1

if step == 1:
    # Stage 1
    pre.clean_docs()
elif step == 2:
    # Stage 2
    pre.clean_chars()
elif step == 3:
    # Stage 3
    pre.participle()
elif step == 4:
    # Stage 4
    pre.remove_lh_words()
elif step == 5:
    # Plot how many samples are computed
    pre.plot_samples()
elif step == 6:
    # Generate train/test data
    lda.divide_corpus()
    text2ldac.gen_ldac_corpus()
elif step == 7:
    # Run LDA model with Gibbs sampling
    lda.lda_estimate()
    # Using trained model to do inference on test set
    lda.lda_inference()
elif step == 8:
    # Plot "perplexity" to "number of topics" of LDA according to model results
    lda.plot_perplexity()
elif step == 9:
    # Run Dynamic Topic Model(DTM)
    dtm.dtm_estimate()
elif step == 10:
    # Visualize word-time from DTM output
    dtm.show_word_times()
elif step == 11:
    # Visualize topic-doc from DTM output
    dtm.show_topic_docs()
elif step == 12:
    # Visualize topic-time from DTM output
    dtm.cal_topic_times()
elif step == 13:
    # Visualize structual-changes of topic to times
    dtm.cal_strucchange()
elif step == 14:
    # Output doc-topic result
    ntopic, docs = doc2lda.lda_train()
    doc2lda.save_doc_topic(ntopic, docs)