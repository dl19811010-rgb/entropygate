import urllib.request
import json
import time
import random


def req(method, path, data=None, token=None):
    url = f'http://localhost:8000{path}'
    headers = {'Content-Type': 'application/json'}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    body = json.dumps(data).encode() if data else None
    req_obj = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        r = urllib.request.urlopen(req_obj)
        return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())


all_pass = True

ts = int(time.time())
rnd = random.randint(1000, 9999)


def test(name, status_code, code, expected_status=200, expected_code=200):
    global all_pass
    ok = (status_code == expected_status) and (code == expected_code)
    if not ok:
        all_pass = False
    status_text = "OK" if ok else "FAIL"
    print(f'  [{status_text}] {name}: HTTP={status_code} code={code}')


print('=== 集成测试 ===\n')

# 1. 登录
print('1. 管理员认证')
status, res = req('POST', '/api/v1/admin/auth/login', {'username': 'admin', 'password': 'admin123'})
test('登录成功', status, res.get('code'))
token = res.get('data', {}).get('access_token')

status, res = req('POST', '/api/v1/admin/auth/login', {'username': 'admin', 'password': 'wrong'})
test('登录失败-密码错误', status, res.get('code'), expected_code=400)

status, res = req('GET', '/api/v1/admin/auth/me', token=token)
test('获取当前用户', status, res.get('code'))

print()

# 2. 文章模块
print('2. 文章模块')
status, res = req('GET', '/api/v1/articles')
test('公开-文章列表', status, res.get('code'))

article_slug = f'int-test-art-{ts}-{rnd}'
status, res = req('POST', '/api/v1/articles', {
    'title': '集成测试文章', 'slug': article_slug,
    'content': '测试内容', 'status': 'published', 'type': 'news'
}, token=token)
test('管理-创建文章', status, res.get('code'))
article_id = res.get('data', {}).get('id') if res.get('code') == 200 else None

if article_id:
    status, res = req('GET', f'/api/v1/articles/{article_slug}')
    test('公开-文章详情', status, res.get('code'))
    status, res = req('PUT', f'/api/v1/articles/{article_id}', {'title': '更新测试'}, token=token)
    test('管理-更新文章', status, res.get('code'))
    status, res = req('DELETE', f'/api/v1/articles/{article_id}', token=token)
    test('管理-删除文章', status, res.get('code'))

status, res = req('POST', '/api/v1/articles', {
    'title': '无权限测试', 'slug': f'no-perm-{ts}-{rnd}',
    'content': '测试', 'status': 'published', 'type': 'news'
})
test('无token-创建文章(401)', status, res.get('code'), expected_code=401)

print()

# 3. 工具模块
print('3. 工具模块')
status, res = req('GET', '/api/v1/tools')
test('公开-工具列表', status, res.get('code'))

tool_slug = f'int-test-tool-{ts}-{rnd}'
status, res = req('POST', '/api/v1/tools', {
    'name': '集成测试工具', 'slug': tool_slug,
    'description': '测试', 'website_url': 'https://test.com',
    'availability_status': 'available'
}, token=token)
test('管理-创建工具', status, res.get('code'))
tool_id = res.get('data', {}).get('id') if res.get('code') == 200 else None

if tool_id:
    status, res = req('PUT', f'/api/v1/tools/{tool_id}', {'name': '更新工具'}, token=token)
    test('管理-更新工具', status, res.get('code'))
    status, res = req('DELETE', f'/api/v1/tools/{tool_id}', token=token)
    test('管理-删除工具', status, res.get('code'))

print()

# 4. 分类模块
print('4. 分类模块')
status, res = req('GET', '/api/v1/categories')
test('公开-分类列表', status, res.get('code'))

cat_slug = f'int-test-cat-{ts}-{rnd}'
status, res = req('POST', '/api/v1/categories', {
    'name': '测试分类', 'slug': cat_slug,
    'type': 'news', 'sort_order': 99
}, token=token)
test('管理-创建分类', status, res.get('code'))
cat_id = res.get('data', {}).get('id') if res.get('code') == 200 else None

if cat_id:
    status, res = req('PUT', f'/api/v1/categories/{cat_id}', {'name': '更新分类'}, token=token)
    test('管理-更新分类', status, res.get('code'))
    status, res = req('DELETE', f'/api/v1/categories/{cat_id}', token=token)
    test('管理-删除分类', status, res.get('code'))

print()

# 5. 标签模块
print('5. 标签模块')
status, res = req('GET', '/api/v1/tags')
test('公开-标签列表', status, res.get('code'))

tag_slug = f'int-test-tag-{ts}-{rnd}'
status, res = req('POST', '/api/v1/tags', {
    'name': '测试标签', 'slug': tag_slug,
    'type': 'feature', 'color': '#ff0000'
}, token=token)
test('管理-创建标签', status, res.get('code'))
tag_id = res.get('data', {}).get('id') if res.get('code') == 200 else None

if tag_id:
    status, res = req('PUT', f'/api/v1/tags/{tag_id}', {'name': '更新标签'}, token=token)
    test('管理-更新标签', status, res.get('code'))
    status, res = req('DELETE', f'/api/v1/tags/{tag_id}', token=token)
    test('管理-删除标签', status, res.get('code'))

print()

# 6. 仪表盘
print('6. 仪表盘')
status, res = req('GET', '/api/v1/dashboard/stats', token=token)
test('仪表盘统计', status, res.get('code'))

print()

# 7. 来源管理
print('7. 来源管理')
status, res = req('GET', '/api/v1/sources', token=token)
test('来源列表', status, res.get('code'))

status, res = req('POST', '/api/v1/sources', {
    'name': '测试来源', 'url': f'https://test-{ts}-{rnd}.com/rss',
    'type': 'rss', 'fetch_interval': 60, 'is_active': True
}, token=token)
test('创建来源', status, res.get('code'))
src_id = res.get('data', {}).get('id') if res.get('code') == 200 else None

if src_id:
    status, res = req('DELETE', f'/api/v1/sources/{src_id}', token=token)
    test('删除来源', status, res.get('code'))

print()

# 8. 审计日志
print('8. 审计日志')
status, res = req('GET', '/api/v1/audit-logs', token=token)
test('审计日志列表', status, res.get('code'))

print()

# 9. 管理员管理
print('9. 管理员与权限')
status, res = req('GET', '/api/v1/admin/admins', token=token)
test('管理员列表', status, res.get('code'))

status, res = req('GET', '/api/v1/admin/roles', token=token)
test('角色列表', status, res.get('code'))

status, res = req('GET', '/api/v1/admin/permissions', token=token)
test('权限列表', status, res.get('code'))

print()
print('=== 测试结果 ===')
if all_pass:
    print('全部通过!')
else:
    print('存在失败用例!')

