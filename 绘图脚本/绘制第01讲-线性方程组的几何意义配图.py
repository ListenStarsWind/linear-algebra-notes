from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
import yaml


项目根目录 = Path(__file__).resolve().parent.parent
配置路径 = 项目根目录 / "图像参数" / "第01讲-线性方程组的几何意义配图.yaml"

with 配置路径.open("r", encoding="utf-8") as 文件:
    配置 = yaml.safe_load(文件)

输出目录 = 项目根目录 / 配置["输出"]["目录"]
输出目录.mkdir(parents=True, exist_ok=True)

字体候选 = 配置["样式"]["字体"]
plt.rcParams["font.sans-serif"] = 字体候选
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["svg.fonttype"] = "none"

颜色 = 配置["样式"]["配色"]
DPI = int(配置["样式"]["dpi"])
二维范围 = 配置["坐标范围"]["二维"]
三维范围 = 配置["坐标范围"]["三维"]


def 统一二维坐标轴(坐标轴, 标题):
    坐标轴.set_title(标题, fontsize=13, pad=12)
    坐标轴.set_xlabel("x")
    坐标轴.set_ylabel("y")
    坐标轴.set_xlim(二维范围[0], 二维范围[1])
    坐标轴.set_ylim(二维范围[2], 二维范围[3])
    坐标轴.axhline(0, color="#374151", linewidth=0.9)
    坐标轴.axvline(0, color="#374151", linewidth=0.9)
    坐标轴.grid(True, linestyle=":", linewidth=0.55, alpha=0.55)
    坐标轴.set_aspect("equal", adjustable="box")


def 画箭头(坐标轴, 向量, 标签, 颜色值, 起点=(0, 0), 线宽=2.6, 标签偏移=(0.12, 0.12)):
    终点 = np.asarray(起点, dtype=float) + np.asarray(向量, dtype=float)
    坐标轴.annotate(
        "",
        xy=终点,
        xytext=起点,
        arrowprops=dict(arrowstyle="-|>", color=颜色值, linewidth=线宽),
    )
    坐标轴.text(
        终点[0] + 标签偏移[0],
        终点[1] + 标签偏移[1],
        标签,
        color=颜色值,
        fontsize=11,
        weight="bold",
    )


def 保存(图, 文件名):
    for 后缀 in 配置["输出"]["生成格式"]:
        图.savefig(
            输出目录 / f"{文件名}.{后缀}",
            dpi=DPI,
            bbox_inches="tight",
            facecolor="white",
        )
    plt.close(图)


def 图01_二维行图像():
    图, 坐标轴 = plt.subplots(figsize=配置["样式"]["二维尺寸"])
    x = np.linspace(二维范围[0], 二维范围[1], 400)
    坐标轴.plot(x, 2 * x, color=颜色["blue"], linewidth=2.2, label="2x - y = 0")
    坐标轴.plot(x, (x + 3) / 2, color=颜色["orange"], linewidth=2.2, label="-x + 2y = 3")
    解 = np.array([1, 2])
    坐标轴.scatter(*解, s=75, color=颜色["red"], edgecolor="white", linewidth=1.2, zorder=5)
    坐标轴.annotate("solution (1, 2)", 解, xytext=(1.35, 2.9), color=颜色["red"], weight="bold", arrowprops=dict(arrowstyle="->", color=颜色["red"]))
    统一二维坐标轴(坐标轴, "图01 二维行图像：两条直线的交点给出方程组的解")
    坐标轴.legend(loc="upper left", frameon=True, title="每个方程对应一条直线")
    保存(图, "图01-二维行图像-两条直线相交")


def 图02_二维列图像():
    图, 坐标轴 = plt.subplots(figsize=配置["样式"]["二维尺寸"])
    a1 = np.array([2, -1])
    a2 = np.array([-1, 2])
    b = a1 + 2 * a2
    画箭头(坐标轴, a1, "a1", 颜色["blue"], 标签偏移=(0.12, -0.28))
    画箭头(坐标轴, a2, "a2", 颜色["orange"], 标签偏移=(-0.55, 0.12))
    画箭头(坐标轴, 2 * a2, "2a2", 颜色["orange"], 起点=a1, 线宽=2.2, 标签偏移=(-0.8, 0.18))
    画箭头(坐标轴, b, "b", 颜色["red"], 线宽=3.1, 标签偏移=(0.18, 0.18))
    坐标轴.plot([a1[0], b[0]], [a1[1], b[1]], linestyle="--", color=颜色["gray"], linewidth=1)
    坐标轴.plot([2 * a2[0], b[0]], [2 * a2[1], b[1]], linestyle="--", color=颜色["gray"], linewidth=1)
    坐标轴.scatter(*b, color=颜色["red"], s=48, zorder=5)
    统一二维坐标轴(坐标轴, "图02 二维列图像：把 b 写成列向量的线性组合")
    坐标轴.text(-3.7, 7.1, "a1 + 2a2 = b", fontsize=12, weight="bold")
    坐标轴.text(-3.7, 6.35, "x=1, y=2", color=颜色["gray"])
    保存(图, "图02-二维列图像-线性组合得到b")


