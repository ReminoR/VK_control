import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime

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
	form_data = get_auth_page()
	time.sleep(3)
	auth(form_data)
	time.sleep(3)
	get_stream_page()
	time.sleep(3)
	start_stream()


def get_auth_page():
	url = 'https://vk.com'
	r = session.get(url, headers=headers)
	soup = BeautifulSoup(r.text, 'html.parser')
	form = soup.find(id="quick_login_form")
	form_data = {
		'act': form.select('input[name="act"]')[0].get('value'),
		'role': form.select('input[name="role"]')[0].get('value'),
		'expire': '', 
		'recaptcha': '', 
		'captcha_sid': '', 
		'captcha_key': '', 
		'_origin': form.select('input[name="_origin"]')[0].get('value'), 
		'ip_h': form.select('input[name="ip_h"]')[0].get('value'),
		'lg_h': form.select('input[name="lg_h"]')[0].get('value'),
		'email': '79521830375',
		'pass': 'sahaja_tomsk_3'
	}

	print('данные авторизации получены')
	return form_data

def auth(auth_data):
	url = 'https://login.vk.com/?act=login'
	r = session.post(url, auth_data, headers=headers)
	print('авторизация прошла успешно')

def get_stream_page():
	url = 'https://vk.com/videos-146022431'
	r = session.get(url, headers=headers)
	print('страница трансляций получена')
	return r.text

def start_stream():
	url = 'https://vk.com/al_video.php?act=a_add_new_live_trans'
	now = datetime.now()
	date = datetime.strftime(now, '%d.%m.%Y')
	if (now.isoweekday() == 3):
		type_lesson = 'практическое'
	elif (now.isoweekday() == 6):
		type_lesson = 'для начинающих'
	else:
		type_lesson = 'другое'

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
		'rhash': '3ea79cc632737f1523',
		'title': date + ' – ' + type_lesson
	}
	r = session.post(url, data, headers=headers)
	
	print('трансляция "' + data['title'] +'" создана успешно')



main()