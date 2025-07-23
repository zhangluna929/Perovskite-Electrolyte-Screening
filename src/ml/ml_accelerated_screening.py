"""ML-Accelerated Perovskite Materials Screening Platform"""

import numpy as np
import pandas as pd
import json
import pickle
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import matplotlib.pyplot as plt
import seaborn as sns
from pymatgen.core import Structure
from pymatgen.analysis.structure_matcher import StructureMatcher
from pymatgen.analysis.local_env import CrystalNN
import warnings
warnings.filterwarnings('ignore')

plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

class MaterialFeatureExtractor:
    """材料特征提取器"""
    
    def __init__(self):
        self.crystal_nn = CrystalNN()
        
    def extract_composition_features(self, structure):
        """提取组成特征"""
        composition = structure.composition
        features = {}
        
        # 基本组成信息
        features['num_species'] = len(composition.elements)
        features['num_atoms'] = len(structure)
        features['density'] = structure.density
        features['volume_per_atom'] = structure.volume / len(structure)
        
        # 元素属性统计
        atomic_masses = [el.atomic_mass for el in composition.elements]
        atomic_radii = [el.atomic_radius or 1.0 for el in composition.elements]
        electronegativities = [el.X or 2.0 for el in composition.elements]
        
        features['avg_atomic_mass'] = np.mean(atomic_masses)
        features['std_atomic_mass'] = np.std(atomic_masses)
        features['avg_atomic_radius'] = np.mean(atomic_radii)
        features['std_atomic_radius'] = np.std(atomic_radii)
        features['avg_electronegativity'] = np.mean(electronegativities)
        features['std_electronegativity'] = np.std(electronegativities)
        
        # 价电子统计
        valence_electrons = []
        for element in composition.elements:
            if element.Z <= 18:
                valence_electrons.append(element.group)
            else:
                valence_electrons.append(element.group - 10 if element.group > 10 else element.group)
        
        features['avg_valence_electrons'] = np.mean(valence_electrons)
        features['std_valence_electrons'] = np.std(valence_electrons)
        
        return features
    
    def extract_structure_features(self, structure):
        """提取结构特征"""
        features = {}
        
        # 晶格参数
        lattice = structure.lattice
        features['a'] = lattice.a
        features['b'] = lattice.b
        features['c'] = lattice.c
        features['alpha'] = lattice.alpha
        features['beta'] = lattice.beta
        features['gamma'] = lattice.gamma
        features['volume'] = lattice.volume
        
        # 对称性
        sga = structure.get_space_group_info()
        features['space_group_number'] = sga[1]
        features['crystal_system'] = ['triclinic', 'monoclinic', 'orthorhombic', 
                                     'tetragonal', 'trigonal', 'hexagonal', 'cubic'].index(
                                         lattice.get_crystal_system())
        
        # 配位环境
        try:
            coordination_numbers = []
            for i, site in enumerate(structure):
                cn_info = self.crystal_nn.get_cn_dict(structure, i)
                coordination_numbers.append(sum(cn_info.values()))
            
            features['avg_coordination_number'] = np.mean(coordination_numbers)
            features['std_coordination_number'] = np.std(coordination_numbers)
        except:
            features['avg_coordination_number'] = 6.0
            features['std_coordination_number'] = 0.0
        
        # 键长统计
        try:
            bond_lengths = []
            for i, site in enumerate(structure):
                neighbors = structure.get_neighbors(site, 3.0)
                bond_lengths.extend([nn[1] for nn in neighbors])
            
            if bond_lengths:
                features['avg_bond_length'] = np.mean(bond_lengths)
                features['std_bond_length'] = np.std(bond_lengths)
                features['min_bond_length'] = np.min(bond_lengths)
                features['max_bond_length'] = np.max(bond_lengths)
            else:
                features['avg_bond_length'] = 2.0
                features['std_bond_length'] = 0.0
                features['min_bond_length'] = 1.5
                features['max_bond_length'] = 3.0
        except:
            features['avg_bond_length'] = 2.0
            features['std_bond_length'] = 0.0
            features['min_bond_length'] = 1.5
            features['max_bond_length'] = 3.0
        
        return features
    
    def extract_perovskite_features(self, structure):
        """提取钙钛矿特有特征"""
        features = {}
        
        # 容差因子近似计算
        composition = structure.composition
        elements = list(composition.elements)
        
        # 尝试识别A、B、O位点
        try:
            # 假设最大的阳离子为A位，次大的为B位
            cations = [el for el in elements if el.symbol != 'O' and el.symbol != 'F']
            if len(cations) >= 2:
                cations.sort(key=lambda x: x.ionic_radius or x.atomic_radius or 1.0, reverse=True)
                A_site = cations[0]
                B_site = cations[1]
                
                r_A = A_site.ionic_radius or A_site.atomic_radius or 1.0
                r_B = B_site.ionic_radius or B_site.atomic_radius or 1.0
                r_O = 1.4  # 氧离子半径
                
                # 容差因子
                tolerance_factor = (r_A + r_O) / (np.sqrt(2) * (r_B + r_O))
                features['tolerance_factor'] = tolerance_factor
                
                # 八面体因子
                octahedral_factor = r_B / r_O
                features['octahedral_factor'] = octahedral_factor
                
                # 离子半径比
                features['A_B_radius_ratio'] = r_A / r_B
                features['A_O_radius_ratio'] = r_A / r_O
                features['B_O_radius_ratio'] = r_B / r_O
                
        except:
            features['tolerance_factor'] = 1.0
            features['octahedral_factor'] = 0.7
            features['A_B_radius_ratio'] = 1.5
            features['A_O_radius_ratio'] = 2.0
            features['B_O_radius_ratio'] = 1.4
        
        # 氧/氟含量
        o_content = composition.get_atomic_fraction('O') if 'O' in composition else 0
        f_content = composition.get_atomic_fraction('F') if 'F' in composition else 0
        features['oxygen_content'] = o_content
        features['fluorine_content'] = f_content
        features['anion_ratio'] = f_content / (o_content + f_content) if (o_content + f_content) > 0 else 0
        
        return features
    
    def extract_all_features(self, structure):
        """提取所有特征"""
        features = {}
        features.update(self.extract_composition_features(structure))
        features.update(self.extract_structure_features(structure))
        features.update(self.extract_perovskite_features(structure))
        return features

