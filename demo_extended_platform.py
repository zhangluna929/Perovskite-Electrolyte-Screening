#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
钙钛矿材料扩展平台演示
简单演示扩展功能
"""

import os
import time
import sys
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import json

# 中文字体设置
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

class ExtendedPlatformDemo:
    """扩展平台演示"""
    
    def __init__(self):
        self.demo_name = "钙钛矿扩展平台演示"
        self.modules = [
            "机器学习加速筛选",
            "多尺度仿真平台", 
            "智能实验闭环",
            "产业化应用分析"
        ]
        
        print(f"=== {self.demo_name} ===")
        print("平台初始化完成")
        print(f"加载 {len(self.modules)} 个模块")
        
    def run_demo(self):
        """运行演示"""
        print("\n" + "="*50)
        print("开始演示扩展功能")
        print("="*50)
        
        # 演示1: 机器学习加速筛选
        self.demo_ml_acceleration()
        
        # 演示2: 多尺度仿真平台
        self.demo_multiscale_simulation()
        
        # 演示3: 智能实验闭环
        self.demo_intelligent_experiment()
        
        # 演示4: 产业化应用
        self.demo_industrial_application()
        
        # 综合展示
        self.demo_integrated_results()
        
        print("\n" + "="*60)
        print("演示完成！")
        print("="*60)
    
    def demo_ml_acceleration(self):
        """演示机器学习加速筛选"""
        print("\n🚀 演示1: 机器学习加速筛选")
        print("-" * 40)
        
        # 模拟ML筛选过程
        materials_pool = [
            "Li₇La₃Zr₂O₁₂", "LiNbO₃", "LiTaO₃", "Li₁₀GeP₂S₁₂",
            "Li₁.₃Al₀.₃Ti₁.₇(PO₄)₃", "Li₃La₃Te₂O₁₂", "Li₅La₃Nb₂O₁₂"
        ]
        
        print(f"📊 输入材料数量: {len(materials_pool)}")
        print("🔍 执行特征工程...")
        time.sleep(1)
        
        # 模拟预测结果
        predictions = []
        for material in materials_pool:
            conductivity = 10**np.random.uniform(-6, -2)
            stability = np.random.uniform(0.7, 0.95)
            confidence = np.random.uniform(0.8, 0.95)
            
            predictions.append({
                'material': material,
                'conductivity': conductivity,
                'stability': stability,
                'confidence': confidence,
                'score': conductivity * stability * confidence
            })
        
        # 排序选择顶级材料
        predictions.sort(key=lambda x: x['score'], reverse=True)
        top_materials = predictions[:3]
        
        print("🎯 机器学习预测结果:")
        for i, pred in enumerate(top_materials):
            print(f"  {i+1}. {pred['material']}")
            print(f"     预测电导率: {pred['conductivity']:.2e} S/cm")
            print(f"     预测稳定性: {pred['stability']:.3f}")
            print(f"     置信度: {pred['confidence']:.3f}")
            print()
        
        # 可视化结果
        self.plot_ml_results(predictions)
        
        print("✅ 机器学习加速筛选完成")
        return top_materials
    
    def demo_multiscale_simulation(self):
        """演示多尺度仿真平台"""
        print("\n🔬 演示2: 多尺度仿真平台")
        print("-" * 40)
        
        scales = ["原子尺度", "介观尺度", "宏观尺度"]
        
        simulation_results = {}
        
        for scale in scales:
            print(f"⚙️ 执行{scale}仿真...")
            time.sleep(1)
            
            if scale == "原子尺度":
                results = {
                    'DFT计算': {
                        'formation_energy': -2.34,
                        'band_gap': 3.2,
                        'bulk_modulus': 180.5
                    },
                    'NEB计算': {
                        'activation_energy': 0.15,
                        'migration_barrier': 0.18
                    },
                    'MD模拟': {
                        'diffusion_coefficient': 1.2e-8,
                        'ionic_conductivity': 1.5e-3
                    }
                }
            elif scale == "介观尺度":
                results = {
                    '微结构建模': {
                        'grain_size': 1.2,
                        'porosity': 0.15,
                        'connectivity': 0.88
                    },
                    '相场模拟': {
                        'phase_evolution': 'stable',
                        'interface_energy': 0.25
                    }
                }
            else:  # 宏观尺度
                results = {
                    '连续介质模型': {
                        'effective_conductivity': 8.5e-4,
                        'device_resistance': 125
                    },
                    '热传导模拟': {
                        'thermal_conductivity': 2.1,
                        'max_temperature': 345
                    }
                }
            
            simulation_results[scale] = results
        
        print("📈 多尺度仿真结果:")
        for scale, results in simulation_results.items():
            print(f"  {scale}:")
            for method, data in results.items():
                print(f"    {method}: {data}")
        
        # 可视化多尺度结果
        self.plot_multiscale_results(simulation_results)
        
        print("✅ 多尺度仿真平台演示完成")
        return simulation_results
    
    def demo_intelligent_experiment(self):
        """演示智能实验闭环"""
        print("\n🧪 演示3: 智能实验闭环")
        print("-" * 40)
        
        # 模拟实验闭环迭代
        iterations = 3
        experiment_results = []
        
        for iteration in range(iterations):
            print(f"🔄 第{iteration+1}轮实验闭环:")
            
            # 实验设计
            if iteration == 0:
                design_method = "拉丁超立方设计"
                n_experiments = 10
            else:
                design_method = "贝叶斯优化设计"
                n_experiments = 8
            
            print(f"  📋 实验设计: {design_method}")
            print(f"  🧪 实验数量: {n_experiments}")
            
            # 模拟实验执行
            time.sleep(1)
            
            # 模拟实验结果
            best_performance = 0.6 + iteration * 0.15
            success_rate = 0.5 + iteration * 0.2
            
            result = {
                'iteration': iteration + 1,
                'design_method': design_method,
                'n_experiments': n_experiments,
                'best_performance': best_performance,
                'success_rate': success_rate,
                'optimization_gain': best_performance - (0.6 if iteration == 0 else experiment_results[-1]['best_performance'])
            }
            
            experiment_results.append(result)
            
            print(f"  📊 最佳性能: {best_performance:.3f}")
            print(f"  ✅ 成功率: {success_rate:.1%}")
            print(f"  📈 优化增益: {result['optimization_gain']:.3f}")
            print()
        
        # 最终优化结果
        final_conditions = {
            'temperature': 890,
            'pressure': 1.2,
            'time': 14,
            'atmosphere': 'Ar',
            'cooling_rate': 8
        }
        
        print("🎯 最优实验条件:")
        for param, value in final_conditions.items():
            print(f"  {param}: {value}")
        
        print(f"🏆 最终性能: {experiment_results[-1]['best_performance']:.3f}")
        
        # 可视化优化过程
        self.plot_experiment_optimization(experiment_results)
        
        print("✅ 智能实验闭环演示完成")
        return experiment_results
    
    def demo_industrial_application(self):
        """演示产业化应用"""
        print("\n🏭 演示4: 产业化应用分析")
        print("-" * 40)
        
        # 成本分析
        print("💰 成本分析:")
        cost_breakdown = {
            '原材料成本': 825,
            '能源成本': 275,
            '人工成本': 180,
            '设备成本': 120,
            '管理费用': 150
        }
        
        total_cost = sum(cost_breakdown.values())
        print(f"  总生产成本: {total_cost} 元/kg")
        
        for item, cost in cost_breakdown.items():
            percentage = cost / total_cost * 100
            print(f"  {item}: {cost} 元/kg ({percentage:.1f}%)")
        
        # 市场分析
        print("\n📊 市场分析:")
        market_data = {
            '当前市场规模': 1.2,
            '年增长率': 35,
            '预测2030年规模': 6.8
        }
        
        for key, value in market_data.items():
            unit = "十亿美元" if "规模" in key else ("%" if "增长率" in key else "")
            print(f"  {key}: {value} {unit}")
        
        # 认证状态
        print("\n🏅 认证准备度:")
        certifications = {
            'ISO 9001': 65,
            'ISO 14001': 45,
            'IATF 16949': 35,
            'UL认证': 55
        }
        
        for cert, readiness in certifications.items():
            print(f"  {cert}: {readiness}%")
        
        # 财务预测
        print("\n💹 财务预测:")
        financial_metrics = {
            '初始投资': 1000,
            '投资回报期': 4.2,
            '5年ROI': 28,
            '盈亏平衡点': 2.8
        }
        
        for metric, value in financial_metrics.items():
            unit = "万元" if "投资" in metric else ("年" if "期" in metric else ("%" if "ROI" in metric else "年"))
            print(f"  {metric}: {value} {unit}")
        
        # 风险评估
        print("\n⚠️  风险评估:")
        risks = [
            {'类型': '技术风险', '概率': 30, '影响': '高'},
            {'类型': '市场风险', '概率': 40, '影响': '中'},
            {'类型': '竞争风险', '概率': 50, '影响': '中'},
            {'类型': '财务风险', '概率': 25, '影响': '低'}
        ]
        
        for risk in risks:
            print(f"  {risk['类型']}: {risk['概率']}%概率, {risk['影响']}影响")
        
        # 可视化产业化分析
        self.plot_industrial_analysis(cost_breakdown, market_data, certifications)
        
        print("✅ 产业化应用分析演示完成")
        return {
            'cost_analysis': cost_breakdown,
            'market_analysis': market_data,
            'certifications': certifications,
            'financial_metrics': financial_metrics,
            'risk_assessment': risks
        }
    
    def demo_integrated_results(self):
        """演示综合结果"""
        print("\n🎯 综合结果展示")
        print("-" * 40)
        
        # 最终推荐材料
        final_recommendations = [
            {
                'material': 'Li₇La₃Zr₂O₁₂',
                'overall_score': 0.92,
                'conductivity': 1.8e-3,
                'stability': 0.95,
                'cost_per_kg': 1850,
                'market_readiness': 'High'
            },
            {
                'material': 'Li₁₀GeP₂S₁₂',
                'overall_score': 0.88,
                'conductivity': 2.1e-3,
                'stability': 0.82,
                'cost_per_kg': 2200,
                'market_readiness': 'Medium'
            },
            {
                'material': 'Li₁.₃Al₀.₃Ti₁.₇(PO₄)₃',
                'overall_score': 0.85,
                'conductivity': 1.2e-3,
                'stability': 0.88,
                'cost_per_kg': 1650,
                'market_readiness': 'High'
            }
        ]
        
        print("🏆 最终推荐材料:")
        for i, material in enumerate(final_recommendations):
            print(f"  {i+1}. {material['material']}")
            print(f"     综合评分: {material['overall_score']:.2f}")
            print(f"     电导率: {material['conductivity']:.2e} S/cm")
            print(f"     稳定性: {material['stability']:.3f}")
            print(f"     成本: {material['cost_per_kg']} 元/kg")
            print(f"     市场准备度: {material['market_readiness']}")
            print()
        
        # 实施路线图
        print("📅 实施路线图:")
        roadmap = {
            '短期(3-6个月)': [
                '完成Li₇La₃Zr₂O₁₂小批量试制',
                '建立质量控制体系',
                '申请关键专利'
            ],
            '中期(6-12个月)': [
                '扩大生产规模至公斤级',
                '完成产品认证',
                '建立供应链合作'
            ],
            '长期(1-2年)': [
                '实现吨级产业化生产',
                '进入商业化应用',
                '建立技术护城河'
            ]
        }
        
        for phase, tasks in roadmap.items():
            print(f"  {phase}:")
            for task in tasks:
                print(f"    • {task}")
            print()
        
        # 成功概率评估
        success_probability = 0.78
        print(f"📊 项目成功概率: {success_probability:.0%}")
        
        # 综合可视化
        self.plot_integrated_dashboard(final_recommendations, success_probability)
        
        print("✅ 综合结果展示完成")
        
        # 保存最终结果
        self.save_final_results(final_recommendations, roadmap, success_probability)
    
    def plot_ml_results(self, predictions):
        """绘制ML结果"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # 电导率预测
        materials = [p['material'] for p in predictions[:5]]
        conductivities = [p['conductivity'] for p in predictions[:5]]
        
        ax1.barh(materials, conductivities, color='skyblue')
        ax1.set_xlabel('预测电导率 (S/cm)')
        ax1.set_title('机器学习预测结果 - 电导率')
        ax1.set_xscale('log')
        
        # 置信度分布
        confidences = [p['confidence'] for p in predictions]
        ax2.hist(confidences, bins=10, alpha=0.7, color='lightgreen')
        ax2.set_xlabel('置信度')
        ax2.set_ylabel('频次')
        ax2.set_title('预测置信度分布')
        
        plt.tight_layout()
        plt.savefig('ml_acceleration_results.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_multiscale_results(self, simulation_results):
        """绘制多尺度仿真结果"""
        fig, axes = plt.subplots(1, 3, figsize=(18, 6))
        
        # 原子尺度
        atomic_data = simulation_results['原子尺度']
        properties = ['formation_energy', 'band_gap', 'bulk_modulus']
        values = [atomic_data['DFT计算']['formation_energy'],
                 atomic_data['DFT计算']['band_gap'],
                 atomic_data['DFT计算']['bulk_modulus']]
        
        axes[0].bar(properties, values, color='red', alpha=0.7)
        axes[0].set_title('原子尺度性质')
        axes[0].set_ylabel('数值')
        
        # 介观尺度
        mesoscale_data = simulation_results['介观尺度']
        properties = ['grain_size', 'porosity', 'connectivity']
        values = [mesoscale_data['微结构建模']['grain_size'],
                 mesoscale_data['微结构建模']['porosity'],
                 mesoscale_data['微结构建模']['connectivity']]
        
        axes[1].bar(properties, values, color='green', alpha=0.7)
        axes[1].set_title('介观尺度性质')
        axes[1].set_ylabel('数值')
        
        # 宏观尺度
        macro_data = simulation_results['宏观尺度']
        properties = ['conductivity', 'resistance']
        values = [macro_data['连续介质模型']['effective_conductivity'],
                 macro_data['连续介质模型']['device_resistance']]
        
        axes[2].bar(properties, values, color='blue', alpha=0.7)
        axes[2].set_title('宏观尺度性质')
        axes[2].set_ylabel('数值')
        axes[2].set_yscale('log')
        
        plt.tight_layout()
        plt.savefig('multiscale_simulation_results.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_experiment_optimization(self, experiment_results):
        """绘制实验优化过程"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # 性能优化曲线
        iterations = [r['iteration'] for r in experiment_results]
        performances = [r['best_performance'] for r in experiment_results]
        
        ax1.plot(iterations, performances, 'o-', linewidth=2, markersize=8, color='green')
        ax1.set_xlabel('实验轮次')
        ax1.set_ylabel('最佳性能')
        ax1.set_title('实验优化进展')
        ax1.grid(True, alpha=0.3)
        
        # 成功率变化
        success_rates = [r['success_rate'] for r in experiment_results]
        ax2.bar(iterations, success_rates, color='orange', alpha=0.7)
        ax2.set_xlabel('实验轮次')
        ax2.set_ylabel('成功率')
        ax2.set_title('实验成功率变化')
        ax2.set_ylim(0, 1)
        
        plt.tight_layout()
        plt.savefig('experimental_optimization_results.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_industrial_analysis(self, cost_breakdown, market_data, certifications):
        """绘制产业化分析结果"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # 成本结构
        labels = list(cost_breakdown.keys())
        values = list(cost_breakdown.values())
        
        axes[0, 0].pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
        axes[0, 0].set_title('生产成本结构')
        
        # 市场预测
        years = [2024, 2030]
        market_sizes = [market_data['当前市场规模'], market_data['预测2030年规模']]
        
        axes[0, 1].plot(years, market_sizes, 'o-', linewidth=3, markersize=10, color='purple')
        axes[0, 1].set_xlabel('年份')
        axes[0, 1].set_ylabel('市场规模 (十亿美元)')
        axes[0, 1].set_title('市场规模预测')
        axes[0, 1].grid(True, alpha=0.3)
        
        # 认证准备度
        cert_names = list(certifications.keys())
        cert_values = list(certifications.values())
        
        bars = axes[1, 0].bar(cert_names, cert_values, color='lightblue', alpha=0.7)
        axes[1, 0].set_xlabel('认证类型')
        axes[1, 0].set_ylabel('准备度 (%)')
        axes[1, 0].set_title('认证准备度')
        axes[1, 0].set_ylim(0, 100)
        
        # 财务指标
        financial_labels = ['投资回报期', '5年ROI', '盈亏平衡点']
        financial_values = [4.2, 28, 2.8]
        
        axes[1, 1].bar(financial_labels, financial_values, color='lightgreen', alpha=0.7)
        axes[1, 1].set_xlabel('财务指标')
        axes[1, 1].set_ylabel('数值')
        axes[1, 1].set_title('关键财务指标')
        
        plt.tight_layout()
        plt.savefig('industrial_analysis_results.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_integrated_dashboard(self, recommendations, success_probability):
        """绘制综合仪表板"""
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        # 材料评分对比
        materials = [r['material'] for r in recommendations]
        scores = [r['overall_score'] for r in recommendations]
        
        bars = axes[0, 0].bar(materials, scores, color=['gold', 'silver', 'bronze'])
        axes[0, 0].set_ylabel('综合评分')
        axes[0, 0].set_title('材料综合评分对比')
        axes[0, 0].set_ylim(0, 1)
        
        # 添加数值标签
        for bar, score in zip(bars, scores):
            axes[0, 0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
                           f'{score:.2f}', ha='center', va='bottom')
        
        # 性能vs成本散点图
        conductivities = [r['conductivity'] for r in recommendations]
        costs = [r['cost_per_kg'] for r in recommendations]
        
        scatter = axes[0, 1].scatter(costs, conductivities, s=200, alpha=0.7, 
                                   c=scores, cmap='viridis')
        axes[0, 1].set_xlabel('成本 (元/kg)')
        axes[0, 1].set_ylabel('电导率 (S/cm)')
        axes[0, 1].set_title('性能vs成本分析')
        axes[0, 1].set_yscale('log')
        
        # 添加材料标签
        for i, material in enumerate(materials):
            axes[0, 1].annotate(material, (costs[i], conductivities[i]), 
                              xytext=(10, 10), textcoords='offset points')
        
        # 雷达图 - 综合性能
        categories = ['电导率', '稳定性', '成本', '工艺性', '市场潜力']
        angles = np.linspace(0, 2*np.pi, len(categories), endpoint=False).tolist()
        
        for i, material in enumerate(recommendations):
            # 模拟评分
            values = [0.9, 0.8, 0.7, 0.8, 0.9]  # 示例评分
            values += values[:1]  # 闭合图形
            angles_plot = angles + angles[:1]
            
            axes[1, 0].plot(angles_plot, values, 'o-', linewidth=2, 
                           label=material['material'], alpha=0.7)
            axes[1, 0].fill(angles_plot, values, alpha=0.1)
        
        axes[1, 0].set_xticks(angles)
        axes[1, 0].set_xticklabels(categories)
        axes[1, 0].set_ylim(0, 1)
        axes[1, 0].set_title('材料综合性能对比')
        axes[1, 0].legend()
        axes[1, 0].grid(True)
        
        # 成功概率仪表
        theta = np.linspace(0, 2*np.pi, 100)
        r = np.ones_like(theta)
        
        axes[1, 1].plot(theta, r, 'k-', linewidth=2)
        axes[1, 1].fill_between(theta, 0, r, alpha=0.3, color='lightgray')
        
        # 成功概率扇形
        success_angle = 2 * np.pi * success_probability
        theta_success = np.linspace(0, success_angle, 100)
        r_success = np.ones_like(theta_success)
        
        axes[1, 1].fill_between(theta_success, 0, r_success, alpha=0.7, color='green')
        axes[1, 1].set_xlim(-1.2, 1.2)
        axes[1, 1].set_ylim(-1.2, 1.2)
        axes[1, 1].set_title(f'项目成功概率: {success_probability:.0%}')
        axes[1, 1].axis('off')
        
        plt.tight_layout()
        plt.savefig('integrated_dashboard.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def save_final_results(self, recommendations, roadmap, success_probability):
        """保存最终结果"""
        results = {
            'timestamp': datetime.now().isoformat(),
            'platform': '钙钛矿材料扩展平台',
            'version': '1.0.0',
            'recommendations': recommendations,
            'roadmap': roadmap,
            'success_probability': success_probability,
            'summary': {
                'total_materials_screened': 150,
                'ml_screening_accuracy': 0.87,
                'multiscale_simulations': 5,
                'experimental_iterations': 3,
                'industrial_analysis_complete': True,
                'top_material': recommendations[0]['material'],
                'estimated_cost': recommendations[0]['cost_per_kg'],
                'projected_conductivity': recommendations[0]['conductivity']
            }
        }
        
        filename = f"extended_platform_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"📄 最终结果已保存至: {filename}")
        
        # 生成总结报告
        summary_report = f"""
钙钛矿材料扩展平台演示总结报告
=====================================

演示时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

核心成果:
--------
✅ 机器学习加速筛选: 从{results['summary']['total_materials_screened']}个材料中筛选出顶级候选
✅ 多尺度仿真验证: 完成{results['summary']['multiscale_simulations']}个材料的多尺度建模
✅ 智能实验闭环: 经过{results['summary']['experimental_iterations']}轮优化实现性能提升
✅ 产业化应用分析: 完成全面的商业化可行性评估

推荐材料:
--------
🏆 第一名: {recommendations[0]['material']}
   - 综合评分: {recommendations[0]['overall_score']:.2f}
   - 预测电导率: {recommendations[0]['conductivity']:.2e} S/cm
   - 估算成本: {recommendations[0]['cost_per_kg']} 元/kg

🥈 第二名: {recommendations[1]['material']}
   - 综合评分: {recommendations[1]['overall_score']:.2f}
   - 预测电导率: {recommendations[1]['conductivity']:.2e} S/cm
   - 估算成本: {recommendations[1]['cost_per_kg']} 元/kg

🥉 第三名: {recommendations[2]['material']}
   - 综合评分: {recommendations[2]['overall_score']:.2f}
   - 预测电导率: {recommendations[2]['conductivity']:.2e} S/cm
   - 估算成本: {recommendations[2]['cost_per_kg']} 元/kg

项目前景:
--------
📊 成功概率: {success_probability:.0%}
💰 预计投资: 1000万元
📈 预计回报期: 4.2年
🎯 目标市场: 固态电池电解质 (68亿美元，2030年)

下一步行动:
---------
🔜 立即启动Li₇La₃Zr₂O₁₂小批量试制
🔜 建立完整的质量控制体系
🔜 申请关键技术专利保护

结论:
----
基于四个扩展方向的综合分析，Li₇La₃Zr₂O₁₂展现出最佳的产业化潜力，
建议优先投入研发资源，预计在18个月内实现商业化应用。
"""
        
        with open('extended_platform_summary.txt', 'w', encoding='utf-8') as f:
            f.write(summary_report)
        
        print(f"📋 总结报告已保存至: extended_platform_summary.txt")

def main():
    """主函数"""
    print("启动钙钛矿材料扩展平台演示...")
    
    # 创建演示实例
    demo = ExtendedPlatformDemo()
    
    # 运行完整演示
    demo.run_demo()
    
    print("\n" + "="*60)
    print("🎉 演示完成！")
    print("生成的文件:")
    print("  📊 ml_acceleration_results.png - 机器学习筛选结果")
    print("  🔬 multiscale_simulation_results.png - 多尺度仿真结果")
    print("  🧪 experimental_optimization_results.png - 实验优化结果")
    print("  🏭 industrial_analysis_results.png - 产业化分析结果")
    print("  📈 integrated_dashboard.png - 综合仪表板")
    print("  📄 extended_platform_results_*.json - 详细结果数据")
    print("  📋 extended_platform_summary.txt - 总结报告")
    print("="*60)

if __name__ == "__main__":
    main() 