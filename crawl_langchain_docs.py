import os
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import defaultdict

BASE_URL = "https://docs.langchain.com/oss/python/"
DOMAIN = "https://docs.langchain.com"
OUTPUT_DIR = "output"

visited = set()
docs_by_category = defaultdict(list)
session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (compatible; LangchainCrawler/1.1; +https://docs.langchain.com)"
})

def get_html(url):
    """获取页面 HTML"""
    try:
        resp = session.get(url, timeout=10)
        if resp.status_code == 200:
            return resp.text
    except Exception as e:
        print(f"❌ 请求失败: {url} - {e}")
    return None

def extract_category_from_url(url: str):
    """根据路径提取分类名"""
    path = urlparse(url).path.replace("/oss/python/", "")
    parts = [p for p in path.split("/") if p]
    return parts[0] if len(parts) > 0 else "root"

def extract_links(html, base_url):
    """提取所有内部文档链接"""
    soup = BeautifulSoup(html, "html.parser")
    links = set()
    for a in soup.find_all("a", href=True):
        href = urljoin(base_url, a["href"])
        if href.startswith(BASE_URL) and href not in visited and not href.endswith("#"):
            links.add(href)
    return links

def extract_content(html):
    """提取文档标题与正文"""
    soup = BeautifulSoup(html, "html.parser")
    title = soup.find("title").get_text(strip=True) if soup.title else "Untitled"
    main = soup.find("main") or soup.find("article") or soup.body
    # 去除无关部分
    for tag in main.find_all(["nav", "header", "footer", "aside", "script", "style"]):
        tag.decompose()
    text = main.get_text("\n", strip=True)
    return title, text

def crawl(url):
    """递归爬取"""
    if url in visited:
        return
    visited.add(url)

    html = get_html(url)
    if not html:
        return

    category = extract_category_from_url(url)
    title, text = extract_content(html)
    docs_by_category[category].append((title, text))
    print(f"✅ 抓取成功 [{category}] {title}")

    # 提取下一层链接
    for link in extract_links(html, url):
        if len(visited) < 500:
            time.sleep(0.5)
            crawl(link)

def save_markdown_files():
    """为每个分类生成一个 markdown 文件"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for cat, docs in docs_by_category.items():
        filename = os.path.join(OUTPUT_DIR, f"{cat}.md")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"# {cat} (LangChain Python Docs)\n\n")
            for title, text in docs:
                f.write(f"## {title}\n\n{text}\n\n---\n\n")
        print(f"📄 已生成文件: {filename}")

if __name__ == "__main__":
    print("🚀 开始爬取 LangChain 文档 ...\n")
    crawl(BASE_URL)
    save_markdown_files()
    print("\n✅ 所有分类文档已生成完毕！")
