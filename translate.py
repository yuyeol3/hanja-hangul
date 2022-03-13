import json
import os
import han_check


def main():
    file_list = os.listdir("./hangul_hanja")
    # print(file_list)

    with open("text_to_translate.txt", "r", encoding="utf8") as f:
        text = f.read()

    hanja_list = set()

    for char in text:

        if ishanja(char):  # 문자가 한자라면 검사 수행
            hanja_list.add(char)

    for hanja in hanja_list:
        for file_name in file_list:
            with open(f"hangul_hanja/{file_name}", "r", encoding="utf8") as f:
                hanjas = json.load(f)

            if hanja in hanjas:
                matching_hangul = file_name.split('.')[0]

                while hanja in text:
                    text = text.replace(hanja, matching_hangul)

                break


    with open("result.txt", "w", encoding="utf8") as f:
        f.write(text+'\n')


def ishanja(char: str):
    upper_eng = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    lower_eng = "abcdefghijklmnopqrstuvwxyz"

    if char.isalpha():
        if char in upper_eng or char in lower_eng:
            return False
        elif han_check.isHangul(char):
            return False
        else:
            return True

    else:
        return False


if __name__ == "__main__":
    main()


