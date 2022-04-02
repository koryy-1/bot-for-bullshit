import time
from selenium.webdriver.common.keys import Keys
from datetime import datetime
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

def go_fight():
	with open('fight.py', 'r', encoding='utf-8') as file:
		cmd_string = file.read()
	return cmd_string

def make_command():
	with open('commands.py', 'r', encoding='utf-8') as file:
		cmd_string = file.read()
	return cmd_string

def xpath_exist(url):
	try:
		driver.find_element(By.XPATH, url)
		exist = True
	except Exception:
		exist = False
	return exist

def execute_command(command):
	if command.split()[0] == 'help':
		print('fight - включить автобой, нужно быть на странице BATTLE')
		print('parse - парсинг информации героев, нужно быть на странице MARKETPLACE, пока что малополезная функция')
		print('exit - корректный и быстрый выход из программы')
	elif command.split()[0] == 'accept':
		accept_transaction()
	elif command.split()[0] == 'back':
		driver.switch_to.window(driver.window_handles[0])
	elif command.split()[0] == 'goto':
		driver.switch_to.window(driver.window_handles[int(command.split()[1])])
	elif command.split()[0] == 'xpexist':
		print(xpath_exist(command.split()[1]))
	elif command.split()[0] == 'click':
		driver.find_element(By.XPATH, command.split()[1]).click()
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
	else:
		print('unknown command, type "help" for more info')



def init_game_window():
	driver.switch_to.window(driver.window_handles[0])
	
	driver.find_element(By.XPATH, '//button').click()
	driver.find_element(By.XPATH, '//button').click()
	# //button[text()="Импортировать кошелек"]
	driver.find_element(By.XPATH, '//button').click()

	# After this you will need to enter you wallet details

	# inputs = driver.find_elements_by_xpath('//input')
	# print(inputs)

	time.sleep(1)
	
	driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div/div/form/div[4]/div[1]/div/input').send_keys(SECRET_RECOVERY_PHRASE)
	driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(NEW_PASSWORD)
	driver.find_element(By.XPATH, '//*[@id="confirm-password"]').send_keys(NEW_PASSWORD)

	driver.find_element(By.CSS_SELECTOR, '.first-time-flow__terms').click()
	driver.find_element(By.XPATH, '//button[text()="Импорт"]').click()
	time.sleep(2)
	driver.find_element(By.XPATH, '//button[text()="Выполнено"]').click()

	driver.execute_script("window.open('');")
	driver.switch_to.window(driver.window_handles[2])
	driver.get('https://app-alpha.galaxyadventure.io/')
	# window 2 - game
	# window 0 - metamask
	# присоединение метамаска к игре
	time.sleep(3)
	driver.switch_to.window(driver.window_handles[0])
	driver.get('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html')
	time.sleep(1)
	driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div/div[2]/div[4]/div[2]/button[2]').click()
	time.sleep(1)
	driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div/div[2]/div[2]/div[2]/footer/button[2]').click()
	time.sleep(2)
	# подтверждение входа в игре
	driver.switch_to.window(driver.window_handles[2])
	driver.find_element(By.XPATH, '/html/body/div[2]/div/div[6]/button[1]').click()
	time.sleep(2)
	# еще какое-то принятие
	driver.switch_to.window(driver.window_handles[0])
	driver.get('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html')
	time.sleep(2)
	driver.find_element(By.XPATH, '/html/body/div[1]/div/div[3]/div/div[3]/button[2]').click()
	time.sleep(2)
	driver.find_element(By.XPATH, '/html/body/div[2]/div/div/section/header/div/button').click() # закрыть окно с qr
	time.sleep(0.5)
	driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/div[2]/div[1]/div/span').click()
	time.sleep(0.2)
	driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div/li[7]/span').click() # форма пользовательской RPC
	time.sleep(0.5)
	
	driver.find_element(By.XPATH, '/html/body/div[1]/div/div[3]/div/div[2]/div[2]/div/div[2]/div[2]/div[2]/div[2]/div/input').send_keys(NET_NAME)
	driver.find_element(By.XPATH, '/html/body/div[1]/div/div[3]/div/div[2]/div[2]/div/div[2]/div[2]/div[3]/div[2]/div/input').send_keys(RPC_URL)
	driver.find_element(By.XPATH, '/html/body/div[1]/div/div[3]/div/div[2]/div[2]/div/div[2]/div[2]/div[4]/div[2]/div/input').send_keys(ID_NET)
	driver.find_element(By.XPATH, '/html/body/div[1]/div/div[3]/div/div[2]/div[2]/div/div[2]/div[2]/div[5]/div[2]/div/input').send_keys(CURRENCY)
	time.sleep(0.5)
	driver.find_element(By.XPATH, '/html/body/div[1]/div/div[3]/div/div[2]/div[2]/div/div[2]/div[2]/div[7]/button[2]').click()
	time.sleep(2)
	if xpath_exist('/html/body/div[1]/div/div[3]/div/div/div/div[2]/div/div[1]/div/div/div/div/div/span[2]'):
		if driver.find_element(By.XPATH, '/html/body/div[1]/div/div[3]/div/div/div/div[2]/div/div[1]/div/div/div/div/div/span[2]').text == 'BNB':
			print('vowel v accaunt')
		else:
			print('4to-to ne tak')
	else:
		print('ne nawel text s valutoy')

	# проход по ссылке /fight-monster
	driver.switch_to.window(driver.window_handles[2])
	driver.find_element(By.XPATH, '/html/body/div/div/div[1]/div/ul/li[4]/a/div/img').click()

with driver:
	x = random.randint(1300, 1356)
	y = random.randint(1200, 1300)

	driver.set_window_size(x, y)

	# # dev#######################################
	# driver.execute_script("window.open('');")
	# driver.switch_to.window(driver.window_handles[2])
	# driver.get('https://app-alpha.galaxyadventure.io/')
	# ########################################

	init_game_window()
	

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
