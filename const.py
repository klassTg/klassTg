import re

reporterName={339603195:"Король",206656564:"Царь-Иван"}
tok="875337974:AAEAfSYuwK3SeJ-0OFhViUodk2BBCx6tAvs"
reportUser=["339603195"]
# "name":message.from_user.first_name,"fillial":listFill[message.text],"nomer":False,"problem":False

problemType=["Хамство","Отсутсвие товара","Благодарность","Предложения","Другое"]
rule={"Царь-Иван":{"Алексеевка":[],'Московский 259':["Хамство","Отсутсвие товара"]}}
rule={}

def selectRe(session):
    fil,problem=session["fillial"],session["problem"]
    for reporter, pred in rule.items():
        try:
            if fil in pred and (pred[fil]==[] or  problem in pred[fil]):
                for id,nameid in reporterName.items():
                    if nameid==reporter:
                        return id
        except:pass
    else: return list(reporterName.keys())[0]





fil={"Главный офис":"Офис",'Алексеевка':4,'Блюхера':7,'Восточный':10,'Дружбы Народов':9,'Индустриальный':11,'Коммунальник':6,
       'Московский 259':1,'Одесская':2,'Пассионарии':8,'Рогань':5,'Салтовское шоссе 248':3,'Научный':12,'Холодная гора':13}

print(selectRe({"problem":"Хамство","fillial":'Московский 259'}))