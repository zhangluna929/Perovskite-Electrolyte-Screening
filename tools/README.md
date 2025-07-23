# 工具脚本目录

本目录包含各种实用工具脚本。

## 文件说明

- **generate_certificates.py** - 生成材料认证证书
  - 生成详细的材料分析报告
  - 包含性能图表和分析结果
  - 支持多种输出格式

- **simple_certificates.py** - 生成简化版证书
  - 快速生成基础证书
  - 适用于批量处理
  - 轻量级输出

## 使用方法

```bash
# 生成详细证书
python tools/generate_certificates.py

# 生成简化证书  
python tools/simple_certificates.py
```

## 依赖要求

- matplotlib
- numpy
- pandas
- PIL (Pillow) 