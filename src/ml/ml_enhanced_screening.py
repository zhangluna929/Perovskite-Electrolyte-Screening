#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ML增强的材料筛选
作者：LunaZhang
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, r2_score
import joblib
from pathlib import Path
import json
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple, Optional

class MaterialDescriptorCalculator:
    """计算材料描述符"""
    
    def __init__(self):
        # 常用元素属性数据
        self.elem_props = {
            'Li': {'radius': 1.52, 'electronegativity': 0.98, 'valence': 1},
            'La': {'radius': 1.87, 'electronegativity': 1.10, 'valence': 3},
            'Zr': {'radius': 1.60, 'electronegativity': 1.33, 'valence': 4},
            'Nb': {'radius': 1.46, 'electronegativity': 1.60, 'valence': 5},
            'Ta': {'radius': 1.46, 'electronegativity': 1.50, 'valence': 5},
            'O': {'radius': 0.66, 'electronegativity': 3.44, 'valence': -2},
            'F': {'radius': 0.57, 'electronegativity': 3.98, 'valence': -1}
        }
    
    def calc_descriptors(self, composition):
        """根据化学组成计算描述符"""
        descriptors = {}
        
        total_atoms = sum(composition.values())
        
        # 计算平均原子半径
        avg_radius = sum(
            self.elem_props[elem]['radius'] * count
            for elem, count in composition.items()
            if elem in self.elem_props
        ) / total_atoms
        
        # 计算平均电负性
        avg_electronegativity = sum(
            self.elem_props[elem]['electronegativity'] * count
            for elem, count in composition.items()
            if elem in self.elem_props
        ) / total_atoms
        
        # 电负性方差
        electroneg_list = []
        for elem, count in composition.items():
            if elem in self.elem_props:
                electroneg_list.extend([self.elem_props[elem]['electronegativity']] * count)
        electroneg_variance = np.var(electroneg_list) if electroneg_list else 0
        
        # 钙钛矿ABO3结构分析
        a_site_elems = ['Li', 'La', 'Sr', 'Ba', 'Ca']
        b_site_elems = ['Ti', 'Zr', 'Nb', 'Ta', 'Sn']
        
        a_site_count = sum(composition.get(elem, 0) for elem in a_site_elems)
        b_site_count = sum(composition.get(elem, 0) for elem in b_site_elems)
        
        # 容忍因子计算
        if 'O' in composition:
            r_a = avg_radius
            r_b = 1.5
            r_o = self.elem_props['O']['radius']
            tolerance_factor = (r_a + r_o) / (np.sqrt(2) * (r_b + r_o))
        else:
            tolerance_factor = 1.0
        
        descriptors.update({
            'avg_atomic_radius': avg_radius,
            'avg_electronegativity': avg_electronegativity,
            'electronegativity_variance': electroneg_variance,
            'tolerance_factor': tolerance_factor,
            'a_site_count': a_site_count,
            'b_site_count': b_site_count,
            'oxygen_count': composition.get('O', 0),
            'fluorine_count': composition.get('F', 0),
            'total_atoms': total_atoms,
            'li_concentration': composition.get('Li', 0) / total_atoms,
        })
        
        return descriptors

