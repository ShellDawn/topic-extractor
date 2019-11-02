# Topic extractor

#### 环境配置
* Python3
* matplotlib
* numpy
* pandas
* jieba
* R >= 3.4


#### 目录文件说明

    1. [data]：存放原始的数据集(1949-2017年部分人民日报语料).
    
    2. [data_cleaned]：该目录由程序自动生成，用于存放数据预处理阶段生成的文件，程序运行会逐步生成一系列子文件夹与文件.其中[docs]子文件夹存放去除原始数据集中重复文档后的结果，[clean_text_out]子文件存放去除文档中非中文字符后的结果，[tokenize_out]子文件夹存放分词及去掉停用词后的结果，[final_out]子文件夹存放去掉整个语料库中的高频词低频词后的结果，'vocab-tf.txt'记录词频(TF)，'vocab-df.txt'记录词的文档频率(DF).
    
    3. [models]：该目录由程序自动生成，包含3个子目录，其中[db]目录为模型可视化所需的数据文件，[lda]目录为LDA模型的原始输出文件，[dtm]目录为DTM模型的原始输出文件.
    
    4. [results]：该目录由程序自动生成，用于存放最终的可视化图片结果.
    
    5. [scripts]：存放Python与R脚本代码，以及LDA和DTM模型的C++代码.
    
    5. [setting]：存放设置参数的文件.其中'model_params.txt'定义主题模型的参数以及定义高频词低频词的频度阈值，'stop_words.txt'定义停用词表，'synonyms_words.txt'定义同义词表，'user_defined_dicts.txt'设置用户自定义的词典.


#### 程序运行说明

    [1] 去掉重复文档和非中文文本部分：运行[clean_text.bat]即可，生成结果在data_cleaned/clean_text_out.
    
    [2] 进行中文分词并去除停用词：对setting目录下的3个文件(用户自定义词表user_defined_dicts.txt、停用词表stop_words.txt、同义词表synonyms_words.txt）进行设置，然后运行[tokenize_word.bat]即可，生成结果在data_cleaned/tokenize_out.
    
    [3] 去除高频低频词操作：对setting/model_params.txt文件的low_frequency_threshold参数和high_frequency_threshold参数进行设置，然后运行[remove_lh_word.bat]即可.
    
    [4] 显示样本数量随时间变化的曲线：运行[show_text_description.bat]即可.
    
    [5] 运行LDA模型：对setting/model_params.txt文件的LDA部分的参数进行设置，然后运行[run_lda.bat]即可.
    
    [6] 显示perplexity随主题数变化的曲线：运行[show_perplexity.bat]即可.
    
    [7] 运行DTM模型：对setting/model_params.txt文件的DTM部分的参数进行设置，然后运行[run_dtm.bat]即可.
    
    [8] 获取文档-主题权重分布的结果：运行[save_doc_topic.bat]即可.
    
    [9] 显示不同主题对应的文档关联度的曲线：运行[show_topic_doc.bat]即可.
    
    [10] 显示不同主题下的词随时间变化的曲线：运行[show_word_time.bat]即可.
    
    [11] 显示主题随时间变化(包含其标准差)的曲线：对setting/model_params.txt文件的具体topic进行手动设置，以便于在曲线图中进行显示，然后运行[show_topic_time.bat]即可.
    
    [12] 显示不同主题的structural change曲线图：运行[show_structural_change.bat]即可.

#### 参考资料
  [1] [GibbsLDA++: A C/C++ Implementation of Latent Dirichlet Allocation](http://gibbslda.sourceforge.net/) \
  [2] [Dynamic Topic Models (DTM)](https://github.com/blei-lab/dtm) \
  [3] [strucchange: An R Package for Testing for Structural Change in Linear Regression Models](https://cran.r-project.org/web/packages/strucchange/vignettes/strucchange-intro.pdf)
  