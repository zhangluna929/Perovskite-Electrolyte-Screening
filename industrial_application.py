# coding: utf-8
"""
产业化应用分析模块
包含成本分析、市场预测等，数据有些是估算的
"""

import json
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import pandas as pd

# 中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

class IndustrialApplication:
    
    def __init__(self):
        # 成本模型 价格从网上查的，可能不太准
        self.cost_model = {
            'raw_materials': {'Li2CO3': 150000, 'La2O3': 50000, 'ZrO2': 8000},  # 元/吨
            'energy_cost': 0.6,  # 元/kWh
            'labor_cost': 300,   # 元/人·天
            'equipment_depreciation': 0.1,  # 年折旧率
        }
        
        # 市场数据 一些是估算的
        self.market_data = {
            'current_market_size': 2.5,  # 亿元
            'growth_rate': 0.25,         # 年增长率25%
            'target_price': 5000,        # 元/kg 目标售价
            'competition_level': 0.3     # 竞争激烈程度
        }
        
    def cost_analysis(self, material_formula, production_scale=1000):
        print(f"💰 分析 {material_formula} 的生产成本...")
        print(f"📊 生产规模: {production_scale} kg/年")
        # TODO: 成本计算还需要优化
        
        # 原材料成本
        raw_material_cost = self._calculate_raw_material_cost(material_formula, production_scale)
        
        # 能源成本
        energy_cost = self._calculate_energy_cost(production_scale)
        
        # 人工成本
        labor_cost = self._calculate_labor_cost(production_scale)
        
        # 设备折旧
        equipment_cost = self._calculate_equipment_cost(production_scale)
        
        # 其他成本
        other_cost = (raw_material_cost + energy_cost + labor_cost + equipment_cost) * 0.2
        
        total_cost = raw_material_cost + energy_cost + labor_cost + equipment_cost + other_cost
        unit_cost = total_cost / production_scale
        
        cost_breakdown = {
            'raw_materials': raw_material_cost,
            'energy': energy_cost,
            'labor': labor_cost,
            'equipment': equipment_cost,
            'other': other_cost,
            'total': total_cost,
            'unit_cost': unit_cost  # 元/kg
        }
        
        print(f"📋 成本分析结果:")
        print(f"  原材料成本: ¥{raw_material_cost:,.0f}")
        print(f"  能源成本: ¥{energy_cost:,.0f}")
        print(f"  人工成本: ¥{labor_cost:,.0f}")
        print(f"  设备折旧: ¥{equipment_cost:,.0f}")
        print(f"  其他成本: ¥{other_cost:,.0f}")
        print(f"  总成本: ¥{total_cost:,.0f}")
        print(f"  单位成本: ¥{unit_cost:,.0f}/kg")
        
        return cost_breakdown
    
    def market_analysis(self, material_name):
        """市场分析"""
        print(f"📈 {material_name} 市场分析...")
        
        # 市场规模预测
        years = list(range(2024, 2030))
        market_sizes = []
        current_size = self.market_data['current_market_size']
        growth_rate = self.market_data['growth_rate']
        
        for i, year in enumerate(years):
            size = current_size * ((1 + growth_rate) ** i)
            market_sizes.append(size)
        
        # 价格趋势预测
        price_trend = self._predict_price_trend(material_name)
        
        # 竞争分析
        competition_analysis = self._analyze_competition(material_name)
        
        market_data = {
            'years': years,
            'market_sizes': market_sizes,
            'price_trend': price_trend,
            'competition': competition_analysis,
            'roi_projection': self._calculate_roi_projection(market_sizes)
        }
        
        print(f"📊 市场分析结果:")
        print(f"  当前市场规模: {current_size:.1f}亿元")
        print(f"  预计2029年市场规模: {market_sizes[-1]:.1f}亿元")
        print(f"  年复合增长率: {growth_rate*100:.0f}%")
        print(f"  预计投资回收期: {market_data['roi_projection']['payback_period']:.1f}年")
        
        return market_data
    
    def quality_control_system(self, material_name):
        """质量控制体系"""
        print(f"🔍 设计 {material_name} 质量控制体系...")
        
        # 质量控制标准
        qc_standards = {
            'ionic_conductivity': {'min': 1e-3, 'target': 5e-3, 'test_method': 'EIS'},
            'purity': {'min': 99.5, 'target': 99.9, 'test_method': 'XRF'},
            'particle_size': {'min': 1, 'max': 50, 'target': 10, 'test_method': 'Laser_Diffraction'},
            'density': {'min': 95, 'target': 98, 'test_method': 'Archimedes'},
            'moisture': {'max': 0.1, 'test_method': 'Karl_Fischer'}
        }
        
        # 生产工艺控制点
        process_control = {
            'raw_material_inspection': ['化学成分', '纯度', '粒度'],
            'mixing_process': ['混合时间', '混合速度', '温度控制'],
            'sintering_process': ['升温速率', '保温温度', '保温时间', '气氛控制'],
            'cooling_process': ['冷却速率', '最终温度'],
            'final_inspection': ['电导率', '密度', '相纯度', '微观结构']
        }
        
        # 统计过程控制(SPC)
        spc_charts = self._generate_spc_charts()
        
        qc_system = {
            'standards': qc_standards,
            'process_control': process_control,
            'spc_charts': spc_charts,
            'certification_requirements': self._get_certification_requirements()
        }
        
        print(f"✅ 质量控制体系设计完成")
        print(f"  控制参数: {len(qc_standards)} 个")
        print(f"  工艺控制点: {len(process_control)} 个")
        
        return qc_system
    
    def certification_roadmap(self, material_name):
        """标准化认证路线"""
        print(f"📋 制定 {material_name} 认证路线...")
        
        # 认证路径
        certification_path = [
            {
                'stage': '实验室认证',
                'duration': '3-6个月',
                'requirements': ['性能测试', '安全评估', '环境影响'],
                'cost': '50-100万元',
                'standards': ['GB/T', '行业标准']
            },
            {
                'stage': '中试验证',
                'duration': '6-12个月', 
                'requirements': ['工艺稳定性', '批次一致性', '规模化可行性'],
                'cost': '200-500万元',
                'standards': ['ISO 9001', 'GMP']
            },
            {
                'stage': '产品认证',
                'duration': '12-18个月',
                'requirements': ['型式试验', '生产一致性', '质量管理体系'],
                'cost': '100-300万元',
                'standards': ['UL', 'CE', 'CCC']
            },
            {
                'stage': '市场准入',
                'duration': '6-12个月',
                'requirements': ['法规符合性', '知识产权', '市场准入许可'],
                'cost': '50-200万元',
                'standards': ['FDA', 'REACH']
            }
        ]
        
        # 总体时间线
        total_duration = 27  # 最长48个月
        total_cost = 900   # 最高1100万元
        
        roadmap = {
            'certification_path': certification_path,
            'total_duration_months': total_duration,
            'total_cost_million': total_cost,
            'key_milestones': self._define_milestones(),
            'risk_assessment': self._assess_certification_risks()
        }
        
        print(f"🎯 认证路线制定完成:")
        print(f"  预计总时长: {total_duration}个月")
        print(f"  预计总投入: {total_cost}万元")
        print(f"  关键里程碑: {len(roadmap['key_milestones'])}个")
        
        return roadmap
    
    def run_complete_analysis(self):
        """运行完整的产业化分析"""
        print("🏭 开始完整产业化应用分析...")
        print("=" * 60)
        
        # 分析目标材料
        target_material = "Li7La3Zr2O12"
        production_scale = 10000  # kg/年
        
        # 1. 成本分析
        print("\n💰 Step 1: 成本分析")
        cost_data = self.cost_analysis(target_material, production_scale)
        
        # 2. 市场分析
        print("\n📈 Step 2: 市场分析")
        market_data = self.market_analysis(target_material)
        
        # 3. 质量控制
        print("\n🔍 Step 3: 质量控制体系")
        qc_data = self.quality_control_system(target_material)
        
        # 4. 认证路线
        print("\n📋 Step 4: 认证路线规划")
        cert_data = self.certification_roadmap(target_material)
        
        # 5. 综合评估
        print("\n🎯 Step 5: 综合评估")
        business_case = self._generate_business_case(cost_data, market_data, cert_data)
        
        # 保存分析结果
        analysis_result = {
            'analysis_date': datetime.now().isoformat(),
            'target_material': target_material,
            'production_scale': production_scale,
            'cost_analysis': cost_data,
            'market_analysis': market_data,
            'quality_control': qc_data,
            'certification_roadmap': cert_data,
            'business_case': business_case
        }
        
        with open('industrial_analysis_report.json', 'w', encoding='utf-8') as f:
            json.dump(analysis_result, f, ensure_ascii=False, indent=2)
        
        # 生成可视化报告
        self._generate_industrial_visualization(analysis_result)
        
        print(f"\n🎉 完整产业化分析完成！")
        print("📄 分析报告已保存: industrial_analysis_report.json")
        
        return analysis_result
    
    def _calculate_raw_material_cost(self, formula, scale):
        """计算原材料成本"""
        # 简化的成本计算
        if 'Li7La3Zr2O12' in formula:
            # LLZO的原材料成本
            li_cost = 150000 * 0.05 * scale / 1000  # Li2CO3
            la_cost = 50000 * 0.3 * scale / 1000    # La2O3
            zr_cost = 8000 * 0.2 * scale / 1000     # ZrO2
            return li_cost + la_cost + zr_cost
        else:
            # 其他材料的估算成本
            return 30000 * scale / 1000
    
    def _calculate_energy_cost(self, scale):
        """计算能源成本"""
        # 估算每kg产品需要100 kWh能源
        energy_per_kg = 100
        total_energy = energy_per_kg * scale
        return total_energy * self.cost_model['energy_cost']
    
    def _calculate_labor_cost(self, scale):
        """计算人工成本"""
        # 估算每1000kg产品需要10人工作天
        labor_days = scale * 10 / 1000
        return labor_days * self.cost_model['labor_cost']
    
    def _calculate_equipment_cost(self, scale):
        """计算设备折旧成本"""
        # 估算设备投资1000万，年折旧10%
        equipment_investment = 10000000
        annual_depreciation = equipment_investment * self.cost_model['equipment_depreciation']
        return annual_depreciation
    
    def _predict_price_trend(self, material):
        """预测价格趋势"""
        # 简化的价格预测模型
        base_price = 5000  # 元/kg
        years = list(range(2024, 2030))
        prices = []
        
        for i, year in enumerate(years):
            # 考虑学习曲线效应，价格逐年下降
            price = base_price * (0.95 ** i)
            prices.append(price)
        
        return {'years': years, 'prices': prices}
    
    def _analyze_competition(self, material):
        """竞争分析"""
        return {
            'main_competitors': ['公司A', '公司B', '研究所C'],
            'competitive_advantage': ['成本优势', '技术先进', '质量稳定'],
            'market_share_projection': 0.15,  # 预期市场份额15%
            'differentiation_strategy': '高性能低成本'
        }
    
    def _calculate_roi_projection(self, market_sizes):
        """计算ROI预测"""
        investment = 5000  # 万元初始投资
        annual_revenue = market_sizes[2] * 10000 * 0.15  # 第3年收入
        annual_profit = annual_revenue * 0.2  # 利润率20%
        payback_period = investment / annual_profit
        
        return {
            'initial_investment': investment,
            'annual_revenue_projection': annual_revenue,
            'annual_profit_projection': annual_profit,
            'payback_period': payback_period,
            'roi_5_year': (annual_profit * 5 - investment) / investment * 100
        }
    
    def _generate_spc_charts(self):
        """生成统计过程控制图表数据"""
        # 模拟SPC数据
        return {
            'control_limits': {'UCL': 1.2e-3, 'LCL': 0.8e-3, 'CL': 1.0e-3},
            'sample_data': np.random.normal(1.0e-3, 0.1e-3, 30).tolist(),
            'control_status': 'In Control'
        }
    
    def _get_certification_requirements(self):
        """获取认证要求"""
        return {
            'ISO_9001': '质量管理体系',
            'ISO_14001': '环境管理体系', 
            'IATF_16949': '汽车行业质量标准',
            'UL_Certification': '安全认证',
            'CE_Marking': '欧盟符合性声明'
        }
    
    def _define_milestones(self):
        """定义关键里程碑"""
        return [
            {'milestone': '完成实验室测试', 'month': 6},
            {'milestone': '中试线建设完成', 'month': 12},
            {'milestone': '获得产品认证', 'month': 24},
            {'milestone': '实现商业化生产', 'month': 36}
        ]
    
    def _assess_certification_risks(self):
        """评估认证风险"""
        return {
            'technical_risk': '中等',
            'regulatory_risk': '低',
            'market_risk': '中等',
            'financial_risk': '低',
            'mitigation_strategies': ['技术储备', '法规跟踪', '市场调研', '资金规划']
        }
    
    def _generate_business_case(self, cost_data, market_data, cert_data):
        """生成商业案例"""
        # 计算商业可行性
        unit_cost = cost_data['unit_cost']
        target_price = 5000  # 元/kg
        profit_margin = (target_price - unit_cost) / target_price * 100
        
        # 投资回收分析
        total_investment = cert_data['total_cost_million'] * 10000  # 转换为元
        roi = market_data['roi_projection']
        
        return {
            'profit_margin': profit_margin,
            'breakeven_scale': total_investment / (target_price - unit_cost),
            'investment_attractiveness': 'High' if profit_margin > 20 else 'Medium',
            'recommendation': '建议进行产业化投资' if profit_margin > 15 else '需要优化成本',
            'key_success_factors': ['成本控制', '质量稳定', '市场拓展', '技术创新']
        }
    
    def _generate_industrial_visualization(self, analysis_result):
        """生成产业化分析可视化"""
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('产业化应用分析报告', fontsize=18, fontweight='bold')
        
        # 1. 成本结构饼图
        cost_data = analysis_result['cost_analysis']
        cost_labels = ['原材料', '能源', '人工', '设备', '其他']
        cost_values = [
            cost_data['raw_materials'],
            cost_data['energy'], 
            cost_data['labor'],
            cost_data['equipment'],
            cost_data['other']
        ]
        
        axes[0,0].pie(cost_values, labels=cost_labels, autopct='%1.1f%%')
        axes[0,0].set_title('生产成本结构')
        
        # 2. 市场规模预测
        market_data = analysis_result['market_analysis']
        years = market_data['years']
        sizes = market_data['market_sizes']
        
        axes[0,1].plot(years, sizes, 'b-o', linewidth=2, markersize=6)
        axes[0,1].set_title('市场规模预测')
        axes[0,1].set_xlabel('年份')
        axes[0,1].set_ylabel('市场规模 (亿元)')
        axes[0,1].grid(True, alpha=0.3)
        
        # 3. 认证时间线
        cert_data = analysis_result['certification_roadmap']
        stages = [p['stage'] for p in cert_data['certification_path']]
        durations = [int(p['duration'].split('-')[0]) for p in cert_data['certification_path']]
        
        bars = axes[1,0].barh(stages, durations, color=['lightblue', 'lightgreen', 'lightyellow', 'lightcoral'])
        axes[1,0].set_title('认证时间线')
        axes[1,0].set_xlabel('时间 (月)')
        
        # 添加数值标签
        for bar, duration in zip(bars, durations):
            axes[1,0].text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
                          f'{duration}月', va='center')
        
        # 4. 投资回报分析
        business_case = analysis_result['business_case']
        metrics = ['利润率', '投资吸引力', '推荐度']
        
        profit_margin = business_case['profit_margin']
        attractiveness_score = 85 if business_case['investment_attractiveness'] == 'High' else 65
        recommendation_score = 90 if '建议' in business_case['recommendation'] else 50
        
        values = [profit_margin, attractiveness_score, recommendation_score]
        colors = ['green' if v > 70 else 'orange' if v > 50 else 'red' for v in values]
        
        bars = axes[1,1].bar(metrics, values, color=colors)
        axes[1,1].set_title('投资评估指标')
        axes[1,1].set_ylabel('评分')
        axes[1,1].set_ylim(0, 100)
        
        # 添加数值标签
        for bar, value in zip(bars, values):
            axes[1,1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
                          f'{value:.1f}%' if bar.get_x() == 0 else f'{value:.0f}',
                          ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('industrial_analysis_results.png', dpi=300, bbox_inches='tight')
        print("📊 产业化分析图表已保存: industrial_analysis_results.png")
        plt.close()

def main():
    """主函数"""
    analyzer = IndustrialApplication()
    
    print("🏭 产业化应用分析模块")
    print("1. 运行完整分析")
    print("2. 单独成本分析")
    print("3. 单独市场分析")
    
    choice = input("请选择 (1-3): ").strip()
    
    if choice == '1':
        analyzer.run_complete_analysis()
    elif choice == '2':
        analyzer.cost_analysis("Li7La3Zr2O12", 5000)
    elif choice == '3':
        analyzer.market_analysis("Li7La3Zr2O12")
    else:
        print("运行完整分析...")
        analyzer.run_complete_analysis()

if __name__ == "__main__":
    main() 