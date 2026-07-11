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
    const headersWithAuth = {
        'Authorization': auth,
        'User-Agent': 'git/2.0',
        'Accept': '*/*'
    };
    const headersWithoutAuth = {
        'User-Agent': 'git/2.0',
        'Accept': '*/*'
    };
    
    const fakeRepo = '/nonexistent-user/nonexistent-repo.git/info/refs?service=git-upload-pack';
    
    console.log('=== 不存在的仓库 ===');
    const r1 = await makeRequest('cnb.cool', fakeRepo, headersWithoutAuth);
    console.log('Without auth:', r1.status);
    console.log('Body:', r1.body.substring(0, 150).replace(/\n/g, ' '));
    
    const r2 = await makeRequest('cnb.cool', fakeRepo, headersWithAuth);
    console.log('With auth:', r2.status);
    console.log('Body:', r2.body.substring(0, 150).replace(/\n/g, ' '));
}

main().catch(console.error);
