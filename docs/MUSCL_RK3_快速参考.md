# MUSCL+RK3 求解器 - 快速参考卡片

## 核心信息

| 项目 | MUSCL+RK2 | MUSCL+RK3 |
|------|-----------|----------|
| 时间精度 | 二阶 | **三阶** |
| 空间精度 | 二阶 | 二阶 |
| 计算速度 | 快 | 0.71x |
| 推荐场景 | 快速原型 | 高精度 |

## 快速启动

### Python代码
```python
from advanced_solver_weno import AdvancedSolverWithWENO

# RK3（高精度）
solver = AdvancedSolverWithWENO(use_weno=True, with_ignition=True)

# RK2（快速）
solver = AdvancedSolverWithWENO(use_weno=False, with_ignition=True)

# 运行模拟
while solver.time < t_final:
    solver.solve_step_with_threshold()
```

### 命令行
```bash
# RK3
cd shock_tube_solver
python run_weno_simulation.py --with_ignition

# RK2
python run_clean_simulation.py --with_ignition
```

## 性能指标

**测试条件**：500网格，50步

| 指标 | RK2 | RK3 |
|------|-----|-----|
| 时间 | 1.46s | 2.06s |
| 步数/秒 | 34.2 | 24.3 |
| 相对速度 | 1.0x | 0.71x |

## 验证结果

✅ 所有测试通过
✅ 右腔保护正常
✅ 无数值振荡
✅ 物理一致

## 文档

- `MUSCL_RK3_实现总结.md` - 实现细节
- `MUSCL_RK3_测试报告.md` - 测试报告
- `快速开始_MUSCL_RK3.md` - 详细指南
- `README.md` - 项目说明

## 何时使用

**选择RK2**：快速迭代、参数敏感性
**选择RK3**：最终结果、高精度需求

## 关键参数

```python
# 网格数
nx = 2000

# 计算域长度
L = 100.0

# 启用RK3
use_weno = True

# 启用点火核
with_ignition = True
```

## 常见问题

**Q: 结果会改变吗？**
A: 不会显著改变，只是精度更高

**Q: 应该选哪个？**
A: 不确定就选RK2快速测试，再用RK3精细计算

**Q: 计算时间增加多少？**
A: 约增加40%

## 下一步

1. 运行对比测试：`test_muscl_rk2_vs_rk3.py`
2. 查看详细文档
3. 根据需求选择求解器

---

**状态**：✅ 已完成并验证
**版本**：1.0
**日期**：2025-11-13

