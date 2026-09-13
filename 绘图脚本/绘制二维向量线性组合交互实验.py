import json
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
import yaml

参数路径 = Path("图像参数/二维向量线性组合交互实验.yaml")

with 参数路径.open("r", encoding="utf-8") as f:
    参数 = yaml.safe_load(f)


def 必需参数(配置, 键名):
    if 键名 not in 配置:
        raise ValueError(f"YAML 缺少核心参数：{键名}")
    return 配置[键名]


向量参数 = 必需参数(参数, "向量")
v = np.array(必需参数(向量参数, "v"), dtype=float)
w = np.array(必需参数(向量参数, "w"), dtype=float)

if v.shape != (2,) or w.shape != (2,):
    raise ValueError("核心参数 v 和 w 必须是包含两个数值的二维向量")

c初始 = float(参数["初始系数"]["c"])
d初始 = float(参数["初始系数"]["d"])

滑块最小值 = float(参数["滑块"]["最小值"])
滑块最大值 = float(参数["滑块"]["最大值"])
滑块步长 = float(参数["滑块"]["步长"])

x范围 = 参数["坐标范围"]["x"]
y范围 = 参数["坐标范围"]["y"]

显示参数 = 参数.get("显示", {})
显示参考直线 = bool(显示参数.get("显示参考直线", True))
显示辅助平行四边形 = bool(
    显示参数.get("显示辅助平行四边形", False)
)

默认锁定 = bool(
    显示参数.get("默认锁定系数和为1", False)
)

参考直线参数 = 参数.get("参考直线", {})
参考直线最小值 = float(参考直线参数.get("参数最小值", -0.5))
参考直线最大值 = float(参考直线参数.get("参数最大值", 1.5))

输出路径 = Path(参数["输出"]["html"])
输出路径.parent.mkdir(parents=True, exist_ok=True)


def 计算线性组合(c, d):
    return c * v + d * w


u初始 = 计算线性组合(c初始, d初始)


fig = go.Figure()


# -------------------------
# v
# -------------------------

fig.add_trace(
    go.Scatter(
        x=[0, v[0]],
        y=[0, v[1]],
        mode="lines+markers+text",
        text=["", "v"],
        textposition="top center",
        name="v",
    )
)


# -------------------------
# w
# -------------------------

fig.add_trace(
    go.Scatter(
        x=[0, w[0]],
        y=[0, w[1]],
        mode="lines+markers+text",
        text=["", "w"],
        textposition="top center",
        name="w",
    )
)


# -------------------------
# u = cv + dw
# 注意：这是第 3 个 trace
# JavaScript 会实时修改它
# -------------------------

fig.add_trace(
    go.Scatter(
        x=[0, u初始[0]],
        y=[0, u初始[1]],
        mode="lines+markers+text",
        text=["", "u"],
        textposition="top center",
        name="u = cv + dw",
        line=dict(width=4),
    )
)


# -------------------------
# v 与 w 的连线
# 用来观察 c+d=1 时的规律
# -------------------------

if 显示参考直线:
    方向 = v - w

    t = np.linspace(
        参考直线最小值,
        参考直线最大值,
        200,
    )

    直线 = (
        w[:, np.newaxis]
        + 方向[:, np.newaxis] * t
    )

    fig.add_trace(
        go.Scatter(
            x=直线[0],
            y=直线[1],
            mode="lines",
            name="v、w 所在直线",
            line=dict(dash="dash"),
        )
    )


# -------------------------
# 辅助平行四边形
# 初始值先画出来
# 后面 JavaScript 动态更新
# -------------------------

辅助线_trace索引 = None

if 显示辅助平行四边形:

    cv = c初始 * v
    dw = d初始 * w

    辅助线_trace索引 = len(fig.data)

    fig.add_trace(
        go.Scatter(
            x=[
                0,
                cv[0],
                u初始[0],
                dw[0],
                0,
            ],
            y=[
                0,
                cv[1],
                u初始[1],
                dw[1],
                0,
            ],
            mode="lines",
            name="辅助平行四边形",
            line=dict(dash="dot"),
        )
    )

fig.update_layout(
    title=参数["标题"],

    xaxis=dict(
        title="x",
        range=x范围,
        autorange=False,
        zeroline=True,
        zerolinecolor="#333333",
        zerolinewidth=2.5,
        showline=True,
        linecolor="#333333",
        showgrid=True,
        constrain="domain",
    ),

    yaxis=dict(
        title="y",
        range=y范围,
        autorange=False,
        zeroline=True,
        zerolinecolor="#333333",
        zerolinewidth=2.5,
        showline=True,
        linecolor="#333333",
        showgrid=True,
        scaleanchor="x",
        scaleratio=1,
    ),

    width=900,
    height=750,
    hovermode="closest",
    uirevision="二维向量线性组合实验",
)

