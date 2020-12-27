#!/usr/bin/env python
#-*-coding:utf-8-*-

from bs4 import BeautifulSoup
from soupsieve.css_match import RE_NOT_EMPTY
import downloader
from aria2download import add_download_task, login_aria2,print_download_task
from functions_translate import translate_process

def _get_cili_url(soup):
    """get_cili(soup).get the ajax url and Referer url of request"""
    # print(soup)
    # https://www.javbus.com/ajax/uncledatoolsbyajax.php?gid=45137661549&lang=zh&img=https://pics.javbus.com/cover/80c1_b.jpg&uc=0&floor=581

    
    ajax_get_cili_url = 'https://www.javbus.com/ajax/uncledatoolsbyajax.php?lang=zh'
    ajax_data = str(soup.select('script')[8].contents[0])
    # print(ajax_data)
    # print(type(ajax_data))
    listsplit=ajax_data.split(';')[:-1]
    # print(ajax_data)
    for l in ajax_data.split(';')[:-1]:
        ajax_get_cili_url += '&%s' % l[7:].replace("'","").replace(' ','')
    # print (ajax_get_cili_url)  
    return ajax_get_cili_url


def _parser_magnet(html):
    """parser_magnet(html),get all magnets from a html and return the str of magnet"""

    #存放磁力的字符串
    magnet = ''
    soup = BeautifulSoup(html,"html.parser")
    # print(soup)
    try:
        for td in soup.select('td[width="70%"]'):
            # print(td)
            tdsibiling=td.findNext('td')
            # print(tdsibiling)
            mtag=tdsibiling.a.get_text()
            # print(mtag)
            if mtag == '\n':
                msize='1GB' #data is missing
            else:
                msize=mtag.split('                \t')[1] #need to add exception handler for no size case
            # print(msize)
            # print(msize)
            # print(td.a['href'])
            mlink=td.a['href']
            # aria2=login_aria2()
            # add_download_task(aria2,mlink)
            magnet += mlink +'\n'+ msize+'\n'
            # print(magnet)
        return magnet
    except:
        return ""

def get_next_page_url(entrance, html):
    """get_next_page_url(entrance, html),return the url of next page if exist"""
    print("done the page.......")
    soup = BeautifulSoup(html, "html.parser")
    next_page = soup.select('a[id="next"]')
    if next_page:
        next_page_link = next_page[0]['href'].split('/')[-2:]
        next_page_link = '/'+'/'.join(next_page_link)
        next_page_url = entrance + next_page_link
        return next_page_url
    return None

def parser_homeurl(html):
    """parser_homeurl(html),parser every url on every page and yield the url"""

    soup = BeautifulSoup(html,"html.parser")
    for url in soup.select('a[class="movie-box"]'):
        yield url['href']


def parser_homeurl_today(html):
    """parser_homeurl(html),parser every url on every page and yield the url"""

		#   <button class="btn btn-xs btn-primary" disabled="disabled" title="包含高清HD的磁力連結">高清</button>
		#   <button class="btn btn-xs btn-danger " disabled="disabled" title="包含最新出種的磁力連結">昨日新種</button>
		#   <button class="btn btn-xs btn-success " disabled="disabled" title="包含最新出種的磁力連結">今日新種</button>


    soup = BeautifulSoup(html,"html.parser")
    for url in soup.select('a[class="movie-box"]'):
        # print(url)
        for button in url.findAll("button",{"class":"btn-xs"}):
        # for button in url.findAll("button",{"class":"btn-danger"}):
            flag_today_new=button.get_text()
            # print(button.get_text())
            if flag_today_new=='今日新種':
            # if flag_today_new=='昨日新種':
                yield url['href']

def if_this_page_has_word(substring,html):
    soup = BeautifulSoup(html,"html.parser")
    soup_string = str(soup)
    if substring in soup_string:
        print("Next page contains word:",substring )
        return True
    else:
        return False

def parser_homeurl_yesterday(html):
    """parser_homeurl(html),parser every url on every page and yield the url"""

    soup = BeautifulSoup(html,"html.parser")
    for url in soup.select('a[class="movie-box"]'):
        # print(url)
        # for button in url.findAll("button",{"class":"btn-success"}):
        for button in url.findAll("button",{"class":"btn-xs"}):
            flag_today_new=button.get_text()
            # print(button.get_text())
            # if flag_today_new=='今日新種':
            if flag_today_new=='昨日新種':
                yield url['href']




