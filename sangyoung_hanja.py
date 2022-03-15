from selenium import webdriver
import json

def main():
    driver = webdriver.Chrome(executable_path="chromedriver.exe")
    url = "https://ko.wiktionary.org/wiki/%EB%B6%80%EB%A1%9D:%ED%95%9C%EB%AC%B8_%EA%B5%90%EC%9C%A1%EC%9A%A9_%EA%B8%B0%EC%B4%88_%ED%95%9C%EC%9E%90_1800"
    driver.get(url)
    driver.minimize_window()

    tables = driver.find_elements_by_class_name("datatable")

    hanja_kor = {}

    for table in tables:
        rows = table.find_elements_by_tag_name("tr")[2:]
        for row in rows:
            cells = row.find_elements_by_tag_name("td")
            hanja_read = row.find_element_by_tag_name("th").text

            for cell in cells:
                hanjas = cell.find_elements_by_tag_name("a")
                for hanja in hanjas:
                    hanja_kor[hanja.text] = hanja_read



    print(hanja_kor)

    with open("preferences_2.json", "w", encoding="utf8") as f:
        json.dump(hanja_kor, f)


if __name__ == "__main__":
    main()

