import json
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
import yaml


参数路径 = Path("图像参数/三维向量线性组合交互实验.yaml")

with 参数路径.open("r", encoding="utf-8") as f:
    参数 = yaml.safe_load(f)


def 必需参数(配置, 键名):
    if 键名 not in 配置:
        raise ValueError(f"YAML 缺少核心参数：{键名}")
    return 配置[键名]


向量参数 = 必需参数(参数, "向量")
向量 = {}
for 名称 in ("u", "v", "w"):
    向量[名称] = np.array(
        必需参数(向量参数, 名称),
        dtype=float,
    )
    if 向量[名称].shape != (3,):
        raise ValueError(f"核心参数 {名称} 必须是包含三个数值的三维向量")

u = 向量["u"]
v = 向量["v"]
w = 向量["w"]

初始系数 = 必需参数(参数, "初始系数")
c初始 = float(必需参数(初始系数, "c"))
d初始 = float(必需参数(初始系数, "d"))
e初始 = float(必需参数(初始系数, "e"))

滑块参数 = 必需参数(参数, "滑块")
滑块最小值 = float(必需参数(滑块参数, "最小值"))
滑块最大值 = float(必需参数(滑块参数, "最大值"))
滑块步长 = float(必需参数(滑块参数, "步长"))

坐标范围 = 必需参数(参数, "坐标范围")
x范围 = 必需参数(坐标范围, "x")
y范围 = 必需参数(坐标范围, "y")
z范围 = 必需参数(坐标范围, "z")

显示参数 = 参数.get("显示", {})
显示三角形 = bool(显示参数.get("显示三角形", True))
显示四面体 = bool(显示参数.get("显示四面体", True))
显示三角形边 = bool(显示参数.get("显示三角形边", True))
显示系数和为1参考平面 = bool(
    显示参数.get("显示系数和为1参考平面", False)
)

约束模式 = 参数.get("初始约束模式", "自由模式")
允许模式 = {"自由模式", "系数和 = 1", "三角形模式", "三棱锥模式"}
if 约束模式 not in 允许模式:
    raise ValueError(
        f"初始约束模式必须是以下之一：{', '.join(允许模式)}"
    )

输出路径 = Path(必需参数(必需参数(参数, "输出"), "html"))
输出路径.parent.mkdir(parents=True, exist_ok=True)


def 计算线性组合(c, d, e):
    return c * u + d * v + e * w


p初始 = 计算线性组合(c初始, d初始, e初始)
p标签偏移 = np.full(
    3,
    0.08 * max(
        np.linalg.norm(u),
        np.linalg.norm(v),
        np.linalg.norm(w),
    ),
)

fig = go.Figure()

# 原点和三个基础向量。
原点_trace索引 = len(fig.data)
fig.add_trace(
    go.Scatter3d(
        x=[0],
        y=[0],
        z=[0],
        mode="markers+text",
        text=["O"],
        textposition="bottom center",
        name="O",
        showlegend=False,
        marker=dict(size=5, color="#222222"),
        hovertemplate="O<br>(0, 0, 0)<extra></extra>",
    )
)

基础向量_trace索引 = {}
for 名称, 向量值, 颜色 in (
    ("u", u, "#d62728"),
    ("v", v, "#2ca02c"),
    ("w", w, "#1f77b4"),
):
    基础向量_trace索引[名称] = len(fig.data)
    fig.add_trace(
        go.Scatter3d(
            x=[0, 向量值[0]],
            y=[0, 向量值[1]],
            z=[0, 向量值[2]],
            mode="lines+markers+text",
            text=["", 名称],
            textposition="top center",
            name=名称,
            showlegend=True,
            line=dict(color=颜色, width=8),
            marker=dict(size=4, color=颜色),
            hovertemplate=(
                f"{名称}<br>坐标: "
                f"({向量值[0]:.3f}, {向量值[1]:.3f}, "
                f"{向量值[2]:.3f})<extra></extra>"
            ),
        )
    )

p_trace索引 = len(fig.data)
fig.add_trace(
    go.Scatter3d(
        x=[0, p初始[0]],
        y=[0, p初始[1]],
        z=[0, p初始[2]],
        mode="lines+markers",
        name="p = cu + dv + ew",
        showlegend=True,
        line=dict(color="#111111", width=10),
        marker=dict(size=5, color="#111111"),
        hovertemplate="p<br>坐标: (%{x:.3f}, %{y:.3f}, %{z:.3f})<extra></extra>",
    )
)

