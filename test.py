import time
from selenium.webdriver.common.keys import Keys
import datetime
# import undetected_chromedriver.v2 as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
import json
from user_config import *
from bs4 import BeautifulSoup
import random
from criteries import *
# import commands

print('ВНИМАНИЕ')
print('это еще альфа пререлизная версия бота, так что не удивляйтесь возможным ошибкам')
print('если ошибки произошли то просто перезапустите программу')
opt = webdriver.ChromeOptions()
opt.add_extension(EXTENSION_PATH)
opt.add_argument("--mute-audio")

driver = webdriver.Chrome(options=opt)

print('pause')
time.sleep(2)
# поменять размер окна

def accept_transaction():
	driver.switch_to.window(driver.window_handles[1])
	driver.get('chrome-extension://{}/popup.html'.format(EXTENSION_ID))

def parse_info():
	with open('parse_info.py', 'r', encoding='utf-8') as file:
		cmd_string = file.read()
	return cmd_string

def get_stars():
	url_star = '/_next/image?url=%2Fassets%2Fimages%2Fstones%2Fstar1.png&w=64&q=75'

	text_html = driver.page_source
	soup = BeautifulSoup(text_html, 'html.parser')

	divs = soup.find("div", {"class": "card-shop-prices"})
	imgs = divs.findAll("img")
	stars = 0
	for img in imgs:
		if img['src'] == url_star:
			stars += 1
		# print(img['src'])
	return stars

