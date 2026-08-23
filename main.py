#!/usr/bin/env python3
"""
计算流体力学激波管求解器 - 项目主入口

核心功能：
1. 提供统一的命令行接口
2. 支持不同求解器的选择
3. 管理结果输出目录
4. 提供示例运行脚本
"""

import argparse
import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def run_simple_solver():
    """运行简单求解器"""
    print("运行简单激波管求解器...")
    from solver.main import ShockTubeSolver
    
    # 确保结果目录存在
    results_dir = os.path.join(os.path.dirname(__file__), 'results', 'main')
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    
    # 保存当前目录
    original_dir = os.getcwd()
    try:
        # 切换到项目根目录
        os.chdir(os.path.dirname(__file__))
        
        # 创建求解器实例
        solver = ShockTubeSolver(nx=1000, cfl=0.5)
        solver.initialize()
        
        # 运行求解
        solver.solve(t_end=0.01, output_interval=0.002)
        print("简单求解器运行完成！")
    finally:
        # 恢复原始目录
        os.chdir(original_dir)

def run_advanced_solver():
    """运行高级求解器"""
    print("运行高精度激波管求解器...")
    from solver.advanced_solver import AdvancedShockTubeSolver
    
    # 确保结果目录存在
    results_dir = os.path.join(os.path.dirname(__file__), 'results', 'solver')
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    
    # 保存当前目录
    original_dir = os.getcwd()
    try:
        # 切换到项目根目录
        os.chdir(os.path.dirname(__file__))
        
        # 创建求解器实例
        solver = AdvancedShockTubeSolver(
            nx=1000,      # 网格点数
            L=100.0,      # 管长 (m)
            cfl=0.2       # CFL数
        )
        
        # 初始化条件
        solver.initialize_conditions()
        
        # 确保右腔控制参数正确设置
        solver.enforce_no_fuel_right = True      # 裁剪右腔氢气到极小值
        solver.hard_block_reaction_right = True  # 硬禁用右腔化学反应
        solver.h2_clip_ratio = 1e-15             # 右腔氢气上限
        
        # 左端点火模式
        solver.ignite_left_layer = (0.0, 5.0, 1200.0)  # 左端点火
        t_end = 0.05
        
        # 运行求解
        solver.solve(
            t_end=t_end,
            output_interval=0.002,
            combustion_threshold=800
        )
        print("高精度求解器运行完成！")
    finally:
        # 恢复原始目录
        os.chdir(original_dir)

def run_cantera_solver():
    """运行Cantera求解器"""
    print("运行Cantera集成求解器...")
    from solver.cantera_solver import CanteraShockTubeSolver
    
    # 确保结果目录存在
    results_dir = os.path.join(os.path.dirname(__file__), 'results', 'cantera')
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    
    # 保存当前目录
    original_dir = os.getcwd()
    try:
        # 切换到项目根目录
        os.chdir(os.path.dirname(__file__))
        
        # 创建求解器实例
        solver = CanteraShockTubeSolver()
        
        # 运行求解
        solver.run_simulation()
        print("Cantera求解器运行完成！")
    finally:
        # 恢复原始目录
        os.chdir(original_dir)

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="激波管求解器命令行接口")
    parser.add_argument('--solver', type=str, default='advanced', 
                       choices=['simple', 'advanced', 'cantera'],
                       help="选择求解器类型")
    parser.add_argument('--test', action='store_true',
                       help="运行测试模式")
    
    args = parser.parse_args()
    
    if args.test:
        print("运行测试模式...")
        # 这里可以添加测试代码
        print("测试完成！")
        return
    
    # 根据选择运行不同的求解器
    if args.solver == 'simple':
        run_simple_solver()
    elif args.solver == 'advanced':
        run_advanced_solver()
    elif args.solver == 'cantera':
        run_cantera_solver()
    
    print("\n求解完成！结果保存在 results/ 目录下。")

if __name__ == "__main__":
    main()