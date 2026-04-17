#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI小栈网站内容更新脚本 V3.0
- 3大模块：AI工具、AI资讯、AI商业
- AI工具：收录热门AI工具的名称、网址、简介
- AI资讯：技术动态、应用场景、公司消息
- AI商业：商道导师商业案例
"""

import random
import json
import os
from datetime import datetime

# ========== AI工具库（分门别类） ==========
AI_TOOLS_BY_CATEGORY = {
    "💬 对话AI": [
        ("ChatGPT", "https://chat.openai.com", "OpenAI开发的大语言模型，支持对话、写作、编程等多种场景"),
        ("Claude", "https://claude.ai", "Anthropic推出的AI助手，擅长长文本分析和创意写作"),
        ("Gemini", "https://gemini.google.com", "Google推出的多模态AI助手"),
        ("DeepSeek", "https://chat.deepseek.com", "国产开源大模型，性价比高，支持深度推理"),
        ("Kimi", "https://kimi.moonshot.cn", "月之暗面推出的AI助手，支持超长上下文"),
        ("文心一言", "https://yiyan.baidu.com", "百度推出的国产大语言模型，中文能力强"),
        ("通义千问", "https://tongyi.aliyun.com", "阿里云推出的大语言模型，支持多轮对话"),
        ("讯飞星火", "https://xinghuo.xfyun.cn", "科大讯飞推出的认知大模型"),
        ("智谱清言", "https://www.zhipuai.cn", "智谱AI推出的对话助手"),
    ],
    "🎨 图像生成": [
        ("Midjourney", "https://www.midjourney.com", "AI图像生成工具，支持艺术风格创作"),
        ("Stable Diffusion", "https://stability.ai", "开源AI图像生成模型，可本地部署"),
        ("DALL-E", "https://openai.com/dall-e-3", "OpenAI推出的AI绘图工具"),
        ("Adobe Firefly", "https://firefly.adobe.com", "Adobe推出的AI图像生成工具"),
        ("Ideogram", "https://ideogram.ai", "AI图像生成，支持文字渲染"),
        ("Leonardo.ai", "https://leonardo.ai", "游戏和创意领域的AI图像生成"),
    ],
    "🎬 视频制作": [
        ("Runway", "https://runwayml.com", "AI视频生成和编辑平台"),
        ("Sora", "https://openai.com/sora", "OpenAI推出的AI视频生成模型"),
        ("Pika", "https://pika.art", "AI视频生成新兴力量"),
        ("HeyGen", "https://heygen.com", "AI数字人视频制作"),
        ("剪映", "https://www.capcut.cn", "字节跳动AI视频剪辑工具"),
    ],
    "💻 编程开发": [
        ("GitHub Copilot", "https://github.com/features/copilot", "GitHub推出的AI编程助手"),
        ("Cursor", "https://cursor.sh", "AI代码编辑器，集成GPT-4"),
        ("Codeium", "https://codeium.com", "免费AI编程助手"),
        ("Tabnine", "https://tabnine.com", "AI代码补全工具"),
        ("Replit", "https://replit.com", "AI驱动的在线编程平台"),
    ],
    "📝 写作办公": [
        ("Notion AI", "https://notion.so", "笔记工具的AI助手，支持写作和整理"),
        ("Gamma", "https://gamma.app", "AI幻灯片生成工具"),
        ("Beautiful.ai", "https://www.beautiful.ai", "AI驱动的演示文稿设计工具"),
        ("Canva AI", "https://www.canva.com", "设计平台的AI功能集成"),
        ("飞书妙记", "https://www.feishu.cn", "字节跳动AI会议记录工具"),
    ],
    "📢 内容营销": [
        ("Jasper", "https://www.jasper.ai", "AI营销内容生成工具"),
        ("Copy.ai", "https://www.copy.ai", "AI文案写作工具"),
        ("Writesonic", "https://writesonic.com", "AI内容创作平台"),
        ("Rytr", "https://rytr.me", "AI写作助手，性价比高"),
    ],
    "🔍 搜索研究": [
        ("Perplexity", "https://www.perplexity.ai", "AI搜索引擎，结合实时信息"),
        ("Consensus", "https://consensus.app", "AI学术论文搜索引擎"),
        ("Elicit", "https://elicit.org", "AI研究助手，辅助文献综述"),
    ],
    "🎭 创意娱乐": [
        ("Character.AI", "https://character.ai", "AI角色扮演对话平台"),
        ("Pi AI", "https://pi.ai", "Inflection推出的个人AI助手"),
        ("Poe", "https://poe.com", "Quora推出的AI聊天聚合平台"),
        ("Suno", "https://suno.ai", "AI音乐生成工具"),
    ],
}

# 扁平化列表（保持兼容性）
AI_TOOLS = []
for tools in AI_TOOLS_BY_CATEGORY.values():
    AI_TOOLS.extend(tools)

# ========== AI资讯库 ==========
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
        ("2026年4月AI行业全景扫描：巨头融资创新高", "https://www.msn.cn/zh-cn/%E6%8A%80%E6%9C%AF/%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD/2026%E5%B9%B44%E6%9C%88ai%E8%A1%8C%E4%B8%9A%E5%85%A8%E6%99%AF%E6%89%AB%E6%8F%8F-%E5%B7%82%E5%A4%B4%E8%9E%8D%E8%B5%84%E5%88%9B%E6%96%B0%E9%AB%98-%E6%A8%A1%E5%9E%8B%E8%BF%AD%E4%BB%A3%E6%8F%90%E9%80%9F-%E6%99%BA%E8%83%BD%E4%BD%93%E6%97%B6%E4%BB%A3%E5%90%AF%E5%B9%95/ar-AA20qJiq", "头部企业持续重塑行业格局"),
        ("AI赛道最大金主：英伟达密集出手，超级独角兽诞生", "https://m.36kr.com/p/3716969592927621", "短短两个多月时间内多次投资布局"),
        ("2026年Q1 AI融资疯了：1890亿美元单月纪录", "https://simonaking.com/blog/ai-funding-2026-q1/", "全球创业公司融资总额创历史新高"),
        ("2026年AI巨头全景深度解析：九大公司模型与资本博弈", "https://zhuanlan.zhihu.com/p/2010476815681071043", "OpenAI、Google DeepMind、Anthropic、Meta竞争格局"),
        ("全球AI投资：硬件狂飙与应用落差", "https://cloud.tencent.com.cn/developer/article/2655665", "资本过度集中硬件，应用端商业化滞后"),
        ("2026年全球模型巨头对比：Anthropic、Google、OpenAI", "https://www.sohu.com/a/1008612733_121755728", "商业模式以C端订阅和B端API为主"),
        ("OpenAI再融资1220亿美元：成全球估值最高AI创企", "https://www.jiemian.com/article/14193337.html", "Anthropic正推进600亿美元融资计划"),
        ("阿里千问登顶全球调用榜：2026年4月AI圈动态", "https://blog.csdn.net/weixin_41908519/article/details/159963116", "从OpenAI刷新纪录到阿里千问登顶"),
        ("英伟达Blackwell GPU供不应求：AI芯片需求爆发", "https://finance.sina.com.cn/roll/2026-03-02/doc-inhpqqum4668320.shtml", "算力成为AI发展的关键瓶颈"),
    ],
}

def get_ai_news(count=10, history_file="history.json"):
    """获取AI资讯，合并tech/app/company三个板块"""
    all_news = []
    for category in ["tech", "app", "company"]:
        all_news.extend(CONTENT_DB.get(category, []))
    
    # 读取历史，避免重复
    used_titles = set()
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
    
    # 去重
    unused = [item for item in all_news if item[0] not in used_titles]
    used = [item for item in all_news if item[0] in used_titles]
    
    # 优先新内容
    selected = random.sample(unused, min(int(count * 0.8), len(unused)))
    remaining = count - len(selected)
    if remaining > 0 and used:
        selected.extend(random.sample(used, min(remaining, len(used))))
    
    return selected[:count]

def save_to_history(content_data, history_file="history.json"):
    """保存历史记录"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    history = []
    if os.path.exists(history_file):
        try:
            with open(history_file, 'r', encoding='utf-8') as f:
                history = json.load(f)
        except:
            history = []
    
    new_record = {
        "date": today,
        "timestamp": datetime.now().isoformat(),
        "content": content_data
    }
    history.insert(0, new_record)
    history = history[:30]  # 保留30天
    
    with open(history_file, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
    
    return len(history)

def generate_html(ai_tools_by_category, ai_news, history_file="history.json"):
    today = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # 生成工具卡片（按分类）
    tools_html = ""
    category_colors = {
        "💬 对话AI": "linear-gradient(135deg, #4f8fff, #8b5cf6)",
        "🎨 图像生成": "linear-gradient(135deg, #ec4899, #f472b6)",
        "🎬 视频制作": "linear-gradient(135deg, #ff6b35, #fbbf24)",
        "💻 编程开发": "linear-gradient(135deg, #06d6a0, #10b981)",
        "📝 写作办公": "linear-gradient(135deg, #8b5cf6, #a78bfa)",
        "📢 内容营销": "linear-gradient(135deg, #f59e0b, #fbbf24)",
        "🔍 搜索研究": "linear-gradient(135deg, #3b82f6, #60a5fa)",
        "🎭 创意娱乐": "linear-gradient(135deg, #ec4899, #f9a8d4)",
    }
    
    for cat_name, tools in ai_tools_by_category.items():
        cat_color = category_colors.get(cat_name, "linear-gradient(135deg, #4f8fff, #8b5cf6)")
        tools_html += '<div class="tool-category"><h3 class="cat-title" style="background:' + cat_color + ';">' + cat_name + ' (' + str(len(tools)) + ')</h3><div class="tool-grid">'
        for tool_name, tool_url, tool_desc in tools:
            tools_html += '<div class="tool-card"><h4><a href="' + tool_url + '" target="_blank">' + tool_name + '</a></h4><p>' + tool_desc + '</p><a href="' + tool_url + '" target="_blank" class="tool-link">访问网站</a></div>'
        tools_html += '</div></div>'
    
    # 生成资讯卡片
    news_html = ""
    for i, (news_title, news_url, news_desc) in enumerate(ai_news, 1):
        news_html += '<div class="card"><span class="card-num">' + str(i) + '</span><div class="card-body"><h3><a href="' + news_url + '" target="_blank">' + news_title + '</a></h3><p>' + news_desc + '</p></div></div>'
    
    # 生成往期回顾
    history_html = ""
    if os.path.exists(history_file):
        try:
            with open(history_file, 'r', encoding='utf-8') as f:
                history = json.load(f)
            
            if history:
                history_items = ""
                for day_data in history[:7]:
                    date = day_data["date"]
                    content = day_data.get("content", {})
                    news_items = content.get("news", [])
                    for item in news_items[:3]:
                        history_items += '<div class="history-item"><span class="history-date">' + date + '</span><a href="' + item[1] + '" target="_blank">' + item[0] + '</a></div>'
                
                if history_items:
                    history_html = '''
        <section class="section" id="history">
            <h2><span style="background:rgba(139,92,246,0.15);padding:8px 12px;border-radius:8px;">[*]</span> 往期回顾</h2>
            <p style="color:var(--muted);margin-bottom:20px;">最近7天的AI资讯回顾</p>
            <div class="history-list">''' + history_items + '''
            </div>
        </section>'''
        except:
            pass
    
    # HTML模板
    html = '''<!DOCTYPE html>
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
        .container { max-width: 1100px; margin: 0 auto; padding: 20px 20px 60px; }
        .section { display: none; animation: fadeIn 0.4s ease; }
        .section.active { display: block; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        
        /* AI工具模块 */
        .section h2 { font-size: 1.4rem; margin-bottom: 12px; display: flex; align-items: center; gap: 12px; }
        .section h2 span { font-size: 1.6rem; }
        .section > p { color: var(--muted); margin-bottom: 24px; font-size: 14px; }
        .tool-category { margin-bottom: 32px; }
        .cat-title { display: inline-block; padding: 10px 20px; border-radius: 25px; font-size: 15px; font-weight: 600; color: white; margin-bottom: 16px; }
        .tool-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 16px; }
        .tool-card { background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 20px; transition: all 0.3s; }
        .tool-card:hover { background: var(--card-hover); border-color: var(--blue); transform: translateY(-4px); box-shadow: 0 8px 25px rgba(0,0,0,0.3); }
        .tool-card h4 { font-size: 16px; margin-bottom: 8px; }
        .tool-card h4 a { color: var(--text); text-decoration: none; cursor: pointer; transition: color 0.3s; }
        .tool-card h4 a:hover { color: var(--blue); }
        .tool-card p { color: var(--muted); font-size: 13px; margin-bottom: 12px; }
        .tool-link { display: inline-block; padding: 6px 14px; background: linear-gradient(135deg, var(--blue), var(--purple)); border-radius: 20px; color: white; text-decoration: none; font-size: 13px; transition: all 0.3s; }
        .tool-link:hover { transform: scale(1.05); box-shadow: 0 4px 15px rgba(79,143,255,0.4); }
        
        /* AI资讯模块 */
        .card-list { display: flex; flex-direction: column; gap: 12px; }
        .card { background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 16px 20px; display: flex; gap: 16px; align-items: flex-start; transition: all 0.3s; }
        .card:hover { background: var(--card-hover); border-color: var(--blue); transform: translateX(4px); box-shadow: 0 4px 20px rgba(0,0,0,0.3); }
        .card-num { width: 28px; height: 28px; background: linear-gradient(135deg, var(--blue), var(--purple)); border-radius: 8px; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 14px; flex-shrink: 0; }
        .card-body { flex: 1; min-width: 0; }
        .card-body h3 { font-size: 15px; margin-bottom: 6px; }
        .card-body h3 a { color: var(--text); text-decoration: none; cursor: pointer; transition: all 0.3s; display: block; padding: 4px 0; border-radius: 4px; }
        .card-body h3 a:hover { color: var(--blue); background: rgba(79,143,255,0.1); padding-left: 8px; }
        .card-body p { color: var(--muted); font-size: 13px; }
        
        /* 往期回顾 */
        .history-list { display: flex; flex-direction: column; gap: 8px; }
        .history-item { display: flex; gap: 12px; align-items: center; padding: 8px 12px; background: var(--card); border-radius: 8px; font-size: 13px; }
        .history-date { color: var(--muted); font-size: 12px; white-space: nowrap; }
        .history-item a { color: var(--text); text-decoration: none; }
        .history-item a:hover { color: var(--blue); }
        
        /* 二维码区域 */
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
            .tool-grid { grid-template-columns: 1fr; }
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
        <a class="active" data-section="tools">[1] AI工具</a>
        <a data-section="news">[2] AI资讯</a>
        <a href="/business-mentor/">[3] AI商业</a>
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
        <section class="section active" id="tools">
            <h2><span style="background:rgba(79, 143, 255, 0.15);padding:8px 12px;border-radius:8px;">[1]</span> AI工具集</h2>
            <p>收录主流AI工具，名称、网址、简介一目了然</p>
            <div class="tool-grid">{{TOOLS}}</div>
        </section>
        <section class="section" id="news">
            <h2><span style="background:rgba(6, 214, 160, 0.15);padding:8px 12px;border-radius:8px;">[2]</span> AI资讯</h2>
            <p>每日精选AI技术动态、应用场景、公司消息</p>
            <div class="card-list">{{NEWS}}</div>
        </section>
        {{HISTORY}}
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
    
    # 替换变量
    html = html.replace("{{UPDATE_TIME}}", today)
    html = html.replace("{{TOOLS}}", tools_html)
    html = html.replace("{{NEWS}}", news_html)
    html = html.replace("{{HISTORY}}", history_html)
    
    return html

def main():
    print("[START] AI News Website Update V3.0")
    
    history_file = "history.json"
    
    # 获取AI工具（分门别类）
    ai_tools_by_category = AI_TOOLS_BY_CATEGORY
    
    # 获取AI资讯
    ai_news = get_ai_news(count=10, history_file=history_file)
    
    # 保存历史
    content_data = {"news": ai_news}
    history_count = save_to_history(content_data, history_file)
    total_tools = sum(len(tools) for tools in ai_tools_by_category.values())
    print("[OK] AI Tools: " + str(total_tools) + " items (" + str(len(ai_tools_by_category)) + " categories)")
    print("[OK] AI News: " + str(len(ai_news)) + " items")
    print("[OK] History saved: " + str(history_count) + " days")
    
    # 生成HTML
    html_content = generate_html(ai_tools_by_category, ai_news, history_file)
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("[DONE] index.html generated (" + str(len(html_content)) + " bytes)")

if __name__ == "__main__":
    exit(main())
