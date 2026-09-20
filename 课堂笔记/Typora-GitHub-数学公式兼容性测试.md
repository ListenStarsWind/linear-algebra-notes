# Typora 1.13.6 与 GitHub 数学公式兼容性测试

> 目的：确认本项目中哪些 Markdown / LaTeX 数学语法能够同时被 Typora 1.13.6 与 GitHub 正常渲染。
>
> 测试原则：以 GitHub 网页最终显示效果为准。Typora 中正常但 GitHub 异常的语法，不纳入项目公共子集。

---

## 一、基础行内公式

普通行内公式：

$Ax=b$

带上下标：

$a_{ij},\quad x_1,\quad x_n,\quad \lambda^2$

分式与根号：

$\frac{a+b}{c},\quad \sqrt{x^2+y^2}$

希腊字母：

$\alpha,\beta,\gamma,\lambda,\mu,\pi$

向量：

$\mathbf{v},\quad \vec{v},\quad \boldsymbol{x}$

集合与关系：

$x\in\mathbb{R}^n,\quad A\subseteq B,\quad x\neq 0$

---

## 二、`$$ ... $$` 块公式

$$
Ax=b
$$

矩阵：

$$
\begin{bmatrix}
2 & -1\\
-1 & 2
\end{bmatrix}
\begin{bmatrix}
x\\
y
\end{bmatrix}
=
\begin{bmatrix}
0\\
3
\end{bmatrix}
$$

---

## 三、GitHub 风格 `math` 代码块

```math
Ax=b
```

```math
\begin{bmatrix}
2 & -1\\
-1 & 2
\end{bmatrix}
\begin{bmatrix}
x\\
y
\end{bmatrix}
=
\begin{bmatrix}
0\\
3
\end{bmatrix}
```

---

## 四、常见矩阵环境

`bmatrix`：

$$
\begin{bmatrix}
1 & 2\\
3 & 4
\end{bmatrix}
$$

`pmatrix`：

$$
\begin{pmatrix}
1 & 2\\
3 & 4
\end{pmatrix}
$$

`vmatrix`：

$$
\begin{vmatrix}
1 & 2\\
3 & 4
\end{vmatrix}
$$

`matrix`：

$$
\begin{matrix}
1 & 2\\
3 & 4
\end{matrix}
$$

---

## 五、多行公式环境

`aligned`：

$$
\begin{aligned}
x+y &= 3\\
2x-y &= 0
\end{aligned}
$$

`cases`：

$$
f(x)=
\begin{cases}
x^2, & x\ge 0\\
-x, & x<0
\end{cases}
$$

---

## 六、线性代数高频写法

行列式：

$$
\det(A)
$$

核：

$$
\ker(A)
$$

实数空间：

$$
\mathbb{R}^n
$$

粗体向量：

$$
\mathbf{x}
$$

转置：

$$
A^T
$$

逆矩阵：

$$
A^{-1}
$$

范数：

$$
\lVert x\rVert
$$

内积：

$$
\langle x,y\rangle
$$

求和：

$$
\sum_{i=1}^{n} c_i v_i
$$

线性组合：

$$
p=c_1v_1+\cdots+c_nv_n
$$

---

## 七、`span` 相关兼容性测试

### 7.1 已知风险：`\operatorname`

$$
\operatorname{span}(v_1,\ldots,v_n)
$$

```math
\operatorname{span}(v_1,\ldots,v_n)
```

### 7.2 `\mathrm`

$$
\mathrm{span}(v_1,\ldots,v_n)
$$

```math
\mathrm{span}(v_1,\ldots,v_n)
```

### 7.3 `\mathop`

$$
\mathop{\mathrm{span}}(v_1,\ldots,v_n)
$$

```math
\mathop{\mathrm{span}}(v_1,\ldots,v_n)
```

---

## 八、文字类命令

`\text{}`：

$$
x=0\quad \text{或}\quad x=1
$$

`\mathrm{}`：

$$
\mathrm{rank}(A)
$$

`\mathbf{}`：

$$
\mathbf{x}
$$

`\mathbb{}`：

$$
\mathbb{R}^3
$$

---

## 九、特殊符号与容易冲突的字符

下划线：

$$
v_1,\quad v_{10}
$$

星号：

$$
A^*,\quad x*y
$$

花括号：

$$
\{x\in\mathbb{R}:x>0\}
$$

反斜杠换行：

$$
\begin{aligned}
a&=b+c\\
d&=e+f
\end{aligned}
$$

省略号：

$$
v_1,v_2,\ldots,v_n
$$

---

## 十、Markdown 结构中嵌入公式

### 列表

- 第一项：$Ax=b$
- 第二项：$\det(A)\neq 0$
- 第三项：$\mathbb{R}^n$

### 引用

> 若 $\det(A)\neq 0$，则 $A$ 可逆。

### 表格

| 对象 | 数学表达 |
|---|---|
| 矩阵方程 | $Ax=b$ |
| 行列式 | $\det(A)$ |
| 核 | $\ker(A)$ |
| 实数空间 | $\mathbb{R}^n$ |

---

## 十一、较复杂的组合测试

$$
A=
\begin{bmatrix}
a_{11} & a_{12} & \cdots & a_{1n}\\
a_{21} & a_{22} & \cdots & a_{2n}\\
\vdots & \vdots & \ddots & \vdots\\
a_{m1} & a_{m2} & \cdots & a_{mn}
\end{bmatrix}
$$

```math
A=
\begin{bmatrix}
a_{11} & a_{12} & \cdots & a_{1n}\\
a_{21} & a_{22} & \cdots & a_{2n}\\
\vdots & \vdots & \ddots & \vdots\\
a_{m1} & a_{m2} & \cdots & a_{mn}
\end{bmatrix}
```

---

## 十二、测试结果记录

建议分别在 Typora 1.13.6 与 GitHub 中检查，并填写：

| 测试项 | Typora 1.13.6 | GitHub | 是否纳入项目公共子集 | 备注 |
|---|---|---|---|---|
| `$...$` 行内公式 |  |  |  |  |
| `$$...$$` 块公式 |  |  |  |  |
| `math` 代码块 |  |  |  |  |
| `bmatrix` |  |  |  |  |
| `pmatrix` |  |  |  |  |
| `vmatrix` |  |  |  |  |
| `aligned` |  |  |  |  |
| `cases` |  |  |  |  |
| `\det` |  |  |  |  |
| `\ker` |  |  |  |  |
| `\mathbb` |  |  |  |  |
| `\mathbf` |  |  |  |  |
| `\text` |  |  |  |  |
| `\mathrm` |  |  |  |  |
| `\operatorname` |  |  |  |  |
| `\mathop{\mathrm{span}}` |  |  |  |  |
| 列表内公式 |  |  |  |  |
| 引用内公式 |  |  |  |  |
| 表格内公式 |  |  |  |  |

---

## 十三、最终采用规则

完成测试后，只保留 Typora 与 GitHub 都能稳定渲染的语法。

若两者表现不一致：

1. GitHub 正常、Typora 异常：优先调整 Typora。
2. Typora 正常、GitHub 异常：更换公式写法。
3. 两种写法效果相同：优先选择结构更清晰、对 GitHub 更稳定的写法。
