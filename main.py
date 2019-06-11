import telebot
import random
import re
import const
import time
bot = telebot.TeleBot(const.tok)
# все текущие/не законченые заявки
sessionId={}

# лист сформированных заявок
listReport={}

realConversation={}

cleenBoard=telebot.types.ReplyKeyboardRemove()
keyboardMain = telebot.types.ReplyKeyboardMarkup()
keyboardMain.row('Оставить отзыв', 'Пока')

keyboardMainReporter = telebot.types.ReplyKeyboardMarkup()
keyboardMainReporter.row('Оставить отзыв', 'Переписочки')

keyboardOkTel = telebot.types.ReplyKeyboardMarkup()
keyboardOkTel.row('Ввести номер', 'Нет, спасибо')

sticksPack=["CAADAgADBQADn13rDBd2M2-XsrJjAg","CAADAgADeAADx2NcFX23_TcAATbBcAI"]
fil={"Главный офис":"Офис",'Алексеевка':4,'Блюхера':7,'Восточный':10,'Дружбы Народов':9,'Индустриальный':11,'Коммунальник':6,
       'Московский 259':1,'Одесская':2,'Пассионарии':8,'Рогань':5,'Салтовское шоссе 248':3,'Научный':12,'Холодная гора':13}

filAdr={"Главный офис": "пр. Московский, 257",'Московский 259': 'Харьков, пр. Московский, 259', 'Одесская': 'Харьков, пр. Гагарина, 178', 'Салтовское шоссе 248': 'Харьков, Салтовское Шоссе, 248',
        'Алексеевка': 'Харьков, пр. Людвига Свободы, 43', 'Рогань': 'Харьков, вул. Сергея Грицевца, 29', 'Коммунальник': 'Харьков, пр. Героев Сталинграда, 136/8',
        'Блюхера': 'Харьков, пр. Тракторостроителей, 128в', 'Пассионарии': 'Харьков, ул. Клочковская, 104-а', 'Дружбы Народов': 'Харьков, ул. Леся Сердюка, 36',
        'Восточный': 'Харьков, пр. Московский, 295', 'Индустриальный': 'Харьков, пр. Архитектора Алешина, 8', 'Научный': 'Харьков, ул. 23-го Августа, 33а',
        'Холодная гора': 'Харьков, ул. Дудинской, 1а'}

filPred={'Алексеевка':'Алексеевке','Блюхера':"Блюхера",'Восточный':"Восточном",'Дружбы Народов':"Дружбе Народов",'Индустриальный':"Индустриальном",'Коммунальник':"Коммунальном",
       'Московский 259':"Московском 259",'Одесская':'Одесской','Пассионарии':'Пассионарии','Рогань':'Рогане','Салтовское шоссе 248':'Салтовском шоссе 248',
         'Научный':"Научной",'Холодная гора':"Холодной горе","Главный офис":"Главном офисе"}



keyboardFil = telebot.types.ReplyKeyboardMarkup()

listFill={}

problemType=["Хамство","Отсутсвие товара","Благодарность","Предложения","Другое"]

keyboardProblemType = telebot.types.ReplyKeyboardMarkup()
for i in problemType:
    keyboardProblemType.add(i)

for i,v in filAdr.items():



    s="КЛАСС-"+str(fil[i])+". "+i+". "+v
    print(s)
    listFill[s]=i

    keyboardFil.add(s)


def sendReport(message,shot=False,ster=False):
    if not ster:

        if not shot:
            for id in const.reportUser:
                repMess= log(message)
                for text in repMess:
                    bot.send_message(id,text)
        else:
            for id in const.reportUser:
                bot.send_message(id, message)
    else:
        for id in const.reportUser:
            bot.send_sticker(id, message)
            bot.send_message(id, message)


# bot.send_message(chat_id='339603195', text='Hello Царь!')
def log(message):
    from  datetime import datetime
    a=[]
    print(message)
    a.append("\n _________________")
    a.append(datetime.now())
    a.append("Сообщение от {0} {1}. (id={2}) )\n Текст ={3}".format(message.from_user.first_name,message.from_user.last_name,str(message.from_user.id),message.text))
    for i in a:
        print(i)
    return a






@bot.message_handler(commands=['start'])


def handle_start_help(message):
    if message.chat.id not in const.reporterName:
        bot.send_message( message.chat.id,"Привет любимый покупатель "+message.from_user.first_name,reply_markup=keyboardMain)
        bot.register_next_step_handler(message, handle_test)
    else:
        bot.send_message(message.chat.id, "Привет супермен " + message.from_user.first_name,
                         reply_markup=keyboardMainReporter)
        bot.register_next_step_handler(message, handle_tolk)
    log(message)
    sendReport(message)

