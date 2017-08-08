# coding: utf8
import os
import  re
import json
def get_table_content(dir):
    table_dict={}
    for name in os.listdir(dir):
        content = ''
        rf = open(os.path.join(dir, name), 'r')
        if 'Mostfrequentlywords' in name:
            for eachline in rf:
                if eachline != '\n':
                    content+=eachline.strip().split()[1]+'\n'
        else:
            for eachline in rf:
                if eachline!='\n':
                    content+=eachline.strip().split()[0]+'\n'
        rf.close()
        table_dict[name]=content
    return table_dict

def corpus_data_contain_features(corpus_file,table_dict,file_tag):
    features_list=[]
    rf=open(corpus_file).readlines()
    id,j=0,0
    for eachline in rf:
        features = []
        if eachline =='\n':
            features_list.append({'id':id,'sent_end_tag':1})
            id+=1
        else:
            line_list = eachline.strip().split()
            token = line_list[0]
            features={'POS_feature':'VBN'}
            j+=1
            if file_tag==1:
                features = dict(features,**{'id': id, 'sent_end_tag': 0,'token':token,'BIEO':line_list[1], 'IOB2':line_list[2]})
            else:
                features = dict(features,**{'id': id, 'sent_end_tag': 0,'token':token})

            features_list.append(dict(features, **features_extract(token,table_dict)))
            id+= 1
    return features_list

def features_extract(token,table_dict):
    feature_dict = {}

    feature_dict = dict(feature_dict, **Word_structure_feature(token))
    feature_dict['word_length'] = word_length(token)
    feature_dict['keywords_feature'] = Keywords_feature(token, table_dict)
    feature_dict = dict(feature_dict, **Affix_feature(token, table_dict))
    feature_dict = dict(feature_dict, **Morphology_feature(token, table_dict))
    feature_dict = dict(feature_dict, **Boundary_word_feature(token, table_dict))
    feature_dict['Unary_feature'] = Unary_feature(token, table_dict)
    feature_dict['Nested_feature'] = Nested_feature(token, table_dict)
    feature_dict['StopWord_feature'] = StopWord_feature(token, table_dict)
    feature_dict['CommenWord_feature'] = CommenWord_feature(token, table_dict)
    feature_dict['Context_feature'] = Context_feature(token, table_dict)
    feature_dict = dict(feature_dict, **Dict_feature(token,table_dict))

    return feature_dict


def W_match_pattern(pattern,token):
    p=re.match(pattern,token)
    if p:
        return 'Y'
    else:
        return 'N'

def Word_structure_feature(token):
    word_structure_feature={}
    word_structure_feature['CapWord']=W_match_pattern("^[A-Z][a-z]+$",token)
    word_structure_feature['AllCaps']=W_match_pattern("^[A-Z]+$",token)
    word_structure_feature['CapsMix']=W_match_pattern('^[A-Z]*([A-Z][a-z]|[a-z][A-Z])[A-z]*$',token)
    word_structure_feature['AlphaDigitMix']=W_match_pattern('^[A-Z0-9]*([A-z][0-9]|[0-9][A-z])[A-z0-9]*$',token)
    word_structure_feature['AlphaDigit']=W_match_pattern('^[A-Z]+[0-9]+$',token)
    word_structure_feature['Hyphen']=W_match_pattern('.*[-].*',token)
    word_structure_feature['InitHyphen']=W_match_pattern('[-].*',token)
    word_structure_feature['EndHyphen']=W_match_pattern('.*[-]$',token)
    word_structure_feature['Punctuation']=W_match_pattern('[,.;:?!]$',token)
    word_structure_feature['Quote']=W_match_pattern('.*[/’].*',token)
    word_structure_feature['GreekLetter']=W_match_pattern('''^[αβγδεζηθικλμνξπρστυφχψω]|[alpha]{5}|[beta]{4}|[gamma]{5}|[delte]{5}|[\
                                        epsilon]{7}|[zeta]{4}|[eta]{3}|[theta]{5}|[iota]{4}|[kappa]{5}|[lambda]{6}|[mu]{2}|[nu]{2}|[xi]{2}|[omicron]{7}|[pi]⑵|[rho]{3}\
                                        |[sigma]{5}|[tau]{3}|[upsilon]{7}|[phi]{3}|[chi]{3}|[psi]{3}|[omega]{5}''',token)
    word_structure_feature['UpperLetter']=W_match_pattern('^[A-Z]',token)
    word_structure_feature['Numeral']=W_match_pattern('^[0-9]',token)
    word_structure_feature['TwoNumeral']=W_match_pattern('^[0-9][0-9]',token)
    word_structure_feature['ContainSlaslT']=W_match_pattern('.*[/].*',token)
    word_structure_feature['LeftMarkChar']=W_match_pattern('^[\\[(].*',token)
    word_structure_feature['RightMarkChar']=W_match_pattern('.*[\\])]$.*',token)
    word_structure_feature['EndDot'] = W_match_pattern('^[A-z]*[.]$', token)
    word_structure_feature['OneOrTwoLetter'] = W_match_pattern('^[A-z]{1,2}$', token)
    word_structure_feature['AllDigit'] = W_match_pattern('^[0-9]+$', token)
    word_structure_feature['Equal'] = W_match_pattern('.*[=][A-z]*', token)
    word_structure_feature['Underline'] = W_match_pattern('[\w]*_[\w]*', token)
    word_structure_feature['Plus'] = W_match_pattern('[\w]*[+][\w]*', token)

    return word_structure_feature



