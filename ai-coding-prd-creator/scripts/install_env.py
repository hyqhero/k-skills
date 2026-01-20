#!/usr/bin/env python3
"""
环境安装指导脚本
根据选择的技术框架生成对应的安装命令
支持跨平台（Windows/macOS/Linux）
"""

import argparse
import json
import sys
import platform


# 常见框架的安装命令映射
FRAMEWORK_INSTALL_COMMANDS = {
    # Python Web框架
    "flask": {
        "name": "Flask",
        "description": "轻量级Python Web框架",
        "prerequisites": ["Python 3.7+"],
        "install_commands": [
            "pip install flask"
        ],
        "verify_command": "python -c \"import flask; print(flask.__version__)\""
    },
    "django": {
        "name": "Django",
        "description": "全功能Python Web框架",
        "prerequisites": ["Python 3.8+"],
        "install_commands": [
            "pip install django"
        ],
        "verify_command": "python -c \"import django; print(django.get_version())\""
    },
    "fastapi": {
        "name": "FastAPI",
        "description": "现代Python Web框架",
        "prerequisites": ["Python 3.7+"],
        "install_commands": [
            "pip install fastapi uvicorn"
        ],
        "verify_command": "python -c \"import fastapi; print(fastapi.__version__)\""
    },
    "streamlit": {
        "name": "Streamlit",
        "description": "Python数据应用框架",
        "prerequisites": ["Python 3.7+"],
        "install_commands": [
            "pip install streamlit"
        ],
        "verify_command": "python -c \"import streamlit; print(streamlit.__version__)\""
    },
    "tkinter": {
        "name": "Tkinter",
        "description": "Python内置GUI库",
        "prerequisites": ["Python 3.6+"],
        "install_commands": {
            "windows": [
                "# Tkinter通常随Python一起安装，无需额外安装",
                "# 如果缺失，重新安装Python时勾选'tcl/tk and IDLE'选项"
            ],
            "macos": [
                "# Tkinter通常随Python一起安装，无需额外安装",
                "# 如果缺失，重新安装Python或使用: brew install python-tk"
            ],
            "linux": [
                "# Ubuntu/Debian: sudo apt-get install python3-tk",
                "# CentOS/RHEL: sudo yum install python3-tkinter",
                "# Fedora: sudo dnf install python3-tkinter"
            ]
        },
        "verify_command": "python -c \"import tkinter; print('Tkinter已安装')\""
    },

    # Node.js框架
    "nextjs": {
        "name": "Next.js",
        "description": "React全栈框架",
        "prerequisites": ["Node.js 14+"],
        "install_commands": [
            "npx create-next-app@latest my-app",
            "# 或者全局安装:",
            "npm install -g create-next-app"
        ],
        "verify_command": "npx next --version"
    },
    "react": {
        "name": "React",
        "description": "前端框架",
        "prerequisites": ["Node.js 14+"],
        "install_commands": [
            "npx create-react-app my-app"
        ],
        "verify_command": "npx react-scripts --version"
    },
    "vue": {
        "name": "Vue.js",
        "description": "渐进式前端框架",
        "prerequisites": ["Node.js 14+"],
        "install_commands": [
            "npm install -g @vue/cli",
            "vue create my-app"
        ],
        "verify_command": "vue --version"
    },
    "express": {
        "name": "Express",
        "description": "Node.js Web框架",
        "prerequisites": ["Node.js 14+"],
        "install_commands": [
            "mkdir my-app && cd my-app",
            "npm init -y",
            "npm install express"
        ],
        "verify_command": "node -e \"console.log(require('express/package.json').version)\""
    },

    # 静态站点生成器
    "hexo": {
        "name": "Hexo",
        "description": "静态博客生成器",
        "prerequisites": ["Node.js 14+"],
        "install_commands": [
            "npm install -g hexo-cli",
            "hexo init my-blog"
        ],
        "verify_command": "hexo version"
    },
    "hugo": {
        "name": "Hugo",
        "description": "快速静态站点生成器",
        "prerequisites": ["无特殊要求"],
        "install_commands": {
            "windows": [
                "# 方法1: 使用Chocolatey",
                "choco install hugo-extended",
                "# 方法2: 使用Scoop",
                "scoop install hugo-extended",
                "# 方法3: 从官网下载: https://gohugo.io/getting-started/installing/"
            ],
            "macos": [
                "# 使用Homebrew安装",
                "brew install hugo"
            ],
            "linux": [
                "# Ubuntu/Debian",
                "sudo apt-get install hugo",
                "# CentOS/RHEL",
                "sudo yum install hugo",
                "# Fedora",
                "sudo dnf install hugo",
                "# 或使用snap",
                "sudo snap install hugo"
            ]
        },
        "verify_command": "hugo version"
    },
    "jekyll": {
        "name": "Jekyll",
        "description": "Ruby静态站点生成器",
        "prerequisites": ["Ruby"],
        "install_commands": {
            "windows": [
                "# 1. 从 https://rubyinstaller.org/ 下载安装Ruby",
                "# 2. 安装后打开'Ruby Command Prompt with Ruby'执行:",
                "gem install jekyll bundler"
            ],
            "macos": [
                "# macOS通常已安装Ruby，直接执行:",
                "gem install jekyll bundler",
                "# 如果权限问题，执行:",
                "sudo gem install jekyll bundler"
            ],
            "linux": [
                "# Ubuntu/Debian",
                "sudo apt-get install ruby-full build-essential zlib1g-dev",
                "# 安装Ruby后执行:",
                "gem install jekyll bundler",
                "# 注意：可能需要配置Ruby路径",
                "echo 'export PATH=\"$HOME/.gem/ruby/3.0.0/bin:$PATH\"' >> ~/.bashrc",
                "source ~/.bashrc"
            ]
        },
        "verify_command": "jekyll --version"
    },

    # 数据分析工具
    "pandas": {
        "name": "Pandas",
        "description": "Python数据分析库",
        "prerequisites": ["Python 3.7+"],
        "install_commands": [
            "pip install pandas openpyxl"
        ],
        "verify_command": "python -c \"import pandas; print(pandas.__version__)\""
    },
    "matplotlib": {
        "name": "Matplotlib",
        "description": "Python绘图库",
        "prerequisites": ["Python 3.7+"],
        "install_commands": [
            "pip install matplotlib"
        ],
        "verify_command": "python -c \"import matplotlib; print(matplotlib.__version__)\""
    },

    # 桌面应用
    "electron": {
        "name": "Electron",
        "description": "跨平台桌面应用框架",
        "prerequisites": ["Node.js 14+"],
        "install_commands": [
            "npm install -g electron"
        ],
        "verify_command": "electron --version"
    }
}


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


