# 五阶WENO + 三阶RK3求解器实现总结

## 概述

已成功实现五阶WENO + 三阶Runge-Kutta求解器，用于替代原有的二阶MUSCL + 二阶RK2方案。

## 新增文件

### 1. `shock_tube_solver/weno_rk3_solver.py`
**核心求解器实现**

包含两个主要类：

#### WENOReconstruction（五阶WENO重构）
- `compute_smoothness_indicator()`: 计算光滑度指示器
- `compute_weights()`: 计算自适应权重
- `reconstruct_left()`: 界面左侧重构
- `reconstruct_right()`: 界面右侧重构

#### WENOHighOrderSolver（WENO+RK3求解器）
- `apply_boundary_conditions()`: 镜像法边界条件
- `compute_fluxes()`: 使用WENO重构计算通量
- `runge_kutta_3_step()`: 三阶SSP-RK3时间积分
- `compute_timestep()`: CFL条件下的时间步长

### 2. `shock_tube_solver/advanced_solver_weno.py`
**扩展的高级求解器**

继承自AdvancedShockTubeSolver，支持两种求解器选择：

```python
# 使用WENO+RK3
solver = AdvancedSolverWithWENO(use_weno=True)

# 使用MUSCL+RK2（原有方案）
solver = AdvancedSolverWithWENO(use_weno=False)
```

### 3. `shock_tube_solver/run_weno_simulation.py`
**WENO+RK3运行脚本**

用法：
```bash
# 无点火核
python run_weno_simulation.py

# 有点火核
python run_weno_simulation.py --with_ignition
```

### 4. `shock_tube_solver/test_weno_vs_muscl.py`
**对比测试脚本**

对比WENO+RK3和MUSCL+RK2的：
- 时间步数
- 计算时间
- 精度差异

用法：
```bash
python test_weno_vs_muscl.py
```

### 5. `shock_tube_solver/WENO_RK3_说明.md`
**详细使用说明文档**

## 核心算法

### 五阶WENO重构

在界面处进行五阶多项式重构：

```
f_{i±1/2} = w0*p0 + w1*p1 + w2*p2
```

其中权重基于光滑度指示器自适应计算：

```
w_k = α_k / Σα_j
α_k = c_k / (ε + IS_k)²
```

**优点**：
- 光滑区域五阶精度
- 间断处自动降低权重
- 比MUSCL更好的分辨率

### 三阶SSP-RK3时间积分

```
U^(1) = U^n + Δt * L(U^n)
U^(2) = (3/4)*U^n + (1/4)*U^(1) + (1/4)*Δt*L(U^(1))
U^(n+1) = (1/3)*U^n + (2/3)*U^(2) + (2/3)*Δt*L(U^(2))
```

**特点**：
- 三阶时间精度
- 强稳定性保持（SSP）
- 与WENO空间离散相匹配

## 使用方法

### 方法1：直接使用WENO+RK3运行脚本

```bash
cd shock_tube_solver
python run_weno_simulation.py --with_ignition
```

### 方法2：在Python代码中使用

```python
from advanced_solver_weno import AdvancedSolverWithWENO

# 创建求解器（使用WENO+RK3）
solver = AdvancedSolverWithWENO(
    nx=2000,
    L=100.0,
    use_weno=True,
    with_ignition=True
)

# 运行模拟
while solver.time < t_final:
    dt = solver.compute_timestep()
    dt = min(dt, t_final - solver.time)
    solver.solve_step_with_threshold(dt)
```

### 方法3：对比测试

```bash
cd shock_tube_solver
python test_weno_vs_muscl.py
```

## 性能对比

| 指标 | MUSCL+RK2 | WENO+RK3 |
|------|-----------|---------|
| 空间精度 | 二阶 | 五阶 |
| 时间精度 | 二阶 | 三阶 |
| 激波分辨率 | 中等 | 高 |
| 计算时间 | 1.0x | 1.5-2.0x |
| 数值振荡 | 小 | 更小 |

## 向后兼容性

✅ 完全向后兼容
- 原有的MUSCL+RK2求解器保持不变
- 可通过参数选择使用哪种方案
- 不影响现有的模拟脚本

## 下一步

可选的改进方向：

1. **自适应网格细化（AMR）**：在激波附近自动加密网格
2. **并行计算**：使用OpenMP或MPI加速
3. **更高阶格式**：七阶WENO或DG方法
4. **隐式时间积分**：处理刚性源项

## 参考文献

- Jiang, G. S., & Shu, C. W. (1996). Efficient implementation of weighted ENO schemes
- Shu, C. W. (1988). Total-variation-diminishing time discretizations