p标签_trace索引 = len(fig.data)
fig.add_trace(
    go.Scatter3d(
        x=[p初始[0] + p标签偏移[0]],
        y=[p初始[1] + p标签偏移[1]],
        z=[p初始[2] + p标签偏移[2]],
        mode="text",
        text=["p"],
        textposition="middle center",
        name="p 标签",
        showlegend=False,
        hovertemplate="p<br>坐标: (%{x:.3f}, %{y:.3f}, %{z:.3f})<extra></extra>",
    )
)

# u、v、w 张成的三角形。
三角形_trace索引 = len(fig.data)
fig.add_trace(
    go.Mesh3d(
        x=[u[0], v[0], w[0]],
        y=[u[1], v[1], w[1]],
        z=[u[2], v[2], w[2]],
        i=[0],
        j=[1],
        k=[2],
        name="三角形 u-v-w",
        opacity=0.35,
        color="#f2a900",
        visible=显示三角形,
        hovertemplate="三角形顶点<br>(%{x:.3f}, %{y:.3f}, %{z:.3f})<extra></extra>",
    )
)

# O、u、v、w 围成的四面体，共四个三角形面。
四面体_trace索引 = len(fig.data)
fig.add_trace(
    go.Mesh3d(
        x=[0, u[0], v[0], w[0]],
        y=[0, u[1], v[1], w[1]],
        z=[0, u[2], v[2], w[2]],
        i=[0, 0, 0, 1],
        j=[1, 1, 2, 2],
        k=[2, 3, 3, 3],
        name="四面体 O-u-v-w",
        opacity=0.18,
        color="#9467bd",
        visible=显示四面体,
        hovertemplate="四面体表面<br>(%{x:.3f}, %{y:.3f}, %{z:.3f})<extra></extra>",
    )
)

# 三角形的三条有向边。线段和文字分开，避免方向标签附着在顶点上。
三角形边_trace索引 = []
三角形法向 = np.cross(v - u, w - u)
三角形法向长度 = np.linalg.norm(三角形法向)
三角形尺度 = max(
    np.linalg.norm(v - u),
    np.linalg.norm(w - v),
    np.linalg.norm(u - w),
)
边标签偏移 = (
    0.06 * 三角形尺度 * 三角形法向 / 三角形法向长度
    if 三角形法向长度 > 1e-12
    else np.zeros(3)
)
for 起点名称, 终点名称, 起点, 终点, 方向名称 in (
    ("u", "v", u, v, "v-u"),
    ("v", "w", v, w, "w-v"),
    ("w", "u", w, u, "u-w"),
):
    边中点 = (起点 + 终点) / 2 + 边标签偏移
    边线_trace索引 = len(fig.data)
    三角形边_trace索引.append(边线_trace索引)
    fig.add_trace(
        go.Scatter3d(
            x=[起点[0], 终点[0]],
            y=[起点[1], 终点[1]],
            z=[起点[2], 终点[2]],
            mode="lines",
            name=f"{起点名称} -> {终点名称} ({方向名称})",
            showlegend=False,
            line=dict(color="#555555", width=5, dash="dash"),
            visible=显示三角形边,
            hovertemplate=(
                f"{方向名称}<br>起点: "
                f"({起点[0]:.3f}, {起点[1]:.3f}, {起点[2]:.3f})<br>"
                f"终点: ({终点[0]:.3f}, {终点[1]:.3f}, {终点[2]:.3f})"
                "<extra></extra>"
            ),
        )
    )
    标签_trace索引 = len(fig.data)
    三角形边_trace索引.append(标签_trace索引)
    fig.add_trace(
        go.Scatter3d(
            x=[边中点[0]],
            y=[边中点[1]],
            z=[边中点[2]],
            mode="text",
            text=[方向名称],
            textposition="middle center",
            name=f"{起点名称} -> {终点名称} ({方向名称}) 标签",
            showlegend=False,
            visible=显示三角形边,
            hovertemplate=(
                f"{方向名称}<br>方向: {起点名称} → {终点名称}"
                "<extra></extra>"
            ),
        )
    )