@bot.message_handler(content_types=['text'])
def helphelp(message):
    sendReport(message)
    if message.text!="/start":
        bot.send_message(message.chat.id, message.from_user.first_name + " используй /start", reply_markup=cleenBoard)



def handle_test(message):
    if "отзыв" in message.text.lower():
        bot.send_message(message.chat.id,message.from_user.first_name+" выбирете филлиал о котором вы хотите сообщить",reply_markup=keyboardFil)
        log(message)
        sendReport(message)
        bot.register_next_step_handler(message, takeFill)
    elif "пока" in message.text.lower():
        bot.send_message(message.chat.id, message.from_user.first_name + " пока", reply_markup=cleenBoard)

    else:
        bot.send_message(message.chat.id, message.from_user.first_name + " используй /start", reply_markup=cleenBoard)

def handle_tolk(message,content_types='text'):
    if message.text == None:
        bot.send_message(message.chat.id, message.from_user.first_name + " используй /start", reply_markup=cleenBoard)

    if "отзыв" in message.text.lower():
        bot.send_message(message.chat.id,message.from_user.first_name+" выбирете филлиал о котором вы хотите сообщить",reply_markup=keyboardFil)
        log(message)
        sendReport(message)
        bot.register_next_step_handler(message, takeFill)
    elif "переписочки" in message.text.lower():
        keyboardConversation=telebot.types.ReplyKeyboardMarkup()
        print(listReport)

        listSend=False

        for id,messages in listReport.items():

            if messages["idLis"]==message.chat.id:
                print(id,messages)
                print(id,messages["idLis"],formatMess(messages['description']))
                bot.send_message(message.chat.id, str(id)+" : "+formatMess(messages['description']))
                keyboardConversation.add(str(messages['description']['id']))
                listSend=True

        if listSend:
            bot.send_message(message.chat.id, message.from_user.first_name + " выбери кому отвечать.", reply_markup=keyboardConversation)
            bot.register_next_step_handler(message, select_tolk)

        else:
            bot.send_message(message.chat.id,  "сообщений нет")

            bot.register_next_step_handler(message, handle_tolk)

    else:
        bot.send_message(message.chat.id, message.from_user.first_name + " используй /start", reply_markup=cleenBoard)


def select_tolk(message):
    if message.text == None:
        select_tolk(message)
        return ()
    sendReport(message)
    print("listReport",listReport)
    if message.text in listReport:
        realConversation[message.chat.id]=message.text
        temp=listReport[message.text]["description"]
        bot.send_message(message.chat.id, " вы начали общение с "+temp["name"]+ " для завершения диалога напишите /end для паузы /pause", reply_markup=cleenBoard)
        bot.send_message(message.text, " к вам подключился на сотрудник", reply_markup=cleenBoard)
        bot.register_next_step_handler(message, chatConver)
    else:
        bot.send_message(message.chat.id, " вы выбрали неверный id " , reply_markup=cleenBoard)
        helphelp(message)

def chatConver(message):
    message.chat.id

    klient=realConversation[message.chat.id]

    if message.content_type=='photo':
        print(message.json)
        nPhoto=message.json["photo"][-1]['file_id']
        bot.send_photo(klient,nPhoto)


    if message.content_type=='text':
        if message.text=="/end":
            del realConversation[message.chat.id]
            del listReport[klient]
            return ()
        if message.text=="/pause":
            del realConversation[message.chat.id]
            return ()
        else:
            bot.send_message(klient, message.text)
            bot.register_next_step_handler(message, chatConver)

    if message.content_type == 'sticker':
        bot.send_sticker(klient, message.json["sticker"]['file_id'])
        bot.register_next_step_handler(message, chatConver)




def takeFill(message):
    if message.text == None:
        bot.register_next_step_handler(message, takeFill)
        return ()
    log(message)
    sendReport(message)
    if message.text in listFill:
        sessionId[message.chat.id]={"id":message.chat.id,"name":message.from_user.first_name,"fillial":listFill[message.text],"problem":False}

        preName=filPred[listFill[message.text]]
        bot.send_message(message.chat.id, message.from_user.first_name + " в чем дело на "+preName+"?",reply_markup=keyboardProblemType)

        bot.register_next_step_handler(message, takePr)



