# 快速开始

一个筛选钙钛矿电解质的工具，从67个CIF文件里找出好材料。

## 30秒上手

```bash
git clone https://github.com/yourusername/perovskite-screening.git
cd perovskite-screening
pip install pymatgen numpy scipy matplotlib pandas
python src/utils/run_complete_screening.py
```

## 主要命令

```bash
# 完整筛选流程
python src/utils/run_complete_screening.py

# 只跑核心筛选
python src/core/perovskite_screening.py

# 机器学习预测
python src/ml/ml_accelerated_screening.py

# 多尺度仿真
python src/simulation/multiscale_simulation_platform.py

# Web界面 (http://localhost:8501)
python src/interface/web_interface.py
```

## 重要文件

- `src/core/perovskite_screening.py` - 主程序
- `src/utils/run_complete_screening.py` - 一键运行
- `results/json_data/` - 计算结果
- `results/visualizations/` - 分析图表
- `data/raw_materials/` - 原始数据

## 查看结果

```bash
# 图表在这里
ls results/visualizations/

# 数据在这里  
cat results/json_data/bvse_results.json
```

## 常见问题

**缺依赖包？**
```bash
pip install pymatgen numpy scipy matplotlib pandas
```

**找不到CIF文件？**
确保 `data/raw_materials/` 里有67个CIF文件

**程序报错？**
检查Python版本，需要3.8以上

## 推荐材料

算出来几个还不错的：

- Li₇La₃Zr₂O₁₂ - 电导率最高
- LiNbO₃ - 比较稳定  
- LiTaO₃ - 凑合用

## 需要帮助？

- 看 README.md 详细说明
- 有Bug提Issue
- 想讨论开Discussions

用起来有问题随时问。 