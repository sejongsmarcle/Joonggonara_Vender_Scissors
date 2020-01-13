import os
import sys
import time
from winsound import Beep

from selenium import webdriver
from bs4 import BeautifulSoup
import telegram


# TODO

# python auto restart

# select other category

# postnum, title, author -> json? dict

# 분당 게시글 빈도수 그래프 분석을 통한 유동적인 데이터 크롤링

'''
log-level: 
Sets the minimum log level.
Valid values are from 0 to 3: 

    INFO = 0, 
    WARNING = 1, 
    LOG_ERROR = 2, 
    LOG_FATAL = 3.

default is 0.

    # pop from empty list 오류 발생 시

    # 공지사항 리스트 수 변경으로 div:nth-child() 안의 숫자가 바뀔 경우 
    # 게시글 selector 다시 추출해서 재설정하는게 빠르고 편함

    # update v20200107

    # find the first user article that below the notice article

    # Run only once when starting program

    # board order

    #main-area > div:nth-child(7) > table > tbody > tr:nth-child(1) > td.td_article > div.board-list > div > a
    #main-area > div:nth-child(7) > table > tbody > tr:nth-child(2) > td.td_article > div.board-list > div > a
    #main-area > div:nth-child(7) > table > tbody > tr:nth-child(3) > td.td_article > div.board-list > div > a


'''

# args (for auto restart)
executable = sys.executable
args = sys.argv[:]
args.insert(0, sys.executable)

#telegram
my_token = '837339362:AAESYsiM7S5qRu4SBGYK-OLhrEgRtPWgDcA'
bot         = telegram.Bot(my_token)
chat_id     = bot.getUpdates()[-1].message.chat.id
text_tmp    = bot.getUpdates()[-1].message.text

#selenium.webdriver
options = webdriver.ChromeOptions()
#options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument('disable-gpu')
options.add_argument('log-level=1')

driver = webdriver.Chrome(executable_path='D:/chromedriver.exe', chrome_options=options)
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
        print(postnum)
        break
    except:
        print(str(articleIndex))
        articleIndex+=1
        #time.sleep(1)
        continue

# main

postnum_chk  = []
title_chk    = []
author_chk   = []

article = {
    'num'   : ' ',
    'title' : ' ',
    'name'  : ' ' 
}

print("Starting...")
t=0
while True:
    #driver.get('https://cafe.naver.com/ArticleList.nhn?search.clubid=10050146&search.menuid=424&search.boardtype=L')
    driver.refresh()
    driver.switch_to.frame('cafe_main')
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    #main-area > div:nth-child(7) > table > tbody > tr:nth-child(1) > td.td_article > div.board-list > div > a
    #main-area > div:nth-child(7) > table > tbody > tr:nth-child(2) > td.td_article > div.board-list > div > a
    #main-area > div:nth-child(7) > table > tbody > tr:nth-child(3) > td.td_article > div.board-list > div > a

    #네이밍 방식 변경
    #before
    #chk before after

    #after
    #과거 현재 미래
    #before now after

    postnum_before  = []
    title_before    = []
    author_before   = []

    postnum_after  = []
    title_after    = []
    author_after   = []

    # 굳이 중복 검사할 필요 없이
    # 그냥 전부 연산해도되는거 아닌가

    try:
        for i in range(1, 10+1):
            postnum_before.append(
                soup.select(
                '#main-area > div:nth-child('+str(articleIndex)+') > table > tbody > tr:nth-child('+str(i)+') > td.td_article > div.board-number > div')
                .pop().text.strip()
            )
            title_before.append(
                soup.select(
                '#main-area > div:nth-child('+str(articleIndex)+') > table > tbody > tr:nth-child('+str(i)+') > td.td_article > div.board-list > div > a')
                .pop().text.strip()
            )
            author_before.append(
                soup.select(
                '#main-area > div:nth-child('+str(articleIndex)+') > table > tbody > tr:nth-child('+str(i)+') > td.td_name > div > table > tbody > tr > td > a')
                .pop().text.strip()
            )
    except Exception as e:
        print(e)
        #bot.sendMessage(chat_id=chat_id, text=str(e))
        time.sleep(1)
        continue

    # initialize
    if t==0:
        postnum_chk = postnum_before
        title_chk = title_before
        author_chk = author_before

        postnum_after = postnum_before
        title_after = title_before
        author_after = author_before

    for postnum, title, author in zip(postnum_before, title_before, author_before):
        if not (postnum in postnum_chk):

            #append to after list
            postnum_after.append(postnum)
            title_after.append(title)
            author_after.append(author)



            '''
            # pop oldest element(1, 2, 3 -> 1, 2)
            postnum_chk.pop()
            title_chk.pop()
            author_chk.pop()

            #append(push) updated element(1, 2 -> 1_new, 1, 2)
            postnum_chk.insert(0, postnum)
            title_chk.insert(0, title)
            author_chk.insert(0, author)
            '''

    # 그냥 체크리스트 자체를 갱신해버리면?
    postnum_chk = postnum_before
    title_chk = title_before
    author_chk = author_before
    

    for postnum, title, author in zip(postnum_after, title_after, author_after):
        vender_flag = False

        # check vender by title
        for word in blacklist:
            try:
                if word in title:
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
            print(title)
            individual += 1        
            for keyword in keywords:
                if (keyword in title):
                    print('\n'+title)
                    for i in range(0, 5):
                        Beep(4186, 100)
                    
                    link='https://cafe.naver.com/joonggonara/'+postnum
                    bot.sendMessage(chat_id=chat_id, text=title+'\n'+author+'\n'+link)
                    author_tmp = author
            
            if individual%10 == 0 or vender % 100 == 0:
                count=open("count.txt", 'w')
                count.write(str(individual)+'\n')
                count.write(str(vender)+'\n')
                count.close()

    if t%24==0:
        #t=0
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

#                if(len(texts)==1):
#                    texts[1]=author_tmp

#               texts[1] 이 아니라 새로 하나 만들어서 넘겨야할듯

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

#    now=time.gmtime(time.time())
#    print('{:d}시 {:d}분 {:d}초 {:s}\t{:d} : {:d}\t개인: {:.2f}%\t업자: {:.2f}%'\
#        .format(now.tm_hour+9, now.tm_min, now.tm_sec, sign[t%8], \
#            individual, vender, \
#            individual/(individual+vender)*100, vender/(individual+vender)*100), end='\r')

    time.sleep(1)
    t+=1

count=open("count.txt", 'w')
count.write(str(individual)+'\n')
count.write(str(vender)+'\n')
count.close()

driver.close()

os.execvp(executable, args)
'''
except Exception as e:
    print(e)
    bot.sendMessage(chat_id=chat_id, text=e)

    count=open("count.txt", 'w')
    count.write(str(individual)+'\n')
    count.write(str(vender)+'\n')
    count.close()

    # Restart program

    os.system("python joonggonara.py")
'''