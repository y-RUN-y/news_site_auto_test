## 介绍
腾讯新闻网页版自动化测试框架，基于 Python + pytest + Playwright 构建，采用页面对象模型（POM）设计，使用 Poetry 管理依赖，Allure 生成可视化测试报告。支持对腾讯新闻网页版的功能、兼容性进行自动化测试，提供可扩展的测试架构与丰富的工具函数。

## 软件架构

### 核心技术栈
- **开发语言**：Python 3.14+（遵循 `pyproject.toml` 要求）
- **测试框架**：pytest 9.0.3+
- **浏览器自动化**：Playwright 1.58.0+（支持 Chromium、Firefox、WebKit）
- **报告工具**：Allure pytest 2.15.3+
- **依赖管理**：Poetry 2.0.0+
- **代码规范**：black、isort（开发依赖）

### 项目结构
```
tencent_news_web_test/
├── pages/ # 页面对象模型（POM）封装
│   ├── base_page.py # 基础页面类，封装通用操作
│   └── home_page.py # 首页页面类，封装首页相关操作
├── test/ # 测试用例与配置
│   ├── __init__.py
│   ├── conftest.py # pytest 夹具（fixture）配置
│   └── test_home_page.py # 首页测试用例
├── utils/ # 工具函数
│   ├── __init__.py
│   └── conf_loader.py # 配置加载工具
├── report/ # 测试报告与截图输出目录
│   ├── json/ # Allure 原始 JSON 报告
│   └── html/ # Allure 生成的 HTML 报告
├── screenshots/ # 测试失败截图目录
├── .gitignore # Git 忽略文件
├── LICENSE # MIT 开源协议
├── pyproject.toml # Poetry 项目配置与工具配置
├── poetry.lock # Poetry 依赖锁定文件
├── run.py # 测试执行入口脚本
└── README.md # 项目说明文档
```

### 工作流程
1. 编写/维护页面对象（`pages/` 目录）与测试用例（`test/` 目录）
2. 执行 `poetry install` 安装依赖
3. 运行 `python run.py` 执行测试
4. 生成并查看 Allure HTML 报告
5. 集成到 CI/CD 流水线实现自动化回归

## 安装教程

### 前置要求
- Python 3.14+（需与 `pyproject.toml` 中 `requires-python` 一致）
- Poetry（依赖管理工具，安装方式：`pip install poetry`）

### 步骤
1. **克隆仓库**
   ```bash
   git clone https://gitee.com/hope-to-learn/tencent_news_web_test.git
   cd tencent_news_web_test
   ```
2. **安装项目依赖**
   ```bash
   poetry install
   ```
   该命令会自动创建虚拟环境并安装所有依赖（包括 pytest、playwright、allure-pytest 等）。
3. **安装 Playwright 浏览器**
   ```bash
   poetry run playwright install
   ```
   该命令会安装 Chromium、Firefox、WebKit 等浏览器驱动（默认使用 Chromium，可在 `pyproject.toml` 的 `[tool.playwright]` 中修改平台配置）。
4. **（可选）配置 Playwright 启动参数**
   编辑 `pyproject.toml` 中的 `[tool.playwright]` 部分，调整测试行为：
   ```toml
   [tool.playwright]
   platform = "" # 留空默认使用 Chromium，可选 chromium、firefox、webkit
   launch_options = {
     headless = false,
     timeout = 3000,
     slow_mo = 1000
   }
   ```
   - `headless`：是否无头模式运行（默认 `false`，显示浏览器界面）
   - `timeout`：导航超时时间（毫秒）
   - `slow_mo`：操作延迟（毫秒，便于观察测试过程）

## 使用说明

### 执行测试

### 自定义 pytest 配置
项目已通过 `pyproject.toml` 的 `[tool.pytest.ini_options]` 配置默认参数：
- 测试路径：`test/`
- 测试文件匹配：`test_*.py`
- 日志级别：INFO，输出到控制台与 `./test_log.log`
- 自动清理 Allure 旧报告：`--clean-alluredir`
可根据需要修改该配置。

### 运行入口脚本
项目提供 `run.py` 作为简化执行入口，可直接运行：
```bash
python run.py
```

## 开源协议
本项目采用 MIT 开源协议，详见 [LICENSE](LICENSE) 文件。
