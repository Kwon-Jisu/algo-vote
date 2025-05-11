import re
from datetime import datetime


def rule_based_response(query: str) -> str | None:
    # 현재 시간
    if re.search(r"(현재|지금).*(시간|시각)", query):
        return f"[RuleAgent] 현재 시각은 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}입니다."

    # 뉴스 출처
    if "뉴스 출처" in query or "어디서 수집" in query:
        return "[RuleAgent] 뉴스는 BBC, 연합뉴스, Google News 등 다양한 공개 API 및 RSS 피드에서 수집합니다."

    # 정치 관련 필터
    if "정치 뉴스만" in query:
        return "[RuleAgent] 정치 카테고리 필터를 적용했습니다. 질문을 다시 입력해주세요."

    # 챗봇 기능 안내
    if "무슨 기능" in query or "뭐 할 수 있어" in query:
        return "[RuleAgent] 이 챗봇은 실시간 뉴스 검색, 요약, 질의응답 기능을 제공합니다."

    return None
