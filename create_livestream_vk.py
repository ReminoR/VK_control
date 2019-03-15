import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
import auth_vk
import sys
import argparse

session = requests.Session()

headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Language':'ru-ru,ru;q=0.8,en-us;q=0.5,en;q=0.3',
	'Accept-Encoding':'gzip, deflate',
	'Connection':'keep-alive',
	'DNT':'1'
}



def main():
	#Авторизация ВК
	form_data = auth_vk.get_auth_page('79521830375', 'sahaja_tomsk_3', session, headers)
	time.sleep(3)
	auth_vk.auth(form_data, session, headers)
	time.sleep(3)

	#Создать трансляцию
	start_stream()
	time.sleep(3)

def createParser ():
	parser = argparse.ArgumentParser()
	parser.add_argument ('-c', '--custom', action='store_true', default=False) # Ввести название вручную
	parser.add_argument ('group') # Группа для трансляции (Обязательный аргумент. Варианты: sy - для сахаджа йогов, by - для начинающих)
	parser.add_argument ('-n', '--name', default=False) # Название трансляции (Необязательный)

	return parser

def start_stream():
	url = 'https://vk.com/al_video.php?act=a_add_new_live_trans'
	now = datetime.now()
	date = datetime.strftime(now, '%d.%m.%Y')
	owner_id, name_stream, rhash = '', '', ''

	if (namespace.group == 'sy'):
		owner_id = '-146022431'
		rhash = '3ea79cc632737f1523'
		if namespace.custom and not namespace.name:
			name_stream = input('Введите название трансляции: ')
		elif namespace.name:
			name_stream = namespace.name
		else:
			name_stream = 'Прямая трансляция'

	elif (namespace.group == 'by'):
		owner_id = '-153258851'
		rhash = '56f5b8636e0e74e78f'
		if namespace.custom:
			name_stream = input('Введите название трансляции: ')
		elif namespace.name:
			name_stream = namespace.name
		else:
			name_stream = 'Прямая трансляция'

	data = {
		'al': '1',
		'category': '16',
		'description': '',
		'enable_donations': '',
		'no_comments': '',
		'notify_followers': '1',
		'owner_id': owner_id,
		'preparation_check': '',
		'publish': '1',
		'thumb_id': '',
		'rhash': rhash,
		'title': date + ' – ' + name_stream
	}
	r = session.post(url, data, headers=headers)

	print(r.text)
	
	print('Трансляция "' + data['title'] +'" в группе "' + namespace.group + '" создана успешно')
	return


if __name__ == '__main__':
	parser = createParser()
	namespace = parser.parse_args()
	main()
