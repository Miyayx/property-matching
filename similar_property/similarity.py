# -*- coding:utf-8 -*-

"""
查找相似属性
"""
import math
import re
import sys
import codecs

DATE_PATTERN = re.compile(r'^((?:19|20)?\d{2})[-.]?((?:[0-1]?|1)[0-9])[-.]?((?:[0-3]?|[1-3])[0-9])?$') 
DATE_PATTERN2 = re.compile(r'[0-9]{2,4}年([0-9]{1,2}月)?([0-9]{1,2}日)?') 
CHINESE = ur"[\u4e00-\u9fa5]+"

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

def jaccard_distance(s1, s2):
    if len(s1) == 0 and len(s2) == 0:
        return 0
    return 1 - len(set(list(s1))&set(list(s2))) * 1.0 /len(set(list(s1))|set(list(s2)))

def normalized_google_distance(s1, s2):
    """
    Normalized Google Distance
    set1 
    set2
    """
    log = math.log
    if len(s1) == 0 or len(s2) == 0 or len(set(s1)&set(s2)) == 0:
        return 1
    return (log(max(len(s1), len(s2))) - log(len(set(s1) & set(s2)))) / \
            (log(len(s1)+len(s2)) - log(min(len(s1), len(s2))))

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
    if len(w1) == 0 or len(w2) == 0:
        return 0
    return 1-edit_distance(w1, w2)*1.0/max(len(w1),len(w2))

def label_similarity(p1, p2):
    if len(p1.label) == 0 or len(p2.label) == 0:
        return 0
    if re.match(CHINESE, p2.label): #有中文 
        return edit_distance_similarity(p1.zhlabel, p2.label)
    return edit_distance_similarity(p1.label, p2.label)
    #return 1-jaccard_distance(p1.label, p2.label)

#def article_similarity(p1, p2, cl):
#    print "article_similarity"
#    n = 0
#    p2_articles = set(p2.articles)
#    for a1 in p1.articles:
#        if a1 in cl and cl[a1] in p2_articles:
#            n += 1
#            break
#    return n*1.0/min((len(p1.articles),len(p2.articles)))

def article_similarity(p1, p2, cl):
    print "article_similarity"
    n = 0
    if len(p1.infobox.keys()) == 0 or len(p2.infobox.keys()) == 0:
        return 0
    p2_articles = set(p2.infobox.keys())
    for a1 in p1.infobox.keys():
        if a1 in cl and cl[a1] in p2_articles:
            n += 1
            break
    return n*1.0/min((len(p1.infobox.keys()),len(p2.infobox.keys())))

#def reversed_article_similarity(p1, p2):
#    return len((set(p1.articles) & set(p2.articles)))*1.0/min(len(p1.articles), len(p2.articles))

def reversed_article_similarity(p1, p2):
    return len((set(p1.infobox.keys()) & set(p2.infobox.keys())))*1.0/min(len(p1.infobox.keys()), len(p2.infobox.keys()))

def domain_similarity(p1, p2, cl):
    print "domain_similarity"
    return normalized_google_distance(p1.concepts, p2.concepts)

def range_similarity(p1, p2):
    return normalized_google_distance(p1.values, p2.values)

def value_similarity(p1, p2, cl):
    s = 0
    for v in p1.infobox.values():
        if v in cl:
            # is article type
            return article_type_value(p1, p2, cl)
    for v in p1.infobox.values(): 
        if has_number(v):
            return number_type_value(p1, p2, cl)
    return literal_type_value(p1, p2, cl)

