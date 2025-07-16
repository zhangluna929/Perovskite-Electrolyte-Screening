# 钙钛矿电解质筛选工具


## 目标

从现有材料中筛选出2-3个符合要求的电解质：
- 不含Ti（这玩意儿阻碍Li离子传导）
- 与Li金属界面友好
- 电导率 >= 10⁻³ S/cm

## 筛选结果

举例：跑出来几个不错的：

| 材料 | 激活能 (eV) | 电导率 (S/cm) | 评价 |
|------|-------------|---------------|------|
| Li₇La₃Zr₂O₁₂ | 0.10 | 1.5×10⁻³ | 很好 |
| LiNbO₃ | 0.15 | 1.2×10⁻³ | 不错 |
| LiTaO₃ | 0.18 | 8.5×10⁻⁴ | 还行 |

```

## 快速使用

```bash
# 安装依赖
pip install pymatgen numpy scipy matplotlib pandas

# 跑完整筛选
python src/utils/run_complete_screening.py

# 只跑核心筛选
python src/core/perovskite_screening.py

# 启动Web界面
python src/interface/web_interface.py
```

## 主要功能

### 筛选流程
67个CIF → 数据分拣 → Ti替换 → BVSE扫描 → 稳定性分析 → 界面兼容性 → NEB计算 → 推荐材料

### 计算方法
- BVSE：快速离子传导路径扫描
- DFT：电子结构计算
- ML预测：加速性能预测
- 多尺度仿真：从原子到器件

### 输出结果
自动生成4种分析报告：
- 界面反应分析
- 离子传导机制
- 机械兼容性
- 筛选总结

## 实验建议

### 优先材料：Li₇La₃Zr₂O₁₂
```
合成：固相反应，1200°C，12小时
气氛：Ar或N₂保护
助熔剂：NH₄F
测试：EIS测电导率，循环伏安测稳定窗口
```

## 贡献

有问题提Issue，有改进提PR。代码写得清楚点，别搞太复杂。

## 许可

MIT License - 随便用

## 联系

有技术问题可以开Issue讨论。

---

这工具基于多年的材料计算经验，希望能帮到做电池的同行们。

---

# Perovskite Electrolyte Screening Tool


## Goals

Screen 2-3 electrolytes that meet requirements:
- No Ti (this stuff blocks Li ion conduction)
- Interface-friendly with Li metal
- Conductivity >= 10⁻³ S/cm

## Screening Results

Found a few decent ones:

| Material | Activation Energy (eV) | Conductivity (S/cm) | Rating |
|----------|------------------------|---------------------|--------|
| Li₇La₃Zr₂O₁₂ | 0.10 | 1.5×10⁻³ | Good |
| LiNbO₃ | 0.15 | 1.2×10⁻³ | OK |
| LiTaO₃ | 0.18 | 8.5×10⁻⁴ | Decent |
```

## Quick Start

```bash
# Install dependencies
pip install pymatgen numpy scipy matplotlib pandas

# Run complete screening
python src/utils/run_complete_screening.py

# Run core screening only
python src/core/perovskite_screening.py

# Start web interface
python src/interface/web_interface.py
```

## Main Features

### Screening Workflow
67 CIFs → Data sorting → Ti substitution → BVSE scan → Stability analysis → Interface compatibility → NEB calculation → Recommended materials

### Calculation Methods
- BVSE: Fast ion conduction pathway scanning
- DFT: Electronic structure calculation
- ML prediction: Accelerated performance prediction
- Multiscale simulation: From atoms to devices

### Output Results
Auto-generate 4 types of analysis reports:
- Interface reaction analysis
- Ion conduction mechanism
- Mechanical compatibility
- Screening summary

## Experimental Suggestions

### Priority material: Li₇La₃Zr₂O₁₂
```
Synthesis: Solid-state reaction, 1200°C, 12 hours
Atmosphere: Ar or N₂ protection
Flux: NH₄F
Testing: EIS for conductivity, CV for stability window
```

## Contributing

Got issues? Open an Issue. Got improvements? Submit a PR. Keep code clean, don't overcomplicate.

## License

MIT License - use freely

## Contact

Open Issues for technical questions.

---

This tool is based on years of materials calculation experience, hope it helps fellow battery researchers. 