def go_fight():
	# with open('fight.py', 'r', encoding='utf-8') as file:
	# 	cmd_string = file.read()
	# return cmd_string

	cooldown = '/html/body/div/div/div[2]/div/div[1]/div/div[3]/div/div/div[2]/div/div[6]/div[2]/p'
	index_number = '/html/body/div/div/div[2]/div/div[1]/div/div[3]/div/div/div[1]/div[2]'
	balance = '/html/body/div[1]/div/div[3]/div/div/div/div[2]/div/div[1]/div/div/div/div/div/span[1]'
	fight_btn = '/html/body/div/div/div[2]/div/div[2]/div/div/div[1]/div/div[2]/div[2]/button'
	accept_btn = '/html/body/div[1]/div/div[3]/div/div[4]/div[3]/footer/button[2]'
	reject_btn = '/html/body/div[1]/div/div[3]/div/div[4]/div[4]/footer/button[1]'
	close_btn = '/html/body/div[3]/div/div/div[1]/button'
	right_arrow_xp = '/html/body/div/div/div[2]/div/div[1]/div/div[2]/div/div/div[4]/button'
	balance_xp = '/html/body/div[1]/div/div[3]/div/div/div/div[2]/div/div[1]/div/div/div/div/div/span[1]'
	balance_exp = '/html/body/div/div/div[2]/div/div[1]/div/div[3]/div/div/div[2]/div/div[3]/div[2]'
	balance_lvl = '/html/body/div/div/div[2]/div/div[1]/div/div[3]/div/div/div[2]/div/div[2]/div[2]'

	def print_percent_done(index, total, bar_len=50, title='Waiting next battle'):
		
		percent_done = (index+1)/total*100
		percent_done = round(percent_done, 1)

		done = round(percent_done/(100/bar_len))
		togo = bar_len-done

		done_str = '█'*int(done)
		togo_str = '░'*int(togo)

		print(f'\t{title} : [{done_str}{togo_str}] {percent_done}% done', end='\r')


	Battle_number = 1
	Battle_balance = 0
	data_sum = 0
	while True:
		driver.switch_to.window(driver.window_handles[2]) 	
		driver.get('https://app-alpha.galaxyadventure.io/fight-monster')
		time.sleep(3)
		## Шапка боев
		print('|||||||||||||||||||||')
		date_start = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		print(date_start)## Дата старта
		print('#',Battle_number)## Номер боя в текущей сессии
		time.sleep(1)
		print(''' ___          _     _     _            
| _ )  __ _  | |_  | |_  | |  ___   ___
| _ \ / _` | |  _| |  _| | | / -_) (_-<
|___/ \__,_|  \__|  \__| |_| \___| /__/\n''') ## Боевоей клич
		#
		idx_hero = driver.find_element(By.XPATH, index_number).text
		hero_num = idx_hero.split('/')[0][1:]
		max_heroes = idx_hero.split('/')[1]
		#
		b = 0
		#_____________________________________________________________________ 	Бои
		for i in range(int(max_heroes)):	
			idx_hero = driver.find_element(By.XPATH, index_number).text
			hero_num = idx_hero.split('/')[0][1:]
			max_heroes = idx_hero.split('/')[1]
			lvl_hero = driver.find_element(By.XPATH, balance_lvl).text
			timing = driver.find_element(By.XPATH, cooldown).text
			print('Hero #:',hero_num,'/',max_heroes,'||',lvl_hero,' lvl','||','T:',timing)
			if b < 20:
				if timing == '00:00:00':
					b = b + 1
					if b < 2:
						sleep_time = 25
					else:
						sleep_time = 2.5
					driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
					time.sleep(0.3)
					driver.find_element(By.XPATH, fight_btn).click()
					time.sleep(sleep_time)
					if xpath_exist(close_btn):
						driver.find_element(By.XPATH, close_btn).click()
			driver.find_element(By.TAG_NAME,'body').send_keys(Keys.PAGE_UP) 
			driver.find_element(By.XPATH, right_arrow_xp).click()
			time.sleep(1)
		print('Total battles now:',b)
		#_________________________metamask Подтверждение транзакций	
		#metamask
		driver.switch_to.window(driver.window_handles[0]) 
		driver.get('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html')
		time.sleep(2)
		if b > 0:
			
			if xpath_exist('/html/body/div[2]/div/div/section/header/div/button'):
				driver.find_element(By.XPATH, '/html/body/div[2]/div/div/section/header/div/button').click() # закрыть окно с qr
			while xpath_exist(accept_btn):
				driver.find_element(By.XPATH, accept_btn).click() # prinyat
				time.sleep(1)
			time.sleep(25)
		#_________________________metamask Проверка баланса
		driver.switch_to.window(driver.window_handles[0]) 
		driver.get('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html')
		if xpath_exist('/html/body/div[2]/div/div/section/header/div/button'):
			driver.find_element(By.XPATH, '/html/body/div[2]/div/div/section/header/div/button').click()
		while not xpath_exist(balance_xp):
			driver.find_element(By.XPATH, reject_btn).click() # otklonit
			time.sleep(1)
		if xpath_exist(balance_xp):
			Battle_balance = float(driver.find_element(By.XPATH, balance_xp).text)/0.001
		else :
			time.sleep(15)
			driver.switch_to.window(driver.window_handles[0]) 
			driver.get('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html')
			if xpath_exist(balance_xp):
				Battle_balance = driver.find_element(By.XPATH, balance_xp).text/0.00085
		time.sleep(1)
		#_________________________назад к вкладке с игрой
		driver.switch_to.window(driver.window_handles[2]) 	
		driver.get('https://app-alpha.galaxyadventure.io/fight-monster')
		time.sleep(3)
		#_________________________Рассчет времени до ближайшей битвы.
		print('Time to next battle')
		time_delay = 60*60*10
		for i in range(int(max_heroes)):
			idx_hero = driver.find_element(By.XPATH, index_number).text
			hero_num = idx_hero.split('/')[0][1:]
			max_heroes = idx_hero.split('/')[1]
			timing = driver.find_element(By.XPATH, cooldown).text
			print('Hero #:',hero_num,'/',max_heroes,'||','T:',timing)
			if timing != '00:00:00':
				timing = driver.find_element(By.XPATH, cooldown).text
				time_array = timing.split()
				hours = 0
				minuts = 0
				seconds = 0
				for time_str in time_array:
					if time_str.find('h') != -1:
						hours = int(time_str[:-1])
					if time_str.find('m') != -1:
						minuts = int(time_str[:-1])
					if time_str.find('s') != -1:
						seconds = int(time_str[:-1])
				time_delay1 = int(hours)*60*60+int(minuts)*60+int(seconds)
				if time_delay1 < time_delay:
					time_delay = time_delay1
			else :
				time_delay1 = 10
				if time_delay1 <= time_delay:
					time_delay = time_delay1
		#scroll up
			driver.find_element(By.TAG_NAME,'body').send_keys(Keys.PAGE_UP) 
			driver.find_element(By.XPATH, right_arrow_xp).click()
			#posle najatiya na strelku vpravo
			time.sleep(1)
		##________________________Итоги боев + статистика
		print('_____________________')
		print(''' ___                     _   _        
| _ \  ___   ___  _  _  | | | |_   ___
|   / / -_) (_-< | || | | | |  _| (_-<
|_|_\ \___| /__/  \_,_| |_|  \__| /__/\n''')
		print('_____________________')
		date_end = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		print(date_end)#Дата окончания боев
		print('#',Battle_number)## Номер боя в текущей сессии 
		##print('Total duration',Battle_number,'Battles',(date_sum + date_sub).strftime('%H:%M:%S')) ## Общая длительность боев за сессию
		Battle_number = Battle_number + 1
		print('~',round(Battle_balance,0),'battles remain')## Остаток по балансу в пересчете на бои
		if Battle_balance <=5 :##Предупреждение об отрицательном балансе
			print('WARNING:::You need more BNB!!!')
		print('Next battles in:',round(time_delay/60, 2),'min')## Время до след боя
		print('_____________________')
		for f in range(time_delay):
			print_percent_done(f,time_delay)
			time.sleep(1)
		print('Time to battles')
		print('|||||||||||||||||||||')

		get_stars()
	
		

