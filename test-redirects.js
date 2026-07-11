const https = require('https');

const TOKEN = 'a8j40jkuNjK1d18Iufi0GdLNpiC';

function makeRequest(hostname, path, headers, method = 'GET', followRedirects = true) {
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
                if (followRedirects && (res.statusCode === 301 || res.statusCode === 302 || res.statusCode === 307 || res.statusCode === 308)) {
                    const location = res.headers.location;
                    console.log(`  Redirect ${res.statusCode} -> ${location}`);
                    if (location) {
                        const url = new URL(location, 'https://' + hostname);
                        makeRequest(url.hostname, url.pathname + url.search, headers, method, false).then(resolve).catch(reject);
                        return;
                    }
                }
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
    console.log('Final status:', r.status);
    
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
    await testPage('/profile/token');
    await testPage('/user/settings/tokens');
}

main().catch(console.error);
