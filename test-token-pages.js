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

async function testPage(path) {
    console.log(`Testing: ${path}`);
    const r = await makeRequest('cnb.cool', path + '?access_token=' + TOKEN, {
        'Accept': 'text/html'
    });
    console.log('Status:', r.status);
    
    const titleMatch = r.body.match(/<title[^>]*>(.*?)<\/title>/i);
    if (titleMatch) {
        console.log('Title:', titleMatch[1]);
    }
    
    const nextDataMatch = r.body.match(/<script id="__NEXT_DATA__" type="application\/json">(.*?)<\/script>/);
    if (nextDataMatch) {
        try {
            const data = JSON.parse(nextDataMatch[1]);
            console.log('Next.js page:', data.page);
            console.log('Query:', JSON.stringify(data.query));
        } catch (e) {
            console.log('Parse error:', e.message);
        }
    }
    console.log();
}

async function main() {
    await testPage('/profile/tokens');
    await testPage('/profile/token');
    await testPage('/profile/settings/tokens');
    await testPage('/user/settings/tokens');
    await testPage('/settings/tokens');
}

main().catch(console.error);
