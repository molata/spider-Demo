# -*- coding: utf-8 -*-
"""
Created on Thu Nov 03 15:53:45 2016

@author: molata
"""
from bs4 import BeautifulSoup

class HtmlSoup(object):
    "This is a class for handle a section"
       
    def __init__(self, soup, url):
        self.baseUrl = url
        self.soup = soup
        
    def getSection(self):
        soupSection = self.soup.h4
        sectionName = soupSection.string
        return sectionName
        
    def getArticles(self):
        articles = []
        soupArticles = self.soup.select('div[class="article"]')
        for soupArticle in soupArticles:
            article = {}
            try:
                article['title1'] = soupArticle.findPreviousSibling().string
                article['title2'] = soupArticle.a.string
                newUrl = soupArticle.a['href']
                url = self.buildLink(newUrl)
                article['url'] = url
                articles.append(article)  
            except TypeError:
                pass
        return articles       
            
    def buildLink(self, newUrl):
        return self.baseUrl + '' + newUrl
        

        
if __name__ == '__main__':
    """
    through bs4 get section name in economist home pages
    """  
    soup = BeautifulSoup(open('section.html'), 'lxml')
    baseUrl = 'http://www.economist.com'
    htmlSoup = HtmlSoup(soup.div, baseUrl)
    print htmlSoup.getSection()
    print htmlSoup.getArticles()
        

    
