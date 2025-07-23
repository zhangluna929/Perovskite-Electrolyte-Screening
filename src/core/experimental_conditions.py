"""Experimental conditions analysis module"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from scipy.optimize import minimize
import matplotlib.pyplot as plt
from dataclasses import dataclass
import json
from pathlib import Path

@dataclass
class ExperimentalCondition:
    """实验条件数据类"""
    name: str
    value: float
    unit: str
    min_value: float
    max_value: float
    description: str

class ExperimentalConditionAnalyzer:
    """实验条件影响分析器"""
    
    def __init__(self):
        # 定义标准实验条件
        self.standard_conditions = {
            'temperature': ExperimentalCondition(
                name='temperature',
                value=298.0,
                unit='K',
                min_value=250.0,
                max_value=1200.0,
                description='实验温度'
            ),
            'pressure': ExperimentalCondition(
                name='pressure',
                value=1.0,
                unit='atm',
                min_value=0.1,
                max_value=10.0,
                description='环境压力'
            ),
            'atmosphere_o2_content': ExperimentalCondition(
                name='atmosphere_o2_content',
                value=0.21,
                unit='比例',
                min_value=0.0,
                max_value=1.0,
                description='氧气含量'
            ),
            'humidity': ExperimentalCondition(
                name='humidity',
                value=0.5,
                unit='RH',
                min_value=0.0,
                max_value=1.0,
                description='相对湿度'
            ),
            'sintering_temperature': ExperimentalCondition(
                name='sintering_temperature',
                value=1000.0,
                unit='K',
                min_value=800.0,
                max_value=1500.0,
                description='烧结温度'
            ),
            'sintering_time': ExperimentalCondition(
                name='sintering_time',
                value=10.0,
                unit='h',
                min_value=2.0,
                max_value=24.0,
                description='烧结时间'
            ),
            'cooling_rate': ExperimentalCondition(
                name='cooling_rate',
                value=5.0,
                unit='K/min',
                min_value=1.0,
                max_value=20.0,
                description='冷却速率'
            ),
            'particle_size': ExperimentalCondition(
                name='particle_size',
                value=1.0,
                unit='μm',
                min_value=0.1,
                max_value=10.0,
                description='颗粒尺寸'
            ),
            'compaction_pressure': ExperimentalCondition(
                name='compaction_pressure',
                value=200.0,
                unit='MPa',
                min_value=50.0,
                max_value=500.0,
                description='压制压力'
            ),
            'current_density': ExperimentalCondition(
                name='current_density',
                value=1.0,
                unit='mA/cm²',
                min_value=0.1,
                max_value=10.0,
                description='测试电流密度'
            )
        }
        
    def analyze_condition_impact(self, 
                               material_data: Dict,
                               condition_name: str,
                               value_range: Optional[Tuple[float, float]] = None,
                               n_points: int = 50) -> Dict:
        """分析单个实验条件的影响
        
        Args:
            material_data: 材料数据
            condition_name: 条件名称
            value_range: 值范围（可选）
            n_points: 采样点数
            
        Returns:
            影响分析结果
        """
        condition = self.standard_conditions[condition_name]
        
        # 使用指定范围或默认范围
        min_val = value_range[0] if value_range else condition.min_value
        max_val = value_range[1] if value_range else condition.max_value
        
        # 生成采样点
        values = np.linspace(min_val, max_val, n_points)
        
        # 计算性能影响
        performance_impact = self._calculate_performance_impact(
            material_data, condition_name, values
        )
        
        return {
            'condition': condition,
            'values': values.tolist(),
            'performance_impact': performance_impact
        }
    
    def optimize_conditions(self, 
                          material_data: Dict,
                          target_property: str,
                          constraints: Optional[Dict] = None) -> Dict:
        """优化实验条件
        
        Args:
            material_data: 材料数据
            target_property: 目标性能
            constraints: 约束条件
            
        Returns:
            优化结果
        """
        # 初始条件
        x0 = [cond.value for cond in self.standard_conditions.values()]
        
        # 约束条件
        bounds = [(cond.min_value, cond.max_value) 
                 for cond in self.standard_conditions.values()]
        
        # 优化
        result = minimize(
            lambda x: -self._evaluate_performance(material_data, x, target_property),
            x0,
            bounds=bounds,
            method='L-BFGS-B'
        )
        
        # 整理结果
        optimized_conditions = {}
        for i, (name, condition) in enumerate(self.standard_conditions.items()):
            optimized_conditions[name] = {
                'value': result.x[i],
                'unit': condition.unit
            }
        
        return {
            'optimized_conditions': optimized_conditions,
            'predicted_performance': -result.fun,
            'optimization_success': result.success
        }
    
    def analyze_interaction_effects(self,
                                  material_data: Dict,
                                  condition1: str,
                                  condition2: str,
                                  n_points: int = 20) -> Dict:
        """分析两个条件的交互作用
        
        Args:
            material_data: 材料数据
            condition1: 第一个条件
            condition2: 第二个条件
            n_points: 每个维度的采样点数
            
        Returns:
            交互作用分析结果
        """
        cond1 = self.standard_conditions[condition1]
        cond2 = self.standard_conditions[condition2]
        
        # 生成网格点
        x = np.linspace(cond1.min_value, cond1.max_value, n_points)
        y = np.linspace(cond2.min_value, cond2.max_value, n_points)
        X, Y = np.meshgrid(x, y)
        
        # 计算性能影响
        Z = np.zeros_like(X)
        for i in range(n_points):
            for j in range(n_points):
                conditions = {
                    condition1: X[i,j],
                    condition2: Y[i,j]
                }
                Z[i,j] = self._evaluate_interaction(
                    material_data, conditions
                )
        
        return {
            'condition1': cond1,
            'condition2': cond2,
            'X': X.tolist(),
            'Y': Y.tolist(),
            'Z': Z.tolist()
        }
    
    def generate_processing_recipe(self,
                                 material_data: Dict,
                                 performance_target: Dict) -> Dict:
        """生成实验工艺配方
        
        Args:
            material_data: 材料数据
            performance_target: 性能目标
            
        Returns:
            工艺配方
        """
        # 优化条件
        optimized = self.optimize_conditions(
            material_data,
            performance_target['property'],
            performance_target.get('constraints')
        )
        
        # 生成工艺流程
        recipe = {
            'material': material_data.get('formula', 'Unknown'),
            'target_performance': performance_target,
            'processing_steps': [
                {
                    'step': 1,
                    'name': '原料准备',
                    'conditions': {
                        'particle_size': optimized['optimized_conditions']['particle_size']
                    }
                },
                {
                    'step': 2,
                    'name': '压制成型',
                    'conditions': {
                        'compaction_pressure': optimized['optimized_conditions']['compaction_pressure']
                    }
                },
                {
                    'step': 3,
                    'name': '烧结',
                    'conditions': {
                        'temperature': optimized['optimized_conditions']['sintering_temperature'],
                        'time': optimized['optimized_conditions']['sintering_time'],
                        'atmosphere_o2_content': optimized['optimized_conditions']['atmosphere_o2_content'],
                        'cooling_rate': optimized['optimized_conditions']['cooling_rate']
                    }
                },
                {
                    'step': 4,
                    'name': '性能测试',
                    'conditions': {
                        'temperature': optimized['optimized_conditions']['temperature'],
                        'current_density': optimized['optimized_conditions']['current_density']
                    }
                }
            ],
            'predicted_performance': optimized['predicted_performance'],
            'notes': self._generate_processing_notes(optimized['optimized_conditions'])
        }
        
        return recipe
    
    def _calculate_performance_impact(self,
                                    material_data: Dict,
                                    condition_name: str,
                                    values: np.ndarray) -> Dict:
        """计算性能影响
        
        Args:
            material_data: 材料数据
            condition_name: 条件名称
            values: 条件值数组
            
        Returns:
            性能影响
        """
        # 计算不同性能指标
        conductivity = []
        stability = []
        mechanical_strength = []
        
        for value in values:
            # 设置条件
            conditions = {name: cond.value 
                        for name, cond in self.standard_conditions.items()}
            conditions[condition_name] = value
            
            # 计算性能
            perf = self._evaluate_performance(material_data, list(conditions.values()))
            conductivity.append(perf['conductivity'])
            stability.append(perf['stability'])
            mechanical_strength.append(perf['mechanical_strength'])
        
        return {
            'conductivity': conductivity,
            'stability': stability,
            'mechanical_strength': mechanical_strength
        }
    
    def _evaluate_performance(self,
                            material_data: Dict,
                            conditions: List[float],
                            target_property: str = 'conductivity') -> float:
        """评估性能
        
        Args:
            material_data: 材料数据
            conditions: 条件值列表
            target_property: 目标性能
            
        Returns:
            性能值
        """
        # 简化的性能模型
        if target_property == 'conductivity':
            # 电导率模型
            base_conductivity = 1e-3  # 基础电导率
            
            # 温度影响 (Arrhenius关系)
            temperature_effect = np.exp(-0.3 / (8.314e-3 * conditions[0]))
            
            # 湿度影响
            humidity_effect = 1 - 0.2 * conditions[3]  # 湿度降低电导率
            
            # 微结构影响
            particle_size_effect = 1 / np.sqrt(conditions[7])  # 颗粒尺寸越小越好
            
            return base_conductivity * temperature_effect * humidity_effect * particle_size_effect
            
        elif target_property == 'stability':
            # 稳定性模型
            base_stability = 1.0
            
            # 温度影响
            temperature_effect = np.exp(-(conditions[0] - 298) / 500)
            
            # 氧气含量影响
            oxygen_effect = 1 - 0.3 * (1 - conditions[2])
            
            return base_stability * temperature_effect * oxygen_effect
            
        else:
            # 其他性能指标
            return 0.5  # 默认值
    
    def _evaluate_interaction(self,
                            material_data: Dict,
                            conditions: Dict) -> float:
        """评估条件交互作用
        
        Args:
            material_data: 材料数据
            conditions: 条件字典
            
        Returns:
            性能值
        """
        # 使用标准条件
        all_conditions = {name: cond.value 
                        for name, cond in self.standard_conditions.items()}
        
        # 更新指定条件
        all_conditions.update(conditions)
        
        # 计算性能
        return self._evaluate_performance(
            material_data,
            list(all_conditions.values())
        )
    
    def _generate_processing_notes(self, conditions: Dict) -> List[str]:
        """生成工艺注意事项
        
        Args:
            conditions: 优化后的条件
            
        Returns:
            注意事项列表
        """
        notes = []
        
        # 温度相关注意事项
        if conditions['sintering_temperature']['value'] > 1200:
            notes.append("⚠️ 高温烧结，注意炉体保护和安全")
        
        # 气氛相关注意事项
        if conditions['atmosphere_o2_content']['value'] < 0.1:
            notes.append("⚠️ 低氧气氛，需要特殊气体保护")
        
        # 压制相关注意事项
        if conditions['compaction_pressure']['value'] > 400:
            notes.append("⚠️ 高压压制，注意模具强度")
        
        # 颗粒尺寸相关注意事项
        if conditions['particle_size']['value'] < 0.5:
            notes.append("⚠️ 细颗粒，注意防团聚")
        
        return notes

def main():
    """主函数"""
    print("=== 实验条件影响分析演示 ===")
    
    # 创建分析器实例
    analyzer = ExperimentalConditionAnalyzer()
    
    # 示例材料数据
    material_data = {
        'formula': 'Li7La3Zr2O12',
        'density': 5.1,  # g/cm³
        'particle_size': 1.0,  # μm
        'formation_energy': -12.5  # eV/atom
    }
    
    # 分析温度影响
    temp_impact = analyzer.analyze_condition_impact(
        material_data,
        'temperature',
        (300, 1000)
    )
    
    # 优化条件
    performance_target = {
        'property': 'conductivity',
        'target_value': 1e-3,
        'constraints': {
            'temperature': (300, 800),
            'pressure': (0.5, 2.0)
        }
    }
    
    optimized = analyzer.optimize_conditions(
        material_data,
        'conductivity',
        performance_target['constraints']
    )
    
    # 生成工艺配方
    recipe = analyzer.generate_processing_recipe(
        material_data,
        performance_target
    )
    
    # 打印结果
    print("\n优化后的条件:")
    for name, value in optimized['optimized_conditions'].items():
        print(f"{name}: {value['value']:.2f} {value['unit']}")
    
    print(f"\n预期性能: {optimized['predicted_performance']:.2e}")
    
    print("\n工艺注意事项:")
    for note in recipe['notes']:
        print(note)

if __name__ == '__main__':
    main() 