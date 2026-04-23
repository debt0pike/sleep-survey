#!/usr/bin/env python3
"""
睡眠调查 v9 — 飞书多维表格字段初始化脚本
对应新表: 睡眠调查_v9  TABLE_ID=tblv0OzbG1KV7hEr
"""
import json, urllib.request

APP_ID     = 'cli_a95b87c9d1f8dbc2'
APP_SECRET = 'ONch0li1lnHo8NfjMtdq9cxoVtNAXm1m'
APP_TOKEN  = 'YArmbgA4caqIMMsAgtCcJZetnOS'
TABLE_ID   = 'tblv0OzbG1KV7hEr'   # ← 新表

# ── 颜色常量 ──────────────────────────────────────────
C = {
    'green':0, 'teal':1, 'blue':2, 'indigo':3, 'purple':4,
    'pink':5,  'red':6,  'orange':7, 'yellow':8, 'lime':9, 'sage':10,
}

def opt(name, color=0):
    return {'name': name, 'color': color}

# ── 字段定义 (按问卷页面顺序) ────────────────────────
#   每项: (field_name, type, property_dict_or_None)
#   type: 1=文本 2=数字 3=单选 4=多选 1001=创建时间

FIELDS = [
    # ── 基础信息 ──────────────────────────────────────
    ('年龄', 2, {'formatter': '0'}),
    ('性别', 3, {'options': [
        opt('男', C['blue']), opt('女', C['pink']), opt('其他', C['purple'])
    ]}),
    ('身高cm', 2, {'formatter': '0.0'}),
    ('体重kg', 2, {'formatter': '0.0'}),
    ('睡眠问题持续时间', 3, {'options': [
        opt('<1个月', C['lime']),
        opt('1-3个月', C['yellow']),
        opt('3-12个月', C['orange']),
        opt('>1年', C['red']),
    ]}),

    # ── P1: 主要问题 & 改善目标 ───────────────────────
    ('最困扰的问题', 4, {'options': [
        opt('入睡困难',    C['red']),
        opt('夜里容易醒',  C['orange']),
        opt('凌晨 / 清晨容易醒', C['yellow']),
        opt('睡得浅 / 多梦',     C['lime']),
        opt('睡了也不恢复',      C['teal']),
        opt('白天状态差',        C['blue']),
        opt('睡眠忽好忽坏',      C['indigo']),
        opt('一调整、吃补剂或改变作息就更乱', C['purple']),
    ]}),
    ('最困扰的问题_主', 3, {'options': [
        opt('入睡困难',    C['red']),
        opt('夜里容易醒',  C['orange']),
        opt('凌晨 / 清晨容易醒', C['yellow']),
        opt('睡得浅 / 多梦',     C['lime']),
        opt('睡了也不恢复',      C['teal']),
        opt('白天状态差',        C['blue']),
        opt('睡眠忽好忽坏',      C['indigo']),
        opt('一调整、吃补剂或改变作息就更乱', C['purple']),
    ]}),
    ('最想先改善', 4, {'options': [
        opt('更快睡着',      C['green']),
        opt('夜里少醒',      C['teal']),
        opt('醒后更容易再睡',C['blue']),
        opt('不要太早醒',    C['indigo']),
        opt('醒来更清爽',    C['lime']),
        opt('白天更有精神',  C['yellow']),
        opt('减少药物补剂依赖', C['orange']),
        opt('先稳定一点，不要越调越乱', C['purple']),
    ]}),
    ('最想先改善_主', 3, {'options': [
        opt('更快睡着',      C['green']),
        opt('夜里少醒',      C['teal']),
        opt('醒后更容易再睡',C['blue']),
        opt('不要太早醒',    C['indigo']),
        opt('醒来更清爽',    C['lime']),
        opt('白天更有精神',  C['yellow']),
        opt('减少药物补剂依赖', C['orange']),
        opt('先稳定一点，不要越调越乱', C['purple']),
    ]}),

    # ── P2: 作息 & 睡眠评分 ──────────────────────────
    ('作息情况', 1, None),                          # JSON: 上床/睡着/起床时间、时长、稳定度
    ('睡眠1_入睡超30分钟',       2, {'formatter':'0'}),
    ('睡眠2_夜醒2次以上',        2, {'formatter':'0'}),
    ('睡眠3_醒后难再睡',         2, {'formatter':'0'}),
    ('睡眠4_比预期早醒1小时',    2, {'formatter':'0'}),
    ('睡眠5_睡浅易受干扰',       2, {'formatter':'0'}),
    ('睡眠6_梦多梦清晰',         2, {'formatter':'0'}),
    ('睡眠7_睡够不解乏',         2, {'formatter':'0'}),
    ('睡眠8_白天困低迷启动慢',   2, {'formatter':'0'}),
    ('睡眠9_白天低迷晚上清醒',   2, {'formatter':'0'}),
    ('睡眠10_睡眠忽好忽坏',      2, {'formatter':'0'}),

    # ── P3: 睡眠模式类型 ─────────────────────────────
    ('睡前入睡时更像', 4, {'options': [
        opt('脑子停不下来', C['red']),
        opt('身体放不松',   C['orange']),
        opt('对环境敏感',   C['yellow']),
        opt('晚上反而精神', C['indigo']),
        opt('越累越睡不着', C['purple']),
    ]}),
    ('睡前入睡时更像_主', 3, {'options': [
        opt('脑子停不下来', C['red']),
        opt('身体放不松',   C['orange']),
        opt('对环境敏感',   C['yellow']),
        opt('晚上反而精神', C['indigo']),
        opt('越累越睡不着', C['purple']),
    ]}),
    ('夜间醒来时更像', 4, {'options': [
        opt('夜里自然醒',                    C['teal']),
        opt('夜里被身体叫醒（热 / 尿 / 不适）', C['orange']),
        opt('多梦 / 工作梦 / 情绪梦',         C['indigo']),
        opt('早醒后脑子秒上线',               C['red']),
    ]}),
    ('夜间醒来时更像_主', 3, {'options': [
        opt('夜里自然醒',                    C['teal']),
        opt('夜里被身体叫醒（热 / 尿 / 不适）', C['orange']),
        opt('多梦 / 工作梦 / 情绪梦',         C['indigo']),
        opt('早醒后脑子秒上线',               C['red']),
    ]}),
    ('醒后调整后更像', 4, {'options': [
        opt('睡了但像没修好', C['blue']),
        opt('一调整就乱',     C['red']),
    ]}),
    ('醒后调整后更像_主', 3, {'options': [
        opt('睡了但像没修好', C['blue']),
        opt('一调整就乱',     C['red']),
    ]}),

    # ── P4: 影响因素评分 (0/1/2) ─────────────────────
    ('影响1_睡前刷手机短视频',     2, {'formatter':'0'}),
    ('影响2_睡前工作处理消息',     2, {'formatter':'0'}),
    ('影响3_压力责任待命感',       2, {'formatter':'0'}),
    ('影响4_咖啡浓茶能量饮料',     2, {'formatter':'0'}),
    ('影响5_酒精夜宵晚餐太重',     2, {'formatter':'0'}),
    ('影响6_晚间运动',             2, {'formatter':'0'}),
    ('影响7_补剂助眠药叠加',       2, {'formatter':'0'}),
    ('影响8_空腹低碳控糖后夜醒',   2, {'formatter':'0'}),
    ('影响9_噪音光线温度湿度',     2, {'formatter':'0'}),
    ('影响10_出差换环境作息漂移',  2, {'formatter':'0'}),
    ('生活习惯', 1, None),          # JSON: 咖啡因/酒精/运动/晚餐详情

    # ── P5: 身体信号 ─────────────────────────────────
    ('身体信号', 4, {'options': [
        opt('心跳明显 / 心慌',        C['red']),
        opt('呼吸浅 / 胸口紧',        C['orange']),
        opt('热醒 / 出汗 / 发热',     C['yellow']),
        opt('冷醒 / 手脚冷',          C['teal']),
        opt('口干 / 鼻干 / 喉咙干',   C['blue']),
        opt('鼻塞 / 打鼾 / 张口呼吸', C['indigo']),
        opt('反酸 / 胃不舒服 / 胀气', C['purple']),
        opt('饥饿 / 空腹感',          C['pink']),
        opt('夜尿明显',               C['lime']),
        opt('麻 / 抽腿不宁 / 身体疼痛', C['sage']),
        opt('晨起头沉 / 身体困重',    C['green']),
        opt('活动后更精神',           C['teal']),
        opt('活动后更累 / 恢复慢',    C['red']),
    ]}),
    ('身体信号_主', 3, {'options': [
        opt('心跳明显 / 心慌',        C['red']),
        opt('呼吸浅 / 胸口紧',        C['orange']),
        opt('热醒 / 出汗 / 发热',     C['yellow']),
        opt('冷醒 / 手脚冷',          C['teal']),
        opt('口干 / 鼻干 / 喉咙干',   C['blue']),
        opt('鼻塞 / 打鼾 / 张口呼吸', C['indigo']),
        opt('反酸 / 胃不舒服 / 胀气', C['purple']),
        opt('饥饿 / 空腹感',          C['pink']),
        opt('夜尿明显',               C['lime']),
        opt('麻 / 抽腿不宁 / 身体疼痛', C['sage']),
        opt('晨起头沉 / 身体困重',    C['green']),
        opt('活动后更精神',           C['teal']),
        opt('活动后更累 / 恢复慢',    C['red']),
    ]}),

    # ── P6: 睡眠监测 ─────────────────────────────────
    ('监测结果', 4, {'options': [
        opt('深睡少',              C['blue']),
        opt('浅睡多',              C['teal']),
        opt('REM / 做梦时间多',    C['indigo']),
        opt('REM 少或后半夜睡眠被切断', C['purple']),
        opt('夜醒 / 清醒次数多',   C['orange']),
        opt('总时长够但醒来不恢复', C['red']),
        opt('作息和睡眠结构波动很大', C['yellow']),
        opt('数据看起来还行但体感很差', C['lime']),
        opt('不确定怎么看',        C['sage']),
    ]}),
    ('监测数据', 1, None),          # JSON: 总睡眠/深睡/REM/清醒次数

    # ── P7: 方法 & 用药 ───────────────────────────────
    ('方法1_早睡调整作息',    1, None),
    ('方法2_减少手机降光',    1, None),
    ('方法3_泡脚热水澡',      1, None),
    ('方法4_呼吸冥想身体扫描',1, None),
    ('方法5_运动',            1, None),
    ('方法6_调整饮食控糖',    1, None),
    ('方法7_助眠补剂保健品',  1, None),
    ('方法8_助眠药安眠药',    1, None),
    ('确定有帮助的方法', 1, None),
    ('确定不适合的方法', 1, None),
    ('助眠药使用', 3, {'options': [
        opt('没有',              C['green']),
        opt('偶尔',              C['lime']),
        opt('经常',              C['orange']),
        opt('已连续使用≥3个月',  C['red']),
        opt('医生指导下使用',    C['blue']),
    ]}),
    ('药物使用问题', 4, {'options': [
        opt('剂量越来越不够',      C['red']),
        opt('停药或减量后明显更差',C['orange']),
        opt('换药后更乱',          C['yellow']),
        opt('晚上配合酒精 / 保健品', C['purple']),
        opt('无上述情况',          C['green']),
    ]}),

    # ── P8: 风险信号 ─────────────────────────────────
    ('风险信号', 4, {'options': [
        opt('严重打鼾',                      C['red']),
        opt('睡觉中憋醒 / 疑似呼吸暂停',     C['red']),
        opt('夜间心悸明显',                  C['orange']),
        opt('反酸 / 胃食管反流明显影响睡眠', C['orange']),
        opt('腿不宁明显',                    C['yellow']),
        opt('情绪低落或焦虑紧张已明显影响生活', C['purple']),
        opt('白天功能明显受影响',            C['blue']),
        opt('近期体重波动明显',              C['teal']),
    ]}),

    # ── P9: 综合总结 ─────────────────────────────────
    ('最影响睡眠的因素', 1, None),   # 文本: 最多3项，用 / 分隔
    ('方案偏向', 4, {'options': [
        opt('先快速稳定',          C['green']),
        opt('先找清楚原因',        C['blue']),
        opt('先减少调整后不舒服的情况', C['teal']),
        opt('先改善白天状态',      C['lime']),
        opt('先减少药物 / 补剂依赖', C['orange']),
    ]}),
    ('其他补充', 1, None),
]


