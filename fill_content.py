#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大秦无人机低空周报 - 内容回填脚本
将搜集到的资讯填入已有的HTML框架

用法：
  python fill_content.py <期数> <内容JSON文件>

示例：
  python fill_content.py 3 week-003-data.json
"""

import os
import re
import sys
import json
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
WEEK_DIR = SCRIPT_DIR / "week"

# 六大板块ID映射
SECTION_IDS = ["01", "02", "03", "04", "05", "06"]


def load_content_json(json_file):
    """加载内容JSON"""
    with open(json_file, "r", encoding="utf-8") as f:
        return json.load(f)


def create_content_items(items):
    """生成内容条目HTML"""
    html = ""
    for item in items:
        html += f'''
      <div class="content-item">
        <h3 class="content-title"><a href="{item["url"]}" target="_blank">{item["title"]}</a></h3>
        <p class="content-desc">{item["desc"]}</p>
        <p class="content-source">来源：<a href="{item["url"]}" target="_blank">{item["source"]}</a></p>
      </div>'''
    return html


def fill_html_content(html_file, content_data):
    """填充HTML内容"""
    content = html_file.read_text(encoding="utf-8")

    # 更新主题
    if "theme" in content_data:
        content = re.sub(
            r'🔥 本期主题：[^<]+',
            f'🔥 本期主题：{content_data["theme"]}',
            content
        )

    # 填充各板块
    if "sections" in content_data:
        for section_id in SECTION_IDS:
            if section_id not in content_data["sections"]:
                continue

            items = content_data["sections"][section_id]
            if not items:
                continue

            items_html = create_content_items(items)

            # 查找并替换该板块内容
            section_pattern = re.compile(
                rf'      <!-- {section_id} [^>]+ -->\n'
                r'      <div class="content-section">\n'
                r'        <h2 class="section-title">[^<]+</h2>\n'
                r'        <div class="content-list">.*?</div>\n'
                r'      </div>',
                re.DOTALL
            )

            new_section_html = f'''      <!-- {section_id} {items[0].get("section_title", "")} -->
      <div class="content-section">
        <h2 class="section-title"><span class="num">{section_id}</span> {items[0].get("section_title", "")}</h2>
        <div class="content-list">{items_html}
        </div>
      </div>'''

            content = section_pattern.sub(new_section_html, content)

    html_file.write_text(content, encoding="utf-8")


def main():
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    if len(sys.argv) < 3:
        print("=" * 60)
        print("  大秦无人机低空周报 - 内容回填工具")
        print("=" * 60)
        print()
        print("  用法：")
        print("    python fill_content.py <期数> <内容JSON文件>")
        print()
        print("  示例：")
        print("    python fill_content.py 3 week-003-data.json")
        print()
        print("  内容JSON格式：")
        print('''    {
      "theme": "本期主题",
      "sections": {
        "01": [
          {
            "title": "标题",
            "desc": "摘要",
            "url": "链接",
            "source": "来源"
          }
        ]
      }
    }''')
        return

    week_num = int(sys.argv[1])
    json_file = Path(sys.argv[2])

    week_file = WEEK_DIR / f"week-{week_num:03d}.html"

    print("=" * 60)
    print("  大秦无人机低空周报 - 内容回填")
    print("=" * 60)
    print()
    print(f"  📄 目标周报：{week_file.name}")
    print(f"  📊 内容来源：{json_file.name}")
    print()

    if not week_file.exists():
        print(f"❌ 周报文件不存在：{week_file}")
        return
    if not json_file.exists():
        print(f"❌ 内容文件不存在：{json_file}")
        return

    content_data = load_content_json(json_file)
    fill_html_content(week_file, content_data)

    print(f"✅ 内容已回填到：{week_file.name}")
    print()


if __name__ == "__main__":
    main()
