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
	get_stream_page()
	time.sleep(3)
	start_stream()
	time.sleep(3)

def createParser ():
	parser = argparse.ArgumentParser()
	parser.add_argument ('-c', '--custom', action='store_true', default=False)

	return parser

def get_stream_page():
	url = 'https://vk.com/videos-146022431'
	r = session.get(url, headers=headers)
	print('страница трансляций получена')

	return r.text

def start_stream():
	url = 'https://vk.com/al_video.php?act=a_add_new_live_trans'
	now = datetime.now()
	date = datetime.strftime(now, '%d.%m.%Y')

	if namespace.custom:
		type_lesson = custom_stream = input('Введите название трансляции: ')
		thumb_id = ''
	elif (now.isoweekday() == 3):
		type_lesson = 'практическое занятие'
		thumb_id = '456239128_-146022431'
	elif (now.isoweekday() == 6):
		type_lesson = 'занятие для начинающих'
		thumb_id = '456239125_-146022431'
	else:
		type_lesson = 'Прямая трансляция'
		thumb_id = ''

	data = {
		'al': '1',
		'category': '16',
		'description': '',
		'enable_donations': '',
		'no_comments': '',
		'notify_followers': '1',
		'owner_id': '-146022431',
		'preparation_check': '',
		'publish': '1',
		'thumb_id': thumb_id,
		'rhash': '3ea79cc632737f1523',
		'title': date + ' – ' + type_lesson
	}
	r = session.post(url, data, headers=headers)

	print(r.text)
	
	print('трансляция "' + data['title'] +'" создана успешно')
	return


if __name__ == '__main__':
	parser = createParser()
	namespace = parser.parse_args()
	main()
