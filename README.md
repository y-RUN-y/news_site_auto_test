# 腾讯新闻网页版自动化测试框架

基于 Python + pytest + Playwright 构建的端到端自动化测试框架，采用页面对象模型（POM）设计，支持数据驱动测试、失败截图重试和 Allure 可视化报告。

## 技术栈

| 类别 | 技术 | 版本 |
|------|------|------|
| 语言 | Python | 3.12.* |
| 测试框架 | pytest | >=9.0.3 |
| 并发执行 | pytest-xdist | >=3.8.0 |
| 失败重试 | pytest-rerunfailures | >=16.1 |
| 浏览器自动化 | Playwright | >=1.58.0 |
| 报告生成 | allure-pytest | >=2.15.3 |
| 依赖管理 | Pixi | -- |
| 代码规范 | autoflake / black / isort | -- |
| CI/CD | GitHub Actions | -- |

## 项目结构

```
tencent_news_web_test/
├── common/                          # 公共模块
│   ├── __init__.py
│   ├── base_page.py                 # 基础页面类（导航、截图、元素定位、重试机制）
│   ├── conf_loader.py               # pixi.toml 配置加载器
│   ├── csv_reader.py                 # CSV 测试数据读取器
│   └── run_command.py               # 子进程命令执行
├── pages/                           # 页面对象模型（POM）
│   ├── __init__.py
│   ├── main_page.py                 # 首页（导航栏、搜索框、弹窗关闭）
│   └── search_result_page.py        # 搜索结果页（图文卡片、关键词高亮）
├── test_cases/                      # 测试用例
│   ├── __init__.py
│   ├── conftest.py                  # pytest fixtures（browser/context/page、失败截图钩子）
│   ├── test_main_page.py            # 首页测试：导航栏、搜索功能
│   └── test_search_result_page.py   # 搜索结果页测试：卡片内容、关键词高亮、新标签页
├── data/                             # 测试数据（CSV）
│   ├── nav_links.csv                # 导航栏链接数据（19 条）
│   └── search_keywords.csv          # 搜索关键词数据（11 条，含异常输入）
├── scripts/                          # 工具脚本
│   ├── run.py                       # 测试执行入口（支持标记筛选、路径指定）
│   ├── clean.py                     # 清理 screenshots/、report/、test_log.log
│   └── lint.py                      # 代码格式检查（autoflake + black + isort）
├── report/                          # Allure 测试报告
│   ├── json/                        # 原始 JSON 数据
│   └── html/                        # HTML 报告
├── screenshots/                     # 失败截图（自动清理）
├── .github/workflows/
│   └── ci.yml                       # CI 流水线（测试 → 生成报告 → 部署 GitHub Pages）
├── pixi.toml                        # Pixi 项目配置（依赖、任务、工具配置）
├── pytest.ini                       # pytest 配置（标记、日志、重试、并发）
├── changelog.md                      # 变更日志规范
├── AGENTS.md                        # AI 辅助开发规范
├── README.md
└── LICENSE
```

## 快速开始

### 前置要求

- Python 3.12+
- [Pixi](https://pixi.sh) 包管理器

```powershell
# Windows 安装 Pixi
powershell -ExecutionPolicy ByPass -c "irm -Uri https://pixi.sh/ps1 | iex"
```

### 安装

```bash
git clone <repo_url>
cd tencent_news_web_test
pixi install              # 创建虚拟环境 + 安装依赖
pixi run install-playwright  # 下载 Chromium/Firefox/WebKit 浏览器驱动
```

### 运行测试

```bash
# 运行已完成的用例（@pytest.mark.completed）
pixi run run

# 运行进行中的用例（@pytest.mark.inprogress）
pixi run test
```

### 其他命令

```bash
pixi run lint    # 代码格式检查（autoflake + black + isort）
pixi run clean   # 清理 screenshots/、report/、test_log.log
```

## 测试用例

### 首页（`test_main_page.py`）

| 测试类 | 用例 | 说明 |
|--------|------|------|
| - | `test_open_main_page` | 打开首页，验证 URL 与标题 |
| `TestNavBar` | `test_nav_item_data` | 参数化验证导航项文本与链接（数据源：`nav_links.csv`） |
| `TestNavBar` | `test_nav_item_hover` | 验证导航项 hover 时 `::before` 伪元素样式变化 |
| `TestNavBar` | `test_nav_item_click` | 点击导航项，验证新标签页打开与标题匹配 |
| `TestNavBar` | `test_more_nav_item_visible` | 验证"更多"下拉显示/隐藏 |
| `TestNavBar` | `test_more_nav_item_hover` | 验证"更多"子项 hover 文字颜色变化（黑→蓝） |
| `TestNavBar` | `test_more_nav_item_click` | 点击"更多"子项，验证新标签页打开 |
| `TestSearch` | `test_search_suggestions_appear` | 参数化验证搜索建议出现/消失（数据源：`search_keywords.csv`） |
| `TestSearch` | `test_search_with_keywords` | 参数化验证完整搜索流程（URL、标题、新标签页） |

### 搜索结果页（`test_search_result_page.py`）

| 用例 | 说明 |
|------|------|
| `test_result_page_has_cards` | 验证搜索结果包含图文卡片（参数化：`腾讯新闻`、`AI技术`、`世界杯`） |
| `test_card_title_and_description` | 验证前 5 个卡片标题非空 |
| `test_keyword_highlighted` | 验证前 5 个卡片中关键词蓝色高亮 |
| `test_click_card_opens_new_tab` | 点击卡片，验证新标签页打开 |

## 测试数据

`data/` 目录下的 CSV 文件支持参数化测试：

- **`nav_links.csv`** — 19 条导航栏数据（title, link）
- **`search_keywords.csv`** — 11 条搜索关键词数据（keyword, has_suggestions, has_search_res, response_code）

涵盖：正常输入、SQL 注入、XSS、空值、超长字符串、emoji 等异常场景。

## Playwright 配置

编辑 `pixi.toml` 的 `[tool.playwright]` 部分：

```toml
[tool.playwright]
launch_options = {headless = true, timeout = 5000, args = ["--font-render-hinting=none"]}
platform = ""  # 可选 chromium / firefox / webkit，默认 chromium
```

## CI/CD

`.github/workflows/ci.yml` 内置 GitHub Actions 流水线：

1. 安装 Pixi 和依赖
2. 安装 Playwright 浏览器
3. 运行 `pixi run run`（已标记的测试用例）
4. 生成 Allure 报告
5. 部署到 GitHub Pages

触发方式：`workflow_dispatch`（手动）、push、PR。

在线报告：`https://y-run-y.github.io/tencent_news_web_test/`

## 代码规范

```bash
# 自动化检查并修复
pixi run lint
```

## 开源协议

MIT © [希望能学会](LICENSE)