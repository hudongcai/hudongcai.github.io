# 大秦无人机周报生成器

## 快速开始

### 方式一：一键生成（推荐）

双击 `新建周报.bat` → 自动生成下一期框架

### 方式二：完整流程（生成框架 + AI搜集内容 + 回填）

1. **生成框架**
   ```bash
   python generate_weekly.py
   ```

2. **在WorkBuddy中搜集内容**
   ```
   「搜集最近一周的低空经济资讯，生成完整的第X期周报内容」
   ```

3. **保存内容为JSON**
   ```json
   {
     "theme": "本期主题",
     "sections": {
       "01": [
         {
           "title": "标题",
           "desc": "摘要",
           "url": "链接",
           "source": "来源",
           "section_title": "政策新规"
         }
       ]
     }
   }
   ```

4. **内容回填**
   ```bash
   python fill_content.py 3 week-003-data.json
   ```

## 文件说明

| 文件 | 说明 |
|------|------|
| `generate_weekly.py` | 新期生成脚本（生成框架） |
| `fill_content.py` | 内容回填脚本（填充真实内容） |
| `新建周报.bat` | 双击启动脚本（Windows） |

## 参数选项

```bash
# generate_weekly.py
python generate_weekly.py --auto       # 自动模式
python generate_weekly.py --commit     # 自动git commit
python generate_weekly.py --push       # 自动git commit + push
python generate_weekly.py --no-content # 仅生成框架（跳过内容搜集提示）
```

## 六大板块搜索关键词

| 板块 | 推荐关键词 |
|------|-----------|
| **01 政策新规** | 低空经济 政策 2026、无人机 空域开放、民航局 新规 |
| **02 市场商机** | 无人机 招标 采购、低空经济 项目签约、市场规模 |
| **03 产品技术** | 无人机 新品 发布、技术突破、电池 续航 |
| **04 应用案例** | 无人机 应用案例、巡检 应用、应急救援 |
| **05 标准规范** | 无人机 标准 规范、适航认证、合规 |
| **06 热点新闻** | 无人机 展会 活动、企业 动态、重大事件 |

## 完整工作流示例

```
第1步：生成框架
  双击 新建周报.bat
  → 生成 week/week-004.html（占位内容）
  → 更新 index.html（添加第4期卡片）

第2步：AI搜集内容
  在WorkBuddy中说：
  「搜集最近一周低空经济资讯，生成完整第4期周报内容」

第3步：准备JSON
  将AI返回的内容整理保存为 week-004-data.json

第4步：内容回填
  python fill_content.py 4 week-004-data.json

第5步：发布
  git add .
  git commit -m "周报第4期：XXXX"
  git push
```
