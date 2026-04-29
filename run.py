import shutil
import subprocess
from typing import List

from utils.conf_loader import config, project_root

test_cfg = config["build"]
allure_cfg = config["allure"]


def run_command(
    cmd: List[str], capture: bool = False, encoding: str = "utf-8"
) -> subprocess.CompletedProcess:
    """执行命令行工具的通用函数"""
    try:
        result = subprocess.run(
            cmd,
            capture_output=capture,
            text=True,
            encoding=encoding,
            check=False,
            shell=True,
        )
        return result
    except FileNotFoundError as e:
        raise FileNotFoundError(
            f"命令 {cmd[0]} 未找到，请确保已安装并添加到 PATH 中: {e}"
        )


def main():
    if config['mode'] == 'run':
        run_command(["pytest"])
    elif config['mode'] == 'build':
        if test_cfg["black"]:
            # 运行 black 格式化当前项目所有代码
            res = run_command(["black", "."])
        if test_cfg["isort"]:
            # 运行 isort
            run_command(["isort", "."])
        # 运行 pytest 测试
        run_command(['pytest', '-m', 'inprogress'])
        # 清理截图
        if test_cfg["clear_screenshots"]:
            screenshot_dir = project_root / "screenshots"
            if screenshot_dir.exists():
                shutil.rmtree(screenshot_dir)
        if allure_cfg["enable"]:
            # 先清理旧报告目录（Python 原生方式，避免 shell 路径解析问题）
            output_dir = project_root / allure_cfg["output"].strip("'\"")
            if output_dir.exists():
                shutil.rmtree(output_dir)
            # 运行 allure 生成测试报告
            run_command(
                ["allure", "generate", allure_cfg["input"], "-o", allure_cfg["output"]]
            )
            if allure_cfg["open_report"]:
                run_command(["allure", "open", allure_cfg["output"]])


if __name__ == "__main__":
    main()
