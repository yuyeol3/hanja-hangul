import json
import os
import han_check


def main():
    # 번역할 테스트 불러오기
    with open("text_to_translate.txt", "r", encoding="utf8") as f:
        text = f.read()

    hanja_list = get_hanja_sequence(text)

    with open("preferences.json", 'r', encoding="utf8") as f:
        preference_table = json.load(f)  # 선호하는 한자 음변환 테이블

    hanja_hangul_mathcing_table = convert_hanja_to_hangul(hanja_list)

    for hanja_str in hanja_hangul_mathcing_table:
        hanja_hangul_mathcing_table[hanja_str] = initial_law(hanja_hangul_mathcing_table[hanja_str])

    for hanja_str in hanja_hangul_mathcing_table:
        text = text.replace(hanja_str, hanja_hangul_mathcing_table[hanja_str])

    with open("result.txt", "w", encoding="utf8") as f:
        f.write(text+'\n')


    print(" Done!")  # 완료 표시


def get_hanja_sequence(text: str):
    text_end_idx = len(text) - 1
    hanja_list = []
    hanja_seqence = ''
    prev = ''

    for idx, char in enumerate(text):
        if ishanja(char):  # 문자가 한자라면 검사 수행
            hanja_seqence += char

        if ishanja(prev) and (ishanja(char) is False or idx == text_end_idx):
            hanja_list.append(hanja_seqence)
            hanja_seqence = ''

        prev = char


    return hanja_list


def convert_hanja_to_hangul(hanja_list):
    hanja_hangul_mathcing_table = dict()
    file_list = os.listdir("./hangul_hanja")

    with open("preferences.json", 'r', encoding="utf8") as f:
        preference_table = json.load(f)  # 선호하는 한자 음변환 테이블

    for idx, hanja_str in enumerate(hanja_list):
        converted = hanja_str

        # 진행률 표시해주는 코드
        percentage = ((idx + 1) / len(hanja_list)) * 100
        percentage = int(percentage)
        print("\r", end="")
        print(f"{percentage:3}% ", end="")
        for i in range(percentage): print("■", end="")

        for hanja in converted:
            # 선호 한자음이 지정되어 있으면
            if hanja in preference_table:
                converted = converted.replace(hanja, preference_table[hanja])

            # 아닌 경우
            else:
                for file_name in file_list:
                    with open(f"hangul_hanja/{file_name}", "r", encoding="utf8") as f:
                        hanjas = json.load(f)

                    if hanja in hanjas:
                        matching_hangul = file_name.split('.')[0]
                        converted = converted.replace(hanja, matching_hangul)
                        break

        if (2 <= len(converted) and len(converted) <= 4) and (hanja_str[0] == '金' or hanja_str[0] == '金'):
            converted = list(converted)
            converted[0] = "김"
            converted = list_to_str(converted)

        hanja_hangul_mathcing_table[hanja_str] = converted  # 변환된 최종 문자열을 한자 리스트에 바꿔넣음


    return hanja_hangul_mathcing_table


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


def initial_law(string: str):
    # 의존명사 등 문자열의 길이가 1보다 작거나 같으면 두음법칙 적용 X
    if len(string) <= 1:
        return string

    string = list(string)
    head_char = string[0]
    head_char_ord = ord(head_char)

    # ㄹ’을 첫소리로 가진 말이 단어의 첫머리에 올 때 ‘ㄹ’은 ‘ㄴ’으로 바꾸어 표기
    if ord('라') <= head_char_ord and head_char_ord <= ord('맇'):
        string[0] = chr(head_char_ord - 1764)
        head_char = string[0]
        head_char_ord = ord(head_char)
        
    # 구개음으로 발음되는 'ㄴ'이 반모음 'j'를 만나면 두음법칙 적용
    if ( ord('냐') <= head_char_ord and head_char_ord <= ord("냫") ) or \
        ( ord('녀') <= head_char_ord and head_char_ord <= ord("녛") ) or \
            ( ord('뇨') <= head_char_ord and head_char_ord <= ord("눃") ) or \
                ( ord('뉴') <= head_char_ord and head_char_ord <= ord("늏") ) or \
                    ( ord('니') <= head_char_ord and head_char_ord <= ord("닣") ):
                string[0] = chr(head_char_ord + 5292)

    return list_to_str(string)


def list_to_str(arr: list):
    result = ''

    for char in arr:
        result += char

    return result



if __name__ == "__main__":
    main()

