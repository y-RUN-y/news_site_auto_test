import subprocess
from typing import List


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