def get_framework_info(framework_name: str) -> dict:
    """
    获取框架信息
    """
    framework_key = framework_name.lower().replace(".", "").replace("-", "")

    # 模糊匹配
    for key, value in FRAMEWORK_INSTALL_COMMANDS.items():
        if framework_key in key or key in framework_key:
            return value

    return None


def generate_install_commands(framework_name: str, platform: str = None, format: str = "text") -> str:
    """
    生成安装命令
    """
    framework_info = get_framework_info(framework_name)

    if not framework_info:
        return f"错误：未找到框架 '{framework_name}' 的安装信息"

    # 如果没有指定平台，自动检测
    if platform is None:
        platform = detect_platform()

    # 获取安装命令
    install_commands = framework_info.get("install_commands", [])

    # 如果安装命令是字典（区分平台），根据平台选择
    if isinstance(install_commands, dict):
        if platform in install_commands:
            install_commands = install_commands[platform]
        else:
            # 如果找不到对应平台的命令，使用默认值或报错
            return f"警告：未找到适用于 {platform} 平台的安装命令\n\n支持的框架：{framework_info['name']}\n描述：{framework_info['description']}\n前置条件：{', '.join(framework_info['prerequisites'])}\n\n请手动安装或使用以下通用方法："

    # 生成输出
    if format == "json":
        result = framework_info.copy()
        result["detected_platform"] = platform
        return json.dumps(result, indent=2, ensure_ascii=False)
    else:
        output = []
        output.append(f"# {framework_info['name']} 安装指南")
        output.append(f"# 描述：{framework_info['description']}")
        output.append(f"# 检测到的操作系统：{platform.upper()}")
        output.append(f"# 前置条件：{', '.join(framework_info['prerequisites'])}")
        output.append("")
        output.append("# 安装命令：")
        for cmd in install_commands:
            output.append(cmd)
        output.append("")
        output.append("# 验证安装：")
        output.append(framework_info['verify_command'])
        output.append("")
        output.append("# 提示：")
        output.append("# - 如果命令执行失败，请检查是否以管理员/管理员权限运行")
        output.append("# - 如果无法自动识别系统，可使用 --platform 参数指定（windows/macos/linux）")
        output.append("")

        return "\n".join(output)


def list_available_frameworks():
    """
    列出所有支持的框架
    """
    output = []
    output.append("# 支持的框架列表：")
    output.append("")

    for key, info in FRAMEWORK_INSTALL_COMMANDS.items():
        output.append(f"## {info['name']} ({key})")
        output.append(f"描述：{info['description']}")
        output.append(f"前置条件：{', '.join(info['prerequisites'])}")
        output.append("")

    return "\n".join(output)


def main():
    """
    主函数
    """
    parser = argparse.ArgumentParser(description="生成技术框架的安装命令")
    parser.add_argument("--framework", "-f", help="框架名称（如：flask, react, hexo等）")
    parser.add_argument("--list", "-l", action="store_true", help="列出所有支持的框架")
    parser.add_argument("--platform", "-p", choices=["windows", "macos", "linux", "auto"],
                        default="auto", help="指定操作系统（默认自动检测）")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="输出格式")

    args = parser.parse_args()

    if args.list:
        print(list_available_frameworks())
    elif args.framework:
        # 确定使用的平台
        if args.platform == "auto":
            platform = None  # 让函数自动检测
        else:
            platform = args.platform

        print(generate_install_commands(args.framework, platform, args.format))
    else:
        parser.print_help()
        print("\n提示：")
        print("  - 使用 --list 查看所有支持的框架")
        print("  - 使用 --platform 手动指定操作系统（如果自动检测失败）")


if __name__ == "__main__":
    main()
