# coding: utf-8
"""
机器学习筛选模块
sklearn调了好久参数，终于能跑了
"""

import json
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, r2_score
import warnings
warnings.filterwarnings('ignore')  # sklearn的警告太多了

# 中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

class MLEnhancedScreening:
    
    def __init__(self):
        # 存储训练好的模型
        self.models = {
            'conductivity': None,
            'activation_energy': None,
            'stability': None
        }
        self.scaler = StandardScaler()  # 特征标准化
        self.feature_names = []  # 特征名称列表
        
    def extract_features(self, materials_data):
        """提取材料特征"""
        print("🔍 提取材料特征...")
        
        features = []
        
        for material in materials_data:
            formula = material.get('formula', 'LiMO3')
            
            # 基础组成特征
            feature_vector = [
                self._count_element(formula, 'Li'),    # Li含量
                self._count_element(formula, 'La'),    # La含量
                self._count_element(formula, 'Ti'),    # Ti含量
                self._count_element(formula, 'Nb'),    # Nb含量
                self._count_element(formula, 'Ta'),    # Ta含量
                self._count_element(formula, 'Zr'),    # Zr含量
                self._count_element(formula, 'O'),     # O含量
                self._calculate_ionic_radius_avg(formula),  # 平均离子半径
                self._calculate_electronegativity_diff(formula),  # 电负性差
                self._calculate_tolerance_factor(formula),  # 容忍因子
                len(formula),  # 化学式长度（复杂度指标）
                formula.count('2') + formula.count('3') + formula.count('7'),  # 化学计量数
            ]
            
            features.append(feature_vector)
        
        self.feature_names = [
            'Li_count', 'La_count', 'Ti_count', 'Nb_count', 'Ta_count', 'Zr_count', 'O_count',
            'avg_ionic_radius', 'electronegativity_diff', 'tolerance_factor', 
            'formula_complexity', 'stoichiometry_sum'
        ]
        
        return np.array(features)
    
    def train_models(self, training_data=None):
        """训练机器学习模型"""
        print("🤖 训练机器学习模型...")
        
        if training_data is None:
            training_data = self._generate_training_data()
        
        # 提取特征
        X = self.extract_features(training_data)
        
        # 准备标签
        y_conductivity = [m.get('ionic_conductivity', 1e-3) for m in training_data]
        y_activation = [m.get('activation_energy', 0.2) for m in training_data]
        y_stability = [m.get('stability', 0.3) for m in training_data]
        
        # 标准化特征
        X_scaled = self.scaler.fit_transform(X)
        
        # 训练模型
        print("  📊 训练电导率预测模型...")
        self.models['conductivity'] = self._train_model(X_scaled, y_conductivity, 'conductivity')
        
        print("  ⚡ 训练激活能预测模型...")
        self.models['activation_energy'] = self._train_model(X_scaled, y_activation, 'activation_energy')
        
        print("  🏗️ 训练稳定性预测模型...")
        self.models['stability'] = self._train_model(X_scaled, y_stability, 'stability')
        
        print("✅ 所有模型训练完成！")
        
        # 生成特征重要性分析
        self._analyze_feature_importance()
    
    def _train_model(self, X, y, property_name):
        """训练单个预测模型"""
        # 分割训练集和测试集
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # 创建模型集成
        rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
        gb_model = GradientBoostingRegressor(n_estimators=100, random_state=42)
        
        # 训练模型
        rf_model.fit(X_train, y_train)
        gb_model.fit(X_train, y_train)
        
        # 评估模型
        rf_pred = rf_model.predict(X_test)
        gb_pred = gb_model.predict(X_test)
        
        rf_r2 = r2_score(y_test, rf_pred)
        gb_r2 = r2_score(y_test, gb_pred)
        
        # 选择最佳模型
        if rf_r2 > gb_r2:
            best_model = rf_model
            print(f"    选择随机森林模型 (R² = {rf_r2:.3f})")
        else:
            best_model = gb_model
            print(f"    选择梯度提升模型 (R² = {gb_r2:.3f})")
        
        return best_model
    
    def predict_properties(self, materials_data):
        """预测材料性能"""
        print("🔮 预测材料性能...")
        
        if not all(self.models.values()):
            print("⚠️ 模型未训练，先训练模型...")
            self.train_models()
        
        # 提取特征
        X = self.extract_features(materials_data)
        X_scaled = self.scaler.transform(X)
        
        # 预测性能
        predictions = []
        for i, material in enumerate(materials_data):
            pred = {
                'formula': material.get('formula', f'Material_{i}'),
                'predicted_conductivity': self.models['conductivity'].predict([X_scaled[i]])[0],
                'predicted_activation_energy': self.models['activation_energy'].predict([X_scaled[i]])[0],
                'predicted_stability': self.models['stability'].predict([X_scaled[i]])[0],
            }
            
            # 计算综合评分
            pred['ml_score'] = self._calculate_ml_score(pred)
            predictions.append(pred)
        
        # 按评分排序
        predictions.sort(key=lambda x: x['ml_score'], reverse=True)
        
        print(f"✅ 完成 {len(predictions)} 个材料的性能预测")
        return predictions
    
    def ml_accelerated_screening(self, materials_pool):
        """机器学习加速筛选"""
        print("🚀 开始ML加速筛选...")
        
        # 预测性能
        predictions = self.predict_properties(materials_pool)
        
        # 应用筛选标准
        candidates = []
        criteria = {
            'min_conductivity': 1e-3,
            'max_activation_energy': 0.3,
            'min_stability': 0.1
        }
        
        for pred in predictions:
            if (pred['predicted_conductivity'] >= criteria['min_conductivity'] and
                pred['predicted_activation_energy'] <= criteria['max_activation_energy'] and
                pred['predicted_stability'] >= criteria['min_stability']):
                
                pred['ml_passed'] = True
                candidates.append(pred)
            else:
                pred['ml_passed'] = False
        
        # 保存结果
        result_data = {
            'screening_date': datetime.now().isoformat(),
            'total_materials': len(materials_pool),
            'ml_candidates': len(candidates),
            'screening_criteria': criteria,
            'top_candidates': candidates[:10],  # 保存前10名
            'all_predictions': predictions
        }
        
        with open('ml_predictions.json', 'w', encoding='utf-8') as f:
            json.dump(result_data, f, ensure_ascii=False, indent=2)
        
        # 生成可视化
        self._generate_ml_visualization(predictions, candidates)
        
        print(f"🎉 ML筛选完成！筛选出 {len(candidates)} 个候选材料")
        print("📄 结果已保存: ml_predictions.json")
        
        return candidates
    
    def _analyze_feature_importance(self):
        """分析特征重要性"""
        print("📊 分析特征重要性...")
        
        fig, axes = plt.subplots(1, 3, figsize=(18, 6))
        fig.suptitle('机器学习模型特征重要性分析', fontsize=16, fontweight='bold')
        
        properties = ['conductivity', 'activation_energy', 'stability']
        titles = ['离子电导率', '激活能', '稳定性']
        
        for i, (prop, title) in enumerate(zip(properties, titles)):
            if hasattr(self.models[prop], 'feature_importances_'):
                importance = self.models[prop].feature_importances_
                
                # 排序特征重要性
                indices = np.argsort(importance)[::-1]
                
                axes[i].bar(range(len(importance)), importance[indices])
                axes[i].set_title(f'{title}预测模型')
                axes[i].set_ylabel('特征重要性')
                axes[i].set_xticks(range(len(importance)))
                axes[i].set_xticklabels([self.feature_names[j] for j in indices], rotation=45)
        
        plt.tight_layout()
        plt.savefig('ml_feature_importance.png', dpi=300, bbox_inches='tight')
        print("📊 特征重要性图已保存: ml_feature_importance.png")
        plt.close()
    
    def _generate_ml_visualization(self, predictions, candidates):
        """生成ML可视化结果"""
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('机器学习筛选结果', fontsize=16, fontweight='bold')
        
        # 1. 预测性能分布
        conductivities = [p['predicted_conductivity'] for p in predictions]
        activation_energies = [p['predicted_activation_energy'] for p in predictions]
        
        axes[0,0].scatter(activation_energies, conductivities, alpha=0.6)
        axes[0,0].set_xlabel('预测激活能 (eV)')
        axes[0,0].set_ylabel('预测电导率 (S/cm)')
        axes[0,0].set_yscale('log')
        axes[0,0].set_title('性能预测分布')
        
        # 标记候选材料
        cand_conductivities = [c['predicted_conductivity'] for c in candidates]
        cand_activation_energies = [c['predicted_activation_energy'] for c in candidates]
        axes[0,0].scatter(cand_activation_energies, cand_conductivities, 
                         color='red', s=100, label='ML候选材料')
        axes[0,0].legend()
        
        # 2. ML评分排名
        top_10 = predictions[:10]
        formulas = [p['formula'][:8] for p in top_10]
        scores = [p['ml_score'] for p in top_10]
        
        axes[0,1].barh(formulas, scores, color='lightgreen')
        axes[0,1].set_xlabel('ML综合评分')
        axes[0,1].set_title('Top 10 材料排名')
        
        # 3. 筛选通过率
        passed_count = len(candidates)
        total_count = len(predictions)
        failed_count = total_count - passed_count
        
        labels = ['通过ML筛选', '未通过筛选']
        sizes = [passed_count, failed_count]
        colors = ['lightgreen', 'lightcoral']
        
        axes[1,0].pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%')
        axes[1,0].set_title('ML筛选通过率')
        
        # 4. 性能预测对比
        if len(candidates) >= 3:
            top_3 = candidates[:3]
            
            materials = [c['formula'][:10] for c in top_3]
            conductivity_vals = [c['predicted_conductivity'] for c in top_3]
            activation_vals = [c['predicted_activation_energy'] for c in top_3]
            
            x = np.arange(len(materials))
            width = 0.35
            
            ax2 = axes[1,1]
            ax2_twin = ax2.twinx()
            
            bars1 = ax2.bar(x - width/2, conductivity_vals, width, label='电导率', color='blue', alpha=0.7)
            bars2 = ax2_twin.bar(x + width/2, activation_vals, width, label='激活能', color='red', alpha=0.7)
            
            ax2.set_xlabel('材料')
            ax2.set_ylabel('电导率 (S/cm)', color='blue')
            ax2_twin.set_ylabel('激活能 (eV)', color='red')
            ax2.set_title('Top 3 材料性能对比')
            ax2.set_xticks(x)
            ax2.set_xticklabels(materials, rotation=45)
            
            # 添加图例
            lines1, labels1 = ax2.get_legend_handles_labels()
            lines2, labels2 = ax2_twin.get_legend_handles_labels()
            ax2.legend(lines1 + lines2, labels1 + labels2, loc='upper right')
        
        plt.tight_layout()
        plt.savefig('ml_acceleration_results.png', dpi=300, bbox_inches='tight')
        print("📊 ML结果图表已保存: ml_acceleration_results.png")
        plt.close()
    
    def _count_element(self, formula, element):
        """计算元素数量"""
        if element not in formula:
            return 0
        
        # 简化的元素计数（实际应该用更复杂的解析）
        if f'{element}7' in formula:
            return 7
        elif f'{element}3' in formula:
            return 3
        elif f'{element}2' in formula:
            return 2
        elif element in formula:
            return 1
        else:
            return 0
    
    def _calculate_ionic_radius_avg(self, formula):
        """计算平均离子半径（简化）"""
        # 常见离子半径 (Å)
        radii = {'Li': 0.76, 'La': 1.16, 'Ti': 0.605, 'Nb': 0.64, 'Ta': 0.64, 'Zr': 0.72, 'O': 1.40}
        
        total_radius = 0
        total_atoms = 0
        
        for element, radius in radii.items():
            count = self._count_element(formula, element)
            total_radius += count * radius
            total_atoms += count
        
        return total_radius / max(total_atoms, 1)
    
    def _calculate_electronegativity_diff(self, formula):
        """计算电负性差（简化）"""
        # Pauling电负性
        electroneg = {'Li': 0.98, 'La': 1.1, 'Ti': 1.54, 'Nb': 1.6, 'Ta': 1.5, 'Zr': 1.33, 'O': 3.44}
        
        values = []
        for element, en in electroneg.items():
            if element in formula:
                values.append(en)
        
        return max(values) - min(values) if values else 0
    
    def _calculate_tolerance_factor(self, formula):
        """计算容忍因子（简化）"""
        # 这是一个简化的计算，实际需要更精确的结构信息
        if 'Li' in formula and 'O' in formula:
            # 基于经验公式的简化计算
            return 0.9 + 0.1 * np.random.random()
        return 1.0
    
    def _calculate_ml_score(self, prediction):
        """计算ML综合评分"""
        # 归一化和加权评分
        conductivity_score = min(prediction['predicted_conductivity'] / 1e-2, 1.0) * 0.4
        activation_score = max(0, 1 - prediction['predicted_activation_energy'] / 0.3) * 0.4
        stability_score = min(prediction['predicted_stability'] / 0.5, 1.0) * 0.2
        
        return conductivity_score + activation_score + stability_score
    
    def _generate_training_data(self):
        """生成训练数据（模拟已知材料性能）"""
        training_materials = [
            {
                'formula': 'Li7La3Zr2O12',
                'ionic_conductivity': 1.5e-3,
                'activation_energy': 0.10,
                'stability': 0.45
            },
            {
                'formula': 'LiNbO3',
                'ionic_conductivity': 1.2e-3,
                'activation_energy': 0.15,
                'stability': 0.35
            },
            {
                'formula': 'LiTaO3',
                'ionic_conductivity': 8.5e-4,
                'activation_energy': 0.18,
                'stability': 0.30
            },
            {
                'formula': 'LaAlO3',
                'ionic_conductivity': 1e-6,
                'activation_energy': 0.8,
                'stability': 0.25
            },
            {
                'formula': 'SrTiO3',
                'ionic_conductivity': 1e-8,
                'activation_energy': 1.2,
                'stability': 0.20
            },
            # 添加更多训练数据...
        ]
        
        # 扩展训练数据（添加一些变化）
        extended_data = []
        for material in training_materials:
            extended_data.append(material)
            
            # 添加一些噪声变化的数据
            for i in range(3):
                variant = material.copy()
                variant['ionic_conductivity'] *= (1 + 0.1 * np.random.randn())
                variant['activation_energy'] *= (1 + 0.05 * np.random.randn())
                variant['stability'] *= (1 + 0.1 * np.random.randn())
                extended_data.append(variant)
        
        return extended_data

def main():
    """主函数"""
    ml_screener = MLEnhancedScreening()
    
    # 创建模拟材料池
    materials_pool = [
        {'formula': 'Li7La3Zr2O12'},
        {'formula': 'LiNbO3'},
        {'formula': 'LiTaO3'},
        {'formula': 'Li2La2Ti3O10'},
        {'formula': 'LiLaTiO4'},
        {'formula': 'LaAlO3'},
        {'formula': 'SrTiO3'},
    ]
    
    print(f"📚 材料池包含 {len(materials_pool)} 个材料")
    
    # 执行ML加速筛选
    candidates = ml_screener.ml_accelerated_screening(materials_pool)
    
    print(f"\n🎯 ML筛选完成！")
    print(f"发现 {len(candidates)} 个优秀候选材料")

if __name__ == "__main__":
    main() 