import pandas as pd
import config
import dataProcessing
class Segment :
    def __init__(self):
        self.candidateLen = config.candidateLen
        self.wordList_1998_path = config.wordList_1998_path
        self.wordPairList_path_1998 = config.wordPairList_path_1998

    def getCandidateWords(sentence):
        # sentence指句子 candidateLen指候选词的最大长度
        print('正在得到候选词......')
        candidateLen = Segment().candidateLen
        candidate_words_list = []
        sentence_length = len(sentence)
        _,words_dict = dataProcessing.dataProcess().readWordsDict(config.wordList_1998_path)
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

        return candidate_words_list, words_dict

    def findCandidateLeftWords(sentence):

        print('正在得到左邻词......')
        # 返回左邻词词典{word:[[leftword1,s1,s2],[leftword2,s1,s2]]}
        left_word_dict = {}
        left_word_dict['end'] = []
        candidateLen = Segment().candidateLen
        candidate_words_list , words_dict = Segment.getCandidateWords(sentence)

        for candidate_word in candidate_words_list:
            # candidate_word = [word,start,end]
            word = candidate_word[0]
            start = candidate_word[1]
            end = candidate_word[2]
            # 初始化这个候选词的左邻词字典

            left_word_dict[word] = []
            if start == 0:
                left_word = 'start'
                left_word_dict[word].append([left_word, -1, -1])

            if end == len(sentence) - 1:
                left_word = word
                left_word_dict['end'].append([left_word, start, end])

            for i in range(candidateLen):

                if start - i - 1 < 0:
                    break
                tmp_word = sentence[start - i - 1:start]
                if tmp_word in words_dict.keys():
                    left_word = tmp_word
                    left_word_dict[word].append([left_word, start - i - 1, start])

        return candidate_words_list,words_dict,left_word_dict

    def findBestLeftWord(sentence):
        print('正在得到最佳左邻词........')
        candidate_words_list,words_dict,left_word_dict = Segment.findCandidateLeftWords(sentence)
        words_pair_dict = dataProcessing.dataProcess().readWordsPairDict(config.wordPairList_path_1998)
        best_left_word_dict = {}
        words_length = len(words_dict)
        for i in range(len(candidate_words_list)):
            candidate_word = candidate_words_list[i][0]
            s1 = candidate_words_list[i][1]
            s2 = candidate_words_list[i][2]
            max_pro = float('-inf')
            max_end_pro = float('-inf')
            # 累计概率
            if s1 == 0:
                best_left_word = 'start'
                pro = float(words_dict[candidate_word]) / words_length
                best_left_word_dict[candidate_word] = [best_left_word, pro]
                continue

            # 中间的词
            left_word_list = left_word_dict[candidate_word]
            for j in range(len(left_word_list)):
                left_word = left_word_list[j][0]
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
                # 最后的end

                # 拉普拉斯平滑
                # pro = math.log(best_left_word_dict[left_word][1] + 1) + math.log(pair_count + 1) - math.log(sum_pair_count + sentence_length) + 100
                pro = best_left_word_dict[left_word][1] * (pair_count + 1) / ((sum_pair_count) + words_length)
                if pro > max_pro:
                    max_pro = pro
                    best_left_word = left_word

            best_left_word_dict[candidate_word] = [best_left_word, max_pro]

            if s2 == len(sentence) - 1:
                pro = best_left_word_dict[candidate_word][1]
                if pro > max_end_pro:
                    max_end_pro = pro
                    best_left_word_dict['end'] = [candidate_word, max_end_pro]

        return best_left_word_dict

    def getChineseSegment(sentence):
        print('正在切分.......')
        best_left_word_dict = Segment.findBestLeftWord(sentence)
        result = ''
        key = 'end'
        while key != 'start':
            if key == 'end':
                key = best_left_word_dict[key][0]
                continue
            result = key + ' ' + result
            key = best_left_word_dict[key][0]
        return result



if __name__ == '__main__':

    sentence = '事故现场部署了大批警察'

    print(Segment.getChineseSegment(sentence))






