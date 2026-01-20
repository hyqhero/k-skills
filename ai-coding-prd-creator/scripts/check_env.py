#!/usr/bin/env python3
"""
环境检查脚本
检查系统中的编程环境，包括Python、Node.js、数据库等
"""

import subprocess
import json
import sys
import platform
from typing import Dict, List, Optional


def detect_platform() -> str:
    """
    检测当前操作系统
    返回: windows, macos, 或 linux
    """
    system = platform.system().lower()
    if system == "windows":
        return "windows"
    elif system == "darwin":
        return "macos"
    elif system == "linux":
        return "linux"
    else:
        return "unknown"


def run_command(command: str) -> tuple[bool, str]:
    """
    执行shell命令并返回结果
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0, result.stdout.strip()
    except subprocess.TimeoutExpired:
        return False, "Command timeout"
    except Exception as e:
        return False, str(e)


def check_python() -> Dict:
    """
    检查Python环境
    """
    print("检查Python环境...")

    # 检查python3
    success, version = run_command("python3 --version")
    if not success:
        # 尝试python
        success, version = run_command("python --version")

    if success:
        # 检查pip
        pip_success, _ = run_command("pip3 --version")
        if not pip_success:
            pip_success, _ = run_command("pip --version")

        return {
            "installed": True,
            "version": version.replace("Python ", ""),
            "path": run_command("which python3")[1] if run_command("which python3")[0] else run_command("which python")[1],
            "pip_available": pip_success
        }
    else:
        return {
            "installed": False,
            "version": None,
            "pip_available": False
        }


def check_nodejs() -> Dict:
    """
    检查Node.js环境
    """
    print("检查Node.js环境...")

    # 检查node
    success, version = run_command("node --version")
    if success:
        # 检查npm
        npm_success, npm_version = run_command("npm --version")

        return {
            "installed": True,
            "version": version,
            "npm_version": npm_version if npm_success else None,
            "path": run_command("which node")[1] if run_command("which node")[0] else None
        }
    else:
        return {
            "installed": False,
            "version": None,
            "npm_version": None
        }


def check_java() -> Dict:
    """
    检查Java环境
    """
    print("检查Java环境...")

    success, version = run_command("java -version")
    if success:
        # java -version 输出到stderr
        success, version = run_command("java -version 2>&1 | head -n 1")
        if not success:
            version = "Java (版本信息无法解析)"

        return {
            "installed": True,
            "version": version,
            "path": run_command("which java")[1] if run_command("which java")[0] else None
        }
    else:
        return {
            "installed": False,
            "version": None
        }


def check_databases() -> Dict:
    """
    检查常见数据库
    """
    print("检查数据库环境...")

    databases = {
        "mysql": run_command("mysql --version"),
        "postgresql": run_command("psql --version"),
        "mongodb": run_command("mongod --version"),
        "redis": run_command("redis-cli --version"),
        "sqlite3": run_command("sqlite3 --version")
    }

    result = {}
    for db_name, (success, version) in databases.items():
        result[db_name] = {
            "installed": success,
            "version": version if success else None
        }

    return result


def check_git() -> Dict:
    """
    检查Git环境
    """
    print("检查Git环境...")

    success, version = run_command("git --version")
    return {
        "installed": success,
        "version": version if success else None
    }


def main():
    """
    主函数：检查所有环境
    """
    # 检测操作系统
    os_platform = detect_platform()
    print(f"检测到操作系统: {os_platform.upper()}\n")

    env_info = {
        "platform": os_platform,
        "python": check_python(),
        "nodejs": check_nodejs(),
        "java": check_java(),
        "databases": check_databases(),
        "git": check_git()
    }

    # 输出JSON格式
    print("\n环境检查结果（JSON格式）：")
    print(json.dumps(env_info, indent=2, ensure_ascii=False))

    return env_info


if __name__ == "__main__":
    main()
