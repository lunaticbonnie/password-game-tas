import json
import locale
from time import sleep
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

EGG = "🥚"
NUMBERS = " 55555 "
MONTH = "may"
SPONSOR = "shell"
ROMAN_NUMBERS = "XXXV"
ELEMENTS = " Sm "
MOON_EMOJI = "🌕🌖🌗🌘🌑🌒🌓🌔"
LEAP_YEAR = " 0 "
FIRE_EMOJI = "🔥"
I_TEXT = " I am worthy"
WORM_EMOJI = "🐛"
STRONG_EMOJI = "🏋️‍♂️🏋️‍♂️🏋️‍♂️🏋️‍♂️🏋️‍♂️🏋️‍♂️"

def getCountriesString():
    countries = []
    with open("countries.txt", encoding="utf8") as f:
        for line in f.readlines():
            if line:
                countries.append(line.lower())
    return " " + " ".join(countries) + " "

def getWordleAnswer():
    words = {}
    with open("wordle.txt", encoding="utf8") as f:
        for line in f.readlines():
            if line:
                date, word = line.rsplit(" ", 1)
                words[date] = word
    locale.setlocale(locale.LC_ALL, "en_US")
    today = datetime.now().strftime("%b %d %Y")
    return words[today].lower()

def charCount(string: str, expected: str):
    return len([c for c in string if c == expected])

# utils
driver: WebDriver = None
def initWebDriver():
    global driver
    options = ChromeOptions()
    options.add_argument("--disable-logging")
    options.add_argument("--silent")
    options.add_argument("--log-level=3")
    options.add_argument("--disable-extensions")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-infobars")
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument(r"--user-data-dir=C:\Users\lin\AppData\Local\Google\Chrome\User Data\Default")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

def runJs(script: str, *args):
    return driver.execute_script(script, *args)

def getInnerHTML(element: WebElement):
    return runJs("return String(arguments[0].innerHTML)", element)

def sendKeys(element: WebElement, keys: str):
    element.click()
    runJs("arguments[0].innerHTML += arguments[1]", element, keys)

def getPasswordBox() -> WebElement:
    return driver.find_element(By.CSS_SELECTOR, ".ProseMirror")

if __name__ == '__main__':
    initWebDriver()
    driver.get("https://neal.fun/password-game/")
    runJs("window.getChess = () => document.querySelector('img.chess-img')")
    sendKeys(getPasswordBox(), EGG + getCountriesString() + NUMBERS + MONTH + SPONSOR + ROMAN_NUMBERS + getWordleAnswer() + ELEMENTS + MOON_EMOJI + LEAP_YEAR + I_TEXT + STRONG_EMOJI)
    while True:
        try:
            value = getInnerHTML(getPasswordBox())
            if charCount(value, FIRE_EMOJI) > 0:
                runJs("arguments[0].innerHTML = arguments[0].innerHTML.replaceAll('🔥', '.')", getPasswordBox())
                print("On fire!!!!")
            if charCount(value, WORM_EMOJI) < 4:
                sendKeys(getPasswordBox(), WORM_EMOJI * 4)
                sleep(3)
        except Exception as err:
            pass

# https://www.worldometers.info/geography/alphabetical-list-of-countries/
# https://www.esplora.org.mt/wp-content/uploads/2020/11/Periodic-Table-Picture-1.jpg
# https://nextchessmove.com/