class MLEnhancedScreening:
    """ML增强的筛选器"""
    
    def __init__(self, base_dir="."):
        self.base_dir = Path(base_dir)
        self.calc = MaterialDescriptorCalculator()
        self.models = {}
        self.scalers = {}
        self.feature_names = []
        
    def prepare_data(self):
        """准备训练数据"""
        print("准备训练数据...")
        
        # 读取BVSE结果
        bvse_file = self.base_dir / "bvse_results.json"
        if not bvse_file.exists():
            raise FileNotFoundError("找不到BVSE结果文件")
        
        with open(bvse_file, 'r', encoding='utf-8') as f:
            bvse_data = json.load(f)
        
        # 提取特征和目标值
        features_list = []
        targets_list = []
        
        for material in bvse_data.get('qualified_materials', []):
            formula = material['formula']
            composition = self._parse_formula(formula)
            
            # 计算描述符
            descriptors = self.calc.calc_descriptors(composition)
            features_list.append(descriptors)
            
            # 目标值
            targets = {
                'activation_energy': material.get('estimated_ea', 0.3),
                'li_sites_count': material.get('li_sites_count', 1),
                'avg_li_distance': material.get('avg_li_distance', 3.0)
            }
            targets_list.append(targets)
        
        features_df = pd.DataFrame(features_list)
        targets_df = pd.DataFrame(targets_list)
        
        # 数据增强
        features_df, targets_df = self._augment_data(features_df, targets_df)
        
        self.feature_names = features_df.columns.tolist()
        
        print(f"数据准备完成: {len(features_df)}个样本, {len(self.feature_names)}个特征")
        return features_df, targets_df
    
    def _parse_formula(self, formula):
        """解析化学式"""
        import re
        
        composition = {}
        formula = formula.replace(' ', '')
        
        # 正则表达式匹配元素和数字
        pattern = r'([A-Z][a-z]?)(\d*)'
        matches = re.findall(pattern, formula)
        
        for element, count in matches:
            count = int(count) if count else 1
            composition[element] = composition.get(element, 0) + count
        
        return composition
    
    def _augment_data(self, features_df, targets_df):
        """数据增强"""
        n_augment = 200
        
        aug_features = []
        aug_targets = []
        
        for _ in range(n_augment):
            # 随机选择一个基础样本
            base_idx = np.random.randint(0, len(features_df))
            base_feat = features_df.iloc[base_idx].copy()
            base_targ = targets_df.iloc[base_idx].copy()
            
            # 添加噪声
            for col in features_df.columns:
                if col in ['li_concentration', 'tolerance_factor']:
                    noise_factor = 0.1
                else:
                    noise_factor = 0.2
                
                noise = np.random.normal(0, noise_factor * abs(base_feat[col]))
                base_feat[col] += noise
            
            # 目标值也加点噪声
            base_targ['activation_energy'] += np.random.normal(0, 0.05)
            base_targ['activation_energy'] = max(0.1, min(0.5, base_targ['activation_energy']))
            
            aug_features.append(base_feat)
            aug_targets.append(base_targ)
        
        # 合并数据
        aug_feat_df = pd.DataFrame(aug_features)
        aug_targ_df = pd.DataFrame(aug_targets)
        
        combined_feat = pd.concat([features_df, aug_feat_df], ignore_index=True)
        combined_targ = pd.concat([targets_df, aug_targ_df], ignore_index=True)
        
        return combined_feat, combined_targ
    
    def train_models(self, features_df, targets_df):
        """训练ML模型"""
        print("开始训练模型...")
        
        # 对每个目标属性训练模型
        for target_col in targets_df.columns:
            print(f"训练 {target_col} 预测模型...")
            
            X = features_df.fillna(0)
            y = targets_df[target_col].fillna(targets_df[target_col].mean())
            
            # 特征标准化
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            self.scalers[target_col] = scaler
            
            # 划分训练测试集
            X_train, X_test, y_train, y_test = train_test_split(
                X_scaled, y, test_size=0.2, random_state=42
            )
            
            # 尝试不同的模型
            models_to_try = {
                'rf': RandomForestRegressor(n_estimators=100, random_state=42),
                'gbm': GradientBoostingRegressor(n_estimators=100, random_state=42)
            }
            
            best_model = None
            best_score = -np.inf
            
            for model_name, model in models_to_try.items():
                # 交叉验证
                cv_scores = cross_val_score(model, X_train, y_train, cv=5, 
                                          scoring='neg_mean_absolute_error')
                mean_score = cv_scores.mean()
                
                print(f"  {model_name}: CV MAE = {-mean_score:.4f}")
                
                if mean_score > best_score:
                    best_score = mean_score
                    best_model = model
            
            # 训练最好的模型
            best_model.fit(X_train, y_train)
            
            # 测试集评估
            y_pred = best_model.predict(X_test)
            test_mae = mean_absolute_error(y_test, y_pred)
            test_r2 = r2_score(y_test, y_pred)
            
            print(f"  测试集 MAE: {test_mae:.4f}, R²: {test_r2:.4f}")
            
            # 保存模型
            self.models[target_col] = best_model
            
            # 特征重要性
            if hasattr(best_model, 'feature_importances_'):
                importance_df = pd.DataFrame({
                    'feature': self.feature_names,
                    'importance': best_model.feature_importances_
                }).sort_values('importance', ascending=False)
                
                print(f"  重要特征 Top 5:")
                for _, row in importance_df.head().iterrows():
                    print(f"    {row['feature']}: {row['importance']:.4f}")
        
        # 保存模型到文件
        self.save_models()
        print("模型训练完成")
    
    def predict_properties(self, composition):
        """预测材料性质"""
        # 计算描述符
        descriptors = self.calc.calc_descriptors(composition)
        
        # 转成DataFrame
        feat_df = pd.DataFrame([descriptors])
        feat_df = feat_df.reindex(columns=self.feature_names, fill_value=0)
        
        predictions = {}
        
        for target, model in self.models.items():
            # 标准化
            scaler = self.scalers[target]
            X_scaled = scaler.transform(feat_df)
            
            # 预测
            pred = model.predict(X_scaled)[0]
            predictions[target] = pred
        
        return predictions
    
    def batch_screening(self, formulas):
        """批量筛选材料"""
        print(f"批量筛选 {len(formulas)} 个材料...")
        
        results = []
        
        for i, formula in enumerate(formulas):
            try:
                composition = self._parse_formula(formula)
                predictions = self.predict_properties(composition)
                
                # 计算综合评分
                score = self._calc_score(predictions)
                
                result = {
                    'formula': formula,
                    'predicted_activation_energy': predictions.get('activation_energy', 0.3),
                    'predicted_li_sites': predictions.get('li_sites_count', 1),
                    'predicted_li_distance': predictions.get('avg_li_distance', 3.0),
                    'composite_score': score,
                    'recommended': score > 0.7
                }
                
                results.append(result)
                
                if (i + 1) % 50 == 0:
                    print(f"已处理 {i + 1}/{len(formulas)}")
                    
            except Exception as e:
                print(f"处理 {formula} 出错: {e}")
        
        results_df = pd.DataFrame(results)
        results_df = results_df.sort_values('composite_score', ascending=False)
        
        print(f"筛选完成，推荐 {len(results_df[results_df['recommended']])} 个材料")
        
        return results_df
    
    def _calc_score(self, predictions):
        """计算综合评分"""
        # 激活能评分 (越低越好)
        ea = predictions.get('activation_energy', 0.3)
        ea_score = max(0, 1 - ea / 0.3)  
        
        # Li位点数评分
        li_sites = predictions.get('li_sites_count', 1)
        li_sites_score = min(1, li_sites / 4)  
        
        # Li-Li距离评分
        li_distance = predictions.get('avg_li_distance', 3.0)
        li_distance_score = 1 / (1 + abs(li_distance - 2.5))
        
        # 加权平均
        score = (
            0.5 * ea_score +
            0.3 * li_sites_score +
            0.2 * li_distance_score
        )
        
        return score
    
    def save_models(self):
        """保存训练好的模型"""
        models_dir = self.base_dir / "ml_models"
        models_dir.mkdir(exist_ok=True)
        
        # 保存模型和标准化器
        for target, model in self.models.items():
            joblib.dump(model, models_dir / f"{target}_model.pkl")
            joblib.dump(self.scalers[target], models_dir / f"{target}_scaler.pkl")
        
        # 保存特征名称
        with open(models_dir / "feature_names.json", 'w') as f:
            json.dump(self.feature_names, f)
        
        print(f"模型保存到 {models_dir}")
    
    def load_models(self):
        """加载预训练模型"""
        models_dir = self.base_dir / "ml_models"
        
        if not models_dir.exists():
            print("没找到预训练模型")
            return False
        
        try:
            # 加载特征名称
            with open(models_dir / "feature_names.json", 'r') as f:
                self.feature_names = json.load(f)
            
            # 加载模型
            for model_file in models_dir.glob("*_model.pkl"):
                target = model_file.stem.replace("_model", "")
                self.models[target] = joblib.load(model_file)
                
                scaler_file = models_dir / f"{target}_scaler.pkl"
                if scaler_file.exists():
                    self.scalers[target] = joblib.load(scaler_file)
            
            print(f"加载了 {len(self.models)} 个模型")
            return True
            
        except Exception as e:
            print(f"加载模型失败: {e}")
            return False
    
    def generate_materials(self, n_materials=100):
        """生成新的候选材料化学式"""
        print(f"生成 {n_materials} 个新材料...")
        
        # 元素组合规则
        a_site_elems = ['Li', 'La', 'Sr', 'Ba']
        b_site_elems = ['Zr', 'Nb', 'Ta', 'Sn']
        anions = ['O', 'F']
        
        formulas = []
        
        for _ in range(n_materials):
            # 随机选择元素
            a_elem = np.random.choice(a_site_elems)
            b_elem = np.random.choice(b_site_elems)
            anion = np.random.choice(anions)
            
            # 随机配比
            if a_elem == 'Li':
                a_count = np.random.randint(1, 8)
            else:
                a_count = np.random.randint(1, 4)
            
            b_count = np.random.randint(1, 6)
            anion_count = np.random.randint(3, 15)
            
            # 构造化学式
            formula = f"{a_elem}{a_count}{b_elem}{b_count}{anion}{anion_count}"
            formulas.append(formula)
        
        return formulas

