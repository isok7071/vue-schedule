#Для многопоточности(чтобы обновлять расписание)
import re
from requests_ntlm import HttpNtlmAuth
import requests
import pandas as pd
from pandas import json_normalize
import datetime
import pytz
from bs4 import BeautifulSoup

#Дата с действия расписания
dateRasp = ""

#Класс реализующий обновление расписания
class PetroSchedule:
    def __init__(self, username, password):
        #Аутентификация на портале
        self.headers = {'Accept': 'application/json;odata=verbose'}
        self.auth = HttpNtlmAuth(username, password)
        
    #Сохранение актуального расписания по группе
    def saveByGroup(self):
        """Сохранения расписания по группе с портала
        """
        try:
            #Авторизация на портале
            responce = requests.get(r"https://portal.petrocollege.ru/_api/Web/Lists(guid'9c095153-274d-4c73-9b8b-4e3dd6af89e5')/Items(10)/AttachmentFiles",
                                verify=False, auth=self.auth, headers=self.headers, timeout=20)

            #Получаем название файла прикрепленного и переводим название в строку 
            response_json = responce.json()
        except:
            return "Портал недоступен"
        response_json_norm = json_normalize(response_json['d']['results'])
        df = pd.DataFrame.from_dict(response_json_norm["FileName"]).tail(1)
        df_filename = df.FileName.to_string(index=False)
        #Ссылка на актуальное расписание
        link = f"https://portal.petrocollege.ru/Lists/2014/Attachments/10/{df_filename}"
        filename = "raspisaniye.xlsx"
        r = requests.get(link, verify=False, auth=self.auth,
                            headers=self.headers, allow_redirects=True)
        open(filename, "wb").write(r.content)
        global dateRasp
        dateRasp = df_filename
        dateRasp = re.split(r"_|xlsx",dateRasp)
        dateRasp = "<strong>Внимание! Текущее расписание (числитель и знаменатель) в боте с " + dateRasp[1].replace("-"," по ").rstrip(".")+"</strong>\nПожалуйста, сверьтесь с текущей датой."


