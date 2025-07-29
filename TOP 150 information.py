import random
import time
from lxml import etree
import requests
import re
import json

cookie_str='bid=D2C68h3GXLc; _pk_id.100001.4cf6=f6bd1d492074adfe.1743937597.; __yadk_uid=nEIaZRoV3eBSNKSpH8RPGdMBt7UPacpR; ll="118159"; _vwo_uuid_v2=DBAB29FAEA586C11E9E5BCB2DC84FF170|a4a555456da865944e7b370dff30b916; __utmc=30149280; __utmc=223695111; dbcl2="267968154:GRyVxHaZYFw"; ck=cPAc; __utmz=30149280.1744080109.8.2.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; push_doumail_num=0; push_noty_num=0; frodotk_db="5f16cd3b881353d21d4467b29839fb76"; __utmv=30149280.26796; ap_v=0,6.0; __utma=30149280.1668535597.1743937597.1744123210.1744126973.14; __utmt=1; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1744126980%2C%22https%3A%2F%2Fwww.douban.com%2Fmisc%2Fsorry%3Foriginal-url%3Dhttps%3A%2F%2Fmovie.douban.com%2Ftop250%22%5D; _pk_ses.100001.4cf6=1; __utma=223695111.1160767240.1743937597.1744123223.1744126980.14; __utmb=223695111.0.10.1744126980; __utmz=223695111.1744126980.14.5.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/misc/sorry; __utmb=30149280.4.10.1744126973'
headers={
    "cookie":cookie_str,
    "user-agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
}  # 请求头，避免被封，可以让网站认为是用户而非这台主机
response=requests.get('https://movie.douban.com/top250',headers = headers)
html=''
time.sleep(random.randint(10, 20) / 10)
if response.status_code==200:
    html=etree.HTML(response.text)
    firstUrl=html.xpath('//*[@id="content"]//div[@class="pic"]//a/@href')  # 返回所有匹配的列表
    firstUrl=firstUrl[:10]
else: firstUrl=[]

def get_specific_url_e(url):
    movie_response = requests.get(url, headers=headers)
    if movie_response.status_code == 200:
        return etree.HTML(movie_response.text)
    else: return ''

def get_specific_url_r(url):
    movie_response = requests.get(url, headers=headers)
    if movie_response.status_code == 200:
        return movie_response.text
    else: return ''

def scrawl_basic_information(movie_url):
    basic=[]
    for i in range(10):
        movie_html=get_specific_url_e(movie_url[i])
        movie_html_r=get_specific_url_r(movie_url[i])
        movie_name=movie_html.xpath('//*[@id="content"]/h1/span[1]/text()')
        movie_year=movie_html.xpath('//*[@id="content"]/h1/span[2]/text()')
        director=movie_html.xpath('//*[@id="info"]/span[1]/span[2]/a/text()')
        scriptwriter=movie_html.xpath('//*[@id="info"]/span[2]/span[2]/a/text()')
        actor=movie_html.xpath('//*[@id="info"]/span[3]/span[2]//a/text()')
        movie_type=movie_html.xpath('//*[@id="info"]//span[@property="v:genre"]/text()')
        official_url='None'
        if i==4:
            official_url=movie_html.xpath('//*[@id="info"]/a/@href')
        pattern_c=r'<span class="pl">.*?(制片国家/地区:).*?</span>\s*([^<]+)'  # [^<]+:匹配直到下一个HTML标签开始‌的所有字符
        match_c=re.search(pattern_c,movie_html_r)
        country=match_c.group(2).strip()
        pattern_l=r'<span class="pl">.*?(语言:).*?</span>\s*([^<]+)'
        match_l=re.search(pattern_l,movie_html_r)
        language=match_l.group(2).strip()
        pattern_t=r'<span property="v:initialReleaseDate" content="([^"]+)">.*?</span>'
        release_time=re.findall(pattern_t,movie_html_r)
        pattern_run=r'<span property="v:runtime".*?>(.*?)</span>.*?/([^<]+)'
        match_run=re.search(pattern_run,movie_html_r, re.DOTALL)
        runtime1=match_run.group(1).strip()
        runtime2=match_run.group(2).strip()
        if runtime2=='>':
            runtime=runtime1
        else:
            runtime = f"{runtime1} / {runtime2}"
        pattern_a=r'<span class="pl">又名:</span>.*?([^<]+)'
        alias=re.search(pattern_a,movie_html_r,re.DOTALL).group(1).strip()
        pattern_i=r'<span class="pl">IMDb:</span>.*?([^<]+)'
        IMDb=re.search(pattern_i, movie_html_r, re.DOTALL).group(1).strip()
        if i==0 or i==7:
            movie_summary=movie_html.xpath('//*[@id="link-report-intra"]/span[2]/text()')[0]+movie_html.xpath('//*[@id="link-report-intra"]/span[2]/text()')[1]
        elif i==8: movie_summary=movie_html.xpath('//*[@id="link-report-intra"]/span[2]/text()')[0]
        else: movie_summary=movie_html.xpath('//*[@id="link-report-intra"]/span[1]/text()')[0]
        movie_summary = movie_summary.replace(" ","").replace("\n","").replace("\u3000","")
        basic_info={'movie_name':movie_name[0],
                    'movie_year':movie_year[0][1:5],
                    'director':director[0],
                    'scriptwriter':scriptwriter,
                    'actor':actor,
                    'movie_type':movie_type,
                    'official_url':official_url[0],
                    'country':country,
                    'language':language,
                    'release_time':release_time,
                    'runtime':runtime,
                    'alias':alias,
                    'IMDb':IMDb,
                    'movie_summary':movie_summary }
        basic.append(basic_info)
    return basic

