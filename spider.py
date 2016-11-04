#! /usr/bin/env python
# -*- coding=utf-8 -*- 
# @Author pythontab.com

import urllib2
from bs4 import BeautifulSoup
import re
import time, datetime
import codecs
import os
url = "http://www.economist.com"

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

def time_convert(time):
    """
    convert 'Mar 12th 2016' to number like : 20160312
    
    """
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Dec']
    date_tuple = re.findall('([A-Za-z]+)\s+([0-9]+)[a-z]+\s+([0-9]+)', time)[0]
    date_list = list(date_tuple)
    
    date_deci_num = int(date_list[2]) * 10000 + (months.index(date_list[0]) + 1) * 100 + int(date_list[1])
    return date_deci_num
assert time_convert('Mar 12th 2016') == 20160312
assert time_convert('Jan 23rd 2016') == 20160123

def string_makeup(str_raw):
    """
    use re to renew the raw string 
    like : '            Chinese property            ' to 'Chinese property'
    """
    p = re.compile(r'([A-Z].*\w+)')
    str_mature = p.search(str_raw).group()
    return str_mature

assert string_makeup('\xa0For whom the bubble blows') == 'For whom the bubble blows'
assert string_makeup('            India’s young            ') == 'India’s young'

def time_fit(article_time):
    """
    judge whether current article date is in range, 
    return 0: too early
    return 1: well fit
    return 2: too old
    """
    today = datetime.datetime.now()
    today_weekday = today.weekday()
    if (today_weekday >= 4):
        mon_to_today = 1 - today_weekday
        sun_to_today = 5 - today_weekday
    else:
        mon_to_today = 1 - today_weekday - 7
        sun_to_today = 5 - today_weekday -7
        
    mon = today + datetime.timedelta(days = mon_to_today)
    sun = today + datetime.timedelta(days = sun_to_today)
    
    today_date_int = int(today.strftime("%Y%m%d"))
    mon_date_int = int(mon.strftime("%Y%m%d"))
    sun_date_int = int(sun.strftime("%Y%m%d"))
    if (sun_date_int <= article_time <= sun_date_int):
        return 1
    elif (article_time < mon_date_int) :
        return 2
    else :
        return 0

def spider_article(section_base_link, section_base_name, post_dict = {}):
    """
    通过文章的链接初步确定一些符合要求的文章
    再通过时间最终确定，最后还要挖出文章的标题
    <a href="/news/finance-and-economics/21694530-house-prices-are-soaring-big-cities-oversupply-plagues-much">
          <div class="section-teaser-logo">
        <img src="http://cdn.static-economist.com/sites/default/files/imagecache/90_by_90/images/print-edition/20160312_FNP001_0.jpg" alt="Chinese property" title=""  class="imagecache imagecache-90_by_90" width="90" height="90" />      </div>
        <div class="section-teaser-content">
    
    
    <time class="date-created">Mar 12th 2016</time>
    <h3 class="fly-title">
                Commodities            <span class="headline"> Steel chrysanthemums</span> </h3>
                
    links: 'http://www.economist.com/sections/business-finance?page=1'
        'http://www.economist.com/sections/business-finance'
    """
    pages_count = 0  #how many pages we spider
    spider_stop_bool = False     #judge if stop here
    
    while(True):
        if pages_count ==0:
            section_link = section_base_link
        else:
            section_link = section_base_link + '?page=' + str(pages_count)  # brower link
            
        #print section_link
        #print section_name
        pages_count += 1    
        
        section_xml = spider_get(section_link)
        section_soup = BeautifulSoup(section_xml, "lxml")
        articles_xml = section_soup.find_all('article')
        for article_xml in articles_xml:
            article_link_xml = article_xml.attrs['data-href-redirect']
            link_re_type = '/news/' + section_base_name + '/.+'
            #link_re_type = '/news/business/.*'        
            if re.match(link_re_type, article_link_xml):  # conditon1: 链接的类型是否符合
                
                try:
                    article_date = article_xml.find('time').contents[0]  
                    headline = article_xml.find('h3').contents[0].strip('\n')
                    span = article_xml.find('span').contents[0].strip('\n')
                    section_name = article_xml.find_all('span')[1].contents[0].strip()
                    section_name = string_makeup(section_name)
                except: 
                    continue

                time_deci_num = time_convert(article_date) 
                if(time_fit(time_deci_num) == 1):    # 更加关键的是时间是否符合
                    try:
                        headline = string_makeup(headline)   #可能会出现空集的
                        span = string_makeup(span)
                        link = re.findall(link_re_type, article_link_xml)[0].strip('\n') 
                        link = url + link

                        dict_article = {}
                        dict_article['headline'] = headline
                        dict_article['span'] = span 
                        dict_article['link'] = link
                        
                        if not post_dict.has_key(section_name):
                            post_dict[section_name] = []
                        post_dict[section_name].append(dict_article)
                    except:
                        pass                   
                elif (time_fit(time_deci_num) == 2):
                    spider_stop_bool = True
                    break
                    
        if spider_stop_bool:         #jump out this section
            break
        if pages_count >= 8:
            break
    #print post_dict
    #print section_name
    return post_dict
