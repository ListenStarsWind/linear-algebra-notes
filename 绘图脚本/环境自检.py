import numpy as np

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import plotly.graph_objects as go


# ============================================================
# Matplotlib 中文字体配置
# ============================================================

plt.rcParams["font.sans-serif"] = ["Noto Sans CJK SC"]
plt.rcParams["axes.unicode_minus"] = False


# ============================================================
# 测试数学对象
#
# 平面：
#
#     x + y + z = 3
#
# 即：
#
#     z = 3 - x - y
# ============================================================

x = np.linspace(-2, 4, 40)
y = np.linspace(-2, 4, 40)

X, Y = np.meshgrid(x, y)
Z = 3 - X - Y


# ============================================================
# 1. Matplotlib
#    生成供 Markdown 使用的静态 SVG
# ============================================================

图 = plt.figure(figsize=(8, 6))

坐标轴 = 图.add_subplot(
    111,
    projection="3d",
)

坐标轴.plot_surface(
    X,
    Y,
    Z,
    alpha=0.65,
)

坐标轴.set_title("环境自检：平面 x + y + z = 3")

坐标轴.set_xlabel("x")
坐标轴.set_ylabel("y")
坐标轴.set_zlabel("z")

坐标轴.set_box_aspect((1, 1, 1))

图.tight_layout()

静态文件 = "静态图像/环境自检-三维平面.svg"

图.savefig(
    静态文件,
    format="svg",
    bbox_inches="tight",
)

plt.close(图)


# ============================================================
# 2. Plotly
#    生成可由 Windows 浏览器查看的交互式 HTML
# ============================================================

交互图 = go.Figure()

交互图.add_trace(
    go.Surface(
        x=X,
        y=Y,
        z=Z,
        name="x + y + z = 3",
        showscale=False,
    )
)

交互图.update_layout(
    title="环境自检：平面 x + y + z = 3",

    # HTML 最终由 Windows 浏览器渲染，因此把 Windows
    # 常见中文字体放在前面，同时保留 Linux 字体作为后备。
    font={
        "family":
        "Microsoft YaHei, Noto Sans CJK SC, sans-serif"
    },

    scene={
        "xaxis_title": "x",
        "yaxis_title": "y",
        "zaxis_title": "z",
        "aspectmode": "cube",
    },
)

交互文件 = "交互图像/环境自检-三维平面.html"

交互图.write_html(
    交互文件,
    include_plotlyjs=True,
    full_html=True,
)


print("环境自检完成。")
print()
print(f"静态图像：{静态文件}")
print(f"交互图像：{交互文件}")
