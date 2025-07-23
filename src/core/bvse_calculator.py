"""BVSE Calculator"""

import numpy as np
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import time

class BVSECalculator:
    """BVSE计算主类"""
    
    def __init__(self):
        # 键价参数 - 常用的几个
        self.bond_params = {
            ('Li', 'O'): {'r0': 1.466, 'b': 0.37},
            ('La', 'O'): {'r0': 2.172, 'b': 0.37},
            ('Zr', 'O'): {'r0': 1.937, 'b': 0.37},
            ('Ti', 'O'): {'r0': 1.815, 'b': 0.37},
            ('Nb', 'O'): {'r0': 1.911, 'b': 0.37},
            ('Ta', 'O'): {'r0': 1.920, 'b': 0.37},
        }
        
        # Li离子半径
        self.li_radius = 0.76
        
        self.results = {}
    
    def load_structure(self, cif_path):
        """从CIF文件加载结构"""
        # 简化版的CIF解析
        structure_data = {
            'atoms': [],
            'lattice': np.eye(3) * 10,  # 默认10A的立方晶胞
            'formula': 'Unknown'
        }
        
        try:
            with open(cif_path, 'r') as f:
                lines = f.readlines()
            
            # 提取化学式
            for line in lines:
                if '_chemical_formula_sum' in line:
                    formula = line.split("'")[1] if "'" in line else line.split()[1]
                    structure_data['formula'] = formula
                    break
            
            # 提取原子坐标 - 简化处理
            coord_start = False
            for line in lines:
                if 'loop_' in line and '_atom_site' in lines[lines.index(line)+1:lines.index(line)+5]:
                    coord_start = True
                    continue
                
                if coord_start and line.strip() and not line.startswith('_'):
                    parts = line.strip().split()
                    if len(parts) >= 6:
                        element = parts[0].split('_')[0]  # 去掉标号
                        x, y, z = float(parts[2]), float(parts[3]), float(parts[4])
                        
                        structure_data['atoms'].append({
                            'element': element,
                            'coords': np.array([x, y, z])
                        })
        
        except Exception as e:
            print(f"解析CIF文件出错: {e}")
            # 返回默认结构
            structure_data['atoms'] = [
                {'element': 'Li', 'coords': np.array([0.0, 0.0, 0.0])},
                {'element': 'O', 'coords': np.array([0.5, 0.5, 0.5])},
            ]
        
        return structure_data
    
    def calc_bond_valence(self, r_ij, bond_params):
        """计算键价"""
        r0, b = bond_params['r0'], bond_params['b']
        return np.exp((r0 - r_ij) / b)
    
    def find_li_sites(self, structure):
        """找Li位点"""
        li_sites = []
        
        for atom in structure['atoms']:
            if atom['element'] == 'Li':
                li_sites.append(atom['coords'])
        
        # 如果没有Li，生成一些可能的位点
        if not li_sites:
            # 简单的网格搜索
            for x in np.arange(0, 1, 0.25):
                for y in np.arange(0, 1, 0.25):
                    for z in np.arange(0, 1, 0.25):
                        li_sites.append(np.array([x, y, z]))
        
        return li_sites
    
    def calc_site_energy(self, site_coords, structure):
        """计算位点能量"""
        total_bv = 0.0
        
        # 找所有氧原子
        oxygen_coords = []
        for atom in structure['atoms']:
            if atom['element'] == 'O':
                oxygen_coords.append(atom['coords'])
        
        if not oxygen_coords:
            return 0.5  # 默认值
        
        # 计算与氧的键价和
        for o_coord in oxygen_coords:
            distance = np.linalg.norm(site_coords - o_coord)
            
            # 考虑周期性边界条件 - 简化版
            if distance > 5.0:  # 距离太远就跳过
                continue
            
            if distance < 0.5:  # 距离太近也跳过
                continue
            
            bond_key = ('Li', 'O')
            if bond_key in self.bond_params:
                bv = self.calc_bond_valence(distance, self.bond_params[bond_key])
                total_bv += bv
        
        # BVSE = |BV_sum - formal_valence|
        formal_valence = 1.0  # Li+
        bvse = abs(total_bv - formal_valence)
        
        return bvse
    
    def find_conduction_paths(self, structure):
        """寻找传导路径"""
        li_sites = self.find_li_sites(structure)
        
        if len(li_sites) < 2:
            return []
        
        paths = []
        
        # 计算所有位点间的距离和能量势垒
        for i, site1 in enumerate(li_sites):
            for j, site2 in enumerate(li_sites[i+1:], i+1):
                distance = np.linalg.norm(site1 - site2)
                
                # 合理的跳跃距离
                if 1.5 < distance < 4.0:
                    # 中点能量作为势垒
                    midpoint = (site1 + site2) / 2
                    barrier = self.calc_site_energy(midpoint, structure)
                    
                    paths.append({
                        'start': i,
                        'end': j,
                        'distance': distance,
                        'barrier': barrier,
                        'start_coords': site1,
                        'end_coords': site2
                    })
        
        # 按势垒排序
        paths.sort(key=lambda x: x['barrier'])
        
        return paths
    
    def calc_activation_energy(self, paths):
        """计算激活能"""
        if not paths:
            return 0.5  # 默认值
        
        # 取最低的几个势垒
        low_barriers = [p['barrier'] for p in paths[:5]]
        
        if not low_barriers:
            return 0.5
        
        # 简单平均
        avg_barrier = np.mean(low_barriers)
        
        # 转换成eV (经验公式)
        activation_energy = avg_barrier * 0.3  # 大概的转换因子
        
        return activation_energy
    
    def run_bvse_analysis(self, cif_path):
        """运行BVSE分析"""
        print(f"分析 {cif_path}...")
        
        start_time = time.time()
        
        # 加载结构
        structure = self.load_structure(cif_path)
        
        # 找Li位点
        li_sites = self.find_li_sites(structure)
        
        # 计算位点能量
        site_energies = []
        for site in li_sites:
            energy = self.calc_site_energy(site, structure)
            site_energies.append(energy)
        
        # 寻找传导路径
        paths = self.find_conduction_paths(structure)
        
        # 计算激活能
        ea = self.calc_activation_energy(paths)
        
        calc_time = time.time() - start_time
        
        # 整理结果
        result = {
            'formula': structure['formula'],
            'li_sites_count': len(li_sites),
            'avg_site_energy': np.mean(site_energies) if site_energies else 0.5,
            'min_site_energy': np.min(site_energies) if site_energies else 0.5,
            'conduction_paths': len(paths),
            'estimated_ea': ea,
            'avg_li_distance': np.mean([p['distance'] for p in paths]) if paths else 3.0,
            'calculation_time': calc_time
        }
        
        # 判断是否合格
        if ea < 0.3 and len(li_sites) >= 2:
            result['qualified'] = True
        else:
            result['qualified'] = False
        
        print(f"完成，用时 {calc_time:.2f}s")
        
        return result
    
    def batch_analysis(self, cif_files):
        """批量分析"""
        print(f"开始批量分析 {len(cif_files)} 个文件...")
        
        all_results = []
        qualified_count = 0
        
        for i, cif_file in enumerate(cif_files):
            try:
                result = self.run_bvse_analysis(cif_file)
                all_results.append(result)
                
                if result['qualified']:
                    qualified_count += 1
                
                print(f"进度: {i+1}/{len(cif_files)}, 合格: {qualified_count}")
                
            except Exception as e:
                print(f"分析 {cif_file} 失败: {e}")
                continue
        
        # 保存结果
        output = {
            'total_analyzed': len(all_results),
            'qualified_count': qualified_count,
            'qualified_materials': [r for r in all_results if r['qualified']],
            'all_results': all_results
        }
        
        with open('bvse_results.json', 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        print(f"\n分析完成！")
        print(f"总计: {len(all_results)} 个材料")
        print(f"合格: {qualified_count} 个")
        print(f"合格率: {qualified_count/len(all_results)*100:.1f}%")
        
        return output
    
    def generate_report(self, results):
        """生成分析报告"""
        report_lines = [
            "# BVSE分析报告",
            f"分析时间: {time.strftime('%Y-%m-%d %H:%M:%S')}",
            f"作者: LunaZhang",
            "",
            "## 统计信息",
            f"总材料数: {results['total_analyzed']}",
            f"合格材料: {results['qualified_count']}",
            f"合格率: {results['qualified_count']/results['total_analyzed']*100:.1f}%",
            "",
            "## 合格材料列表"
        ]
        
        for mat in results['qualified_materials']:
            report_lines.extend([
                f"### {mat['formula']}",
                f"- Li位点数: {mat['li_sites_count']}",
                f"- 估计激活能: {mat['estimated_ea']:.3f} eV",
                f"- 平均Li距离: {mat['avg_li_distance']:.2f} Å",
                f"- 传导路径: {mat['conduction_paths']} 条",
                ""
            ])
        
        report_text = "\n".join(report_lines)
        
        with open('bvse_report.md', 'w', encoding='utf-8') as f:
            f.write(report_text)
        
        print("报告已保存到 bvse_report.md")
        
        return report_text

def main():
    """主函数"""
    print("BVSE计算器")
    print("=" * 30)
    
    calc = BVSECalculator()
    
    # 测试单个文件
    # result = calc.run_bvse_analysis("test.cif")
    # print(result)
    
    # 批量分析
    cif_files = list(Path("data/raw_materials").rglob("*.cif"))
    
    if cif_files:
        print(f"找到 {len(cif_files)} 个CIF文件")
        results = calc.batch_analysis(cif_files)
        calc.generate_report(results)
    else:
        print("没找到CIF文件")

if __name__ == "__main__":
    main() 