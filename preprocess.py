#coding: utf8
import os
import os.path
import nltk
import sys
import re
reload(sys)
sys.setdefaultencoding("ISO-8859-1")
def preprocess(raw_article_dir):
    path = raw_article_dir
    if os.path.exists('after_process')==False:
        os.makedirs('after_process')
    for root, dirs, files in os.walk(path):
        for file in files:
            current_file=os.path.join(root, file)
            strr=''
            rf = open(current_file, 'r').read().strip()
            if len(rf) == 0:
                continue
            else:
                pattern = re.compile('[0-9|A-z|.]*@[0-9|A-z|.]*')
                pattern.findall(rf)
                if len(pattern.findall(rf)) > 0:
                    str2 = pattern.findall(rf)[-1]
                    index = rf.rfind(str2) + len(str2) + 1
                    rf = rf[index:]
                elif 'Article' in rf:
                    rf = rf[rf.rfind('Article') + 1:]
                else:
                    rf = rf
                after_process_file = 'after_process/' + file
                sent_list = nltk.sent_tokenize(rf)
                for each in sent_list:
                    token_list = nltk.word_tokenize(each)
                    strr += '\n'.join(token_list)
                    strr += '\n\n'
                wf = open(after_process_file, 'w')
                wf.write(strr)
if __name__ == "__main__":
    preprocess('/test')