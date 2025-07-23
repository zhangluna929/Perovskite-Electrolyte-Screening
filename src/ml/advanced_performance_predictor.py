"""Advanced performance prediction model for multi-variable conditions"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_absolute_error, r2_score
import tensorflow as tf
from tensorflow.keras import layers, models
import joblib
from pathlib import Path
import json
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple, Optional
from scipy.integrate import odeint

class AdvancedPerformancePredictor:
    """高级性能预测器"""
    
    def __init__(self):
        self.models = {
            'conductivity': None,  # 电导率模型
            'thermal_stability': None,  # 热稳定性模型
            'cycle_life': None,  # 循环寿命模型
            'mechanical_strength': None  # 机械强度模型
        }
        self.scalers = {}
        self.feature_names = []
        
    def prepare_features(self, material_data: Dict) -> np.ndarray:
        """准备特征向量
        
        Args:
            material_data: 材料数据字典，包含成分、结构等信息
            
        Returns:
            特征向量
        """
        features = []
        
        # 基本描述符
        features.extend([
            material_data.get('avg_atomic_mass', 0),
            material_data.get('density', 0),
            material_data.get('volume_per_atom', 0),
            material_data.get('band_gap', 0),
            material_data.get('formation_energy', 0)
        ])
        
        # 结构特征
        features.extend([
            material_data.get('lattice_a', 0),
            material_data.get('lattice_b', 0),
            material_data.get('lattice_c', 0),
            material_data.get('alpha', 90),
            material_data.get('beta', 90),
            material_data.get('gamma', 90)
        ])
        
        # 掺杂信息
        features.extend([
            material_data.get('dopant_concentration', 0),
            material_data.get('dopant_ionic_radius', 0),
            material_data.get('dopant_electronegativity', 0)
        ])
        
        # 实验条件
        features.extend([
            material_data.get('temperature', 298),
            material_data.get('pressure', 1),
            material_data.get('atmosphere_o2_content', 0.21),
            material_data.get('humidity', 0.5)
        ])
        
        return np.array(features)
    
    def train_models(self, training_data: List[Dict], validation_split: float = 0.2):
        """训练多个性能预测模型
        
        Args:
            training_data: 训练数据列表
            validation_split: 验证集比例
        """
        print("开始训练性能预测模型...")
        
        # 准备数据
        X = np.array([self.prepare_features(data) for data in training_data])
        y = {
            'conductivity': np.array([d.get('conductivity', 0) for d in training_data]),
            'thermal_stability': np.array([d.get('thermal_stability', 0) for d in training_data]),
            'cycle_life': np.array([d.get('cycle_life', 0) for d in training_data]),
            'mechanical_strength': np.array([d.get('mechanical_strength', 0) for d in training_data])
        }
        
        # 对每个性能指标训练单独的模型
        for target_name, target_values in y.items():
            print(f"\n训练 {target_name} 预测模型...")
            
            # 数据标准化
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            self.scalers[target_name] = scaler
            
            # 划分训练集和测试集
            X_train, X_test, y_train, y_test = train_test_split(
                X_scaled, target_values, test_size=validation_split, random_state=42
            )
            
            # 创建和训练模型
            if target_name == 'conductivity':
                # 使用深度神经网络预测电导率
                model = self._build_dnn_model(X_train.shape[1])
                model.fit(X_train, y_train, epochs=100, batch_size=32, validation_split=0.2, verbose=0)
            else:
                # 其他性能使用梯度提升树
                model = GradientBoostingRegressor(
                    n_estimators=100,
                    learning_rate=0.1,
                    max_depth=5,
                    random_state=42
                )
                model.fit(X_train, y_train)
            
            # 评估模型
            y_pred = model.predict(X_test)
            mae = mean_absolute_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            
            print(f"  模型评估结果:")
            print(f"  - MAE: {mae:.4f}")
            print(f"  - R²: {r2:.4f}")
            
            self.models[target_name] = model
    
    def _build_dnn_model(self, input_dim: int) -> tf.keras.Model:
        """构建深度神经网络模型
        
        Args:
            input_dim: 输入维度
            
        Returns:
            编译好的模型
        """
        model = models.Sequential([
            layers.Dense(128, activation='relu', input_dim=input_dim),
            layers.Dropout(0.3),
            layers.Dense(64, activation='relu'),
            layers.Dropout(0.2),
            layers.Dense(32, activation='relu'),
            layers.Dense(1)
        ])
        
        model.compile(optimizer='adam', loss='mse', metrics=['mae'])
        return model
    
    def predict_performance(self, material_data: Dict, conditions: Dict) -> Dict:
        """预测材料在给定条件下的性能
        
        Args:
            material_data: 材料数据
            conditions: 条件参数（温度、气氛等）
            
        Returns:
            性能预测结果
        """
        # 合并材料数据和条件
        input_data = {**material_data, **conditions}
        features = self.prepare_features(input_data)
        
        predictions = {}
        for target_name, model in self.models.items():
            if model is not None:
                # 标准化特征
                X_scaled = self.scalers[target_name].transform(features.reshape(1, -1))
                
                # 预测
                pred = model.predict(X_scaled)[0]
                predictions[target_name] = pred
        
        return predictions
    
    def predict_time_evolution(self, material_data: Dict, conditions: Dict, 
                             time_points: np.ndarray) -> Dict[str, np.ndarray]:
        """预测材料性能随时间的演化
        
        Args:
            material_data: 材料数据
            conditions: 条件参数
            time_points: 时间点数组
            
        Returns:
            各性能指标随时间的变化
        """
        def performance_ode(y, t, material_params):
            """性能演化的微分方程"""
            conductivity, stability = y
            
            # 简化的性能衰减模型
            dcdt = -0.01 * conductivity * (1 - stability)  # 电导率变化
            dsdt = -0.005 * stability  # 稳定性变化
            
            return [dcdt, dsdt]
        
        # 获取初始性能预测
        initial_pred = self.predict_performance(material_data, conditions)
        
        # 初始条件
        y0 = [
            initial_pred.get('conductivity', 0),
            initial_pred.get('thermal_stability', 1)
        ]
        
        # 求解ODE
        solution = odeint(performance_ode, y0, time_points, 
                         args=(material_data,))
        
        return {
            'conductivity': solution[:, 0],
            'thermal_stability': solution[:, 1]
        }
    
    def analyze_condition_sensitivity(self, material_data: Dict, 
                                   parameter_ranges: Dict) -> Dict:
        """分析性能对条件参数的敏感性
        
        Args:
            material_data: 材料数据
            parameter_ranges: 参数范围字典
            
        Returns:
            敏感性分析结果
        """
        sensitivities = {}
        base_prediction = self.predict_performance(material_data, {})
        
        for param, (min_val, max_val) in parameter_ranges.items():
            values = np.linspace(min_val, max_val, 10)
            predictions = []
            
            for val in values:
                conditions = {param: val}
                pred = self.predict_performance(material_data, conditions)
                predictions.append(pred)
            
            # 计算敏感性（相对变化率）
            sensitivity = {}
            for prop in predictions[0].keys():
                baseline = base_prediction[prop]
                if baseline != 0:
                    relative_changes = [(p[prop] - baseline) / baseline 
                                      for p in predictions]
                    sensitivity[prop] = np.std(relative_changes)
                else:
                    sensitivity[prop] = 0
                    
            sensitivities[param] = sensitivity
        
        return sensitivities
    
    def save_models(self, save_dir: str = 'models'):
        """保存模型和标准化器"""
        save_path = Path(save_dir)
        save_path.mkdir(exist_ok=True)
        
        for name, model in self.models.items():
            if model is not None:
                if isinstance(model, tf.keras.Model):
                    model.save(save_path / f'{name}_model')
                else:
                    joblib.dump(model, save_path / f'{name}_model.joblib')
                joblib.dump(self.scalers[name], save_path / f'{name}_scaler.joblib')
    
    def load_models(self, load_dir: str = 'models'):
        """加载保存的模型和标准化器"""
        load_path = Path(load_dir)
        
        for name in self.models.keys():
            model_path = load_path / f'{name}_model'
            scaler_path = load_path / f'{name}_scaler.joblib'
            
            if model_path.exists():
                if model_path.is_dir():  # TensorFlow模型
                    self.models[name] = tf.keras.models.load_model(model_path)
                else:  # scikit-learn模型
                    self.models[name] = joblib.load(model_path)
                    
            if scaler_path.exists():
                self.scalers[name] = joblib.load(scaler_path)

def create_synthetic_training_data(n_samples: int = 1000) -> List[Dict]:
    """创建合成训练数据（用于演示）
    
    Args:
        n_samples: 样本数量
        
    Returns:
        训练数据列表
    """
    np.random.seed(42)
    
    training_data = []
    for _ in range(n_samples):
        # 基本材料参数
        material = {
            'avg_atomic_mass': np.random.uniform(20, 200),
            'density': np.random.uniform(2, 8),
            'volume_per_atom': np.random.uniform(10, 30),
            'band_gap': np.random.uniform(0, 5),
            'formation_energy': np.random.uniform(-10, 0),
            
            # 晶格参数
            'lattice_a': np.random.uniform(3, 6),
            'lattice_b': np.random.uniform(3, 6),
            'lattice_c': np.random.uniform(3, 6),
            'alpha': 90 + np.random.uniform(-5, 5),
            'beta': 90 + np.random.uniform(-5, 5),
            'gamma': 90 + np.random.uniform(-5, 5),
            
            # 掺杂信息
            'dopant_concentration': np.random.uniform(0, 0.1),
            'dopant_ionic_radius': np.random.uniform(0.5, 2),
            'dopant_electronegativity': np.random.uniform(0.9, 3.5),
            
            # 实验条件
            'temperature': np.random.uniform(250, 1000),
            'pressure': np.random.uniform(0.1, 10),
            'atmosphere_o2_content': np.random.uniform(0, 1),
            'humidity': np.random.uniform(0, 1),
            
            # 性能指标（模拟值）
            'conductivity': np.random.lognormal(-5, 1),  # S/cm
            'thermal_stability': np.random.uniform(0, 1),
            'cycle_life': np.random.uniform(100, 1000),
            'mechanical_strength': np.random.uniform(50, 200)
        }
        
        training_data.append(material)
    
    return training_data

def main():
    """主函数"""
    print("=== 高级性能预测模型演示 ===")
    
    # 创建预测器实例
    predictor = AdvancedPerformancePredictor()
    
    # 生成训练数据
    print("\n生成训练数据...")
    training_data = create_synthetic_training_data(1000)
    
    # 训练模型
    print("\n训练模型...")
    predictor.train_models(training_data)
    
    # 测试预测
    print("\n测试预测...")
    test_material = training_data[0]
    test_conditions = {
        'temperature': 300,
        'pressure': 1,
        'atmosphere_o2_content': 0.21,
        'humidity': 0.5
    }
    
    predictions = predictor.predict_performance(test_material, test_conditions)
    print("\n预测结果:")
    for prop, value in predictions.items():
        print(f"{prop}: {value:.4f}")
    
    # 时间演化预测
    print("\n预测性能随时间演化...")
    time_points = np.linspace(0, 1000, 100)
    evolution = predictor.predict_time_evolution(test_material, test_conditions, time_points)
    
    # 条件敏感性分析
    print("\n进行条件敏感性分析...")
    parameter_ranges = {
        'temperature': (250, 1000),
        'pressure': (0.1, 10),
        'atmosphere_o2_content': (0, 1)
    }
    sensitivities = predictor.analyze_condition_sensitivity(test_material, parameter_ranges)
    
    print("\n敏感性分析结果:")
    for param, sensitivity in sensitivities.items():
        print(f"\n{param}:")
        for prop, value in sensitivity.items():
            print(f"  {prop}: {value:.4f}")
    
    # 保存模型
    print("\n保存模型...")
    predictor.save_models()

if __name__ == '__main__':
    main() 