import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime

def get_auth_page(login, password, session, headers):
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
		'email': login,
		'pass': password
	}

	print('данные авторизации для ' + login + ' получены успешно')
	return form_data

def auth(auth_data, session, headers):
	url = 'https://login.vk.com/?act=login'
	r = session.post(url, auth_data, headers=headers)
	print('авторизация прошла успешно')

	return