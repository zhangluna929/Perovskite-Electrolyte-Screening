# 贡献指南

欢迎帮忙改进这个钙钛矿筛选工具。

## 怎么贡献

**报Bug**
- 开Issue说清楚问题
- 贴上错误信息和复现步骤  
- 说明系统环境

**提建议**
- Issue里提功能需求
- 说明用途和实现思路

**改代码**
1. Fork项目
2. 建分支 `git checkout -b feature/something-useful`
3. 写代码 `git commit -m 'Add useful feature'`
4. 推送 `git push origin feature/something-useful`
5. 提PR

## 代码规范

**Python风格**
- 跟PEP 8标准
- 变量名要有意义
- 该写注释的地方写注释
- 一行别超过100字符

**文件组织**
```
src/
├── core/       # 核心算法
├── ml/         # 机器学习
├── simulation/ # 仿真计算  
├── interface/  # 界面
└── utils/      # 工具
```

**提交信息**
```
类型: 简短说明

详细说明（如果需要）
- 修了什么问题
- 加了什么功能

相关Issue: #123
```

## 测试要求

**单元测试**
- 新功能要有测试
- 覆盖率80%以上
- 用pytest框架

**集成测试**  
- 确保与现有代码兼容
- 验证筛选流程完整
- 测试输入输出正确

## 文档要求

- 函数加docstring
- 复杂算法写注释
- 新功能更新README

## PR检查

提交前确认：
- [ ] 测试通过
- [ ] 代码规范
- [ ] 文档更新
- [ ] 回应代码审查

## 开发环境

```bash
git clone https://github.com/yourusername/perovskite-screening.git
cd perovskite-screening
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install pymatgen numpy scipy matplotlib pandas
```

## 优先改进方向

特别欢迎这些方面的贡献：

**算法优化**
- 更好的材料预测模型
- 提高计算效率
- 减少内存使用

**界面改进**
- Web界面优化
- 更好的数据可视化

**数据扩展**  
- 支持更多材料类型
- 集成更多数据源

## 联系

- 项目问题开Issue
- 技术讨论用Discussions

写代码别搞太复杂，简单实用就行。

---

# Contributing Guide

Welcome to help improve this perovskite screening tool.

## How to Contribute

**Report Bugs**
- Open Issue with clear problem description
- Include error messages and reproduction steps
- Mention system environment

**Suggest Features**
- Submit feature requests in Issues
- Explain use case and implementation ideas

**Code Changes**
1. Fork the project
2. Create branch `git checkout -b feature/something-useful`
3. Write code `git commit -m 'Add useful feature'`
4. Push `git push origin feature/something-useful`
5. Submit PR

## Code Standards

**Python Style**
- Follow PEP 8 standards
- Use meaningful variable names
- Add comments where needed
- Keep lines under 100 characters

**File Organization**
```
src/
├── core/       # Core algorithms
├── ml/         # Machine learning
├── simulation/ # Simulation calculations
├── interface/  # User interface
└── utils/      # Utilities
```

**Commit Messages**
```
type: brief description

Detailed explanation (if needed)
- Fixed what problem
- Added what feature

Related Issue: #123
```

## Testing Requirements

**Unit Tests**
- New features need tests
- Coverage >80%
- Use pytest framework

**Integration Tests**
- Ensure compatibility with existing code
- Verify complete screening workflow
- Test input/output correctness

## Documentation Requirements

- Add docstrings to functions
- Comment complex algorithms
- Update README for new features

## PR Checklist

Before submitting:
- [ ] Tests pass
- [ ] Code follows standards
- [ ] Documentation updated
- [ ] Address code review feedback

## Development Environment

```bash
git clone https://github.com/yourusername/perovskite-screening.git
cd perovskite-screening
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install pymatgen numpy scipy matplotlib pandas
```

## Priority Areas

Especially welcome contributions in:

**Algorithm Optimization**
- Better material prediction models
- Improve computational efficiency
- Reduce memory usage

**Interface Improvements**
- Web interface optimization
- Better data visualization

**Data Expansion**
- Support more material types
- Integrate more data sources

## Contact

- Project issues: open Issues
- Technical discussions: use Discussions

Keep code simple and practical, don't overcomplicate. 