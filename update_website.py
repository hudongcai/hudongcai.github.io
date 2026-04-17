#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI小栈网站内容更新脚本 V1.0
- 每个板块10条内容
- 竖向排列展示
- 精美版面设计
"""

import random
from datetime import datetime

# ========== 内容库 ==========
CONTENT_DB = {
    "tech": [
        ("DeepSeek V4: 100万Token窗口+多模态突破", "https://k.sina.com.cn", "原生支持图文视频，上下文窗口扩容至100万+Token"),
        ("通义千问 QWQ-32B 开源：性能对标GPT-4", "https://qwenlm.github.io", "阿里开源32B模型，推理能力大幅提升"),
        ("智谱 GLM-4 Plus 发布：中文理解能力最强", "https://www.zhipuai.cn", "国产大模型新标杆，多项评测第一"),
        ("百度文心4.0 Turbo：响应速度提升50%", "https://yiyan.baidu.com", "企业级AI应用首选，中文处理能力领先"),
        ("字节豆包大模型：日均调用量破万亿", "https://www.volcengine.com", "火山引擎发布豆包最新版本"),
        ("讯飞星火4.0：多语种能力全面提升", "https://xinghuo.xfyun.cn", "科大讯飞新一代认知大模型发布"),
        ("阶跃星辰Step-2：万亿参数MoE大模型发布", "https://stepfun.com", "国内又一重量级大模型，性能直逼GPT-4"),
        ("Kimi（月之暗面）发布200万字上下文", "https://kimi.moonshot.cn", "超长上下文窗口，支持整本书阅读"),
        ("Mistral Large 2：开源最强商用模型", "https://mistral.ai", "支持中文，性能比肩GPT-4o"),
        ("MiniMax海螺AI：国产对话模型新势力", "https://hailuoai.video", "专注长文本理解和多轮对话"),
    ],
    "app": [
        ("AI医疗：协和医院日均AI辅助诊断超万例", "https://www.36kr.com", "AI辅助阅片准确率达97%，大幅提升效率"),
        ("AI教育：个性化学习路径效率提升3倍", "https://www.36kr.com", "自适应学习系统根据学生特点定制课程"),
        ("AI制造：工厂质检效率提升80%", "https://finance.sina.com.cn", "AI视觉检测替代人工，降低成本提升良率"),
        ("AI金融：智能投顾管理资产破万亿", "https://tech.sina.com.cn", "AI量化策略年化收益超基准20%"),
        ("AI办公：Copilot月活企业超10万家", "https://www.microsoft.com", "文档处理效率提升50%，会议纪要自动生成"),
        ("AI客服：某电商平台AI接待率超90%", "https://www.aliyun.com", "7x24小时服务，问题解决率达85%"),
        ("AI创作：某MCN AI生成内容占比超60%", "https://www.36kr.com", "AI辅助写作效率提升5倍，成本降低70%"),
        ("AI编程：GitHub Copilot代码生成超40%", "https://github.blog", "全球超过150万开发者使用"),
        ("AI法律：合同审查效率提升10倍", "https://www.36kr.com", "AI秒级完成合同风险点识别"),
        ("AI设计：Logo生成工具日活破百万", "https://www.36kr.com", "设计师效率神器，3秒生成10种方案"),
    ],
    "company": [
        ("OpenAI年化营收突破40亿美元", "https://tech.sina.com.cn", "AI行业商业化进程加速"),
        ("英伟达Blackwell架构GPU供不应求", "https://finance.sina.com.cn", "AI芯片需求爆发，产能成最大瓶颈"),
        ("微软Copilot全线接入Windows系统", "https://www.microsoft.com", "AI助手将覆盖10亿Windows用户"),
        ("谷歌 Gemini 1.5 Pro 全面开放API", "https://blog.google", "百万Token上下文震惊业界"),
        ("百度文心一言企业用户超1000万", "https://k.sina.com.cn", "国产大模型商业化领先者"),
        ("字节豆包日活用户突破5000万", "https://www.bytedance.com", "国内AI应用增速第一"),
        ("阿里云AI收入同比增长超100%", "https://www.alibabagroup.com", "AI驱动云业务新一轮增长"),
        ("华为盘古大模型5.0：全场景能力升级", "https://www.huawei.com", "赋能千行百业，国产最强行业大模型"),
        ("腾讯混元大模型：企业微信全面接入", "https://www.tencent.com", "社交+AI战略全面推进"),
        ("商汤日日新5.0：CV领域再突破", "https://www.sensetime.com", "计算机视觉+大模型深度融合"),
    ],
    "business": [
        ("AI SaaS订阅模式：年ARR增长200%", "https://www.36kr.com", "按月/年订阅，续费率超90%"),
        ("AI API调用收费：按量计费成主流", "https://openai.com", "Token消耗计费，毛利率超70%"),
        ("AI+知识付费：垂直领域课程热销", "https://www.geekpark.net", "AI使用技巧课程月销百万"),
        ("AI定制开发：企业级解决方案报价百万起", "https://www.36kr.com", "行业定制AI解决方案成蓝海"),
        ("AI硬件销售：AI PC换机潮将至", "https://finance.sina.com.cn", "搭载NPU的PC成为新增长点"),
        ("AI数据服务：高质量数据集售价不菲", "https://tech.sina.com.cn", "垂直领域数据标注需求旺盛"),
        ("AI培训服务：企业内训市场爆发", "https://www.36kr.com", "AI技能培训成企业刚需"),
        ("AI联盟营销：推广分成比例高达50%", "https://www.ifeng.com", "AI产品分销成为新副业"),
        ("AI应用商店：插件生态分成模式兴起", "https://www.36kr.com", "类比App Store的新变现渠道"),
        ("AI硬件机器人：家庭场景商业化提速", "https://tech.sina.com.cn", "AI手机、AI眼镜、AI陪伴机器人热销"),
    ],
}

def select_items(category, count=10):
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
        "tech": ("#4f8fff", "rgba(79, 143, 255, 0.15)"),
        "app": ("#06d6a0", "rgba(6, 214, 160, 0.15)"),
        "company": ("#ff6b35", "rgba(255, 107, 53, 0.15)"),
        "business": ("#ec4899", "rgba(236, 72, 153, 0.15)"),
    }
    
    sections_html = ""
    for sec in section_data:
        sid = sec["id"]
        icon, title, desc = section_map[sid]
        color_code, color_bg = colors[sid]
        
        items_html = ""
        for i, (item_title, url, item_desc) in enumerate(sec["items"], 1):
            items_html += '<div class="news-item" style="background:linear-gradient(135deg,rgba(255,255,255,0.03),rgba(255,255,255,0.01));border:1px solid rgba(255,255,255,0.08);border-radius:12px;padding:20px 24px;margin-bottom:12px;display:flex;gap:16px;align-items:flex-start;transition:all 0.3s;cursor:pointer;" onmouseover="this.style.borderColor=\'' + color_code + '\';this.style.transform=\'translateX(4px)\';" onmouseout="this.style.borderColor=\'rgba(255,255,255,0.08)\';this.style.transform=\'translateX(0)\';">'
            items_html += '<span style="min-width:36px;height:36px;background:' + color_bg + ';border-radius:8px;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:14px;color:' + color_code + ';">' + str(i) + '</span>'
            items_html += '<div style="flex:1;"><h3 style="font-size:15px;font-weight:600;margin-bottom:6px;color:#fff;">' + item_title + '</h3><p style="font-size:13px;color:#9898b0;line-height:1.6;">' + item_desc + '</p></div>'
            items_html += '<a href="' + url + '" target="_blank" style="color:' + color_code + ';text-decoration:none;font-size:13px;white-space:nowrap;align-self:center;">查看详情</a>'
            items_html += '</div>'
        
        sections_html += '<section class="section active" id="' + sid + '">'
        sections_html += '<div style="display:flex;align-items:center;gap:16px;margin-bottom:24px;padding-bottom:16px;border-bottom:1px solid rgba(255,255,255,0.08);">'
        sections_html += '<span style="width:48px;height:48px;background:' + color_bg + ';border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:24px;">' + icon + '</span>'
        sections_html += '<div><h2 style="font-size:1.4rem;font-weight:700;color:#fff;">' + title + '</h2><p style="font-size:13px;color:#6b6b80;margin-top:2px;">' + desc + '</p></div>'
        sections_html += '</div>'
        sections_html += '<div class="news-list">' + items_html + '</div>'
        sections_html += '</section>'
    
    html = HTML_TEMPLATE
    html = html.replace("{{UPDATE_TIME}}", today)
    html = html.replace("{{SECTIONS}}", sections_html)
    return html

# ========== HTML模板 V1.0 ==========
HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>胡栋材的AI小栈 - AI前沿资讯分享</title>
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>T</text></svg>">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        :root {
            --bg-primary: #0a0a0f;
            --bg-secondary: #12121a;
            --bg-card: #1a1a2e;
            --accent-blue: #4f8fff;
            --accent-purple: #8b5cf6;
            --accent-cyan: #06d6a0;
            --accent-orange: #ff6b35;
            --accent-pink: #ec4899;
            --text-primary: #e8e8f0;
            --text-secondary: #9898b0;
            --text-muted: #6b6b80;
            --border-color: rgba(255, 255, 255, 0.08);
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.6;
            min-height: 100vh;
        }
        
        /* Hero Section */
        .hero {
            position: relative;
            padding: 100px 20px 60px;
            text-align: center;
            background: linear-gradient(180deg, rgba(79, 143, 255, 0.08) 0%, transparent 100%);
            overflow: hidden;
        }
        
        .hero::before {
            content: '';
            position: absolute;
            top: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 800px;
            height: 400px;
            background: radial-gradient(ellipse at center top, rgba(79, 143, 255, 0.15), transparent 70%);
            pointer-events: none;
        }
        
        .hero-content {
            position: relative;
            z-index: 1;
        }
        
        .hero-badge {
            display: inline-block;
            padding: 6px 16px;
            background: rgba(79, 143, 255, 0.1);
            border: 1px solid rgba(79, 143, 255, 0.2);
            border-radius: 20px;
            font-size: 12px;
            color: var(--accent-blue);
            letter-spacing: 1px;
            margin-bottom: 20px;
        }
        
        .hero h1 {
            font-size: clamp(2rem, 5vw, 3rem);
            font-weight: 800;
            background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple), var(--accent-pink));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 12px;
            letter-spacing: -0.5px;
        }
        
        .hero p {
            color: var(--text-secondary);
            font-size: 1.1rem;
            max-width: 500px;
            margin: 0 auto;
        }
        
        .update-info {
            margin-top: 24px;
            padding: 12px 24px;
            background: rgba(6, 214, 160, 0.08);
            border: 1px solid rgba(6, 214, 160, 0.15);
            border-radius: 30px;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            font-size: 13px;
            color: var(--text-secondary);
        }
        
        .update-info .dot {
            width: 8px;
            height: 8px;
            background: var(--accent-cyan);
            border-radius: 50%;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.4; }
        }
        
        /* Navigation */
        .nav-container {
            position: sticky;
            top: 0;
            z-index: 100;
            background: rgba(10, 10, 15, 0.9);
            backdrop-filter: blur(20px);
            border-bottom: 1px solid var(--border-color);
            padding: 12px 20px;
        }
        
        .nav-tabs {
            display: flex;
            justify-content: center;
            gap: 8px;
            flex-wrap: wrap;
            max-width: 900px;
            margin: 0 auto;
        }
        
        .nav-tab {
            padding: 10px 20px;
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 25px;
            color: var(--text-secondary);
            font-size: 14px;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
        }
        
        .nav-tab:hover {
            background: var(--bg-secondary);
            color: var(--text-primary);
        }
        
        .nav-tab.active {
            background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple));
            border-color: transparent;
            color: white;
            box-shadow: 0 4px 20px rgba(79, 143, 255, 0.3);
        }
        
        .nav-tab.mentor-link {
            background: linear-gradient(135deg, var(--accent-cyan), var(--accent-blue));
            border-color: transparent;
            color: white;
        }
        
        /* Main Content */
        .container {
            max-width: 900px;
            margin: 0 auto;
            padding: 40px 20px 80px;
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
        
        /* QR Code Section */
        .qr-section {
            background: linear-gradient(135deg, rgba(79, 143, 255, 0.05), rgba(139, 92, 246, 0.05));
            border: 1px solid var(--border-color);
            border-radius: 20px;
            padding: 32px;
            margin-top: 60px;
            text-align: center;
        }
        
        .qr-section h3 {
            font-size: 1.2rem;
            margin-bottom: 24px;
            color: var(--text-primary);
        }
        
        .qr-container {
            display: flex;
            justify-content: center;
            gap: 40px;
            flex-wrap: wrap;
        }
        
        .qr-item {
            text-align: center;
        }
        
        .qr-item img {
            width: 140px;
            height: 140px;
            border-radius: 12px;
            border: 2px solid var(--border-color);
            background: white;
            padding: 8px;
        }
        
        .qr-item p {
            margin-top: 12px;
            font-size: 13px;
            color: var(--text-muted);
        }
        
        /* Footer */
        footer {
            text-align: center;
            padding: 40px 20px;
            border-top: 1px solid var(--border-color);
            margin-top: 60px;
        }
        
        footer p {
            color: var(--text-muted);
            font-size: 14px;
        }
        
        footer a {
            color: var(--accent-purple);
            text-decoration: none;
        }
        
        footer a:hover {
            text-decoration: underline;
        }
        
        /* Responsive */
        @media (max-width: 768px) {
            .hero { padding: 60px 16px 40px; }
            .hero h1 { font-size: 1.8rem; }
            .nav-tabs { gap: 6px; }
            .nav-tab { padding: 8px 14px; font-size: 13px; }
            .news-item { padding: 16px !important; }
            .qr-container { gap: 24px; }
            .qr-item img { width: 120px; height: 120px; }
        }
    </style>
</head>
<body>
    <section class="hero">
        <div class="hero-content">
            <span class="hero-badge">AI FRONTLINE NEWS</span>
            <h1>胡栋材的AI小栈</h1>
            <p>汇聚全球AI最新技术、工具、应用与商业动态</p>
            <div class="update-info">
                <span class="dot"></span>
                最后更新: {{UPDATE_TIME}} | 每天自动更新
            </div>
        </div>
    </section>
    
    <div class="nav-container">
        <nav class="nav-tabs">
            <a class="nav-tab active" data-section="tech">[T] AI最新技术</a>
            <a class="nav-tab" data-section="app">[A] AI应用场景</a>
            <a class="nav-tab" data-section="company">[C] AI公司动态</a>
            <a class="nav-tab" data-section="business">[B] AI商业模式</a>
            <a href="/business-mentor/" class="nav-tab mentor-link">[M] 商道导师</a>
        </nav>
    </div>
    
    <main class="container">
        {{SECTIONS}}
        
        <div class="qr-section">
            <h3>扫码交流</h3>
            <div class="qr-container">
                <div class="qr-item">
                    <img src="wechat-qr.jpg" alt="微信交流" onerror="this.src='data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 140 140%22><rect fill=%22%231a1a2e%22 width=%22140%22 height=%22140%22 rx=%2212%22/><text x=%2270%22 y=%2275%22 text-anchor=%22middle%22 fill=%22%236b6b80%22 font-size=%2212%22>微信二维码</text></svg>'">
                    <p>个人微信</p>
                </div>
                <div class="qr-item">
                    <img src="wechat-group.jpg" alt="微信群" onerror="this.src='data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 140 140%22><rect fill=%22%231a1a2e%22 width=%22140%22 height=%22140%22 rx=%2212%22/><text x=%2270%22 y=%2275%22 text-anchor=%22middle%22 fill=%22%236b6b80%22 font-size=%2212%22>微信群</text></svg>'">
                    <p>交流群</p>
                </div>
            </div>
        </div>
    </main>
    
    <footer>
        <p>内容来源于公开网络，仅供学习参考<br><a href="https://github.com/hudongcai/hudongcai.github.io" target="_blank">GitHub</a></p>
    </footer>
    
    <script>
        const navs = document.querySelectorAll('.nav-tab[data-section]');
        const sections = document.querySelectorAll('.section');
        
        navs.forEach(nav => {
            nav.addEventListener('click', () => {
                navs.forEach(n => n.classList.remove('active'));
                nav.classList.add('active');
                sections.forEach(s => s.classList.remove('active'));
                document.getElementById(nav.dataset.section).classList.add('active');
                window.scrollTo({ top: 0, behavior: 'smooth' });
            });
        });
    </script>
</body>
</html>'''

def main():
    print("[START] Updating AI News Website V1.0")
    
    section_configs = ["tech", "app", "company", "business"]
    section_data = []
    
    for section_id in section_configs:
        items = select_items(section_id, 10)
        section_data.append({"id": section_id, "items": items})
        print("[OK] " + section_id + ": " + str(len(items)) + " items")
    
    html_content = generate_html(section_data)
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("[DONE] index.html generated (" + str(len(html_content)) + " bytes)")
    print("[INFO] 4 sections, 10 items each, V1.0 design")
    
    return 0

if __name__ == "__main__":
    exit(main())