def make_command():
	with open('commands.py', 'r', encoding='utf-8') as file:
		cmd_string = file.read()
	return cmd_string

def xpath_exist(url):
	try:
		driver.find_element(By.XPATH,url)
		exist = True
	except Exception:
		exist = False
	return exist

def execute_command(command):
	if command.split() == []:
		return
	elif command.split()[0] == 'help':
		print('accept - podtverdit perevod', 'back - goto first tab')
	elif command.split()[0] == 'accept':
		accept_transaction()
	elif command.split()[0] == 'back':
		driver.switch_to.window(driver.window_handles[0])
	elif command.split()[0] == 'goto':
		driver.switch_to.window(driver.window_handles[int(command.split()[1])])
	elif command.split()[0] == 'xpexist' and len(command.split()) > 1:
		print(xpath_exist(command.split()[1]))
	elif command.split()[0] == 'click' and len(command.split()) > 1:
		driver.find_element(By.XPATH,command.split()[1]).click()
	elif command.split()[0] == 'parse':
		try:
			exec(parse_info())
		except Exception as e:
			print(e)
	elif command.split()[0] == 'fight':
		try:
			exec(go_fight())
		except Exception as e:
			print(e)
	elif command.split()[0] == 'exec':
		try:
			exec(make_command())
		except Exception as e:
			print(e)
	elif command.split()[0] == 'pers_info':
		try:
			print(get_stars())
		except Exception as e:
			print(e)
	else:
		print('unknown command, type "help" for more info')



