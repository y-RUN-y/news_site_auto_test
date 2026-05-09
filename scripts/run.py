import argparse
import shutil
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from utils.conf_loader import config, project_root
from utils.run_command import run_command

test_cfg = config["build"]
allure_cfg = config["allure"]


def main():
    parser = argparse.ArgumentParser(description="运行测试用例")
    parser.add_argument(
        "--mode",
        type=str,
        choices=["run", "build"],
        default=None,
        help="运行模式：run 或 build（会覆盖配置文件的 mode）",
    )
    parser.add_argument(
        "-m",
        "--marker",
        type=str,
        default=None,
        help="通过标记筛选测试用例（pytest -m 语法）",
    )
    parser.add_argument(
        "test_path",
        type=str,
        nargs="*",
        default=None,
        help="指定要运行的测试文件或测试函数路径",
    )
    args = parser.parse_args()

    screenshot_dir = project_root / "screenshots"
    if screenshot_dir.exists():
        shutil.rmtree(screenshot_dir)

    pytest_cmd = ["pytest"]
    if args.test_path:
        pytest_cmd.extend(args.test_path)
    if args.marker:
        pytest_cmd.extend(["-m", args.marker])

    mode = args.mode if args.mode else config.get("mode", "run")

    if mode == "run":
        run_command(pytest_cmd)
    elif mode == "build":
        pytest_cmd.extend(["-p", "no:dependency"])
        pytest_cmd.extend(["-m", "inprogress"])
        run_command(pytest_cmd)

    if allure_cfg["enable"]:
        output_dir = project_root / allure_cfg["output"].strip("'\"")
        if output_dir.exists():
            shutil.rmtree(output_dir)
        run_command(
            ["allure", "generate", allure_cfg["input"], "-o", allure_cfg["output"]]
        )
        if allure_cfg["open_report"]:
            run_command(["allure", "open", allure_cfg["output"]])


if __name__ == "__main__":
    main()