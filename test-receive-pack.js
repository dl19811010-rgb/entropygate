const https = require('https');

const TOKEN = 'a8j40jkuNjK1d18Iufi0GdLNpiC';

function makeRequest(hostname, path, headers, method = 'GET') {
    return new Promise((resolve, reject) => {
        const options = {
            hostname: hostname,
            path: path,
            method: method,
            headers: headers
        };

        const req = https.request(options, (res) => {
            let data = '';
            res.on('data', (chunk) => data += chunk);
            res.on('end', () => {
                resolve({ status: res.statusCode, headers: res.headers, body: data });
            });
        });

        req.on('error', (e) => reject(e));
        req.end();
    });
}

async function main() {
    const auth = 'Basic ' + Buffer.from('totoss:' + TOKEN).toString('base64');
    const headers = {
        'Authorization': auth,
        'User-Agent': 'git/2.0',
        'Accept': '*/*'
    };
    
    // 测试 git-receive-pack (用于 push)
    console.log('=== 测试 git-receive-pack (写入权限) ===');
    const receivePackPath = '/entropygate.cc.cd/totoss.git/info/refs?service=git-receive-pack';
    
    try {
        const r = await makeRequest('cnb.cool', receivePackPath, headers);
        console.log('Status:', r.status);
        console.log('Body:', r.body.substring(0, 200).replace(/\n/g, ' '));
    } catch (e) {
        console.log('Error:', e.message);
    }
    
    console.log();
    
    // 不带认证测试 receive-pack
    console.log('=== 不带认证测试 git-receive-pack ===');
    const headersNoAuth = {
        'User-Agent': 'git/2.0',
        'Accept': '*/*'
    };
    try {
        const r = await makeRequest('cnb.cool', receivePackPath, headersNoAuth);
        console.log('Status:', r.status);
        console.log('Body:', r.body.substring(0, 200).replace(/\n/g, ' '));
    } catch (e) {
        console.log('Error:', e.message);
    }
}

main().catch(console.error);
