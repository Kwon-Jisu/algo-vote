import re


def extract_dialogue_from_php(file_path, output_dir='./'):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 방송일시 추출: '방송일시 : 2025. 5. 2.'
    date_match = re.search(r'방송일시\s*:\s*(\d{4})\.\s*(\d{1,2})\.\s*(\d{1,2})', content)

    if not date_match:
        print("방송일시를 찾을 수 없습니다.")
        return

    year, month, day = date_match.groups()
    formatted_date = f"{int(year):04d}.{int(month):02d}.{int(day):02d}"
    output_txt_path = f"{output_dir}{formatted_date}.txt"

    # <br>를 개행으로 변환
    content = content.replace('<br>', '\n')

    # -(사회자) ~ 여러분, 고맙습니다. 구간 추출
    dialogue_block_match = re.search(r'(-\(사회자\).*?여러분, 고맙습니다\.[^\n]*\n?)', content, re.DOTALL)

    if not dialogue_block_match:
        print("대화 블록을 찾을 수 없습니다.")
        return

    dialogue_block = dialogue_block_match.group(1)

    # -(화자) 발화내용 추출
    pattern = r'-\((.*?)\)\s*(.*?)(?=\n-\(|\Z)'
    matches = re.findall(pattern, dialogue_block, re.DOTALL)

    with open(output_txt_path, 'w', encoding='utf-8') as f:
        for speaker, text in matches:
            cleaned_text = text.strip()
            if cleaned_text:
                f.write(f"({speaker.strip()}) {cleaned_text}\n")

    print(f"[{len(matches)}개의 발화를 .txt 파일로 저장했습니다: {output_txt_path}")


if __name__ == "__main__":
    extract_dialogue_from_php('../data/broadcast03_2020.php')

