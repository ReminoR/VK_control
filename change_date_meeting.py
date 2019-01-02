import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime as DateTime, timedelta as TimeDelta
import auth_vk

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
	# time.sleep(3)
	auth_vk.auth(form_data, session, headers)
	# time.sleep(3)

	#Изменить описание встречи
	edited_page = get_edit_group_page('112409992')
	# time.sleep(3)
	change_date(edited_page)
	# time.sleep(3)


def get_edit_group_page(event_id):
	url = 'https://vk.com/event' + event_id + '?act=edit'

	r = session.get(url, headers=headers)
	print('страница редактирования сообщества получена')

	return r.text

def change_date(edited_page):
	soup = BeautifulSoup(edited_page, 'html.parser')
	desc = soup.find(id="group_edit_desc").text

	start_date = soup.find(id='group_start_date').get('value')
	start_date_delta = DateTime.strptime(start_date, "%d.%m.%Y %H:%M") + TimeDelta(days=7)
	if start_date_delta.weekday() == 5:
		start_date_new = DateTime.strftime(start_date_delta, '%d.%m.%Y %H:%M')
	else:
		print('Ошибка: Не суббота')
		return

	finish_date = soup.find(id='group_finish_date').get('value')
	finish_date_delta = DateTime.strptime(finish_date, "%d.%m.%Y %H:%M") + TimeDelta(days=7)
	if finish_date_delta.weekday() == 5:
		finish_date_new = DateTime.strftime(finish_date_delta, '%d.%m.%Y %H:%M')
	else:
		print('Ошибка: Не суббота')
		return

	url = 'https://vk.com/groupsedit.php'

	data = {
		'access': 0,
		'act': 'save',
		'addr': 'sy_tomsk',
		'al': 1,
		'category_0': 1109,
		'category_1': 0,
		'category_2': 0,
		'city_id': 144,
		'country_id': 1,
		'description': desc,
		'start_date': start_date_new,
		'finish_date': finish_date_new,
		'email': '',
		'gid': '112409992',
		'hash': '36b5825c1c1935f091',
		'host': '-22211825',
		'is_ads_enabled': 0,
		'is_article': 0,
		'is_source_hidden': 0,
		'name': 'Сахаджа Йога. Медитация.',
		'phone': '',
		'rss_enable': 0,
		'rss_url': '',
		'subject': '',
		'website': ''
	}

	r = session.post(url, data, headers=headers)
	if r.status_code == 200:
		print('Дата и время следующего занятия: ' + start_date_new)
	else:
		print('Ошибка')

	return


if __name__ == '__main__':
	main()