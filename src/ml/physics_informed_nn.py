#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
物理信息神经网络模块
作者：LunaZhang
"""

import torch
import torch.nn as nn
import numpy as np
from typing import Dict, List, Tuple, Optional

class PhysicsNN(nn.Module):
    """
    带物理约束的神经网络基类
    """
    
    def __init__(self, input_dim, hidden_dim=128):
        super().__init__()
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        
        # 网络结构 - 3层隐藏层，经验上效果不错
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1)
        )
        
        # 物理约束 - 这些是硬限制
        self.physics_limits = {
            'min_conductivity': 1e-6,  # S/cm
            'max_activation_energy': 1.0,  # eV
            'min_thermal_stability': 300,  # °C
            'max_volume_change': 0.1,  
        }
    
    def forward(self, x):
        """前向传播"""
        return self.net(x)
    
    def physics_loss(self, pred, target):
        """
        带物理约束的损失函数
        """
        # 基本的MSE损失
        mse_loss = nn.MSELoss()(pred, target)
        
        # 物理违约惩罚
        physics_penalty = torch.zeros_like(mse_loss)
        
        # 电导率下限约束
        cond_mask = pred < self.physics_limits['min_conductivity']
        physics_penalty += torch.sum(
            torch.abs(pred[cond_mask] - self.physics_limits['min_conductivity'])
        )
        
        # 激活能上限约束
        ea_mask = pred > self.physics_limits['max_activation_energy']
        physics_penalty += torch.sum(
            torch.abs(pred[ea_mask] - self.physics_limits['max_activation_energy'])
        )
        
        # 总损失 = 数据拟合 + 物理约束
        total_loss = mse_loss + 0.1 * physics_penalty
        
        return total_loss
    
    def check_predictions(self, predictions):
        """
        检查预测结果是否合理
        """
        violations = {
            'conductivity': [],
            'activation_energy': [],
            'thermal_stability': [],
            'volume_change': []
        }
        
        # 修正不合理的预测
        corrected_preds = predictions.copy()
        
        # 电导率检查
        bad_mask = corrected_preds < self.physics_limits['min_conductivity']
        if np.any(bad_mask):
            violations['conductivity'].append(
                f"发现{np.sum(bad_mask)}个电导率过低的预测"
            )
            corrected_preds[bad_mask] = self.physics_limits['min_conductivity']
        
        # 激活能检查
        bad_mask = corrected_preds > self.physics_limits['max_activation_energy']
        if np.any(bad_mask):
            violations['activation_energy'].append(
                f"发现{np.sum(bad_mask)}个激活能过高的预测"
            )
            corrected_preds[bad_mask] = self.physics_limits['max_activation_energy']
        
        return corrected_preds, violations
    
    def uncertainty_estimate(self, x, n_samples=100):
        """
        用Monte Carlo Dropout估计不确定性
        """
        self.train()  # 开启dropout
        
        preds = []
        for _ in range(n_samples):
            with torch.no_grad():
                pred = self.forward(x)
                preds.append(pred.numpy())
        
        # 统计
        preds = np.array(preds)
        mean_pred = np.mean(preds, axis=0)
        std_pred = np.std(preds, axis=0)
        
        return mean_pred, std_pred

class ConductivityPINN(PhysicsNN):
    """
    专门预测离子电导率的物理网络
    """
    
    def __init__(self, input_dim):
        super().__init__(input_dim)
        
        # 电导率特有的约束
        self.physics_limits.update({
            'temperature_dependence': True,  # 考虑温度依赖
            'concentration_effect': True,    # 考虑浓度效应
        })
    
    def arrhenius_loss(self, conductivity, temperature, activation_energy):
        """
        阿伦尼乌斯方程约束
        σ = σ0 * exp(-Ea/kT)
        """
        k_B = 8.617333262e-5  # eV/K
        expected_cond = torch.exp(-activation_energy / (k_B * temperature))
        
        return nn.MSELoss()(conductivity, expected_cond)
    
    def nernst_einstein_loss(self, conductivity, diffusion_coeff, concentration, temperature):
        """
        纳恩斯特-爱因斯坦方程约束
        σ = (F²/RT) * D * c
        """
        F = 96485.3321233100184  # C/mol
        R = 8.31446261815324  # J/(mol·K)
        
        expected_cond = (F**2 / (R * temperature)) * diffusion_coeff * concentration
        
        return nn.MSELoss()(conductivity, expected_cond)

class StabilityPINN(PhysicsNN):
    """
    专门预测材料稳定性的物理网络
    """
    
    def __init__(self, input_dim):
        super().__init__(input_dim)
        
        # 稳定性相关约束
        self.physics_limits.update({
            'gibbs_energy_threshold': 0.0,  # 吉布斯自由能阈值
            'phase_transition_temp': 0.0,   # 相变温度
        })
    
    def gibbs_energy_loss(self, energy, temperature, entropy):
        """
        吉布斯自由能约束
        G = H - TS
        """
        expected_energy = energy - temperature * entropy
        return torch.mean(torch.relu(-expected_energy))  # 惩罚不稳定态

def test_pinn():
    """
    测试PINN模型
    """
    # 创建测试数据
    input_dim = 10
    n_samples = 100
    X = torch.randn(n_samples, input_dim)
    y = torch.randn(n_samples, 1)
    
    # 测试电导率PINN
    print("测试电导率PINN...")
    cond_model = ConductivityPINN(input_dim)
    pred = cond_model(X)
    loss = cond_model.physics_loss(pred, y)
    print(f"损失: {loss.item():.4f}")
    
    # 测试稳定性PINN
    print("\n测试稳定性PINN...")
    stab_model = StabilityPINN(input_dim)
    pred = stab_model(X)
    loss = stab_model.physics_loss(pred, y)
    print(f"损失: {loss.item():.4f}")
    
    # 测试不确定性估计
    print("\n测试不确定性估计...")
    mean_pred, std_pred = cond_model.uncertainty_estimate(X)
    print(f"预测均值范围: [{mean_pred.min():.4f}, {mean_pred.max():.4f}]")
    print(f"预测标准差范围: [{std_pred.min():.4f}, {std_pred.max():.4f}]")

if __name__ == "__main__":
    test_pinn() 