#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
钙钛矿电解质筛选平台 - 集成版本
整合PINN模型、高级特征工程和分布式计算
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional
import numpy as np
import pandas as pd
from datetime import datetime

from src.ml.physics_informed_nn import ConductivityPINN, StabilityPINN
from src.ml.advanced_feature_engineering import AdvancedFeatureExtractor
from src.core.distributed_computing import DistributedComputingManager, TaskMonitor
from src.core.perovskite_screening import PerovskiteScreening

class IntegratedPlatform:
    """集成筛选平台"""
    
    def __init__(self, base_dir: str = "."):
        self.base_dir = Path(base_dir)
        
        # 初始化日志
        self._setup_logging()
        
        # 初始化各个组件
        self.feature_extractor = AdvancedFeatureExtractor()
        self.compute_manager = DistributedComputingManager(num_nodes=4)
        self.task_monitor = TaskMonitor()
        self.screening = PerovskiteScreening()
        
        # 初始化PINN模型
        self.conductivity_pinn = ConductivityPINN(input_dim=50)  # 假设特征维度为50
        self.stability_pinn = StabilityPINN(input_dim=50)
        
        # 性能指标
        self.performance_targets = {
            'ionic_conductivity': 1e-3,  # S/cm
            'activation_energy': 0.3,    # eV
            'thermal_stability': 400,    # °C
            'cycle_life': 2000          # 循环次数
        }
        
        self.logger.info("集成平台初始化完成")
    
    def _setup_logging(self):
        """设置日志系统"""
        log_dir = self.base_dir / "logs"
        log_dir.mkdir(exist_ok=True)
        
        log_file = log_dir / f"screening_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger("IntegratedPlatform")
    
    async def screen_materials(self, 
                             material_files: List[str],
                             custom_targets: Optional[Dict] = None) -> pd.DataFrame:
        """筛选材料"""
        if custom_targets:
            self.performance_targets.update(custom_targets)
        
        self.logger.info(f"开始筛选 {len(material_files)} 个材料")
        
        # 准备计算任务
        tasks = []
        for file in material_files:
            # 加载结构
            structure = self.screening.load_material(file)
            
            # 提取特征
            features = self.feature_extractor.extract_all_features(structure)
            
            # 创建计算任务
            tasks.append({
                'type': 'material_screening',
                'structure': structure,
                'features': features,
                'file_path': file
            })
        
        # 提交任务到分布式系统
        task_ids = self.compute_manager.submit_batch_tasks(tasks)
        
        # 运行计算
        results = await self.compute_manager.run_tasks()
        
        # 处理结果
        screening_results = []
        for task_id, result in results.items():
            if result.get('status') == 'success':
                processed_result = self._process_screening_result(result)
                screening_results.append(processed_result)
            else:
                self.logger.error(f"任务 {task_id} 失败: {result.get('error')}")
        
        # 转换为DataFrame
        results_df = pd.DataFrame(screening_results)
        
        # 保存结果
        self._save_results(results_df)
        
        return results_df
    
    def _process_screening_result(self, result: Dict) -> Dict:
        """处理筛选结果"""
        processed = {
            'formula': result.get('formula', 'Unknown'),
            'conductivity': result.get('conductivity', 0.0),
            'activation_energy': result.get('activation_energy', 0.0),
            'thermal_stability': result.get('thermal_stability', 0.0),
            'cycle_life': result.get('cycle_life', 0),
            'computation_time': result.get('computation_time', 0.0)
        }
        
        # 计算综合得分
        processed['score'] = self._calculate_score(processed)
        
        # 判断是否达到目标
        processed['meets_targets'] = all([
            processed['conductivity'] >= self.performance_targets['ionic_conductivity'],
            processed['activation_energy'] <= self.performance_targets['activation_energy'],
            processed['thermal_stability'] >= self.performance_targets['thermal_stability'],
            processed['cycle_life'] >= self.performance_targets['cycle_life']
        ])
        
        return processed
    
    def _calculate_score(self, result: Dict) -> float:
        """计算综合得分"""
        weights = {
            'conductivity': 0.4,
            'activation_energy': 0.3,
            'thermal_stability': 0.2,
            'cycle_life': 0.1
        }
        
        # 归一化各个指标
        normalized = {
            'conductivity': min(result['conductivity'] / self.performance_targets['ionic_conductivity'], 1.0),
            'activation_energy': max(0, 1 - result['activation_energy'] / self.performance_targets['activation_energy']),
            'thermal_stability': min(result['thermal_stability'] / self.performance_targets['thermal_stability'], 1.0),
            'cycle_life': min(result['cycle_life'] / self.performance_targets['cycle_life'], 1.0)
        }
        
        # 计算加权得分
        score = sum(normalized[k] * weights[k] for k in weights)
        
        return score
    
    def _save_results(self, results_df: pd.DataFrame):
        """保存筛选结果"""
        # 创建结果目录
        results_dir = self.base_dir / "results"
        results_dir.mkdir(exist_ok=True)
        
        # 保存详细结果
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = results_dir / f"screening_results_{timestamp}.csv"
        results_df.to_csv(results_file, index=False)
        
        # 生成统计报告
        report = self._generate_report(results_df)
        report_file = results_dir / f"screening_report_{timestamp}.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        self.logger.info(f"结果已保存到 {results_dir}")
    
    def _generate_report(self, results_df: pd.DataFrame) -> str:
        """生成筛选报告"""
        total_materials = len(results_df)
        qualified_materials = len(results_df[results_df['meets_targets']])
        
        report = [
            "钙钛矿电解质材料筛选报告",
            "=" * 40,
            f"\n筛选时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"\n总览:",
            f"- 筛选材料总数: {total_materials}",
            f"- 合格材料数量: {qualified_materials}",
            f"- 合格率: {qualified_materials/total_materials*100:.1f}%",
            
            "\n性能指标统计:",
            f"- 离子电导率 (S/cm):",
            f"  - 最大值: {results_df['conductivity'].max():.2e}",
            f"  - 平均值: {results_df['conductivity'].mean():.2e}",
            f"  - 目标值: {self.performance_targets['ionic_conductivity']:.2e}",
            
            f"\n- 激活能 (eV):",
            f"  - 最小值: {results_df['activation_energy'].min():.3f}",
            f"  - 平均值: {results_df['activation_energy'].mean():.3f}",
            f"  - 目标值: {self.performance_targets['activation_energy']:.3f}",
            
            f"\n- 热稳定性 (°C):",
            f"  - 最大值: {results_df['thermal_stability'].max():.1f}",
            f"  - 平均值: {results_df['thermal_stability'].mean():.1f}",
            f"  - 目标值: {self.performance_targets['thermal_stability']:.1f}",
            
            f"\n- 循环寿命 (次):",
            f"  - 最大值: {results_df['cycle_life'].max():.0f}",
            f"  - 平均值: {results_df['cycle_life'].mean():.0f}",
            f"  - 目标值: {self.performance_targets['cycle_life']:.0f}",
            
            "\n计算性能:",
            f"- 总计算时间: {results_df['computation_time'].sum():.1f} 秒",
            f"- 平均计算时间: {results_df['computation_time'].mean():.1f} 秒/材料",
            
            "\n推荐材料:",
        ]
        
        # 添加top5推荐材料
        top_materials = results_df.nlargest(5, 'score')
        for _, material in top_materials.iterrows():
            report.extend([
                f"\n{material['formula']}:",
                f"- 综合得分: {material['score']:.3f}",
                f"- 离子电导率: {material['conductivity']:.2e} S/cm",
                f"- 激活能: {material['activation_energy']:.3f} eV",
                f"- 热稳定性: {material['thermal_stability']:.1f} °C",
                f"- 循环寿命: {material['cycle_life']:.0f} 次"
            ])
        
        return "\n".join(report)
    
    def shutdown(self):
        """关闭平台"""
        self.compute_manager.shutdown()
        self.logger.info("平台已关闭")

def main():
    """主函数"""
    # 初始化平台
    platform = IntegratedPlatform()
    
    # 设置材料文件
    material_files = [
        "raw_materials/01Li-La-Ti–O₃ 主族， NbZrAlGa 衍生物/LaTiO3.cif",
        "raw_materials/02经典钙钛矿锂氧族 (TaNb 系)/LiNbO3.cif",
        "raw_materials/03SrBaCa 基 Ti-O 钙钛矿/SrTiO3.cif"
    ]
    
    # 设置自定义目标
    custom_targets = {
        'ionic_conductivity': 5e-3,  # 提高目标
        'cycle_life': 3000          # 提高目标
    }
    
    try:
        # 运行筛选
        import asyncio
        results = asyncio.run(
            platform.screen_materials(material_files, custom_targets)
        )
        
        # 打印结果
        print("\n筛选结果:")
        print(results)
        
    finally:
        # 关闭平台
        platform.shutdown()

if __name__ == "__main__":
    main() 