def 三维坐标轴(标题):
    图 = plt.figure(figsize=配置["样式"]["三维尺寸"])
    坐标轴 = 图.add_subplot(111, projection="3d")
    坐标轴.set_title(标题, pad=16, fontsize=13)
    坐标轴.set_xlabel("x", labelpad=5)
    坐标轴.set_ylabel("y", labelpad=5)
    坐标轴.set_zlabel("z", labelpad=5)
    坐标轴.set_xlim(三维范围[0], 三维范围[1])
    坐标轴.set_ylim(三维范围[2], 三维范围[3])
    坐标轴.set_zlim(三维范围[4], 三维范围[5])
    坐标轴.set_box_aspect((1, 1, 1))
    坐标轴.view_init(elev=22, azim=-58)
    return 图, 坐标轴


def 画三维箭头(坐标轴, 向量, 标签, 颜色值, 标签偏移=(0.1, 0.1, 0.1), 线宽=2.6):
    向量 = np.asarray(向量, dtype=float)
    坐标轴.quiver(0, 0, 0, *向量, color=颜色值, linewidth=线宽, arrow_length_ratio=0.09)
    坐标轴.text(*(向量 + np.asarray(标签偏移)), 标签, color=颜色值, fontsize=11, weight="bold")


def 图03_三维行图像():
    图, 坐标轴 = 三维坐标轴("图03 三维行图像：三个平面的交点给出方程组的解")
    u = np.linspace(-3.2, 3.2, 18)
    v = np.linspace(-3.2, 3.2, 18)
    U, V = np.meshgrid(u, v)
    平面 = [
        (U, 2 * U, V, 颜色["blue"], "2x - y = 0"),
        (U, V, 1 - U + 2 * V, 颜色["orange"], "-x + 2y - z = -1"),
        (U, V, 1 + 0.75 * V, 颜色["green"], "-3y + 4z = 4")
    ]
    for X, Y, Z, 颜色值, _ in 平面:
        坐标轴.plot_surface(X, Y, Z, color=颜色值, alpha=0.26, linewidth=0, antialiased=True)
    解 = np.array([0, 0, 1])
    坐标轴.scatter(*解, color=颜色["red"], s=75, edgecolor="white", linewidth=1.2, depthshade=False)
    坐标轴.text(0.25, 0.25, 1.2, "solution (0, 0, 1)", color=颜色["red"], weight="bold")
    图.legend(handles=[
        Line2D([0], [0], color=颜色["blue"], linewidth=7, alpha=0.5, label="2x - y = 0"),
        Line2D([0], [0], color=颜色["orange"], linewidth=7, alpha=0.5, label="-x + 2y - z = -1"),
        Line2D([0], [0], color=颜色["green"], linewidth=7, alpha=0.5, label="-3y + 4z = 4"),
    ], loc="upper left", bbox_to_anchor=(0.02, 0.96), fontsize=8)
    保存(图, "图03-三维行图像-三个平面交一点")