def takePr(message):
    if message.text == None:
        bot.register_next_step_handler(message, takePr)
        return ()

    log(message)
    sendReport(message)
    if message.text in problemType:
        sessionId[message.chat.id]["problem"]=message.text

        bot.send_message(message.chat.id, message.from_user.first_name + " опишите проблему", reply_markup=cleenBoard)

        bot.register_next_step_handler(message, choiseTel)

def choiseTel(message):
    if message.text == None:
        bot.register_next_step_handler(message, choiseTel)
        return ()

    sessionId[message.chat.id]["discrib"] = message.text
    log(message)
    sendReport(message)
    bot.send_message(message.chat.id, "Оставите свой номер телефона?",
                     reply_markup=keyboardOkTel)

    bot.register_next_step_handler(message, rezTel )

def rezTel(message):
    if message.text == None:
        bot.register_next_step_handler(message, rezTel)
        return ()

    log(message)
    sendReport(message)
    if message.text=='Ввести номер':

        bot.send_message(message.chat.id, "Ваш номер:",
                         reply_markup=cleenBoard)

        bot.register_next_step_handler(message, takeNumber)
    else:
        sessionId[message.chat.id]["nomer"]=None
        bot.send_message(message.chat.id, "Хорошо",
                        reply_markup=cleenBoard)
        takeDiscrib(message)

def takeNumber(message):
    if message.text == None:
        bot.register_next_step_handler(message, takeNumber)
        return ()

    log(message)
    sendReport(message)


    sessionId[message.chat.id]["nomer"]=message.text

    # bot.send_message(message.chat.id, message.from_user.first_name + " опишите проблему")

    takeDiscrib(message)
    bot.register_next_step_handler(message, takeDiscrib)

def formatMess(printRez):
    print(printRez)
    if printRez["nomer"]==None:
        report = "Сообщение от {0} по поводу филиала {1}. вопрос: {2},а именно {3}, скоро вам ответит Наш сотрудник".format(
            printRez["name"],
            printRez["fillial"], printRez["problem"], printRez["discrib"])
        return report
    else:
        report = "Сообщение от {0} по поводу филиала {1}. вопрос: {2},а именно {3}, скоро вам ответит Наш сотрудник. Указали номер телефона {4}".format(
            printRez["name"],
            printRez["fillial"], printRez["problem"], printRez["discrib"],
            printRez["nomer"]
        )
        return report

def takeDiscrib(message):
    # log(message)
    # sendReport(message)



    if sessionId[message.chat.id]["problem"] in ["Хамство","Отсутсвие товара","Другое"]:
        bot.send_message(message.chat.id, message.from_user.first_name + " мы все поняли, постараемся исправимся")
    else:
        bot.send_message(message.chat.id, message.from_user.first_name + " спасибо за ваше обращение")

    nameStick=sticksPack[random.randint(0,len(sticksPack)-1)]
    bot.send_sticker(message.chat.id,nameStick)



    printRez=sessionId[message.chat.id]
    print(printRez)
    report=formatMess(printRez)

    sendReport(report,True)
    bot.send_message(message.chat.id, report)
    bot.send_message(message.chat.id, "чтобы закончить разговоров напишите: /end")
    takeReport=const.selectRe(printRez)

    print(takeReport,listReport)

    listReport[str(printRez["id"])]={"idLis":takeReport,"description":printRez}
    bot.send_message(takeReport, const.reporterName[takeReport] + " у вас новое сообщение")
    bot.send_message(takeReport, report)

    bot.register_next_step_handler(message, takeConversation)

def takeConversation(message):
    sendReport(message)
    print(message)

    print(listReport)
    taker=listReport[str(message.chat.id)]["idLis"]




    if message.content_type=='photo':
        print(message.json)
        nPhoto=message.json["photo"][-1]['file_id']
        bot.send_message(taker, "сообщение от: " + listReport[str(message.chat.id)]["description"]["name"])
        bot.send_photo(taker,nPhoto)


    if message.content_type=='text':
        if message.text=="/end":
            bot.send_message(message.chat.id, "вы закончили разговор")
            return()

        sendReport(message)
        bot.send_message(taker, "сообщение от: "+listReport[str(message.chat.id)]["description"]["name"])
        bot.send_message(taker, message.text)

    if message.content_type=='sticker':
        sendReport(message)
        print(message)
        bot.send_message(taker, "сообщение от: "+listReport[str(message.chat.id)]["description"]["name"])
        bot.send_sticker(taker, message.json["sticker"]['file_id'])

    bot.register_next_step_handler(message, takeConversation)

    pass


bot.polling(none_stop=True, interval=1)

