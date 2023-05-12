import datetime
import re
from flask import *
import requests
from requests_ntlm import HttpNtlmAuth
from bs4 import BeautifulSoup
import pandas as pd
import parse

username = '10190275'
password = 'QctW9wezkj'

PetroScheduleTypes = parse.PetroSchedule(username, password)

PetroScheduleTypes.saveByGroup()


app = Flask(__name__, static_folder='templates/assets')

class PetroChanges:
    changes = {}

    def __init__(self, username, password, replacements_url):
        #Авторизация на портале и получение json для работы с заменами
        self.auth = HttpNtlmAuth(username, password)

        self.headers = {'Accept': 'application/json;odata=verbose'}
        self.replacements_url = replacements_url
        response = requests.get(
            self.replacements_url, verify=False, auth=self.auth, headers=self.headers)
        self.response_json = response.json()

    def getDictChanges(self):
        for item in self.response_json["d"]["results"]:
            self.changes[item["Id"]] = {
                "Title": item["Title"], "html": item["OData__x0421__x043e__x0434__x0435__x04"]}

        return self.changes

    def getNamesChanges(self):
        '''
        Get dict of schedules change names
        :return: dict {id:name}
        '''
        names = {}
        for item in self.response_json["d"]["results"]:
            names[item["Id"]] = item["Title"]
        return names

    def gitDictChangesByDate(self, date):
        '''
        Получение замен по дню
        date(string): Дата в формате ДДММГГГГ (01012022)

        return: dict {Id:{Title:title, html: html}
        '''
        changes = self.getDictChanges()

        for day in changes:
            if date == re.sub("[^0-9]", "", changes[day]["Title"]):
                return changes[day]
        return "В данный момент либо изменений нет, либо вы ввели неправильное значение"

    def getChangesByDay(self, date):
        '''
        Получение для отправки замен по дню 
        date(string): Дата в формате ДДММГГГГ (01012022)
        
        return: message(string) - отформатированный текст с заменами
        '''
        message = f"<strong>Замены на {date[0:2]}.{date[2:4]}.{date[4:9]}</strong>\n"
        data = self.gitDictChangesByDate(date)
        if type(data) == str:
            return data
        html = data["html"].split("1 пара")[0]
        soup = BeautifulSoup(html, 'lxml')
        table_rows = soup.find_all("tr")
        i = 0
        for tr_row in table_rows:
            # Пропускаем названия колонок на портале
            i += 1
            if (i < 3):
                continue
            columns_in_row = tr_row.find_all("td")
            for column_td in columns_in_row:
                # Формирование нормального отображения для замен
                if re.findall(r'\d\d[-]{0,1}\d\d["к","з"]{0,1}[" "]{0,1}(\(подг\)){0,1}$', column_td.text):
                    message += "ГРУППА: " + column_td.text+"\nНОМЕР ПАРЫ: "
                else:
                    message += column_td.text+"\n"

                if columns_in_row.index(column_td) == 1:
                    message += "ПО РАСПИСАНИЮ: "

                elif columns_in_row.index(column_td) == 2:
                    message += "ПО ЗАМЕНЕ: "
            message += '_______\n\n'

        return (message)

    def getChangesByQuery(self, date, query):
        '''
        Получение замен по дню и поисковому запросу
        date(string): Дата в формате ДДММГГГГ (01012022)
        query(string): Поисковый запрос по заменам
        return: message(string) - отформатированный текст с заменами, содержащий замены из поискового запроса
        '''
        message = f"<strong>Замены на {date[0:2]}.{date[2:4]}.{date[4:9]}</strong>\n"

        data = self.gitDictChangesByDate(date)
        if type(data) == str:
            return data
        html = data["html"].split("1 пара")[0]
        soup = BeautifulSoup(html, 'lxml')
        tables_rows = soup.find_all("tr")
        i = 0
        for tr_row in tables_rows:
            # Пропуск названия колонок
            i += 1
            if (i < 3):
                continue
            #Поиск по заменам
            if query.lower() in (str(tr_row)).lower() or "№ пары".lower() in (str(tr_row)).lower():
                columns_in_row = tr_row.find_all("td")
                #Форматирвоние замен
                for column_td in columns_in_row:
                    if re.findall(r'\d\d[-]{0,1}\d\d["к","з"]{0,1}[" "]{0,1}(\(подг\)){0,1}$', column_td.text):
                        message += "ГРУППА: " + column_td.text+"\nНОМЕР ПАРЫ: "
                    else:
                        message += column_td.text+"\n"

                    if columns_in_row.index(column_td) == 1:
                        message += "ПО РАСПИСАНИЮ: "

                    elif columns_in_row.index(column_td) == 2:
                        message += "ПО ЗАМЕНЕ: "

                message += '_______\n\n'
        if not message:
            return "Ничего не найдено, ваш запрос: " + query
        return message

    def getCabsChanges(self, date):
        message = f"<strong>Переносы кабинетов на {date[0:2]}.{date[2:4]}.{date[4:9]}</strong>\n"
        data = self.gitDictChangesByDate(date)
        if type(data) == str:
            return data
        try:
            html = data["html"].split('6 пара</strong></td></tr>')[1]
            soup = BeautifulSoup(html, 'lxml')
            table_rows = soup.find_all("tr")
            message += "|Откуда |1 пара | 2 пара | 3 пара | 4 пара | 5 пара | 6 пара|\n"
            for tr_row in table_rows:
                table_td = tr_row.find_all("td")
                for td_text in table_td:
                    message += "| " + td_text.text
                message += '\n\n'
        except:
            message += "Переносов кабинетов не обнаружено"
        return (message)


@app.route('/')
def home():

    replacements_url = r"https://portal.petrocollege.ru/_api/Web/Lists/GetByTitle('Замены')/Items?$top=10&$orderby=Id desc"    
    date = datetime.datetime.today()
    date_formatted = date.strftime('%d%m%Y')

    response = PetroChanges(username, password, replacements_url).getChangesByQuery(
            date_formatted, 'Медников')
    return response

@app.route('/about')
def about():
    file = 'raspisaniye.xlsx'
    xl = pd.read_excel(file)
    raspisaniye = pd.DataFrame(xl, columns=['10-30'])[0:]
    return formatDf(raspisaniye[0:6])

def formatDf(datafr):
        """Функция форматирующая DataFrame,убирает ненужную итнформацию

        Args:
            datafr : Получаемый датафрейм

        Returns:
            formatted_str (string): Возвращает строку готовую для вывода
        """
        # преобразуем датафрейм в html, для того чтобы убрать пустые пространство в строках
        try:
            html = datafr.to_html(index=False)
            soup = BeautifulSoup(html, 'lxml')
            # Выбор всех строк полученной таблицы парсером
            table_rows = soup.find_all("tr")

            # Форматирование полученных строк и создание результирующей строки
            formatted_str = ""
            for tr_row in table_rows:
                formatted_str += tr_row.text.replace(
                    "NaN", "Нет пары").replace("\\n", "\n")
            return formatted_str

        except:
            # Форматирование на случай если не парсер не сработает
            formatted_str = datafr.to_string(index=False).replace(" ", "").replace("NaN", "Нет пары").replace("\n", "\n\n").replace(
                "\\n", "\n")
            formatted_str = re.sub("([А-Я])", " \\1", str)
            formatted_strtr = re.sub(" С Д О", "СДО", str)
            return formatted_str
if __name__ == '__main__': 
   app.run(debug = True) 