from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
import time
from Match_Class import Match
from difflib import SequenceMatcher


def Create_List(elements):  # Create list of websites elements (teams or odds)
    element_list = []
    for element in range(len(elements)):
        element_list.append(elements[element].text)
    return element_list


def Create_Object(Teams_list, Odds_List, Website):  # Create match object list and returns it

    Website_list = []
    for index in range(0, len(Teams_list), 2):
        Odds_Index = int(3 * (index / 2))
        Website_list.append(
            Match(Teams_list[index], Teams_list[index + 1], float(Odds_List[Odds_Index]), float(Odds_List[Odds_Index + 1]),
                  float(Odds_List[Odds_Index + 2]), Website))
    return Website_list


def Compare_Websites(website_1, website_2):
    count = 0
    for i in range(0, len(website_1)):
        for j in range(0, len(website_2)):
            if (SequenceMatcher(None,website_1[i].Team_1,website_2[j].Team_1).ratio()>0.5) and (SequenceMatcher(None,website_1[i].Team_2,website_2[j].Team_2).ratio()>0.5):
                print(website_1[i].Team_1 +" vs " +website_2[j].Team_2)
                Calculate_Arbitrage(website_1[i], website_2[j])
                count += 1
                break
    print(count)

def Calculate_Arbitrage(Match_obj_1, Match_obj_2):  # Calculate Arbitrage
    list_All = [[Match_obj_1.Win_1, Match_obj_2.Win_1], [Match_obj_1.Draw, Match_obj_2.Draw],
                [Match_obj_1.Win_2, Match_obj_2.Win_2]]
    Co = []
    arb = 0
    for i in range(0, 3):
        if list_All[i][0] < list_All[i][1]:
            b_odd = list_All[i][1]
        else:
            b_odd = list_All[i][0]
        Co.append(b_odd)
        arb += 1/b_odd
    print(arb)
    if arb < 1:
        print("Hello" + Match_obj_1.Website + "and" + Match_obj_2.Website + " Rate " + str(arb) + str(Co))


def Scrape(link, team_path, odds_path, cookie_path=""):  # Scrape information from website
    s = Service(r"C:\Users\Gustav Jenner\Downloads\chromedriver.exe")
    driver = webdriver.Chrome(service=s)
    driver.get(link)
    time.sleep(10)
    if cookie_path != "":
        Allow_cookies = driver.find_element(By.XPATH, cookie_path)
        Allow_cookies.click()
        time.sleep(5)
    Teams = driver.find_elements(By.XPATH, team_path)
    Team_List = Create_List(Teams)
    Odds = driver.find_elements(By.XPATH, odds_path)
    Odds_List = Create_List(Odds)

    #driver.quit()

    return [Team_List, Odds_List]


def man():
    Campo_data = Scrape("https://campobet.se/sv/sport/prelive?sportids=0&catids=0&champids=16808",
                        '//*[@class="asb-text asb-pos-wide"]',
                        '//*[@class = "asb-flex-cc asb-unshrink _asb_price-block-content-price "]/span',
                        '//*[@class="gdpr-cookies__btn g-btn g-btn-green ng-binding"]') #champions league

    Unibet_data = Scrape("https://www.unibet.com/betting/sports/filter/football/champions_league/all/matches",
                    '//*[@class = "c539a"]', '//*[@class = "_8e013"]',
                    '//*[@id = "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"]') #champions league


    print(Campo_data[0][1])

    Campo = Create_Object(Campo_data[0],Campo_data[1],"Campo")
    Unibet = Create_Object(Unibet_data[0],Unibet_data[1],"Unibet")

    Compare_Websites(Campo,Unibet)

def open():
    s = Service(r"C:\Users\Gustav Jenner\Downloads\chromedriver.exe")
    driver = webdriver.Chrome(service=s)
    driver.get("https://campobet.se/sv/sport/prelive?sportids=0&catids=0&champids=16808")
    time.sleep(10)


open()

# %%

