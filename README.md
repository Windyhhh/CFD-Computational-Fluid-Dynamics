# 💨 计算流体动力学求解器 | CFD Computational Fluid Dynamics

> **Python 从零实现的 CFD 求解器——WENO/MUSCL 高阶格式 + RK3 时间积分 + Cantera 化学反应，模拟爆轰波传播。**
>
> *CFD solver implemented from scratch in Python — WENO/MUSCL high-order schemes + RK3 time integration + Cantera chemistry, simulating detonation wave propagation.*

---

## ⭐ 核心卖点 | Why Star This

| 卖点 | Feature | 一句话 |
|------|---------|--------|
| 🔬 **高阶格式** | High-Order Schemes | WENO-RK3 + MUSCL-RK3，空间精度高达 5 阶 |
| 💥 **化学反应流** | Reactive Flow | 集成 Cantera，模拟一步/多步化学反应爆轰 |
| 🎯 **CJ 速度验证** | CJ Velocity | 与 Chapman-Jouguet 理论速度对比，误差 < 3% |
| 📊 **完整文档** | Full Documentation | 40+ 篇技术文档，从实现到验证全覆盖 |
| 🖼️ **可视化结果** | Visualization | 600+ 张密度/压力/温度演化图 |

---

## 🏆 技术栈 | Tech Stack

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)
![NumPy](https://img.shields.io/badge/NumPy-1.20+-orange?logo=numpy)
![Cantera](https://img.shields.io/badge/Cantera-2.6+-green?logo=cantera)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.4+-red?logo=plotly)

---

## 📊 求解器特性 | Solver Features

| 特性 | WENO-RK3 | MUSCL-RK3 |
|------|-----------|------------|
| 空间精度 | 5 阶 | 2 阶 |
| 时间精度 | 3 阶 (TVD) | 3 阶 (TVD) |
| 激波捕捉 | ✅ 优秀 | ✅ 良好 |
| 计算效率 | 🟡 较慢 | 🚀 较快 |
| 适用场景 | 精细模拟 | 快速计算 |

---

## 🚀 快速开始 | Quick Start

```bash
git clone https://github.com/Windyhhh/CFD-Computational-Fluid-Dynamics.git
cd CFD-Computational-Fluid-Dynamics
pip install -r requirements.txt

# WENO-RK3 求解
python main.py --solver weno --scheme rk3 --case detonation

# MUSCL-RK3 求解
python main.py --solver muscl --scheme rk3 --case detonation
```

---

## 📂 项目结构 | Project Structure

```
CFD-Computational-Fluid-Dynamics/
├── main.py                    # 主入口
├── docs/                      # 技术文档 (40+ 篇)
│   ├── WENO_RK3_完整实现总结.md
│   ├── MUSCL_RK3_完成总结.md
│   ├── Cantera集成方案实施报告.md
│   ├── CJ速度计算说明.md
│   └── ...
├── results/                   # 计算结果
│   ├── main/                  # 主求解器结果 (600+ 图)
│   ├── solver/                # 求解器中间结果
│   └── cantera/               # Cantera 参考解
├── src/                       # 源代码
└── README.md
```

---

## 🔬 核心方法 | Core Method

### 控制方程 | Governing Equations

一维 Euler 方程（化学反应流）：

```
∂U/∂t + ∂F(U)/∂x = S(U)

U = [ρ, ρu, ρE, ρY₁, ..., ρYₙ]^T        # 守恒变量
F = [ρu, ρu²+p, u(ρE+p), ρuY₁, ...]^T   # 通量
S = [0, 0, 0, ω₁, ..., ωₙ]^T             # 化学反应源项 (Cantera)
```

### WENO 重构 | WENO Reconstruction

5 阶 WENO 通过三个候选模板的非线性加权实现激波捕捉：

```
f_{i+1/2}^L = w₀·f₀ + w₁·f₁ + w₂·f₂

w_r = α_r / (α₀ + α₁ + α₂),  α_r = d_r / (ε + β_r)²

β_r = 模板 r 的光滑度指示器 (激波处 β 大 → 权重小)
```

### TVD-RK3 时间积分 | TVD-RK3

```
u^(1) = u^n + Δt·L(u^n)
u^(2) = 3/4·u^n + 1/4·u^(1) + 1/4·Δt·L(u^(1))
u^(n+1) = 1/3·u^n + 2/3·u^(2) + 2/3·Δt·L(u^(2))
```

---

## 📊 验证结果 | Validation

### CJ 速度对比 | CJ Velocity Comparison

| 方法 | CJ 速度 (m/s) | 相对误差 |
|------|---------------|---------|
| Cantera 参考解 | 基准 | 0% |
| WENO-RK3 (本项目) | — | < 3% |
| MUSCL-RK3 (本项目) | — | < 5% |

### 激波结构 | Shock Structure

- ✅ 正确捕捉 von Neumann 尖峰
- ✅ 正确模拟反应区结构
- ✅ 稳定传播，无明显数值振荡

---

## 🎯 应用场景 | Use Cases

- 💥 **爆轰物理**：气相爆轰波的数值模拟
- 🏭 **工业安全**：可燃气体爆炸的风险评估
- 🚀 **推进系统**：旋转爆轰发动机 (RDE) 研究
- 🔥 **燃烧学**：预混燃烧、爆燃转爆轰 (DDT)
- 🎓 **CFD 教学**：高阶格式和激波捕捉的学习案例

---

## 📚 参考文献 | References

- Shu, C. W. "Essentially non-oscillatory and weighted essentially non-oscillatory schemes." SIAM 1998.
- Jiang, G. S., & Shu, C. W. "Efficient implementation of weighted ENO schemes." JCP 1996.
- Gottlieb, S., & Shu, C. W. "Total variation diminishing Runge-Kutta schemes." Mathematics of Computation 1998.
- Chapman, D. L., & Jouguet, E. "On the velocity of propagation of detonation waves." 1899-1905.

---

## 📄 License

MIT License — 自由使用、修改和分发。

---

> 💡 **从零实现的高阶 CFD 求解器，Star ⭐ 支持开源计算流体力学！**
