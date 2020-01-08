from selenium import webdriver
from bs4 import BeautifulSoup
import time
from winsound import Beep
import telegram
import os

#telegram
my_token = '837339362:AAESYsiM7S5qRu4SBGYK-OLhrEgRtPWgDcA'
bot         = telegram.Bot(my_token)
chat_id     = bot.getUpdates()[-1].message.chat.id
text_tmp    = bot.getUpdates()[-1].message.text

#selenium.webdriver
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument('disable-gpu')
options.add_argument('log-level=1')

driver = webdriver.Chrome(executable_path='D:/chromedriver.exe', options=options)
driver.implicitly_wait(1)

def fopen_r(filename):
    f=open(filename, 'r')
    _list=[]
    while True:
        line=f.readline()
        if not line:
            break
        _list.append(line[:-1])
    f.close()
    return _list

blacklist   = fopen_r("blacklist.txt")
block_user  = fopen_r("block_user.txt")
count       = fopen_r("count.txt")

individual  = int(count[0])
vender      = int(count[1])

keywords    = ['V30', 'v30', 'G7', 'g7']
sign        = ['↑', '↗', '→', '↘', '↓', '↙', '←', '↖']

title_tmp   = ' '
author_tmp  = ' '

#get article index
driver.get('https://cafe.naver.com/ArticleList.nhn?search.clubid=10050146&search.menuid=424&search.boardtype=L')
driver.switch_to.frame('cafe_main')
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

articleIndex    = 0
while True:
    try:
        postnum=soup.select(
            '#main-area > div:nth-child('+str(articleIndex)+') > table > tbody > tr:nth-child(1) > td.td_article > div.board-number > div').pop().text.strip()
        print("Got it!")
        break
    except:
        print(str(articleIndex), end='\r')
        articleIndex+=1
        continue

t=0
while True:
    driver.get('https://cafe.naver.com/ArticleList.nhn?search.clubid=10050146&search.menuid=424&search.boardtype=L')
    driver.switch_to.frame('cafe_main')
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    try:
        postnum=soup.select(
            '#main-area > div:nth-child('+str(articleIndex)+') > table > tbody > tr:nth-child(1) > td.td_article > div.board-number > div').pop().text.strip()
        title = soup.select(
            '#main-area > div:nth-child('+str(articleIndex)+') > table > tbody > tr:nth-child(1) > td.td_article > div.board-list > div > a').pop().text.strip()
        author = soup.select(
            '#main-area > div:nth-child('+str(articleIndex)+') > table > tbody > tr:nth-child(1) > td.td_name > div > table > tbody > tr > td > a').pop().text.strip()
    except Exception as e:
        print(e)
        bot.sendMessage(chat_id=chat_id, text=str(e))
        continue

    if title_tmp != title:
        title_tmp = title

        vender_flag = False

        # check vender by title
        for word in blacklist:
            try:
                if word[0] in title:
                    vender+=1
                    vender_flag = True
                    break
            except Exception as e:
                print(e)
                print('word:',word,'\ntitle:',title)
                bot.sendMessage(chat_id=chat_id, \
                    text=str(e)+"\n\n"+"word: "+word+"\ntitle: "+title)
                break

        #check vender by author
        for user in block_user:
            if user in author:
                vender+=1
                vender_flag = True
                break

        if not vender_flag:
            individual += 1        
            for keyword in keywords:
                if (keyword in title):
                    print('\n'+title)
                    for i in range(0, 5):
                        Beep(4186, 100)
                    
                    link='https://cafe.naver.com/joonggonara/'+postnum
                    bot.sendMessage(chat_id=chat_id, text=title+'\n'+author+'\n'+link)
            
            if individual%10 == 0 or vender % 100 == 0:
                count=open("count.txt", 'w')
                count.write(str(individual)+'\n')
                count.write(str(vender)+'\n')
                count.close()

    if t%24==0:
        t=0
        #print("don't worry. I'm working...")

        # telegram receive part
        text = bot.getUpdates()[-1].message.text

        #check the command
        if text_tmp != text:
            text_tmp = text
            texts = text.split(' ')
            
            if 'help' in text:
                bot.sendMessage(chat_id=chat_id, text='block [id]\nadd [blacklist]\nex)block gogotaxi\nadd <')
                break

            if texts[0] == 'block':
                f=open("block_user.txt", 'a')
                f.write(texts[1]+"\n")
                f.close()
                block_user.append(texts[1])
                bot.sendMessage(chat_id=chat_id, text='blocked user ' + texts[1])
                print('blocked user ' + texts[1]+'\n')
            elif texts[0] == 'add':
                f=open("blacklist.txt", 'a')
                f.write(texts[1]+"\n")
                f.close()
                blacklist.append([texts[1]])
                bot.sendMessage(chat_id=chat_id, text='add blacklist ' + texts[1])
                print('add blacklist ' + texts[1]+'\n')
            elif texts[0] == 'show':
                bot.sendMessage(chat_id=chat_id, text=str(individual)+str(vender))
                print('show blocked user list')
            else:
                bot.sendMessage(chat_id=chat_id, text='I can\'t understand.\nWhat did you say?')
            print()

    now=time.gmtime(time.time())
    print('{:d}시 {:d}분 {:d}초 {:s}\t{:d} : {:d}\t개인: {:.2f}%\t업자: {:.2f}%'\
        .format(now.tm_hour+9, now.tm_min, now.tm_sec, sign[t%8], \
            individual, vender, \
            individual/(individual+vender)*100, vender/(individual+vender)*100), end='\r')

    time.sleep(1)
    t+=1

count=open("count.txt", 'w')
count.write(str(individual)+'\n')
count.write(str(vender)+'\n')
count.close()

driver.close()
'''
except Exception as e:
    print(e)
    bot.sendMessage(chat_id=chat_id, text=e)

    count=open("count.txt", 'w')
    count.write(str(individual)+'\n')
    count.write(str(vender)+'\n')
    count.close()

    os.system("python joonggonara.py")
'''