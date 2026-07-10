import httpx
import json

base = 'http://localhost:8000/api/v1/intelligence'

print('=== stats ===')
r = httpx.get(base + '/stats/overview')
data = r.json()['data']
print(json.dumps(data, indent=2, ensure_ascii=False))

print('\n=== capabilities ===')
r = httpx.get(base + '/capabilities')
data = r.json()['data']
print('total:', data['total'])
for item in data['items']:
    print('  -', item['name'], '(', item['type'], ')', '-', item['status'])

print('\n=== events ===')
r = httpx.get(base + '/events')
data = r.json()['data']
print('total:', data['total'])
for item in data['items']:
    print('  -', item['title'][:50], '(score:', item['overall_score'], ')')

print('\n=== timeline ===')
r = httpx.get(base + '/events/timeline?days=30')
data = r.json()['data']
print('events in 30 days:', data['total'])

print('\n=== aiq/Q001 ===')
r = httpx.get(base + '/aiq/Q001')
data = r.json()['data']
print('status:', data['status'])
print('answer:', data['answer'])