# c+d+e=1 的平面只显示有限片区，坐标范围仍完全由 YAML 控制。
参考平面_trace索引 = None
方向1 = v - u
方向2 = w - u
if np.linalg.norm(np.cross(方向1, 方向2)) > 1e-12:
    平面顶点 = np.array(
        [
            u - 0.5 * 方向1 - 0.5 * 方向2,
            u + 1.5 * 方向1 - 0.5 * 方向2,
            u + 1.5 * 方向1 + 1.5 * 方向2,
            u - 0.5 * 方向1 + 1.5 * 方向2,
        ]
    )
    参考平面_trace索引 = len(fig.data)
    fig.add_trace(
        go.Mesh3d(
            x=平面顶点[:, 0],
            y=平面顶点[:, 1],
            z=平面顶点[:, 2],
            i=[0, 0],
            j=[1, 2],
            k=[2, 3],
            name="c+d+e=1 参考平面",
            opacity=0.12,
            color="#17becf",
            visible=显示系数和为1参考平面,
            hovertemplate="c+d+e=1 参考平面<extra></extra>",
        )
    )

fig.update_layout(
    title=参数["标题"],
    scene=dict(
        xaxis=dict(title="x", range=x范围, autorange=False, showgrid=True),
        yaxis=dict(title="y", range=y范围, autorange=False, showgrid=True),
        zaxis=dict(title="z", range=z范围, autorange=False, showgrid=True),
        aspectmode="data",
        camera=dict(eye=dict(x=1.55, y=1.55, z=1.25)),
    ),
    width=1000,
    height=800,
    hovermode="closest",
    uirevision="三维向量线性组合实验",
    margin=dict(l=0, r=0, t=55, b=0),
)

plot_html = fig.to_html(
    full_html=False,
    include_plotlyjs=True,
    div_id="三维线性组合图",
)

索引参数 = {
    "p": p_trace索引,
    "pLabel": p标签_trace索引,
    "triangle": 三角形_trace索引,
    "tetrahedron": 四面体_trace索引,
    "edges": 三角形边_trace索引,
    "plane": 参考平面_trace索引,
}

控制面板 = f"""
<div style="font-family: sans-serif; max-width: 1000px; margin-bottom: 15px;">
    <div style="margin-bottom: 10px;">
        <label for="约束模式">约束模式：</label>
        <select id="约束模式">
            <option value="自由模式" {"selected" if 约束模式 == "自由模式" else ""}>自由模式</option>
            <option value="系数和 = 1" {"selected" if 约束模式 == "系数和 = 1" else ""}>系数和 = 1</option>
            <option value="三角形模式" {"selected" if 约束模式 == "三角形模式" else ""}>三角形模式</option>
            <option value="三棱锥模式" {"selected" if 约束模式 == "三棱锥模式" else ""}>三棱锥模式</option>
        </select>
    </div>

    <div><label>c = <span id="c值"></span></label>
        <input id="c滑块" type="range" min="{滑块最小值}" max="{滑块最大值}" step="{滑块步长}" value="{c初始}" style="width: 500px;"></div>
    <div><label>d = <span id="d值"></span></label>
        <input id="d滑块" type="range" min="{滑块最小值}" max="{滑块最大值}" step="{滑块步长}" value="{d初始}" style="width: 500px;"></div>
    <div><label>e = <span id="e值"></span></label>
        <input id="e滑块" type="range" min="{滑块最小值}" max="{滑块最大值}" step="{滑块步长}" value="{e初始}" style="width: 500px;"></div>

    <div style="margin-top: 10px;">
        <button type="button" data-c="0.3333333333" data-d="0.3333333333" data-e="0.3333333333">三角形重心</button>
        <button type="button" data-c="0.5" data-d="0" data-e="0.5">u 与 w 的中点</button>
        <button type="button" data-c="0.5" data-d="0.5" data-e="0.5">三个系数均为 1/2</button>
    </div>

    <div style="margin-top: 10px;">
        <label><input id="显示三角形" type="checkbox" {"checked" if 显示三角形 else ""}> 显示 u、v、w 三角形</label>
        <label><input id="显示四面体" type="checkbox" {"checked" if 显示四面体 else ""}> 显示 O、u、v、w 四面体</label>
        <label><input id="显示三角形边" type="checkbox" {"checked" if 显示三角形边 else ""}> 显示三角形有向边</label>
        <label><input id="显示参考平面" type="checkbox" {"checked" if 显示系数和为1参考平面 else ""}> 显示 c+d+e=1 参考平面</label>
    </div>

    <div style="margin-top: 10px;">
        c+d+e = <span id="系数和"></span><br>
        p = <span id="p值"></span>
    </div>
</div>
"""

