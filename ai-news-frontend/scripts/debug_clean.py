import json

with open('E:/aitoto/ai-news-frontend/src/data/mockArticles.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

article = data['articles'][0]
title = article['title']
summary = article['summary']

print('TITLE:', repr(title))
print('SUMMARY START:', repr(summary[:len(title)+5]))
print('FIND:', summary.find(title))
print('EQ:', summary.startswith(title))
print('TITLE LEN:', len(title))
print('SUMMARY START LEN:', len(summary[:len(title)]))
for i, (a, b) in enumerate(zip(title, summary)):
    if a != b:
        print(f'diff at {i}: title={repr(a)} summary={repr(b)}')
        break
else:
    if len(summary) >= len(title):
        print('first len(title) chars are equal')
    else:
        print('summary shorter than title')
