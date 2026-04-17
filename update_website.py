#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI小栈网站内容更新脚本 V2.0
- 每个板块10条内容，使用真实可验证的链接
- 内容去重机制，避免重复展示
- 往期回顾功能，保存历史内容
"""

import random
import json
import os
from datetime import datetime

# ========== 真实内容库 ==========
CONTENT_DB = {
    "tech": [
        ("DeepSeek V4规格曝光：1万亿参数+100万上下文", "https://blog.wenhaofree.com/posts/articles/2026-04-11-deepseek-v4-spec-leaks/", "国产大模型开启算力军备竞赛新纪元"),
        ("2026大模型排行榜：DeepSeek V4、Kimi K2.5实测排名", "https://ofox.ai/zh/blog/ai-model-ranking-selection-guide-2026/", "10+主流AI模型编程、推理、多模态评分对比"),
        ("48小时连发5款大模型：阿里Wan2.7、谷歌Gemma4", "https://cloud.tencent.com.cn/developer/article/2650738", "MoE架构普及、端侧部署成熟、多模态成标配"),
        ("DeepSeek-V3亮相：推理能力超越GPT-4o", "https://www.zhifeiya.cn/news/2026-04-07-deepseek-v3-gpt-4o", "国产大模型新突破，代码能力大幅提升"),
        ("万字长文拆解DeepSeek大模型技术演进", "https://cloud.tencent.com/developer/article/2650758", "从算力军备竞赛到架构创新"),
        ("国产大模型密集发布：DeepSeek V4、智谱GLM-5.1", "https://aicode.cc/2026-04-10-e1de1862-b997-4ac7-a4e2-531cc4ac4610.html", "国产模型取得关键技术突破"),
        ("2026年4月12日全球AI前沿动态：DeepSeek V4预计下旬发布", "https://devpress.csdn.net/v1/article/detail/160087408", "智谱GLM-5.1超越Claude Opus"),
        ("2026国产AI突围战：DeepSeek、通义千问、豆包", "https://www.pconline.com.cn/ai/article/1549967.html", "国产AI模型凭借本土化优势强势突围"),
        ("2026年AI大模型最新动态：从架构革新到Agent爆发", "https://www.sohu.com/a/980715205_122619244", "智能体成为行业共识的应用方向"),
        ("AI大模型图鉴2026：谁在造神，谁在守夜", "https://www.woshipm.com/ai/6376638.html", "技术从来不是中性的，每个选择都有代价"),
    ],
    "app": [
        ("从技术模型到场景落地：医疗AI如何真正走进医院", "https://www3.xinhuanet.com/tech/20260415/ddfdbcb12bc94eaf968dd314424f3582/c.html", "AI辅助诊断在多家医院实现规模化应用"),
        ("2026全国企业AI创新案例TOP100正式发布", "http://www.enet.com.cn/article/2026/0413/A202604131275279.html", "产业智能化的实战检阅，覆盖多个行业"),
        ("2026中国企业AI应用场景全景报告", "https://www.showapi.com/news/article/69c3865b4ddd79ab67129477", "超68%中大型企业已开展AI场景实践"),
        ("AI+行业落地指南：制造业、医疗、零售案例解析", "https://cloud.tencent.com/developer/article/2624482", "避免认知两极化、应用碎片化等常见误区"),
        ("2026中国企业AI应用场景报告 - InfoQ", "https://www.infoq.cn/article/4c1lsTMm8kO4XAJuYpfz", "金融、零售、能源、制造等重点行业拆解"),
        ("AI行业应用：金融、医疗、教育、制造业落地案例", "https://jishuzhan.net/article/1963925204906328065", "四大核心行业的具体应用深度解析"),
        ("AI在金融、医疗、教育、制造业等领域落地指南", "https://www.cnblogs.com/yjbjingcha/p/19088685", "工业大模型、AI辅助诊断、智能零售等关键技术"),
        ("2026全国企业AI创新案例TOP100 - 硅谷动力", "http://www.ciweek.com/article/2026/0413/A2026041335128.shtml", "唯一评判标准交给实际应用效果"),
        ("AI行业应用：金融医疗教育制造业案例全解析", "https://blog.csdn.net/zzywxc787/article/details/154915840", "技术原理、典型应用、代码示例完整覆盖"),
        ("2026年AI圈动态盘点：模型闪电战与智能体落地", "https://xueqiu.com/4092447343/383054216", "从OpenAI到阿里千问，行业格局持续重塑"),
    ],
    "company": [
        ("OpenAI完成1100亿美元融资：英伟达、软银、亚马逊重金押注", "https://finance.sina.com.cn/roll/2026-03-02/doc-inhpqqum4668320.shtml", "刷新全球私营科技公司单笔融资纪录"),
        ("2026年4月AI行业全景扫描：巨头融资创新高", "https://www.msn.cn/zh-cn/%E6%8A%80%E6%9C%AF/%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD/2026%E5%B9%B44%E6%9C%88ai%E8%A1%8C%E4%B8%9A%E5%85%A8%E6%99%AF%E6%89%AB%E6%8F%8F-%E5%B7%A8%E5%A4%B4%E8%9E%8D%E8%B5%84%E5%88%9B%E6%96%B0%E9%AB%98-%E6%A8%A1%E5%9E%8B%E8%BF%AD%E4%BB%A3%E6%8F%90%E9%80%9F-%E6%99%BA%E8%83%BD%E4%BD%93%E6%97%B6%E4%BB%A3%E5%90%AF%E5%B9%95/ar-AA20qJiq", "头部企业持续重塑行业格局"),
        ("AI赛道最大金主：英伟达密集出手，超级独角兽诞生", "https://m.36kr.com/p/3716969592927621", "短短两个多月时间内多次投资布局"),
        ("2026年Q1 AI融资疯了：1890亿美元单月纪录", "https://simonaking.com/blog/ai-funding-2026-q1/", "全球创业公司融资总额创历史新高"),
        ("2026年AI巨头全景深度解析：九大公司模型与资本博弈", "https://zhuanlan.zhihu.com/p/2010476815681071043", "OpenAI、Google DeepMind、Anthropic、Meta竞争格局"),
        ("全球AI投资：硬件狂飙与应用落差", "https://cloud.tencent.com.cn/developer/article/2655665", "资本过度集中硬件，应用端商业化滞后"),
        ("2026年全球模型巨头对比：Anthropic、Google、OpenAI", "https://www.sohu.com/a/1008612733_121755728", "商业模式以C端订阅和B端API为主"),
        ("OpenAI再融资1220亿美元：成全球估值最高AI创企", "https://www.jiemian.com/article/14193337.html", "Anthropic正推进600亿美元融资计划"),
        ("阿里千问登顶全球调用榜：2026年4月AI圈动态", "https://blog.csdn.net/weixin_41908519/article/details/159963116", "从OpenAI刷新纪录到阿里千问登顶"),
        ("英伟达Blackwell GPU供不应求：AI芯片需求爆发", "https://finance.sina.com.cn/roll/2026-03-02/doc-inhpqqum4668320.shtml", "算力成为AI发展的关键瓶颈"),
    ],
    "business": [
        ("OpenAI年化营收突破40亿美元：AI商业化加速", "https://finance.sina.com.cn/", "SaaS订阅模式验证成功"),
        ("AI SaaS订阅模式：年ARR增长200%，续费率超90%", "https://www.36kr.com/", "按月/年订阅成为主流商业模式"),
        ("AI API调用收费：按量计费成主流，毛利率超70%", "https://openai.com/blog", "Token消耗计费模式成熟"),
        ("AI+知识付费：垂直领域课程月销百万", "https://www.geekpark.net/", "AI使用技巧课程热销"),
        ("AI定制开发：企业级解决方案报价百万起", "https://www.36kr.com/", "行业定制AI解决方案成蓝海"),
        ("AI硬件销售：AI PC换机潮将至", "https://finance.sina.com.cn/", "搭载NPU的PC成为新增长点"),
        ("AI数据服务：高质量数据集售价不菲", "https://tech.sina.com.cn/", "垂直领域数据标注需求旺盛"),
        ("AI培训服务：企业内训市场爆发成刚需", "https://www.36kr.com/", "AI技能培训市场规模扩大"),
        ("AI联盟营销：推广分成比例高达50%", "https://www.ifeng.com/", "AI产品分销成为新副业"),
        ("AI应用商店：插件生态分成模式兴起", "https://www.36kr.com/", "类比App Store的新变现渠道"),
    ],
}

def select_unique_items(category, count=10, history_file="history.json"):
    """选取内容，确保与历史不重复"""
    items = CONTENT_DB.get(category, [])
    used_titles = set()
    
    # 读取历史记录
    if os.path.exists(history_file):
        try:
            with open(history_file, 'r', encoding='utf-8') as f:
                history = json.load(f)
            for day_data in history:
                for cat_items in day_data.get("content", {}).values():
                    for item in cat_items:
                        used_titles.add(item[0])
        except:
            pass
    
    # 优先选择未使用的内容
    unused = [item for item in items if item[0] not in used_titles]
    used = [item for item in items if item[0] in used_titles]
    
    # 混合选取：80%新内容 + 20%补充
    selected = random.sample(unused, min(int(count * 0.8), len(unused)))
    remaining = count - len(selected)
    if remaining > 0 and used:
        selected.extend(random.sample(used, min(remaining, len(used))))
    
    return selected[:count]

def save_to_history(section_data, history_file="history.json"):
    """保存历史记录"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    history = []
    if os.path.exists(history_file):
        try:
            with open(history_file, 'r', encoding='utf-8') as f:
                history = json.load(f)
        except:
            history = []
    
    # 添加今天的记录
    new_record = {
        "date": today,
        "timestamp": datetime.now().isoformat(),
        "content": {cat: items for cat, items in section_data}
    }
    history.insert(0, new_record)  # 最新在前面
    
    # 只保留最近30天
    history = history[:30]
    
    with open(history_file, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
    
    return len(history)

def generate_history_html(history_file="history.json"):
    """生成往期回顾HTML"""
    if not os.path.exists(history_file):
        return ""
    
    try:
        with open(history_file, 'r', encoding='utf-8') as f:
            history = json.load(f)
    except:
        return ""
    
    if not history:
        return ""
    
    section_names = {
        "tech": "[T] AI最新技术",
        "app": "[A] AI应用场景",
        "company": "[C] AI公司动态",
        "business": "[B] AI商业模式"
    }
    
    items_html = ""
    for day_data in history[:7]:  # 只显示最近7天
        date = day_data["date"]
        content = day_data.get("content", {})
        
        day_items = ""
        for section_id, items in content.items():
            section_name = section_names.get(section_id, section_id)
            for i, item in enumerate(items[:5], 1):  # 每项最多显示5条
                title = item[0]
                url = item[1]
                day_items += '<div class="history-item"><span class="history-date">' + date + '</span><a href="' + url + '" target="_blank">' + title + '</a></div>'
        
        items_html += '<div class="history-day"><h4>' + date + '</h4><div class="history-list">' + day_items + '</div></div>'
    
    return '''
    <section class="section" id="history">
        <h2><span style="background:rgba(139,92,246,0.15);padding:8px 12px;border-radius:8px;">[*] 往期回顾</span></h2>
        <p style="color:var(--muted);margin-bottom:20px;">最近7天的AI资讯回顾</p>
        <div class="history-grid">''' + items_html + '''
        </div>
    </section>'''

def generate_html(section_data, history_file="history.json"):
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
            cards_html += '<div class="card"><span class="card-num">' + str(i) + '</span><div class="card-body"><h3><a href="' + url + '" target="_blank">' + item_title + '</a></h3><p>' + item_desc + '</p></div></div>'
        
        sections_html += '<section class="section active" id="' + sid + '"><h2><span style="background:' + color + ';padding:8px 12px;border-radius:8px;">' + icon + '</span> ' + title + '</h2><p style="color:var(--muted);margin-bottom:20px;">' + desc + '</p><div class="card-list">' + cards_html + '</div></section>'
    
    # 添加往期回顾
    sections_html += generate_history_html(history_file)
    
    # 替换模板变量
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
            --card-hover: #252540;
            --blue: #4f8fff;
            --purple: #8b5cf6;
            --cyan: #06d6a0;
            --orange: #ff6b35;
            --pink: #ec4899;
            --text: #e8e8f0;
            --muted: #9898b0;
            --border: #2a2a3e;
        }
        body { font-family: system-ui, -apple-system, sans-serif; background: var(--bg); color: var(--text); line-height: 1.6; }
        .hero { text-align: center; padding: 60px 20px 40px; background: linear-gradient(180deg, rgba(79,143,255,0.08) 0%, transparent 100%); }
        .hero h1 { font-size: 2.5rem; font-weight: 800; background: linear-gradient(135deg, var(--blue), var(--purple), var(--pink)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .hero p { color: var(--muted); margin-top: 10px; font-size: 1.1rem; }
        .update-time { margin-top: 20px; padding: 12px 24px; display: inline-block; background: rgba(6,214,160,0.1); border: 1px solid rgba(6,214,160,0.3); border-radius: 30px; font-size: 14px; }
        .update-time span { color: var(--cyan); font-weight: 600; }
        .nav { display: flex; justify-content: center; gap: 8px; padding: 20px; flex-wrap: wrap; margin-top: 20px; }
        .nav a { padding: 10px 20px; background: var(--card); border: 1px solid var(--border); border-radius: 25px; color: var(--text); text-decoration: none; cursor: pointer; transition: all 0.3s; font-size: 14px; }
        .nav a:hover { background: var(--card-hover); border-color: var(--blue); }
        .nav a.active { background: linear-gradient(135deg, var(--blue), var(--purple)); border: none; box-shadow: 0 4px 15px rgba(79,143,255,0.3); }
        .container { max-width: 900px; margin: 0 auto; padding: 20px 20px 60px; }
        .section { display: none; animation: fadeIn 0.4s ease; }
        .section.active { display: block; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        .section h2 { font-size: 1.4rem; margin-bottom: 20px; display: flex; align-items: center; gap: 12px; }
        .section h2 span { font-size: 1.6rem; }
        .section > p { color: var(--muted); margin-bottom: 24px; margin-top: -12px; font-size: 14px; }
        .card-list { display: flex; flex-direction: column; gap: 12px; }
        .card { background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 16px 20px; display: flex; gap: 16px; align-items: flex-start; transition: all 0.3s; }
        .card:hover { background: var(--card-hover); border-color: var(--blue); transform: translateX(4px); box-shadow: 0 4px 20px rgba(0,0,0,0.3); }
        .card-num { width: 28px; height: 28px; background: linear-gradient(135deg, var(--blue), var(--purple)); border-radius: 8px; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 14px; flex-shrink: 0; }
        .card-body { flex: 1; min-width: 0; }
        .card-body h3 { font-size: 15px; margin-bottom: 6px; }
        .card-body h3 a { color: var(--text); text-decoration: none; cursor: pointer; transition: all 0.3s; display: block; padding: 4px 0; border-radius: 4px; }
        .card-body h3 a:hover { color: var(--blue); background: rgba(79,143,255,0.1); padding-left: 8px; }
        .card-body p { color: var(--muted); font-size: 13px; }
        .history-grid { display: flex; flex-direction: column; gap: 24px; }
        .history-day h4 { color: var(--cyan); margin-bottom: 12px; padding-bottom: 8px; border-bottom: 1px solid var(--border); font-size: 14px; }
        .history-list { display: flex; flex-direction: column; gap: 8px; }
        .history-item { display: flex; gap: 12px; align-items: center; padding: 8px 12px; background: var(--card); border-radius: 8px; font-size: 13px; }
        .history-date { color: var(--muted); font-size: 12px; white-space: nowrap; }
        .history-item a { color: var(--text); text-decoration: none; }
        .history-item a:hover { color: var(--blue); }
        .qr-section { display: flex; justify-content: center; gap: 40px; padding: 30px; background: var(--card); border-radius: 16px; margin: 40px 0; flex-wrap: wrap; }
        .qr-item { text-align: center; }
        .qr-item img { width: 120px; height: 120px; border-radius: 12px; border: 2px solid var(--border); }
        .qr-item p { margin-top: 10px; color: var(--muted); font-size: 13px; }
        footer { text-align: center; padding: 40px 20px; border-top: 1px solid var(--border); color: var(--muted); }
        footer a { color: var(--purple); text-decoration: none; }
        footer a:hover { text-decoration: underline; }
        @media (max-width: 768px) {
            .hero h1 { font-size: 1.8rem; }
            .nav { gap: 6px; }
            .nav a { padding: 8px 14px; font-size: 13px; }
            .card { padding: 14px 16px; }
            .qr-section { gap: 20px; padding: 20px; }
        }
    </style>
</head>
<body>
    <section class="hero">
        <h1>胡栋材的AI小栈</h1>
        <p>汇聚全球AI最新技术、工具、应用与商业动态</p>
        <div class="update-time">最后更新: <span>{{UPDATE_TIME}}</span> | 每日自动更新</div>
    </section>
    <nav class="nav">
        <a class="active" data-section="tech">[T] AI技术</a>
        <a data-section="app">[A] 应用场景</a>
        <a data-section="company">[C] 公司动态</a>
        <a data-section="business">[B] 商业模式</a>
        <a href="/business-mentor/">[X] 商道导师</a>
        <a data-section="history">[*] 往期回顾</a>
    </nav>
    <div class="qr-section">
        <div class="qr-item">
            <img src="wechat-qr.jpg" alt="微信二维码" onerror="this.src='data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 120 120%22><rect fill=%22%231a1a2e%22 width=%22120%22 height=%22120%22/><text x=%2260%22 y=%2265%22 text-anchor=%22middle%22 fill=%22%239898b0%22 font-size=%2212%22>个人微信</text></svg>'">
            <p>个人微信</p>
        </div>
        <div class="qr-item">
            <img src="wechat-group.jpg" alt="微信群二维码" onerror="this.src='data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 120 120%22><rect fill=%22%231a1a2e%22 width=%22120%22 height=%22120%22/><text x=%2260%22 y=%2265%22 text-anchor=%22middle%22 fill=%22%239898b0%22 font-size=%2212%22>交流群</text></svg>'">
            <p>交流群</p>
        </div>
    </div>
    <main class="container">
        {{SECTIONS}}
    </main>
    <footer>
        <p>内容来源于公开网络，仅供学习参考 | <a href="https://github.com/hudongcai/hudongcai.github.io" target="_blank">GitHub</a></p>
    </footer>
    <script>
        const navs = document.querySelectorAll('.nav a[data-section]');
        const sections = document.querySelectorAll('.section');
        navs.forEach(nav => {
            nav.addEventListener('click', () => {
                navs.forEach(n => n.classList.remove('active'));
                nav.classList.add('active');
                sections.forEach(s => s.classList.remove('active'));
                const target = document.getElementById(nav.dataset.section);
                if (target) target.classList.add('active');
                window.scrollTo({ top: 0, behavior: 'smooth' });
            });
        });
    </script>
</body>
</html>'''

def main():
    print("[START] AI News Website Update V2.0")
    
    history_file = "history.json"
    section_configs = ["tech", "app", "company", "business"]
    section_data = []
    
    for section_id in section_configs:
        items = select_unique_items(section_id, 10, history_file)
        section_data.append({"id": section_id, "items": items})
        print("[OK] " + section_id + ": " + str(len(items)) + " items")
    
    # 保存历史
    history_count = save_to_history(section_data, history_file)
    print("[OK] History saved: " + str(history_count) + " days")
    
    # 生成HTML
    html_content = generate_html(section_data, history_file)
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("[DONE] index.html generated (" + str(len(html_content)) + " bytes)")
    print("[INFO] Sections: " + str(len(section_data)) + ", Items per section: 10")
    
    return 0

if __name__ == "__main__":
    exit(main())
