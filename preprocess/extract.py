import re
import os


def extract_and_merge_to_txt(file_path, output_dir='./'):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 방송일시 추출
    date_match = re.search(r'방송일시\s*:\s*(\d{4})\.\s*(\d{1,2})\.\s*(\d{1,2})', content)
    if not date_match:
        print("방송일시를 찾을 수 없습니다.")
        return

    year, month, day = date_match.groups()
    formatted_date = f"{int(year):04d}.{int(month):02d}.{int(day):02d}"

    # <br> 개행 처리
    content = content.replace('<br>', '\n')

    # 대화 블록 추출
    dialogue_block_match = re.search(r'(-\(사회자\).*?여러분, 고맙습니다\.[^\n]*\n?)', content, re.DOTALL)
    if not dialogue_block_match:
        print("대화 블록을 찾을 수 없습니다.")
        return

    dialogue_block = dialogue_block_match.group(1)

    # 발화 추출
    pattern = r'(-\([^)]+\))\s*(.*?)(?=\n-\(|\Z)'
    matches = re.findall(pattern, dialogue_block, re.DOTALL)

    # 모든 발화를 순차적으로 이어붙임
    full_text = ""
    for speaker, text in matches:
        cleaned_text = text.strip()
        if cleaned_text:
            speaker = speaker.lstrip('-')  # '-' 제거
            full_text += f"{speaker} {cleaned_text} "

    full_text = full_text.strip()

    # TXT 파일로 저장
    output_path = os.path.join(output_dir, f"{formatted_date}.txt")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_text)

    print(f"[{formatted_date}] 기준으로 모든 발화를 병합한 텍스트 저장 완료: {output_path}")


if __name__ == "__main__":
    extract_and_merge_to_txt('../data/broadcast03_2020.php')

