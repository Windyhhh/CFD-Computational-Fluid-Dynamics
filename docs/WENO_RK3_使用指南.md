# WENO+RK3求解器 - 使用指南

## 概述

现在支持**三种求解器方案**：
1. **MUSCL+RK2** - 二阶空间，二阶时间（快速）
2. **MUSCL+RK3** - 二阶空间，三阶时间（平衡）
3. **WENO+RK3** - 五阶空间，三阶时间（高精度）✨

## 快速开始

### 1. 使用WENO+RK3

```python
from advanced_solver_weno import AdvancedSolverWithWENO

# 创建WENO+RK3求解器
solver = AdvancedSolverWithWENO(
    nx=2000,              # 网格数
    L=100.0,              # 计算域长度
    use_weno=True,        # 启用WENO
    use_rk3=True,         # 启用RK3（WENO自动使用RK3）
    with_ignition=True    # 启用点火核
)

# 运行模拟
while solver.time < t_final:
    solver.solve_step_with_threshold()
```

### 2. 使用MUSCL+RK3

```python
solver = AdvancedSolverWithWENO(
    nx=2000,
    L=100.0,
    use_weno=False,       # 使用MUSCL
    use_rk3=True,         # 启用RK3
    with_ignition=True
)
```

### 3. 使用MUSCL+RK2（默认）

```python
solver = AdvancedSolverWithWENO(
    nx=2000,
    L=100.0,
    use_weno=False,       # 使用MUSCL
    use_rk3=False,        # 使用RK2
    with_ignition=True
)
```

## 参数说明

### 主要参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `nx` | int | 2000 | 网格单元数 |
| `L` | float | 100.0 | 计算域长度（m） |
| `use_weno` | bool | False | 是否使用WENO（True）或MUSCL（False） |
| `use_rk3` | bool | False | 是否使用RK3（True）或RK2（False） |
| `with_ignition` | bool | False | 是否启用点火核 |

### 膜片位置和右腔保护

这些参数在求解器内部自动处理：

```python
# 膜片位置（自动设置）
solver.x_interface = 50.0  # m

# 右腔保护（自动启用）
solver.enforce_no_fuel_right = True
```

## 求解器对比

| 特性 | MUSCL+RK2 | MUSCL+RK3 | WENO+RK3 |
|------|-----------|----------|---------|
| 空间精度 | 二阶 | 二阶 | **五阶** |
| 时间精度 | 二阶 | 三阶 | 三阶 |
| 激波分辨率 | 中等 | 中等 | **高** |
| 计算速度 | 快 | 中等 | 慢 |
| 推荐场景 | 快速原型 | 平衡 | 高精度 |

## 内部参数传递

### 膜片位置（x_interface）

膜片位置在`advanced_solver.py`中初始化：
```python
self.x_interface = 50.0  # 膜片位置（m）
```

在求解器中自动传递：
```python
# WENO求解器
F = self.high_order_solver.compute_fluxes(
    self.U, gamma, 
    x_interface=self.x_interface,           # 膜片位置
    enforce_right_chamber=self.enforce_no_fuel_right
)

# MUSCL求解器
F = self.high_order_solver.compute_fluxes(
    self.U, gamma, 
    self.x_interface,                       # 膜片位置
    self.enforce_no_fuel_right
)
```

### 右腔保护机制

在`advanced_solver.py`中启用：
```python
self.enforce_no_fuel_right = True  # 强制右腔无燃料
```

作用：
- 防止左腔燃烧产物进入右腔
- 保持右腔组分稳定
- 在通量计算中强制右腔组分为初始值

## 使用建议

### 场景1：快速参数扫描
```python
solver = AdvancedSolverWithWENO(
    nx=500,           # 较少网格
    use_weno=False,
    use_rk3=False     # MUSCL+RK2最快
)
```

### 场景2：精度与速度平衡
```python
solver = AdvancedSolverWithWENO(
    nx=1500,
    use_weno=False,
    use_rk3=True      # MUSCL+RK3
)
```

### 场景3：最高精度
```python
solver = AdvancedSolverWithWENO(
    nx=2000,
    use_weno=True,    # WENO+RK3
    use_rk3=True
)
```

## 常见问题

**Q: WENO+RK3会改变结果吗？**
A: 会改进结果。WENO提供更好的激波分辨率，RK3提供更高的时间精度。

**Q: 膜片位置如何修改？**
A: 在`advanced_solver.py`中修改`self.x_interface`的初始值。

**Q: 右腔保护如何禁用？**
A: 在`advanced_solver.py`中设置`self.enforce_no_fuel_right = False`。

**Q: 计算时间会增加多少？**
A: WENO+RK3相对MUSCL+RK2约增加3-5倍。

## 技术细节

### WENO重构

五阶WENO使用三个子模板的加权组合：
```
p0 = (2*f[i-2] - 7*f[i-1] + 11*f[i]) / 6
p1 = (-f[i-1] + 5*f[i] + 2*f[i+1]) / 6
p2 = (2*f[i] + 5*f[i+1] - f[i+2]) / 6

f_WENO = w0*p0 + w1*p1 + w2*p2
```

权重基于光滑度指示器自动调整。

### 右腔保护实现

在通量计算中：
```python
if enforce_right_chamber and x[i] > x_interface:
    # 在右腔界面处，强制组分通量为零
    F[i, j] = 0.0  (j=3到6为组分)
```

## 下一步

1. 运行对比测试：`test_weno_vs_muscl.py`
2. 查看性能数据
3. 根据需求选择求解器

---

**版本**：1.0
**日期**：2025-11-13

