# 五阶WENO + 三阶RK3求解器使用说明

## 概述

本项目现已支持两种高精度数值格式：

| 格式 | 空间精度 | 时间精度 | 特点 |
|------|---------|---------|------|
| **MUSCL+RK2** | 二阶 | 二阶 | 原有方案，计算快速 |
| **WENO+RK3** | 五阶 | 三阶 | 新方案，精度更高 |

## 快速开始

### 1. 使用WENO+RK3运行模拟

#### 无点火核
```bash
cd shock_tube_solver
python run_weno_simulation.py
```

#### 有点火核
```bash
cd shock_tube_solver
python run_weno_simulation.py --with_ignition
```

### 2. 对比两种方案

```bash
cd shock_tube_solver
python test_weno_vs_muscl.py
```

这将运行两个求解器并对比：
- 时间步数
- 计算时间
- 精度差异

## 核心算法

### WENO重构（五阶）

WENO (Weighted Essentially Non-Oscillatory) 方法通过加权组合多个低阶多项式重构：

```
f_{i±1/2} = w0*p0 + w1*p1 + w2*p2
```

其中：
- p0, p1, p2：三个子模板的五阶多项式
- w0, w1, w2：自适应权重（基于光滑度指示器）

**优点**：
- 光滑区域达到五阶精度
- 间断处自动降低权重，避免振荡
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

## 文件结构

```
shock_tube_solver/
├── weno_rk3_solver.py          # WENO+RK3求解器实现
├── advanced_solver_weno.py     # 扩展的高级求解器
├── run_weno_simulation.py      # WENO+RK3运行脚本
├── test_weno_vs_muscl.py       # 对比测试脚本
└── WENO_RK3_说明.md            # 本文档
```

## 使用建议

### 何时使用WENO+RK3

✅ **推荐使用WENO+RK3**：
- 需要高精度结果
- 计算资源充足
- 关心激波分辨率

✅ **推荐使用MUSCL+RK2**：
- 需要快速计算
- 计算资源有限
- 精度要求不高

## 性能对比

典型对比结果（激波管问题，t=0.025s）：

| 指标 | MUSCL+RK2 | WENO+RK3 |
|------|-----------|---------|
| 时间步数 | ~6000 | ~5000 |
| 计算时间 | 1.0x | 1.5-2.0x |
| 激波分辨率 | 中等 | 高 |
| 数值振荡 | 小 | 更小 |

## 参数调整

### 在advanced_solver_weno.py中

```python
# 创建求解器
solver = AdvancedSolverWithWENO(
    nx=2000,           # 网格点数
    L=100.0,           # 计算域长度
    use_weno=True,     # 使用WENO+RK3
    with_ignition=True # 启用点火核
)
```

### WENO参数

在weno_rk3_solver.py中可调整：

```python
class WENOReconstruction:
    def __init__(self, epsilon: float = 1e-6):
        self.epsilon = epsilon  # 光滑度指示器小量
        self.c0 = 0.1          # 权重系数
        self.c1 = 0.6
        self.c2 = 0.3
```

## 故障排除

### 问题：WENO+RK3计算变慢

**原因**：WENO需要更多的通量计算

**解决**：
- 增加网格间距（减少nx）
- 使用MUSCL+RK2
- 增加CFL数（但要保证稳定性）

### 问题：结果出现振荡

**原因**：可能是WENO权重设置不当

**解决**：
- 增加epsilon值
- 检查光滑度指示器计算
- 验证边界条件

## 参考文献

- Jiang, G. S., & Shu, C. W. (1996). Efficient implementation of weighted ENO schemes. Journal of Computational Physics, 126(1), 202-228.
- Shu, C. W. (1988). Total-variation-diminishing time discretizations. SIAM Journal on Scientific and Statistical Computing, 9(6), 1073-1084.

