# Topic extractor

### 环境配置
* Windows
* Python3
* matplotlib
* pandas
* R


### 目录文件说明

    1. [data]目录：存放原始的数据集(1949-2017年部分人民日报语料)。
    
    2. [cleaned_data]目录：该目录由程序自动生成，用于存放数据预处理阶段生成的文件，程序运行会逐步生成一系列子文件夹与文件。其中[docs]子文件夹存放去除原始数据集中重复文档后的结果，[clean_text_out]子文件存放去除文档中非中文字符后的结果，[tokenize_out]子文件夹存放分词及去掉停用词后的结果，[final_out]子文件夹存放去掉整个语料库中的高频词低频词后的结果，'vocab.txt'存放的是去掉分词及停用词后的所有非重复的词。
    
    3. [models]目录：该目录由程序自动生成，包含3个子目录，其中[db]目录为DTM模型的输入文件及进行可视化制图所需的结果文件，[lda]目录为LDA模型的原始输出文件，[dtm]目录为DTM模型的原始输出文件。
    
    4. [results]目录：该目录由程序自动生成，用于存放最终的可视化图片结果。
    
    5. [setting]目录：存放设置参数的文件。其中'model_params.txt'定义主题模型的参数以及定义高频词低频词的频度阈值，'stop_words.txt'定义停用词表，'synonyms_words.txt'定义同义词表，'user_defined_dicts.txt'设置用户自定义的词典。


### 程序运行说明

    [1] 去掉重复文档和非中文文本部分：双击【1.clean_text.bat】即可，生成结果在cleaned_data/clean_text_out。
    
    [2] 进行中文分词并去除停用词：对setting目录下的3个文件(用户自定义词表user_defined_dicts.txt、停用词表stop_words.txt、同义词表synonyms_words.txt）进行设置，然后双击【2.tokenize_word.bat】即可，生成结果在cleaned_data/tokenize_out。
    
    [3] 去除高频低频词操作：对setting/model_params.txt文件的low_frequency_threshold参数和high_frequency_threshold参数进行设置，然后双击【3.remove_lh_word.bat】即可，生成结果在cleaned_data/final_out和cleaned_data/vocab.txt。
    
    [4] 显示样本数量随时间变化的曲线：双击【4.show_text_description.bat】即可，运行结果保存在results/text-description.png。
    
    [5] 运行LDA模型：对setting/model_params.txt文件的LDA部分的参数进行设置，然后双击【5.run_lda.bat】即可，程序生成结果在models/lda。
    
    [6] 显示主题数的困惑度曲线：双击【6.show_perplexity.bat】即可，运行结果保存在results/perplexity.png。
    
    [7] 运行DTM模型：对setting/model_params.txt文件的DTM部分的参数进行设置，然后双击【7.run_dtm.bat】即可，程序生成结果在models/dtm。
    
    [8] 显示不同主题下的词随时间变化的曲线：双击【8.show_word_time.bat】即可，运行结果保存在models/db/word-times_topic-xx.csv和results/word-times_topic-xx.png。
    
    [9] 显示不同主题对应的文档关联度的曲线：双击【8.show_topic_doc.bat】即可，运行结果保存在models/db/topic_docs.csv和results/topic-xx-docs.png。
    
    [10] 显示主题随时间变化(包含其标准差)的曲线：对setting/model_params.txt文件的具体topic进行手动设置，以便于在曲线图中进行显示，然后双击【8.show_topic_time.bat】即可，运行结果保存在models/db/topic_times.csv和results/topic-time.png。
    
    [11] 显示不同主题的structural change曲线图：双击【8.show_structural_change.bat】即可，运行结果保存在results/strucchange_topicxxx.svg、topic_time_std_strucchange.svg、word_time_std_strucchange_topicxx.svg。
    
    [12] 获取文档-主题权重分布的结果：双击【8.save_doc_topic.bat】即可，运行结果保存在models/db/doc_topic.csv。