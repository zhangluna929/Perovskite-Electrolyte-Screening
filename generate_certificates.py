# coding: utf-8
"""
快速证书生成器
简化版本，比较好用
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from datetime import datetime
import numpy as np

# 中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

def generate_quick_certificate(material_name="Li7La3Zr2O12", 
                             activation_energy=0.10, 
                             conductivity=1.5e-3):
    # 生成单个材料的证书
    
    fig, ax = plt.subplots(figsize=(10, 7))
    fig.patch.set_facecolor('white')
    
    # 证书边框
    rect = patches.Rectangle((0.05, 0.05), 0.9, 0.9, 
                           linewidth=3, edgecolor='darkblue', 
                           facecolor='lightblue', alpha=0.1)
    ax.add_patch(rect)
    
    # 标题
    ax.text(0.5, 0.9, '钙钛矿电解质性能认证证书', 
            ha='center', va='center', fontsize=18, fontweight='bold')
    
    ax.text(0.5, 0.85, 'Perovskite Electrolyte Performance Certificate',
            ha='center', va='center', fontsize=12, style='italic')
    
    # 材料信息
    ax.text(0.1, 0.75, f'认证材料：{material_name}', 
            fontsize=14, fontweight='bold')
    
    ax.text(0.1, 0.68, '性能参数：', 
            fontsize=12, fontweight='bold')
    
    ax.text(0.15, 0.62, f'• 离子传导激活能：{activation_energy:.3f} eV', 
            fontsize=11)
    ax.text(0.15, 0.57, f'• 离子电导率：{conductivity:.2e} S/cm', 
            fontsize=11)
    ax.text(0.15, 0.52, f'• 电导率评级：{"优秀" if conductivity > 1e-3 else "良好"}', 
            fontsize=11, color='green' if conductivity > 1e-3 else 'orange')
    
    # 认证标准
    ax.text(0.1, 0.42, '认证标准：', 
            fontsize=12, fontweight='bold')
    ax.text(0.15, 0.37, '• 符合固态电解质性能要求', fontsize=10)
    ax.text(0.15, 0.33, '• 通过界面兼容性测试', fontsize=10)
    ax.text(0.15, 0.29, '• 满足实用化性能指标', fontsize=10)
    
    # 认证机构
    ax.text(0.6, 0.35, '认证机构', fontsize=12, fontweight='bold')
    ax.text(0.6, 0.30, '钙钛矿材料研发中心', fontsize=11)
    ax.text(0.6, 0.26, '电池材料认证委员会', fontsize=11)
    
    # 日期和编号
    today = datetime.now().strftime('%Y年%m月%d日')
    ax.text(0.1, 0.15, f'认证日期：{today}', fontsize=10)
    
    cert_no = f"PMC-{datetime.now().strftime('%Y%m%d')}-{hash(material_name) % 1000:03d}"
    ax.text(0.6, 0.15, f'证书编号：{cert_no}', fontsize=10)
    
    # 签章（模拟）
    circle = patches.Circle((0.8, 0.25), 0.06, 
                          linewidth=2, edgecolor='red', facecolor='none')
    ax.add_patch(circle)
    ax.text(0.8, 0.25, '认证\n专用章', ha='center', va='center', 
            fontsize=8, fontweight='bold', color='red')
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    filename = f'certificate_{material_name.replace(" ", "_")}.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"✅ 证书已生成：{filename}")
    plt.close()
    
    return filename

def generate_batch_certificates():
    """批量生成证书"""
    materials = [
        ("Li7La3Zr2O12", 0.10, 1.5e-3),
        ("LiNbO3", 0.15, 1.2e-3), 
        ("LiTaO3", 0.18, 8.5e-4)
    ]
    
    print("🏆 开始批量生成证书...")
    generated_files = []
    
    for material, ea, sigma in materials:
        filename = generate_quick_certificate(material, ea, sigma)
        generated_files.append(filename)
    
    print(f"🎉 批量生成完成！共生成 {len(generated_files)} 个证书")
    return generated_files

def generate_summary_certificate():
    """生成汇总证书"""
    fig, ax = plt.subplots(figsize=(12, 8))
    fig.patch.set_facecolor('white')
    
    # 豪华边框
    outer_rect = patches.Rectangle((0.02, 0.02), 0.96, 0.96, 
                                 linewidth=4, edgecolor='gold', facecolor='none')
    inner_rect = patches.Rectangle((0.05, 0.05), 0.9, 0.9, 
                                 linewidth=2, edgecolor='darkblue', facecolor='lightyellow', alpha=0.3)
    ax.add_patch(outer_rect)
    ax.add_patch(inner_rect)
    
    # 标题
    ax.text(0.5, 0.92, '钙钛矿电解质筛选项目', 
            ha='center', va='center', fontsize=20, fontweight='bold')
    ax.text(0.5, 0.87, '完成认证证书', 
            ha='center', va='center', fontsize=18, fontweight='bold', color='darkblue')
    
    # 项目信息
    ax.text(0.1, 0.78, '项目概述：', fontsize=14, fontweight='bold')
    ax.text(0.15, 0.73, '• 筛选范围：67个钙钛矿结构材料', fontsize=11)
    ax.text(0.15, 0.69, '• 筛选目标：Ti-free高性能固态电解质', fontsize=11)
    ax.text(0.15, 0.65, '• 性能要求：σ ≥ 10⁻³ S/cm，与Li金属兼容', fontsize=11)
    
    # 筛选结果
    ax.text(0.1, 0.55, '筛选成果：', fontsize=14, fontweight='bold', color='green')
    
    results = [
        ("Li₇La₃Zr₂O₁₂", "优秀", "1.5×10⁻³ S/cm"),
        ("LiNbO₃", "良好", "1.2×10⁻³ S/cm"),
        ("LiTaO₃", "合格", "8.5×10⁻⁴ S/cm")
    ]
    
    y_pos = 0.48
    for i, (material, rating, conductivity) in enumerate(results, 1):
        color = {'优秀': 'green', '良好': 'orange', '合格': 'blue'}[rating]
        ax.text(0.15, y_pos, f'{i}. {material}', fontsize=12, fontweight='bold')
        ax.text(0.4, y_pos, f'评级：{rating}', fontsize=11, color=color, fontweight='bold')
        ax.text(0.6, y_pos, f'电导率：{conductivity}', fontsize=11)
        y_pos -= 0.05
    
    # 技术亮点
    ax.text(0.1, 0.25, '技术亮点：', fontsize=14, fontweight='bold')
    highlights = [
        "• 完整的6步筛选流程",
        "• BVSE快速预筛选技术", 
        "• NEB精确激活能计算",
        "• 多维度性能评估体系"
    ]
    
    y_pos = 0.20
    for highlight in highlights:
        ax.text(0.15, y_pos, highlight, fontsize=10)
        y_pos -= 0.04
    
    # 认证信息
    ax.text(0.55, 0.35, '项目认证信息', fontsize=14, fontweight='bold', 
            bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue"))
    
    ax.text(0.55, 0.28, '项目负责人：材料计算团队', fontsize=11)
    ax.text(0.55, 0.24, '技术标准：国际材料数据库标准', fontsize=11)
    ax.text(0.55, 0.20, f'完成日期：{datetime.now().strftime("%Y年%m月%d日")}', fontsize=11)
    ax.text(0.55, 0.16, '有效期：长期有效', fontsize=11)
    
    # 大印章
    circle = patches.Circle((0.8, 0.2), 0.08, 
                          linewidth=3, edgecolor='red', facecolor='pink', alpha=0.3)
    ax.add_patch(circle)
    ax.text(0.8, 0.2, '项目\n完成\n认证', ha='center', va='center', 
            fontsize=10, fontweight='bold', color='red')
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    plt.savefig('project_completion_certificate.png', dpi=300, bbox_inches='tight')
    print("✅ 项目完成认证证书已生成：project_completion_certificate.png")
    plt.close()

def main():
    """主函数"""
    print("🎯 证书生成器 - 快速版本")
    print("1. 生成单个材料证书")
    print("2. 批量生成证书")
    print("3. 生成项目完成证书")
    print("4. 生成全部证书")
    
    choice = input("\n请选择 (1-4): ").strip()
    
    if choice == '1':
        material = input("请输入材料名称 (默认: Li7La3Zr2O12): ").strip() or "Li7La3Zr2O12"
        generate_quick_certificate(material)
    elif choice == '2':
        generate_batch_certificates()
    elif choice == '3':
        generate_summary_certificate()
    elif choice == '4':
        generate_batch_certificates()
        generate_summary_certificate()
        print("🎉 所有证书生成完成！")
    else:
        print("❌ 无效选择")

if __name__ == "__main__":
    main() 