# ── 工具函数 ─────────────────────────────────────────
def feishu_post(url, data, headers=None):
    h = {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
    if headers:
        h.update(headers)
    req = urllib.request.Request(url, json.dumps(data).encode(), h)
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())

def get_token():
    r = feishu_post(
        'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal',
        {'app_id': APP_ID, 'app_secret': APP_SECRET})
    return r.get('tenant_access_token', '')

def create_field(token, name, ftype, property_dict):
    data = {'field_name': name, 'type': ftype}
    if property_dict:
        data['property'] = property_dict
    return feishu_post(
        f'https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/fields',
        data, {'Authorization': f'Bearer {token}'})

if __name__ == '__main__':
    token = get_token()
    print(f'Token 获取成功\n开始创建字段 ({len(FIELDS)} 个)...\n')
    ok, fail = 0, 0
    for name, ftype, prop in FIELDS:
        r = create_field(token, name, ftype, prop)
        code = r.get('code', -1)
        if code == 0:
            fid = r.get('data', {}).get('field', {}).get('field_id', '')
            type_label = {1:'文本', 2:'数字', 3:'单选', 4:'多选'}.get(ftype, str(ftype))
            print(f'  ✓ [{type_label}] {name}  ({fid})')
            ok += 1
        else:
            print(f'  ✗ {name}  → code={code} {r.get("msg","")}')
            fail += 1
    print(f'\n完成: {ok} 成功, {fail} 失败')
    print(f'\n下一步: 更新 server.py 中的 TABLE_ID = "{TABLE_ID}"')
