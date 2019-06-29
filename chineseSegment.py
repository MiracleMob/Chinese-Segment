import pandas as pd
import config
import dataProcessing
import time
class Segment :
    def __init__(self):
        self.candidateLen = config.candidateLen
        self.wordList_1998_path = config.wordList_1998_path
        self.wordPairList_path_1998 = config.wordPairList_path_1998

    def getCandidateWords(sentence,words_dict):
        # sentence指句子 candidateLen指候选词的最大长度
        candidateLen = Segment().candidateLen
        candidate_words_list = []
        sentence_length = len(sentence)
        #_,words_dict = dataProcessing.dataProcess().readWordsDict(config.wordList_1998_path)
        for index in range(sentence_length):
            # 每个字作为候选词加进候选词列表
            # candidate_words_list.append([word,index,index])
            # 当前字下 存在候选词的个数
            tmp_count = 0
            for i in range(candidateLen):
                # 在当前位置寻找候选词，范围为candidateLen
                if index + i < sentence_length:
                    word = sentence[index:index + i + 1]
                    if word in words_dict.keys():
                        candidate_words_list.append([word, index, index + i])
                        tmp_count += 1
                if index - i >= 0:
                    word = sentence[index - i:index + 1]
                    if word in words_dict.keys():
                        if [word, index - i, index] not in candidate_words_list:
                            candidate_words_list.append([word, index - i, index])
                            tmp_count += 1
            if tmp_count == 0:
                # 词表中不存在
                w = sentence[index]
                # 频率计为1
                words_dict[w] = 1
                candidate_words_list.append([w, index, index])

        print(candidate_words_list)

        return candidate_words_list, words_dict



    def findCandidateLeftWords(sentence,words_dict):

        # 返回左邻词词典{word:[[leftword1,s1,s2],[leftword2,s1,s2]]}`
        left_word_dict = {}
        left_word_dict['end'] = []
        candidateLen = Segment().candidateLen
        candidate_words_list , words_dict = Segment.getCandidateWords(sentence,words_dict)

        for candidate_word in candidate_words_list:
            # candidate_word = [word,start,end]
            word = candidate_word[0]
            start = candidate_word[1]
            end = candidate_word[2]
            word_str = word + ' '+str(start)+' '+str(end)
            # 初始化这个候选词的左邻词字典

            left_word_dict[word_str] = []
            if start == 0:
                left_word = 'start'
                left_word_dict[word_str].append([left_word, -1, -1])

            if end == len(sentence) - 1:
                left_word = word
                left_word_dict['end'].append([left_word, start, end])

            for i in range(candidateLen):

                if start - i - 1 < 0:
                    break
                tmp_word = sentence[start - i - 1:start]
                if tmp_word in words_dict.keys():
                    left_word = tmp_word
                    left_word_dict[word_str].append([left_word, start - i - 1, start - 1])

        print(left_word_dict)

        return candidate_words_list,words_dict,left_word_dict

    def findBestLeftWord(sentence,words_dict,words_pair_dict):
        candidate_words_list,words_dict,left_word_dict = Segment.findCandidateLeftWords(sentence, words_dict)
        #words_pair_dict = dataProcessing.dataProcess().readWordsPairDict(config.wordPairList_path_1998)
        best_left_word_dict = {}
        words_length = len(words_dict)
        max_end_pro = float('-inf')
        for i in range(len(candidate_words_list)):
            candidate_word = candidate_words_list[i][0]
            s1 = candidate_words_list[i][1]
            s2 = candidate_words_list[i][2]
            max_pro = float('-inf')
            candidate_word_str = candidate_word + ' '+str(s1) +' '+str(s2)
            # 累计概率
            if s1 == 0:
                best_left_word = 'start' + ' -1 -1'
                #best_left_word = 'start'
                pro = float(words_dict[candidate_word]) / words_length
                ##
                #candidate_word = candidate_word +' '+str(s1) +' '+str(s2)
                best_left_word_dict[candidate_word_str] = [best_left_word, pro]
                continue

            # 中间的词
            left_word_list = left_word_dict[candidate_word_str]
            for j in range(len(left_word_list)):
                left_word = left_word_list[j][0]
                s1_left = left_word_list[j][1]
                s2_left = left_word_list[j][2]

                word_pair = left_word + ' ' + candidate_word
                sum_pair_count = 0
                pair_count = 0
                for key in words_pair_dict.keys():
                    if key.split()[1] == candidate_word:
                        sum_pair_count += 1
                    if key == word_pair:
                        pair_count = words_pair_dict[key]
                    else:
                        # 如果不存在词对，计为1
                        pair_count = 0
                left_word_str = left_word +' '+str(s1_left)+' '+str(s2_left)
                if left_word_str not in best_left_word_dict.keys():
                    continue
                ##拉普拉斯平滑
                # pro = math.log(best_left_word_dict[left_word][1] + 1) + math.log(pair_count + 1) - math.log(sum_pair_count + sentence_length) + 100
                pro = best_left_word_dict[left_word_str][1] * (pair_count + 1) / ((sum_pair_count) + words_length)
                if pro > max_pro:
                    max_pro = pro
                    best_left_word = left_word_str

            best_left_word_dict[candidate_word_str] = [best_left_word, max_pro]

            if s2 == len(sentence) - 1:
                pro = best_left_word_dict[candidate_word_str][1]
                if pro > max_end_pro:
                    max_end_pro = pro
                    best_left_word_dict['end'] = [candidate_word_str, max_end_pro]

        print(best_left_word_dict)

        return best_left_word_dict


    def sentenceCut(sentence):
        sentence_list = []
        def is_Chinese(word):
            if '\u4e00' <=word <= '\u9fff':
                return True
            else:
                return False
        i = 0
        while i < len(sentence):
            s = ''
            digit = ''
            if sentence[i].isdigit() == False and is_Chinese(sentence[i]) == False:
                sentence_list.append(sentence[i])
                i += 1
                continue
            while i<len(sentence) and is_Chinese(sentence[i]):
                s += sentence[i]
                i += 1
            if s!= '':
                sentence_list.append(s)
                continue
            while i<len(sentence) and sentence[i].isdigit():
                digit += sentence[i]
                i += 1
            if digit!='':
                sentence_list.append(digit)
                continue

        return sentence_list







    def getChineseSegment(sentence,words_dict,words_pair_dict):
        print('正在切分.......')
        best_left_word_dict = Segment.findBestLeftWord(sentence,words_dict,words_pair_dict)
        result = ''
        key = 'end'
        while key != 'start -1 -1':
            if key == 'end':
                key = best_left_word_dict[key][0]
                continue
            result = key.split()[0] + ' ' + result
            key = best_left_word_dict[key][0]
        return result

    def saveResult(self,result_list,path):

        for i in range(len(result_list)):
            with open(path,'a') as f:
                f.write(result_list[i])
                f.write('\n')



