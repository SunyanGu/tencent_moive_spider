#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   waikeungshen
#   Date    :   14/10/30 16:35:44
#   Desc    :
#

# 关联规则挖掘：Apriori算法
# 按照Apriori算法的基本思想来实现
# Apriori 性质：任一频繁项集的所有非空子集也必须是频繁的。
import pymongo


class FrequentPattern:
    def __init__(self, Itemset, sup):
        self.Itemset = Itemset
        self.sup = sup

class Apriori:
    def __init__(self, ItemsBorght, min_sup):
        self.ItemsBorght = ItemsBorght
        self.min_sup = min_sup

    def get_1dim_frequent_item(self):
        '''
            得到1维频繁项集
        '''
        FrequentItem = []  # 频繁项集
        for Items in ItemsBorght:
            for item in Items:
                if list(item) not in (i.Itemset for i in FrequentItem): # 如果不在，就添加一个
                    FrequentItem.append(FrequentPattern(list(item), 1))
                else:   # 已经存在，则sup++
                    for i in FrequentItem:
                        if list(item) == i.Itemset:
                            i.sup = i.sup + 1
        print ("1维候选频繁项集:")
        self.print_frequent_item(FrequentItem)
        FrequentItem = [i for i in FrequentItem if i.sup >= min_sup]    # 删除小余min_sup的项
        print ("1维频繁项集:")
        self.print_frequent_item(FrequentItem)
        return FrequentItem

    def apriori_gen(self, FrequentItem, k):
        '''
            查找新的潜在频繁项集
        '''

        # 提取Itemset 并排序
        items = [i.Itemset for i in FrequentItem]
        print(items)
        #items.sort()

        # 自连接
        FrequentItem = []
        for item1 in items:
            for item2 in items:
                if item1 != item2:
                    if (item1[0:len(item1)-1] == item2[0:len(item2)-1]) and (item1[len(item1)-1] < item2[len(item2)-1]):
                        c = list(set(item1).union(set(item2)))
                        if self.__has_infrequent_subset(c, items, k) == False:
                            FrequentItem.append(c)
        # 求候选频繁项集
        temp = []
        for i in FrequentItem:
            for Items in ItemsBorght:
                if len(set(i).difference(Items)) == 0:   # 是子集
                    if i not in (j.Itemset for j in temp):
                        temp.append(FrequentPattern(i, 1))
                    else:
                        for j in temp:
                            if i == j.Itemset:
                                j.sup = j.sup + 1
        FrequentItem = temp
        if temp == []:
            return None
        print ("%d维候选频繁项集:" % k)
        self.print_frequent_item(FrequentItem)

        FrequentItem = [i for i in FrequentItem if i.sup >= min_sup]    # 删除小余min_sup的项
        print ("%d维频繁项集:" % k)
        self.print_frequent_item(FrequentItem)

        return FrequentItem

    def __getSubset(self, c, k):
        '''
            求C的子集, k 为子集长度
        '''
        subs = []
        if k == 1:
            for i in c:
                subs.append(list(i))
        else:
            first = c[0]
            i = c[1:len(c)]
            sub = self.__getSubset(i, k-1)
            for s in sub:
                s.append(first)
                subs.append(s)
        return subs

    def __has_infrequent_subset(self, c, items, k):
        subs = self.__getSubset(c, k-1)
        flag = False
        for each in subs:
            for i in items:
                if len(set(each).difference(i)) == 0:
                    flag = True
            if flag == False:
                return True
        return False

    def print_frequent_item(self, FrequentItem):
        '''
            打印频繁项集
        '''
        for i in FrequentItem:
            print (i.Itemset, i.sup)

    def do(self):
        frequent_item = self.get_1dim_frequent_item()  # 1维频繁项集
        k = 2
        while True:
            frequent_item = self.apriori_gen(frequent_item, k)
            k = k + 1
            if frequent_item ==None:
                break
        return

# if __name__ == "__main__":
#     # ItemsBorght = [['A', 'C', 'D'],
#     #                ['B', 'C', 'E'],
#     #                ['A', 'B', 'C', 'E'],
#     #                ['B', 'E']]
#     # min_sup = 2
#     # apriori = Apriori(ItemsBorght, min_sup)
#     # apriori.do()
#
#     # print "*" * 10
#     ItemsBorght = [['M', 'O', 'N', 'K', 'E', 'Y'],
#                    ['D', 'O', 'N', 'K', 'E', 'Y'],
#                    ['M', 'A', 'K', 'E'],
#                    ['M', 'U', 'C', 'K', 'Y'],
#                    ['C', 'O', 'O', 'K', 'I', 'E']]
#     min_sup = 3
#     apriori = Apriori(ItemsBorght, min_sup)
#     apriori.do()
Client = pymongo.MongoClient('localhost',27017)
tencetn_moive = Client['tencetn_moive']
movie_information_review = tencetn_moive['movie_information_review']

remove_list = ['内地','香港','台湾','日本','韩国','美国','印度','泰国','欧洲','德国','丹麦','法国','加拿大','以色列','英国','院线']

ItemsBorght = []
for i in movie_information_review.find():

    a = []
    for j in i['label']:
        a.extend([j])
    if type(i['director']) == list:
        for m in range(0,len(i['director'])):
            a.append(i['director'][m])
    else:
        a.extend([i['director']])
    for k in i['actor']:
        a.extend([k])
    ItemsBorght.append(a)
# min_sup = 20
# apriori = Apriori(ItemsBorght, min_sup)
# apriori.do()
list = []
for i in ItemsBorght:
    for j in remove_list:
        if j in i:
            i.remove(j)
    #print(i)
    list.append(i)
#print(list)
for i in list:
    #print(i)
    if '张艺谋' in i:
        print(i)

# for i in movie_information_review.find():
#     for j in i['label']:
#         print(j)
#     for k in i['actor']:
#         print(k)






