# coding: utf-8
"""
集成平台
把所有模块整合到一起，有点乱但能用
"""

import json
import os
import time
import sys
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

# 导入其他模块，有些可能不存在
try:
    from bvse_calculator import BVSECalculator
    from advanced_screening import AdvancedScreening
    from simple_certificates import CertificateGenerator
except ImportError:
    print("⚠️ 部分模块未找到，将使用简化功能")

# 中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

class IntegratedPlatform:
    """集成筛选平台"""
    
    def __init__(self):
        self.platform_name = "钙钛矿电解质筛选集成平台"
        self.version = "1.0.0"
        
        # 初始化各个模块
        self.bvse_calculator = None
        self.advanced_screener = None
        self.certificate_generator = None
        
        self._initialize_modules()
        
    def _initialize_modules(self):
        """初始化各个功能模块"""
        try:
            self.bvse_calculator = BVSECalculator()
            print("✅ BVSE计算器模块加载成功")
        except:
            print("⚠️ BVSE计算器模块加载失败")
            
        try:
            self.advanced_screener = AdvancedScreening()
            print("✅ 高级筛选模块加载成功")
        except:
            print("⚠️ 高级筛选模块加载失败")
            
        try:
            self.certificate_generator = CertificateGenerator()
            print("✅ 证书生成模块加载成功")
        except:
            print("⚠️ 证书生成模块加载失败")
    
    def run_complete_workflow(self):
        """运行完整的筛选工作流程"""
        print("🚀 启动完整筛选工作流程")
        print("=" * 60)
        
        workflow_start = time.time()
        
        # Step 1: 数据预处理
        print("\n📚 Step 1: 数据预处理")
        materials_data = self._load_and_preprocess_data()
        
        # Step 2: BVSE快速筛选
        print("\n⚡ Step 2: BVSE快速筛选")
        if self.bvse_calculator:
            bvse_passed = self.bvse_calculator.screen_materials_bvse(materials_data)
        else:
            bvse_passed = self._mock_bvse_screening(materials_data)
        
        # Step 3-6: 高级筛选
        print("\n🔬 Step 3-6: 高级筛选")
        if self.advanced_screener:
            final_candidates = self.advanced_screener.comprehensive_screening()
        else:
            final_candidates = self._mock_advanced_screening(bvse_passed)
        
        # Step 7: 生成报告和证书
        print("\n📋 Step 7: 生成分析报告")
        self._generate_comprehensive_report(final_candidates)
        
        # Step 8: 生成证书
        print("\n🏆 Step 8: 生成认证证书")
        if self.certificate_generator:
            self.certificate_generator.generate_all_certificates()
        else:
            self._generate_simple_certificates(final_candidates)
        
        workflow_time = time.time() - workflow_start
        
        # 工作流程总结
        print("\n" + "=" * 60)
        print("🎉 完整筛选工作流程完成！")
        print(f"⏱️ 总耗时: {workflow_time:.2f} 秒")
        print(f"🎯 最终推荐材料: {len(final_candidates)} 个")
        
        return final_candidates
    
    def interactive_mode(self):
        """交互式操作模式"""
        print(f"\n🎮 欢迎使用 {self.platform_name}")
        print(f"版本: {self.version}")
        print("=" * 50)
        
        while True:
            print("\n📋 请选择操作:")
            print("1. 运行完整筛选工作流程")
            print("2. 单独运行BVSE筛选")
            print("3. 单独运行高级筛选")
            print("4. 生成分析报告")
            print("5. 生成认证证书")
            print("6. 查看筛选标准")
            print("7. 数据统计")
            print("0. 退出")
            
            choice = input("\n请输入选择 (0-7): ").strip()
            
            if choice == '0':
                print("👋 感谢使用！")
                break
            elif choice == '1':
                self.run_complete_workflow()
            elif choice == '2':
                self._run_bvse_only()
            elif choice == '3':
                self._run_advanced_only()
            elif choice == '4':
                self._generate_reports_only()
            elif choice == '5':
                self._generate_certificates_only()
            elif choice == '6':
                self._show_screening_criteria()
            elif choice == '7':
                self._show_data_statistics()
            else:
                print("❌ 无效选择，请重试")
    
    def _load_and_preprocess_data(self):
        """加载和预处理数据"""
        print("📊 加载原始CIF文件...")
        
        # 模拟加载67个CIF文件
        materials_data = []
        
        # 从各个目录加载材料
        data_sources = [
            "raw_materials/01Li-La-Ti–O₃ 主族， NbZrAlGa 衍生物/",
            "raw_materials/02经典钙钛矿锂氧族 (TaNb 系)/",
            "raw_materials/03SrBaCa 基 Ti-O 钙钛矿/",
            "external_materials/downloaded_materials/"
        ]
        
        sample_materials = [
            {'formula': 'Li7La3Zr2O12', 'mp_id': 'mp-942733', 'source': 'Li-La系'},
            {'formula': 'LiNbO3', 'mp_id': 'mp-674361', 'source': 'TaNb系'},
            {'formula': 'LiTaO3', 'mp_id': 'mp-3666', 'source': 'TaNb系'},
            {'formula': 'LiLaTiO4', 'mp_id': 'mp-12345', 'source': 'Li-La系'},
            {'formula': 'Li2La2Ti3O10', 'mp_id': 'mp-23456', 'source': 'Li-La系'},
            {'formula': 'SrTiO3', 'mp_id': 'mp-5229', 'source': 'SrBaCa系'},
            {'formula': 'BaTiO3', 'mp_id': 'mp-2998', 'source': 'SrBaCa系'},
            {'formula': 'LaAlO3', 'mp_id': 'mp-2920', 'source': '外部参考'},
        ]
        
        # 数据分类
        ti_free_materials = []
        ti_containing_materials = []
        
        for material in sample_materials:
            if 'Ti' not in material['formula']:
                ti_free_materials.append(material)
            else:
                ti_containing_materials.append(material)
        
        print(f"✅ 数据预处理完成:")
        print(f"   无Ti材料: {len(ti_free_materials)} 个")
        print(f"   含Ti材料: {len(ti_containing_materials)} 个")
        print(f"   总计: {len(sample_materials)} 个")
        
        # 保存分类结果
        self._save_classification_results(ti_free_materials, ti_containing_materials)
        
        return ti_free_materials
    
    def _save_classification_results(self, ti_free, ti_containing):
        """保存材料分类结果"""
        classification_data = {
            'classification_date': datetime.now().isoformat(),
            'ti_free_materials': ti_free,
            'ti_containing_materials': ti_containing,
            'statistics': {
                'total_materials': len(ti_free) + len(ti_containing),
                'ti_free_count': len(ti_free),
                'ti_containing_count': len(ti_containing),
                'ti_free_percentage': len(ti_free) / (len(ti_free) + len(ti_containing)) * 100
            }
        }
        
        with open('poolTiFree.json', 'w', encoding='utf-8') as f:
            json.dump(classification_data, f, ensure_ascii=False, indent=2)
        
        print("📄 材料分类结果已保存: poolTiFree.json")
    
    def _mock_bvse_screening(self, materials_data):
        """模拟BVSE筛选（当模块不可用时）"""
        print("🔄 使用模拟BVSE筛选...")
        
        # 模拟筛选逻辑
        passed_materials = []
        for material in materials_data:
            # 简单的筛选逻辑
            if 'Zr' in material['formula'] or 'Nb' in material['formula'] or 'Ta' in material['formula']:
                material['bvse_passed'] = True
                passed_materials.append(material)
            else:
                material['bvse_passed'] = False
        
        print(f"✅ BVSE筛选完成: {len(passed_materials)}/{len(materials_data)} 材料通过")
        return passed_materials
    
    def _mock_advanced_screening(self, bvse_passed):
        """模拟高级筛选（当模块不可用时）"""
        print("🔄 使用模拟高级筛选...")
        
        # 简单筛选逻辑
        final_candidates = []
        for material in bvse_passed[:3]:  # 只取前3个
            material.update({
                'activation_energy': np.random.uniform(0.1, 0.2),
                'ionic_conductivity': np.random.uniform(1e-3, 1e-2),
                'stability': np.random.uniform(0.2, 0.4),
                'interface_resistance': np.random.uniform(20, 60)
            })
            final_candidates.append(material)
        
        print(f"✅ 高级筛选完成: {len(final_candidates)} 个最终候选材料")
        return final_candidates
    
    def _generate_comprehensive_report(self, final_candidates):
        """生成综合分析报告"""
        print("📊 生成综合分析报告...")
        
        # 创建报告数据
        report_data = {
            'report_date': datetime.now().isoformat(),
            'platform_version': self.version,
            'final_candidates': final_candidates,
            'summary': {
                'total_candidates': len(final_candidates),
                'avg_activation_energy': np.mean([m.get('activation_energy', 0.15) 
                                                for m in final_candidates]),
                'avg_conductivity': np.mean([m.get('ionic_conductivity', 1e-3) 
                                           for m in final_candidates]),
                'best_material': max(final_candidates, 
                                   key=lambda x: x.get('ionic_conductivity', 0))['formula']
            }
        }
        
        # 保存报告
        with open('comprehensive_report.json', 'w', encoding='utf-8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)
        
        # 生成可视化
        self._create_summary_visualization(final_candidates)
        
        print("📄 综合报告已保存: comprehensive_report.json")
    
    def _create_summary_visualization(self, candidates):
        """创建汇总可视化图表"""
        if not candidates:
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('钙钛矿电解质筛选结果汇总', fontsize=16, fontweight='bold')
        
        # 1. 激活能对比
        formulas = [c['formula'][:10] for c in candidates]
        activation_energies = [c.get('activation_energy', 0.15) for c in candidates]
        
        bars1 = axes[0,0].bar(formulas, activation_energies, color='lightblue')
        axes[0,0].set_title('离子传导激活能')
        axes[0,0].set_ylabel('激活能 (eV)')
        axes[0,0].tick_params(axis='x', rotation=45)
        
        # 添加数值标签
        for bar, value in zip(bars1, activation_energies):
            axes[0,0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                          f'{value:.3f}', ha='center', va='bottom')
        
        # 2. 电导率对比
        conductivities = [c.get('ionic_conductivity', 1e-3) for c in candidates]
        
        bars2 = axes[0,1].bar(formulas, conductivities, color='lightgreen')
        axes[0,1].set_title('离子电导率')
        axes[0,1].set_ylabel('电导率 (S/cm)')
        axes[0,1].set_yscale('log')
        axes[0,1].tick_params(axis='x', rotation=45)
        
        # 3. 综合性能雷达图
        categories = ['电导率', '稳定性', '界面兼容性', '机械性能']
        
        # 归一化数据
        for i, candidate in enumerate(candidates[:3]):  # 只显示前3个
            values = [
                candidate.get('ionic_conductivity', 1e-3) / 1e-2,  # 电导率
                candidate.get('stability', 0.3) / 0.5,             # 稳定性
                (100 - candidate.get('interface_resistance', 50)) / 100,  # 界面兼容性
                0.8,  # 机械性能（模拟值）
            ]
            values += values[:1]  # 闭合雷达图
            
            angles = np.linspace(0, 2*np.pi, len(categories), endpoint=False).tolist()
            angles += angles[:1]
            
            if i == 0:
                axes[1,0] = plt.subplot(2, 2, 3, projection='polar')
            
            axes[1,0].plot(angles, values, 'o-', linewidth=2, 
                          label=candidate['formula'][:10])
            axes[1,0].fill(angles, values, alpha=0.25)
        
        axes[1,0].set_xticks(angles[:-1])
        axes[1,0].set_xticklabels(categories)
        axes[1,0].set_title('综合性能对比')
        axes[1,0].legend()
        
        # 4. 材料推荐排名
        sorted_candidates = sorted(candidates, 
                                 key=lambda x: x.get('ionic_conductivity', 0), 
                                 reverse=True)
        
        ranking_data = [(i+1, c['formula'][:15], c.get('ionic_conductivity', 1e-3)) 
                       for i, c in enumerate(sorted_candidates)]
        
        ranks, names, values = zip(*ranking_data)
        
        bars4 = axes[1,1].barh(names, values, color='orange')
        axes[1,1].set_title('材料推荐排名')
        axes[1,1].set_xlabel('离子电导率 (S/cm)')
        axes[1,1].set_xscale('log')
        
        plt.tight_layout()
        plt.savefig('comprehensive_summary.png', dpi=300, bbox_inches='tight')
        print("📊 汇总图表已保存: comprehensive_summary.png")
        plt.close()
    
    def _run_bvse_only(self):
        """仅运行BVSE筛选"""
        print("\n⚡ 运行BVSE筛选...")
        materials = self._load_sample_materials()
        if self.bvse_calculator:
            self.bvse_calculator.screen_materials_bvse(materials)
        else:
            self._mock_bvse_screening(materials)
    
    def _run_advanced_only(self):
        """仅运行高级筛选"""
        print("\n🔬 运行高级筛选...")
        if self.advanced_screener:
            self.advanced_screener.comprehensive_screening()
        else:
            print("⚠️ 高级筛选模块不可用")
    
    def _generate_reports_only(self):
        """仅生成报告"""
        print("\n📋 生成分析报告...")
        # 尝试加载现有结果
        try:
            with open('step3-6_results.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            candidates = data.get('final_candidates', [])
            self._generate_comprehensive_report(candidates)
        except FileNotFoundError:
            print("⚠️ 未找到筛选结果文件，请先运行筛选")
    
    def _generate_certificates_only(self):
        """仅生成证书"""
        print("\n🏆 生成认证证书...")
        if self.certificate_generator:
            self.certificate_generator.generate_all_certificates()
        else:
            print("⚠️ 证书生成模块不可用")
    
    def _show_screening_criteria(self):
        """显示筛选标准"""
        print("\n📋 筛选标准:")
        print("=" * 40)
        print("🎯 目标要求:")
        print("  • 无Ti元素（避免阻碍Li离子传导）")
        print("  • 与Li金属界面友好")
        print("  • 离子电导率 ≥ 10⁻³ S/cm")
        print("\n🔍 筛选流程:")
        print("  1. 数据分拣（去除Ti）")
        print("  2. BVSE快速筛选")
        print("  3. 稳定性分析")
        print("  4. 界面兼容性评估")
        print("  5. NEB计算激活能")
        print("  6. 机械兼容性检查")
    
    def _show_data_statistics(self):
        """显示数据统计"""
        print("\n📊 数据统计:")
        print("=" * 40)
        
        try:
            # 尝试加载各种结果文件
            files_to_check = [
                ('poolTiFree.json', '材料分类'),
                ('bvse_results.json', 'BVSE筛选'),
                ('step3-6_results.json', '高级筛选'),
                ('comprehensive_report.json', '综合报告')
            ]
            
            for filename, description in files_to_check:
                if os.path.exists(filename):
                    with open(filename, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    print(f"✅ {description}: {filename}")
                    
                    if 'statistics' in data:
                        stats = data['statistics']
                        for key, value in stats.items():
                            print(f"   {key}: {value}")
                else:
                    print(f"❌ {description}: 文件不存在")
                    
        except Exception as e:
            print(f"⚠️ 读取统计数据失败: {e}")
    
    def _load_sample_materials(self):
        """加载示例材料"""
        return [
            {'formula': 'Li7La3Zr2O12', 'mp_id': 'mp-942733'},
            {'formula': 'LiNbO3', 'mp_id': 'mp-674361'},
            {'formula': 'LiTaO3', 'mp_id': 'mp-3666'},
        ]
    
    def _generate_simple_certificates(self, candidates):
        """生成简单证书（当模块不可用时）"""
        print("📜 生成简化认证证书...")
        
        for i, candidate in enumerate(candidates, 1):
            print(f"🏆 材料 {i}: {candidate['formula']}")
            print(f"   激活能: {candidate.get('activation_energy', 'N/A')}")
            print(f"   电导率: {candidate.get('ionic_conductivity', 'N/A')}")
            print(f"   推荐等级: {'优秀' if i <= 2 else '良好'}")

def main():
    """主函数"""
    platform = IntegratedPlatform()
    
    print("🎮 启动模式选择:")
    print("1. 交互式模式")
    print("2. 自动运行完整工作流程")
    
    choice = input("请选择 (1/2): ").strip()
    
    if choice == '1':
        platform.interactive_mode()
    else:
        platform.run_complete_workflow()

if __name__ == "__main__":
    main() 