import sys,os,collections
os.chdir(os.path.join(os.path.dirname(__file__)))
sys.path.insert(0,"_vendor")

import requests
from bs4 import BeautifulSoup

import csv
cantfind=[]
useragent={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
results=open("analysis_results.csv","r")
habitats=open("preferred_habitats.csv","w+")
reader=csv.reader(results)
writer=csv.writer(habitats)
next(reader)
writer.writerow(['Bird','Habitat'])
for row in reader:
    bird=row[0].split(" (")[0].replace(" ","_").replace("'","")
    html=BeautifulSoup(requests.get(f"https://www.allaboutbirds.org/guide/{bird}",headers=useragent).text,features="html.parser")
    print(bird)
    link=html.find("a",{"href":f"/guide/{bird}/lifehistory#habitat"})
    if not link:
        cantfind.append(bird)
        continue
    habitat=link.find("span",{"class":"text-label"}).text.removeprefix("Habitat")
    if habitat:
        writer.writerow([row[0],habitat])
    else:
        cantfind.append(bird)

print(cantfind)