class MLAcceleratedScreening:
    """机器学习加速筛选系统"""
    
    def __init__(self):
        self.feature_extractor = MaterialFeatureExtractor()
        self.scaler = StandardScaler()
        self.models = {}
        self.feature_names = []
        
    def prepare_training_data(self, cif_files, property_data):
        """准备训练数据"""
        print("正在准备训练数据...")
        
        X = []
        y = {}
        material_names = []
        
        for property_name in ['activation_energy', 'conductivity', 'stability']:
            y[property_name] = []
        
        for cif_file in cif_files:
            try:
                structure = Structure.from_file(cif_file)
                features = self.feature_extractor.extract_all_features(structure)
                
                # 获取材料名称
                material_name = cif_file.split('/')[-1].replace('.cif', '')
                
                # 查找对应的性质数据
                property_values = property_data.get(material_name, {})
                
                if property_values:
                    X.append(list(features.values()))
                    material_names.append(material_name)
                    
                    for prop_name in y.keys():
                        y[prop_name].append(property_values.get(prop_name, 0))
                    
                    if not self.feature_names:
                        self.feature_names = list(features.keys())
                        
            except Exception as e:
                print(f"处理文件 {cif_file} 时出错: {e}")
                continue
        
        X = np.array(X)
        for prop_name in y.keys():
            y[prop_name] = np.array(y[prop_name])
        
        print(f"准备了 {len(X)} 个样本，{len(self.feature_names)} 个特征")
        return X, y, material_names
    
    def train_models(self, X, y):
        """训练机器学习模型"""
        print("正在训练机器学习模型...")
        
        # 标准化特征
        X_scaled = self.scaler.fit_transform(X)
        
        # 为每个性质训练模型
        for prop_name, prop_values in y.items():
            print(f"训练 {prop_name} 预测模型...")
            
            # 使用多个模型集成
            models = {
                'rf': RandomForestRegressor(n_estimators=100, random_state=42),
                'gbr': GradientBoostingRegressor(n_estimators=100, random_state=42)
            }
            
            best_model = None
            best_score = -np.inf
            
            for model_name, model in models.items():
                # 交叉验证
                scores = cross_val_score(model, X_scaled, prop_values, cv=5, scoring='r2')
                avg_score = np.mean(scores)
                
                print(f"  {model_name}: R² = {avg_score:.3f} ± {np.std(scores):.3f}")
                
                if avg_score > best_score:
                    best_score = avg_score
                    best_model = model
            
            # 训练最佳模型
            best_model.fit(X_scaled, prop_values)
            self.models[prop_name] = best_model
            
            print(f"  最佳模型 R² = {best_score:.3f}")
        
        print("模型训练完成！")
    
    def predict_properties(self, structures):
        """预测材料性质"""
        predictions = {}
        
        for prop_name in self.models.keys():
            predictions[prop_name] = []
        
        for structure in structures:
            features = self.feature_extractor.extract_all_features(structure)
            feature_vector = np.array([features.get(name, 0) for name in self.feature_names]).reshape(1, -1)
            feature_vector_scaled = self.scaler.transform(feature_vector)
            
            for prop_name, model in self.models.items():
                pred = model.predict(feature_vector_scaled)[0]
                predictions[prop_name].append(pred)
        
        return predictions
    
    def feature_importance_analysis(self):
        """特征重要性分析"""
        print("进行特征重要性分析...")
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        axes = axes.flatten()
        
        for i, (prop_name, model) in enumerate(self.models.items()):
            if hasattr(model, 'feature_importances_'):
                importances = model.feature_importances_
                indices = np.argsort(importances)[::-1][:10]  # 前10个重要特征
                
                ax = axes[i]
                ax.barh(range(len(indices)), importances[indices])
                ax.set_yticks(range(len(indices)))
                ax.set_yticklabels([self.feature_names[i] for i in indices])
                ax.set_xlabel('特征重要性')
                ax.set_title(f'{prop_name} 特征重要性')
                ax.invert_yaxis()
        
        plt.tight_layout()
        plt.savefig('feature_importance_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def validate_models(self, X, y, material_names):
        """模型验证"""
        print("进行模型验证...")
        
        X_scaled = self.scaler.transform(X)
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        axes = axes.flatten()
        
        for i, (prop_name, model) in enumerate(self.models.items()):
            y_pred = model.predict(X_scaled)
            y_true = y[prop_name]
            
            r2 = r2_score(y_true, y_pred)
            mae = mean_absolute_error(y_true, y_pred)
            rmse = np.sqrt(mean_squared_error(y_true, y_pred))
            
            ax = axes[i]
            ax.scatter(y_true, y_pred, alpha=0.7)
            ax.plot([y_true.min(), y_true.max()], [y_true.min(), y_true.max()], 'r--', lw=2)
            ax.set_xlabel(f'真实值 {prop_name}')
            ax.set_ylabel(f'预测值 {prop_name}')
            ax.set_title(f'{prop_name}\nR² = {r2:.3f}, MAE = {mae:.3f}, RMSE = {rmse:.3f}')
            
            # 添加网格
            ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('model_validation.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def save_models(self, filename='ml_models.pkl'):
        """保存模型"""
        model_data = {
            'models': self.models,
            'scaler': self.scaler,
            'feature_names': self.feature_names
        }
        
        with open(filename, 'wb') as f:
            pickle.dump(model_data, f)
        
        print(f"模型已保存至 {filename}")
    
    def load_models(self, filename='ml_models.pkl'):
        """加载模型"""
        with open(filename, 'rb') as f:
            model_data = pickle.load(f)
        
        self.models = model_data['models']
        self.scaler = model_data['scaler']
        self.feature_names = model_data['feature_names']
        
        print(f"模型已从 {filename} 加载")

def create_synthetic_training_data():
    """创建合成训练数据（用于演示）"""
    print("创建合成训练数据...")
    
    # 基于已有筛选结果创建训练数据
    training_data = {
        'Li7La3Zr2O12': {
            'activation_energy': 0.10,
            'conductivity': 1.5e-3,
            'stability': 0.95
        },
        'LiNbO3': {
            'activation_energy': 0.15,
            'conductivity': 1.2e-3,
            'stability': 0.90
        },
        'LiTaO3': {
            'activation_energy': 0.18,
            'conductivity': 8.5e-4,
            'stability': 0.88
        },
        'LiLaTiO4': {
            'activation_energy': 0.25,
            'conductivity': 5.0e-4,
            'stability': 0.85
        },
        'LiLa3Ti2O9': {
            'activation_energy': 0.22,
            'conductivity': 6.2e-4,
            'stability': 0.87
        },
        'BaTiO3': {
            'activation_energy': 0.35,
            'conductivity': 1.0e-5,
            'stability': 0.95
        },
        'SrTiO3': {
            'activation_energy': 0.40,
            'conductivity': 5.0e-6,
            'stability': 0.92
        },
        'LaAlO3': {
            'activation_energy': 0.45,
            'conductivity': 1.0e-6,
            'stability': 0.90
        },
        'LaGaO3': {
            'activation_energy': 0.38,
            'conductivity': 2.0e-6,
            'stability': 0.88
        },
        'CaTiO3': {
            'activation_energy': 0.42,
            'conductivity': 3.0e-6,
            'stability': 0.85
        }
    }
    
    # 添加更多随机数据以增加样本量
    np.random.seed(42)
    for i in range(20):
        material_name = f'synthetic_material_{i}'
        training_data[material_name] = {
            'activation_energy': np.random.uniform(0.15, 0.50),
            'conductivity': 10**np.random.uniform(-6, -2),
            'stability': np.random.uniform(0.70, 0.95)
        }
    
    return training_data

def main():
    """主函数"""
    print("=== 钙钛矿材料机器学习加速筛选平台 ===")
    
    # 初始化系统
    ml_system = MLAcceleratedScreening()
    
    # 获取CIF文件列表
    import glob
    cif_files = glob.glob('**/*.cif', recursive=True)
    print(f"找到 {len(cif_files)} 个CIF文件")
    
    # 创建训练数据
    property_data = create_synthetic_training_data()
    
    # 准备训练数据
    X, y, material_names = ml_system.prepare_training_data(cif_files[:30], property_data)
    
    if len(X) > 0:
        # 训练模型
        ml_system.train_models(X, y)
        
        # 模型验证
        ml_system.validate_models(X, y, material_names)
        
        # 特征重要性分析
        ml_system.feature_importance_analysis()
        
        # 保存模型
        ml_system.save_models()
        
        # 预测新材料
        print("\n=== 预测新材料性质 ===")
        test_structures = []
        for cif_file in cif_files[30:35]:
            try:
                structure = Structure.from_file(cif_file)
                test_structures.append(structure)
            except:
                continue
        
        if test_structures:
            predictions = ml_system.predict_properties(test_structures)
            
            print("\n预测结果:")
            for i, structure in enumerate(test_structures):
                print(f"\n材料 {i+1}: {structure.formula}")
                print(f"  预测激活能: {predictions['activation_energy'][i]:.3f} eV")
                print(f"  预测电导率: {predictions['conductivity'][i]:.2e} S/cm")
                print(f"  预测稳定性: {predictions['stability'][i]:.3f}")
        
        # 生成加速筛选报告
        generate_ml_screening_report(ml_system, predictions, test_structures)
    
    else:
        print("没有足够的训练数据")

def generate_ml_screening_report(ml_system, predictions, test_structures):
    """生成机器学习筛选报告"""
    print("\n生成机器学习筛选报告...")
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # 1. 预测vs真实值对比
    ax1 = axes[0, 0]
    if len(predictions['activation_energy']) > 0:
        ax1.scatter(range(len(predictions['activation_energy'])), 
                   predictions['activation_energy'], 
                   c='red', alpha=0.7, s=100, label='预测激活能')
        ax1.set_xlabel('材料编号')
        ax1.set_ylabel('激活能 (eV)')
        ax1.set_title('激活能预测结果')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
    
    # 2. 电导率预测
    ax2 = axes[0, 1]
    if len(predictions['conductivity']) > 0:
        ax2.scatter(range(len(predictions['conductivity'])), 
                   np.log10(predictions['conductivity']), 
                   c='blue', alpha=0.7, s=100, label='预测电导率')
        ax2.set_xlabel('材料编号')
        ax2.set_ylabel('log₁₀(电导率 S/cm)')
        ax2.set_title('电导率预测结果')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
    
    # 3. 稳定性预测
    ax3 = axes[1, 0]
    if len(predictions['stability']) > 0:
        ax3.scatter(range(len(predictions['stability'])), 
                   predictions['stability'], 
                   c='green', alpha=0.7, s=100, label='预测稳定性')
        ax3.set_xlabel('材料编号')
        ax3.set_ylabel('稳定性')
        ax3.set_title('稳定性预测结果')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
    
    # 4. 综合性能雷达图
    ax4 = axes[1, 1]
    if len(predictions['activation_energy']) > 0:
        # 归一化数据用于雷达图
        norm_activation = 1 - np.array(predictions['activation_energy']) / 0.5  # 激活能越低越好
        norm_conductivity = (np.log10(predictions['conductivity']) + 6) / 4  # 电导率越高越好
        norm_stability = np.array(predictions['stability'])  # 稳定性越高越好
        
        materials = [f'材料{i+1}' for i in range(len(predictions['activation_energy']))]
        
        # 创建综合评分
        overall_scores = (norm_activation + norm_conductivity + norm_stability) / 3
        
        bars = ax4.bar(range(len(overall_scores)), overall_scores, 
                      color=['red', 'orange', 'yellow', 'lightgreen', 'green'],
                      alpha=0.7)
        ax4.set_xlabel('材料编号')
        ax4.set_ylabel('综合评分')
        ax4.set_title('材料综合性能评分')
        ax4.set_ylim(0, 1)
        
        # 添加数值标签
        for i, bar in enumerate(bars):
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                    f'{height:.2f}', ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig('ml_screening_report.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # 保存预测结果
    if test_structures:
        results = []
        for i, structure in enumerate(test_structures):
            results.append({
                'material': structure.formula,
                'predicted_activation_energy': predictions['activation_energy'][i],
                'predicted_conductivity': predictions['conductivity'][i],
                'predicted_stability': predictions['stability'][i],
                'overall_score': (
                    (1 - predictions['activation_energy'][i] / 0.5) + 
                    (np.log10(predictions['conductivity'][i]) + 6) / 4 + 
                    predictions['stability'][i]
                ) / 3
            })
        
        with open('ml_predictions.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print("预测结果已保存至 ml_predictions.json")

if __name__ == "__main__":
    main() 