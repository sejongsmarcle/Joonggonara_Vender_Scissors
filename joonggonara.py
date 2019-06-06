from selenium import webdriver
from bs4 import BeautifulSoup
import time
from winsound import Beep
import telegram

my_token = '837339362:AAESYsiM7S5qRu4SBGYK-OLhrEgRtPWgDcA'
bot = telegram.Bot(my_token)
chat_id = bot.getUpdates()[-1].message.chat.id
text_tmp = bot.getUpdates()[-1].message.text

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument('disable-gpu')

driver = webdriver.Chrome(executable_path='D:/chromedriver.exe', chrome_options=options)
driver.implicitly_wait(1)

title_tmp = ' '
author_tmp = ' '
#info = (title_tmp, author_tmp)
'''
blacklist = ['☆', '★', '◀', '▶', '■', '□', '●', '○', '◇', '◈', '♪', '♨', '♣', '♧', '⊙', '#', '@', '<', '>', \
             '삽니다', '매입', '파손', '고장', '최고가', '최상', \
             '최저가', '할인', '대박', '세일', '한정', '특', '특급', '특가', '최대한', '저렴하게', 'S급', 's급', '싸게', \
             '전국', '택배', '가개통', '선택', '약정', '전문', '강변', '출장', '급처', '사은품', '최고회원', \
             '부산', '수원', '대전', '대구', '전주', '청주']

block_user = ['모바일', '폰', 'phone', 'Phone', '남포폰깨비', '햄툐리a', 'diddud1234', '후애마이', 'foreversoo1', '럭키쵸이', '안전거래직', '난야똑또기', '절대신용7', '원하다폰', 'kg5161', '카나리비오', '중고폰', 'baksaphone', 'chsekfr77', '깔끔하게쿨하게', '아나바다폰', 'rhden2626', '45351', 'rnjstnsgud1487', '몽몽이58', 'Hey', 'jhpa', '르샤트', '강아징아아', '꼬마', 'wjdnf33', 'hiplaza1989', '6106모바일2', 'rnjstnsgud1487', 'superlueh4', 'Smile Phone', '깜장발이', '금빛돼지']
'''

'''
f=open("blacklist.txt", 'r')
blacklist=[]
while True:
    line=f.readline()
    if not line:
        break
    blacklist.append(line[:-1])
f.close()

f=open("block_user.txt", 'r')
block_user=[]
while True:
    line=f.readline()
    if not line:
        break
    block_user.append(line[:-1])
f.close()
'''

def fopen(filename, mode):
    f=open(filename, mode)
    _list=[]
    while True:
        line=f.readline()
        if not line:
            break
        _list.append(line[:-1])
    f.close()
    return _list

blacklist=fopen("blacklist.txt", 'r')
block_user=fopen("block_user", 'r')


individual = 0
vender = 0
keywords = ['V30', 'v30', 'G7', 'g7']

sign=['↑', '↗', '→', '↘', '↓', '↙', '←', '↖']

t=0
while True:
    driver.get('https://cafe.naver.com/ArticleList.nhn?search.clubid=10050146&search.menuid=424&search.boardtype=L')
    driver.switch_to.frame('cafe_main')

    # print(driver.page_source)

    # inner_elem=driver.find_elements_by_class_name('m-tcol-c')

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    try:
        postnum=soup.select(
            '#main-area > div:nth-child(5) > table > tbody > tr:nth-child(1) > td.td_article > div.board-number > div').pop().text.strip()
        title = soup.select(
            '#main-area > div:nth-child(5) > table > tbody > tr:nth-child(1) > td.td_article > div.board-list > div > a').pop().text.strip()
        author = soup.select(
            '#main-area > div:nth-child(5) > table > tbody > tr:nth-child(1) > td.td_name > div > table > tbody > tr > td > a').pop().text.strip()
    except IndexError:
        print('IndexError: pop from empty list')
        bot.sendMessage(chat_id=chat_id, text='IndexError: pop from empty list')
        continue

    if title_tmp != title:
        title_tmp = title

        vender_flag = False

        # check vender by title
        try:
            for word in blacklist:
                if word in title:
                    vender+=1
                    vender_flag = True
                    break
        except TypeError:
            print("TypeError: 'in <string>' requires string as left operand, not list")
            print('word:',word,'\ntitle:',title)
            bot.sendMessage(chat_id=chat_id, \
                text="TypeError: 'in <string>' requires string as left operand, not list\n\n"+\
                "word: "+word+"\ntitle: "+title)
            break

        #check vender by author
        for user in block_user:
            if user in author:
                vender+=1
                vender_flag = True
                break

        if not vender_flag:
            individual += 1        

        if not vender_flag:
            for keyword in keywords:
                if (keyword in title):
                    print('\n'+title)
                    for i in range(0, 5):
                        Beep(4186, 100)
                    
                    link='https://cafe.naver.com/joonggonara/'+postnum
                    bot.sendMessage(chat_id=chat_id, text=title+'\n'+author+'\n'+link)

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

            if texts[0] == 'block':
                f=open("block_user.txt", 'a')
                f.write(texts[1]+"\n")
                f.close()
                block_user.append(texts[1])
                bot.sendMessage(chat_id=chat_id, text='blocked user ' + texts[1])
                print('blocked user ' + texts[1])
            elif texts[0] == 'add':
                blacklist.append([texts[1]])
                bot.sendMessage(chat_id=chat_id, text='add blacklist ' + texts[1])
                print('add blacklist' + texts[1])
            elif texts[0] == 'show':
                bot.sendMessage(chat_id=chat_id, text=block_user)
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


driver.close()