def value_similarity2(p1, p2, cl):
    N = 0
    s = 0

    with codecs.open("property-article-value.dat", "a", "utf-8") as fo:
        p1_list = []
        for a1, v1 in p1.infobox.iteritems():
            p1_list.append(a1+"::="+v1)
        fo.write(p1.label+"\t"+";;;".join(p1_list)+"\n")

        p2_list = []
        for a2, v2 in p2.infobox.iteritems():
            p2_list.append(a2+"::="+v2)
        fo.write(p2.label+"\t"+";;;".join(p2_list)+"\n")

    for a1, v1 in p1.infobox.iteritems():
        v2 = None
        if a1 in p2.infobox:
            N += 1
            v2 = p2.infobox[a1]
        elif a1 in cl and cl[a1] in p2.infobox:
            N += 1
            a2 = cl[a1]
            v2 = p2.infobox[a2]
        if v2 == None:
            continue
        if v1 in cl and v2 == cl[v1]: #article type
            s += 1
        elif has_number(v1) and has_number(v2):
            nums1 = re.findall(r'\d+', v1) 
            nums2 = re.findall(r'\d+', v2)

            n = 0
            for n1 in nums1:
                for n2 in nums2:
                    if len(set(n1)&set(n2)) > 0:
                        n += 1
                        break
            s += n * 1.0/min(len(nums1), len(nums2))
        else:
            s += edit_distance_similarity(v1, v2)
    return s * 1.0 / N if N > 0 else 0


def article_type_value(p1, p2, cl):
    print 'article_type'
    N = 0
    c = 0
    for a1, v1 in p1.infobox.iteritems():
        if a1 in p2.infobox:
            N += 1
            v2 = p2.infobox[a1]
            if v1 in cl and v2 == cl[v1]:
                c += 1
        elif a in cl and cl[a] in p2.infobox:
            N += 1
            a2 = cl[a]
            v2 = p2.infobox[a2]
            if v1 in cl and v2 == cl[v1]:
                c += 1

    #v1, v2 = set(p1.infobox.values()), set(p2.infobox.values())
    #for v in set(p1.infobox.values()):
    #    if v in cl:
    #        v1.remove(v)
    #        v1.add(cl[v])
    #
    #return normalized_google_distance(v1, v2)
    return c*1.0/N if N > 0 else 0

#def literal_type_value(p1, p2):
#    print 'literal_type'
#    words1 = [re.findall(r'\w+', v) for v in p1.zhvalues]
#    words2 = [re.findall(r'\w+', v) for v in p2.values]
#
#    zhs1 = [re.findall(ur'[\u4e00-\u9fff]+', v) for v in p1.zhvalues]
#    #print "zhs1:", zhs1
#    zhs2 = [re.findall(ur'[\u4e00-\u9fff]+', v) for v in p2.values]
#    #print "zhs2:", zhs2
#
#    n = 0
#
#    for i in range(len(words1)):
#        for j in range(len(words2)):
#            if words1[i] == words2[j] or zhs1[i] == zhs2[j]:
#                n += 1
#                break
#
#    return n * 1.0/min(len(zhs1), len(zhs2))

def literal_type_value(p1, p2):
    print 'literal_type'
    values1, values2 = p1.zhvalues, p2.values
    
    if len(values1) == 0 or len(values2) == 0:
        return 0 

    s = 0
    for v1 in values1:
        for v2 in values2:
            s += edit_distance_similarity(v1, v2)

    return 1 - s/(len(values1) * len(values2))

def literal_type_value2(p1, p2, cl):
    print 'literal_type'
    N = 0
    s = 0
    for a1, v1 in p1.infobox.iteritems():
        if a1 in p2.infobox:
            N += 1
            v2 = p2.infobox[a1]
            s += edit_distance_similarity(v1, v2)
        elif a in cl and cl[a] in p2.infobox:
            N += 1
            a2 = cl[a]
            v2 = p2.infobox[a2]
            s += edit_distance_similarity(v1, v2)

    return s*1.0 / N if N > 0 else 0

def number_type_value(p1, p2):
    print 'number_type'
    
    nums1 = [re.findall(r'\d+', v) for v in p1.values]
    nums2 = [re.findall(r'\d+', v) for v in p2.values]

    n = 0
    for n1 in nums1:
        for n2 in nums2:
            if len(set(n1)&set(n2)) > 0:
                n += 1
                break
    return n * 1.0/min(len(nums1), len(nums2))

def popular_similarity(p1, p2):
    print 'popular similarity'
    if p1.popular == None or p2.popular == None:
        print 'No popular value for properties'
        return 0
    else:
        print p1.label, p1.popular, p2.label, p2.popular
        return abs(p1.popular - p2.popular)


if __name__=="__main__":
    print is_date('1991年1月23日')
