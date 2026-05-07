import argparse
import os
import shutil

from utils.conf_loader import config, project_root
from utils.run_command import run_command

test_cfg = config["build"]
allure_cfg = config["allure"]
ci_cfg = config.get("ci", {})


def is_ci_environment():
    """检测是否在 CI 环境中运行"""
    return os.environ.get("CI", "").lower() == "true" or os.environ.get("GITEA_ACTIONS", "") == "true"


def apply_ci_defaults(pytest_cmd):
    """应用 CI 环境的默认配置"""
    if ci_cfg.get("parallel", False):
        workers = ci_cfg.get("workers", 4)
        pytest_cmd.extend(["-n", str(workers)])
    timeout = ci_cfg.get("timeout", 30000)
    pytest_cmd.extend(["--timeout", str(timeout)])
    return pytest_cmd


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
        "--ci",
        action="store_true",
        default=False,
        help="CI 模式：自动应用 CI 环境配置（无头模式、并行等）",
    )
    parser.add_argument(
        "-m",
        "--marker",
        type=str,
        default=None,
        help="通过标记筛选测试用例（pytest -m 语法）",
    )
    parser.add_argument(
        "-k",
        "--keyword",
        type=str,
        default=None,
        help="通过关键词表达式筛选测试用例（pytest -k 语法）",
    )
    parser.add_argument(
        "-n",
        "--workers",
        type=int,
        default=None,
        help="并行执行的 worker 数量",
    )
    parser.add_argument(
        "test_path",
        type=str,
        nargs="*",
        default=None,
        help="指定要运行的测试文件或测试函数路径",
    )
    args = parser.parse_args()

    mode = args.mode
    is_ci = args.ci or is_ci_environment()

    screenshot_dir = project_root / "screenshots"
    if screenshot_dir.exists():
        shutil.rmtree(screenshot_dir)
    pytest_cmd = ["pytest"]
    if args.test_path:
        pytest_cmd.extend(args.test_path)
    if args.keyword:
        pytest_cmd.extend(["-k", args.keyword])

    if is_ci:
        pytest_cmd = apply_ci_defaults(pytest_cmd)

    if mode == "run":
        run_command(pytest_cmd)
    elif mode == "build":
        if test_cfg["black"]:
            run_command(["black", "."])
        if test_cfg["isort"]:
            run_command(["isort", "."])
        pytest_cmd.extend(["-p", "no:dependency"])
        if args.test_path:
            run_command(pytest_cmd)
        else:
            pytest_cmd.extend(["-m", "inprogress"])
            run_command(pytest_cmd)
    elif config.get("mode") == "build":
        pytest_cmd.extend(["-p", "no:dependency"])
        if args.test_path or args.keyword:
            run_command(pytest_cmd)
        else:
            pytest_cmd.extend(["-m", "inprogress"])
            run_command(pytest_cmd)
    else:
        run_command(pytest_cmd)

    if allure_cfg["enable"]:
        output_dir = project_root / allure_cfg["output"].strip("'\"")
        if output_dir.exists():
            shutil.rmtree(output_dir)
        run_command(
            ["allure", "generate", allure_cfg["input"], "-o", allure_cfg["output"]]
        )
        if allure_cfg["open_report"] and not is_ci:
            run_command(["allure", "open", allure_cfg["output"]])


if __name__ == "__main__":
    main()