#assert spider_article('http://www.economist.com/sections/culture', 'books-and-arts') != {}

def spider_special_report(section_base_link, post_dict = {}):
    """
    通过文章的链接初步确定一些符合要求的文章
    再通过时间最终确定，最后还要挖出文章的标题
<li class="clearfix views-row views-row-1 views-row-odd views-row-first">
</noscript></div>  
  <div class="views-field-field-special-report-published-value">
                <span class="field-content"><span class="date-display-single">Feb 27th 2016</span></span>
  </div>
</div>
<div class="clearfix">
    <ul class="grid-5 grid-first">
        <li><a href="/news/special-report/21693411-joko-widodo-was-elected-shake-up-indonesias-politics-and-make-his-country-richer-he">Indonesia: Jokowi’s moment</a></li>
        <li><a href="/news/special-report/21693409-jokowis-independence-double-edged-sword-lone-fighter">Politics: Lone fighter</a></li>
        <li><a href="/news/special-report/21693410-roots-corruption-go-deep-and-wide-setya-show">Corruption: The Setya show</a></li>
        <li><a href="/news/special-report/21693405-secure-growth-it-needs-indonesia-must-resist-its-protectionist-urges-roll-out">Business and economics: Roll out the welcome mat</a></li>
      </ul>
      <ul class="grid-5">
        <li><a href="/news/special-report/21693404-after-decades-underinvestment-infrastructure-spending-picking-up-last">Infrastructure: The 13,466-island problem</a></li>
        <li><a href="/news/special-report/21693407-indonesias-stance-towards-rest-world-has-become-more-assertive-less-talk-more">Foreign policy: Less talk, more action</a></li>
        <li><a href="/news/special-report/21693412-until-politicians-call-halt-indonesias-forests-will-keep-burning-world-fire">Forests: A world on fire</a></li>
        <li><a href="/news/special-report/21693406-it-will-take-ruthless-determination-well-luck-realise-indonesias-potential">Looking ahead: The country of the future</a></li>
      </ul>
  </div>
</li>

Indonesia: Jokowi’s moment
    """
    
    section_xml = spider_get(section_base_link)
    section_soup = BeautifulSoup(section_xml, "lxml")
    articles_xml = section_soup.find_all('ul')
    
    for article_ul_xml in articles_xml:
        articles_xml = article_ul_xml.find('li')
        try:
            if articles_xml['class'] == ['clearfix', 'views-row', 'views-row-1', 'views-row-odd', 'views-row-first']:
                spans = articles_xml.find_all('span')
                for span in spans:
                    try:
                        if span['class'] == ['field-content']:
                            article_date = span.find('span').string
                    except:
                        pass
                time_deci_num = time_convert(article_date) 
                if(time_fit(time_deci_num) == 1):    # 更加关键的是时间是否符合
                    lis = articles_xml.find_all('li')
                    for li in lis:
                        try:
                            name = li.find('a').string
                            headline = re.findall('([A-Z]+.*):.*', name)[0]
                            span = re.findall('.*:\s+([A-Z].*[a-z]+)', name)[0]
                            link = url + li.find('a')['href']
                            section_name = 'Special report'
                        except KeyError:
                            pass

                        dict_article = {}
                        dict_article['headline'] = headline
                        dict_article['span'] = span 
                        dict_article['link'] = link
                        if not post_dict.has_key(section_name):
                            post_dict[section_name] = []
                        post_dict[section_name].append(dict_article)
                
        except :
            pass
    return post_dict
#assert spider_special_report('http://www.economist.com/printedition/specialreports') == {}

