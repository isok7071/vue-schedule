from flask import *
import requests
from requests_ntlm import HttpNtlmAuth

app = Flask(__name__, static_folder='templates/assets')


@app.route('/')
def home():
    username = '10190275'
    password = 'QctW9wezkj'
    replacements_url = r"https://portal.petrocollege.ru/_api/Web/Lists/GetByTitle('Замены')/Items?$top=10&$orderby=Id desc"    

    #Авторизация на портале и получение json для работы с заменами
    auth = HttpNtlmAuth(username, password)

    headers = {'Accept': 'application/json;odata=verbose'}
    response = requests.get(
        replacements_url, verify=False, auth=auth, headers=headers)
    response_json = response.json()
    return response_json

@app.route('/about')
def about():
    return 'About'

if __name__ == '__main__': 
   app.run(debug = True) 