def init_game_window():
	driver.switch_to.window(driver.window_handles[0])
	
	driver.find_element(By.XPATH,'//button').click()
	driver.find_element(By.XPATH,'//button').click()
	# //button[text()="Импортировать кошелек"]
	driver.find_element(By.XPATH,'//button').click()

	# After this you will need to enter you wallet details

	# inputs = driver.find_elements_by_xpath('//input')
	# print(inputs)

	time.sleep(1)
	
	driver.find_element(By.XPATH,'/html/body/div[1]/div/div[2]/div/div/form/div[4]/div[1]/div/input').send_keys(SECRET_RECOVERY_PHRASE)
	driver.find_element(By.XPATH,'//*[@id="password"]').send_keys(NEW_PASSWORD)
	driver.find_element(By.XPATH,'//*[@id="confirm-password"]').send_keys(NEW_PASSWORD)

	driver.find_element(By.CSS_SELECTOR,'.first-time-flow__terms').click()
	driver.find_element(By.XPATH,'//button[text()="Импорт"]').click()
	time.sleep(2)
	driver.find_element(By.XPATH,'//button[text()="Выполнено"]').click()

	driver.execute_script("window.open('');")
	driver.switch_to.window(driver.window_handles[2])
	driver.get('https://app.galaxyadventure.io/marketplace')
	# window 2 - game
	# window 0 - metamask
	# присоединение метамаска к игре
	time.sleep(3)
	driver.switch_to.window(driver.window_handles[0])
	driver.get('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html')
	time.sleep(1)
	driver.find_element(By.XPATH,'/html/body/div[1]/div/div[2]/div/div[2]/div[4]/div[2]/button[2]').click()
	time.sleep(1)
	driver.find_element(By.XPATH,'/html/body/div[1]/div/div[2]/div/div[2]/div[2]/div[2]/footer/button[2]').click()
	time.sleep(2)
	# подтверждение входа в игре
	driver.switch_to.window(driver.window_handles[2])
	driver.find_element(By.XPATH,'/html/body/div[2]/div/div[6]/button[1]').click()
	time.sleep(2)
	# еще какое-то принятие
	driver.switch_to.window(driver.window_handles[0])
	driver.get('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html')
	time.sleep(2)
	driver.find_element(By.XPATH,'/html/body/div[1]/div/div[3]/div/div[3]/button[2]').click()
	time.sleep(2)
	driver.find_element(By.XPATH,'/html/body/div[2]/div/div/section/header/div/button').click() # закрыть окно с qr
	time.sleep(0.5)
	driver.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/div[2]/div[1]/div/span').click()
	time.sleep(0.2)
	driver.find_element(By.XPATH,'/html/body/div[1]/div/div[2]/div/li[7]/span').click() # форма пользовательской RPC
	time.sleep(0.5)
	
	driver.find_element(By.XPATH,'/html/body/div[1]/div/div[3]/div/div[2]/div[2]/div/div[2]/div[2]/div[2]/div[2]/div/input').send_keys(NET_NAME)
	driver.find_element(By.XPATH,'/html/body/div[1]/div/div[3]/div/div[2]/div[2]/div/div[2]/div[2]/div[3]/div[2]/div/input').send_keys(RPC_URL)
	driver.find_element(By.XPATH,'/html/body/div[1]/div/div[3]/div/div[2]/div[2]/div/div[2]/div[2]/div[4]/div[2]/div/input').send_keys(ID_NET)
	driver.find_element(By.XPATH,'/html/body/div[1]/div/div[3]/div/div[2]/div[2]/div/div[2]/div[2]/div[5]/div[2]/div/input').send_keys(CURRENCY)
	time.sleep(0.5)
	driver.find_element(By.XPATH,'/html/body/div[1]/div/div[3]/div/div[2]/div[2]/div/div[2]/div[2]/div[7]/button[2]').click()
	time.sleep(2)
	if xpath_exist('/html/body/div[1]/div/div[3]/div/div/div/div[2]/div/div[1]/div/div/div/div/div/span[2]'):
		if driver.find_element(By.XPATH,'/html/body/div[1]/div/div[3]/div/div/div/div[2]/div/div[1]/div/div/div/div/div/span[2]').text == 'BNB':
			print('vowel v accaunt')
		else:
			print('4to-to ne tak')
	else:
		print('ne nawel text s valutoy')

	# проход по ссылке /fight-monster
	driver.switch_to.window(driver.window_handles[2])
	driver.find_element(By.XPATH,'/html/body/div/div/div[1]/div/ul/li[4]/a/div/img').click()

with driver:
	x = random.randint(1300, 1356)
	y = random.randint(1200, 1300)

	driver.set_window_size(x, y)

	# # dev#######################################
	# driver.execute_script("window.open('');")
	# driver.switch_to.window(driver.window_handles[2])
	# driver.get('https://app.galaxyadventure.io/')
	# ########################################

	# autobattle and parsing inventarya

	init_game_window()
	
	# try:
	# 	exec(go_fight())
	# except Exception as e:
	# 	print(e)

	while True:
		command = input('cmd >')

		if not (command == 'exit'):
			# with open('questions_for_3_test.json', 'r', encoding='utf-8') as file:
			# 	data = json.load(file)

			execute_command(command)
		else:
			print('vihod iz progi')
			# driver.quit()
			break

