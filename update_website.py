#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新AI小栈网站内容
- 读取最新的AI资讯数据
- 生成新的index.html
- 提交到GitHub Pages仓库
"""

import urllib.request
import urllib.parse
import json
import os
import random
from datetime import datetime

# ========== 配置 ==========
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
WEBSITE_REPO = "hudongcai/hudongcai.github.io"

# ========== 五大板块内容库 ==========
CONTENT_DB = {
    "tech": [
        ("DeepSeek V4 发布：百万Token窗口 + 多模态突破", "https://k.sina.com.cn/article_7857201856_1d45362c0019048aae.html", "原生支持图文视频，上下文窗口扩容至100万+Token"),
        ("通义千问 QWQ-32B 开源：性能对标GPT-4", "https://qwenlm.github.io/blog/qwq-32b/", "阿里开源32B模型，推理能力大幅提升"),
        ("智谱 GLM-4 Plus 发布：中文理解能力最强", "https://www.zhipuai.cn/", "国产大模型新标杆，多项评测第一"),
        ("百度文心4.0 Turbo：响应速度提升50%", "https://yiyan.baidu.com/", "企业级AI应用首选，中文处理能力领先"),
        ("字节豆包大模型：日均调用量破万亿", "https://www.volcengine.com/product/doubao", "火山引擎发布豆包最新版本"),
        ("讯飞星火4.0：多语种能力全面提升", "https://xinghuo.xfyun.cn/", "科大讯飞新一代认知大模型发布"),
        ("阶跃星辰Step-2：万亿参数MoE大模型发布", "https://stepfun.com/", "国内又一重量级大模型，性能直逼GPT-4"),
        ("MiniMax海螺AI：国产对话模型新势力", "https://hailuoai.video/", "专注长文本理解和多轮对话"),
        ("Kimi（月之暗面）发布200万字上下文", "https://kimi.moonshot.cn/", "超长上下文窗口，支持整本书阅读"),
        ("Mistral Large 2：开源最强商用模型", "https://mistral.ai/news/mistral-large-2/", "支持中文，性能比肩GPT-4o"),
    ],
    "app": [
        ("AI医疗：协和医院日均AI辅助诊断超万例", "https://www.36kr.com/channel/tech", "AI辅助阅片准确率达97%，大幅提升效率"),
        ("AI教育：个性化学习路径效率提升3倍", "https://www.36kr.com/p/3572274259016581", "自适应学习系统根据学生特点定制课程"),
        ("AI制造：工厂质检效率提升80%", "https://finance.sina.com.cn/", "AI视觉检测替代人工，降低成本提升良率"),
        ("AI金融：智能投顾管理资产破万亿", "https://tech.sina.com.cn/", "AI量化策略年化收益超基准20%"),
        ("AI办公：Copilot月活企业超10万家", "https://www.microsoft.com/zh-cn/microsoft-365/blog", "文档处理效率提升50%，会议纪要自动生成"),
        ("AI客服：某电商平台AI接待率超90%", "https://www.aliyun.com/", "7x24小时服务，问题解决率达85%"),
        ("AI创作：某MCN AI生成内容占比超60%", "https://www.36kr.com/", "AI辅助写作效率提升5倍，成本降低70%"),
        ("AI编程：GitHub Copilot代码生成超40%", "https://github.blog/", "全球超过150万开发者使用"),
        ("AI法律：合同审查效率提升10倍", "https://www.36kr.com/channel/tech", "AI秒级完成合同风险点识别"),
        ("AI设计：Logo生成工具日活破百万", "https://www.36kr.com/", "设计师效率神器，3秒生成10种方案"),
    ],
    "company": [
        ("OpenAI年化营收突破40亿美元", "https://tech.sina.com.cn/", "AI行业商业化进程加速"),
        ("英伟达Blackwell架构GPU供不应求", "https://finance.sina.com.cn/", "AI芯片需求爆发，产能成最大瓶颈"),
        ("微软Copilot全线接入Windows系统", "https://www.microsoft.com/zh-cn/microsoft-365/blog", "AI助手将覆盖10亿Windows用户"),
        ("谷歌 Gemini 1.5 Pro 全面开放API", "https://blog.google/technology/ai/", "百万Token上下文震惊业界"),
        ("百度文心一言企业用户超1000万", "https://k.sina.com.cn/", "国产大模型商业化领先者"),
        ("字节豆包日活用户突破5000万", "https://www.bytedance.com/", "国内AI应用增速第一"),
        ("阿里云AI收入同比增长超100%", "https://www.alibabagroup.com/", "AI驱动云业务新一轮增长"),
        ("华为盘古大模型5.0：全场景能力升级", "https://www.huawei.com/cn/", "赋能千行百业，国产最强行业大模型"),
        ("腾讯混元大模型：企业微信全面接入", "https://www.tencent.com/", "社交+AI战略全面推进"),
        ("商汤日日新5.0：CV领域再突破", "https://www.sensetime.com/cn/", "计算机视觉+大模型深度融合"),
    ],
    "business": [
        ("AI SaaS订阅模式：年ARR增长200%", "https://www.36kr.com/", "按月/年订阅，续费率超90%"),
        ("AI API调用收费：按量计费成主流", "https://openai.com/blog", "Token消耗计费，毛利率超70%"),
        ("AI+知识付费：垂直领域课程热销", "https://www.geekpark.net/", "AI使用技巧课程月销百万"),
        ("AI定制开发：企业级解决方案报价百万起", "https://www.36kr.com/p/", "行业定制AI解决方案成蓝海"),
        ("AI硬件销售：AI PC换机潮将至", "https://finance.sina.com.cn/", "搭载NPU的PC成为新增长点"),
        ("AI数据服务：高质量数据集售价不菲", "https://tech.sina.com.cn/", "垂直领域数据标注需求旺盛"),
        ("AI培训服务：企业内训市场爆发", "https://www.36kr.com/p/", "AI技能培训成企业刚需"),
        ("AI联盟营销：推广分成比例高达50%", "https://www.ifeng.com/", "AI产品分销成为新副业"),
        ("AI应用商店：插件生态分成模式兴起", "https://www.36kr.com/", "类比App Store的新变现渠道"),
        ("AI硬件机器人：家庭场景商业化提速", "https://tech.sina.com.cn/", "AI手机、AI眼镜、AI陪伴机器人热销"),
    ],
}

# ========== 网站HTML模板 ==========
HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>胡栋材的AI小栈 - AI前沿资讯分享</title>
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🤖</text></svg>">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }

        :root {
            --bg-primary: #0a0a0f;
            --bg-secondary: #12121a;
            --bg-card: #1a1a2e;
            --bg-card-hover: #222240;
            --accent-blue: #4f8fff;
            --accent-purple: #8b5cf6;
            --accent-cyan: #06d6a0;
            --accent-orange: #ff6b35;
            --accent-pink: #ec4899;
            --accent-yellow: #fbbf24;
            --text-primary: #e8e8f0;
            --text-secondary: #9898b0;
            --text-muted: #6b6b80;
            --border-color: #2a2a3e;
            --glow-blue: rgba(79, 143, 255, 0.15);
            --glow-purple: rgba(139, 92, 246, 0.15);
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.6;
            min-height: 100vh;
        }

        .hero {
            position: relative;
            padding: 80px 20px 60px;
            text-align: center;
            overflow: hidden;
        }

        .hero::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(ellipse at 30% 20%, var(--glow-blue) 0%, transparent 50%),
                        radial-gradient(ellipse at 70% 80%, var(--glow-purple) 0%, transparent 50%);
            animation: bgPulse 8s ease-in-out infinite alternate;
        }

        @keyframes bgPulse {
            0% { opacity: 0.6; transform: scale(1); }
            100% { opacity: 1; transform: scale(1.05); }
        }

        .hero-content {
            position: relative;
            z-index: 1;
        }

        .hero-badge {
            display: inline-block;
            padding: 6px 18px;
            background: rgba(79, 143, 255, 0.12);
            border: 1px solid rgba(79, 143, 255, 0.3);
            border-radius: 20px;
            font-size: 13px;
            color: var(--accent-blue);
            margin-bottom: 24px;
            letter-spacing: 1px;
        }

        .hero h1 {
            font-size: clamp(2.2rem, 5vw, 3.5rem);
            font-weight: 800;
            background: linear-gradient(135deg, #4f8fff, #8b5cf6, #ec4899);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 16px;
            letter-spacing: -0.5px;
        }

        .hero p {
            color: var(--text-secondary);
            font-size: 1.1rem;
            max-width: 600px;
            margin: 0 auto 30px;
        }

        .hero-url {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 10px 24px;
            background: rgba(139, 92, 246, 0.1);
            border: 1px solid rgba(139, 92, 246, 0.25);
            border-radius: 30px;
            color: var(--accent-purple);
            font-size: 14px;
            text-decoration: none;
            transition: all 0.3s ease;
        }

        .hero-url:hover {
            background: rgba(139, 92, 246, 0.2);
            border-color: rgba(139, 92, 246, 0.5);
            transform: translateY(-2px);
        }

        .update-info {
            margin-top: 20px;
            font-size: 13px;
            color: var(--text-muted);
        }

        .update-info .dot {
            display: inline-block;
            width: 8px;
            height: 8px;
            background: var(--accent-cyan);
            border-radius: 50%;
            margin-right: 6px;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.4; }
        }

        .nav-tabs {
            display: flex;
            justify-content: center;
            gap: 8px;
            padding: 0 20px 40px;
            flex-wrap: wrap;
            position: relative;
            z-index: 1;
        }

        .nav-tab {
            padding: 10px 22px;
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 25px;
            color: var(--text-secondary);
            font-size: 14px;
            cursor: pointer;
            transition: all 0.3s ease;
            white-space: nowrap;
        }

        .nav-tab:hover {
            background: var(--bg-card-hover);
            color: var(--text-primary);
        }

        .nav-tab.active {
            background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple));
            border-color: transparent;
            color: white;
            box-shadow: 0 4px 20px rgba(79, 143, 255, 0.3);
        }

        .nav-tab .tab-icon {
            margin-right: 6px;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px 60px;
        }

        .section {
            display: none;
            animation: fadeIn 0.4s ease;
        }

        .section.active {
            display: block;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .section-header {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 24px;
        }

        .section-icon {
            width: 48px;
            height: 48px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
        }

        .section-header > div:last-child {
            flex: 1;
        }

        .section-header h2 {
            font-size: 1.5rem;
            font-weight: 700;
        }

        .section-header .section-desc {
            color: var(--text-muted);
            font-size: 13px;
            margin-left: auto;
        }

        .news-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 16px;
        }

        .news-card {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 20px;
            display: flex;
            gap: 16px;
            transition: all 0.3s ease;
            cursor: pointer;
        }

        .news-card:hover {
            background: var(--bg-card-hover);
            transform: translateY(-2px);
            box-shadow: 0 8px 30px rgba(0,0,0,0.3);
        }

        .news-card:hover .card-title {
            color: var(--accent-blue);
        }

        .card-index {
            width: 32px;
            height: 32px;
            background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple));
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 14px;
            flex-shrink: 0;
        }

        .card-content {
            flex: 1;
            min-width: 0;
        }

        .card-title {
            font-size: 15px;
            font-weight: 600;
            margin-bottom: 8px;
            color: var(--text-primary);
            transition: color 0.3s;
        }

        .card-desc {
            font-size: 13px;
            color: var(--text-secondary);
            line-height: 1.6;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }

        .card-link {
            display: inline-flex;
            align-items: center;
            gap: 4px;
            margin-top: 10px;
            font-size: 12px;
            color: var(--accent-blue);
            text-decoration: none;
        }

        .card-link:hover {
            text-decoration: underline;
        }

        footer {
            text-align: center;
            padding: 40px 20px;
            border-top: 1px solid var(--border-color);
            margin-top: 60px;
        }

        footer a {
            color: var(--accent-purple);
            text-decoration: none;
        }

        footer a:hover {
            text-decoration: underline;
        }

        .footer-content {
            color: var(--text-muted);
            font-size: 14px;
        }

        .wechat-section {
            display: flex;
            justify-content: center;
            gap: 30px;
            margin: 30px 0;
            flex-wrap: wrap;
        }

        .wechat-card {
            text-align: center;
        }

        .wechat-card img {
            width: 120px;
            height: 120px;
            border-radius: 12px;
            border: 2px solid var(--border-color);
        }

        .wechat-card p {
            margin-top: 8px;
            font-size: 13px;
            color: var(--text-muted);
        }

        @media (max-width: 768px) {
            .hero { padding: 50px 16px 40px; }
            .hero h1 { font-size: 1.8rem; }
            .nav-tabs { gap: 6px; padding: 0 12px 30px; }
            .nav-tab { padding: 8px 14px; font-size: 13px; }
            .news-card { padding: 16px; gap: 12px; }
            .section-header .section-desc { display: none; }
        }

        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-track { background: var(--bg-secondary); }
        ::-webkit-scrollbar-thumb { background: var(--border-color); border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: var(--text-muted); }
    </style>
</head>
<body>
    <section class="hero">
        <div class="hero-content">
            <span class="hero-badge">🤖 AI 前沿资讯</span>
            <h1>胡栋材的AI小栈</h1>
            <p>汇聚全球AI最新技术、工具、应用、公司与商业动态</p>
            <div class="update-info">
                <span class="dot"></span>
                最后更新：{update_time} | 每天自动更新
            </div>
        </div>
    </section>

    <nav class="nav-tabs">
        {nav_tabs}
        <a href="/business-mentor/" class="nav-tab" style="text-decoration:none; background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple)); border-color: transparent; color: white;">
            <span class="tab-icon">🎯</span>商道导师
        </a>
    </nav>

    <main class="container">
        {sections}
    </main>

    <footer>
        <div class="wechat-section">
            <div class="wechat-card">
                <img src="wechat-qr.jpg" alt="微信二维码" onerror="this.style.display='none'">
                <p>微信交流</p>
            </div>
            <div class="wechat-card">
                <img src="wechat-group.jpg" alt="微信群二维码" onerror="this.style.display='none'">
                <p>加入交流群</p>
            </div>
        </div>
        <p class="footer-content">
            内容来源于公开网络，仅供学习参考<br>
            <a href="https://github.com/hudongcai/hudongcai.github.io" target="_blank">GitHub</a>
        </p>
    </footer>

    <script>
        const tabs = document.querySelectorAll('.nav-tab');
        const sections = document.querySelectorAll('.section');

        tabs.forEach(tab => {{
            tab.addEventListener('click', () => {{
                const target = tab.dataset.section;
                
                tabs.forEach(t => t.classList.remove('active'));
                tab.classList.add('active');
                
                sections.forEach(s => {{
                    s.classList.remove('active');
                    if (s.id === target) {{
                        s.classList.add('active');
                    }}
                }});

                window.scrollTo({{ top: 0, behavior: 'smooth' }});
            }});
        }});

        const observer = new IntersectionObserver((entries) => {{
            entries.forEach(entry => {{
                if (entry.isIntersecting) {{
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }}
            }});
        }}, {{ threshold: 0.1 }});

        document.querySelectorAll('.news-card').forEach(card => {{
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            observer.observe(card);
        }});
    </script>
</body>
</html>
'''

# ========== 工具函数 ==========

def check_url(url):
    """检查链接是否有效"""
    if not url or url.startswith("site:") or "..." in url:
        return False
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        req = urllib.request.Request(url, headers=headers, method='HEAD')
        with urllib.request.urlopen(req, timeout=5) as resp:
            return resp.status == 200
    except:
        return False

def select_items(category, count=5):
    """为指定分类随机选取内容"""
    items = random.sample(CONTENT_DB.get(category, []), min(count, len(CONTENT_DB.get(category, []))))
    return items

def verify_items(items):
    """审核并补足内容"""
    valid = []
    for item in items:
        title, url, desc = item
        if check_url(url):
            valid.append(item)
        else:
            print(f"  ❌ 失效: {title[:35]}...")
    
    attempts = 0
    while len(valid) < 5 and attempts < 50:
        attempts += 1
        for cat_items in CONTENT_DB.values():
            for item in random.sample(cat_items, len(cat_items)):
                if item not in valid and check_url(item[1]):
                    valid.append(item)
                    print(f"  📦 补足: {item[0][:35]}...")
                    break
            if len(valid) >= 5:
                break
    
    return valid[:5]

def generate_html(section_data):
    """生成网站HTML"""
    today = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    nav_configs = [
        ("tech", "🔬", "AI最新技术"),
        ("app", "🚀", "AI应用场景"),
        ("company", "🏢", "AI公司动态"),
        ("business", "💰", "AI商业模式"),
    ]
    
    nav_tabs = ""
    for section_id, icon, title in nav_configs:
        nav_tabs += f'''<div class="nav-tab" data-section="{section_id}">
            <span class="tab-icon">{icon}</span>{title}
        </div>\n'''
    
    sections_html = ""
    section_configs = [
        ("tech", "🔬", "AI最新技术", "追踪大模型、架构突破、开源进展", "rgba(79, 143, 255, 0.15)"),
        ("app", "🚀", "AI应用场景", "从实验室到产业深水区", "rgba(6, 214, 160, 0.15)"),
        ("company", "🏢", "AI公司动态", "融资、并购、战略与博弈", "rgba(255, 107, 53, 0.15)"),
        ("business", "💰", "AI商业模式", "从技术驱动到生态重构", "rgba(236, 72, 153, 0.15)"),
    ]
    
    for section_id, icon, title, desc, color in section_configs:
        sections_html += f'''
        <section class="section" id="{section_id}">
            <div class="section-header">
                <div class="section-icon" style="background: {color};">{icon}</div>
                <div>
                    <h2>{title}</h2>
                    <p class="section-desc">{desc}</p>
                </div>
            </div>
            <div class="news-grid">
'''
        
        items = next((s["items"] for s in section_data if s["id"] == section_id), [])
        
        for i, (item_title, url, item_desc) in enumerate(items, 1):
            sections_html += f'''
                <a href="{url}" target="_blank" class="news-card" style="text-decoration:none; color:inherit;">
                    <div class="card-index">{i}</div>
                    <div class="card-content">
                        <div class="card-title">{item_title}</div>
                        <div class="card-desc">{item_desc}</div>
                        <span class="card-link">阅读原文 →</span>
                    </div>
                </a>
'''
        
        sections_html += '''
            </div>
        </section>
'''
    
    return HTML_TEMPLATE.format(
        update_time=today,
        nav_tabs=nav_tabs,
        sections=sections_html
    )

def main():
    print("=" * 60)
    print("🤖 更新AI小栈网站内容")
    print("=" * 60)
    
    section_configs = [
        ("tech", "🔬", "最新AI技术"),
        ("app", "💡", "最新AI应用场景"),
        ("company", "🏢", "最新AI公司消息"),
        ("business", "💰", "最新AI商业盈利模式"),
    ]
    
    section_data = []
    
    for section_id, icon, title in section_configs:
        print(f"\n📂 {icon} {title}")
        items = select_items(section_id, 8)
        valid_items = verify_items(items)
        
        section_data.append({
            "id": section_id,
            "icon": icon,
            "title": title,
            "items": valid_items
        })
    
    html_content = generate_html(section_data)
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"\n✅ 已生成 index.html ({len(html_content)} 字符)")
    print(f"   更新内容：{len(section_data)} 个板块，每板块 5 条")
    
    return 0

if __name__ == "__main__":
    exit(main())
