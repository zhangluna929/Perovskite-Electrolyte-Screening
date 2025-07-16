# coding: utf-8
"""
平台运行器
主菜单，把所有模块整合起来
"""

import os
import sys
import time
import json
from datetime import datetime

def print_banner():
    # 欢迎界面 用box字符画的
    banner = """
    ╔════════════════════════════════════════════════════════════════╗
    ║                  钙钛矿电解质筛选扩展平台                      ║
    ║                Perovskite Electrolyte Screening Platform       ║
    ║                                                                ║
    ║                         版本 1.0.0                            ║
    ╚════════════════════════════════════════════════════════════════╝
    """
    print(banner)

def show_main_menu():
    """显示主菜单"""
    print("\n🎯 主菜单 - 请选择功能模块:")
    print("=" * 60)
    print("1. 🔍 BVSE快速筛选")
    print("2. 🔬 高级筛选流程")
    print("3. 🤖 机器学习加速筛选")
    print("4. 🏭 产业化应用分析")
    print("5. 🌐 Web界面启动")
    print("6. 🏆 生成认证证书")
    print("7. 📊 扩展平台演示")
    print("8. 🔧 集成平台运行")
    print("9. ⚙️ 系统设置")
    print("0. 👋 退出程序")
    print("=" * 60)

def run_bvse_screening():
    print("\n⚡ 启动BVSE快速筛选...")
    try:
        from bvse_calculator import BVSECalculator
        calc = BVSECalculator()
        mats = calc.load_ti_free_materials()  # 加载无Ti材料
        results = calc.screen_materials_bvse(mats)
        print(f"✅ BVSE筛选完成，通过筛选: {len(results)} 个材料")
    except ImportError:
        print("⚠️ BVSE模块未找到，请检查文件是否存在")
    except Exception as e:
        print(f"❌ BVSE筛选出错: {e}")

def run_advanced_screening():
    """运行高级筛选"""
    print("\n🔬 启动高级筛选流程...")
    try:
        from advanced_screening import AdvancedScreening
        screener = AdvancedScreening()
        results = screener.comprehensive_screening()
        print(f"✅ 高级筛选完成，最终候选: {len(results)} 个材料")
    except ImportError:
        print("⚠️ 高级筛选模块未找到，请检查文件是否存在")
    except Exception as e:
        print(f"❌ 高级筛选出错: {e}")

def run_ml_screening():
    """运行机器学习筛选"""
    print("\n🤖 启动机器学习加速筛选...")
    try:
        from ml_enhanced_screening import MLEnhancedScreening
        ml_screener = MLEnhancedScreening()
        
        # 创建测试材料池
        materials_pool = [
            {'formula': 'Li7La3Zr2O12'},
            {'formula': 'LiNbO3'},
            {'formula': 'LiTaO3'},
            {'formula': 'Li2La2Ti3O10'},
            {'formula': 'LiLaTiO4'},
        ]
        
        results = ml_screener.ml_accelerated_screening(materials_pool)
        print(f"✅ ML筛选完成，发现候选: {len(results)} 个材料")
    except ImportError:
        print("⚠️ ML筛选模块未找到，请检查文件是否存在")
        print("💡 提示: 需要安装scikit-learn: pip install scikit-learn")
    except Exception as e:
        print(f"❌ ML筛选出错: {e}")

def run_industrial_analysis():
    """运行产业化分析"""
    print("\n🏭 启动产业化应用分析...")
    try:
        from industrial_application import IndustrialApplication
        analyzer = IndustrialApplication()
        analyzer.run_complete_analysis()
        print("✅ 产业化分析完成")
    except ImportError:
        print("⚠️ 产业化分析模块未找到，请检查文件是否存在")
    except Exception as e:
        print(f"❌ 产业化分析出错: {e}")

def run_web_interface():
    """启动Web界面"""
    print("\n🌐 启动Web界面...")
    try:
        from web_interface import app
        print("🚀 Web服务器启动中...")
        print("📱 访问地址: http://localhost:5000")
        print("⏹️ 按 Ctrl+C 停止服务器")
        app.run(debug=True, host='0.0.0.0', port=5000)
    except ImportError:
        print("⚠️ Web界面模块未找到，请检查文件是否存在")
        print("💡 提示: 需要安装Flask: pip install flask")
    except Exception as e:
        print(f"❌ Web界面启动失败: {e}")

def generate_certificates():
    """生成认证证书"""
    print("\n🏆 生成认证证书...")
    
    print("请选择证书类型:")
    print("1. 简单证书生成")
    print("2. 完整证书套件")
    print("3. 快速证书生成")
    
    choice = input("请选择 (1-3): ").strip()
    
    try:
        if choice == '1':
            from simple_certificates import CertificateGenerator
            generator = CertificateGenerator()
            generator.generate_all_certificates()
        elif choice == '2':
            from simple_certificates import CertificateGenerator
            generator = CertificateGenerator()
            generator.generate_all_certificates()
        elif choice == '3':
            from generate_certificates import generate_batch_certificates, generate_summary_certificate
            generate_batch_certificates()
            generate_summary_certificate()
        else:
            print("❌ 无效选择")
            return
        
        print("✅ 证书生成完成")
    except ImportError:
        print("⚠️ 证书生成模块未找到，请检查文件是否存在")
    except Exception as e:
        print(f"❌ 证书生成出错: {e}")

