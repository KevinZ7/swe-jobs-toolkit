import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from urllib.parse import urlparse, parse_qs
from selenium.webdriver.common.action_chains import ActionChains
import random
from time import sleep
from fake_useragent import UserAgent

currentFilePath = os.path.dirname(__file__)

chromeProfilePath = "C:\\Users\\Kevin\\AppData\\Local\\Google\\Chrome for Testing\\User Data"
chromeProfileDirectory = "Profile 1"
chromeDriverPath = "c:\\Programming Tools\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe"
chromeBinaryPath = r"C:\Programming Tools\chrome-win64\chrome-win64\chrome.exe"

options = Options()
options.add_argument(f"user-data-dir={chromeProfilePath}")
options.add_argument(f"profile-directory={chromeProfileDirectory}")
options.binary_location = chromeBinaryPath

service= Service(executable_path=chromeDriverPath)
driver = webdriver.Chrome(options=options, service=service)
actions = ActionChains(driver)
driver.implicitly_wait(4)
BASE_URL = "https://www.google.ca/"
URL_MAX_RETRY = 5



def getCompanyIds(driver,companyName, baseUrl):
  sleep(random.random()*2)
  try:
    retryCounter = 0
    while not driver.current_url.startswith(BASE_URL) and retryCounter < 5:
      sleep(random.random()*5)
      driver.get(baseUrl)
      retryCounter += 1
    
    if not driver.current_url.startswith(BASE_URL):
      raise ConnectionError(f"Base Linkedin URL incorrect: received {driver.current_url} instead of {BASE_URL}")


    googleSearchTextInputXpath = '//*[@id="APjFqb"]'
    
    googleSearchTextInput = driver.find_element(By.XPATH,googleSearchTextInputXpath)
    sleep(random.random()*2)
    googleSearchTextInput.click()
    searchInput = f"site:linkedin.com {companyName} jobs"
    for char in searchInput:
      sleep(random.random()*0.3)
      googleSearchTextInput.send_keys(char)
    sleep(random.random()*2)
    googleSearchTextInput.send_keys(Keys.ENTER)

    
    firstResult = driver.find_element(By.TAG_NAME, "h3")
    firstResult.click()

    showAllJobsButtonXpath = "//*[text()='Show all jobs']"
    showAllJobsButton = driver.find_element(By.XPATH,showAllJobsButtonXpath)
    sleep(random.random()*1)
    showAllJobsButton.click()

    sleep(1)
    url = driver.current_url

    parsedUrl = urlparse(url)
    queryParams = parse_qs(parsedUrl.query)

    companyIds = queryParams.get('f_C')


    if companyIds:
      return companyIds[0]
    else:
      return ""
  except Exception as e:
    print(e)
    return ""



companiesFilePath = os.path.join(currentFilePath,'..','interesting_tech_companies.txt')
companiesIdFilePath = os.path.join(currentFilePath,'..','tech_company_linkedin_ids.txt')
companyToIds = {}
with open(companiesFilePath, 'r', encoding='utf-8') as file:
  with open(companiesIdFilePath,'a',encoding='utf-8') as writeFile:
    rawInput = file.read()
    companies = rawInput.split('\n')
    companies.pop()

    for company in companies:
      name, careerLink = company.split('|')
      companyIds = getCompanyIds(driver,name,BASE_URL)
      writeFile.write(f"{name}:{companyIds}\n")


