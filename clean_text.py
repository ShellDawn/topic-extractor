# -*- coding:utf-8 -*-
import codecs
import os
import re


class DocInfo:
    def __init__(self):
        self.name = ""
        self.date = ""
        self.publish = ""
        self.title = ""
        self.asc_title = ""


def is_repeat(docs, d):
    flag = False
    old = ""
    new = ""
    for doc in docs:
        if doc.date == d.date and doc.title == d.title:
            flag = True
            old = doc.name
            new = d.name
            return flag, old, new
    return flag, old, new


# Stage 1: Remove repeated documents in data directory
def clean_docs(docs_dir, output_dir):
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    print("Removing repeated documents....")
    docs_info = []
    for root, dirs, files in os.walk(docs_dir):
        for file in files:
            doc_path = os.path.join(root, file)
            doc = codecs.open(doc_path, 'r', 'utf-8')
            d_content = []
            d_info = DocInfo()
            d_info.name = doc_path
            for line in doc:
                if line.startswith("<日期>"):
                    d_info.date = line.split('=')[1]
                elif line.startswith("<版次>"):
                    d_info.publish = line.split('=')[1]
                elif line.startswith("<标题>"):
                    d_info.title = line.split('=')[1]
                elif line.startswith("<副标题>"):
                    d_info.asc_title = line.split('=')[1]
                elif line.startswith('\n') or \
                        line.startswith("<版名>") or \
                        line.startswith("<正文>") or \
                        line.startswith("<作者>") or \
                        line.startswith("<数据库>"):
                    pass
                else:
                    d_content.append(line)

            flag, old, new = is_repeat(docs_info, d_info)
            if not flag:
                docs_info.append(d_info)
                out_file = str(d_info.date[:-1].strip())+'_'+str(d_info.publish[:-1].strip())+\
                           '_'+str(d_info.title.strip()[:2])+'.txt'
                with codecs.open(output_dir+'/'+out_file, 'w', 'utf-8') as out_file:
                    out_file.write(str(d_info.title))
                    out_file.write(str(d_info.asc_title))
                    for content in d_content:
                        out_file.write(content)
            else:
                print("Repeated documents:", old, new)
    print("Finished.\n")


# Stage 2: Clean non Zh-CN characters in documents
def clean_chars(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    print("Cleaning non Zh-CN characters...")
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            doc_path = os.path.join(root, file)
            out_file = output_dir+'/'+file
            fin = codecs.open(doc_path, 'r', 'utf-8')
            fout = codecs.open(out_file, 'w', 'utf-8')
            for line in fin:
                # using range of Zh-CN coding: \u4e00 - \u9fa5
                p2 = re.compile('[^\u4e00-\u9fa5]')
                zh = " ".join(p2.split(line)).strip()
                zh = " ".join(zh.split())
                fout.write(zh.strip() + '\n')
            fin.close()
            fout.close()
    print("Finished.\n")


if __name__ == '__main__':
    docs_dir = "./data"
    stage1_dir = "./cleaned_data/docs"
    stage2_dir = "./cleaned_data/clean_text_out"
    clean_docs(docs_dir, stage1_dir)
    clean_chars(stage1_dir, stage2_dir)
