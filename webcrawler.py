from selenium import webdriver
import os


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
    driver.implicitly_wait(10)
    driver.get(url)
    anime_details = [] #A single array with 3 elements [Anime_name, Status, Latest Episode]
    anime_details.append(driver.find_element_by_xpath("//p[@class='alias']").text.split(';')[0]) #index 0 - Anime
    anime_details.append(driver.find_element_by_xpath("//*[@id='main']/div/div[5]/div/div/div[2]/div[3]/dl[1]/dd[2]").text) #index 1 - Status
    latest_range = len(driver.find_elements_by_xpath("//div[@id='episode_page']/span")) - 1
    latest_ep = driver.find_elements_by_xpath("//div[@id='episode_page']/span")[latest_range].get_attribute("ep_end")
    anime_details.append(latest_ep) #index 2 - Latest episode
    driver.quit()
    return anime_details

def get_anime_details(anime_name):
    global url_addition
    url_addition = "watch/" + format_anime_name(anime_name)
    #Set up selenium web crawling driver
    #driver = webdriver.Chrome(os.getcwd() + "/chromedriver") #current directory of chromedriver.exe (UNCOMMENT TO TEST LOCALLY)
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options) #(UNCOMMENT TO TEST ON SERVER)
    driver.implicitly_wait(10)
    driver.get(main_url + url_addition)
    anime_details = [] #A single array with 3 elements [Anime_name, Status, Latest Episode]
    anime_details.append(anime_name) #index 0 - Anime
    anime_details.append(driver.find_element_by_xpath("//*[@id='main']/div/div[5]/div/div/div[2]/div[3]/dl[1]/dd[2]").text) #index 1 - Status
    latest_range = len(driver.find_elements_by_xpath("//div[@id='episode_page']/span")) - 1
    latest_ep = driver.find_elements_by_xpath("//div[@id='episode_page']/span")[latest_range].get_attribute("ep_end")
    anime_details.append(latest_ep) #index 2 - Latest episode
    driver.quit()
    return anime_details


def format_anime_name(animename): #Format anime name to be website-link-friendly
    animename = animename.replace(' ', '-')
    if "(" and ")" in animename:
        animename = animename.replace('(', '')
        animename = animename.replace(')', '')
    if ":" in animename:
        animename = animename.replace(':','')
    return animename
