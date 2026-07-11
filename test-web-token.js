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
    console.log('1. Testing profile/tokens page with access_token...');
    const r2 = await makeRequest('cnb.cool', '/profile/tokens?access_token=' + TOKEN, {
        'Accept': 'text/html'
    });
    console.log('Status:', r2.status);
    
    const nextDataMatch = r2.body.match(/<script id="__NEXT_DATA__" type="application\/json">(.*?)<\/script>/);
    if (nextDataMatch) {
        try {
            const data = JSON.parse(nextDataMatch[1]);
            console.log('Found __NEXT_DATA__');
            console.log('Page:', data.page);
            console.log('Query:', JSON.stringify(data.query));
            const pageProps = data.props?.pageProps;
            if (pageProps) {
                console.log('PageProps keys:', Object.keys(pageProps));
                if (pageProps.profile?.tokens) {
                    console.log('Tokens data:', JSON.stringify(pageProps.profile.tokens).substring(0, 500));
                }
            }
        } catch (e) {
            console.log('Parse error:', e.message);
        }
    } else {
        console.log('No __NEXT_DATA__ found');
        console.log('Body snippet:', r2.body.substring(0, 300));
    }
}

main().catch(console.error);
