import json
import requests
from bs4 import BeautifulSoup

kor_hanja = {}

with open("kor_unicodes.json", 'r', encoding="utf8") as f:
    kor_letters = json.load(f)

headers = {"User-Agent":r"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"}

for letter in kor_letters:
    page = 1
    while True:
        kor_hanja[letter] = []

        url = f"https://hanja.dict.naver.com/#/search?range=letter&page={page}&query={letter}&autoConvert="
        res = requests.get(url, headers=headers)
        res.raise_for_status()

        print(res.text)
        soup = BeautifulSoup(res.text, 'lxml')
        hanjas = soup.find_all("a", attrs={'class':'hanja_link'})

        if len(hanjas) == 0:  # 종료조건
            break

        for hanja in hanjas:
            kor_hanja[letter].append(hanja)
            print(hanja)

        page += 1


