#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新AI小栈网站内容
"""

import random
from datetime import datetime

# ========== 内容库 ==========
CONTENT_DB = {
    "tech": [
        ("DeepSeek V4: 100万Token窗口+多模态突破", "https://k.sina.com.cn", "原生支持图文视频"),
        ("通义千问 QWQ-32B 开源", "https://qwenlm.github.io", "推理能力大幅提升"),
        ("智谱 GLM-4 Plus 发布", "https://www.zhipuai.cn", "中文理解能力最强"),
        ("百度文心4.0 Turbo", "https://yiyan.baidu.com", "响应速度提升50%"),
        ("字节豆包日均调用量破万亿", "https://www.volcengine.com", "火山引擎发布豆包最新版本"),
        ("讯飞星火4.0发布", "https://xinghuo.xfyun.cn", "多语种能力全面提升"),
        ("阶跃星辰Step-2万亿参数MoE", "https://stepfun.com", "性能直逼GPT-4"),
        ("Kimi发布200万字上下文", "https://kimi.moonshot.cn", "支持整本书阅读"),
        ("Mistral Large 2开源", "https://mistral.ai", "支持中文性能比肩GPT-4"),
        ("MiniMax海螺AI对话模型", "https://hailuoai.video", "专注长文本理解"),
    ],
    "app": [
        ("AI医疗: 协和医院日均AI辅助诊断超万例", "https://www.36kr.com", "准确率达97%"),
        ("AI教育: 个性化学习路径效率提升3倍", "https://www.36kr.com", "自适应学习系统"),
        ("AI制造: 工厂质检效率提升80%", "https://finance.sina.com.cn", "AI视觉检测"),
        ("AI金融: 智能投顾管理资产破万亿", "https://tech.sina.com.cn", "年化收益超基准20%"),
        ("AI办公: Copilot月活企业超10万家", "https://www.microsoft.com", "效率提升50%"),
        ("AI客服: 电商平台AI接待率超90%", "https://www.aliyun.com", "7x24服务"),
        ("AI创作: MCN AI生成内容占比超60%", "https://www.36kr.com", "效率提升5倍"),
        ("AI编程: GitHub Copilot代码生成超40%", "https://github.blog", "150万开发者使用"),
        ("AI法律: 合同审查效率提升10倍", "https://www.36kr.com", "秒级风险识别"),
        ("AI设计: Logo生成工具日活破百万", "https://www.36kr.com", "3秒10种方案"),
    ],
    "company": [
        ("OpenAI年化营收突破40亿美元", "https://tech.sina.com.cn", "AI商业化加速"),
        ("英伟达Blackwell GPU供不应求", "https://finance.sina.com.cn", "AI芯片需求爆发"),
        ("微软Copilot全线接入Windows", "https://www.microsoft.com", "覆盖10亿用户"),
        ("谷歌 Gemini 1.5 Pro全面开放API", "https://blog.google", "百万Token上下文"),
        ("百度文心一言企业用户超1000万", "https://k.sina.com.cn", "国产大模型领先"),
        ("字节豆包日活突破5000万", "https://www.bytedance.com", "国内AI增速第一"),
        ("阿里云AI收入同比增长超100%", "https://www.alibabagroup.com", "AI驱动增长"),
        ("华为盘古大模型5.0全场景升级", "https://www.huawei.com", "赋能千行百业"),
        ("腾讯混元大模型接入企业微信", "https://www.tencent.com", "社交+AI战略"),
        ("商汤日日新5.0 CV领域再突破", "https://www.sensetime.com", "计算机视觉+大模型"),
    ],
    "business": [
        ("AI SaaS订阅模式: 年ARR增长200%", "https://www.36kr.com", "续费率超90%"),
        ("AI API调用收费: 按量计费成主流", "https://openai.com", "毛利率超70%"),
        ("AI+知识付费: 垂直领域课程热销", "https://www.geekpark.net", "月销百万"),
        ("AI定制开发: 企业方案报价百万起", "https://www.36kr.com", "行业定制蓝海"),
        ("AI硬件销售: AI PC换机潮将至", "https://finance.sina.com.cn", "新增长点"),
        ("AI数据服务: 高质量数据集售价不菲", "https://tech.sina.com.cn", "数据标注需求旺"),
        ("AI培训服务: 企业内训市场爆发", "https://www.36kr.com", "AI技能培训刚需"),
        ("AI联盟营销: 推广分成比例高达50%", "https://www.ifeng.com", "新副业"),
        ("AI应用商店: 插件生态分成兴起", "https://www.36kr.com", "类比App Store"),
        ("AI硬件机器人: 家庭场景商业化提速", "https://tech.sina.com.cn", "AI设备热销"),
    ],
}

def select_items(category, count=5):
    items = CONTENT_DB.get(category, [])
    return random.sample(items, min(count, len(items)))

def generate_html(section_data):
    today = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    section_map = {
        "tech": ("[T]", "AI最新技术", "追踪大模型、架构突破、开源进展"),
        "app": ("[A]", "AI应用场景", "从实验室到产业深水区"),
        "company": ("[C]", "AI公司动态", "融资、并购、战略与博弈"),
        "business": ("[B]", "AI商业模式", "从技术驱动到生态重构"),
    }
    
    colors = {
        "tech": "rgba(79, 143, 255, 0.15)",
        "app": "rgba(6, 214, 160, 0.15)",
        "company": "rgba(255, 107, 53, 0.15)",
        "business": "rgba(236, 72, 153, 0.15)",
    }
    
    sections_html = ""
    for sec in section_data:
        sid = sec["id"]
        icon, title, desc = section_map[sid]
        color = colors[sid]
        
        cards_html = ""
        for i, (item_title, url, item_desc) in enumerate(sec["items"], 1):
            cards_html += '<div class="card"><h3>' + str(i) + '. ' + item_title + '</h3><p>' + item_desc + '</p><a href="' + url + '" target="_blank">阅读原文</a></div>'
        
        sections_html += '<section class="section active" id="' + sid + '"><h2><span style="background:' + color + ';padding:8px 12px;border-radius:8px;">' + icon + '</span> ' + title + '</h2><p style="color:var(--muted);margin-bottom:20px;">' + desc + '</p><div class="grid">' + cards_html + '</div></section>'
    
    # 使用字符串替换而不是format
    html = HTML_TEMPLATE
    html = html.replace("{{UPDATE_TIME}}", today)
    html = html.replace("{{SECTIONS}}", sections_html)
    return html

# ========== HTML模板 ==========
HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>胡栋材的AI小栈 - AI前沿资讯分享</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        :root {
            --bg: #0a0a0f;
            --card: #1a1a2e;
            --blue: #4f8fff;
            --purple: #8b5cf6;
            --cyan: #06d6a0;
            --orange: #ff6b35;
            --pink: #ec4899;
            --text: #e8e8f0;
            --muted: #9898b0;
        }
        body { font-family: system-ui, sans-serif; background: var(--bg); color: var(--text); line-height: 1.6; }
        .hero { text-align: center; padding: 80px 20px 40px; background: linear-gradient(135deg, rgba(79,143,255,0.1), rgba(139,92,246,0.1)); }
        .hero h1 { font-size: 2.5rem; background: linear-gradient(135deg, var(--blue), var(--purple)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .hero p { color: var(--muted); margin-top: 10px; }
        .update-time { margin-top: 15px; color: var(--muted); font-size: 14px; }
        .update-time span { color: var(--cyan); }
        .nav { display: flex; justify-content: center; gap: 10px; padding: 20px; flex-wrap: wrap; }
        .nav a { padding: 10px 20px; background: var(--card); border: 1px solid #333; border-radius: 25px; color: var(--text); text-decoration: none; cursor: pointer; transition: all 0.3s; }
        .nav a:hover { background: #2a2a40; }
        .nav a.active { background: linear-gradient(135deg, var(--blue), var(--purple)); border: none; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .section { display: none; }
        .section.active { display: block; }
        .section h2 { font-size: 1.5rem; margin-bottom: 20px; display: flex; align-items: center; gap: 10px; }
        .section h2 span { font-size: 1.8rem; }
        .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(350px, 1fr)); gap: 16px; }
        .card { background: var(--card); border: 1px solid #333; border-radius: 12px; padding: 20px; transition: all 0.3s; }
        .card:hover { transform: translateY(-2px); box-shadow: 0 8px 30px rgba(0,0,0,0.3); }
        .card h3 { font-size: 15px; margin-bottom: 8px; }
        .card p { color: var(--muted); font-size: 13px; }
        .card a { color: var(--blue); text-decoration: none; font-size: 13px; margin-top: 10px; display: inline-block; }
        .mentor-link { background: linear-gradient(135deg, var(--blue), var(--purple)); }
        footer { text-align: center; padding: 40px; border-top: 1px solid #333; margin-top: 40px; color: var(--muted); }
        @media (max-width: 768px) {
            .grid { grid-template-columns: 1fr; }
            .hero h1 { font-size: 1.8rem; }
        }
    </style>
</head>
<body>
    <section class="hero">
        <h1>胡栋材的AI小栈</h1>
        <p>汇聚全球AI最新技术、工具、应用与商业动态</p>
        <p class="update-time">最后更新: <span>{{UPDATE_TIME}}</span> | 每天自动更新</p>
    </section>
    <nav class="nav">
        <a class="active" data-section="tech">[T] AI最新技术</a>
        <a data-section="app">[A] AI应用场景</a>
        <a data-section="company">[C] AI公司动态</a>
        <a data-section="business">[B] AI商业模式</a>
        <a href="/business-mentor/" class="mentor-link">[X] 商道导师</a>
    </nav>
    <main class="container">
        {{SECTIONS}}
    </main>
    <footer>
        <p>内容来源于公开网络，仅供学习参考 | <a href="https://github.com/hudongcai/hudongcai.github.io" style="color:var(--purple)">GitHub</a></p>
    </footer>
    <script>
        const navs = document.querySelectorAll('.nav a[data-section]');
        const sections = document.querySelectorAll('.section');
        navs.forEach(nav => {
            nav.addEventListener('click', () => {
                navs.forEach(n => n.classList.remove('active'));
                nav.classList.add('active');
                sections.forEach(s => s.classList.remove('active'));
                document.getElementById(nav.dataset.section).classList.add('active');
            });
        });
    </script>
</body>
</html>'''

def main():
    print("[START] Updating AI News Website")
    
    section_configs = ["tech", "app", "company", "business"]
    section_data = []
    
    for section_id in section_configs:
        items = select_items(section_id, 5)
        section_data.append({"id": section_id, "items": items})
        print("[OK] " + section_id + ": " + str(len(items)) + " items selected")
    
    html_content = generate_html(section_data)
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("[DONE] index.html generated (" + str(len(html_content)) + " bytes)")
    print("[INFO] " + str(len(section_data)) + " sections, 5 items each")
    
    return 0

if __name__ == "__main__":
    exit(main())
