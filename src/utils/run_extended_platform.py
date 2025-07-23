#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
钙钛矿材料扩展平台启动脚本
Extended Platform Launcher for Perovskite Materials
"""

import os
import sys
import time
from datetime import datetime
import subprocess

def print_banner():
    """打印启动横幅"""
    print("=" * 70)
    print("🚀 钙钛矿材料扩展平台启动器 v1.0.0")
    print("   Extended Platform Launcher for Perovskite Materials")
    print("=" * 70)
    print("📅 启动时间:", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print("📂 工作目录:", os.getcwd())
    print("🐍 Python版本:", sys.version.split()[0])
    print("=" * 70)

def check_dependencies():
    """检查依赖项"""
    print("\n🔍 检查依赖项...")
    
    required_packages = [
        'numpy', 'matplotlib', 'pandas', 'scipy', 
        'scikit-learn', 'pymatgen', 'tqdm'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} (缺失)")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  缺少依赖项: {', '.join(missing_packages)}")
        print("请运行以下命令安装缺失的依赖项:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    print("\n✅ 所有依赖项已安装")
    return True

def check_files():
    """检查文件完整性"""
    print("\n📁 检查文件完整性...")
    
    required_files = [
        'ml_accelerated_screening.py',
        'multiscale_simulation_platform.py',
        'intelligent_experimental_loop.py',
        'industrial_application.py',
        'integrated_platform.py',
        'demo_extended_platform.py'
    ]
    
    missing_files = []
    
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} (缺失)")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n⚠️  缺少文件: {', '.join(missing_files)}")
        return False
    
    print("\n✅ 所有文件完整")
    return True

def show_menu():
    """显示主菜单"""
    print("\n" + "=" * 50)
    print("🎛️  功能菜单")
    print("=" * 50)
    print("1. 🤖 机器学习加速筛选")
    print("2. 🔬 多尺度仿真平台")
    print("3. 🧪 智能实验闭环")
    print("4. 🏭 产业化应用分析")
    print("5. 🎯 集成平台（完整流程）")
    print("6. 🎬 扩展平台演示")
    print("7. 📊 查看历史结果")
    print("8. 🔧 系统设置")
    print("0. 🚪 退出")
    print("=" * 50)

def run_module(module_name, description):
    """运行指定模块"""
    print(f"\n🚀 启动{description}...")
    print(f"📄 执行文件: {module_name}")
    print("⏳ 加载中...")
    
    try:
        # 导入并运行模块
        if module_name == 'ml_accelerated_screening.py':
            import ml_accelerated_screening
            ml_accelerated_screening.main()
        elif module_name == 'multiscale_simulation_platform.py':
            import multiscale_simulation_platform
            multiscale_simulation_platform.main()
        elif module_name == 'intelligent_experimental_loop.py':
            import intelligent_experimental_loop
            intelligent_experimental_loop.main()
        elif module_name == 'industrial_application.py':
            import industrial_application
            industrial_application.main()
        elif module_name == 'integrated_platform.py':
            import integrated_platform
            integrated_platform.main()
        elif module_name == 'demo_extended_platform.py':
            import demo_extended_platform
            demo_extended_platform.main()
        
        print(f"\n✅ {description}执行完成")
        
    except Exception as e:
        print(f"\n❌ 执行{description}时出错: {e}")
        print("请检查错误信息并重试")

def view_results():
    """查看历史结果"""
    print("\n📊 查看历史结果...")
    
    result_patterns = [
        'ml_predictions.json',
        'multiscale_simulation_report.json',
        'intelligent_experimental_loop_report.json',
        'industrial_analysis_report.json',
        'integrated_workflow_results_*.json',
        'extended_platform_results_*.json'
    ]
    
    found_files = []
    
    for pattern in result_patterns:
        if '*' in pattern:
            # 处理通配符
            import glob
            files = glob.glob(pattern)
            found_files.extend(files)
        else:
            if os.path.exists(pattern):
                found_files.append(pattern)
    
    if found_files:
        print(f"\n📁 找到 {len(found_files)} 个结果文件:")
        for i, file in enumerate(found_files, 1):
            file_size = os.path.getsize(file) / 1024  # KB
            mod_time = datetime.fromtimestamp(os.path.getmtime(file))
            print(f"  {i}. {file} ({file_size:.1f} KB, {mod_time.strftime('%Y-%m-%d %H:%M')})")
        
        choice = input("\n输入文件编号查看内容 (回车跳过): ")
        if choice.isdigit() and 1 <= int(choice) <= len(found_files):
            selected_file = found_files[int(choice) - 1]
            print(f"\n📄 查看文件: {selected_file}")
            
            try:
                with open(selected_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # 如果是JSON文件，格式化显示
                if selected_file.endswith('.json'):
                    import json
                    try:
                        data = json.loads(content)
                        print(json.dumps(data, indent=2, ensure_ascii=False)[:2000] + "...")
                    except:
                        print(content[:2000] + "...")
                else:
                    print(content[:2000] + "...")
                    
            except Exception as e:
                print(f"❌ 读取文件失败: {e}")
    else:
        print("\n📭 未找到历史结果文件")

def system_settings():
    """系统设置"""
    print("\n🔧 系统设置")
    print("-" * 30)
    
    settings = {
        'working_directory': os.getcwd(),
        'python_version': sys.version.split()[0],
        'platform': sys.platform,
        'cpu_count': os.cpu_count(),
        'current_user': os.getenv('USER') or os.getenv('USERNAME') or 'Unknown'
    }
    
    print("📋 系统信息:")
    for key, value in settings.items():
        print(f"  {key}: {value}")
    
    print("\n🎨 可用操作:")
    print("  1. 清理临时文件")
    print("  2. 生成系统报告")
    print("  3. 检查磁盘空间")
    print("  0. 返回主菜单")
    
    choice = input("\n选择操作: ")
    
    if choice == '1':
        clean_temp_files()
    elif choice == '2':
        generate_system_report()
    elif choice == '3':
        check_disk_space()

def clean_temp_files():
    """清理临时文件"""
    print("\n🧹 清理临时文件...")
    
    temp_patterns = [
        '*.png', '*.jpg', '*.svg',  # 图片文件
        '__pycache__', '.pytest_cache',  # Python缓存
        '*.pyc', '*.pyo',  # 编译文件
        '*.tmp', '*.temp'  # 临时文件
    ]
    
    cleaned_count = 0
    
    for pattern in temp_patterns:
        if '*' in pattern:
            import glob
            files = glob.glob(pattern)
            for file in files:
                try:
                    if os.path.isfile(file):
                        os.remove(file)
                        cleaned_count += 1
                        print(f"  ✅ 删除: {file}")
                except:
                    pass
    
    print(f"\n🎉 清理完成，删除 {cleaned_count} 个文件")

def generate_system_report():
    """生成系统报告"""
    print("\n📋 生成系统报告...")
    
    report_content = f"""
