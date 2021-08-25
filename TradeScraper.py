#Proof of concept Tradera Username Webscraper.
# Scrapes all users from first account to final
# Saves it as a textfile for every 100 000th user
# DO NOT RUN THIS AT LONG INTERVALS AS IT MIGHT BE AGAINST TOS
# I AM NOT RESPONSIBLE FOR HOW YOU USE THIS PROGRAM
# And do not for the love of god run this in a threaded instance, this will definitely get you IP banned.

from bs4 import BeautifulSoup
import requests
import os
import sys


path = os.getcwd()
foldername = "ScrapedFolder"
path = os.path.join(os.getcwd(), foldername)

breaker = 0

# Checks if account is active
def isActive(currentPage):
    accountActive = False
    redirecturl = str(currentPage.url)
    if 'deregistered' not in redirecturl:
        accountActive = True
    return accountActive

# Checks if account is valid
def isValid(soup):
    accountValid = False
    title = soup.find_all('title')
    if "Sidan kan inte hittas på Tradera.com" not in str(title):
        accountValid = True
    return accountValid

# final function used to combine and return the scraped strings
def strCombiner(number):
    global breaker
    url = "https://www.tradera.com/profile/feedback/{}/".format(str(number))
    currentPage = requests.get(url)
    if isActive(currentPage) == True:
        soup = BeautifulSoup(currentPage.content,
                             'html.parser')  # sorts with bs4
        if isValid(soup) == True:
            breaker = 0
            location = soup.find_all('span', {"class": "text-paragraph"})
            location = str(location).split('>')[1]
            location = location.split('<')[0]
            username = soup.find_all('title')
            username = str(username).replace(
                "[<title>Alla omdömen om ", "").replace(" på Tradera.com</title>]", "")
            return username, location, number
        else:
            print("Counter breaks at 100, current:", breaker)
            breaker+=1
            return "Error Page"
    else:
        breaker = 0
        return str(currentPage.url).split('/')[6], number

def writer(path, lists):
    with open(path, 'a', encoding='utf8') as a_writer:
        for s in lists:
            a_writer.write(str(s) + "\n")
        a_writer.close


def run():
    global breaker
    number = 0
    contentlist = []
    part = 0
    if not os.path.exists(path):
        os.makedirs(foldername)
    while True:
        if breaker == 100:
            print("Script is most likley done")
            break
        try:
            userInfo = strCombiner(number)
            contentlist.append(userInfo)
            print(userInfo)
        except KeyboardInterrupt:
            writer(path + "\\extracted_test{}.txt".format("_NotCompleteUserStop"), contentlist)
            break
        except:
            print("An exception occurred")
        number+=1
        if len(contentlist) == 20000:
            part+=1
            newpath = path + "\\extracted_test{}.txt".format("part" + str(part))
            writer(newpath, contentlist)
            contentlist = []

print(run())
