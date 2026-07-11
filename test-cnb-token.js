const https = require('https');

const TOKEN = 'a8j40jkuNjK1d18Iufi0GdLNpiC';
const BASE_URL = 'api.cnb.cool';

function makeRequest(path, method = 'GET', body = null) {
    return new Promise((resolve, reject) => {
        const options = {
            hostname: BASE_URL,
            path: path,
            method: method,
            headers: {
                'Authorization': `Bearer ${TOKEN}`,
                'Accept': 'application/vnd.cnb.api+json',
                'Content-Type': 'application/json'
            }
        };

        const req = https.request(options, (res) => {
            let data = '';
            res.on('data', (chunk) => data += chunk);
            res.on('end', () => {
                try {
                    resolve({
                        status: res.statusCode,
                        headers: res.headers,
                        body: JSON.parse(data)
                    });
                } catch (e) {
                    resolve({
                        status: res.statusCode,
                        headers: res.headers,
                        body: data
                    });
                }
            });
        });

        req.on('error', (e) => reject(e));
        req.setTimeout(10000, () => {
            req.destroy(new Error('Request timeout'));
        });

        if (body) {
            req.write(JSON.stringify(body));
        }
        req.end();
    });
}

async function main() {
    console.log('=== 测试 CNB 令牌 ===\n');

    console.log('1. 测试获取仓库信息 (需要 repo-basic-info:r)...');
    try {
        const result = await makeRequest('/entropygate.cc.cd/totoss');
        console.log('   状态:', result.status);
        console.log('   响应:', JSON.stringify(result.body, null, 2).substring(0, 500));
    } catch (e) {
        console.log('   错误:', e.message);
    }

    console.log('\n2. 测试获取用户信息 (需要 account-profile:r)...');
    try {
        const result = await makeRequest('/user');
        console.log('   状态:', result.status);
        console.log('   响应:', JSON.stringify(result.body, null, 2).substring(0, 500));
    } catch (e) {
        console.log('   错误:', e.message);
    }

    console.log('\n3. 测试获取仓库文件内容 (需要 repo-code:r)...');
    try {
        const result = await makeRequest('/entropygate.cc.cd/totoss/-/git/contents/README.md');
        console.log('   状态:', result.status);
        console.log('   响应:', JSON.stringify(result.body, null, 2).substring(0, 500));
    } catch (e) {
        console.log('   错误:', e.message);
    }

    console.log('\n4. 测试获取用户仓库列表 (需要 account-engage:r)...');
    try {
        const result = await makeRequest('/user/repos?page=1&page_size=5');
        console.log('   状态:', result.status);
        console.log('   响应:', JSON.stringify(result.body, null, 2).substring(0, 500));
    } catch (e) {
        console.log('   错误:', e.message);
    }
}

main().catch(console.error);
