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


class BaiduTranslater:
    appid = configs.BAIDU_APPID
    secretKey = configs.BAIDU_SECRET_KEY

    def __init__(self):
        self.httpClient = httplib.HTTPConnection('api.fanyi.baidu.com', 80, timeout=5)

    #@retry(Exception, tries=4, delay=3, backoff=2)
    @retry((socket.timeout, httplib.CannotSendRequest), tries=4, delay=5, backoff=2)
    def translate(self, q, fromLang='en', toLang='zh'):
        try:
            q = q.encode('utf-8')
        except:
            pass
        myurl = '/api/trans/vip/translate'
        salt = random.randint(32768, 65536)
        sign = BaiduTranslater.appid+q+str(salt)+BaiduTranslater.secretKey
        m1 = md5.new()
        m1.update(sign)
        sign = m1.hexdigest()
        myurl = myurl+'?appid='+BaiduTranslater.appid+'&q='+urllib.quote(q)+'&from='+fromLang+'&to='+toLang+'&salt='+str(salt)+'&sign='+sign
 
        #try:
        self.httpClient.request('GET', myurl)
     
        #response是HTTPResponse对象
        response = self.httpClient.getresponse()
        j = response.read()
        return self.parse_json(j)
        #except Exception, e:
        #    print e
        #    return None

    def close(self):
        if self.httpClient:
            self.httpClient.close()

    def parse_json(self, j):
        d = {}
        Json = json.loads(j)
        if not 'trans_result' in Json:
            return d
        for item in Json['trans_result']:
            src, dst = item['src'], item['dst']
            d[src] = dst
        return d


if __name__=="__main__":
    bt = BaiduTranslater()
    print bt.translate('apple')
