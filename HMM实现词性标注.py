from pyltp import Segmentor, Postagger, NamedEntityRecognizer
import os
import numpy as np
import jieba
import time

LTP_DATA_DIR = r'ltp_data_v3.4.0'  # LTP模型文件夹的路径

segmentor = Segmentor()  # 分词函数
segmentor.load(os.path.join(LTP_DATA_DIR, "cws.model"))  # 加载模型

postagger = Postagger()  # 词性标注函数
postagger.load(os.path.join(LTP_DATA_DIR, "pos.model"))  # 加载模型

# 导入训练集,数据预处理后按句分开
fp = open(r'train_1.txt', 'r', encoding='utf-8')
text = fp.read()
list1 = ''.join(text)
list1 = list1.replace(u'\u3000', u'').replace(u'\xa0', u'').replace('\n', '').replace('\r', '').replace(" ", "")
list1 = list1.replace('？', '。').replace('！', '。')
list1 = list1.split('。')
fp.close()
words = []  # 训练集分词结果存入words
words_class = []  # 训练集词性标注结果存入words_class

for i in range(len(list1)):
    words.append(jieba.lcut(list1[i]))
    # print(words[i])
    words_class.append(list(postagger.postag(words[i])))
    # print(words_class[i])

id = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'g': 5, 'h': 6, 'i': 7, 'j': 8, 'k': 9, 'm': 10, 'n': 11, 'nd': 12,
      'nh': 13, 'ni': 14, 'nl': 15, 'ns': 16, 'nt': 17, 'nz': 18, 'o': 19, 'p': 20, 'q': 21, 'r': 22, 'u': 23, 'v': 24,
      'wp': 25, 'ws': 26, 'x': 27, 'z': 28}  # 各词性的索引值，字母与词性对应关系详见报告
id_verse = {value: key for key, value in id.items()}  # id1的逆字典，即各索引值对应的词性
A = []  # 概率转移矩阵

C = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # 初始概率Π初始化
for i in range(29):
    A.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

B = {}  # 发射概率矩阵
fre = {}  # 词频统计


def pro_calculate(A, C, id, mark):  # 概率计算函数1，主要计算概率转移矩阵A1，与初始概率矩阵C1
    marks_num = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for m1 in mark:
        if len(m1) != 0:
            C[id[m1[0]]] += 1
            marks_num[id[m1[0]]] += 1
            for i in range(1, len(m1)):
                A[id[m1[i - 1]]][id[m1[i]]] += 1
                if i + 1 != len(m1):
                    marks_num[id[m1[i]]] += 1
    for i in range(len(A)):
        for j in range(len(A[i])):
            if marks_num[i] != 0:
                A[i][j] = A[i][j] / marks_num[i]
    for i in range(len(C)):
        C[i] = C[i] / len(mark)


def word_pro(B, fre, id):  # 概率计算函数2,主要计算发射概率矩阵B1
    for i in range(len(words)):
        for j in range(len(words[i])):
            if words[i][j] not in B:
                B[words[i][j]] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                B[words[i][j]][id[words_class[i][j]]] += 1
                fre[words[i][j]] = 1
            else:
                B[words[i][j]][id[words_class[i][j]]] += 1
                fre[words[i][j]] += 1
    word = list(B.keys())
    for w in word:
        for i in range(29):
            B[w][i] = B[w][i] / fre[w]


path = []  # 回溯后求得的词性标注序列存放在path


def viterbi(list2, A, B, C):  # 维特比算法，求最优的隐状态序列
    for sentences in list2:
        way = []
        for i in range(29):
            way.append([])
        last = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        if sentences[0] in B:
            for i in range(29):
                if B[sentences[0]][i] != 0:
                    last[i] = B[sentences[0]][i] * C[i]
                else:
                    last[i] = C[i] / len(list(B.keys()))
        else:
            for i in range(29):
                last[i] = C[i] / len(list(B.keys()))
        for z in range(29):
            way[z].append(z)
        for w in range(1, len(sentences)):
            new = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            if sentences[w] in B:
                for j in range(29):
                    Max = 0
                    f = 0
                    for i in range(29):
                        t = last[i] * A[i][j]
                        if t > Max:
                            Max = t
                            if B[sentences[w]][j] != 0:
                                new[j] = Max * B[sentences[w]][j]
                            else:
                                new[j] = Max / len(list(B.keys()))
                            f = i
                    way[j].append(f)
            else:
                for j in range(29):
                    Max = 0
                    f = 0
                    for i in range(29):
                        t = last[i] * A[i][j]
                        if t > Max:
                            Max = t
                            new[j] = Max / len(list(B.keys()))
                            f = i
                    way[j].append(f)
            last = new
        best = 0
        best_long = 0
        for y in range(29):
            if last[y] > best_long:
                best_long = last[y]
                best = y
        n = len(way[0])
        way = np.array(way)
        path.append([])
        findpath(way, best, n)
        path[len(path) - 1].reverse()


def findpath(way, best, n):  # 递归回溯路径
    if n == 0:
        return
    else:
        path[len(path) - 1].append(id_verse[best])
        best = way[best][n - 1]
        findpath(way[:, 0:n - 1], best, n - 1)


def getR(pre, stwords):
    Rs = []
    for i in range(29):
        TP = 0
        lens = 0
        for j in range(len(pre)):
            if id_verse[i] not in stwords[j]:
                continue
            tp = 0
            for k in range(len(pre[j])):
                if id_verse[i] == stwords[j][k]:
                    lens += 1
                    if pre[j][k] == stwords[j][k]:
                        tp = tp + 1
            TP = TP + tp
        if lens != 0:
            Rs.append(round(TP / lens, 4))
    mr = sum(Rs) / len(Rs)
    return mr


def getP(pre, stwords):
    Rp = []
    for i in range(29):
        TP = 0
        lens = 0
        for j in range(len(pre)):
            if id_verse[i] not in pre[j]:
                continue
            tp = 0
            for k in range(len(pre[j])):
                if id_verse[i] == pre[j][k]:
                    lens += 1
                    if pre[j][k] == stwords[j][k]:
                        tp = tp + 1
            TP = TP + tp
        if lens != 0:
            Rp.append(round(TP / lens, 4))
    mp = sum(Rp) / len(Rp)
    return mp


def getF(p, r):
    return round((2 * p * r) / (p + r), 4)


start = time.time()
pro_calculate(A, C, id, words_class)
word_pro(B, fre, id)
list2 = []
fp = open(r'test_1.txt', 'r', encoding='utf-8')
text = fp.read()
txt = ''.join(text)
txt = txt.replace(u'\u3000', u'').replace(u'\xa0', u'').replace('\n', '').replace('\r', '').replace(" ", "")
txt = txt.replace('？', '。').replace('！', '。')
txt = txt.split('。')
fp.close()
for i in range(len(txt)):
    list2.append(jieba.lcut(txt[i]))
    print(list2[len(list2) - 1])
viterbi(list2, A, B, C)
over = time.time()
stseq = []
for i in range(len(list2)):
    stseq.append(list(postagger.postag(list2[i])))
R = getR(path, stseq)
P = getP(path, stseq)
F = getF(P, R)
fp = open('HMM词性标注.txt', 'w', encoding='utf-8')
for sentence in path:
    for word in sentence:
        fp.write(word + ',')
fp.close()
print('HMM模型构建与预测总耗时为:{}'.format(over - start))
print('macroP值为:{}'.format(P))
print('macroR值为:{}'.format(R))
print('macroF值为:{}'.format(F))
