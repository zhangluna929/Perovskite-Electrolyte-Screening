#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高级特征工程模块
用于提取和处理复杂的材料描述符
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from pymatgen.core import Structure, Element
from pymatgen.analysis.local_env import VoronoiNN
from pymatgen.analysis.defects import VacancyGenerator
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer

class AdvancedFeatureExtractor:
    """高级特征提取器"""
    
    def __init__(self):
        # 初始化元素属性数据库
        self.element_properties = {
            'Li': {
                'ionic_radius': 0.76,
                'electronegativity': 0.98,
                'oxidation_states': [1],
                'electron_affinity': 59.6,
                'polarizability': 24.3
            },
            'La': {
                'ionic_radius': 1.06,
                'electronegativity': 1.10,
                'oxidation_states': [3],
                'electron_affinity': 48.0,
                'polarizability': 31.1
            },
            # 可以添加更多元素
        }
        
        # 缺陷能量数据库（示例值）
        self.defect_formation_energies = {
            'Li_vacancy': 0.5,  # eV
            'O_vacancy': 2.0,   # eV
            'Li_interstitial': 1.0,  # eV
        }
    
    def extract_structural_features(self, structure: Structure) -> Dict:
        """提取结构特征"""
        features = {}
        
        # 基本结构参数
        features['volume'] = structure.volume
        features['density'] = structure.density
        features['num_sites'] = len(structure)
        
        # 晶体对称性
        spacegroup = SpacegroupAnalyzer(structure)
        features['crystal_system'] = spacegroup.get_crystal_system()
        features['space_group_number'] = spacegroup.get_space_group_number()
        features['point_group'] = spacegroup.get_point_group_symbol()
        
        # 配位环境
        voronoi = VoronoiNN()
        coord_numbers = []
        for site in structure:
            try:
                coord_numbers.append(len(voronoi.get_nn_info(structure, structure.index(site))))
            except:
                coord_numbers.append(0)
        
        features['avg_coordination_number'] = np.mean(coord_numbers)
        features['std_coordination_number'] = np.std(coord_numbers)
        
        return features
    
    def extract_defect_features(self, structure: Structure) -> Dict:
        """提取缺陷相关特征"""
        features = {}
        
        # 生成空位缺陷
        vacancy_generator = VacancyGenerator(structure)
        vacancies = vacancy_generator.generate()
        
        # 计算缺陷浓度
        features['vacancy_concentration'] = len(vacancies) / len(structure)
        
        # 估算缺陷形成能
        defect_energies = []
        for vacancy in vacancies:
            element = vacancy.site.specie.symbol
            if f"{element}_vacancy" in self.defect_formation_energies:
                defect_energies.append(self.defect_formation_energies[f"{element}_vacancy"])
        
        if defect_energies:
            features['avg_defect_formation_energy'] = np.mean(defect_energies)
            features['min_defect_formation_energy'] = np.min(defect_energies)
        else:
            features['avg_defect_formation_energy'] = 0.0
            features['min_defect_formation_energy'] = 0.0
        
        return features
    
    def extract_electronic_features(self, structure: Structure) -> Dict:
        """提取电子结构特征"""
        features = {}
        
        # 计算平均电负性
        electronegativities = []
        for site in structure:
            if site.specie.symbol in self.element_properties:
                electronegativities.append(
                    self.element_properties[site.specie.symbol]['electronegativity']
                )
        
        features['avg_electronegativity'] = np.mean(electronegativities)
        features['std_electronegativity'] = np.std(electronegativities)
        
        # 计算极化率
        polarizabilities = []
        for site in structure:
            if site.specie.symbol in self.element_properties:
                polarizabilities.append(
                    self.element_properties[site.specie.symbol]['polarizability']
                )
        
        features['avg_polarizability'] = np.mean(polarizabilities)
        features['total_polarizability'] = np.sum(polarizabilities)
        
        return features
    
    def extract_doping_features(self, structure: Structure, dopants: List[str]) -> Dict:
        """提取掺杂相关特征"""
        features = {}
        
        # 计算掺杂浓度
        total_sites = len(structure)
        dopant_counts = {}
        
        for site in structure:
            if site.specie.symbol in dopants:
                dopant_counts[site.specie.symbol] = dopant_counts.get(site.specie.symbol, 0) + 1
        
        for dopant in dopants:
            features[f'{dopant}_concentration'] = dopant_counts.get(dopant, 0) / total_sites
        
        # 计算掺杂位点的局部环境
        voronoi = VoronoiNN()
        dopant_environments = []
        
        for site_idx, site in enumerate(structure):
            if site.specie.symbol in dopants:
                try:
                    nn_info = voronoi.get_nn_info(structure, site_idx)
                    dopant_environments.extend([n['site'].specie.symbol for n in nn_info])
                except:
                    continue
        
        if dopant_environments:
            # 统计掺杂位点的配位环境
            unique_neighbors, counts = np.unique(dopant_environments, return_counts=True)
            for neighbor, count in zip(unique_neighbors, counts):
                features[f'dopant_neighbor_{neighbor}'] = count / len(dopant_environments)
        
        return features
    
    def extract_ion_transport_features(self, structure: Structure) -> Dict:
        """提取离子传输相关特征"""
        features = {}
        
        # 计算通道尺寸
        voronoi = VoronoiNN()
        channel_radii = []
        
        for site_idx, site in enumerate(structure):
            if site.specie.symbol == 'Li':  # 假设Li是迁移离子
                try:
                    nn_info = voronoi.get_nn_info(structure, site_idx)
                    # 估算通道半径为到最近邻的最小距离
                    distances = [n['distance'] for n in nn_info]
                    channel_radii.append(min(distances) / 2)
                except:
                    continue
        
        if channel_radii:
            features['min_channel_radius'] = np.min(channel_radii)
            features['avg_channel_radius'] = np.mean(channel_radii)
            features['std_channel_radius'] = np.std(channel_radii)
        else:
            features['min_channel_radius'] = 0.0
            features['avg_channel_radius'] = 0.0
            features['std_channel_radius'] = 0.0
        
        # 计算Li-Li距离
        li_distances = []
        li_sites = [site for site in structure if site.specie.symbol == 'Li']
        
        for i, site1 in enumerate(li_sites):
            for site2 in li_sites[i+1:]:
                distance = structure.get_distance(structure.index(site1),
                                               structure.index(site2))
                li_distances.append(distance)
        
        if li_distances:
            features['min_li_li_distance'] = np.min(li_distances)
            features['avg_li_li_distance'] = np.mean(li_distances)
            features['std_li_li_distance'] = np.std(li_distances)
        else:
            features['min_li_li_distance'] = 0.0
            features['avg_li_li_distance'] = 0.0
            features['std_li_li_distance'] = 0.0
        
        return features
    
    def extract_all_features(self, 
                           structure: Structure,
                           dopants: Optional[List[str]] = None) -> Dict:
        """提取所有特征"""
        all_features = {}
        
        # 提取各类特征
        structural_features = self.extract_structural_features(structure)
        defect_features = self.extract_defect_features(structure)
        electronic_features = self.extract_electronic_features(structure)
        transport_features = self.extract_ion_transport_features(structure)
        
        # 合并特征
        all_features.update(structural_features)
        all_features.update(defect_features)
        all_features.update(electronic_features)
        all_features.update(transport_features)
        
        # 如果提供了掺杂元素信息，则提取掺杂特征
        if dopants:
            doping_features = self.extract_doping_features(structure, dopants)
            all_features.update(doping_features)
        
        return all_features

def main():
    """主函数 - 特征提取测试"""
    from pymatgen.core import Structure
    
    # 加载示例结构
    structure = Structure.from_file("path/to/structure.cif")
    
    # 创建特征提取器
    extractor = AdvancedFeatureExtractor()
    
    # 提取所有特征
    features = extractor.extract_all_features(
        structure,
        dopants=['Nb', 'Ta']
    )
    
    # 打印特征
    print("提取的特征:")
    for name, value in features.items():
        print(f"{name}: {value}")

if __name__ == "__main__":
    main() 