# -*- coding: utf-8 -*-
"""
Created on Thu Nov 03 22:55:17 2016

@author: molata
"""
import codecs
import os
from htmlSoup import HtmlSoup
from bs4 import BeautifulSoup

class TextBuild(object):
    "This txt for build string"
    
    def __init__(self):
        self.text = ''
        
    def buildSection(self, fileObject, sectionName = "", articles = []):
        #S1 write sectionName
        textTitle = self.buildTitle(sectionName)
        fileObject.write(textTitle + "" + '\r\n')
        #S2 write articles
        formatArtile = '[color=#ff0000][font=Arial][size=4]'
        i = 0
        for artile in articles:
            try:
                textArticle = self.buildArticle(artile, i + 1)
                if i == 0:
                    fileObject.write(formatArtile)
            except TypeError:
                i = i - 1
            fileObject.write(textArticle + '' + '\r\n')
            i = i + 1
        fileObject.write('\r\n')
        
    def buildTitle(self, titleName = ""):
        title = "[font=Arial][size=4][color=#ff0000][b]title[/b][/color][/size][/font]"
        title = title.replace('title', titleName)
        return title
        
    def buildArticle(self, dictArticle = {}, inx = 1):
        article = 'inx. title1[backcolor=transparent][backcolor=transparent][url=link]title2[/url][/backcolor] [/backcolor]'
        article = article.replace('inx', str(inx))
        article = article.replace('title1', dictArticle['title1'])
        article = article.replace('title2', dictArticle['title2'])
        article = article.replace('link', dictArticle['url'])
        return article
        

        
if __name__ == '__main__':
    """
    through bs4 get section name in economist home pages
    """  
    soup = BeautifulSoup(open('section.html'), 'lxml')
    baseUrl = 'http://www.economist.com'
    htmlSoup = HtmlSoup(soup.div, baseUrl)
    sectionName = htmlSoup.getSection()
    articles = htmlSoup.getArticles()
    fileObject = codecs.open('TE.txt', 'w', 'utf-8')
    
    textBuild = TextBuild()
    textBuild.buildSection(fileObject, sectionName, articles)

    fileObject.close()
    
            
            
        
        
        