v_json = json.dumps(v.tolist(), ensure_ascii=False)
w_json = json.dumps(w.tolist(), ensure_ascii=False)
u_json = json.dumps(u.tolist(), ensure_ascii=False)
索引_json = json.dumps(索引参数, ensure_ascii=False)
p标签偏移_json = json.dumps(p标签偏移.tolist(), ensure_ascii=False)

脚本 = f"""
<script>
const u = {u_json};
const v = {v_json};
const w = {w_json};
const p标签偏移 = {p标签偏移_json};
const 图 = document.getElementById("三维线性组合图");
const 索引 = {索引_json};

const c滑块 = document.getElementById("c滑块");
const d滑块 = document.getElementById("d滑块");
const e滑块 = document.getElementById("e滑块");
const c值 = document.getElementById("c值");
const d值 = document.getElementById("d值");
const e值 = document.getElementById("e值");
const 系数和 = document.getElementById("系数和");
const p值 = document.getElementById("p值");
const 约束模式 = document.getElementById("约束模式");

function 限制(value, minimum, maximum) {{
    return Math.max(minimum, Math.min(maximum, value));
}}

function 应用约束(来源) {{
    let c = parseFloat(c滑块.value);
    let d = parseFloat(d滑块.value);
    let e = parseFloat(e滑块.value);
    const 模式 = 约束模式.value;

    if (模式 === "系数和 = 1") {{
        if (来源 === "e") {{
            c = 1 - d - e;
        }} else {{
            e = 1 - c - d;
        }}
    }} else if (模式 === "三角形模式") {{
        c = 限制(c, 0, 1);
        d = 限制(d, 0, 1 - c);
        e = 1 - c - d;
    }} else if (模式 === "三棱锥模式") {{
        c = 限制(c, 0, 1);
        d = 限制(d, 0, 1 - c);
        e = 限制(e, 0, 1 - c - d);
    }}

    c滑块.value = c;
    d滑块.value = d;
    e滑块.value = e;
    return [c, d, e];
}}

function 更新图像(来源) {{
    const [c, d, e] = 应用约束(来源);
    const px = c * u[0] + d * v[0] + e * w[0];
    const py = c * u[1] + d * v[1] + e * w[1];
    const pz = c * u[2] + d * v[2] + e * w[2];

    c值.textContent = c.toFixed(3);
    d值.textContent = d.toFixed(3);
    e值.textContent = e.toFixed(3);
    系数和.textContent = (c + d + e).toFixed(3);
    p值.textContent = "(" + px.toFixed(3) + ", " + py.toFixed(3) + ", " + pz.toFixed(3) + ")";

    Plotly.restyle(图, {{x: [[0, px]], y: [[0, py]], z: [[0, pz]]}}, [索引.p]);
    Plotly.restyle(图, {{
        x: [[px + p标签偏移[0]]],
        y: [[py + p标签偏移[1]]],
        z: [[pz + p标签偏移[2]]],
    }}, [索引.pLabel]);
}}

function 设置显示(元素, trace索引) {{
    if (trace索引 !== null && trace索引 !== undefined) {{
        Plotly.restyle(图, {{visible: 元素.checked}}, [trace索引]);
    }}
}}

c滑块.addEventListener("input", () => 更新图像("c"));
d滑块.addEventListener("input", () => 更新图像("d"));
e滑块.addEventListener("input", () => 更新图像("e"));
约束模式.addEventListener("change", () => 更新图像("模式"));

document.getElementById("显示三角形").addEventListener("change", (event) => 设置显示(event.target, 索引.triangle));
document.getElementById("显示四面体").addEventListener("change", (event) => 设置显示(event.target, 索引.tetrahedron));
document.getElementById("显示三角形边").addEventListener("change", (event) => {{
    索引.edges.forEach((trace索引) => 设置显示(event.target, trace索引));
}});
document.getElementById("显示参考平面").addEventListener("change", (event) => 设置显示(event.target, 索引.plane));

document.querySelectorAll("button[data-c]").forEach((按钮) => {{
    按钮.addEventListener("click", () => {{
        c滑块.value = 按钮.dataset.c;
        d滑块.value = 按钮.dataset.d;
        e滑块.value = 按钮.dataset.e;
        更新图像("预设");
    }});
}});

更新图像("初始化");
</script>
"""

完整_html = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>{参数["标题"]}</title>
</head>
<body>
{控制面板}
{plot_html}
{脚本}
</body>
</html>
"""

输出路径.write_text(完整_html, encoding="utf-8")
print(f"已生成：{输出路径}")
