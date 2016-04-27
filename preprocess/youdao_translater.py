#/usr/bin/env python
#-*- coding:utf-8 -*-
 
import httplib
import md5
import urllib, urllib2
import random
import json
import socket

import time
from functools import wraps
import configs

def retry(ExceptionToCheck, tries=4, delay=3, backoff=2, logger=None):
    """Retry calling the decorated function using an exponential backoff.

    http://www.saltycrane.com/blog/2009/11/trying-out-retry-decorator-python/
    original from: http://wiki.python.org/moin/PythonDecoratorLibrary#Retry

    :param ExceptionToCheck: the exception to check. may be a tuple of
        exceptions to check
    :type ExceptionToCheck: Exception or tuple
    :param tries: number of times to try (not retry) before giving up
    :type tries: int
    :param delay: initial delay between retries in seconds
    :type delay: int
    :param backoff: backoff multiplier e.g. value of 2 will double the delay
        each retry
    :type backoff: int
    :param logger: logger to use. If None, print
    :type logger: logging.Logger instance
    """
    def deco_retry(f):

        @wraps(f)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                except ExceptionToCheck, e:
                    print e
                    msg = "%s, Retrying in %d seconds..." % (str(e), mdelay)
                    if logger:
                        logger.warning(msg)
                    else:
                        print msg
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return f(*args, **kwargs)

        return f_retry  # true decorator

    return deco_retry


class YoudaoTranslater:
    appkey = configs.YOUDAO_API_KEY
    keyfrom = configs.YOUDAO_API_KEYFROM

    def __init__(self):
        self.httpClient = httplib.HTTPConnection('fanyi.youdao.com', 80, timeout=10)

    #@retry(Exception, tries=4, delay=3, backoff=2)
    #@retry((socket.timeout, httplib.CannotSendRequest), tries=4, delay=5, backoff=2)
    def translate(self, q):
        try:
            q = q.encode('utf-8')
        except:
            pass
        myurl = 'openapi.do'
        doctype = 'json'
        myurl = myurl+'?key='+YoudaoTranslater.appkey+'&keyfrom='+YoudaoTranslater.keyfrom+'&doctype='+doctype+'&q='+urllib.quote(q)
        print myurl
 
        try:
            self.httpClient.request('GET', myurl)
     
            #response是HTTPResponse对象
            response = self.httpClient.getresponse()
            res = response.read()
            print res
            return self.parse_json(res)
        except Exception, e:
            print e
            return None

    def close(self):
        if self.httpClient:
            self.httpClient.close()

    def parse_json(self, res):
        d = {}
        j = json.loads(res)
        print j

class YoudaoTranslater:
    appkey = configs.YOUDAO_API_KEY
    keyfrom = configs.YOUDAO_API_KEYFROM

    def __init__(self):
        pass

    def translate(self, q):
        doctype="json"
        url = "http://fanyi.youdao.com/openapi.do"+ '?key='+YoudaoTranslater.appkey+'&keyfrom='+YoudaoTranslater.keyfrom+'&type=data&doctype='+doctype+'&version=1.1&q='+\
                urllib.quote(q)
        j = urllib.urlopen(url).read()
        print j
        return self.parse_json(j)

    def parse_json(self, j):
        d = {}
        Json = json.loads(j)
        if 'web' in Json:
            print Json['web']
            d[Json['query']] = Json['web'][0]['value']
        else:
            d[Json['query']] = Json['translation']
        return d


if __name__=="__main__":
    yd = YoudaoTranslater()
    print yd.translate('name')
    print yd.translate('apple')
