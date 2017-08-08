#coding: utf8
import os
import os.path
import nltk
import preprocess
import features_extract
import sys
reload(sys)
sys.setdefaultencoding("ISO-8859-1")
print('please input the folder or file path you want to be named entity recognition ')
dir=raw_input()
preprocess.preprocess(dir)
feature_name_list = ['token', 'CapWord', 'AllCaps', 'CapsMix', 'AlphaDigitMix', 'AlphaDigit', 'Hyphen', 'InitHyphen', \
                         'EndHyphen', 'Punctuation', 'Quote', 'GreekLetter', 'UpperLetter', 'Numeral', 'TwoNumeral','ContainSlaslT', \
                         'LeftMarkChar', 'RightMarkChar','EndDot','OneOrTwoLetter','AllDigit','Equal','Underline','Plus','word_length',\
                         'keywords_feature', 'prefix3', 'prefix4', 'suffix3', 'suffix4', 'morph', \
                         's_morph', 'left_boundary', 'right_boundary', 'Unary_feature', 'Nested_feature', 'StopWord_feature', \
                         'CommenWord_feature', 'Context_feature', 'POS_feature', 'dict', 'dict_U', 'dict_N']
table_dict= features_extract.get_table_content('table\\')

def function(inputFileName,outputFileName1,outputFileName2):
    global characterNumberBegin
    inputFile = open(inputFileName)
    outputFile1 = open(outputFileName1,"w")
    outputFile2 = open(outputFileName2,"w")
    sentenceNumber=1
    characterNumber=0
    flag1=1
    flag2=0

    characterBegin=0
    characterEnd=0
    characterFlag=0
    words=''
    while True:
        line = inputFile.readline()
        lineList=line.strip('\n').split("	")

        if not line:
            break
        if len(lineList)==1:
            if flag2==1:
                flag2=0
                characterEnd=characterNumberEnd
                outputFile2.write(str(sentenceNumber)+"|"+str(characterBegin)+" "+str(characterEnd)+"|"+words[characterBegin:characterEnd]+"\n")
            outputFile1.write(str(sentenceNumber)+"	"+words+'\n')
            sentenceNumber+=1
            characterNumberEnd=0
            characterNumberBegin=0

            words=''
            flag1=1
        else:
            if flag2==0:
                if lineList[-1]=="B-bacteria":
                    flag2=1
                    characterBegin=characterNumberBegin
                else:
                    flag2=0
            elif flag2==1:
                if lineList[-1]=="B-bacteria":
                    flag2=1
                    characterEnd=characterNumberEnd
                    outputFile2.write(str(sentenceNumber)+"|"+str(characterBegin)+" "+str(characterEnd)+"|"+words[characterBegin:characterEnd]+"\n")

                    characterBegin=characterNumberBegin
                elif lineList[-1]=="I-bacteria":
                    flag2=1
                elif lineList[-1]=="O":
                    flag2=0
                    characterEnd=characterNumberEnd
                    outputFile2.write(str(sentenceNumber)+"|"+str(characterBegin)+" "+str(characterEnd)+"|"+words[characterBegin:characterEnd]+"\n")


            if lineList[0]==".":
                words+='.'
                characterNumberBegin=len(words)+1
                characterNumberEnd=len(words)
                flag1=0
            elif lineList[0]==",":
                words+=','
                characterNumberBegin=len(words)+1
                characterNumberEnd=len(words)
                flag1=0
            elif lineList[0]==";":
                words+=';'
                characterNumberBegin=len(words)+1
                characterNumberEnd=len(words)
                flag1=0
            elif lineList[0]=="!":
                words+='!'
                characterNumberBegin=len(words)+1
                characterNumberEnd=len(words)
                flag1=0
            elif lineList[0]=="?":
                words+='?'
                characterNumberBegin=len(words)+1
                characterNumberEnd=len(words)
                flag1=0
            elif lineList[0]=="(":
                words+=(' '*(1-flag1)+'(')
                characterNumberBegin=len(words)
                characterNumberEnd=len(words)
                flag1=1
            elif lineList[0]==")":
                words+=')'
                characterNumberBegin=len(words)+1
                characterNumberEnd=len(words)
                flag1=0
            else:
                words+=(' '*(1-flag1)+lineList[0])
                characterNumberBegin=len(words)+1
                characterNumberEnd=len(words)
                flag1=0

path = 'after_process/'
if os.path.exists('result')==False:
    os.makedirs('result')
if os.path.exists('apply_forCRF')==False:
    os.makedirs('apply_forCRF')
if os.path.exists('sentenceID')==False:
    os.makedirs('sentenceID')
if os.path.exists('bacteria')==False:
    os.makedirs('bacteria')


for root, dirs, files in os.walk(path):
   for file in files:
       current_file=os.path.join(root, file)
       features_list = features_extract.corpus_data_contain_features(current_file, table_dict, file_tag = 0)
       apply_for_CRF_file='apply_forCRF/'+ file
       features_extract.get_text_forCRF(feature_name_list, features_list,apply_for_CRF_file)
       result='result/'+ file
       os.system(os.path.abspath('.')+"/crf_test.exe -m "+os.path.abspath('.')+"/myCRFmodel_IOB2 " + apply_for_CRF_file + ">>" + result)
       function(result,'sentenceID/'+file,'bacteria/'+file)


