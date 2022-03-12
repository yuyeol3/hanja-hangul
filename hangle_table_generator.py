import json
from selenium import webdriver
from time import sleep
import shutil
import os

def get_driver():
    driver_options = webdriver.ChromeOptions()
    driver_options.add_argument('headless')

    driver = webdriver.Chrome(executable_path="chromedriver.exe", options=driver_options)
    url = "data:,"
    driver.get(url)
    driver.minimize_window()

    return driver


def main():
    dir_name = 'hangul_hanja'

    shutil.rmtree(dir_name)  # 폴더와 그 폴더 안의 항목들 삭제
    os.mkdir(dir_name)  # 경로 생성

    driver = get_driver()
    reset_count = 0

    with open("kor_unicodes.json", 'r', encoding="utf8") as f:
        kor_letters = json.load(f)


    num_of_char = len(kor_letters)

    for idx, letter in enumerate(kor_letters):
        print(f"{letter}: {((idx + 1) / num_of_char) * 100:.2f}% 완료")
        page = 1
        kor_hanja = []
        while True:
            url = f"https://hanja.dict.naver.com/#/search?range=letter&page={page}&query={letter}&autoConvert=false"
            driver.get(url)

            sleep(1)
            
            hanjas = driver.find_elements_by_class_name("hanja_link")
            hanjas = [i.text for i in hanjas]

            if len(hanjas) == 0:
                break

            for hanja in hanjas:
                kor_hanja.append(hanja)

            
            page += 1
            reset_count += 1
        
        if len(kor_hanja) >= 1:
            with open(f"hangul_hanja/{letter}.json", "w", encoding="utf8") as f:
                json.dump(kor_hanja, f)


        if reset_count >= 50:  # 메모리 누수 문제로 일정 횟수 이후 웹드라이버 초기화
            driver.close()
            driver = get_driver()
            reset_count = 0


if __name__ == "__main__":
    main()