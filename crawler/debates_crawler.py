# crawler/news_crawler.py
import requests
from bs4 import BeautifulSoup
import urllib.parse


def search_news(query: str) -> list:
    """키워드로 중앙선거방송토론위원회 웹사이트의 뉴스를 검색합니다."""
    base_url = "https://debates.go.kr/2016_broadcast/broadcast03_2020.php?ctg=2"
    search_url = f"{base_url}?search={urllib.parse.quote(query)}"
    
    try:
        response = requests.get(search_url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        news_items = []
        
        # 뉴스 항목 찾기 - 공지사항과 보도자료 모두 검색
        news_links = soup.select('table a[href*="news"]')
        
        for link in news_links:
            title = link.get_text(strip=True)
            href = link.get('href')
            if href and title:
                full_url = urllib.parse.urljoin(base_url, href)
                news_items.append(f"{title}: {full_url}")
        
        return news_items if news_items else ["검색 결과가 없습니다."]
        
    except requests.RequestException as e:
        return [f"뉴스 검색 중 오류 발생: {str(e)}"]
