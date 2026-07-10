import json
import re
import time
import random
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

BASE_URL = 'https://news.aibase.com'
LIST_URL = f'{BASE_URL}/zh/news'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}


def fetch_page(url, params=None):
    resp = requests.get(url, headers=HEADERS, params=params, timeout=30)
    resp.raise_for_status()
    return resp.text


def clean_title(title):
    # 移除标题尾部的时间/阅读量信息，如 "44 分钟前37.6K"、"2 小时前12.4K"
    title = re.sub(r'\d+\s*(分钟前|小时前|天前|周前|月前|年前)\s*[\d.]+[KkMm]?$', '', title)
    # 移除列表页序号前缀，如 "#1标题内容"
    title = re.sub(r'^#\d+', '', title)
    title = re.sub(r'\s+', ' ', title).strip()
    return title


def parse_article_list(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = []
    # aibase 列表页每条新闻是一个 a 标签，封面图 img 的 alt 属性为干净标题
    selectors = [
        'article a[href]',
        '.news-item a[href]',
        '.news-list a[href]',
        '.item a[href]',
        'a[href*="/zh/news/"]',
    ]
    seen = set()
    for sel in selectors:
        for a in soup.select(sel):
            href = a.get('href', '')
            if not href or href in seen:
                continue
            full_url = urljoin(BASE_URL, href)
            # 只保留文章详情页
            if '/zh/news/' not in full_url or full_url.count('/') < 5:
                continue
            # 优先使用封面图 alt 作为标题
            img = a.find('img')
            title = clean_title(img.get('alt', '') if img else '')
            if not title:
                title = clean_title(a.get_text(strip=True))
            if not title or len(title) < 5:
                continue
            seen.add(href)
            items.append({
                'title': title,
                'url': full_url,
                'slug': urlparse(full_url).path.strip('/').split('/')[-1],
            })
    return items


def clean_summary(text, title=''):
    text = re.sub(r'\s+', ' ', text).strip()
    # 移除常见的站点/栏目前缀和标题重复（按长度降序，避免子串优先匹配）
    prefixes = sorted([
        'AI资讯', 'AI新闻资讯', '正文', '发布于AI新闻资讯', '发布时间',
        '阅读 :', '发布于', 'AI快讯', 'AIBase'
    ], key=len, reverse=True)
    # 循环清理前缀，直到没有变化
    changed = True
    while changed:
        original = text
        for prefix in prefixes:
            text = re.sub(rf'^\s*{re.escape(prefix)}\s*', '', text)
            text = re.sub(rf'\s*{re.escape(prefix)}\s*', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        changed = text != original
    # 去除标题在摘要开头的重复（含冒号分隔）
    if title:
        idx = text.find(title)
        if idx == 0:
            rest = text[len(title):]
            rest = re.sub(r'^\s*[:：]\s*', '', rest)
            text = rest
    # 去除发布时间和阅读信息，如 "2026年7月3号 17:59 1 分钟"
    text = re.sub(r'\d{4}年\d{1,2}月\d{1,2}号\s*\d{1,2}:\d{2}\s*\d+\s*分钟', '', text)
    # 去除独立的时间/阅读标签
    text = re.sub(r'发布时间\s*[:：]', '', text)
    text = re.sub(r'阅读\s*[:：]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    # 限制长度
    if len(text) > 220:
        text = text[:220] + '...'
    return text


def fetch_article_summary(url, title=''):
    """抓取文章详情页，提取正文前 200 字作为摘要。"""
    try:
        html = fetch_page(url)
        soup = BeautifulSoup(html, 'html.parser')
        # 移除脚本和样式
        for tag in soup(['script', 'style', 'nav', 'header', 'footer']):
            tag.decompose()
        # 尝试定位正文容器
        content = None
        for sel in ['article', '.content', '.article-content', '.post-content', 'main', '.main']:
            content = soup.select_one(sel)
            if content:
                break
        if not content:
            content = soup.body
        text = content.get_text(separator=' ', strip=True)
        text = re.sub(r'\s+', ' ', text)
        return clean_summary(text, title)
    except Exception as e:
        print(f'抓取详情失败 {url}: {e}')
        return ''


def classify_article(title, summary):
    """根据标题/摘要简单归类到 AI新动态 或 AI工具指南。"""
    text = (title + summary).lower()
    tool_keywords = ['教程', '指南', '使用', '怎么', '如何', '工具', '操作', '步骤', 'prompt', '提示词', '安装', '配置', '插件', '应用']
    if any(k in text for k in tool_keywords):
        return 'ai-tools'
    return 'ai-news'


def random_recent_time():
    """生成最近 7 天内的一个随机时间。"""
    days_ago = random.randint(0, 7)
    hours_ago = random.randint(0, 23)
    minutes_ago = random.randint(0, 59)
    dt = datetime.now() - timedelta(days=days_ago, hours=hours_ago, minutes=minutes_ago)
    return dt.strftime('%Y-%m-%dT%H:%M:%S')


def main():
    print('开始采集 aibase.com 文章列表...')
    all_links = []
    for page in range(1, 4):
        try:
            html = fetch_page(LIST_URL, params={'page': page} if page > 1 else None)
            links = parse_article_list(html)
            print(f'第 {page} 页找到 {len(links)} 篇文章')
            all_links.extend(links)
            time.sleep(1)
        except Exception as e:
            print(f'第 {page} 页失败: {e}')

    # 去重
    seen = set()
    unique_links = []
    for item in all_links:
        if item['url'] not in seen:
            seen.add(item['url'])
            unique_links.append(item)

    print(f'去重后共 {len(unique_links)} 篇文章，开始抓取摘要...')
    articles = []
    for idx, item in enumerate(unique_links[:60], start=1):
        summary = fetch_article_summary(item['url'], item['title'])
        category = classify_article(item['title'], summary)
        articles.append({
            'id': idx,
            'title': item['title'],
            'summary': summary,
            'category_slug': category,
            'source': {'name': 'AIBase'},
            'publish_time': random_recent_time(),
            'view_count': random.randint(1200, 45000),
            'url': item['url'],
            'slug': item['slug'],
        })
        if idx % 10 == 0:
            print(f'已处理 {idx}/{min(len(unique_links), 60)}')
        time.sleep(0.5)

    output = {
        'articles': articles,
        'categories': [
            {'id': 1, 'name': 'AI新动态', 'slug': 'ai-news'},
            {'id': 2, 'name': 'AI工具指南', 'slug': 'ai-tools'},
        ]
    }
    with open('E:/aitoto/ai-news-frontend/src/data/mockArticles.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f'已保存 {len(articles)} 篇文章到 src/data/mockArticles.json')


if __name__ == '__main__':
    main()