def 图04_三维列图像():
    图, 坐标轴 = 三维坐标轴("图04 三维列图像：把 b 写成列向量的线性组合")
    c1 = np.array([2, -1, 0])
    c2 = np.array([-1, 2, -3])
    c3 = np.array([0, -1, 4])
    b = c1 + c2
    画三维箭头(坐标轴, c1, "c1", 颜色["blue"], 标签偏移=(0.08, -0.2, 0.08))
    画三维箭头(坐标轴, c2, "c2", 颜色["orange"], 标签偏移=(-0.65, 0.05, -0.1))
    画三维箭头(坐标轴, c3, "c3", 颜色["gray"], 标签偏移=(0.12, 0.12, 0.12), 线宽=1.6)
    坐标轴.quiver(*c1, *c2, color=颜色["orange"], linewidth=2.2, arrow_length_ratio=0.09)
    坐标轴.quiver(*c2, *c1, color=颜色["blue"], linewidth=2.2, arrow_length_ratio=0.09)
    坐标轴.plot([c1[0], b[0]], [c1[1], b[1]], [c1[2], b[2]], linestyle="--", color=颜色["gray"], linewidth=1)
    坐标轴.plot([c2[0], b[0]], [c2[1], b[1]], [c2[2], b[2]], linestyle="--", color=颜色["gray"], linewidth=1)
    坐标轴.quiver(0, 0, 0, *b, color=颜色["red"], linewidth=3.4, arrow_length_ratio=0.09)
    坐标轴.text(*(b + np.array([0.12, 0.12, 0.12])), "b", color=颜色["red"], fontsize=11, weight="bold")
    坐标轴.text2D(0.04, 0.9, "b = c1 + c2 = [1, 1, -3]^T", transform=坐标轴.transAxes, fontsize=11, weight="bold")
    坐标轴.text2D(0.04, 0.855, "solution: (x, y, z) = (1, 1, 0)", transform=坐标轴.transAxes, color=颜色["gray"])
    保存(图, "图04-三维列图像-线性组合得到b")


def 图05_哪些b可解():
    图 = plt.figure(figsize=(12, 5.6))
    左轴 = 图.add_subplot(121, projection="3d")
    右轴 = 图.add_subplot(122, projection="3d")
    向量组 = [np.array([2, 0.5, 0.3]), np.array([0.5, 2, -0.5]), np.array([-0.4, 0.2, 2])]
    for 坐标轴, 标题 in [(左轴, "独立方向：张成整个三维空间"), (右轴, "共面：只张成一个平面")]:
        坐标轴.set_title(标题, fontsize=11, pad=10)
        坐标轴.set_xlim(-3, 3)
        坐标轴.set_ylim(-3, 3)
        坐标轴.set_zlim(-3, 3)
        坐标轴.set_xlabel("x")
        坐标轴.set_ylabel("y")
        坐标轴.set_zlabel("z")
        坐标轴.set_box_aspect((1, 1, 1))
        坐标轴.view_init(elev=22, azim=-58)
    for 索引, 向量 in enumerate(向量组):
        画三维箭头(左轴, 向量, f"a{索引 + 1}", list(颜色.values())[索引])
    左轴.text2D(0.04, 0.86, "any b\nAx = b 有解", transform=左轴.transAxes, color=颜色["green"], weight="bold", bbox=dict(facecolor="white", alpha=0.8, edgecolor="none", pad=3))
    平面向量 = [np.array([2, 0, 0]), np.array([0, 2, 0]), np.array([1, 1, 0])]
    for 索引, 向量 in enumerate(平面向量):
        画三维箭头(右轴, 向量, f"a{索引 + 1}", list(颜色.values())[索引])
    网格 = np.linspace(-2.6, 2.6, 2)
    X, Y = np.meshgrid(网格, 网格)
    右轴.plot_surface(X, Y, 0 * X, color=颜色["blue"], alpha=0.2, linewidth=0)
    b内 = np.array([1.5, 1.0, 0])
    b外 = np.array([0.8, 0.8, 2.1])
    画三维箭头(右轴, b内, "b_in", 颜色["green"], 线宽=3)
    画三维箭头(右轴, b外, "b_out", 颜色["red"], 线宽=3)
    右轴.text2D(0.04, 0.86, "b_in: 可解\nb_out: 不可解", transform=右轴.transAxes, weight="bold", bbox=dict(facecolor="white", alpha=0.8, edgecolor="none", pad=3))
    图.suptitle("图05 哪些 b 可解：列向量张成空间决定方程组是否有解", fontsize=14, y=0.98)
    图.tight_layout(rect=(0, 0, 1, 0.94))
    保存(图, "图05-哪些b可解-张成空间决定可解性")


def 主程序():
    for 旧文件 in 输出目录.glob("图*.png"):
        旧文件.unlink()
    for 旧文件 in 输出目录.glob("图*.svg"):
        旧文件.unlink()
    图01_二维行图像()
    图02_二维列图像()
    图03_三维行图像()
    图04_三维列图像()
    图05_哪些b可解()
    文件列表 = sorted(输出目录.glob("图*.png"))
    print("静态配图生成完成。")
    print(f"输出目录：{输出目录.relative_to(项目根目录)}")
    print(f"PNG 数量：{len(文件列表)}，SVG 同步生成：{len(list(输出目录.glob('图*.svg')))} 张")
    for 文件 in 文件列表:
        print(f"- {文件.relative_to(项目根目录)}")


if __name__ == "__main__":
    主程序()