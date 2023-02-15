import shutil
from datetime import time
from fileinput import filename
from threading import Timer
import pytesseract
from PIL import Image
import urllib.request
import os
import requests
import telebot
import datetime

link = 'https://api.vk.com/method/'
group_id = '-134054041'
par = '&copy_history_depth=2'
method = 'wall.getById?posts='

token = '&access_token=vk1.a.fcT5pYyA3VXJoNbDEigy57XnVyKnGUWZLvCcWnlNullj2r9LpXG3T4T1S39Bk1apNCgi1KXSBifnCbfHV2wuFaTNeIkIjmt6JxwQMKkLn5Ki1G5yk5XYbJlGj-_Rc0tDgxDa9RDHIC-ca8sVre9imerCJuMHIsSKEJR58U3CAbz1j7PHdVDWECXA1XEnFkovqXwJiJR516akFHFGLv5X5g&expires_in=86400&user_id=782043762&v=5.131'


#
def scan():
    post = check()
    print('Вышло рассписание')
    image_list = []
    url = []
    sizes = []
    s = open('db.txt', 'w')
    s.write(str(post))
    uu = link + method + group_id + '_' + str(post) + par + token
    req = requests.get(uu)
    data = req.json()
    # print(uu)

    for i in data['response'][0]['attachments']:
        image_list.append(i)
    for i in range(len(image_list)):
        sizes.append(image_list[i]['photo']['sizes'])

    for i in range(len(sizes)):
        for j in range(len(sizes)):
            if sizes[i][j]['width'] >= 500:
                url.append(sizes[i][j]['url'])
            # print(url)

    for z in range(len(url)):
        img = urllib.request.urlopen(url[z]).read()
        out = open("img/img" + str(z) + ".jpg", "wb")
        out.write(img)
        imgName = "img/img" + str(z) + ".jpg"
        image = Image.open(imgName)
        # print(imgName)

        string = pytesseract.image_to_string(image, lang='rus')
        # print(string)
        # print(string.lower())
        global dy
        if 'понедельник' in string.lower():
            dy = 'на понедельник'
        elif 'вторник' in string.lower():
            dy = 'на вторник'
        elif 'среда' in string.lower():
            dy = 'на среду'
        elif 'четверг' in string.lower():
            dy = 'на четверг'
        elif 'пятница' in string.lower():
            dy = 'на пятницу'

        if "вт2-20" in string.lower() or "вт-2-20" in string.lower() or "вт-220" in string.lower() or "вт220" in string.lower():
            os.rename('img/img' + str(z) + '.jpg', 'send/img.jpg')
            # print('I am faggot')
            break
        out.close


#
#
#
# scan()

#
def check():
    req = requests.get(link + 'wall.get?owner_id=' + group_id + '&copy_history_depth=2' + token)

    data = req.json()
    # post1 = 1508
    post1 = data['response']['items'][0]['id']
    print(post1)
    return post1


check()


#

def proces():
    s = open('db.txt', 'r')
    p = check()
    t = int(s.read(4))
    if int(p) > t:
        scan()
        try:
            with open("send/img.jpg", "rb") as file:
                bot.send_photo(channel_id, file, caption="вышло расписание " + dy)  # Отправляем сообщение
                print(f"[{datetime.datetime.now()}] Отправил {dy}")  # лог в консоль
        except:
            with open("except/sorry.jpeg", "rb") as file:
                bot.send_photo(channel_id, file, caption="Извини, но расписания не будет(((")  # Отправляем сообщение
                print(f"[{datetime.datetime.now()}] Отправил {dy}")  # лог в консоль
    shutil.rmtree('img', ignore_errors=True)
    shutil.rmtree('send', ignore_errors=True)
    os.mkdir('img')
    os.mkdir('send')


bot = telebot.TeleBot("6171691064:AAHSEtfDYPYEqfnkwzeokzWbx8GSQC08I94")  # сюда вставляете ваш токен бота
channel_id = -1001807714277
#
# t = Timer(200, proces)
# t.start()
while True:  # Бесконечный цикл
    def meme():  # Обьявляем функцию
        proces()


    meme()  # вызываем функцию
time.sleep(60000)  # перер

print(dy)
