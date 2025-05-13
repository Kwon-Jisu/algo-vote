import re
from bs4 import BeautifulSoup
import os

def extract_dialogue_from_php(file_path, output_dir='./'):
    with open(file_path, 'r', encoding='utf-8') as f:
        raw_content = f.read()

    # BeautifulSoup으로 HTML 파싱
    soup = BeautifulSoup(raw_content, "html.parser")

    # 방송 제목 추출
    title_div = soup.find("div", class_="movie_Tit")
    if not title_div:
        print("방송 제목을 찾을 수 없습니다.")
        return

    broadcast_title = title_div.get_text(strip=True)

    # 파일명으로 사용하기 위해 특수문자 제거 및 공백 -> _
    safe_title = re.sub(r'[\\/:*?"<>|]', '', broadcast_title)
    safe_title = safe_title.replace(' ', '_')
    output_txt_path = os.path.join(output_dir, f"{safe_title}.txt")

    # <br> 태그를 개행 문자로 변환
    for br in soup.find_all("br"):
        br.replace_with("\n")

    # 전체 텍스트 추출
    content = soup.get_text()

    # 대화 블록 추출
    dialogue_block_match = re.search(
        r'(-\(사회자\).*?여러분, 고맙습니다\.[^\n]*\n?)',
        content,
        re.DOTALL
    )

    if not dialogue_block_match:
        print("대화 블록을 찾을 수 없습니다.")
        return

    dialogue_block = dialogue_block_match.group(1)

    # -(화자) 발화내용 추출
    pattern = r'-\((.*?)\)\s*(.*?)(?=\n-\(|\Z)'
    matches = re.findall(pattern, dialogue_block, re.DOTALL)

    saved_count = 0  # 저장된 발화 수 카운트

    with open(output_txt_path, 'w', encoding='utf-8') as f:
        for speaker, text in matches:
            cleaned_text = text.strip()
            if len(cleaned_text) > 26:
                f.write(f"({speaker.strip()}) {cleaned_text}\n")
                saved_count += 1

    print(f"[{saved_count}개의 발화를 .txt 파일로 저장했습니다: {output_txt_path}]")

if __name__ == "__main__":
    extract_dialogue_from_php('../data/broadcast03_2020.php')


