# 数据目录说明

## 目录结构

```
data/
├── raw_materials/          # 原始67个CIF文件
│   ├── examples/          # 示例文件（3-5个CIF）
│   ├── 01Li-La-Ti–O₃ 主族， NbZrAlGa 衍生物/
│   ├── 02经典钙钛矿锂氧族 (TaNb 系)/
│   └── 03SrBaCa 基 Ti-O 钙钛矿/
└── external_materials/     # 外部参考材料
    ├── examples/          # 参考示例
    └── downloaded_materials/  # 从Materials Project下载的材料
```

## 数据说明

### 原始材料 (raw_materials/)
包含67个钙钛矿结构的CIF文件，按化学组成分为三类：
- **Li-La-Ti-O系**: 锂镧钛氧化物及其衍生物
- **TaNb系**: 钽铌氧化物钙钛矿
- **SrBaCa-Ti-O系**: 碱土金属钛氧化物

### 外部材料 (external_materials/)
从Materials Project数据库下载的参考材料：
- **LaAlO3_LaGaO3/**: 镧铝/镓氧化物
- **Other_ABO3/**: 其他ABO3型钙钛矿
- **Sr_Ba_Ca_Ti_O/**: 碱土金属钛氧化物

## 完整数据获取

由于文件大小限制，仓库中只包含少量示例文件。要获取完整的67个CIF文件：

1. **联系作者获取**：通过GitHub Issues联系LunaZhang
2. **Materials Project下载**：使用项目中的材料ID从MP数据库下载
3. **文献来源**：参考相关论文获取结构文件

## 数据格式

所有CIF文件包含：
- 晶体结构信息
- 空间群对称性
- 原子坐标
- 晶格参数

## 使用说明

1. 将完整数据放入对应目录
2. 运行筛选程序会自动识别和处理所有CIF文件
3. 程序会生成JSON格式的处理结果

## 注意事项

- CIF文件名中包含化学式和Materials Project ID
- 确保文件编码为UTF-8
- 某些文件名包含特殊字符，注意系统兼容性 