def run_demo_platform():
    """运行扩展平台演示"""
    print("\n📊 启动扩展平台演示...")
    try:
        import demo_extended_platform
        # 运行演示
        print("✅ 演示运行完成")
    except ImportError:
        print("⚠️ 演示模块未找到，请检查文件是否存在")
    except Exception as e:
        print(f"❌ 演示运行出错: {e}")

def run_integrated_platform():
    """运行集成平台"""
    print("\n🔧 启动集成平台...")
    try:
        from integrated_platform import IntegratedPlatform
        platform = IntegratedPlatform()
        platform.interactive_mode()
    except ImportError:
        print("⚠️ 集成平台模块未找到，请检查文件是否存在")
    except Exception as e:
        print(f"❌ 集成平台出错: {e}")

def show_system_settings():
    """显示系统设置"""
    print("\n⚙️ 系统设置")
    print("=" * 40)
    
    # 检查依赖
    print("📋 依赖检查:")
    dependencies = [
        ('numpy', 'numpy'),
        ('matplotlib', 'matplotlib'),
        ('pandas', 'pandas'), 
        ('scikit-learn', 'sklearn'),
        ('flask', 'flask')
    ]
    
    for name, module in dependencies:
        try:
            __import__(module)
            print(f"  ✅ {name}: 已安装")
        except ImportError:
            print(f"  ❌ {name}: 未安装")
    
    # 检查文件
    print("\n📁 模块文件检查:")
    modules = [
        'bvse_calculator.py',
        'advanced_screening.py',
        'ml_enhanced_screening.py',
        'industrial_application.py',
        'web_interface.py',
        'simple_certificates.py',
        'generate_certificates.py',
        'integrated_platform.py',
        'demo_extended_platform.py'
    ]
    
    for module in modules:
        if os.path.exists(module):
            print(f"  ✅ {module}: 存在")
        else:
            print(f"  ❌ {module}: 缺失")
    
    # 检查数据文件
    print("\n📊 数据文件检查:")
    data_files = [
        'poolTiFree.json',
        'bvse_results.json', 
        'step3-6_results.json',
        'ml_predictions.json'
    ]
    
    for data_file in data_files:
        if os.path.exists(data_file):
            try:
                with open(data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                print(f"  ✅ {data_file}: 存在且有效")
            except:
                print(f"  ⚠️ {data_file}: 存在但格式错误")
        else:
            print(f"  ❌ {data_file}: 不存在")

def create_sample_data():
    """创建示例数据文件"""
    print("\n🔧 创建示例数据文件...")
    
    # 创建基础材料池
    sample_materials = {
        'creation_date': datetime.now().isoformat(),
        'materials': [
            {'formula': 'Li7La3Zr2O12', 'mp_id': 'mp-942733'},
            {'formula': 'LiNbO3', 'mp_id': 'mp-674361'},
            {'formula': 'LiTaO3', 'mp_id': 'mp-3666'},
            {'formula': 'Li2La2Ti3O10', 'mp_id': 'mp-23456'},
            {'formula': 'LiLaTiO4', 'mp_id': 'mp-12345'},
        ]
    }
    
    with open('poolTiFree.json', 'w', encoding='utf-8') as f:
        json.dump(sample_materials, f, ensure_ascii=False, indent=2)
    
    print("✅ 示例数据文件已创建: poolTiFree.json")

def main():
    """主函数"""
    print_banner()
    
    while True:
        show_main_menu()
        
        try:
            choice = input("\n请输入选择 (0-9): ").strip()
            
            if choice == '0':
                print("\n👋 感谢使用钙钛矿电解质筛选平台！")
                print("🔬 祝您科研顺利！")
                break
            elif choice == '1':
                run_bvse_screening()
            elif choice == '2':
                run_advanced_screening()
            elif choice == '3':
                run_ml_screening()
            elif choice == '4':
                run_industrial_analysis()
            elif choice == '5':
                run_web_interface()
            elif choice == '6':
                generate_certificates()
            elif choice == '7':
                run_demo_platform()
            elif choice == '8':
                run_integrated_platform()
            elif choice == '9':
                show_system_settings()
                
                # 提供创建示例数据的选项
                create_data = input("\n是否创建示例数据文件? (y/n): ").strip().lower()
                if create_data == 'y':
                    create_sample_data()
                    
            else:
                print("❌ 无效选择，请输入 0-9 之间的数字")
                
        except KeyboardInterrupt:
            print("\n\n⏹️ 程序被用户中断")
            break
        except Exception as e:
            print(f"\n❌ 程序出错: {e}")
            
        # 暂停一下，让用户看到结果
        input("\n按Enter键继续...")

if __name__ == "__main__":
    main() 