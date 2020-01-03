from bs4 import BeautifulSoup
from selenium import webdriver
import requests, os

#Chrome web driver set up for Heroku https://www.andressevilla.com/running-chromedriver-with-python-selenium-on-heroku/
chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")

main_url = "https://9anime.xyz/"
url_addition = ""

def set_anime_details(url):
    #Set up selenium web crawling driver
    #driver = webdriver.Chrome(os.getcwd() + "/chromedriver") #current directory of chromedriver.exe (UNCOMMENT TO TEST LOCALLY)
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options) #(UNCOMMENT TO TEST ON SERVER)
    data = requests.get(url).text
    driver.quit()
    soup = BeautifulSoup(data, 'lxml')
    anime_details = [] #A single array with 3 elements [Anime_name, Status, Latest Episode]
    anime_details.append(soup.find(class_="info").find(class_="title").text) #index 0 - Anime
    anime_details.append(soup.find(class_="info").find_all('dd')[1].text) #index 1 - Status
    anime_details.append(check_num_episodes(anime_details[0])) #index 2 - Latest episode
    return anime_details

def get_anime_details_by_name(anime_name):
    global url_addition
    url_addition = "watch/" + format_anime_name(anime_name)
    #Set up selenium web crawling driver
    #driver = webdriver.Chrome(os.getcwd() + "/chromedriver") #current directory of chromedriver.exe (UNCOMMENT TO TEST LOCALLY)
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options) #(UNCOMMENT TO TEST ON SERVER)
    data = requests.get(main_url + url_addition).text
    driver.quit()
    soup = BeautifulSoup(data, 'lxml')
    anime_details = [] #A single array with 3 elements [Anime_name, Status, Latest Episode]
    anime_details.append(soup.find(class_="info").find(class_="title").text) #index 0 - Anime
    anime_details.append(soup.find(class_="info").find_all('dd')[1].text) #index 1 - Status
    anime_details.append(check_num_episodes(anime_details[0])) #index 2 - Latest episode
    return anime_details

def check_num_episodes(animename):
    global url_addition
    url_addition = "watch/" + format_anime_name(animename)
    #Set up selenium web crawling driver
    #driver = webdriver.Chrome(os.getcwd() + "/chromedriver") #current directory of chromedriver.exe (UNCOMMENT TO TEST LOCALLY)
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options) #(UNCOMMENT TO TEST ON SERVER)
    driver.get(main_url + url_addition)
    data = driver.execute_script("return document.documentElement.outerHTML")
    driver.quit()
    soup = BeautifulSoup(data, 'lxml')
    #Get latest episode of Anime
    latest_range = len(soup.find(class_="range").find_all('span')) - 1
    return soup.find(class_="range").find_all('span')[latest_range].get('ep_end')

def format_anime_name(animename): #Format anime name to be website-link-friendly
    animename = animename.replace(' ', '-')
    if "(" and ")" in animename:
        animename = animename.replace('(', '')
        animename = animename.replace(')', '')
    if ":" in animename:
        animename = animename.replace(':','')
    return animename
