# -*- coding: utf-8 -*-


import urllib2
from bs4 import BeautifulSoup
import random
import time
import sys
sys.path.append("/home/david/iPython") 
import helpers
import re

urls = ["http://obraspublicas.corrientes.gob.ar/home/autoridad", 
       "http://catastro.corrientes.gob.ar/home/autoridades",
       "http://vialidad.corrientes.gov.ar/noticia/autoridades--2"]
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}


Links = ["http://coordinacion.corrientes.gob.ar/home/autoridades", 
         "http://salud.corrientes.gob.ar/home/autoridades",
         "http://icaa.corrientes.gob.ar/home/autoridades",
         "http://senergia.corrientes.gob.ar/home/autoridades",
         "http://recursosforestales.corrientes.gob.ar/home/autoridades",
         "http://www.corrientes.gov.ar/home/autoridades"]  

def helper(name,pos,url,minis):
    
    entity = {
            "_meta": {
                "id": re.sub("[^a-zA-Z0-9]", "", name + str(random.random())),
                "entity_type": "person"
            },
            "name": name,
            "fields": [
          {"tag": "picture_url", "value": url},
          {"tag": "chamber", "value": minis},
          {"tag": "political_position", "value":pos}]
    }
    helpers.emit(entity)

def replacer(text):
    res = text.replace("<strong>","").replace("Dr.","").replace("Dra.","").replace("Ing.",""). \
    replace("Lic.","").replace("Farm.","").replace("C.P.","").replace("Hidráulico y Civil",""). \
    replace("Agrim. Nac.","").replace("Agrim.","").replace("Ftal.","").replace("Zona N° 1",""). \
    replace("-","").replace("Civil","").replace("CP.","").replace("Agron.","").replace("Arq.","").replace("Cr.","")
    return res
    
def scrap():
    perfis = []
    for Link in Links:
        time.sleep(random.uniform(0.3,0.7))
        req = urllib2.Request(Link, headers=hdr)
        page = urllib2.urlopen(req)

        positions = ["Producción", "Ministro"]

        soup = BeautifulSoup(page, "html.parser")
        
        try:
            minister = soup.find("div",{"class":"sub-wrap"})
            ministerio = str(minister).split("<small>")[0].split("<span>")[1].strip()
        except Exception as e:
            ministerio = "N/A"
        

        content = soup.find_all("li",{"class":"media"})
        regex1 = "<strong>(.+?)</strong>" 

        ever=[]
        for i in content:
            try:
                pattern = re.compile(regex1)
                name, pos = [replacer(j).strip() 
                             for j in re.findall(pattern,str(i)) 
                             if j.replace("<strong>","").strip() != '<br/>']
                for k in positions:
                    if k in name:
                        pos, name = [replacer(j).strip() 
                                     for j in re.findall(pattern,str(i))]
            except Exception as e:
                regex_name = "<strong>(.+?)</strong>" 
                regex_pos = '<strong style="text-align: center;">(.+?)</strong>' 
                    
                pattern_name = re.compile(regex_name)
                pattern_pos = re.compile(regex_pos)
                
                name = [replacer(j).strip() 
                        for j in re.findall(pattern_name,str(i)) 
                        if j.replace("<strong>","").strip() != '<br/>'][0]
                pos = [replacer(j).strip() for j in re.findall(pattern_pos,str(i)) 
                             if j.replace("<strong>","").strip() != '<br/>'][0]
            try:
                if "email" not in i.img["src"] and "telefono" not in i.img["src"]:
                    url = "http://www.corrientes.gov.ar" + str(i.img["src"])
                else:
                    url = "N/A"
            except Exception as e:
                url = "N/A"
            helper(name,pos,url,ministerio)
            time.sleep(random.uniform(0.2,0.4))
        perfis = ever
        
    return perfis

def obras_publicas():
    req = urllib2.Request(urls[0], headers=hdr)
    page = urllib2.urlopen(req)

    soup = BeautifulSoup(page, "html.parser")
    
    try:
        minister = soup.find("div",{"class":"sub-wrap"})
        ministerio = str(minister).split("<small>")[0].split("<span>")[1].strip()
    except Exception as e:
        ministerio = "N/A"
    
    article = soup.find("article",{"class":"page"})
    url = "http://www.corrientes.gov.ar" + str(article.img["src"])
    texto = [i.getText().strip() for i in article.find_all("p")]
    pos = texto[-2]
    name = texto[-1]
    helper(name,pos,url,ministerio)
 
def catastro():
    req = urllib2.Request(urls[1], headers=hdr)
    page = urllib2.urlopen(req)

    soup = BeautifulSoup(page, "html.parser")
    
    try:
        minister = soup.find("div",{"class":"sub-wrap"})
        ministerio = str(minister).split("<small>")[0].split("<span>")[1].strip()
    except Exception as e:
        ministerio = "N/A"
    
    content = soup.find_all("li", {"class":"media"})
    
    article = soup.find("article",{"class":"page"})
    
    regex1 = "<strong>(.+?)</strong>" 

    ever=[]
    for i in range(len(content)):
        if i < 2:
            pattern = re.compile(regex1)
            texto = [replacer(j).strip() 
                     for j in re.findall(pattern,str(content[i])) 
                     if j.replace("<strong>","").strip() != '<br/>']
        
            name = texto[0]
            pos = texto[1]
        else:
            name = [replacer(j).strip() 
                    for j in re.findall(pattern,str(content[i])) 
                    if j.replace("<strong>","").strip() != '<br/>'][0]
            pos = "Jefes de Zona"
        try:
            if "email" not in content[i].img["src"] and "telefono" not in content[i].img["src"]:
                url = "http://www.corrientes.gov.ar" + str(content[i].img["src"])
            else:
                url = "N/A"
        except Exception as e:
            url = "N/A"
        time.sleep(random.uniform(0.2,0.4))
        helper(name,pos,url,ministerio)
    return ever

def main():
    scrap()
    time.sleep(random.uniform(0.2,0.4))
    obras_publicas()
    time.sleep(random.uniform(0.2,0.4))
    catastro()