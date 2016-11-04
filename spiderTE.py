#! /usr/bin/env python
# -*- coding=utf-8 -*- 
# @Author pythontab.com

import urllib2
from bs4 import BeautifulSoup
import time
import codecs
from htmlSoup import HtmlSoup
from textBuild import TextBuild

def spider_get(url):
    """
    通过urllib的方式捕获网页的内容
    """
    
    req_header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
'Accept':'text/html;q=0.9,*/*;q=0.8',
'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
'Connection':'close',
'Referer':None #注意如果依然不能抓取的话，这里可以设置抓取网站的host
}
    req_timeout = 5
    try:
        req = urllib2.Request(url,None,req_header)
        resp = urllib2.urlopen(req,None,req_timeout)
    except :
        print "a bad network environment! Please try again!" + '\t' + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        time.sleep(5)
        exit()
    home = resp.read().decode('utf-8')
    return home

if __name__ == '__main__':
    """
    through bs4 get section name in economist home pages
    """  
    print "Launch success!" + '\t' + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    #S1 spider html from www
    url = "http://www.economist.com/printedition"
    baseUrl = "http://www.economist.com"
    html = spider_get(url)
    html_soup = BeautifulSoup(html, "lxml")
    #html_soup = BeautifulSoup(open('html.html'), "lxml")
    
    #S2 find all articles
    value = 'section first'
    soupSectionTitles = html_soup.select('div > h4')
    
    #S3 write to txt
    fileObject = codecs.open('economist.txt', 'w', 'utf-8')
    textBuild = TextBuild()
    for soupSectionTitle in soupSectionTitles:
        soupSection = soupSectionTitle.find_parent()
        htmlSoup = HtmlSoup(soupSection, baseUrl)
        sectionName = htmlSoup.getSection()
        sectionContent = htmlSoup.getArticles()
        if sectionName != 'Letters' and sectionName != 'Briefing' and sectionName != 'China' and sectionName != 'Economic and financial indicators' and sectionName !='The world this week':
            textBuild.buildSection(fileObject, sectionName, sectionContent)    
    
    #S4 add warning
    with codecs.open('warn.txt', 'r', 'utf-8') as warnObject:
        fileObject.write(warnObject.read() + '\n')
    fileObject.close()
    
    #S5 successful
    print "spider successful!"
        
        
        
        
    
    


    