def scrawl_statistics_information(statistics_url):
    statistics=[]
    for i in range(10):
        statistics_html = get_specific_url_e(statistics_url[i])
        statistics_point=statistics_html.xpath('//*[@id="interest_sectl"]/div[1]/div[2]/strong/text()')
        point_sen=f"'豆瓣评分':{statistics_point}".replace("'","")
        try:
            statistics_number=statistics_html.xpath('//*[@id="interest_sectl"]/div[1]/div[2]/div/div[2]/a/span/text()')
            number_sen=f"{statistics_number[0]}人评价".replace("'","")#这里有一处列表和子串引号的改动
        except Exception as e:
            number_sen=""
        star_number=statistics_html.xpath('//div[@class="ratings-on-weight"]//span[@class="rating_per"]/text()')
        star_statistics=[]
        stars = ['5星', '4星', '3星', '2星', '1星']
        for star, percent in zip(stars, star_number):
            star_statistics.append(f"{star}：{percent}")
        compare=statistics_html.xpath('//div[@class="rating_betterthan"]//a/text()')
        statistics_compare=f"'好于'{compare[0]}';好于'{compare[1]}"
        statistics_compare=statistics_compare.replace("'","").replace(" ","")
        statistics.append({
            'statistics_point':point_sen,
            'statistics_number':number_sen,
            'star_statistics':star_statistics,
            'statistics_compare':statistics_compare
        })
    return statistics

def star(word):
    if word=="力荐": return "five stars"
    elif word=="推荐": return "four stars"
    elif word=="还行": return "three stars"
    elif word=="较差": return "two stars"
    elif word=="很差": return "one stars"
    elif word=="": return "Empty!"

def comment_page(url,begin):
    comment_html_e=get_specific_url_e(url)
    comment_html_r=get_specific_url_r(url)
    path11='//*[@id="comments"]/div['
    path12=']/div[2]/h3/span[2]/a/text()'
    pattern2=r'<span class="allstar.*?rating" title="(.*?)"></span>'
    path32=']/div[2]/p/span/text()'
    pattern4=r'<span class="votes vote-count">(.*?)</span>'
    path1, path3 = [], []
    for j in range(20):
        path1.append(f"{path11}{j + 1}{path12}".replace("'", ""))
        path3.append(f"{path11}{j + 1}{path32}".replace("'", ""))
    star_total = re.findall(pattern2, comment_html_r)
    if len(star_total) < 20:
        new_lst = [""] * (20 - len(star_total))
        star_total.extend(new_lst)
    useful_total = re.findall(pattern4, comment_html_r)
    customers = []
    for k in range(20):
        try:
            customer_name=comment_html_e.xpath(path1[k])[0].strip()
        except Exception as e:
            customer_name=""
        comment_star=star(star_total[k])
        comment_content=comment_html_e.xpath(path3[k])[0].strip()
        useful=useful_total[k]
        customer=f"第{begin+k+1}条:{customer_name} 看过 给出 {comment_star} 评价是:{comment_content} {useful}有用 "
        customers.append(customer.replace("'", " ").strip())
    return customers

def scrawl_sixty_comments(firstUrl):
    comments=[]
    for i in range(10):
        movie_html=get_specific_url_e(firstUrl[i])
        movie_comment=movie_html.xpath('//*[@id="comments-section"]/div[1]/h2/i/text()')[0]
        comment_url=movie_html.xpath('//*[@id="comments-section"]/div[1]/h2/span/a/@href')[0]
        comment_number=movie_html.xpath('//*[@id="comments-section"]/div[1]/h2/span/a/text()')[0]
        page1=comment_page(comment_url,0)
        page_html_e=get_specific_url_e(comment_url)
        page2_url=page_html_e.xpath('//*[@id="paginator"]/a[3]/@href')[0][:-13]
        page2_url=f"'https://movie.douban.com/subject/1292720/comments'{page2_url}'sort=new_score'".replace("'","")
        page2=comment_page(page2_url,20)
        page3=comment_page(page2_url,40)
        comments.append({
            "movie_comment":movie_comment,
            "comment_number":comment_number,
            "sixty_comments":[page1+page2+page3]
        })
    return comments

f1,f2,f3=scrawl_basic_information(firstUrl),scrawl_statistics_information(firstUrl),scrawl_sixty_comments(firstUrl)
all_information=[]
for i in range(10):
    time.sleep(random.randint(5, 15) / 10)
    movie_information={**f1[i],**f2[i],**f3[i]}
    all_information.append(movie_information)

with open("movie_json","w",encoding="utf-8") as file:
    json.dump(all_information,file,ensure_ascii=False,indent=4)
