#!/usr/bin/env python
#-*-coding:utf-8-*-

import requests

headers = {
    'User-Agent	' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0', 
}

# headers={
# 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
# 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
# 'Accept-Language':'en-US,en;q=0.5',
# 'Accept-Encoding':'gzip',
# 'DNT':'1',
# 'Connection':'close'
# }

def get_html(url, Referer_url=None):
    '''get_html(url),download and return html'''
    if Referer_url:
        headers['Referer'] = Referer_url
    req = requests.get(url, headers=headers)
    # print(req.content)
    return req.content
