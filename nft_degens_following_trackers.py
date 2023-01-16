try:
    import tweepy
    import requests
    from bs4 import BeautifulSoup
    from selenium import webdriver
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    import re
    import os
    import time
    from datetime import datetime, timezone
    import ast
    from rich.console import Console
    from rich.table import Column, Table
    import random
    import platform
    from discord_webhook import DiscordWebhook, DiscordEmbed

    from selenium.webdriver.chrome.options import Options

    chrome_options=Options()
    # chrome_options.addArguments("--window-size=1920,1080")
    # chrome_options.addArguments("--start-maximized")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-software-rasterizer")
    # chrome_options.add_argument("window-size=1400,2100") 
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument('--disable-dev-shm-usage')
except:
    print("Please run 'pip install -r requirements.txt' to install the required modules before running again.\n")

start_time = time.time()

### Discord Channel Webhook ###

WEBHOOK_URL = 'https://discord.com/api/webhooks/937332643064860724/UNx8Ea2Xh1v-8s9PuiV2UACPhm9NwW5Jcg6HKxGA3j5hqhM9s21zhKk77vWjSkOyz90Y'

print('\nScanning what the degens are following ...\n')

webhook = DiscordWebhook(url=WEBHOOK_URL, rate_limit_retry=True, )

embed = DiscordEmbed(title="Running 'nft_degens_followings_trackers.py'", description='Scanning what the degens are following lately ...')
webhook.add_embed(embed)

response = webhook.execute()

### Retrieve the list of degens ###

with open("degens_list.txt") as file:
    lines = file.readlines()
    lines = [line.rstrip() for line in lines]
file.close()

print('Retrieved the list of degens ...\n')

## Create .txt that contains each degens' followings in the previous check separately

new_file_flag = 0

if os.path.exists('prev_followings.txt')==False:  
    new_file_flag = 1
    create_file= open("prev_followings.txt",'w+')  # This is just to  create the file in case it doesn't exist
    create_file.close()
else:
    with open('prev_followings.txt') as f:
        prev_followings_dict = ast.literal_eval(f.read().replace('\n', ''))

print("Retrieved every degens' followings in the previous check ...\n")

rerun_num = 1   


### TWITTER DOES NOT SHOW FOLLOWINGS IN REVERSE CHRONOLOGICAL ORDER ###

# ### Access to Twitter ###
# url = 'https://twitter.com/i/flow/login'
# driver.get(url)

# print("Logging in ...\n")

# ### Credentials ###

# email = 'ENTER EMAIL'
# username = 'ENTER TWITTER USERNAME'
# password = 'ENTER PASSWORD'

# # Find login box
# username_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[@class='r-30o5oe r-1niwhzg r-17gur6a r-1yadl64 r-deolkf r-homxoj r-poiln3 r-7cikom r-1ny4l3l r-t60dpp r-1dz5y72 r-fdjqy7 r-13qz1uu']")))
# time.sleep(3)
# username_input.send_keys(email, Keys.ENTER)

# WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[@class='r-30o5oe r-1niwhzg r-17gur6a r-1yadl64 r-deolkf r-homxoj r-poiln3 r-7cikom r-1ny4l3l r-t60dpp r-1dz5y72 r-fdjqy7 r-13qz1uu']")))
# corpus = BeautifulSoup(driver.page_source, 'html.parser')
# text_box_unprocessed = corpus.find_all("span", {"class": "css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0"})
# text_box_processed = text_box_unprocessed[0].get_text()

# if 'phone number or username' in text_box_processed:
#     user_name_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[@class='r-30o5oe r-1niwhzg r-17gur6a r-1yadl64 r-deolkf r-homxoj r-poiln3 r-7cikom r-1ny4l3l r-t60dpp r-1dz5y72 r-fdjqy7 r-13qz1uu']")))
#     time.sleep(3)
#     user_name_input.send_keys(username, Keys.ENTER)
#     password_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[@class='r-30o5oe r-1niwhzg r-17gur6a r-1yadl64 r-deolkf r-homxoj r-poiln3 r-7cikom r-1ny4l3l r-t60dpp r-1dz5y72 r-fdjqy7 r-13qz1uu']")))
#     time.sleep(3)
#     password_input.send_keys(password, Keys.ENTER)
# else:
#     password_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[@class='r-30o5oe r-1niwhzg r-17gur6a r-1yadl64 r-deolkf r-homxoj r-poiln3 r-7cikom r-1ny4l3l r-t60dpp r-1dz5y72 r-fdjqy7 r-13qz1uu']")))
#     time.sleep(3)
#     password_input.send_keys(password, Keys.ENTER)

