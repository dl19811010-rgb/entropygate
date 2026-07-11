const CnbApiClient = require('@cnbcool/mcp-server/dist/api/client').default;

const client = new CnbApiClient({
    baseUrl: 'https://api.cnb.cool',
    token: 'a8j40jkuNjK1d18Iufi0GdLNpiC'
});

async function main() {
    console.log('Testing CNB MCP Server API client...');
    console.log('Base URL:', client.baseUrl);
    
    try {
        const result = await client.request('GET', '/entropygate.cc.cd/totoss');
        console.log('Success:', JSON.stringify(result, null, 2).substring(0, 500));
    } catch (e) {
        console.log('Error:', e.message);
    }
}

main().catch(console.error);
