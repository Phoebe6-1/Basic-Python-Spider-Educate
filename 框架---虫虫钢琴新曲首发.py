import requests
from bs4 import BeautifulSoup
import json

# 发送请求
url = 'https://www.gangqinpu.com/'
response = requests.get(url)
soup=''
# 获取网页响应
if response.status_code == 200:
    html_content = response.text
    soup=BeautifulSoup(html_content,'lxml')
    # info1=soup.find_all('h2')
    # for item in info1:
    #     print(item.text)
else:
    print(f"请求失败，状态码：{response.status_code}")

new_song_info=[]
all_info=soup.find_all('li',class_='clearfix')
for item in all_info:
    song_name=item.find('p').text.strip().replace('\n','')
    song_author_html=item.find('div',class_='fr')
    if song_author_html is not None:
        song_auther=song_author_html.text.strip()
    else:
        song_auther='Empty'
    link=f"https://www.gangqinpu.com/{item.find('a').get('href')}"
    a_song={
            'song_name':song_name,
            'song_author':song_auther,
            'song_link':link
            }
    new_song_info.append(a_song)
for item in new_song_info:
    print(item)

with open("song_json","w",encoding="utf-8") as file:
    json.dump(new_song_info,file,ensure_ascii=False,indent=4)
