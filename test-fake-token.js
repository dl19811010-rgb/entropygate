const https = require('https');

const FAKE_TOKEN = 'abcdefghijklmnopqrstuvwxyz1234567890';
const REAL_TOKEN = 'a8j40jkuNjK1d18Iufi0GdLNpiC';

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
    const path = '/entropygate.cc.cd/totoss.git/info/refs?service=git-upload-pack';
    
    const testTokens = [
        { name: 'Real token', token: REAL_TOKEN },
        { name: 'Fake token', token: FAKE_TOKEN },
        { name: 'Short token', token: 'short' },
    ];
    
    for (const test of testTokens) {
        const auth = 'Basic ' + Buffer.from('totoss:' + test.token).toString('base64');
        const headers = {
            'Authorization': auth,
            'User-Agent': 'git/2.0',
            'Accept': '*/*'
        };
        try {
            const r = await makeRequest('cnb.cool', path, headers);
            const tokenMatch = r.body.match(/token: (.+)/);
            const tokenDisplay = tokenMatch ? tokenMatch[1] : 'none';
            console.log(test.name + ': ' + r.status + ' | token in response: ' + tokenDisplay);
        } catch (e) {
            console.log(test.name + ': Error - ' + e.message);
        }
    }
}

main().catch(console.error);
