"""Core module for perovskite electrolyte screening platform"""

import numpy as np
from pathlib import Path
from typing import Dict, List, Optional
from ..ml.advanced_performance_predictor import AdvancedPerformancePredictor
from ..ml.ml_enhanced_screening import MLEnhancedScreening
from .experimental_conditions import ExperimentalConditionAnalyzer

class PerovskiteScreening:
    """钙钛矿筛选主类"""
    
    def __init__(self):
        self.perf_predictor = AdvancedPerformancePredictor()
        self.ml_screen = MLEnhancedScreening()
        self.cond_analyzer = ExperimentalConditionAnalyzer()
        self.materials = []  # 存储材料数据
        
    def load_material(self, cif_file):
        """从CIF文件加载材料"""
        mat_data = self.ml_screen.load_structure(cif_file)
        
        # 设置默认实验条件
        mat_data.update({
            'temperature': 298,  # 室温
            'pressure': 1.0,
            'atmosphere_o2_content': 0.21,
            'humidity': 0.5
        })
        
        return mat_data
    
    def predict_performance(self, mat_data, conditions=None):
        """性能预测"""
        default_conds = {
            'temperature': 298,
            'pressure': 1.0,
            'atmosphere_o2_content': 0.21,
            'humidity': 0.5
        }
        
        if conditions:
            default_conds.update(conditions)
        
        base_pred = self.ml_screen.predict_properties(mat_data)
        adv_pred = self.perf_predictor.predict_performance(mat_data, default_conds)
        
        results = {
            'conductivity': base_pred.get('predicted_conductivity', 0),
            'activation_energy': base_pred.get('predicted_activation_energy', 0),
            'stability': base_pred.get('predicted_stability', 0),
            'thermal_stability': adv_pred.get('thermal_stability', 0),
            'cycle_life': adv_pred.get('cycle_life', 0),
            'mechanical_strength': adv_pred.get('mechanical_strength', 0),
            'conditions': default_conds
        }
        
        results['score'] = self._calc_score(results)
        return results
    
    def temperature_scan(self, mat_data, temp_range=(250, 1000), points=50):
        """温度扫描分析"""
        temps = np.linspace(temp_range[0], temp_range[1], points)
        conductivities = []
        stabilities = []
        
        for T in temps:
            conds = {
                'temperature': T,
                'pressure': 1.0,
                'atmosphere_o2_content': 0.21,
                'humidity': 0.5
            }
            
            pred = self.perf_predictor.predict_performance(mat_data, conds)
            conductivities.append(pred.get('conductivity', 0))
            stabilities.append(pred.get('thermal_stability', 0))
        
        return {
            'temperatures': temps.tolist(),
            'conductivities': conductivities,
            'thermal_stabilities': stabilities
        }
    
    def predict_lifetime(self, mat_data, conditions, time_points):
        """预测材料随时间的性能变化"""
        return self.perf_predictor.predict_time_evolution(mat_data, conditions, time_points)
    
    def analyze_conditions(self, mat_data, conditions_list=None):
        """分析实验条件影响"""
        if not conditions_list:
            conditions_list = [
                'temperature',
                'sintering_temperature', 
                'atmosphere_o2_content',
                'particle_size'
            ]
        
        results = {}
        
        for cond in conditions_list:
            impact = self.cond_analyzer.analyze_condition_impact(mat_data, cond)
            results[cond] = impact
        
        # 条件交互作用
        if len(conditions_list) >= 2:
            interactions = {}
            for i in range(len(conditions_list)):
                for j in range(i+1, len(conditions_list)):
                    c1, c2 = conditions_list[i], conditions_list[j]
                    interaction = self.cond_analyzer.analyze_interaction_effects(mat_data, c1, c2)
                    interactions[f"{c1}-{c2}"] = interaction
            
            results['interactions'] = interactions
        
        return results
    
    def optimize_conditions(self, mat_data, target):
        """优化工艺条件"""
        opt_result = self.cond_analyzer.optimize_conditions(
            mat_data,
            target['property'],
            target.get('constraints')
        )
        
        recipe = self.cond_analyzer.generate_processing_recipe(mat_data, target)
        
        return {
            'optimized_conditions': opt_result,
            'processing_recipe': recipe
        }
    
    def generate_report(self, mat_data, analysis_results):
        """生成分析报告"""
        report_lines = [
            "# 实验条件分析报告",
            f"\n## 材料信息",
            f"化学式: {mat_data.get('formula', '未知')}",
            f"\n## 条件影响分析"
        ]
        
        for condition, impact in analysis_results.items():
            if condition != 'interactions':
                report_lines.extend([
                    f"\n### {condition}",
                    f"影响趋势: {self._get_trend(impact)}"
                ])
        
        if 'interactions' in analysis_results:
            report_lines.append("\n## 条件交互作用")
            for pair, interaction in analysis_results['interactions'].items():
                c1, c2 = pair.split('-')
                report_lines.extend([
                    f"\n### {c1} 与 {c2}",
                    f"交互强度: {self._analyze_interaction(interaction)}"
                ])
        
        return "\n".join(report_lines)
    
    def _calc_score(self, results):
        """计算综合评分"""
        weights = {
            'conductivity': 0.3,
            'activation_energy': 0.2,
            'stability': 0.15,
            'thermal_stability': 0.15,
            'cycle_life': 0.1,
            'mechanical_strength': 0.1
        }
        
        norm_vals = {
            'conductivity': min(results['conductivity'] / 1e-2, 1.0),
            'activation_energy': max(0, 1 - results['activation_energy'] / 0.3),
            'stability': results['stability'],
            'thermal_stability': results['thermal_stability'],
            'cycle_life': min(results['cycle_life'] / 1000, 1.0),
            'mechanical_strength': min(results['mechanical_strength'] / 200, 1.0)
        }
        
        score = sum(norm_vals[k] * weights[k] for k in weights)
        return score
    
    def make_report(self, mat_data, predictions):
        """生成材料性能报告"""
        report = [
            "# 材料性能预测报告",
            f"\n## 基本信息",
            f"化学式: {mat_data.get('formula', '未知')}",
            f"晶系: {mat_data.get('crystal_system', '未知')}",
            f"空间群: {mat_data.get('space_group', '未知')}",
            
            f"\n## 性能预测",
            f"离子电导率: {predictions['conductivity']:.2e} S/cm",
            f"激活能: {predictions['activation_energy']:.3f} eV",
            f"稳定性: {predictions['stability']:.2f}",
            f"热稳定性: {predictions['thermal_stability']:.2f}",
            f"循环寿命: {predictions['cycle_life']:.0f} 次",
            f"机械强度: {predictions['mechanical_strength']:.1f} MPa",
            
            f"\n## 测试条件",
            f"温度: {predictions['conditions']['temperature']} K",
            f"压力: {predictions['conditions']['pressure']} atm",
            f"氧气浓度: {predictions['conditions']['atmosphere_o2_content']*100:.1f}%",
            f"湿度: {predictions['conditions']['humidity']*100:.1f}%",
            
            f"\n## 综合评价",
            f"总评分: {predictions['score']:.2f}/1.00"
        ]
        
        score = predictions['score']
        if score >= 0.8:
            report.append("\n建议: 优秀材料，可以做实验验证")
        elif score >= 0.6:
            report.append("\n建议: 还不错，可以考虑优化后使用")
        else:
            report.append("\n建议: 性能一般，建议找其他材料")
        
        return "\n".join(report)

    def _get_trend(self, impact):
        """简单的趋势分析"""
        try:
            values = np.array(impact['performance_impact']['conductivity'])
            slope = np.polyfit(range(len(values)), values, 1)[0]
            
            if slope > 0:
                return "正相关"
            elif slope < 0:
                return "负相关"  
            else:
                return "无明显影响"
        except:
            return "数据不足"
    
    def _analyze_interaction(self, interaction):
        """分析交互作用强度"""
        try:
            Z = np.array(interaction['Z'])
            
            if np.max(Z) - np.min(Z) > 0.1:
                return "强交互作用"
            else:
                return "弱交互作用"
        except:
            return "无法分析"

def main():
    """测试用的主函数"""
    print("=== 钙钛矿筛选平台测试 ===")
    
    platform = PerovskiteScreening()
    
    # 测试流程
    # cif_path = "test_material.cif"
    # mat_data = platform.load_material(cif_path)
    # predictions = platform.predict_performance(mat_data)
    # report = platform.make_report(mat_data, predictions)
    # print(report)

if __name__ == '__main__':
    main() 