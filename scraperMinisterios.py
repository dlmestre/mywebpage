# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import random
import time
import sys
sys.path.append(r"C:\Users\CHUSA\Documents")
import helpers
import re
from selenium import webdriver

path = r"C:\Users\CHUSA\phantomjs-2.0.0-windows\phantomjs-2.0.0-windows\bin\phantomjs.exe"


Urls = ["http://sanluis.gov.ar/ministerios/", 
        "http://sanluis.gov.ar/gobernador/", 
        "http://sanluis.gov.ar/vicegobernador/"]


def helper(name,pos,url,title,url_page):
    
    entity = {
            "_meta": {
                "id": re.sub("[^a-zA-Z0-9]", "", name + str(random.random())),
                "entity_type": "person"
            },
            "name": name,
            "fields": [
          {"tag": "picture_url", "value": url},
          {"tag": "chamber", "value": title},
          {"tag": "url", "value": url_page},
          {"tag": "political_position", "value":pos}]
    }
    helpers.emit(entity)

def replacer(text):
    res = text.replace("<strong>","").replace("Dr.","").replace("Dra.","").replace("Ing.",""). \
    replace("Lic.","").replace("Farm.","").replace("C.P.","").replace("Hidráulico y Civil",""). \
    replace("Agrim. Nac.","").replace("Agrim.","").replace("Ftal.","").replace("Zona N° 1",""). \
    replace("-","").replace("Civil","").replace("CP.","").replace("(Mag.)","").replace("N.","")
    return res
    
def scrap_basic(url):
    driver = webdriver.PhantomJS(path)
    driver.set_window_size(1120,550)
    driver.implicitly_wait(10)
    driver.get(url)
    time.sleep(random.uniform(0.1,0.4))
    
    return driver

def main_page():
    driver = scrap_basic(Urls[0])
    soup = BeautifulSoup(driver.page_source, "html.parser")
    cont = soup.find("ul",{"class":"listado"})
    pages = ["http://sanluis.gov.ar" + str(i.a["href"]) for i in cont.find_all("li")]
    return pages

def Ministerios():
    
    Links = main_page()
    
    for Link in Links:
        driver = scrap_basic(Link)
        
        soup = BeautifulSoup(driver.page_source, "html.parser")
        
        try:
            title = str(soup.find("p", {"class","titulogrismin"})).split("<span>")[0].replace('<p class="titulogrismin">',"")
        except Exception as e:
            title = "N/A"
            
        first = soup.find("div",{"class":"nombre"})
        
        try:
            pos = [" ".join(replacer(i.text).split()) for i in first.find_all("div")][0]
        except Exception as e:
            pos = "N/A"
        try:
            name = [replacer(i.text).strip() for i in first.find_all("div")][1]
        except Exception as e:
            name = "N/A"
        try:
            foto = "http://sanluis.gov.ar" + str(soup.find("div",{"class":"fotoministro"}).img["src"]) 
        except Exception as e:
            foto = "N/A"
            
        helper(name, pos, foto, title, Link)
        
        time.sleep(random.uniform(0.3,0.7))
    
    
def Onigramas():
    Links = main_page()
    
    for Link in Links:
        driver = scrap_basic(Link)
        time.sleep(random.uniform(0.3,0.7))
        
        button_path = 'div.expandable-hitarea'
        
        foto = "N/A"
    
        buttons = driver.find_elements_by_css_selector(button_path)
    
        for button in buttons:
            webdriver.ActionChains(driver).move_to_element(button).click(button).perform()
            time.sleep(random.uniform(1.1,1.3))
        time.sleep(random.uniform(1.1,1.7))
        
        page = BeautifulSoup(driver.page_source, "html.parser")
        onigrama = page.find("ul", {"class":"treeview"})
        
        title = str(page.find("p", {"class","titulogrismin"})).split("<span>")[0].replace('<p class="titulogrismin">',"") 
    
        positions = [(i.text).strip() for i in onigrama.find_all("span",{"class":"catnombre"})]
        names = [replacer(i.text).strip() for i in onigrama.find_all("span",{"class":"catdescripcion"})]

        for i in range(len(positions)):
            helper(names[i], positions[i], foto, title, Link)
            time.sleep(random.uniform(0.2,0.4))

        time.sleep(random.uniform(0.3,0.7))

def governadores():
    for Url in Urls[1:]:
        driver = scrap_basic(Url)
        time.sleep(random.uniform(0.3,0.7))
        
        page = BeautifulSoup(driver.page_source, "html.parser")
        title = page.find("p", {"class","titulogris"}).text
        
        foto = "http://sanluis.gov.ar" + str(page.find("img",{"class":"fotoprincipal"})["src"]) 
        
        pos = page.find("div", {"class":"tituloDoble"}).h3.text
        name = page.find("div", {"class":"tituloDoble"}).h2.text
        name = replacer(name).strip()
        
        helper(name, pos, foto, title, Url)
    
    for Url in Urls[1:]:
        driver = scrap_basic(Url)
        time.sleep(random.uniform(0.3,0.7))
        
        page = BeautifulSoup(driver.page_source, "html.parser")
        onigrama = page.find("ul", {"class":"treeview"})
        
        title = page.find("p", {"class","titulogris"}).text
        
        foto = "N/A"
        
        positions = [(i.text).strip() for i in onigrama.find_all("span",{"class":"catnombre"})]
        names = [replacer(i.text).strip() for i in onigrama.find_all("span",{"class":"catdescripcion"})]

        for i in range(len(positions)):
            helper(names[i], positions[i], foto, title, Url)
            time.sleep(random.uniform(0.2,0.4))

        time.sleep(random.uniform(0.3,0.7))
    
def main():
    Ministerios()
    Onigramas()
    governadores()
    

