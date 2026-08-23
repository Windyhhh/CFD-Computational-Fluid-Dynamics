# 快速开始：MUSCL+RK3求解器

## 什么是MUSCL+RK3？

- **MUSCL**：二阶空间重构（Monotonic Upstream-centered Scheme for Conservation Laws）
- **RK3**：三阶时间积分（Strong Stability Preserving Runge-Kutta）
- **优势**：时间精度从二阶提升到三阶，计算成本增加约40%

## 快速测试

### 1. 运行快速对比测试

```bash
cd shock_tube_solver
python << 'EOF'
from advanced_solver_weno import AdvancedSolverWithWENO
import time

# 测试MUSCL+RK2
print("Testing MUSCL+RK2...")
start = time.time()
solver_rk2 = AdvancedSolverWithWENO(nx=500, use_weno=False, with_ignition=True)
for i in range(50):
    solver_rk2.solve_step_with_threshold()
print(f"  50 steps in {time.time()-start:.2f}s")

# 测试MUSCL+RK3
print("Testing MUSCL+RK3...")
start = time.time()
solver_rk3 = AdvancedSolverWithWENO(nx=500, use_weno=True, with_ignition=True)
for i in range(50):
    solver_rk3.solve_step_with_threshold()
print(f"  50 steps in {time.time()-start:.2f}s")
EOF
```

### 2. 运行完整模拟

```bash
# 使用MUSCL+RK3（有点火核）
python run_weno_simulation.py --with_ignition

# 使用MUSCL+RK2（有点火核）
python run_clean_simulation.py --with_ignition
```

## 在代码中使用

### 创建求解器

```python
from advanced_solver_weno import AdvancedSolverWithWENO

# 使用MUSCL+RK3
solver = AdvancedSolverWithWENO(
    nx=2000,           # 网格数
    L=100.0,           # 计算域长度
    use_weno=True,     # 启用RK3
    with_ignition=True # 启用点火核
)

# 使用MUSCL+RK2
solver = AdvancedSolverWithWENO(
    nx=2000,
    L=100.0,
    use_weno=False,    # 使用RK2
    with_ignition=True
)
```

### 运行模拟

```python
t_final = 0.025  # 最终时间
output_interval = 0.001

next_output = output_interval
while solver.time < t_final:
    # 自动计算时间步长
    solver.solve_step_with_threshold()
    
    if solver.time >= next_output:
        print(f"t={solver.time:.6f}s")
        next_output += output_interval
```

## 性能指标

| 方案 | 时间精度 | 相对速度 | 推荐场景 |
|------|---------|---------|---------|
| MUSCL+RK2 | 二阶 | 1.0x | 快速原型 |
| MUSCL+RK3 | 三阶 | 0.71x | 高精度需求 |

## 常见问题

### Q: 应该选择RK2还是RK3？

**A:** 
- 快速测试/原型 → 选择RK2
- 需要高精度 → 选择RK3
- 不确定 → 先用RK2快速测试，再用RK3精细计算

### Q: RK3会改变结果吗？

**A:** 不会显著改变。两种方案的物理结果一致，只是时间精度不同。

### Q: 如何切换求解器？

**A:** 只需改变`use_weno`参数：
```python
use_weno=False  # MUSCL+RK2
use_weno=True   # MUSCL+RK3
```

### Q: 计算时间会增加多少？

**A:** 约增加40%（RK3需要3次通量计算，RK2需要2次）

## 输出文件

模拟结果保存在`results/`目录：
- `weno_*_t_*.txt` - 数据文件
- `weno_*_t_*.png` - 可视化图像

## 下一步

1. 查看详细文档：`MUSCL_RK3_实现总结.md`
2. 运行对比测试：`test_muscl_rk2_vs_rk3.py`
3. 修改参数进行敏感性分析

## 技术支持

遇到问题？检查：
1. 网格数是否足够（建议≥1000）
2. CFL数是否合理（默认0.3）
3. 点火核参数是否正确