def main():
    """主函数"""
    print("ML增强材料筛选系统")
    print("=" * 40)
    
    # 创建筛选器
    screener = MLEnhancedScreening()
    
    # 尝试加载已有模型
    if not screener.load_models():
        print("开始训练新模型...")
        
        # 准备数据
        features_df, targets_df = screener.prepare_data()
        
        # 训练模型
        screener.train_models(features_df, targets_df)
    
    # 生成新材料
    new_materials = screener.generate_materials(200)
    
    # 批量筛选
    results = screener.batch_screening(new_materials)
    
    # 保存结果
    output_file = "ml_screening_results.csv"
    results.to_csv(output_file, index=False)
    
    # 显示最好的候选
    print(f"\nTop 10 推荐材料:")
    print("=" * 40)
    top_materials = results.head(10)
    
    for _, mat in top_materials.iterrows():
        print(f"材料: {mat['formula']}")
        print(f"  激活能: {mat['predicted_activation_energy']:.3f} eV")
        print(f"  Li位点: {mat['predicted_li_sites']:.1f}")
        print(f"  评分: {mat['composite_score']:.3f}")
        print(f"  推荐: {'是' if mat['recommended'] else '否'}")
        print()
    
    print(f"结果保存到 {output_file}")
    print(f"发现 {len(results[results['recommended']])} 个推荐材料")

if __name__ == "__main__":
    main() 