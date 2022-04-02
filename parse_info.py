accept_btn = '/html/body/div[1]/div/div[3]/div/div[4]/div[3]/footer/button[2]'
buy_xp = '/html/body/div/div/div[2]/div/div/div/div[2]/div/div/div[1]/div[1]/div/div[2]/div[2]/div/div[9]/button'
balance_xp = '/html/body/div[1]/div/div[3]/div/div/div/div[2]/div/div[1]/div/div/div/div/div/span[1]'


if driver.find_element(By.XPATH, '/html/body/div/div/div[1]/div/div[5]/span').text == 'MARKETPLACE':
	id_pers_class = 'card-shop-name market-id'
	url_star = '/_next/image?url=%2Fassets%2Fimages%2Fstones%2Fstar1.png&w=96&q=75'
if driver.find_element(By.XPATH, '/html/body/div/div/div[1]/div/div[5]/span').text == 'INVENTORY':
	id_pers_class = 'index-number'
	url_star = '/_next/image?url=%2Fassets%2Fimages%2Fstones%2Fstar1.png&w=64&q=75'
if driver.find_element(By.XPATH, '/html/body/div/div/div[1]/div/div[5]/span').text == 'BATTLE':
	id_pers_class = 'index-number'
	url_star = '/_next/image?url=%2Fassets%2Fimages%2Fstones%2Fstar1.png&w=64&q=75'

# for i in range(10):
text_html = driver.page_source
soup = BeautifulSoup(text_html, 'html.parser')

divs = soup.findAll("div", {"class": "card-shop"})
for card in divs:
	id_pers = card.find("div", {"class": id_pers_class})
	if id_pers == None:
		id_pers = card.find("div", {"class": id_pers_class})
	if id_pers == None:
		break
	print(id_pers.text)
	rows = card.findAll("div", {"class": "card-shop-row"})
	imgs = card.findAll("img")
	stars = 0
	for img in imgs:
		if img['src'] == url_star:
			stars += 1
		# print(img['src'])
	print(f'stars\t\t{stars}')
	for row in rows:
		pers_info_label = row.find("div", {"class": "card-shop-label"})
		pers_info_value = row.find("div", {"class": "card-shop-value"})
		if not (pers_info_label == None) or not (pers_info_value == None):
			print(f'{pers_info_label.text}\t\t{pers_info_value.text}')
			# Звезда
			# Цена
			# Уровень
			# Опыт
			if (pers_info_label.text == 'price'
				and
				(int(pers_info_value.text.replace(',', '')) <= red_price)
				and
				stars >= red_stars
				and
				pers_info_label.text == 'Level'
				and
				int(pers_info_value.text) >= red_lvl):
				driver.find_element(By.XPATH, buy_xp).click() # kupit geroya
				time.sleep(1)
				driver.find_element(By.XPATH, '/html/body/div[2]/div/div[6]/button[1]').click() # OK
				
				driver.switch_to.window(driver.window_handles[0])
				driver.get('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html')
				#
				time.sleep(4)

				if xpath_exist(accept_btn):
					driver.find_element(By.XPATH, accept_btn).click() # prinyat
				else:
					print('popolni balance')
				#
				time.sleep(3)

				driver.switch_to.window(driver.window_handles[2])
				time.sleep(1)
				driver.get('https://app.galaxyadventure.io/fight-monster')
				time.sleep(3)

			if (pers_info_label.text == 'price'
				and
				(int(pers_info_value.text.replace(',', '')) <= norm_price)
				and
				stars >= norm_stars
				and
				pers_info_label.text == 'Level'
				and
				int(pers_info_value.text) >= norm_lvl):
				accept_buy = input('kupit dannogo geroya? da/net')
				if accept_buy == 'da':
					driver.find_element(By.XPATH, buy_xp).click() # kupit geroya
					time.sleep(1)
					driver.find_element(By.XPATH, '/html/body/div[2]/div/div[6]/button[1]').click() # OK
					
					driver.switch_to.window(driver.window_handles[0])
					driver.get('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html')
					#
					time.sleep(4)

					if xpath_exist(accept_btn):
						driver.find_element(By.XPATH, accept_btn).click() # prinyat
					else:
						print('popolni balance')
					#
					time.sleep(3)

					driver.switch_to.window(driver.window_handles[2])
					time.sleep(1)
					driver.get('https://app.galaxyadventure.io/fight-monster')
					time.sleep(3)



	print('\n')
	time.sleep(10)