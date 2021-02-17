import requests
from bs4 import BeautifulSoup

url = "https://chemistry.fandom.com/wiki/List_of_elements_by_atomic_mass#fn_2"

source = requests.get(url).content

soup = BeautifulSoup(source, "html.parser")

div = soup.find("div", attrs={"class":"mw-parser-output"})
table = div.find_all("table")[1]
rows = table.find_all("tr")[1:]

f = open("atomicMass.csv", "w")

for r in rows:
    rowValues = r.find_all("td")

    symbol = rowValues[2].text
    atomicMass = rowValues[3].text

    if '(' in atomicMass:
        i = atomicMass.index('(')
        atomicMass = atomicMass[:i]
    if '[' in atomicMass:
        i = atomicMass.index(']')
        atomicMass = atomicMass.replace('[', '')
        atomicMass = atomicMass[:i-1]
    if ' ' in atomicMass:
        i = atomicMass.index(' ')
        atomicMass = atomicMass[:i]

    atomicMass = float(atomicMass)
    f.write(f"{symbol}, {atomicMass}\n")
    
