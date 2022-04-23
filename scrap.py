import requests
import numpy as np
from bs4 import BeautifulSoup
import time as t
import random as rand
import os

file = open("list_urls2.txt","r+")
list_of_urls = file.readlines()
print("I run !")
producent = input("Podaj producenta: ")
final_data = []
file_name = "data_"+producent+"001"+".csv"
z = 0

for list in list_of_urls:
    t.perf_counter()
    if z != 0:
        t.sleep(waiting)
    file = open("list_urls2.txt","r+")
    dir = file.readlines()[z]
    dns = "https://www.gsmarena.com/"
    nazwa,opis,zdjecia,linki = [],[],[],[]
    np.asarray((nazwa,opis,zdjecia,linki))
    url = dns+str(dir)
    url = url.strip()
    html =  requests.get(url)
    data = BeautifulSoup(html.text,features='html.parser')
    finding  = data.find('div',{'class':'makers'})
    print("Producent: "+producent+" | DNS: "+dns+" | URL: "+url+" | File name: "+file_name+" | HTML: "+str(html))
    
    for name in finding.find_all("span"):
        nazwa.append(producent+" "+name.text)

    for photos in finding.find_all("img"):
        zdjecia.append(photos.get("src"))

    for desc in finding.find_all("img"):
        opis.append(desc.get("title"))

    for link in finding.find_all("a"):
        linki.append(dns+link.get("href"))

    array_of_data = np.column_stack((nazwa,opis,linki,zdjecia))
    if z == 0:
        final_data = array_of_data
    else:
        final_data = np.row_stack((final_data ,array_of_data))
    waiting =  round(rand.uniform(0.5,2.1),2)
    print("Shape of data array: "+str(np.shape(array_of_data))+" | Shape of final data array: "+str(np.shape(final_data)))
    print("We wait: "+str(waiting)+" | Iteracja = "+str(z))
    np.savetxt(file_name,final_data,fmt='%s',delimiter=';',newline='\n',header='NAZWA;OPIS;LINKI;ZDJĘCIA',encoding="utf-8")
    z = z + 1

print("Saved as: "+file_name+" | Saved in: "+os.path.abspath(file_name)+" | Took me: "+str(round(t.perf_counter(),2))+"s")
file.close()