# -------------------------
# 生成 Plotly 主体 HTML
# -------------------------
plot_html = fig.to_html(
    full_html=False,
    include_plotlyjs=True,
    div_id="线性组合图",
)

# -------------------------
# 把 Python 参数传给 JavaScript
# -------------------------

v_json = json.dumps(v.tolist())
w_json = json.dumps(w.tolist())

辅助索引_json = (
    "null"
    if 辅助线_trace索引 is None
    else str(辅助线_trace索引)
)


# -------------------------
# 自定义交互控件
# -------------------------

控制面板 = f"""
<div style="
    font-family: sans-serif;
    max-width: 900px;
    margin-bottom: 15px;
">

    <div>
        <label>
            c =
            <span id="c值">{c初始}</span>
        </label>

        <input
            id="c滑块"
            type="range"
            min="{滑块最小值}"
            max="{滑块最大值}"
            step="{滑块步长}"
            value="{c初始}"
            style="width: 500px;"
        >
    </div>

    <div>
        <label>
            d =
            <span id="d值">{d初始}</span>
        </label>

        <input
            id="d滑块"
            type="range"
            min="{滑块最小值}"
            max="{滑块最大值}"
            step="{滑块步长}"
            value="{d初始}"
            style="width: 500px;"
        >
    </div>

    <div style="margin-top: 10px;">

        <label>
            <input
                id="锁定"
                type="checkbox"
                {"checked" if 默认锁定 else ""}
            >
            锁定 c + d = 1
        </label>

    </div>

    <div style="margin-top: 10px;">

        c + d =
        <span id="系数和"></span>

        <br>

        u =
        <span id="u值"></span>

    </div>

</div>
"""


脚本 = f"""
<script>

const v = {v_json};
const w = {w_json};

const 图 = document.getElementById("线性组合图");

const c滑块 = document.getElementById("c滑块");
const d滑块 = document.getElementById("d滑块");

const c值 = document.getElementById("c值");
const d值 = document.getElementById("d值");

const 系数和 = document.getElementById("系数和");
const u值 = document.getElementById("u值");

const 锁定 = document.getElementById("锁定");

const 辅助线索引 = {辅助索引_json};


function 更新图像(改变来源) {{

    let c = parseFloat(c滑块.value);
    let d = parseFloat(d滑块.value);


    // -------------------------
    // 如果锁定 c+d=1
    // 改 c 时自动调整 d
    // 改 d 时自动调整 c
    // -------------------------

    if (锁定.checked) {{

        if (改变来源 === "c") {{

            d = 1 - c;
            d滑块.value = d;

        }} else if (改变来源 === "d") {{

            c = 1 - d;
            c滑块.value = c;

        }} else {{

            d = 1 - c;
            d滑块.value = d;
        }}
    }}


    const ux =
        c * v[0]
        + d * w[0];

    const uy =
        c * v[1]
        + d * w[1];


    c值.textContent = c.toFixed(2);
    d值.textContent = d.toFixed(2);

    系数和.textContent =
        (c + d).toFixed(2);

    u值.textContent =
        "("
        + ux.toFixed(3)
        + ", "
        + uy.toFixed(3)
        + ")";


    // -------------------------
    // 更新 u
    // trace 2
    // -------------------------

    Plotly.restyle(
        图,
        {{
            x: [[0, ux]],
            y: [[0, uy]]
        }},
        [2]
    );


    // -------------------------
    // 更新辅助平行四边形
    // -------------------------

    if (辅助线索引 !== null) {{

        const cvx = c * v[0];
        const cvy = c * v[1];

        const dwx = d * w[0];
        const dwy = d * w[1];

        Plotly.restyle(
            图,
            {{
                x: [[
                    0,
                    cvx,
                    ux,
                    dwx,
                    0
                ]],

                y: [[
                    0,
                    cvy,
                    uy,
                    dwy,
                    0
                ]]
            }},
            [辅助线索引]
        );
    }}
}}


c滑块.addEventListener(
    "input",
    () => 更新图像("c")
);

d滑块.addEventListener(
    "input",
    () => 更新图像("d")
);

锁定.addEventListener(
    "change",
    () => 更新图像("锁定")
);


更新图像("初始化");

</script>
"""


完整_html = f"""
<!DOCTYPE html>

<html lang="zh-CN">

<head>

<meta charset="UTF-8">

<title>
{参数["标题"]}
</title>

</head>

<body>

{控制面板}

{plot_html}

{脚本}

</body>

</html>
"""


输出路径.write_text(
    完整_html,
    encoding="utf-8",
)

print(
    f"已生成：{输出路径}"
)
