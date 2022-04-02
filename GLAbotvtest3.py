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
balance_xp = '/html/body/div[1]/div/div[3]/div/div/div/div[2]/div/div[1]/div/div/div/div/div/span[1]'


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
	imgs = divs.find_all("img")
	stars = 0
	for img in imgs:
		if img['src'] == url_star:
			stars += 1
		# print(img['src'])
	# print(f'stars\t\t{stars}')
	return stars

def init_game_window():
	reject_btn = '/html/body/div[1]/div/div[3]/div/div[4]/div[4]/footer/button[1]'
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
	driver.get('https://app.galaxyadventure.io')
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
	#Проверка баланса
	global start_Battle_balance 
	driver.switch_to.window(driver.window_handles[0]) 
	driver.get('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html')
	if xpath_exist('/html/body/div[2]/div/div/section/header/div/button'):
		driver.find_element(By.XPATH, '/html/body/div[2]/div/div/section/header/div/button').click()
	while not xpath_exist(balance_xp):
		driver.find_element(By.XPATH, reject_btn).click() # otklonit
		time.sleep(1)
	if xpath_exist(balance_xp):
		start_Battle_balance = float(driver.find_element(By.XPATH, balance_xp).text)
	else :
		time.sleep(15)
		driver.switch_to.window(driver.window_handles[0]) 
		driver.get('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html')
		if xpath_exist(balance_xp):
			start_Battle_balance = float(driver.find_element(By.XPATH, balance_xp).text)
	time.sleep(1)
	# проход по ссылке /fight-monster
	driver.switch_to.window(driver.window_handles[2])
	driver.find_element(By.XPATH,'/html/body/div/div/div[1]/div/ul/li[4]/a/div/img').click()

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
	balance_exp = '/html/body/div/div/div[2]/div/div[1]/div/div[3]/div/div/div[2]/div/div[3]/div[2]'
	balance_lvl = '/html/body/div/div/div[2]/div/div[1]/div/div[3]/div/div/div[2]/div/div[2]/div[2]'

	def print_percent_done(index, total, bar_len=25, title='Waiting next battle'):
		
		percent_done = (index+1)/total*100
		percent_done = round(percent_done, 1)

		done = round(percent_done/(100/bar_len))
		togo = bar_len-done

		done_str = '█'*int(done)
		togo_str = '░'*int(togo)

		print(f'\t{title} : [{done_str}{togo_str}] {percent_done}% done', end='\r')

	total_battles = 0
	Battle_number = 1
	Battle_balance = start_Battle_balance
	while True:
		driver.switch_to.window(driver.window_handles[2]) 	
		driver.get('https://app.galaxyadventure.io/fight-monster')
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
		Sum_rewards = 0
		#
		b = 0
		#_____________________________________________________________________ 	Бои
		for i in range(int(max_heroes)):			
			idx_hero = driver.find_element(By.XPATH, index_number).text
			hero_num = idx_hero.split('/')[0][1:]
			hero_num = int(''.join(hero_num))
			max_heroes = idx_hero.split('/')[1]
			lvl_hero = driver.find_element(By.XPATH, balance_lvl).text
			balance_exp_1 = driver.find_element(By.XPATH, balance_exp).text
			exp_1 = balance_exp_1.split('/')[0]
			exp_2 = balance_exp_1.split('/')[1].replace('/', '')
			exp_1 = int(''.join(exp_1))
			exp_2 = int(''.join(exp_2))
			timing = driver.find_element(By.XPATH, cooldown).text
			reward = 128*0.8
			lvlx = 1
			input('сейчас будет деление, press Enter')
			if int(exp_2) < 3491:
				if int(exp_2) < 991:
					print((10*0.8*get_stars()*1))
					input('знаменатель при lvlx = 1 press Enter')
					time_to_up = (exp_2-exp_1)/(10*0.8*get_stars()*1)
					lvlx = 1
				else:
					print((10*0.8*get_stars()*1.2))
					input('знаменатель при lvlx = 1.2 press Enter')
					time_to_up = (exp_2-exp_1)/(10*0.8*get_stars()*1.2)
					lvlx = 1.2
			else:
				print((10*0.8*get_stars()*1.8))
				input('знаменатель при lvlx = 1.8 press Enter')
				time_to_up = (exp_2-exp_1)/(10*0.8*get_stars()*1.8)
				lvlx = 1.8
			if hero_num < 10 :
				print('Hero #:  ',hero_num,'/',max_heroes,'  ||',get_stars(),'*','||',lvl_hero,'lvl','||',int(reward*get_stars()*lvlx),'GLA/b','||','T:',timing)
			elif hero_num > 9 and hero_num < 100 :
				print('Hero #:  ',hero_num,'/',max_heroes,' ||',get_stars(),'*','||',lvl_hero,'lvl','||',int(reward*get_stars()*lvlx),'GLA/b','||','T:',timing)
			else : 
				print('Hero #:  ',hero_num,'/',max_heroes,'||',get_stars(),'*','||',lvl_hero,'lvl','||',int(reward*get_stars()*lvlx),'GLA/b','||','T:',timing)
			if b < 30:
				if timing == '00:00:00':
					b = b + 1
					if b < 4:
						sleep_time = 35
						# 
					else:
						sleep_time = 2.5
					driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
					time.sleep(0.3)
					driver.find_element(By.XPATH, fight_btn).click()
					time.sleep(2)

					#for i in range (5):
					# if xpath_exist('/html/body/div[2]/div/span'):
					# 	time.sleep(5)
					
					while xpath_exist('/html/body/div[2]/div/span'): 
						qwe = driver.find_element(By.XPATH, '/html/body/div[2]/div/span').get_attribute('style')
						print(qwe)
						time.sleep(0.5)
					# time.sleep(sleep_time)
					if xpath_exist(close_btn):
						driver.find_element(By.XPATH, close_btn).click()
					Sum_rewards = Sum_rewards + (reward*get_stars()*lvlx)
			else :
				break
			driver.find_element(By.TAG_NAME,'body').send_keys(Keys.PAGE_UP) 
			driver.find_element(By.XPATH, right_arrow_xp).click()
			time.sleep(1)
		print('Total battles now:',b)
		total_battles = total_battles + b
		input('СЕЙЧАС БУДЕТ ПОДТВЕРЖДЕНИЕ НА МЕТАМАСКЕ скипнуть ctrl+C')
		if b > 0: 
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
				Battle_balance = float(driver.find_element(By.XPATH, balance_xp).text)
			else :
				time.sleep(15)
				driver.switch_to.window(driver.window_handles[0]) 
				driver.get('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html')
				if xpath_exist(balance_xp):
					Battle_balance = float(driver.find_element(By.XPATH, balance_xp).text)
			time.sleep(1)
			#_________________________назад к вкладке с игрой
		driver.switch_to.window(driver.window_handles[2]) 	
		driver.get('https://app.galaxyadventure.io/fight-monster')
		time.sleep(3)
		#_________________________Рассчет времени до ближайшей битвы.
		print('Time to next battle')
		time_delay = 60*60*10
		soonup = 0
		time_to_up = 99999
		lateup = 0 
		for i in range(int(max_heroes)):
			idx_hero = driver.find_element(By.XPATH, index_number).text
			hero_num = idx_hero.split('/')[0][1:]
			hero_num = int(''.join(hero_num))
			max_heroes = idx_hero.split('/')[1]
			lvl_hero = driver.find_element(By.XPATH, balance_lvl).text
			balance_exp_1 = driver.find_element(By.XPATH, balance_exp).text
			exp_1 = balance_exp_1.split('/')[0]
			exp_2 = balance_exp_1.split('/')[1].replace('/', '')
			exp_1 = int(''.join(exp_1))
			exp_2 = int(''.join(exp_2))
			timing = driver.find_element(By.XPATH, cooldown).text
			reward = 128*0.8
			lvlx = 1
			if int(exp_2) < 3491:
				if int(exp_2) < 991:
					time_to_up = int((exp_2-exp_1)/(10*0.8*get_stars()*1))
					lvlx = 1
				else:
					time_to_up = int((exp_2-exp_1)/(10*0.8*get_stars()*1.2))
					lvlx = 1.2
			else:
				time_to_up = int((exp_2-exp_1)/(10*0.8*get_stars()*1.8))
				lvlx = 1.8
			if hero_num < 10 :
				print('Hero #:  ',hero_num,'/',max_heroes,'  ||',get_stars(),'*','||',lvl_hero,'lvl','||',round((exp_1/exp_2)*100,1),'/100%',' ~',int(time_to_up*(6-0.5*get_stars())/24),'days','\t||','T:',timing)
			elif hero_num > 9 and hero_num < 100 :
				print('Hero #:  ',hero_num,'/',max_heroes,' ||',get_stars(),'*','||',lvl_hero,'lvl','||',round((exp_1/exp_2)*100,1),'/100%',' ~',int(time_to_up*(6-0.5*get_stars())/24),'days','\t||','T:',timing)
			else : 
				print('Hero #:  ',hero_num,'/',max_heroes,'||',get_stars(),'*','||',lvl_hero,'lvl','||',round((exp_1/exp_2)*100,1),'/100%',' ~',int(time_to_up*(6-0.5*get_stars())/24),'days','\t||','T:',timing)
			if lvlx == 1.2 and int(time_to_up*(6-0.5*get_stars())/24) <= 7:
				soonup = soonup + 1
			elif lvlx == 1.2 and int(time_to_up*(6-0.5*get_stars())/24) > 7:
				lateup = lateup + 1 
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
				time_delay1 = 1
				if time_delay1 <= time_delay:
					time_delay = time_delay1
				break
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
		print('Total battles :',total_battles)
		print('Rewards ~',round(Sum_rewards,0),'GLA')
		Battle_number = Battle_number + 1
		print('up:',soonup,'/',lateup)
		print('Spent on commissions :',round((start_Battle_balance)-(Battle_balance),5),'BNB')
		print('Metamask Balance :',Battle_balance,'BNB')
		if total_battles > 0 :
			print('AbFee :',round(((start_Battle_balance)-(Battle_balance))/total_battles,5),'BNB')
		print('~',round(Battle_balance/0.00085,0),'battles remain')## Остаток по балансу в пересчете на бои
		if Battle_balance <=5*0.00085 :##Предупреждение об отрицательном балансе
			print('WARNING:::You need more BNB!!!')
		print('Next battles in:',round(time_delay/60, 2),'min')## Время до след боя
		print('_____________________')
		for f in range(time_delay):
			print_percent_done(f,time_delay)
			time.sleep(1)
		print('Time to battles')
		print('|||||||||||||||||||||')
	
		

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
	
	try:
		exec(go_fight())
	except Exception as e:
		print(e)

	# while True:
	# 	command = input('cmd >')

	# 	if not (command == 'exit'):
	# 		# with open('questions_for_3_test.json', 'r', encoding='utf-8') as file:
	# 		# 	data = json.load(file)

	# 		execute_command(command)
	# 	else:
	# 		print('vihod iz progi')
	# 		# driver.quit()
	# 		break
