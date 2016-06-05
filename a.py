from numpy import *
import pymongo

def loadDataSet():
    return [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]

def createC1(dataSet):
    C1 = []
    for transaction in dataSet:
        for item in transaction:
            if not [item] in C1:
                C1.append([item])
    C1.sort()
    return map(frozenset, C1)#use frozen set so we
                            #can use it as a key in a dict

def scanD(D, Ck, minSupport):
    ssCnt = {}
    count = 0
    ck = list(Ck)
    for tid in D:
        count += 1
        for can in ck:
            if can.issubset(tid):
                if not can in ssCnt: ssCnt[can]=1
                else: ssCnt[can] += 1
    numItems = float(count)
    retList = []
    supportData = {}
    for key in ssCnt:
        support = ssCnt[key]/numItems
        if support >= minSupport:
            retList.insert(0,key)
        supportData[key] = support
    return retList, supportData

def aprioriGen(Lk, k): #creates Ck
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i+1, lenLk):
            L1 = list(Lk[i])[:k-2]; L2 = list(Lk[j])[:k-2]
            L1.sort(); L2.sort()
            if L1==L2: #if first k-2 elements are equal
                retList.append(Lk[i] | Lk[j]) #set union
    return retList

def apriori(dataSet, minSupport = 0.27):
    C1 = createC1(dataSet)
    D = map(set, dataSet)
    L1, supportData = scanD(D, C1, minSupport)
    L = [L1]
    k = 2
    while (len(L[k-2]) > 0):
        Ck = aprioriGen(L[k-2], k)
        Lk, supK = scanD(D, Ck, minSupport)#scan DB to get Lk
        supportData.update(supK)
        L.append(Lk)
        k += 1
    return L, supportData


Client = pymongo.MongoClient('localhost',27017)
tencetn_moive = Client['tencetn_moive']
movie_information_review = tencetn_moive['movie_information_review']

remove_list = ['内地','香港','台湾','日本','韩国','美国','印度','泰国','欧洲','德国','丹麦','法国','加拿大','以色列','英国','院线','剧情']

ItemsBorght = []
for i in movie_information_review.find():
    a = []
    for j in i['label']:
        a.extend([j])
    if type(i['director']) == list:
        for m in range(0,len(i['director'])):
            a.append(i['director'][m])
            #print('this is a list')
    else:
        a.extend([i['director']])
    for k in i['actor']:
        a.extend([k])
    ItemsBorght.append(a)
new_list = []
for i in ItemsBorght:
    for j in remove_list:
        if j in i:
            i.remove(j)
    new_list.append(i)
#print(new_list)
relation = []

for i in new_list:
    if '张艺谋' in i:
        relation.append(i)
        print(i)
#print(relation)
C1 = createC1(relation)
D = map(set,relation)



L,suppData = apriori(relation)
L1 = aprioriGen(L[0],2)
L2 = aprioriGen(L1,1)
for i in L1:
    print(i)
for i in L2:
    print(i)
print(L[0])





