#!/usr/bin/env python
"""
绿园中学物语：依赖安装脚本
简化版安装脚本，处理游戏所需的所有依赖
"""

import os
import sys
import subprocess
import platform

# 确保正确的工作目录
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT_DIR)

# 设置彩色输出
GREEN = YELLOW = RED = BLUE = RESET = ""
try:
    if platform.system() == "Windows":
        try:
            import colorama
            colorama.init()
            GREEN = colorama.Fore.GREEN
            YELLOW = colorama.Fore.YELLOW
            RED = colorama.Fore.RED
            BLUE = colorama.Fore.BLUE
            RESET = colorama.Style.RESET_ALL
        except ImportError:
            pass
    else:
        GREEN = "\033[92m"
        YELLOW = "\033[93m"
        RED = "\033[91m"
        BLUE = "\033[94m"
        RESET = "\033[0m"
except:
    pass

def print_header():
    """打印安装程序标题"""
    print("\n" + "=" * 60)
    print(f"{GREEN}绿园中学物语：依赖安装程序{RESET}")
    print("=" * 60)
    print("本程序将安装游戏运行所需的所有依赖\n")

def create_virtual_env():
    """创建Python虚拟环境"""
    print(f"\n{BLUE}正在设置Python虚拟环境...{RESET}")
    
    # 检查是否已存在虚拟环境
    venv_dir = "web_venv"
    
    # 判断虚拟环境是否已存在
    if os.path.exists(venv_dir):
        print(f"{YELLOW}检测到已存在的虚拟环境: {venv_dir}{RESET}")
        
        # 获取Python解释器路径
        if platform.system() == "Windows":
            python_path = os.path.join(venv_dir, "Scripts", "python.exe")
        else:
            python_path = os.path.join(venv_dir, "bin", "python")
        
        if os.path.exists(python_path):
            print(f"{GREEN}使用现有虚拟环境: {venv_dir}{RESET}")
            return True, python_path
    
    # 创建新的虚拟环境
    try:
        print(f"{YELLOW}创建新的虚拟环境: {venv_dir}{RESET}")
        subprocess.run([sys.executable, "-m", "venv", venv_dir], check=True)
        
        # 获取Python解释器路径
        if platform.system() == "Windows":
            python_path = os.path.join(venv_dir, "Scripts", "python.exe")
        else:
            python_path = os.path.join(venv_dir, "bin", "python")
        
        print(f"{GREEN}虚拟环境创建成功: {venv_dir}{RESET}")
        return True, python_path
    except Exception as e:
        print(f"{RED}虚拟环境创建失败: {str(e)}{RESET}")
        print(f"{YELLOW}将使用系统Python继续安装{RESET}")
        return False, sys.executable

def install_dependencies(python_path=None):
    """安装项目依赖"""
    if not python_path:
        python_path = sys.executable
    
    print(f"{BLUE}开始安装项目依赖...{RESET}")
    
    try:
        # 首先更新pip
        print(f"{BLUE}更新pip...{RESET}")
        subprocess.run([python_path, "-m", "pip", "install", "--upgrade", "pip"], check=True)
        
        # 尝试直接从requirements.txt安装
        requirements_path = os.path.join(ROOT_DIR, "web_app", "requirements.txt")
        if os.path.exists(requirements_path):
            print(f"{BLUE}从requirements.txt安装依赖...{RESET}")
            try:
                subprocess.run(
                    [python_path, "-m", "pip", "install", "--prefer-binary", "-r", requirements_path],
                    check=True
                )
                print(f"{GREEN}所有依赖安装成功{RESET}")
                return True
            except subprocess.CalledProcessError:
                print(f"{YELLOW}通过requirements.txt安装依赖失败，尝试单独安装关键依赖...{RESET}")
        
        # 单独安装关键依赖
        required_packages = [
            "flask",
            "openai",
            "pyyaml",
            "python-dotenv",
            "pillow",
            "requests",
            "colorama",
            "jieba",
            "snownlp"
        ]
        
        success_count = 0
        for package in required_packages:
            try:
                print(f"{BLUE}安装包: {package}{RESET}")
                subprocess.run([python_path, "-m", "pip", "install", "--prefer-binary", package], check=True)
                success_count += 1
                print(f"{GREEN}成功安装 {package}{RESET}")
            except:
                print(f"{YELLOW}警告: {package} 安装失败{RESET}")
        
        print(f"{GREEN}成功安装了 {success_count}/{len(required_packages)} 个依赖包{RESET}")
        return success_count == len(required_packages)
        
    except Exception as e:
        print(f"{RED}安装依赖失败: {str(e)}{RESET}")
        return False

def setup_env_file():
    """设置环境变量文件"""
    print(f"{YELLOW}检查环境变量设置...{RESET}")
    
    env_path = os.path.join(ROOT_DIR, ".env")
    env_example_path = os.path.join(ROOT_DIR, ".env.example")
    
    # 如果.env已存在，不做任何操作
    if os.path.exists(env_path):
        print(f"{GREEN}.env文件已存在，跳过设置{RESET}")
        return True
    
    # 如果.env.example存在，复制为.env
    if os.path.exists(env_example_path):
        try:
            with open(env_example_path, 'r', encoding='utf-8') as src:
                content = src.read()
            
            with open(env_path, 'w', encoding='utf-8') as dest:
                dest.write(content)
            
            print(f"{GREEN}已从.env.example创建.env文件{RESET}")
            print(f"{YELLOW}注意: 请编辑.env文件，设置您的API密钥{RESET}")
            return True
        except Exception as e:
            print(f"{RED}创建.env文件失败: {e}{RESET}")
            return False
    else:
        # 手动创建一个基本的.env文件
        try:
            with open(env_path, 'w', encoding='utf-8') as f:
                f.write("# DeepSeek API密钥\n")
                f.write("DEEPSEEK_API_KEY=your-api-key-here\n")
            
            print(f"{GREEN}已创建基本的.env文件{RESET}")
            print(f"{YELLOW}注意: 请编辑.env文件，设置您的API密钥{RESET}")
            return True
        except Exception as e:
            print(f"{RED}创建.env文件失败: {e}{RESET}")
            return False

def main():
    """主函数，协调整个安装过程"""
    print_header()
    
    # 创建虚拟环境
    venv_created, python_path = create_virtual_env()
    
    # 安装依赖
    deps_installed = install_dependencies(python_path)
    
    # 设置环境变量文件
    env_setup = setup_env_file()
    
    # 显示安装结果
    print("\n" + "=" * 60)
    print(f"{GREEN}安装过程完成{RESET}")
    print("=" * 60)
    print(f"虚拟环境: {'创建成功' if venv_created else '使用系统Python'}")
    print(f"依赖安装: {'成功' if deps_installed else '部分失败'}")
    print(f"环境设置: {'完成' if env_setup else '失败'}")
    
    # 提供下一步指导
    print("\n" + "=" * 60)
    print(f"{BLUE}下一步操作:{RESET}")
    print("1. 确保在.env文件中设置了有效的API密钥")
    print("2. 运行游戏:")
    print("   - 命令行版本: python main.py")
    print("   - Web版本: python web_start.py")
    print("=" * 60)

if __name__ == "__main__":
    main() 