if __name__ == '__main__':


    sentence_list = dataProcessing.dataProcess().getTestData()
    # sentence_list= [
    #     '我们在学习',
    #     '等到处长发现他们有意见分歧',
    #     '2018年11月8日，这是我的生日。'
    # ]
    for sentence in sentence_list:
        print(Segment.sentenceCut(sentence))

    print('reading data')

    _, words_dict = dataProcessing.dataProcess().readWordsDict(
        config.wordList_1998_path)
    words_pair_dict = dataProcessing.dataProcess().readWordsPairDict(
        config.wordPairList_path_1998)

    result_list = []
    sentence = '欢乐热闹的气氛已悄悄降临'
    print(Segment.getChineseSegment(sentence,words_dict,words_pair_dict))
    for sentences in sentence_list:
        sentence_cut = Segment.sentenceCut(sentences)
        result = ''
        for sentence in sentence_cut:
            if '\u4e00' <=sentence[0]<= '\u9fff' and len(sentence) > 1:
                result += Segment.getChineseSegment(sentence, words_dict,
                                                    words_pair_dict)
                # try:
                #    result += Segment.getChineseSegment(sentence, words_dict,words_pair_dict)
                # except:
                #    result += sentence + ' '
                # print(result)
            else:
                result += sentence +' '
        print(result)
        result_list.append(result)

    Segment().saveResult(result_list,config.test_result_path)








