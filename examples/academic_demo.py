#!/usr/bin/env python3
"""academic_demo.py

简单演示如何使用钙钛矿电解质理论筛选平台的核心功能：
1. BVSE理论计算
2. 机器学习性能预测
3. 多尺度仿真验证（可选）

作者：LunaZhang
"""

from pathlib import Path
import json
from src.core.bvse_calculator import BVSECalculator
from src.ml.ml_enhanced_screening import MLEnhancedScreening

# CIF路径（示例）
CIF_PATH = Path('data/raw_materials/Li7La3Zr2O12_mp-942733_computed.cif')

if not CIF_PATH.exists():
    raise FileNotFoundError(f'找不到示例CIF文件: {CIF_PATH}')

print('='*60)
print('步骤 1: BVSE理论计算')
print('='*60)
calc = BVSECalculator()
result_bvse = calc.run_bvse_analysis(str(CIF_PATH))
print(json.dumps(result_bvse, indent=2, ensure_ascii=False))

print('\n' + '='*60)
print('步骤 2: 机器学习性能预测')
print('='*60)
ml_screen = MLEnhancedScreening()

# 从化学式解析组成
composition = ml_screen._parse_formula(result_bvse['formula'])
# 加载预训练模型，如果没有则提示用户先训练
if not ml_screen.load_models():
    print('⚠ 未找到预训练模型，请先运行 ml_enhanced_screening.py --train')
else:
    predictions = ml_screen.predict_properties(composition)
    print(json.dumps(predictions, indent=2, ensure_ascii=False))

print('\n演示结束。如果需要多尺度仿真，请运行 simulation/multiscale_simulation_platform.py') 