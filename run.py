import subprocess
from typing import List

from utils.conf_loader import config

code_cfg = config["code"]
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
    if code_cfg["black"]:
        # 运行 black 格式化当前项目所有代码
        res = run_command(["black", "."], capture=True)
        print(res.stderr)
    if code_cfg["isort"]:
        # 运行 isort
        run_command(["isort", "."], capture=True)
    # 运行 pytest 测试
    run_command(["pytest"])
    if allure_cfg["enable"]:
        # 运行 allure 生成测试报告
        run_command(
            ["allure", "generate", allure_cfg["input"], "-o", allure_cfg["output"]]
        )
        if allure_cfg["open_report"]:
            run_command(["allure", "open", allure_cfg["output"]])


if __name__ == "__main__":
    main()
