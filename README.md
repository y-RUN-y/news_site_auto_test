# 腾讯新闻网页版自动化测试框架

基于 Python + pytest + Playwright 构建，采用页面对象模型（POM）设计，Pixi 管理依赖，Allure 生成可视化报告。覆盖腾讯新闻网页版导航栏、搜索及搜索结果页的自动化回归测试。

## 技术栈

| 类别 | 技术 | 版本 |
|---|---|---|
| 语言 | Python | 3.12.* |
| 测试框架 | pytest | >=9.0.3 |
| 浏览器自动化 | Playwright | >=1.58.0 |
| 报告 | allure-pytest | >=2.15.3 |
| 依赖管理 | Pixi | -- |
| 代码规范 | black / isort / autoflake | -- |
| CI/CD | GitHub Actions | -- |

## 项目结构

```
tencent_news_web_test/
├── common/                          # 公共模块
│   ├── base_page.py                 # 基础页面类（导航、截图、元素定位、iframe 切换）
│   ├── conf_loader.py               # TOML 配置加载器
│   ├── csv_reader.py                # CSV 测试数据读取
│   └── run_command.py               # 子进程命令执行
├── pages/                           # 页面对象模型（POM）
│   ├── main_page.py                 # 首页（导航栏操作、搜索建议、弹窗关闭）
│   └── search_result_page.py        # 搜索结果页（图文卡片验证、关键词高亮）
├── test_cases/                      # 测试用例
│   ├── conftest.py                  # pytest fixtures（browser / context / page）
│   ├── test_main_page.py            # 首页测试：导航栏、搜索功能
│   └── test_search_result_page.py   # 搜索结果页测试：卡片内容、关键词高亮、新标签页
├── data/                            # 测试数据（CSV）
│   ├── nav_links.csv                # 导航栏链接数据（19 条）
│   └── search_keywords.csv          # 搜索关键词数据（含 SQL 注入、XSS、空值、超长输入、emoji）
├── scripts/                         # 工具脚本
│   ├── run.py                       # 测试执行入口（支持 -m 标记筛选）
│   ├── clean.py                     # 清理截图/报告/日志
│   └── lint.py                      # 代码格式检查
├── report/                          # Allure 测试报告
│   ├── json/                        # 原始 JSON
│   └── html/                        # HTML 报告
├── screenshots/                     # 失败截图
├── .github/workflows/ci.yml         # CI 流水线
├── pixi.toml                        # Pixi 项目配置
├── pytest.ini                       # pytest 配置
└── AGENTS.md                        # AI 辅助开发规范
```

## 快速开始

### 前置要求

- Python 3.12+
- [Pixi](https://pixi.sh)（`powershell -ExecutionPolicy ByPass -c "irm -Uri https://pixi.sh/ps1 | iex"`）

### 安装

```bash
git clone <repo_url>
cd tencent_news_web_test
pixi install           # 创建虚拟环境 + 安装依赖
pixi run install-playwright  # 下载 Chromium/Firefox/WebKit 浏览器驱动
```

### 运行测试

```bash
# 运行已完成标记的用例（@pytest.mark.completed）
pixi run run

# 运行进行中的用例（@pytest.mark.inprogress）
pixi run test

# 运行所有用例
python scripts/run.py

# 按标记筛选
python scripts/run.py -m completed

# 指定测试文件
python scripts/run.py test_cases/test_main_page.py

# 单条用例
pytest test_cases/test_main_page.py::test_open_main_page
```

### 其他命令

```bash
pixi run lint    # 代码格式检查（autoflake + black + isort）
pixi run clean   # 清理 screenshots/、report/、test_log.log
```

## 测试用例一览

### 首页（`test_main_page.py`）

| 测试 | 说明 |
|---|---|
| `test_open_main_page` | 打开首页，验证 URL 与标题 |
| `TestNavBar::test_nav_item_data` | 参数化：每个导航项的文本与 href（数据源 `nav_links.csv`） |
| `TestNavBar::test_nav_item_hover` | 导航项 hover 伪元素变化 |
| `TestNavBar::test_nav_item_click` | 点击导航链接，验证新标签页 |
| `TestNavBar::test_more_nav_item_visible` | "更多"下拉显示/隐藏 |
| `TestNavBar::test_more_nav_item_hover` | "更多"子项 hover 文字颜色变化 |
| `TestNavBar::test_more_nav_item_click` | "更多"子项点击，验证新标签页 |
| `TestSearch::test_search_suggestions_appear` | 参数化：输入关键词后搜索建议出现/消失 |
| `TestSearch::test_search_with_keywords` | 参数化：完整搜索流程，验证 URL、标题、响应码 |

### 搜索结果页（`test_search_result_page.py`）

| 测试 | 说明 |
|---|---|
| `test_result_page_has_cards` | 验证搜索结果包含图文卡片 |
| `test_card_title_and_description` | 验证前 5 个卡片标题非空 |
| `test_keyword_highlighted` | 验证关键词在前 5 个卡片中蓝色高亮 |
| `test_click_card_opens_new_tab` | 点击卡片，验证新标签页打开 |

搜索关键词参数化：`腾讯新闻`、`AI技术`、`世界杯`

## Playwright 配置

编辑 `pixi.toml` 的 `[tool.playwright]`：

```toml
[tool.playwright]
launch_options = {headless = true, timeout = 5000, args = ["--font-render-hinting=none"]}
platform = ""  # 可选 chromium / firefox / webkit，默认 Chromium
```

## CI/CD

已内置 GitHub Actions 流水线（`.github/workflows/ci.yml`）：

- **触发方式**：`workflow_dispatch`（手动）、push、PR
- **流程**：安装依赖 → 运行 `pixi run run` → 上传 Allure 报告 → 部署到 GitHub Pages
- **在线报告**：`https://y-run-y.github.io/tencent_news_web_test/`

## 测试数据

CSV 文件位于 `data/`，支持参数化测试：

- **`nav_links.csv`** — 19 条导航栏数据，包含标题与期望链接
- **`search_keywords.csv`** — 11 条搜索关键词，涵盖正常输入、SQL 注入、XSS、空值、超长字符串、emoji

## 开源协议

MIT © [希望能学会](LICENSE)
