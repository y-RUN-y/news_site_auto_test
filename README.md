## 介绍
 腾讯新闻网页版自动化测试框架，基于 Python + pytest + Playwright 构建，采用页面对象模型（POM）设计，使用 Pixi 管理依赖，Allure 生成可视化测试报告。支持对腾讯新闻网页版的功能、兼容性进行自动化测试，提供可扩展的测试架构与丰富的工具函数。

 ## 软件架构

 ### 核心技术栈
 - **开发语言**：Python 3.12+（遵循 `pixi.toml` 要求）
 - **测试框架**：pytest 9.0.3+
 - **浏览器自动化**：Playwright 1.58.0+（支持 Chromium、Firefox、WebKit）
 - **报告工具**：Allure pytest 2.15.3+
 - **依赖管理**：Pixi 0.23.0+
 - **代码规范**：black、isort（开发依赖）
 - **CI/CD**：Gitee CI（`.gitee-ci.yml`）

### 项目结构
 ```
 tencent_news_web_test/
 ├── pages/ # 页面对象模型（POM）封装
 │   ├── base_page.py # 基础页面类，封装通用操作
 │   └── main_page.py # 首页页面类，封装首页相关操作
 ├── test_cases/ # 测试用例与配置
 │   ├── conftest.py # pytest 夹具（fixture）配置
 │   ├── test_pages/ # 页面测试用例
 │   └── test_flows/ # 流程测试用例
 ├── utils/ # 工具函数
 │   ├── conf_loader.py # 配置加载工具
 │   ├── csv_reader.py # CSV 数据读取工具
 │   ├── notify.py # CI 通知工具
 │   └── run_command.py # 命令执行工具
 ├── data/ # 测试数据（CSV 文件）
 ├── report/ # 测试报告与截图输出目录
 │   ├── json/ # Allure 原始 JSON 报告
 │   └── html/ # Allure 生成的 HTML 报告
 ├── screenshots/ # 测试失败截图目录
 ├── .gitee-ci.yml # Gitee CI 流水线配置
 ├── .gitignore # Git 忽略文件
 ├── LICENSE # MIT 开源协议
 ├── pixi.toml # Pixi 项目配置与工具配置
 ├── pixi.lock # Pixi 依赖锁定文件
 ├── run.py # 测试执行入口脚本
 └── README.md # 项目说明文档
 ```

### 工作流程
 1. 编写/维护页面对象（`pages/` 目录）与测试用例（`test_cases/` 目录）
 2. 执行 `pixi install` 安装依赖
 3. 运行 `python run.py` 执行测试
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
    pixi run playwright install
    ```
    该命令会安装 Chromium、Firefox、WebKit 等浏览器驱动（默认使用 Chromium，可在 `pixi.toml` 的 `[tool.playwright]` 中修改平台配置）。
 4. **（可选）配置 Playwright 启动参数**
    编辑 `pixi.toml` 中的 `[tool.playwright]` 部分，调整测试行为：
    ```toml
    [tool.playwright]
    platform = "" # 留空默认使用 Chromium，可选 chromium、firefox、webkit
    launch_options = {headless = false, timeout = 3000, slow_mo = 1000}
    ```
    - `headless`：是否无头模式运行（默认 `true`，CI 环境强制为 true）
    - `timeout`：导航超时时间（毫秒）
    - `slow_mo`：操作延迟（毫秒，便于观察测试过程）

## 使用说明

 ### 执行测试

 ### 自定义 pytest 配置
 项目已通过 `pixi.toml` 的 `[tool.pytest.ini_options]` 配置默认参数：
 - 测试路径：`test_cases/`
 - 测试文件匹配：`test_*.py`
 - 日志级别：DEBUG，输出到控制台与 `./test_log.log`
 - 自动清理 Allure 旧报告：`--clean-alluredir`
 可根据需要修改该配置。

 ### 运行入口脚本
 项目提供 `run.py` 作为简化执行入口，可直接运行：
 ```bash
 python run.py --mode run
 ```

 或使用 pixi：
 ```bash
 pixi run test
 ```

 ## CI/CD 集成

 ### Gitee CI 配置
 项目已内置 `.gitee-ci.yml` 配置文件，支持以下功能：

 - **自动运行测试**：每次 Push/PR 时自动执行测试
 - **代码质量检查**：自动运行 black、isort 代码格式检查
 - **Allure 报告生成**：自动生成 HTML 测试报告
 - **报告在线发布**：自动部署到 Gitee Pages（main/master 分支）
 - **失败通知**：支持企业微信、钉钉、飞书 webhook 通知
 - **定时执行**：支持每日定时自动构建

 ### CI 环境变量
 在 Gitee 仓库设置中添加以下 Secret 变量：

 | 变量名 | 说明 | 示例 |
|--------|------|------|
| `NOTIFY_WEBHOOK_URL` | 通知 webhook 地址 | 企业微信/钉钉机器人 URL |
| `NOTIFY_TYPE` | 通知类型 | `wechat`、`dingtalk`、`lark` |
| `MENTIONED_MOBILE` | 需要 @ 的手机号 | `13800138000`（多个用逗号分隔）|

 ### CI 配置示例
 编辑 `pixi.toml` 中的 `[tool.ci]` 部分调整 CI 行为：

 ```toml
 [tool.ci]
 headless = true           # CI 环境强制使用无头模式
 timeout = 30000           # CI 环境增加超时时间
 parallel = true          # 是否并行执行测试
 workers = 4              # 并行 worker 数量
 screenshot_on_failure = true
 notify_on_failure = true
 ```

 ### 手动触发 CI
 在 Gitee 仓库的 "流水线" 页面可以手动触发构建，选择分支和配置后即可执行。

 ### 查看测试报告
 CI 成功后，访问 Gitee Pages 查看测试报告：
 ```
 https://[用户名].gitee.io/tencent-news-web-test/
 ```

 ## 开源协议
 本项目采用 MIT 开源协议，详见 [LICENSE](LICENSE) 文件。
