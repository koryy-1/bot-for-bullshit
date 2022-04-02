cooldown = '/html/body/div/div/div[2]/div/div[1]/div/div[3]/div/div/div[2]/div/div[6]/div[2]/p'
balance = '/html/body/div[1]/div/div[3]/div/div/div/div[2]/div/div[1]/div/div/div/div/div/span[1]'
fight_btn = '/html/body/div/div/div[2]/div/div[2]/div/div/div[1]/div/div[2]/div[2]/button'
accept_btn = '/html/body/div[1]/div/div[3]/div/div[4]/div[3]/footer/button[2]'
close_btn = '/html/body/div[3]/div/div/div[1]/button'

timing = driver.find_element_by_xpath(cooldown).text

# while True:
print(timing)
if timing == '00:00:00':
	# pereklu4it okna
	driver.find_element_by_xpath(fight_btn).click() # 1 lvl boss
	# '/html/body/div[3]/div/div/div[1]/div' battle

	driver.switch_to.window(driver.window_handles[0]) # metamask
	time.sleep(0.5)
	prev_balance = driver.find_element_by_xpath(balance).text
	next_balance = prev_balance

	driver.find_element_by_xpath(accept_btn).click() # prinyat

	while prev_balance == next_balance:
		next_balance = driver.find_element_by_xpath(balance).text # sravnit 4isla
		time.sleep(5)
	
	driver.switch_to.window(driver.window_handles[2]) # game
	time.sleep(10)
	driver.find_element_by_xpath(close_btn).click() # krestik
	
	# time.sleep(60*60*6)
		something