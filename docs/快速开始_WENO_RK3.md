# 快速开始：五阶WENO + 三阶RK3求解器

## 🚀 最快开始方式

### 1. 运行WENO+RK3模拟（有点火核）

```bash
cd shock_tube_solver
python run_weno_simulation.py --with_ignition
```

### 2. 运行WENO+RK3模拟（无点火核）

```bash
cd shock_tube_solver
python run_weno_simulation.py
```

### 3. 对比WENO+RK3和MUSCL+RK2

```bash
cd shock_tube_solver
python test_weno_vs_muscl.py
```

## 📊 查看结果

```bash
cd shock_tube_solver
python show_results.py      # 显示数值结果
python plot_xt.py           # 绘制x-t图
```

## 🔧 在代码中使用

### 使用WENO+RK3

```python
from advanced_solver_weno import AdvancedSolverWithWENO

solver = AdvancedSolverWithWENO(
    nx=2000,
    L=100.0,
    use_weno=True,          # 启用WENO+RK3
    with_ignition=True      # 启用点火核
)

# 运行模拟
while solver.time < 0.025:
    dt = solver.compute_timestep()
    dt = min(dt, 0.025 - solver.time)
    solver.solve_step_with_threshold(dt)
```

### 使用MUSCL+RK2（原有方案）

```python
from advanced_solver_weno import AdvancedSolverWithWENO

solver = AdvancedSolverWithWENO(
    nx=2000,
    L=100.0,
    use_weno=False,         # 使用MUSCL+RK2
    with_ignition=True
)
```

## 📈 性能对比

| 方案 | 精度 | 速度 | 分辨率 |
|------|------|------|--------|
| MUSCL+RK2 | 二阶 | 快 | 中等 |
| **WENO+RK3** | **五阶** | **中等** | **高** |

## 📚 详细文档

- `WENO_RK3_说明.md` - 详细使用说明
- `shock_tube_solver/WENO_RK3_说明.md` - 算法详解
- `WENO_RK3_实现总结.md` - 实现细节

## ✅ 验证

运行后会自动验证：
- ✓ 右腔无燃烧
- ✓ 氧气浓度正常
- ✓ 数值稳定性

## 🎯 推荐用法

**对于精度要求高的应用**：
```bash
python run_weno_simulation.py --with_ignition
```

**对于快速测试**：
```bash
# 使用原有的MUSCL+RK2
python run_clean_simulation.py --with_ignition
```

**对于性能对比**：
```bash
python test_weno_vs_muscl.py
```

## 💡 提示

1. WENO+RK3计算时间约为MUSCL+RK2的1.5-2.0倍
2. 精度提升明显，特别是在激波附近
3. 两种方案都支持点火核和右腔保护
4. 可根据需求灵活选择

## 🔗 相关文件

```
shock_tube_solver/
├── weno_rk3_solver.py          # WENO+RK3核心实现
├── advanced_solver_weno.py     # 扩展求解器
├── run_weno_simulation.py      # 运行脚本
├── test_weno_vs_muscl.py       # 对比测试
└── WENO_RK3_说明.md            # 详细说明
```