def query_W_in_Table(token,file_content):
    if token in file_content:
        return 'Y'
    else:
        return 'N'

def word_length(token):
    l=len(token)
    if l==1:
        return '1'
    elif l==2:
        return '2'
    elif l>=3 and l<=5:
        return '3'
    else:
        return '4'


def Keywords_feature(token,table_dict):
    files_content=table_dict['keyWordTable.txt']
    return query_W_in_Table(token,files_content)

def Affix_feature(token,table_dict):
    affix_feature={}
    affix_feature['prefix3']=query_W_in_Table(token[0:3],table_dict['prefix3Table.txt'])
    affix_feature['prefix4']=query_W_in_Table(token[0:4],table_dict['prefix4Table.txt'])
    affix_feature['suffix3']=query_W_in_Table(token[-3:len(token)],table_dict['suffix3Table.txt'])
    affix_feature['suffix4']=query_W_in_Table(token[-4:len(token)],table_dict['suffix4Table.txt'])
    return affix_feature

def Morphology_feature(token,table_dict):
    morphology_feature={}
    morphword=re.sub('[A-Z]','A',token)
    morphword=re.sub('[a-z]','a',morphword)
    morphword=re.sub('\d','0',morphword)
    morphword=re.sub('[^A-Za-z\d]','x',morphword)
    morphology_feature['morph']=query_W_in_Table(morphword,table_dict['morph_listTable.txt'])
    s_morphword=re.compile(ur"(\w)(\1+)").sub(ur"\1",morphword)
    morphology_feature['s_morph']=query_W_in_Table(s_morphword,table_dict['s_morph_listTable.txt'])
    return morphology_feature

def Boundary_word_feature(token,table_dict):
    boundary_word_feature={}
    boundary_word_feature['left_boundary']=query_W_in_Table(token,table_dict['left_boundaryTable.txt'])
    boundary_word_feature['right_boundary']=query_W_in_Table(token,table_dict['right_boundaryTable.txt'])
    return boundary_word_feature

def Unary_feature(token,table_dict):
    return query_W_in_Table(token,table_dict['unaryTable.txt'])

def Nested_feature(token,table_dict):
    return query_W_in_Table(token,table_dict['nestedTable.txt'])

def StopWord_feature(token,table_dict):
    return query_W_in_Table(token,table_dict['stopTable.txt'])

def CommenWord_feature(token,table_dict):
    return query_W_in_Table(token,table_dict['commonTable.txt'])

def Context_feature(token,table_dict):
    return query_W_in_Table(token,table_dict['contextTable.txt'])

def Dict_feature(token,table_dict):
    dict_feature={}
    dict_feature['dict']=query_W_in_Table(token,table_dict['bacteria_dict_Table.txt'])
    dict_feature['dict_U']=query_W_in_Table(token,table_dict['bacteria_dict_U_Table.txt'])
    dict_feature['dict_N']=query_W_in_Table(token,table_dict['bacteria_dict_N_Table.txt'])
    return dict_feature




def get_text_forCRF(feature_name_list ,features_list,out_put_file):
    wf=open(out_put_file,'w')
    str=''
    for each_record in features_list:
        if each_record["sent_end_tag"]== 0:
            str += each_record['token']
            for each_feature_name in feature_name_list[1:]:
                str+=' '+each_record[each_feature_name]
        str+='\n'
    wf.write(str)


if __name__ == "__main__":
    feature_name_list = ['token', 'CapWord', 'AllCaps', 'CapsMix', 'AlphaDigitMix', 'AlphaDigit', 'Hyphen', 'InitHyphen', \
                         'EndHyphen', 'Punctuation', 'Quote', 'GreekLetter', 'UpperLetter', 'Numeral', 'TwoNumeral','ContainSlaslT', \
                         'LeftMarkChar', 'RightMarkChar','EndDot','OneOrTwoLetter','AllDigit','Equal','Underline','Plus','word_length',\
                         'keywords_feature', 'prefix3', 'prefix4', 'suffix3', 'suffix4', 'morph', \
                         's_morph', 'left_boundary', 'right_boundary', 'Unary_feature', 'Nested_feature', 'StopWord_feature', \
                         'CommenWord_feature', 'Context_feature', 'POS_feature', 'dict', 'dict_U', 'dict_N', 'BIEO','IOB2']
    feature_name_list2 = feature_name_list[:-2]
    feature_name_list2.append(feature_name_list[-1])
    table_dict= get_table_content('table')
    features_list=corpus_data_contain_features('bacteria_train.iob',table_dict,file_tag=1)
    get_text_forCRF(feature_name_list[:-1],features_list ,'train_forCRF_BIEO.txt' )
    get_text_forCRF(feature_name_list2, features_list, 'train_forCRF_IOB2.txt')

    features_list = corpus_data_contain_features('bacteria_test.iob', table_dict,file_tag=1)
    get_text_forCRF(feature_name_list[:-1], features_list, 'test_forCRF_BIEO.txt')
    get_text_forCRF(feature_name_list2, features_list, 'test_forCRF_IOB2.txt')