# time.sleep(5)

if 'mac' in platform.platform().lower():
    print('PC is not Mac OS, using chromedriver for MacOS ...\n')
    chrome_options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    driver = webdriver.Chrome('./chromedriver_mac64/chromedriver', chrome_options=chrome_options)
else:
    print('PC is Windows OS, using chromedriver for Windows ...\n')
    chrome_options.binary_location = "C:\Program Files\Google\Chrome\Application\chrome.exe"
    driver = webdriver.Chrome('./chromedriver_win32/chromedriver.exe', chrome_options=chrome_options)

followings_dict = {}
cur_new_followings_summary_set = set()

console = Console()

table = Table(show_lines = True, header_style="bold yellow")
table.add_column("Degen", style="dim", width=40)
table.add_column("New Followings in Twitter", justify="right")

total_degens = len(lines)
count = 0

for line in lines:
    # print(line)

    rerun_state = 0

    count = count + 1

    if line == '':
        print('Empty line found. Please delete the line. Skipping ...')
        continue

    while (rerun_state == 0):

        try:

            homepage = 'https://en.whotwi.com/'

            print('(' + str(count) + '/' + str(total_degens) + ') ' + 'Scanning @' + line.split('/')[-1] + ' ...\n')

            url = homepage + line + '/friends'

            driver.get(url)

            # time.sleep(30)

            page_flag = 0
            followings_flag = 0
            user_not_found_flag = 0
            user_private_flag = 0
            user_suspended_flag = 0

            timeout = 40   # [seconds]
            timeout_start = time.time()

            while followings_flag == 0:
                while page_flag == 0:
                    if time.time() > timeout_start + timeout:
                        print('Refreshing ' + url + ' ...\n')
                        driver.get(url)
                        timeout = 40   # [seconds]
                        timeout_start = time.time()
                    for text in driver.find_elements_by_xpath('//div[@id="user_column_summary_screen_name"]'):
                        if line.lower() in text.get_attribute('textContent').lower():
                            page_flag = 1
                            break
                    for text in driver.find_elements_by_xpath('//div[@class="white_page"]'):
                        if 'not found' in text.get_attribute('textContent'):
                            page_flag = 1
                            user_not_found_flag = 1
                            break
                    for text in driver.find_elements_by_xpath('//ul[@class="user_column_info_list"]'):
                        if 'Private' in text.get_attribute('textContent'):
                            page_flag = 1
                            user_private_flag = 1
                            break
                    for text in driver.find_elements_by_xpath('//div[@class="white_page"]'):
                        if 'suspended' in text.get_attribute('textContent'):
                            page_flag = 1
                            user_suspended_flag = 1
                            break
                if user_not_found_flag == 1:
                    followings_flag = 1
                elif user_private_flag == 1:
                    followings_flag = 1
                elif user_suspended_flag == 1:
                    followings_flag = 1
                else:
                    try:
                        WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, "//ul[@class='user_list']")))
                        followings_flag = 1
                    except:
                        print('Reconnecting to ' + url + ' ...\n')
                        page_flag = 0
                        driver.get(url)
                        timeout = 40   # [seconds]
                        timeout_start = time.time()

            if user_not_found_flag == 1:
                print('Skipping @' + line.split('/')[-1] + ' as the user is not found ...\n')
                webhook = DiscordWebhook(url=WEBHOOK_URL, rate_limit_retry=True)
                followings_text = 'Skipping @' + line.split('/')[-1] + ' as the user is not found ...\n\n'
                embed = DiscordEmbed(title="(" + str(count) + "/" + str(total_degens) + ") " + "@" + line.split('/')[-1] + "'s latest followings", description=followings_text)
                webhook.add_embed(embed)
                response = webhook.execute()
                break

            if user_private_flag == 1:
                print('Skipping @' + line.split('/')[-1] + ' as the user is private ...\n')
                webhook = DiscordWebhook(url=WEBHOOK_URL, rate_limit_retry=True)
                followings_text = 'Skipping @' + line.split('/')[-1] + ' as the user is private ...\n\n'
                embed = DiscordEmbed(title="(" + str(count) + "/" + str(total_degens) + ") " + "@" + line.split('/')[-1] + "'s latest followings", description=followings_text)
                webhook.add_embed(embed)
                response = webhook.execute()
                break

            if user_suspended_flag == 1:
                print('Skipping @' + line.split('/')[-1] + ' as the user is suspended ...\n')
                webhook = DiscordWebhook(url=WEBHOOK_URL, rate_limit_retry=True)
                followings_text = 'Skipping @' + line.split('/')[-1] + ' as the user is suspended ...\n\n'
                embed = DiscordEmbed(title="(" + str(count) + "/" + str(total_degens) + ") " + "@" + line.split('/')[-1] + "'s latest followings", description=followings_text)
                webhook.add_embed(embed)
                response = webhook.execute()
                break

            time.sleep(random.randint(1, 3))                          # delay for human-like effect

            new_followings_set = set()
            new_followings_list = []
            description_dict = {}

            for following in driver.find_elements_by_xpath('//ul[@class="user_list"]//span[@class="user_list_screen_name"]'):
                # print(following.get_attribute('textContent'))
                new_followings_set.add(following.get_attribute('textContent'))
                new_followings_list.append(following.get_attribute('textContent'))

            description_count = 0
            for description in driver.find_elements_by_xpath('//div[@class="col-sm-8 user_list_description_pc"]//span[@itemprop="description"]'):
                # print(following.get_attribute('textContent'))
                description_dict[new_followings_list[description_count]] = description.get_attribute('textContent')
                description_count = description_count + 1

            degen_id = line.split('/')[-1]

            followings_dict[degen_id] = new_followings_set

            if new_file_flag == 1:
                cur_new_followings_set = new_followings_set
            else:
                if degen_id in prev_followings_dict:
                    cur_new_followings_set = new_followings_set - set(prev_followings_dict[degen_id])
                else:
                    cur_new_followings_set = new_followings_set

            followings_text = ''

            if len(cur_new_followings_set) == 0:
                table.add_row(
                    degen_id, 'Nil'
                )
                followings_text = followings_text + 'Nil'
            else:
                row1_flag = 1
                for following in cur_new_followings_set:
                    if row1_flag == 1:
                        table.add_row(
                            degen_id, following
                        )
                        row1_flag = 0
                    else:
                        table.add_row( 
                            ' ', following
                        )
                    cur_new_followings_summary_set.add(following)
                    followings_text = followings_text + 'https://twitter.com/' + following.split('@')[1] + '\n' + description_dict[following] + '\n\n'

            webhook = DiscordWebhook(url=WEBHOOK_URL, rate_limit_retry=True)

            embed = DiscordEmbed(title="(" + str(count) + "/" + str(total_degens) + ") " + "@" + degen_id + "'s latest followings", description=followings_text)
            webhook.add_embed(embed)

            response = webhook.execute()

            rerun_state = 1

        except:
            rerun_state = 0
            rerun_num = rerun_num + 1
            if (rerun_num == 5):
                rerun_state = 1
                print("Error encountered when scraping data from Twitter. Skipping the user ...")
                rerun_num = 1
            else:
                driver.quit()

                print("Error encountered when scraping data from Twitter. Retrying the user ...")                           # TO DISPLAY IN TELEGRAM BOT
                webhook = DiscordWebhook(url=WEBHOOK_URL, rate_limit_retry=True, content='Error encountered when scraping data from Twitter. Restarting ...')
                response = webhook.execute()

if rerun_num == 5:
    print("Please check the programming and try again later.")
    webhook = DiscordWebhook(url=WEBHOOK_URL, rate_limit_retry=True, content='Please check the programming and try again later.')
    response = webhook.execute()
else:
    console.print(table)

    print("\nSummary of new followings in URL ...\n")

    for unique_following in cur_new_followings_summary_set:
        print('https://twitter.com/' + unique_following.split('@')[1])

    print("\nSaving degens' followings for next check ...\n")

    file_var = open('prev_followings.txt', "w+")
    file_var.write(str(followings_dict))
    file_var.close()

    driver.quit()

    print('Scanning complete.\n')
    webhook = DiscordWebhook(url=WEBHOOK_URL, rate_limit_retry=True, content='Scanning complete.')
    response = webhook.execute()

    duration = time.time() - start_time

    print('Total time taken: ' + str(duration) + 's')



