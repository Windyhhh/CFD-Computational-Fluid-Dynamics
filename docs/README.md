# 一维激波管CFD求解器（带燃烧反应）

## 简介

这是一个基于有限体积法（FVM）的一维可压缩流动求解器，用于模拟Sod激波管问题，支持H₂-O₂燃烧反应。

**核心特性：**
- HLL Riemann求解器
- MUSCL-Hancock高阶格式（二阶空间精度）
- 二阶或三阶Runge-Kutta时间积分（可选）
- H₂-O₂燃烧反应（Arrhenius动力学）
- 可选点火核（ignition kernel）
- 右腔保护机制（防止燃烧产物进入）

---

## 快速开始

### 1. 运行纯净模拟（无燃烧）
```bash
cd shock_tube_solver
python run_clean_simulation.py
```

### 2. 运行带点火核的燃烧模拟
```bash
cd shock_tube_solver
python run_clean_simulation.py --with_ignition
```

### 3. 使用MUSCL+RK3求解器（三阶时间精度）
```bash
cd shock_tube_solver
python run_weno_simulation.py --with_ignition
```

### 4. 使用WENO+RK3求解器（五阶空间精度）
```bash
cd shock_tube_solver
# 在Python代码中指定use_weno=True
python -c "
from advanced_solver_weno import AdvancedSolverWithWENO
solver = AdvancedSolverWithWENO(nx=2000, use_weno=True, with_ignition=True)
# 运行模拟...
"
```

### 5. 查看结果
```bash
python show_results.py      # 显示数值结果
python plot_xt.py           # 绘制x-t图
```

---

## 初始条件

### 标准Sod激波管问题

| 参数 | 左腔 (x≤50m) | 右腔 (x>50m) |
|------|-------------|------------|
| 压力 (atm) | 30 | 0.03 |
| 温度 (K) | 600 | 300 |
| Y_H₂ | 0.15 | 0.00 |
| Y_O₂ | 0.25 | 0.23 |
| Y_N₂ | 0.60 | 0.77 |

### 点火核参数
- **位置**：x = 45.0 ~ 49.8 m
- **温度**：1200 K
- **作用**：触发左腔H₂-O₂燃烧反应

---

## 求解器选择

### MUSCL+RK2（默认）
- **空间精度**：二阶
- **时间精度**：二阶
- **计算速度**：快（基准）
- **推荐场景**：快速原型、参数敏感性分析
- **运行脚本**：`run_clean_simulation.py`

### MUSCL+RK3（推荐）
- **空间精度**：二阶
- **时间精度**：三阶
- **计算速度**：0.71x（相对RK2）
- **推荐场景**：精度与速度平衡
- **运行脚本**：`run_weno_simulation.py`

### WENO+RK3（高精度）✨
- **空间精度**：五阶
- **时间精度**：三阶
- **计算速度**：~0.2x（相对RK2）
- **推荐场景**：最高精度需求
- **运行脚本**：`run_weno_simulation.py`

**性能对比**：
| 指标 | MUSCL+RK2 | MUSCL+RK3 | WENO+RK3 |
|------|-----------|----------|---------|
| 空间精度 | 二阶 | 二阶 | **五阶** |
| 时间精度 | 二阶 | 三阶 | 三阶 |
| 步数/秒 | 34.2 | 24.3 | ~7 |
| 相对速度 | 1.0x | 0.71x | ~0.2x |

详见 `shock_tube_solver/MUSCL_RK3_实现总结.md`、`shock_tube_solver/WENO_RK3_使用指南.md` 和 `WENO_RK3_完整实现总结.md`

---

## 关键参数

在 `advanced_solver.py` 中可配置：

```python
# 右腔约束参数
self.enforce_no_fuel_right = True        # 强制右腔无燃料
self.hard_block_reaction_right = True    # 硬禁用右腔反应
self.h2_clip_ratio = 1e-15               # 右腔H₂上限

# 燃烧反应参数
self.combustion_threshold = 800.0        # 燃烧温度阈值 (K)
self.reaction_rate_factor = 1.0          # 反应速率因子
```

---

## 问题解决

### 问题1：右腔燃烧
**原因**：燃烧产物通过激波混合进入右腔
**解决**：强制右腔组分保持初始值
**状态**：✅ 已解决

### 问题2：膜片处氧气浓度异常
**原因**：消耗的O₂通过激波混合进入右腔
**解决**：强制右腔组分保持初始值
**状态**：✅ 已解决

### 问题3：氧气浓度振荡
**原因**：Riemann求解器中的组分通量导致右腔组分不稳定
**解决**：在通量计算中强制右腔使用初始组分
**修复效果**：
- 有点火核：振荡幅度从 15.2% 降至 **0.29%** ↓ 98.1%
- 无点火核：振荡幅度从 2.0% 降至 **0.16%** ↓ 92.2%
**状态**：✅ 已解决

详见 `问题解决总结.md` 和 `氧气振荡修复总结.md`

---

## 文件结构

```
shock_tube_solver/
├── advanced_solver.py              # 主求解器（MUSCL+RK2）
├── advanced_solver_weno.py         # 扩展求解器（支持MUSCL/WENO + RK2/RK3）
├── riemann_solver.py               # Riemann求解器（MUSCL）
├── weno_rk3_solver.py              # WENO求解器（五阶）
├── run_clean_simulation.py         # 运行脚本（MUSCL+RK2）
├── run_weno_simulation.py          # 运行脚本（MUSCL+RK3/WENO+RK3）
├── show_results.py                 # 结果显示
├── plot_xt.py                      # x-t图绘制
├── test_muscl_rk2_vs_rk3.py        # MUSCL性能对比测试
├── test_weno_rk3_integration.py    # WENO集成测试
├── MUSCL_RK3_实现总结.md           # MUSCL+RK3实现细节
├── MUSCL_RK3_测试报告.md           # MUSCL+RK3测试报告
├── 快速开始_MUSCL_RK3.md           # MUSCL+RK3使用指南
├── WENO_RK3_使用指南.md            # WENO+RK3使用指南
├── main.py                         # 主程序入口
└── results/                        # 输出结果目录
```

---

## 输出结果

模拟结果保存在 `results/` 目录：
- `advanced_final_t_*.txt`：数值结果（密度、速度、压力、温度、组分）
- `advanced_*.png`：可视化图像

---

## 参考文献

- Toro, E. F. (2009). Riemann Solvers and Numerical Methods for Fluid Dynamics
- van Leer, B. (1979). Towards the ultimate conservative difference scheme