def parser_content(html):
    """parser_content(html),parser page's content of every url and yield the dict of content"""

    soup = BeautifulSoup(html, "html.parser")

    categories = {}

    code_name_doc = soup.find('span', text="識別碼:")
    code_name = code_name_doc.parent.contents[2].text if code_name_doc else ''
    categories['識別碼'] = code_name
    #code_name = soup.find('span', text="識別碼:").parent.contents[2].text if soup.find('span', text="識別碼:") else ''

    date_issue_doc = soup.find('span', text="發行日期:")
    date_issue = date_issue_doc.parent.contents[1].strip() if date_issue_doc else ''
    categories['發行日期'] = date_issue
    #date_issue = soup.find('span', text="發行日期:").parent.contents[1].strip() if soup.find('span', text="發行日期:") else ''

    duration_doc = soup.find('span', text="長度:")
    duration = duration_doc.parent.contents[1].strip() if duration_doc else ''
    categories['長度'] = duration
    #duration = soup.find('span', text="長度:").parent.contents[1].strip() if soup.find('span', text="長度:") else ''

    director_doc = soup.find('span', text="導演:")
    director = director_doc.parent.contents[2].text if director_doc else ''
    categories['導演'] = director
    #director = soup.find('span', text="導演:").parent.contents[2].text if soup.find('span', text="導演:") else ''

    manufacturer_doc = soup.find('span', text="製作商:")
    manufacturer = manufacturer_doc.parent.contents[2].text if manufacturer_doc else ''
    categories['製作商'] = manufacturer
    #manufacturer = soup.find('span', text="製作商:").parent.contents[2].text if soup.find('span', text="製作商:") else ''

    publisher_doc = soup.find('span', text="發行商:")
    publisher = publisher_doc.parent.contents[2].text if publisher_doc else ''
    categories['發行商'] = publisher
    #publisher = soup.find('span', text="發行商:").parent.contents[2].text if soup.find('span', text="發行商:") else ''

    series_doc = soup.find('span', text="系列:")
    series = series_doc.parent.contents[2].text if series_doc else ''
    categories['系列'] = series
    #series = soup.find('span', text="系列:").parent.contents[2].text if soup.find('span', text="系列:") else ''

    genre_doc = soup.find('p', text="類別:")
    genre =(i.text.strip() for i in genre_doc.find_next('p').select('span')) if genre_doc else ''
    #genre =(i.text.strip() for i in soup.find('p', text="類別:").find_next('p').select('span')) if soup.find('p', text="類別:") else ''
    genre_text = ''
    for tex in genre:
        genre_text += '%s   ' % tex 
    categories['類別'] = genre_text

    actor_doc = soup.select('span[onmouseover^="hoverdiv"]')
    actor = (i.text.strip() for i in actor_doc) if actor_doc else ''
    #actor = (i.text.strip() for i in soup.select('span[onmouseover^="hoverdiv"]')) if soup.select('span[onmouseover^="hoverdiv"]') else ''
    actor_text = ''
    for tex in actor:
        actor_text += '%s   ' % tex 
    categories['演員'] = actor_text

    title_doc = soup.find('h3')
    title=title_doc.contents[0]
    categories['Title'] = title
    
    empty_str=''
    categories['Title_ch'] = translate_process(empty_str.join(title.split(' ')[1:]))

    
    #网址加入字典
    url = soup.select('link[hreflang="zh"]')[0]['href']
    categories['URL'] = url
    
    #将磁力链接加入字典
    magnet_html = downloader.get_html(_get_cili_url(soup), Referer_url=url)
    # print(magnet_html)
    # magnet_html = downloader.get_html('https://www.javbus.com/ajax/uncledatoolsbyajax.php?gid=45137661677&lang=zh&img=https://pics.javbus.com/cover/80c1_b.jpg&uc=0&floor=100', Referer_url=url)
    # print(magnet_html)

    magnet = _parser_magnet(magnet_html)
    
    categories['磁力链接'] = magnet
    print(categories) 
    return categories


