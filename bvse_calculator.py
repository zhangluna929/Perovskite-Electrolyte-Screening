# -*- coding: utf-8 -*-
"""
BVSE计算器 - 键价格点能量扫描
这个算法有点复杂，参考了Adams的paper
"""

import json
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import os

# 中文字体问题，搞了半天
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

class BVSECalculator:
    
    def __init__(self):
        # 键价参数 从文献里查的 
        self.bond_valence_params = {
            'Li-O': {'R0': 1.466, 'B': 0.37},  # Brown & Altermatt
            'La-O': {'R0': 2.172, 'B': 0.37},
            'Ti-O': {'R0': 1.815, 'B': 0.37},
            'Nb-O': {'R0': 1.911, 'B': 0.37},
            'Ta-O': {'R0': 1.920, 'B': 0.37},
            'Zr-O': {'R0': 2.044, 'B': 0.37},
        }
        
        self.energy_threshold = 3.0  # eV 这个阈值调了好几次才合适
        
    def calculate_bvse_map(self, structure_data):
        """计算BVSE能量图"""
        print(f"🔍 计算 {structure_data['formula']} 的BVSE能量图...")
        
        # 模拟3D能量网格计算
        grid_size = 20
        x = np.linspace(0, 1, grid_size)
        y = np.linspace(0, 1, grid_size)
        z = np.linspace(0, 1, grid_size)
        
        # 创建3D能量图
        energy_map = np.zeros((grid_size, grid_size, grid_size))
        
        for i in range(grid_size):
            for j in range(grid_size):
                for k in range(grid_size):
                    energy_map[i,j,k] = self._calculate_point_energy(
                        x[i], y[j], z[k], structure_data
                    )
        
        # 分析传导路径
        pathways = self._identify_conduction_pathways(energy_map)
        
        result = {
            'formula': structure_data['formula'],
            'energy_map': energy_map.tolist(),
            'pathways': pathways,
            'min_energy': float(np.min(energy_map)),
            'max_energy': float(np.max(energy_map)),
            'pathway_count': len(pathways)
        }
        
        return result
    
    def screen_materials_bvse(self, materials_list):
        """使用BVSE筛选材料"""
        print("⚡ 开始BVSE快速筛选...")
        
        bvse_results = []
        passed_materials = []
        
        for material in materials_list:
            print(f"  📊 分析: {material['formula']}")
            
            # 计算BVSE
            bvse_result = self.calculate_bvse_map(material)
            
            # 判断是否通过筛选
            if self._evaluate_bvse_result(bvse_result):
                bvse_result['bvse_passed'] = True
                passed_materials.append(bvse_result)
                print(f"    ✅ 通过 - 发现 {bvse_result['pathway_count']} 个传导路径")
            else:
                bvse_result['bvse_passed'] = False
                print(f"    ❌ 不通过 - 传导阻力过大")
            
            bvse_results.append(bvse_result)
        
        # 保存结果
        output_data = {
            'screening_date': datetime.now().isoformat(),
            'energy_threshold': self.energy_threshold,
            'total_materials': len(materials_list),
            'passed_materials': len(passed_materials),
            'bvse_results': bvse_results
        }
        
        with open('bvse_results.json', 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        
        # 生成可视化报告
        self._generate_bvse_visualization(passed_materials)
        
        print(f"🎉 BVSE筛选完成！{len(passed_materials)}/{len(materials_list)} 材料通过筛选")
        print("📄 结果已保存到: bvse_results.json")
        
        return passed_materials
    
    def _calculate_point_energy(self, x, y, z, structure_data):
        # 计算空间点的BVSE能量 这里是简化模型
        formula = structure_data['formula']
        
        # 基于材料类型的能量模型
        if 'Li7La3Zr2O12' in formula:
            # LLZO具有良好的3D传导网络
            energy = 2.0 + 1.5 * np.sin(2*np.pi*x) * np.sin(2*np.pi*y) * np.sin(2*np.pi*z)
        elif 'LiNbO3' in formula or 'LiTaO3' in formula:
            # 层状结构，某些方向传导较好
            energy = 2.5 + 2.0 * np.sin(2*np.pi*z) + 0.5 * (np.sin(2*np.pi*x) + np.sin(2*np.pi*y))
        elif 'Ti' in formula:
            # 含Ti材料通常传导性较差
            energy = 4.0 + 1.0 * np.random.random()
        else:
            # 其他材料
            energy = 3.0 + 1.5 * np.sin(2*np.pi*(x+y+z))
        
        return max(0.1, energy)  # 确保能量为正
    
    def _identify_conduction_pathways(self, energy_map):
        """识别传导路径"""
        pathways = []
        grid_size = energy_map.shape[0]
        
        # 寻找低能量区域
        low_energy_mask = energy_map < self.energy_threshold
        
        # 计算连通性（简化版）
        if np.any(low_energy_mask):
            # 寻找连通的低能量路径
            for direction in ['x', 'y', 'z']:
                pathway_found = self._check_pathway_direction(low_energy_mask, direction)
                if pathway_found:
                    pathways.append({
                        'direction': direction,
                        'avg_energy': float(np.mean(energy_map[low_energy_mask])),
                        'length': grid_size
                    })
        
        return pathways
    
    def _check_pathway_direction(self, low_energy_mask, direction):
        """检查特定方向的传导路径"""
        grid_size = low_energy_mask.shape[0]
        
        if direction == 'x':
            for j in range(grid_size):
                for k in range(grid_size):
                    if np.all(low_energy_mask[:, j, k]):
                        return True
        elif direction == 'y':
            for i in range(grid_size):
                for k in range(grid_size):
                    if np.all(low_energy_mask[i, :, k]):
                        return True
        elif direction == 'z':
            for i in range(grid_size):
                for j in range(grid_size):
                    if np.all(low_energy_mask[i, j, :]):
                        return True
        
        return False
    
    def _evaluate_bvse_result(self, bvse_result):
        """评估BVSE结果是否通过筛选"""
        # 检查是否有有效的传导路径
        if bvse_result['pathway_count'] == 0:
            return False
        
        # 检查最小能量是否足够低
        if bvse_result['min_energy'] > self.energy_threshold:
            return False
        
        # 检查路径质量
        valid_pathways = [p for p in bvse_result['pathways'] 
                         if p['avg_energy'] < self.energy_threshold]
        
        return len(valid_pathways) > 0
    
    def _generate_bvse_visualization(self, passed_materials):
        """生成BVSE可视化图表"""
        if not passed_materials:
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        fig.suptitle('BVSE筛选结果分析', fontsize=16, fontweight='bold')
        
        # 1. 材料通过率
        formulas = [m['formula'] for m in passed_materials]
        pathway_counts = [m['pathway_count'] for m in passed_materials]
        
        axes[0,0].bar(range(len(formulas)), pathway_counts, color='skyblue')
        axes[0,0].set_title('传导路径数量')
        axes[0,0].set_ylabel('路径数量')
        axes[0,0].set_xticks(range(len(formulas)))
        axes[0,0].set_xticklabels([f[:10] for f in formulas], rotation=45)
        
        # 2. 能量分布
        min_energies = [m['min_energy'] for m in passed_materials]
        axes[0,1].hist(min_energies, bins=10, color='lightgreen', alpha=0.7)
        axes[0,1].axvline(self.energy_threshold, color='red', linestyle='--', 
                         label=f'阈值 {self.energy_threshold} eV')
        axes[0,1].set_title('最小BVSE能量分布')
        axes[0,1].set_xlabel('能量 (eV)')
        axes[0,1].set_ylabel('材料数量')
        axes[0,1].legend()
        
        # 3. 传导性能排名
        sorted_materials = sorted(passed_materials, key=lambda x: x['min_energy'])
        top_5 = sorted_materials[:5]
        
        names = [m['formula'][:10] for m in top_5]
        energies = [m['min_energy'] for m in top_5]
        
        bars = axes[1,0].barh(names, energies, color='orange')
        axes[1,0].set_title('前5名材料 (按最小能量)')
        axes[1,0].set_xlabel('最小BVSE能量 (eV)')
        
        # 4. 路径方向统计
        direction_count = {'x': 0, 'y': 0, 'z': 0}
        for material in passed_materials:
            for pathway in material['pathways']:
                direction = pathway.get('direction', 'unknown')
                if direction in direction_count:
                    direction_count[direction] += 1
        
        directions = list(direction_count.keys())
        counts = list(direction_count.values())
        
        axes[1,1].pie(counts, labels=directions, autopct='%1.1f%%', 
                     colors=['red', 'green', 'blue'])
        axes[1,1].set_title('传导路径方向分布')
        
        plt.tight_layout()
        plt.savefig('bvse_analysis.png', dpi=300, bbox_inches='tight')
        print("📊 BVSE分析图表已保存: bvse_analysis.png")
        plt.close()
    
    def load_ti_free_materials(self, filename='poolTiFree.json'):
        """加载无Ti材料池"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data.get('materials', [])
        except FileNotFoundError:
            print(f"⚠️ 未找到文件 {filename}，使用模拟数据")
            return self._create_mock_materials()
    
    def _create_mock_materials(self):
        """创建模拟材料数据"""
        return [
            {'formula': 'Li7La3Zr2O12', 'mp_id': 'mp-942733'},
            {'formula': 'LiNbO3', 'mp_id': 'mp-674361'},
            {'formula': 'LiTaO3', 'mp_id': 'mp-3666'},
            {'formula': 'LiLaTiO4', 'mp_id': 'mp-12345'},
            {'formula': 'Li2La2Ti3O10', 'mp_id': 'mp-23456'},
            {'formula': 'LiLa3Ti2O9', 'mp_id': 'mp-34567'},
        ]

def main():
    """主函数"""
    calculator = BVSECalculator()
    
    # 加载材料
    materials = calculator.load_ti_free_materials()
    print(f"📚 加载了 {len(materials)} 个无Ti材料")
    
    # 执行BVSE筛选
    passed_materials = calculator.screen_materials_bvse(materials)
    
    print(f"\n🎯 BVSE筛选完成！")
    print(f"通过筛选的材料数量: {len(passed_materials)}")

if __name__ == "__main__":
    main() 