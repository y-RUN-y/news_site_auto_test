import argparse
import shutil

from utils.conf_loader import config, project_root
from utils.run_command import run_command

test_cfg = config["build"]
allure_cfg = config["allure"]


def main():
    parser = argparse.ArgumentParser(description="运行测试用例")
    parser.add_argument(
        "-k",
        "--keyword",
        type=str,
        default=None,
        help="通过关键词表达式筛选测试用例（pytest -k 语法）",
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

    # 构建 pytest 命令
    pytest_cmd = ["pytest"]
    if args.test_path:
        pytest_cmd.extend(args.test_path)
    if args.keyword:
        pytest_cmd.extend(["-k", args.keyword])
    if args.marker:
        pytest_cmd.extend(["-m", args.marker])

    if config["mode"] == "run":
        screenshot_dir = project_root / "screenshots"
        if screenshot_dir.exists():
            shutil.rmtree(screenshot_dir)
        run_command(pytest_cmd)
    elif config["mode"] == "build":
        if test_cfg["black"]:
            run_command(["black", "."])
        if test_cfg["isort"]:
            run_command(["isort", "."])
        # 如果指定了测试路径或关键词，则使用它们；否则默认运行 inprogress 标记的测试
        pytest_cmd.extend(["-p", "no:dependency"])
        if args.test_path or args.keyword:
            run_command(pytest_cmd)
        else:
            pytest_cmd.extend(["-m", "inprogress"])
            run_command(pytest_cmd)
        if test_cfg["clear_screenshots"]:
            screenshot_dir = project_root / "screenshots"
            if screenshot_dir.exists():
                shutil.rmtree(screenshot_dir)
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
