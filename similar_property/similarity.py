# -*- coding:utf-8 -*-

"""
查找相似属性
"""
import math
import re

DATE_PATTERN = re.compile(r'^((?:19|20)?\d{2})[-.]?((?:[0-1]?|1)[0-9])[-.]?((?:[0-3]?|[1-3])[0-9])?$') 
DATE_PATTERN2 = re.compile(r'[0-9]{2,4}年([0-9]{1,2}月)?([0-9]{1,2}日)?') 

def has_number(s):
    return bool(re.search(r'\d', s))

def is_date(s):
    """
    描述：时间判断。
    参数：strdate 要分析的时间字符串，比如目标时间类型datetime(1992, 2, 3)
    可以被解析的是下述字符串之一：
    19920203 
    199203
    1992.02.03
    1992.02
    1992-02-03
    1992-02
    920203
    """
    m = DATE_PATTERN.match(s)
    if m or DATE_PATTERN2.match(s):
        return True
    else:
        return False

def edit_distance(s1, s2):
    l1, l2 = len(s1), len(s2)
    dp = [[0]*(l2+1) for i in range(l1+1)]

    for i in range(l1+1):
        dp[i][0] = i
    for j in range(l2+1):
        dp[0][j] = j

    for i in range(1, l1+1):
        for j in range(1, l2+1):
            dp[i][j] = min(dp[i-1][j]+1, dp[i][j-1]+1, dp[i-1][j-1] if s1[i-1] == s2[j-1] else dp[i-1][j-1]+1 )
    return dp[l1][l2]

def normalized_google_distance(s1, s2):
    """
    Normalized Google Distance
    set1 
    set2
    """
    log = math.log
    return log(max(len(s1), len(s2))) - log(len(set(s1) & set(s2))) / \
            log(len(s1)+len(s2)) - log(min(len(s1), len(s2)))

def valuesimilarity_literal(p1, p2):
    s = 0
    for v1 in p1.values:
        for v2 in p2.values:
            s += edit_distance_similarity(v1, v2)

    return s*1.0/len(p1.values)*len(p2.values)

def valuesimilarity_number(p1, p2):
    a = [has_number(v) for v in p1.values]
    b = [has_number(v) for v in p2.values]
    ar = a.count(True)*1.0/len(a)
    br = b.count(True)*1.0/len(b)
    return ar*br

def valuesimilarity_date(p1, p2):
    a = [is_date(v) for v in p1.values]
    b = [is_date(v) for v in p2.values]
    ar = a.count(True)*1.0/len(a)
    br = b.count(True)*1.0/len(b)
    return ar*br 

def valuesimilarity_length(p1, p2):
    a = [len(v) for v in p1.values]
    b = [len(v) for v in p2.values]
    av = sum(a)*1.0/len(a)
    bv = sum(b)*1.0/len(b)
    return  abs(av-bv)/max(av, bv)

def word_intersection_similarity(w1, w2):
    return len(set(w1)&set(w2))*1.0/len(set(w1)|set(w2))

def edit_distance_similarity(w1, w2):
    return 1-edit_distance(w1, w2)*1.0/max(len(w1),len(w2))

def reversed_article_similarity(p1, p2):
    return 1 - len((set(p1.articles) & set(p2.articles)))*1.0/min(len(p1.articles), len(p2.articles))

def domain_similarity(p1, p2):
    return normalized_google_distance(p1.concepts, p2.concepts)

def article_type_value(p1, p2):
    pass

def literal_type_value(p1, p2):
    pass

def number_type_value(p1, p2):
    pass

if __name__=="__main__":
    print is_date('1991年1月23日')
