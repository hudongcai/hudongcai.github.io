#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大秦无人机低空周报 - 智能生成脚本
自动检测当前期数，搜索最近一周低空经济资讯，生成完整HTML并更新首页

用法：
  python generate_weekly.py              # 交互模式（默认）
  python generate_weekly.py --auto       # 自动模式（无需确认）
  python generate_weekly.py --commit     # 生成后自动 git commit（不push）
  python generate_weekly.py --push       # 生成后自动 git commit + push
  python generate_weekly.py --no-content # 仅生成框架，不搜集内容（旧模式）
"""

import os
import re
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime, timedelta

# ============ 配置 ============
SCRIPT_DIR = Path(__file__).resolve().parent
WEEK_DIR = SCRIPT_DIR / "week"
INDEX_FILE = SCRIPT_DIR / "index.html"

# 中文数字映射
CN_NUMBERS = {
    1: "一", 2: "二", 3: "三", 4: "四", 5: "五",
    6: "六", 7: "七", 8: "八", 9: "九", 10: "十",
    11: "十一", 12: "十二", 13: "十三", 14: "十四", 15: "十五",
    16: "十六", 17: "十七", 18: "十八", 19: "十九", 20: "二十",
    21: "二十一", 22: "二十二", 23: "二十三", 24: "二十四", 25: "二十五",
    26: "二十六", 27: "二十七", 28: "二十八", 29: "二十九", 30: "三十",
}

# 六大板块定义 + 搜索关键词
SECTIONS = [
    {
        "id": "01",
        "title": "政策新规",
        "desc": "国家/地方低空经济政策、法规、规划",
        "keywords": [
            "低空经济 政策 2026",
            "无人机 空域开放 新规",
            "民航局 无人机 政策",
            "地方 低空经济 规划"
        ]
    },
    {
        "id": "02",
        "title": "市场商机",
        "desc": "招标采购、项目合作、市场数据",
        "keywords": [
            "无人机 招标 采购",
            "低空经济 项目签约",
            "无人机 市场规模 2026",
            "无人机 订单 采购"
        ]
    },
    {
        "id": "03",
        "title": "产品技术",
        "desc": "无人机新品、技术突破、解决方案",
        "keywords": [
            "无人机 新品 发布 2026",
            "无人机 技术突破",
            "无人机 电池 续航",
            "无人机 解决方案"
        ]
    },
    {
        "id": "04",
        "title": "应用案例",
        "desc": "行业落地案例、示范项目、实战效果",
        "keywords": [
            "无人机 应用案例",
            "无人机 巡检 应用",
            "无人机 应急救援",
            "低空经济 示范项目"
        ]
    },
    {
        "id": "05",
        "title": "标准规范",
        "desc": "行业标准、适航认证、合规要求",
        "keywords": [
            "无人机 标准 规范",
            "无人机 适航认证",
            "低空经济 合规",
            "无人机 检测 认证"
        ]
    },
    {
        "id": "06",
        "title": "热点新闻",
        "desc": "行业大事、展会活动、企业动态",
        "keywords": [
            "无人机 展会 活动",
            "无人机 企业 动态",
            "低空经济 新闻",
            "无人机 重大事件"
        ]
    },
]

# ============ 核心函数 ============

def get_next_week_number():
    """检测当前最新期数，返回下一期编号"""
    if not WEEK_DIR.exists():
        return 1
    existing = sorted(WEEK_DIR.glob("week-*.html"))
    if not existing:
        return 1
    last = existing[-1].stem
    num = int(last.split("-")[1])
    return num + 1


def get_date_range():
    """获取最近一周的日期范围字符串"""
    today = datetime.now()
    week_ago = today - timedelta(days=7)
    return f"{week_ago.month}月{week_ago.day}日-{today.month}月{today.day}日"


def get_today_str():
    """获取当前日期字符串，格式：2026年05月25日"""
    now = datetime.now()
    return f"{now.year}年{now.month:02d}月{now.day:02d}日"


def generate_placeholder_items(section):
    """生成占位条目（仅用于无内容时）"""
    return f'''
      <div class="content-item">
        <h3 class="content-title"><a href="#" target="_blank">【待填写标题 - {section["desc"]}】</a></h3>
        <p class="content-desc">【待填写摘要】</p>
        <p class="content-source">来源：<a href="#" target="_blank">【待填写来源】</a></p>
      </div>'''


def generate_section_html(section, items=None):
    """生成单个板块的HTML"""
    items_html = ""
    if items:
        for item in items:
            items_html += f'''
      <div class="content-item">
        <h3 class="content-title"><a href="{item["url"]}" target="_blank">{item["title"]}</a></h3>
        <p class="content-desc">{item["desc"]}</p>
        <p class="content-source">来源：<a href="{item["url"]}" target="_blank">{item["source"]}</a></p>
      </div>'''
    else:
        items_html = generate_placeholder_items(section)

    return f'''
      <!-- {section["id"]} {section["title"]} -->
      <div class="content-section">
        <h2 class="section-title"><span class="num">{section["id"]}</span> {section["title"]}</h2>
        <div class="content-list">{items_html}
        </div>
      </div>'''


def generate_week_html(week_num, cn_number, date_str, content_data=None):
    """生成完整HTML"""
    # 确定本期主题
    theme = "低空经济一周动态"
    if content_data and "theme" in content_data:
        theme = content_data["theme"]

    # 生成各板块
    sections_html = ""
    for section in SECTIONS:
        items = None
        if content_data and "sections" in content_data:
            items = content_data["sections"].get(section["id"])
        sections_html += generate_section_html(section, items)

    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="大秦无人机低空周报（第{week_num}期）- {date_str}">
  <title>大秦无人机低空周报（第{week_num}期）</title>
  <link rel="stylesheet" href="../css/style.css">
  <!-- 不蒜子统计 -->
  <script async src="https://busuanzi.ibruce.info/busuanzi/2.3/busuanzi.pure.mini.js"></script>
</head>
<body>
  <!-- Header -->
  <header class="header">
    <div class="container">
      <div class="header-brand">
        <img src="../assets/logo-light.png" alt="大秦无人机" class="header-logo logo-light"><img src="../assets/logo.png" alt="大秦无人机" class="header-logo logo-dark">
        <h1 class="header-title">大秦无人机低空周报</h1>
        <div class="header-meta">
          <span>📅 更新日期：{date_str}</span>
        </div>
      </div>
    </div>
  </header>

  <!-- Main Content -->
  <main class="main">
    <div class="container">
      <!-- 周报标题区 -->
      <div class="week-header">
        <a href="../index.html" class="back-link">← 返回首页</a>
        <h1 class="week-title">大秦无人机低空周报（第{cn_number}期）</h1>
        <p class="week-theme">🔥 本期主题：{theme}</p>
        <div class="week-meta">
          <span>📅 {date_str}</span>
        </div>
      </div>
{sections_html}

      <!-- 访问统计 -->
      <div class="stats-section">
        <span id="busuanzi_container_page_pv">本文阅读量：<span id="busuanzi_value_page_pv">-</span> 次</span>
      </div>
    </div>
  </main>

  <!-- Fixed Footer -->
  <footer class="fixed-footer">
    <div class="footer-content">
      <div class="footer-brand">
        <img src="../assets/logo-light.png" alt="大秦无人机" class="footer-logo logo-light"><img src="../assets/logo.png" alt="大秦无人机" class="footer-logo logo-dark">
      </div>
      <div class="footer-links">
        <a href="https://kdocs.cn/join/gn3eyg3?f=101vln" target="_blank" class="footer-link">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
            <polyline points="14 2 14 8 20 8"/>
            <line x1="16" y1="13" x2="8" y2="13"/>
            <line x1="16" y1="17" x2="8" y2="17"/>
          </svg>
          售前弹药库
        </a>
        <a href="https://www.daqinuav.com/" target="_blank" class="footer-link">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/>
            <line x1="2" y1="12" x2="22" y2="12"/>
            <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>
          </svg>
          公司官网
        </a>
      </div>
      <div class="footer-brand">
        <span class="footer-slogan">西北领先的低空数字经济服务商</span>
      </div>
      <div class="footer-qr">
        <img src="../assets/wechat-qr.png" alt="微信二维码" class="footer-qr-img">
        <span class="footer-qr-text">添加微信</span>
      </div>
    </div>
  </footer>
</body>
</html>'''


def update_index_html(week_num, cn_number, date_str):
    """更新首页：添加新期数卡片 + 更新日期"""
    content = INDEX_FILE.read_text(encoding="utf-8")

    content = re.sub(
        r'📅 更新日期：\d{4}年\d{2}月\d{2}日',
        f'📅 更新日期：{date_str}',
        content
    )

    new_card = f'''        <a href="week/week-{week_num:03d}.html" class="week-card">
          <div class="week-card-number">{week_num:02d}</div>
          <div class="week-card-title">第{cn_number}期</div>
          <div class="week-card-arrow">→</div>
        </a>'''

    upcoming_pattern = re.compile(
        r'        <a href="#" class="week-card" style="opacity: 0\.5; cursor: not-allowed;">\n'
        r'          <div class="week-card-number">\d+</div>\n'
        r'          <div class="week-card-title">即将发布</div>\n'
        r'          <div class="week-card-arrow">🚧</div>\n'
        r'        </a>',
        re.MULTILINE
    )

    match = upcoming_pattern.search(content)
    if match:
        content = content[:match.start()] + new_card + content[match.end():]
    else:
        grid_end = content.find('      </div>\n\n      <!-- 访问统计 -->')
        if grid_end > 0:
            content = content[:grid_end] + new_card + '\n' + content[grid_end:]

    remaining_upcoming = len(upcoming_pattern.findall(content))
    cards_to_add = max(0, 4 - remaining_upcoming)

    for i in range(cards_to_add):
        next_placeholder_num = week_num + remaining_upcoming + i + 1
        placeholder_card = f'''        <a href="#" class="week-card" style="opacity: 0.5; cursor: not-allowed;">
          <div class="week-card-number">{next_placeholder_num:02d}</div>
          <div class="week-card-title">即将发布</div>
          <div class="week-card-arrow">🚧</div>
        </a>'''
        grid_end = content.find('      </div>\n\n      <!-- 访问统计 -->')
        if grid_end > 0:
            content = content[:grid_end] + placeholder_card + '\n' + content[grid_end:]

    INDEX_FILE.write_text(content, encoding="utf-8")


def git_commit(week_num, cn_number, has_content, push=False):
    """Git提交并可选推送"""
    try:
        subprocess.run(["git", "add", "."], cwd=SCRIPT_DIR, check=True, capture_output=True)

        status = "完整内容" if has_content else "新增框架（待填写内容）"
        commit_msg = f"周报第{week_num}期：{status}"
        subprocess.run(
            ["git", "commit", "-m", commit_msg],
            cwd=SCRIPT_DIR, check=True, capture_output=True
        )
        print(f"✅ Git 已提交：{commit_msg}")

        if push:
            subprocess.run(
                ["git", "push"],
                cwd=SCRIPT_DIR, check=True, capture_output=True
            )
            print("✅ Git 已推送到远程仓库")
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Git 操作失败：{e.stderr.decode('utf-8', errors='replace') if e.stderr else str(e)}")


def save_content_data(content_data, week_num):
    """保存内容数据到JSON（供调试/存档用）"""
    data_file = SCRIPT_DIR / "data" / f"week-{week_num:03d}.json"
    data_file.parent.mkdir(exist_ok=True)
    data_file.write_text(json.dumps(content_data, ensure_ascii=False, indent=2), encoding="utf-8")


def show_search_guide(week_num):
    """显示内容搜集指南"""
    date_range = get_date_range()
    print()
    print("=" * 60)
    print("  📚 下一步：在WorkBuddy中搜集内容")
    print("=" * 60)
    print()
    print(f"  请在WorkBuddy中输入以下指令：")
    print()
    print(f'  「搜集最近一周（{date_range}）的低空经济资讯，')
    print(f'   生成完整的第{week_num}期周报内容」')
    print()
    print("  或分板块搜索：")
    for section in SECTIONS:
        print(f"    {section['id']} {section['title']}:")
        print(f"      {section['keywords'][0]}")
    print()
    print("  💡 AI搜集内容后，可重新运行此脚本或手动填入HTML")
    print()


def main():
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    auto_mode = "--auto" in sys.argv
    do_commit = "--commit" in sys.argv
    do_push = "--push" in sys.argv
    no_content = "--no-content" in sys.argv

    print("=" * 60)
    print("  大秦无人机低空周报 - 智能生成器")
    print("=" * 60)
    print()

    week_num = get_next_week_number()
    cn_number = CN_NUMBERS.get(week_num, str(week_num))
    date_str = get_today_str()
    week_file = WEEK_DIR / f"week-{week_num:03d}.html"

    print(f"  📰 下一期：第 {week_num} 期（第{cn_number}期）")
    print(f"  📅 日期：{date_str}")
    print(f"  📄 文件：{week_file.name}")

    if week_file.exists():
        print(f"\n⚠️ 第{week_num}期已存在：{week_file}")
        if auto_mode:
            print("自动模式：跳过覆盖，退出。")
            return
        response = input("是否覆盖？(y/N): ").strip().lower()
        if response != 'y':
            print("已取消。")
            return

    if not auto_mode and not no_content:
        response = input(f"\n是否自动搜集内容？(Y/n): ").strip().lower()
        no_content = (response == 'n')

    if not auto_mode:
        response = input(f"\n确认生成第{cn_number}期周报？(Y/n): ").strip().lower()
        if response == 'n':
            print("已取消。")
            return

    WEEK_DIR.mkdir(exist_ok=True)

    if no_content:
        content_data = None
        print("\n⏭️ 跳过内容搜集，仅生成框架...")
    else:
        print("\n" + "=" * 60)
        print("  ⚠️  注意：Python脚本无法直接调用WebSearch工具")
        print("=" * 60)
        print("\n  解决方案：")
        print("  1. 此脚本先生成框架")
        print("  2. 然后在WorkBuddy中手动搜索内容")
        print("  3. 最后将内容填入HTML\n")

        if not auto_mode:
            input("按回车继续...")
        content_data = None

    html = generate_week_html(week_num, cn_number, date_str, content_data)
    week_file.write_text(html, encoding="utf-8")
    print(f"\n✅ 已生成：{week_file.name}")

    update_index_html(week_num, cn_number, date_str)
    print(f"✅ 已更新首页：index.html")

    if do_commit or do_push:
        git_commit(week_num, cn_number, has_content=(content_data is not None), push=do_push)

    print()
    print("=" * 60)
    print(f"  📰 第{cn_number}期周报已创建！")
    print("=" * 60)
    print()

    if no_content:
        print("  📝 接下来请：")
        print(f"     1. 打开 week/{week_file.name}")
        print("     2. 修改本期主题（替换「低空经济一周动态」）")
        print(f"     3. 为每个板块添加 3-5 条真实资讯")
        print(f"        每条包含：标题链接、摘要、来源")
        print(f"     4. 删除各板块的占位条目")
        if not do_push:
            print(f"     5. 完成后提交：")
            print(f"        git add .")
            print(f'        git commit -m "周报第{week_num}期：XXXX"')
            print(f"        git push")
        print()
    else:
        show_search_guide(week_num)


if __name__ == "__main__":
    main()
