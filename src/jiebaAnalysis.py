import jieba
import jieba.posseg as pseg

"""传出结果，形式为字典，key为value中词语类型，value为列表"""
def out(content):
    jieba.load_userdict("static/dict.txt")
    # 补充由于结构较为复杂难以分出的案由
    content = content.replace(" ", "").replace("\n", "")
    words = pseg.lcut(content, use_paddle=True)
    wordsList = []
    # 初步分词结果
    flagList = []
    # 初步分词结果对应的词性
    length = 0
    for word, flag in words:
        length += 1
        wordsList.append(str(word))
        flagList.append(str(flag))
    nr = get_about_nr(wordsList, flagList, length)
    ns = get_about_ns(wordsList, flagList, length)
    # v = get_v(wordsList, flagList, length)
    r = get_r(wordsList, flagList, length)
    adj = get_adj(wordsList, flagList, length)
    result = {"不涉及地点名词": nr, "涉及地点名词": ns, "案由": r, "形容词": adj}
    return result

"""从txt文件中读出一个字符串，该方法仅为本地进行调试使用"""
def getStrFromTxt(file):
    # 使用try结构解决在本地调试时由于编码出现的问题
    try:
        return getStrFromTxt1(file)
    except:
        return getStrFromTxt2(file)

"""getStrFromTxt的子方法，该方法仅为本地进行调试使用"""
def getStrFromTxt1(file):
    f = open(file, mode="r", encoding='gbk')
    content = f.read()
    return content

"""getStrFromTxt的子方法，该方法仅为本地进行调试使用"""
def getStrFromTxt2(file):
    f = open(file, mode="r", encoding="utf-8")
    content = f.read()
    return content

"""展示分词结果于本地，该方法仅为本地进行调试使用"""
def showRes(content):
    jieba.load_userdict("static/dict.txt")
    content = content.replace(" ", "").replace("\n", "")
    words = pseg.lcut(content, use_paddle=True)
    wordsList = []
    flagList = []
    length = 0
    for word, flag in words:
        length += 1
        wordsList.append(str(word))
        flagList.append(str(flag))
        # print(word + " " + flag)
    # 基本等同于out方法的结果
    print("不涉及地点的名词")
    print(get_about_nr(wordsList, flagList, length))
    print("涉及地点名词")
    print(get_about_ns(wordsList, flagList, length))
    print("案由")
    print(get_r(wordsList, flagList, length))
    # print("动词")
    # print(get_v(wordsList, flagList, length))
    print("形容词")
    print(get_adj(wordsList, flagList, length))
    return

"""得到不涉及地点名词分词结果"""
def get_about_nr(wordsList, flagList, length):
    n_outList = []
    for i in range(0, length):
        # 人名
        if flagList[i] == "nr" and len(wordsList[i]) > 1:
            n_outList.append(wordsList[i])
        # 文化程度
        elif "文化" in wordsList[i]:
            n_outList.append(wordsList[i])
        # 民族
        elif flagList[i] == "nz" and wordsList[i].endswith("族"):
            n_outList.append(wordsList[i])
        # 性别
        elif flagList[i] == "n" and (wordsList[i] == "男" or wordsList[i] == "女"):
            n_outList.append(wordsList[i])
    # printTimes(n_outList)
    n_outList = list(set(n_outList))
    return n_outList

"""得到涉及地点名词的分词结果"""
def get_about_ns(wordsList, flagList, length):
    n_outList = []
    for i in range(0, length):
        # 得到完整的法院名称
        if flagList[i] == "nt" and str(wordsList[i]).endswith("法院"):
            if i == 0:
                n_outList.append(wordsList[i])
                continue
            elif i == 1:
                n_outList.append(wordsList[i - 1] + wordsList[i])
                continue
            if flagList[i - 1] != "x":
                # 对于文中出现的法院进行向前补充地名得到完整法院名称
                toOutTempWord = wordsList[i - 1] + wordsList[i]
                tempI = i - 2
                while flagList[tempI] == "ns" or isNs(wordsList[tempI]):
                    toOutTempWord = wordsList[tempI] + toOutTempWord
                    tempI -= 1
                    if tempI < 0:
                        break
                n_outList.append(correct(toOutTempWord))
                # 由最后运行结果补充的特判
            else:
                n_outList.append(wordsList[i])
        # 得到完整地名
        elif flagList[i] == "ns":
            toOutP = wordsList[i]
            try:
                i += 1
                # 得到地名后向后匹配地名，得到完整地名
                while flagList[i] == 'ns' or isNs(wordsList[i]):
                    toOutP += wordsList[i]
                    if i + 1 < length:
                        i += 1
            except:
                continue
            if len(toOutP) > 1:
                n_outList.append(toOutP)
    # printTimes(n_outList)
    n_outList = list(set(n_outList))
    return n_outList

"""由于jieba库对地点的识别存在一些问题，在此补充简易的判断是否为地名的方法"""
def isNs(string):
    maybeNs = ["省", "市", "自治区", "县", "区"]
    for i in range(0, len(maybeNs)):
        if maybeNs[i] in string:
            return True
    return False

"""得到动词及动宾短语，以列表形式返回"""
# 后经讨论认为该词性存在意义不大
"""
def get_v(wordsList, flagList, length):
    v_outList = []
    for i in range(0, length):
        if flagList[i] == "v" and len(wordsList[i]) > 1:
            v_outList.append(wordsList[i])
        elif (flagList[i] == "vn" or flagList[i] == "v") and flagList[i + 1] == "n":
            v_outList.append(wordsList[i] + wordsList[i + 1])
            i += 1
    # printTimes(v_outList)
    v_outList = list(set(v_outList))
    return v_outList
"""

"""得到案由，以列表形式返回"""
def get_r(wordsList, flagList, length):
    fileReason = open("static/dict.txt", encoding='utf-8').read().split(" re\n")
    r_outList = []
    for i in range(0, length):
        if flagList[i] == "re":
            r_outList.append(wordsList[i])
        else:
            if wordsList[i][0:len(wordsList[i]) - 1] in fileReason:
                r_outList.append(wordsList[i][0:len(wordsList[i]) - 1])
    # printTimes(r_outList)
    r_outList = list(set(r_outList))
    return r_outList

"""得到形容词，以列表形式返回"""
def get_adj(wordsList, flagList, length):
    adj_outList = []
    for i in range(0, length):
        if flagList[i] == "a" or flagList[i] == "ag":
            adj_outList.append(wordsList[i])
    for i in adj_outList:
        if check(adj_outList, i) == 1:
            adj_outList.remove(i)
    # printTimes(adj_outList)
    adj_outList = list(set(adj_outList))
    return adj_outList

"""返回初始分词过程中某一个词的出现次数"""
def check(outList, word):
    ans = 0
    for i in range(0, len(outList)):
        if outList[i] == word:
            ans += 1
    return ans

"""输出一个列表中每个元素的出现次数于本地，该方法仅供分析词频使用"""
def printTimes(outList):
    for i in range(0, len(outList)):
        print(outList[i], end=":")
        print(check(outList, outList[i]), end=";")
    print()

"""基于结果对部分法院名称进行修正"""
def correct(sentence):
    sentence = sentence.replace("根据", "").replace("维持", "").replace("报请","").replace("影响", "")
    sentence = sentence.replace("撤销", "").replace("了", "").replace("及", "").replace("依据", "")
    if sentence.startswith("和"):
        sentence = sentence[1:]
    return sentence
