import argparse
import shutil
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from common.conf_loader import config, project_root
from common.run_command import run_command

allure_cfg = config["allure"]


def main():
    parser = argparse.ArgumentParser(description="运行测试用例")
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
