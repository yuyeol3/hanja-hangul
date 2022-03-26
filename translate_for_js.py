import json
import os
import han_check
import clipboard
# import sys
# sys.path.insert(1, './src/core_program/')  # path에 다음을 끼워넣기

def main():
    file_list = os.listdir("./hangul_hanja")

    with open("text_to_translate.txt", "r", encoding="utf8") as f:
        text = f.read()


    hanja_list = set()

    for char in text:
        if ishanja(char):  # 문자가 한자라면 검사 수행
            hanja_list.add(char)


    with open("preferences.json", 'r', encoding="utf8") as f:
        preference_table = json.load(f)  # 선호하는 한자 음변환 테이블


    for idx, hanja in enumerate(hanja_list):

        # 진행률 표시해주는 코드
        percentage = ((idx + 1) / len(hanja_list)) * 100
        percentage = int(percentage)
        print("\r", end="")
        print(f"{percentage:3}% ", end="")
        for i in range(percentage): print("■", end="")

        # 선호 한자음이 지정되어 있으면
        if hanja in preference_table:
            text = text.replace(hanja, preference_table[hanja])


        # 아닌 경우
        else:
            for file_name in file_list:
                with open(f"hangul_hanja/{file_name}", "r", encoding="utf8") as f:
                    hanjas = json.load(f)

                if hanja in hanjas:
                    matching_hangul = file_name.split('.')[0]

                    while hanja in text:
                        text = text.replace(hanja, matching_hangul)

                    break


    clipboard.copy(text)

    print(" Done!")  # 완료 표시


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