钙钛矿材料扩展平台系统报告
=========================

生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

系统信息:
--------
Python版本: {sys.version}
操作系统: {sys.platform}
CPU数量: {os.cpu_count()}
当前用户: {os.getenv('USER') or os.getenv('USERNAME') or 'Unknown'}
工作目录: {os.getcwd()}

文件状态:
--------
"""
    
    # 检查文件
    files = [
        'ml_accelerated_screening.py',
        'multiscale_simulation_platform.py',
        'intelligent_experimental_loop.py',
        'industrial_application.py',
        'integrated_platform.py',
        'demo_extended_platform.py'
    ]
    
    for file in files:
        if os.path.exists(file):
            size = os.path.getsize(file) / 1024
            mod_time = datetime.fromtimestamp(os.path.getmtime(file))
            report_content += f"✅ {file} ({size:.1f} KB, {mod_time.strftime('%Y-%m-%d %H:%M')})\n"
        else:
            report_content += f"❌ {file} (缺失)\n"
    
    report_content += f"\n生成于: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    
    filename = f"system_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    print(f"📄 系统报告已保存至: {filename}")

def check_disk_space():
    """检查磁盘空间"""
    print("\n💽 检查磁盘空间...")
    
    try:
        import shutil
        total, used, free = shutil.disk_usage('.')
        
        print(f"📊 磁盘使用情况:")
        print(f"  总空间: {total // (1024**3):.1f} GB")
        print(f"  已使用: {used // (1024**3):.1f} GB")
        print(f"  可用空间: {free // (1024**3):.1f} GB")
        print(f"  使用率: {(used/total)*100:.1f}%")
        
        if free < 1024**3:  # 小于1GB
            print("⚠️  磁盘空间不足，建议清理文件")
        else:
            print("✅ 磁盘空间充足")
            
    except Exception as e:
        print(f"❌ 检查磁盘空间失败: {e}")

def main():
    """主函数"""
    print_banner()
    
    # 检查系统环境
    if not check_dependencies():
        print("\n❌ 依赖项检查失败，请先安装缺失的依赖项")
        return
    
    if not check_files():
        print("\n❌ 文件完整性检查失败，请确保所有文件都存在")
        return
    
    print("\n🎉 系统检查通过，准备启动...")
    
    # 主循环
    while True:
        show_menu()
        
        try:
            choice = input("\n请选择功能 (0-8): ").strip()
            
            if choice == '0':
                print("\n感谢使用钙钛矿材料扩展平台！")
                print("项目地址: https://github.com/LunaZhang/perovskite-screening")
                print("联系作者: LunaZhang")
                break
            
            elif choice == '1':
                run_module('ml_accelerated_screening.py', '机器学习加速筛选')
            
            elif choice == '2':
                run_module('multiscale_simulation_platform.py', '多尺度仿真平台')
            
            elif choice == '3':
                run_module('intelligent_experimental_loop.py', '智能实验闭环')
            
            elif choice == '4':
                run_module('industrial_application.py', '产业化应用分析')
            
            elif choice == '5':
                run_module('integrated_platform.py', '集成平台')
            
            elif choice == '6':
                run_module('demo_extended_platform.py', '扩展平台演示')
            
            elif choice == '7':
                view_results()
            
            elif choice == '8':
                system_settings()
            
            else:
                print("❌ 无效选择，请重试")
            
            # 询问是否继续
            if choice not in ['0', '7', '8']:
                continue_choice = input("\n是否继续使用？(y/n): ").strip().lower()
                if continue_choice == 'n':
                    break
                    
        except KeyboardInterrupt:
            print("\n\n👋 用户中断，退出程序")
            break
        except Exception as e:
            print(f"\n❌ 程序执行错误: {e}")
            print("请重试或联系技术支持")

if __name__ == "__main__":
    main() 