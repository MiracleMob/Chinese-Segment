import config
import pandas as pd
import re
import os

class dataProcess :

    def __init__(self):
        self.corpus_1998_path = config.corpus_1998_path
        self.corpus_2014_path = config.corpus_2014_path
        self.wordList_1998_path = config.wordList_1998_path
        self.wordList_2014_path = config.corpus_2014_path
        self.wordPairList_path_1998 = config.wordPairList_path_1998
        self.wordPairList_path_2014 = config.wordPairList_path_2014


    def getWordDict1998(self,path):
        words_list = []
        words_dict = {}
        with open(path) as f1:
            line = f1.readline()
            while line:
                re_words = re.compile(u"[\u4e00-\u9fa5]+")
                tmp_str = re.findall(re_words, line)
                words_list.append(tmp_str)
                line = f1.readline()
        length = len(words_list)
        for i in range(length):
            tmp_length = len(words_list[i])
            if tmp_length == 0:
                continue
            for j in range(1, len(words_list[i])):
                word = words_list[i][j]
                if word in words_dict.keys():
                    words_dict[word] += 1
                else:
                    words_dict[word] = 1

        return words_list,words_dict

    def getWordDict2014(self,path):
        words_list = []
        words_dict = []
        files = os.listdir(path)
        for dirs in files:
            if (os.path.isdir(path + '/' + dirs)):
                if (dirs[0] == '.'):
                    pass
                else:
                    dir = dirs
                    files_sub = os.listdir(path + '/' + dir)

                    for file in files_sub:
                        if (os.path.isfile(path + '/' + dir + '/' + file)):
                            data_2014_path = path + '/' + dir + '/' + file
                            print(data_2014_path)
                            with open(data_2014_path) as f1:
                                try:
                                    line = f1.readline()
                                    print(line)
                                    while line:
                                        re_words = re.compile(u"[\u4e00-\u9fa5]+")
                                        tmp_str = re.findall(re_words, line)
                                        words_list.append(tmp_str)
                                        line = f1.readline()
                                except:
                                    pass
        length = len(words_dict)
        for i in range(length):
            tmp_length = len(words_list[i])
            if tmp_length == 0:
                continue
            for j in range(0, len(words_list[i])):
                word = words_list[i][j]
                if word in words_dict.keys():
                    words_dict[word] += 1
                else:
                    words_dict[word] = 1


        return words_list,words_dict

    def save_words_dict(self,words_dict,filename):

        word_csv_list = []
        frequency_csv_list = []
        for key, value in words_dict.items():
            word_csv_list.append(key)
            frequency_csv_list.append(value)

        dataframe = pd.DataFrame({'词语': word_csv_list, '词频': frequency_csv_list})
        dataframe.to_csv('data/' + filename)

    def readWordsDict(self,wordList_path):
        words_dict = {}
        words_list = pd.read_csv(wordList_path)
        count = 0
        for i in range(len(words_list)):
            word = words_list.loc[i]['词语']
            frequency = words_list.loc[i]['词频']
            count += frequency
            words_dict[word] = frequency
        return words_list,words_dict





    def SaveWordsPairDict(self,words_dict_path,filename):
        words_pair = {}
        words_list,_ = self.getWordDict2014(words_dict_path)
        print(type(words_list))
        length = len(words_list)
        for i in range(length):
            tmp_length = len(words_list[i])
            if tmp_length == 0:
                continue
            for j in range(0, len(words_list[i]) - 1):
                word1 = words_list[i][j]
                word2 = words_list[i][j + 1]
                key = word1 + ' ' + word2
                if key in words_pair.keys():
                    words_pair[key] += 1
                else:
                    words_pair[key] = 1

        pair_csv_list = []
        frequencyPair_csv_list = []
        for key, value in words_pair.items():
            pair_csv_list.append(key)
            frequencyPair_csv_list.append(value)
        dataframe = pd.DataFrame({'词对': pair_csv_list, '词频': frequencyPair_csv_list})
        dataframe.to_csv('data/' + filename)
        #dataframe.to_pickle('/Users/mxb/PycharmProjects/Chinese_Segment/data' + filename)


    def readWordsPairDict(self,wordPairList_path):
        words_pair_dict = {}

        words_pair_list = pd.read_csv(wordPairList_path)
        #words_pair_list = pd.read_pickle(wordPairList_path)
        for i in range(len(words_pair_list)):
            word_pair = words_pair_list.loc[i]['词对']
            frequency = words_pair_list.loc[i]['词频']
            words_pair_dict[word_pair] = frequency
            # if frequency > 5:
            #    words_pair_dict[word_pair] = frequency
        return words_pair_dict
    def getTestData(self):
        with open(config.test_data_path,encoding='gbk') as f:
            sentence_list = []
            line = f.readline().strip()
            while line:
                sentence_list.append(line)
                line = f.readline().strip()

        return sentence_list

if __name__ == '__main__':
    dict_path = ''
    dataProcess().SaveWordsPairDict(config.corpus_2014_path,'WordPairList2014.pkl')