def make_section(section_list, section_name, file_object):
    """
    Function: convert to a new type
    contents: 
             [font=Arial][size=4][color=#ff0000][b]Leaders[/b][/color][/size][/font][font=Arial][size=4][color=#ff0000]
[/color][/size][/font]
[color=#ff0000][font=Arial][size=4]1. After Moore’s law[backcolor=transparent][backcolor=transparent][url=http://www.economist.com/news/leaders/21694528-era-predictable-improvement-computer-hardware-ending-what-comes-next-future]The future of computing[/url][/backcolor] [/backcolor]
2. The Petrobras scandal[backcolor=transparent][backcolor=transparent][url=http://www.economist.com/news/leaders/21694535-justice-not-political-war-should-determine-fate-brazils-government-interrogating-lula]Interrogating Lula[/url][/backcolor][/backcolor]
3. Farming in Africa[backcolor=transparent][backcolor=transparent][url=http://www.economist.com/news/leaders/21694539-after-many-wasted-years-african-agriculture-improving-quickly-here-how-keep-trend]Miracle grow[/url][/backcolor] [/backcolor]
4. China’s economy[backcolor=transparent][backcolor=transparent][url=http://www.economist.com/news/leaders/21694533-leaning-towards-stimulus-rather-reform-chinas-leaders-are-storing-up]Ore-inspiring[/url][/backcolor][/backcolor]
5. Europe’s migrant crisis[backcolor=transparent][backcolor=transparent][url=http://www.economist.com/news/leaders/21694536-european-bargain-turkey-controversial-offers-best-hope-ending-migrant]A messy but necessary deal[/url][/backcolor][/backcolor]
    
    """
    section_type = '[font=Arial][size=4][color=#ff0000][b]section_title[/b][/color][/size][/font][font=Arial][size=4][color=#ff0000]'
    section_space = '[/color][/size][/font]'
    first_article_head = '[color=#ff0000][font=Arial][size=4]' 
    
    
    section = section_type.replace('section_title', section_name)
    file_object.write(section + "\n")    #write headline
    file_object.write(section_space + "\n")
    article_count = 1
    for article_dict in section_list:
        headline = article_dict['headline']
        span = article_dict['span']
        link = article_dict['link']
        
        article = 'count. headline[backcolor=transparent][backcolor=transparent][url=link]span[/url][/backcolor] [/backcolor]'
        article = article.replace('count', str(article_count))
        article = article.replace('headline', headline)
        article = article.replace('span', span)
        article = article.replace('link', link)# replace index, article_headline, article_link, article_span
        if article_count == 1:
            file_object.write(first_article_head + article + "\n")
        else:
            file_object.write(article + "\n")
        #print article
        article_count += 1
      
    file_object.write("\n")


if __name__ == '__main__':
    """
    through bs4 get section name in economist home pages
    """   
    print "Launch success!" + '\t' + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    home = spider_get(url)
    home_soup = BeautifulSoup(home, "lxml")
    
    """
    some we need to know: these sections are not equal to whose section we will release!

    <li class="even"><a href="/sections/united-states">United States</a></li>
    <li><a href="/sections/britain">Britain</a></li>
    """
    sections_link = []
    sections_xml = home_soup.find_all('a')
    print sections_xml
    for section_xml in sections_xml:
        section_re_type = '<a\s+href="(/sections/\S+)">.*</a>'  # normal sections
        print(str(section_xml))
        #if re.match(section_re_type, str(section_xml)):
        section_link = url + re.findall(section_re_type, str(section_xml))[0]
        sections_link.append(section_link)    
    sections_link.append(url + "/printedition/specialreports")        
    #print sections_link       
    
    """
    find concrete section 
    warn: we need to spider pages more than one, we should stop it base time
    methods: 1)because we will do this as quickly as we can , so we can brower from first page
             2)if time return less, jump out 

    """
    # data struct define here
    sections = {}
    for section_link in sections_link:
        print section_link
        if section_link == 'http://www.economist.com/sections/business-finance':
            section_name = 'finance-and-economics'
            #sections[section_name] = spider_article(section_link, section_name)
            sections = spider_article(section_link, section_name, sections)
            section_name = 'business'
            #sections[section_name] = spider_article(section_link, section_name)
            sections = spider_article(section_link, section_name, sections)
            section_name = 'business-and-finance'
            #sections['business'] = spider_article(section_link, section_name)
            sections = spider_article(section_link, section_name, sections)
        elif section_link == 'http://www.economist.com/sections/china' or \
        section_link == 'http://www.economist.com/sections/china':
            pass
        elif section_link == 'http://www.economist.com/printedition/specialreports':
            sections = spider_special_report(section_link, sections)
        else:
            if section_link == 'http://www.economist.com/sections/culture': 
                section_name = 'books-and-arts'
            elif section_link == 'http://www.economist.com/sections/middle-east-africa':
                section_name = 'middle-east-and-africa'
            elif section_link == 'http://www.economist.com/sections/science-technology':
                section_name = 'science-and-technology'
            else:
                section_name = re.findall('sections/(\S+[a-z]+)', section_link)[0]
                
            #sections[section_name] = spider_article(section_link, section_name)
            sections = spider_article(section_link, section_name, sections)
    #print sections
    """
    function: build post
    """
    file_object = codecs.open('economist.txt', 'w', 'utf-8')
    sections_name = ('Leaders', 'United States', 'The Americas', 'Asia', 'Middle East and Africa', \
                    'Europe', 'Britain', 'International','Special report', 'Business', 'Finance and economics', 'Science and technology', \
                    'Books and arts', 'Obituary' )
    for section_name in sections_name: 
        try:
            section_list = sections[section_name]
            make_section(section_list, section_name, file_object)
        except KeyError:
            pass
    with codecs.open('warn.txt', 'r', 'utf-8') as warn_object:
        file_object.write(warn_object.read() + '\n')
    file_object.close()

    os.system("cls")
    title = u'                       Thanks for BY_0505新                       '
    content = '                                  -------- All Afiers like you!             '
    print title.encode('gbk')
    print content
    time.sleep(8)

    
