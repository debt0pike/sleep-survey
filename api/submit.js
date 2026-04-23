const APP_ID     = process.env.FEISHU_APP_ID     || 'cli_a95b87c9d1f8dbc2';
const APP_SECRET = process.env.FEISHU_APP_SECRET || 'ONch0li1lnHo8NfjMtdq9cxoVtNAXm1m';
const APP_TOKEN  = process.env.FEISHU_APP_TOKEN  || 'YArmbgA4caqIMMsAgtCcJZetnOS';
const TABLE_ID   = process.env.FEISHU_TABLE_ID   || 'tblv0OzbG1KV7hEr';

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') { res.status(200).end(); return; }
  if (req.method !== 'POST')   { res.status(405).end(); return; }

  try {
    // 获取飞书 token
    const tokenRes = await fetch(
      'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal',
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ app_id: APP_ID, app_secret: APP_SECRET })
      }
    );
    const { tenant_access_token: token } = await tokenRes.json();

    // 写入多维表格
    const { fields } = req.body;
    const recordRes = await fetch(
      `https://open.feishu.cn/open-apis/bitable/v1/apps/${APP_TOKEN}/tables/${TABLE_ID}/records`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ fields })
      }
    );
    const result = await recordRes.json();
    res.status(200).json(result);
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
}
