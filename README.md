# 💨 CFD Computational Fluid Dynamics | 计算流体动力学合集

> **Collection of Computational Fluid Dynamics (CFD) projects. Includes solvers, simulations, mesh generation, and visualization for various flow problems. From simple 2D lid-driven cavity to complex 3D turbulent flows.**
>
> 计算流体动力学（CFD）项目合集。包含求解器、模拟、网格生成和各种流动问题的可视化。从简单的 2D 顶盖驱动方腔到复杂的 3D 湍流。

---

## 🌟 Features | 核心特性

- **Multiple Solvers** — FVM, FDM, spectral methods
- **2D/3D Flows** — From cavity to complex geometries
- **Turbulence** — RANS, LES, DNS models
- **Mesh Generation** — Structured/unstructured grids
- **Visualization** — Contour plots, streamlines, vector fields
- **Validation** — Benchmark cases (Lid-driven cavity, Poiseuille)

---

## 🚀 Quick Start | 快速开始

```bash
# Run 2D lid-driven cavity
python solvers/lid_driven_cavity.py --Re 100 --grid 128x128

# Run 3D channel flow
python solvers/channel_flow_3d.py --Re 5000 --model les

# Visualize results
python visualize.py --input results/flow.vtk --type contour
```

---

## 📚 Projects | 项目列表

| Project | Type | Dimensions | Turbulence |
|---------|------|------------|------------|
| **Lid-Driven Cavity** | Benchmark | 2D | Laminar |
| **Poiseuille Flow** | Benchmark | 2D/3D | Laminar |
| **Cylinder Wake** | Vortex shedding | 2D | Laminar/LES |
| **Channel Flow** | Internal flow | 3D | RANS/LES/DNS |
| **Airfoil** | External flow | 2D/3D | RANS |
| **Heat Transfer** | Conjugate HT | 3D | RANS |

---

## 🔬 Numerical Methods | 数值方法

- **Finite Volume Method (FVM)** — Conservation-based
- **Finite Difference Method (FDM)** — Simple structured grids
- **SIMPLE/PISO** — Pressure-velocity coupling
- **Runge-Kutta** — Time integration
- **TVD/WENO** — High-resolution schemes

---

## 📄 License | 许可证

MIT License.

[GitHub](https://github.com/Windyhhh/CFD-Computational-Fluid-Dynamics)
