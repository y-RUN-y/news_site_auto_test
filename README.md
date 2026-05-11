# 腾讯新闻网页版自动化测试框架

基于 Python + pytest + Playwright 构建，采用页面对象模型（POM）设计，使用 Pixi 管理依赖，Allure 生成可视化测试报告。支持对腾讯新闻网页版的功能、兼容性进行自动化测试，提供可扩展的测试架构与丰富的工具函数。

## 软件架构

### 核心技术栈

- **开发语言**：Python 3.12+（遵循 `pixi.toml` 要求）
- **测试框架**：pytest 9.0.3+
- **浏览器自动化**：Playwright 1.58.0+（支持 Chromium、Firefox、WebKit）
- **报告工具**：Allure pytest 2.15.3+
- **依赖管理**：Pixi 0.23.0+
- **代码规范**：black、isort、autoflake（开发依赖）
- **CI/CD**：GitHub Actions（`.github/workflows/ci.yml`）

### 项目结构

```
tencent_news_web_test/
├── pages/                          # 页面对象模型（POM）封装
│   ├── __init__.py
│   ├── base_page.py                # 基础页面类，封装通用操作（导航、截图、元素定位等）
│   ├── main_page.py                # 首页页面类，封装搜索、导航栏等操作
│   └── search_result_page.py       # 搜索结果页页面类，封装图文卡片操作
├── test_cases/                     # 测试用例与配置
│   ├── __init__.py
│   ├── conftest.py                 # pytest 夹具（fixture）配置，提供 browser/context/page
│   ├── test_main_page.py           # 首页测试用例（导航栏、搜索功能）
│   └── test_search_result_page.py  # 搜索结果页测试用例（卡片展示、关键词高亮等）
├── utils/                          # 工具函数
│   ├── __init__.py
│   ├── conf_loader.py              # 配置加载工具（读取 pixi.toml）
│   ├── csv_reader.py               # CSV 数据读取工具（参数化测试数据源）
│   └── run_command.py              # 命令执行工具
├── scripts/                        # 项目脚本
│   ├── run.py                      # 测试执行入口脚本
│   ├── lint.py                     # 代码格式检查脚本（autoflake + black + isort）
│   └── clean.py                    # 清理脚本（删除截图、报告、日志）
├── data/                           # 测试数据（CSV 文件）
│   ├── nav_links.csv               # 导航栏链接测试数据
│   └── search_keywords.csv         # 搜索关键词测试数据（含异常输入）
├── report/                         # 测试报告与截图输出目录
│   ├── json/                       # Allure 原始 JSON 报告
│   └── html/                       # Allure 生成的 HTML 报告
├── screenshots/                    # 测试失败截图目录
├── .github/
│   └── workflows/
│       └── ci.yml                  # GitHub CI 流水线配置
├── .gitignore
├── LICENSE                         # MIT 开源协议
├── pixi.toml                       # Pixi 项目配置与工具配置
├── pixi.lock                       # Pixi 依赖锁定文件
├── pytest.ini                      # pytest 配置文件
├── changelog.md                    # 更新日志
├── AGENTS.md                       # AI 助手开发规范
└── README.md                       # 项目说明文档
```

### 工作流程

1. 编写/维护页面对象（`pages/` 目录）与测试用例（`test_cases/` 目录）
2. 执行 `pixi install` 安装依赖
3. 运行 `pixi run test` 执行测试（或 `python scripts/run.py -m completed`）
4. 生成并查看 Allure HTML 报告
5. 集成到 CI/CD 流水线实现自动化回归

## 安装教程

### 前置要求

- Python 3.12+（需与 `pixi.toml` 中 `python` 版本一致）
- Pixi（依赖管理工具，安装方式：`pip install pixi`）

### 步骤

1. **克隆仓库**

   ```bash
   git clone https://gitee.com/hope-to-learn/tencent_news_web_test.git
   cd tencent_news_web_test
   ```

2. **安装项目依赖**

   ```bash
   pixi install
   ```

   该命令会自动创建虚拟环境并安装所有依赖（包括 pytest、playwright、allure-pytest 等）。

3. **安装 Playwright 浏览器**

   ```bash
   pixi run install-playwright
   ```

   该命令会安装 Chromium、Firefox、WebKit 等浏览器驱动（默认使用 Chromium，可在 `pixi.toml` 的 `[tool.playwright]` 中修改平台配置）。

4. **（可选）配置 Playwright 启动参数**

   编辑 `pixi.toml` 中的 `[tool.playwright]` 部分，调整测试行为：

   ```toml
   [tool.playwright]
   launch_options = {headless = true, timeout = 5000, args = ["--font-render-hinting=none"]}
   platform = "" # 测试平台：chromium、firefox、webkit，默认留空使用 Chromium
   ```

   - `headless`：是否无头模式运行（默认 `true`，CI 环境强制为 true）
   - `timeout`：导航超时时间（毫秒，默认 5000）
   - `slow_mo`：操作延迟（毫秒，便于观察测试过程）
   - `args`：传递给浏览器的额外启动参数

## 使用说明

### 执行测试

项目已通过 `pytest.ini` 配置默认参数：

- 测试路径：`test_cases/`
- 测试文件匹配：`test_*.py`
- 日志级别：DEBUG，输出到控制台与 `./test_log.log`
- 自动清理 Allure 旧报告：`--clean-alluredir`

### 运行入口脚本

项目提供 `scripts/run.py` 作为简化执行入口，支持按标记筛选测试用例：

```bash
# 运行已完成标记的测试
python scripts/run.py -m completed

# 运行进行中的测试
python scripts/run.py -m inprogress

# 运行指定测试文件
python scripts/run.py test_cases/test_main_page.py

# 使用 pixi 执行（推荐）
pixi run test
```

### 代码格式检查

```bash
pixi run lint
```

自动运行 autoflake、black、isort 进行代码格式检查与修复。

### 清理测试产物

```bash
pixi run clean
```

删除 `screenshots/`、`report/` 目录和 `test_log.log` 文件。

## 测试标记

测试用例通过 `@pytest.mark.completed` 和 `@pytest.mark.inprogress` 标记区分状态，可在 `pytest.ini` 中查看自定义标记。当前所有测试用例均标记为 `completed`。

## CI/CD 集成

### GitHub Actions 配置

项目已内置 `.github/workflows/ci.yml` 配置文件，支持以下功能：

- **自动运行测试**：每次 Push/PR 时自动执行测试
- **代码质量检查**：自动运行 autoflake、black、isort 代码格式检查
- **Allure 报告生成**：自动生成 HTML 测试报告
- **报告在线发布**：自动部署到 GitHub Pages（master 分支）
- **构建产物上传**：自动上传 Allure 报告为构建产物

### 手动触发 CI

在 GitHub 仓库的 "Actions" 页面可以手动触发构建，选择分支后即可执行。

### 查看测试报告

CI 成功后，访问 GitHub Pages 查看测试报告：

```
https://y-run-y.github.io/tencent_news_web_test/
```

或从构建产物的 Artifact 中下载 `report/html` 目录查看。

## 测试数据

测试数据使用 CSV 文件管理，位于 `data/` 目录：

- **nav_links.csv**：导航栏链接测试数据，包含标题和期望链接
- **search_keywords.csv**：搜索关键词测试数据，包含正常搜索词、异常输入（SQL 注入、XSS、空值）、超长输入、emoji 等场景

## 开源协议

本项目采用 MIT 开源协议，详见 [LICENSE](LICENSE) 文件。