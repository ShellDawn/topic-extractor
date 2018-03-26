# Topic extractor


## 目录文件说明

1.[Data]目录：原始的数据集。

2.[cleaned_data]目录：数据预处理阶段生成的文件，程序运行会逐步生成4个子文件夹和1个'temp_dicts.txt'。其中[stage_1_out]子文件夹存放去除原始数据集中重复文档后的文档，[stage_2_out]子文件存放去除文档中非中文字符后的结果，[stage_3_out]子文件夹存放分词及去掉停用词后的结果，[stage_4_out]子文件夹存放去掉整个语料库中的高频词低频词后的结果，'temp_dicts.txt'存放的是去掉分词及停用词后的所有非重复的词。

3.[lib]目录：LDA和DTM模型的C++源码及可执行程序文件。

4.[models]目录：包含3个子目录，其中[db]目录为DTM模型的输入文件及进行可视化制图所需的结果文件，[lda]目录为LDA模型的原始输出文件，[dtm]目录为DTM模型的原始输出文件。

5.[setting]目录：存放设置参数的文件。其中'model_params.txt'定义主题模型的参数以及定义高频词低频词的频度阈值，'stop_words.txt'定义停用词表，'synonyms_words.txt'定义同义词表，'user_defined_dicts.txt'设置用户自定义的词典。

6.[Figures]目录：存放最终的可视化图片结果。

## 程序运行说明

通过设置main.py中参数step的值来选择所要运行的程序段，各数值的含义如下：

[1] 去掉重复文档：生成结果在cleaned_data目录下的stage_1_out子文件夹中。

[2] 去重非中文文本部分：生成结果在cleaned_data目录下的stage_2_out子文件夹中。

[3] 分词并去除停用词操作：生成结果在cleaned_data目录下的stage_3_out子文件夹中，涉及setting目录下的3个文件(用户自定义词表user_defined_dicts.txt、停用词表stop_words.txt、同义词表synonyms_words.txt）。

[4] 去除高频低频词操作(运行约2h)：生成结果在cleaned_data目录下的stage_4_out子文件夹及temp_dicts.txt，涉及setting目录下model_params.txt文件的low_frequency_threshold参数和high_frequency_threshold参数设置。

[5] 显示样本数量随时间变化的曲线，运行结果保存在Figures目录下。

[6] 运行LDA并显示主题数的困惑度曲线(运行约1h)：涉及setting目录下model_params.txt文件的LDA部分的ntopics参数设置，运行结果保存在Figures目录下。

[7] 运行动态主题模型DTM(运行约2h)：涉及setting目录下model_params.txt文件的DTM部分的topics、words参数设置。

[8] 显示不同主题下的词随时间变化的曲线，运行结果保存在Figures目录下。

[9] 显示不同主题对应的文档关联度的曲线，运行结果保存在Figures目录下。

[10] 显示主题随时间变化(包含其标准差)的曲线：涉及setting目录下model_params.txt文件的DTM部分的具体topic的手动设置，以便于在曲线图中进行显示，运行结果保存在Figures目录下。

[11] 显示不同主题的structual change曲线图，运行结果保存在Figures目录下。

「注意」
(1)上述[1]-[7]的操作有严格的先后顺序，即每一步的执行必须要确保前面的步骤已经执行完毕！
(2)在运行第[6]步之前记住要在setting目录下model_params.txt文件的DTM部分进行具体topic的手动设置！
