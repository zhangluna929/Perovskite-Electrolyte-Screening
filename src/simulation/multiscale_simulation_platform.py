"""Multi-scale Simulation Platform for Perovskite Materials"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import json
import os
from datetime import datetime
from pymatgen.core import Structure
from pymatgen.analysis.diffusion.aimd.pathway import ProbabilityDensityAnalysis
from pymatgen.analysis.diffusion.aimd.van_hove import VanHoveAnalysis
import warnings
warnings.filterwarnings('ignore')

plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

class AtomicScaleSimulation:
    """原子尺度仿真 (Å级别)"""
    
    def __init__(self, structure):
        self.structure = structure
        self.temperature = 300  # K
        self.time_step = 0.001  # ps
        self.total_time = 1.0   # ns
        
    def dft_calculation(self):
        """DFT计算 (简化版)"""
        print("执行DFT计算...")
        
        # 模拟DFT计算结果
        results = {
            'total_energy': -1234.56,  # eV
            'formation_energy': -2.34,  # eV/atom
            'band_gap': 3.2,  # eV
            'bulk_modulus': 180.5,  # GPa
            'shear_modulus': 85.3,  # GPa
            'elastic_constants': np.random.rand(6, 6) * 100,  # GPa
            'phonon_frequencies': np.random.rand(3 * len(self.structure)) * 1000,  # cm⁻¹
        }
        
        return results
    
    def neb_calculation(self):
        """NEB迁移路径计算"""
        print("执行NEB迁移路径计算...")
        
        # 模拟NEB计算
        path_length = 20
        reaction_coordinate = np.linspace(0, 1, path_length)
        
        # 生成能量曲线
        barrier_height = 0.15 + np.random.normal(0, 0.05)
        energy_profile = barrier_height * np.exp(-((reaction_coordinate - 0.5) / 0.15)**2)
        
        results = {
            'reaction_coordinate': reaction_coordinate,
            'energy_profile': energy_profile,
            'activation_energy': np.max(energy_profile),
            'migration_path': self._generate_migration_path(),
            'jump_frequency': 1e12 * np.exp(-barrier_height / (8.617e-5 * self.temperature))  # Hz
        }
        
        return results
    
    def _generate_migration_path(self):
        """生成迁移路径坐标"""
        # 简化的3D迁移路径
        t = np.linspace(0, 2*np.pi, 20)
        x = np.cos(t) * 0.5
        y = np.sin(t) * 0.5
        z = np.sin(2*t) * 0.2
        
        return np.column_stack([x, y, z])
    
    def md_simulation(self):
        """分子动力学模拟"""
        print("执行分子动力学模拟...")
        
        # 模拟MD轨迹
        n_steps = int(self.total_time / self.time_step)
        n_atoms = len(self.structure)
        
        # 生成模拟轨迹
        trajectory = np.random.normal(0, 0.1, (n_steps, n_atoms, 3))
        
        # 计算扩散系数
        msd = np.array([np.mean(np.sum(traj**2, axis=2)) for traj in trajectory])
        time_array = np.arange(n_steps) * self.time_step
        
        # 线性拟合获得扩散系数
        diffusion_coeff = np.polyfit(time_array[100:], msd[100:], 1)[0] / 6  # cm²/s
        
        results = {
            'trajectory': trajectory,
            'msd': msd,
            'diffusion_coefficient': diffusion_coeff,
            'conductivity': self._calculate_conductivity(diffusion_coeff),
            'activation_energy': self._calculate_activation_energy()
        }
        
        return results
    
    def _calculate_conductivity(self, diffusion_coeff):
        """由扩散系数计算离子电导率"""
        # 使用Nernst-Einstein方程
        charge = 1  # Li+离子电荷
        concentration = 1e22  # 载流子浓度 cm⁻³
        k_B = 1.381e-23  # J/K
        e = 1.602e-19   # C
        
        conductivity = (charge**2 * e**2 * concentration * diffusion_coeff) / (k_B * self.temperature)
        return conductivity
    
    def _calculate_activation_energy(self):
        """计算激活能"""
        # 简化计算
        return 0.15 + np.random.normal(0, 0.05)

class MesoscaleSimulation:
    """介观尺度仿真 (μm级别)"""
    
    def __init__(self, atomic_results):
        self.atomic_results = atomic_results
        self.grain_size = 1.0  # μm
        self.grain_boundary_thickness = 1.0  # nm
        
    def microstructure_modeling(self):
        """微结构建模"""
        print("执行微结构建模...")
        
        # 生成2D微结构
        nx, ny = 100, 100
        microstructure = np.random.randint(0, 10, (nx, ny))
        
        # 晶界效应
        grain_boundary_map = self._generate_grain_boundaries(microstructure)
        
        results = {
            'microstructure': microstructure,
            'grain_boundary_map': grain_boundary_map,
            'average_grain_size': self.grain_size,
            'grain_boundary_density': np.sum(grain_boundary_map) / (nx * ny),
            'effective_conductivity': self._calculate_effective_conductivity(grain_boundary_map)
        }
        
        return results
    
    def _generate_grain_boundaries(self, microstructure):
        """生成晶界图"""
        from scipy import ndimage
        
        # 检测晶界
        grain_boundaries = np.zeros_like(microstructure)
        
        # 简化的晶界检测
        for i in range(1, microstructure.shape[0]-1):
            for j in range(1, microstructure.shape[1]-1):
                if (microstructure[i, j] != microstructure[i-1, j] or
                    microstructure[i, j] != microstructure[i+1, j] or
                    microstructure[i, j] != microstructure[i, j-1] or
                    microstructure[i, j] != microstructure[i, j+1]):
                    grain_boundaries[i, j] = 1
        
        return grain_boundaries
    
    def _calculate_effective_conductivity(self, grain_boundary_map):
        """计算有效电导率"""
        # 考虑晶界电阻
        bulk_conductivity = self.atomic_results.get('conductivity', 1e-3)
        grain_boundary_conductivity = bulk_conductivity * 0.01  # 晶界电导率通常很低
        
        gb_fraction = np.sum(grain_boundary_map) / grain_boundary_map.size
        
        # 串联电阻模型
        effective_conductivity = 1 / (
            (1 - gb_fraction) / bulk_conductivity + 
            gb_fraction / grain_boundary_conductivity
        )
        
        return effective_conductivity
    
    def phase_field_modeling(self):
        """相场建模"""
        print("执行相场建模...")
        
        # 简化的相场模拟
        nx, ny = 50, 50
        dx, dy = 0.1, 0.1  # μm
        
        # 初始化相场
        phi = np.random.rand(nx, ny) * 0.1
        
        # 模拟相演化
        for step in range(100):
            phi = self._phase_field_evolution(phi, dx, dy)
        
        results = {
            'final_phase_field': phi,
            'phase_fraction': np.mean(phi > 0.5),
            'interface_energy': self._calculate_interface_energy(phi),
            'microstructure_evolution': self._analyze_microstructure_evolution(phi)
        }
        
        return results
    
    def _phase_field_evolution(self, phi, dx, dy):
        """相场演化计算"""
        # 简化的Allen-Cahn方程
        M = 1.0  # 迁移率
        kappa = 0.1  # 梯度能系数
        
        # 计算拉普拉斯算子
        laplacian = (np.roll(phi, 1, axis=0) + np.roll(phi, -1, axis=0) +
                    np.roll(phi, 1, axis=1) + np.roll(phi, -1, axis=1) - 4*phi) / (dx**2)
        
        # 化学势
        mu = phi**3 - phi - kappa * laplacian
        
        # 更新相场
        phi_new = phi + M * 0.01 * (np.roll(mu, 1, axis=0) + np.roll(mu, -1, axis=0) +
                                   np.roll(mu, 1, axis=1) + np.roll(mu, -1, axis=1) - 4*mu)
        
        return phi_new
    
    def _calculate_interface_energy(self, phi):
        """计算界面能"""
        # 简化计算
        gradient_x = np.gradient(phi, axis=0)
        gradient_y = np.gradient(phi, axis=1)
        gradient_magnitude = np.sqrt(gradient_x**2 + gradient_y**2)
        
        return np.mean(gradient_magnitude)
    
    def _analyze_microstructure_evolution(self, phi):
        """分析微结构演化"""
        return {
            'average_phase_size': np.mean(phi[phi > 0.5]),
            'phase_connectivity': self._calculate_connectivity(phi),
            'interface_roughness': np.std(phi)
        }
    
    def _calculate_connectivity(self, phi):
        """计算相连通性"""
        # 简化的连通性计算
        binary_phase = phi > 0.5
        return np.sum(binary_phase) / binary_phase.size

class MacroscaleSimulation:
    """宏观尺度仿真 (mm-cm级别)"""
    
    def __init__(self, mesoscale_results):
        self.mesoscale_results = mesoscale_results
        self.device_size = 1.0  # cm
        
    def continuum_modeling(self):
        """连续介质建模"""
        print("执行连续介质建模...")
        
        # 有限元网格
        nx, ny = 20, 20
        x = np.linspace(0, self.device_size, nx)
        y = np.linspace(0, self.device_size, ny)
        X, Y = np.meshgrid(x, y)
        
        # 电导率分布
        conductivity_field = np.ones((nx, ny)) * self.mesoscale_results.get('effective_conductivity', 1e-3)
        
        # 添加非均匀性
        conductivity_field += np.random.normal(0, conductivity_field * 0.1)
        
        # 解泊松方程 (简化)
        potential_field = self._solve_poisson_equation(conductivity_field)
        
        results = {
            'mesh_coordinates': (X, Y),
            'conductivity_field': conductivity_field,
            'potential_field': potential_field,
            'current_density': self._calculate_current_density(conductivity_field, potential_field),
            'device_resistance': self._calculate_device_resistance(conductivity_field)
        }
        
        return results
    
    def _solve_poisson_equation(self, conductivity_field):
        """求解泊松方程"""
        # 简化的泊松方程求解
        nx, ny = conductivity_field.shape
        potential = np.zeros((nx, ny))
        
        # 边界条件
        potential[0, :] = 1.0  # 顶部电极
        potential[-1, :] = 0.0  # 底部电极
        
        # 迭代求解
        for iteration in range(1000):
            potential_new = potential.copy()
            
            for i in range(1, nx-1):
                for j in range(1, ny-1):
                    potential_new[i, j] = 0.25 * (
                        potential[i-1, j] + potential[i+1, j] + 
                        potential[i, j-1] + potential[i, j+1]
                    )
            
            potential = potential_new
            
            if iteration % 100 == 0:
                residual = np.mean(np.abs(potential_new - potential))
                if residual < 1e-6:
                    break
        
        return potential
    
    def _calculate_current_density(self, conductivity_field, potential_field):
        """计算电流密度"""
        # J = -σ∇φ
        grad_x, grad_y = np.gradient(potential_field)
        current_x = -conductivity_field * grad_x
        current_y = -conductivity_field * grad_y
        
        return np.sqrt(current_x**2 + current_y**2)
    
    def _calculate_device_resistance(self, conductivity_field):
        """计算器件电阻"""
        # 简化计算
        avg_conductivity = np.mean(conductivity_field)
        thickness = 0.1  # cm
        area = self.device_size**2  # cm²
        
        resistance = thickness / (avg_conductivity * area)
        return resistance
    
    def thermal_modeling(self):
        """热力学建模"""
        print("执行热力学建模...")
        
        # 温度分布
        nx, ny = 20, 20
        temperature_field = np.ones((nx, ny)) * 300  # K
        
        # 添加热源
        heat_source = np.zeros((nx, ny))
        heat_source[nx//2, ny//2] = 1000  # W/m³
        
        # 热传导方程求解
        thermal_conductivity = 5.0  # W/(m·K)
        heat_capacity = 1000  # J/(kg·K)
        density = 5000  # kg/m³
        
        # 简化的热传导
        for step in range(100):
            temperature_field = self._solve_heat_equation(
                temperature_field, heat_source, thermal_conductivity, 
                heat_capacity, density
            )
        
        results = {
            'temperature_field': temperature_field,
            'max_temperature': np.max(temperature_field),
            'temperature_gradient': np.gradient(temperature_field),
            'thermal_stress': self._calculate_thermal_stress(temperature_field)
        }
        
        return results
    
    def _solve_heat_equation(self, T, Q, k, cp, rho):
        """求解热传导方程"""
        dt = 0.01  # s
        dx = 0.05  # m
        
        # 热扩散系数
        alpha = k / (rho * cp)
        
        # 有限差分
        T_new = T.copy()
        
        # 内部点
        for i in range(1, T.shape[0]-1):
            for j in range(1, T.shape[1]-1):
                d2T_dx2 = (T[i+1, j] - 2*T[i, j] + T[i-1, j]) / dx**2
                d2T_dy2 = (T[i, j+1] - 2*T[i, j] + T[i, j-1]) / dx**2
                
                T_new[i, j] = T[i, j] + dt * (alpha * (d2T_dx2 + d2T_dy2) + Q[i, j] / (rho * cp))
        
        return T_new
    
    def _calculate_thermal_stress(self, temperature_field):
        """计算热应力"""
        # 简化的热应力计算
        T_ref = 300  # K
        alpha_thermal = 1e-5  # 1/K
        elastic_modulus = 200e9  # Pa
        
        thermal_strain = alpha_thermal * (temperature_field - T_ref)
        thermal_stress = elastic_modulus * thermal_strain
        
        return thermal_stress

class MultiscaleSimulationPlatform:
    """多尺度仿真平台主类"""
    
    def __init__(self, structure):
        self.structure = structure
        self.atomic_sim = AtomicScaleSimulation(structure)
        self.simulation_results = {}
        
    def run_full_simulation(self):
        """运行完整的多尺度仿真"""
        print("=== 开始多尺度仿真 ===")
        
        # 1. 原子尺度仿真
        print("\n1. 原子尺度仿真")
        dft_results = self.atomic_sim.dft_calculation()
        neb_results = self.atomic_sim.neb_calculation()
        md_results = self.atomic_sim.md_simulation()
        
        self.simulation_results['atomic'] = {
            'dft': dft_results,
            'neb': neb_results,
            'md': md_results
        }
        
        # 2. 介观尺度仿真
        print("\n2. 介观尺度仿真")
        mesoscale_sim = MesoscaleSimulation(md_results)
        microstructure_results = mesoscale_sim.microstructure_modeling()
        phase_field_results = mesoscale_sim.phase_field_modeling()
        
        self.simulation_results['mesoscale'] = {
            'microstructure': microstructure_results,
            'phase_field': phase_field_results
        }
        
        # 3. 宏观尺度仿真
        print("\n3. 宏观尺度仿真")
        macroscale_sim = MacroscaleSimulation(microstructure_results)
        continuum_results = macroscale_sim.continuum_modeling()
        thermal_results = macroscale_sim.thermal_modeling()
        
        self.simulation_results['macroscale'] = {
            'continuum': continuum_results,
            'thermal': thermal_results
        }
        
        print("\n=== 多尺度仿真完成 ===")
        return self.simulation_results
    
    def visualize_results(self):
        """可视化仿真结果"""
        print("生成多尺度仿真可视化...")
        
        fig = plt.figure(figsize=(20, 15))
        
        # 1. 原子尺度 - NEB路径
        ax1 = plt.subplot(3, 4, 1)
        neb_data = self.simulation_results['atomic']['neb']
        ax1.plot(neb_data['reaction_coordinate'], neb_data['energy_profile'], 'b-o', linewidth=2)
        ax1.set_xlabel('反应坐标')
        ax1.set_ylabel('能量 (eV)')
        ax1.set_title('原子尺度：NEB迁移路径')
        ax1.grid(True, alpha=0.3)
        
        # 2. 原子尺度 - 3D迁移路径
        ax2 = plt.subplot(3, 4, 2, projection='3d')
        path = neb_data['migration_path']
        ax2.plot(path[:, 0], path[:, 1], path[:, 2], 'r-o', linewidth=2)
        ax2.set_xlabel('X (Å)')
        ax2.set_ylabel('Y (Å)')
        ax2.set_zlabel('Z (Å)')
        ax2.set_title('原子尺度：3D迁移路径')
        
        # 3. 原子尺度 - MSD
        ax3 = plt.subplot(3, 4, 3)
        md_data = self.simulation_results['atomic']['md']
        time_steps = np.arange(len(md_data['msd'])) * 0.001
        ax3.plot(time_steps, md_data['msd'], 'g-', linewidth=2)
        ax3.set_xlabel('时间 (ps)')
        ax3.set_ylabel('MSD (Å²)')
        ax3.set_title('原子尺度：均方位移')
        ax3.grid(True, alpha=0.3)
        
        # 4. 原子尺度 - 弹性常数
        ax4 = plt.subplot(3, 4, 4)
        elastic_constants = self.simulation_results['atomic']['dft']['elastic_constants']
        im1 = ax4.imshow(elastic_constants, cmap='viridis')
        ax4.set_title('原子尺度：弹性常数矩阵')
        plt.colorbar(im1, ax=ax4)
        
        # 5. 介观尺度 - 微结构
        ax5 = plt.subplot(3, 4, 5)
        microstructure = self.simulation_results['mesoscale']['microstructure']['microstructure']
        im2 = ax5.imshow(microstructure, cmap='tab10')
        ax5.set_title('介观尺度：微结构')
        ax5.set_xlabel('位置 (μm)')
        ax5.set_ylabel('位置 (μm)')
        
        # 6. 介观尺度 - 晶界
        ax6 = plt.subplot(3, 4, 6)
        grain_boundaries = self.simulation_results['mesoscale']['microstructure']['grain_boundary_map']
        im3 = ax6.imshow(grain_boundaries, cmap='binary')
        ax6.set_title('介观尺度：晶界分布')
        ax6.set_xlabel('位置 (μm)')
        ax6.set_ylabel('位置 (μm)')
        
        # 7. 介观尺度 - 相场
        ax7 = plt.subplot(3, 4, 7)
        phase_field = self.simulation_results['mesoscale']['phase_field']['final_phase_field']
        im4 = ax7.imshow(phase_field, cmap='RdBu')
        ax7.set_title('介观尺度：相场分布')
        ax7.set_xlabel('位置 (μm)')
        ax7.set_ylabel('位置 (μm)')
        plt.colorbar(im4, ax=ax7)
        
        # 8. 介观尺度 - 有效电导率
        ax8 = plt.subplot(3, 4, 8)
        scales = ['原子', '介观', '宏观']
        conductivities = [
            self.simulation_results['atomic']['md']['conductivity'],
            self.simulation_results['mesoscale']['microstructure']['effective_conductivity'],
            1e-4  # 示例值
        ]
        bars = ax8.bar(scales, np.log10(conductivities), color=['red', 'green', 'blue'], alpha=0.7)
        ax8.set_ylabel('log₁₀(电导率 S/cm)')
        ax8.set_title('多尺度电导率对比')
        
        # 9. 宏观尺度 - 电势分布
        ax9 = plt.subplot(3, 4, 9)
        potential_field = self.simulation_results['macroscale']['continuum']['potential_field']
        im5 = ax9.imshow(potential_field, cmap='plasma')
        ax9.set_title('宏观尺度：电势分布')
        ax9.set_xlabel('位置 (cm)')
        ax9.set_ylabel('位置 (cm)')
        plt.colorbar(im5, ax=ax9)
        
        # 10. 宏观尺度 - 电流密度
        ax10 = plt.subplot(3, 4, 10)
        current_density = self.simulation_results['macroscale']['continuum']['current_density']
        im6 = ax10.imshow(current_density, cmap='hot')
        ax10.set_title('宏观尺度：电流密度')
        ax10.set_xlabel('位置 (cm)')
        ax10.set_ylabel('位置 (cm)')
        plt.colorbar(im6, ax=ax10)
        
        # 11. 宏观尺度 - 温度场
        ax11 = plt.subplot(3, 4, 11)
        temperature_field = self.simulation_results['macroscale']['thermal']['temperature_field']
        im7 = ax11.imshow(temperature_field, cmap='coolwarm')
        ax11.set_title('宏观尺度：温度场')
        ax11.set_xlabel('位置 (cm)')
        ax11.set_ylabel('位置 (cm)')
        plt.colorbar(im7, ax=ax11)
        
        # 12. 尺度关联图
        ax12 = plt.subplot(3, 4, 12)
        scales_detail = ['原子\n(Å)', '介观\n(μm)', '宏观\n(cm)']
        length_scales = [1e-10, 1e-6, 1e-2]  # m
        time_scales = [1e-12, 1e-9, 1e-3]    # s
        
        ax12.loglog(length_scales, time_scales, 'bo-', linewidth=2, markersize=8)
        for i, scale in enumerate(scales_detail):
            ax12.annotate(scale, (length_scales[i], time_scales[i]), 
                         xytext=(10, 10), textcoords='offset points')
        
        ax12.set_xlabel('长度尺度 (m)')
        ax12.set_ylabel('时间尺度 (s)')
        ax12.set_title('多尺度关联图')
        ax12.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('multiscale_simulation_results.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def generate_report(self):
        """生成仿真报告"""
        print("生成多尺度仿真报告...")
        
        report = {
            'simulation_timestamp': datetime.now().isoformat(),
            'material_formula': self.structure.formula,
            'summary': {
                'atomic_scale': {
                    'activation_energy': self.simulation_results['atomic']['neb']['activation_energy'],
                    'diffusion_coefficient': self.simulation_results['atomic']['md']['diffusion_coefficient'],
                    'bulk_modulus': self.simulation_results['atomic']['dft']['bulk_modulus'],
                    'ionic_conductivity': self.simulation_results['atomic']['md']['conductivity']
                },
                'mesoscale': {
                    'average_grain_size': self.simulation_results['mesoscale']['microstructure']['average_grain_size'],
                    'grain_boundary_density': self.simulation_results['mesoscale']['microstructure']['grain_boundary_density'],
                    'effective_conductivity': self.simulation_results['mesoscale']['microstructure']['effective_conductivity'],
                    'phase_fraction': self.simulation_results['mesoscale']['phase_field']['phase_fraction']
                },
                'macroscale': {
                    'device_resistance': self.simulation_results['macroscale']['continuum']['device_resistance'],
                    'max_temperature': self.simulation_results['macroscale']['thermal']['max_temperature'],
                    'thermal_stress_max': np.max(self.simulation_results['macroscale']['thermal']['thermal_stress'])
                }
            },
            'performance_metrics': {
                'overall_conductivity': self.simulation_results['mesoscale']['microstructure']['effective_conductivity'],
                'thermal_stability': 'Good' if self.simulation_results['macroscale']['thermal']['max_temperature'] < 400 else 'Fair',
                'mechanical_stability': 'Good' if self.simulation_results['atomic']['dft']['bulk_modulus'] > 100 else 'Fair'
            },
            'recommendations': self._generate_recommendations()
        }
        
        # 保存报告
        with open('multiscale_simulation_report.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False, default=str)
        
        print("报告已保存至 multiscale_simulation_report.json")
        return report
    
    def _generate_recommendations(self):
        """生成优化建议"""
        recommendations = []
        
        # 基于仿真结果的建议
        conductivity = self.simulation_results['mesoscale']['microstructure']['effective_conductivity']
        if conductivity < 1e-4:
            recommendations.append("建议优化晶界导电性，减少晶界电阻")
        
        activation_energy = self.simulation_results['atomic']['neb']['activation_energy']
        if activation_energy > 0.3:
            recommendations.append("建议通过掺杂降低离子迁移激活能")
        
        max_temp = self.simulation_results['macroscale']['thermal']['max_temperature']
        if max_temp > 400:
            recommendations.append("建议改善散热设计，降低工作温度")
        
        bulk_modulus = self.simulation_results['atomic']['dft']['bulk_modulus']
        if bulk_modulus < 100:
            recommendations.append("建议增强机械强度，提高结构稳定性")
        
        return recommendations

def main():
    """主函数"""
    print("=== 多尺度仿真平台 ===")
    
    # 加载一个示例结构
    try:
        import glob
        cif_files = glob.glob('**/*.cif', recursive=True)
        if cif_files:
            structure = Structure.from_file(cif_files[0])
            print(f"加载材料: {structure.formula}")
            
            # 创建多尺度仿真平台
            platform = MultiscaleSimulationPlatform(structure)
            
            # 运行仿真
            results = platform.run_full_simulation()
            
            # 可视化结果
            platform.visualize_results()
            
            # 生成报告
            report = platform.generate_report()
            
            print("\n=== 仿真完成 ===")
            print(f"总体电导率: {report['summary']['mesoscale']['effective_conductivity']:.2e} S/cm")
            print(f"激活能: {report['summary']['atomic_scale']['activation_energy']:.3f} eV")
            print(f"器件电阻: {report['summary']['macroscale']['device_resistance']:.2f} Ω")
            
        else:
            print("未找到CIF文件")
            
    except Exception as e:
        print(f"仿真过程中出错: {e}")
        
        # 使用虚拟结构进行演示
        print("使用虚拟结构进行演示...")
        from pymatgen.core import Lattice, Structure
        
        # 创建简单的立方结构
        lattice = Lattice.cubic(4.0)
        structure = Structure(lattice, ['Li', 'O'], [[0, 0, 0], [0.5, 0.5, 0.5]])
        
        platform = MultiscaleSimulationPlatform(structure)
        results = platform.run_full_simulation()
        platform.visualize_results()
        platform.generate_report()

if __name__ == "__main__":
    main() 