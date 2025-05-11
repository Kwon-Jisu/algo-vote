# tools/rule_tool.py
from langchain.tools import tool
from datetime import datetime

# tool은 LangChain에서 제공하는 데코레이터로,
# 함수에 메타데이터를 추가하여 에이전트가 사용할 수 있는 도구로 등록할 수 있게 합니다.
@tool
def get_time(_: str) -> str:
    """현재 시간을 반환합니다."""
    return datetime.now().strftime("현재 시간은 %Y-%m-%d %H:%M:%S 입니다.")

@tool
def get_news_source(_: str) -> str:
    """뉴스의 출처를 알려줍니다."""
    return "뉴스는 BBC, 연합뉴스, Google News 등에서 수집됩니다."
