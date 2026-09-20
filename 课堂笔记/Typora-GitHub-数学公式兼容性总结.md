# Typora 1.13.6 与 GitHub 数学公式兼容性总结

本文依据当前实测结果整理，只记录已经能够被 GitHub 正常识别和渲染的写法。

项目目标不是要求 Typora 与 GitHub 在字体、颜色、间距等视觉细节上完全一致，而是保证同一份 Markdown 在两边表达相同的数学内容。

---

## 一、行内公式

GitHub 可以正常识别普通行内数学公式：

```markdown
$Ax=b$
```

例如：

$Ax=b$

上下标、分式、根号、希腊字母、集合符号等常见写法也可以正常使用：

```markdown
$a_{ij},\quad x_1,\quad x_n,\quad \lambda^2$
```

```markdown
$\frac{a+b}{c},\quad \sqrt{x^2+y^2}$
```

```markdown
$\alpha,\beta,\gamma,\lambda,\mu,\pi$
```

```markdown
$x\in\mathbb{R}^n,\quad A\subseteq B,\quad x\neq 0$
```

---

## 二、块级公式

对于正式笔记，优先使用 GitHub 风格的 `math` 代码块。

````markdown
```math
Ax=b
```
````

GitHub 与 Typora 1.13.6 都能够正常渲染。

复杂矩阵同样可以直接放入 `math` 代码块：

````markdown
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
````

当前项目建议把这种写法作为块级数学公式的默认形式。

---

## 三、矩阵环境

以下矩阵环境已经实测可以正常渲染。

### `bmatrix`

````markdown
```math
\begin{bmatrix}
1 & 2\\
3 & 4
\end{bmatrix}
```
````

### `pmatrix`

````markdown
```math
\begin{pmatrix}
1 & 2\\
3 & 4
\end{pmatrix}
```
````

### `vmatrix`

````markdown
```math
\begin{vmatrix}
1 & 2\\
3 & 4
\end{vmatrix}
```
````

### `matrix`

````markdown
```math
\begin{matrix}
1 & 2\\
3 & 4
\end{matrix}
```
````

---

## 四、多行公式

### `aligned`

````markdown
```math
\begin{aligned}
x+y &= 3\\
2x-y &= 0
\end{aligned}
```
````

### `cases`

````markdown
```math
f(x)=
\begin{cases}
x^2, & x\ge 0\\
-x, & x<0
\end{cases}
```
````

这两种环境均可正常用于多行方程、分段函数等内容。

---

## 五、线性代数常用数学命令

以下写法已经能够在 GitHub 中正常识别。

### 行列式

```markdown
$\det(A)$
```

### 核

```markdown
$\ker(A)$
```

### 实数空间

```markdown
$\mathbb{R}^n$
```

### 粗体向量

```markdown
$\mathbf{x}$
```

### 转置

```markdown
$A^T$
```

### 逆矩阵

```markdown
$A^{-1}$
```

### 范数

```markdown
$\lVert x\rVert$
```

### 内积

```markdown
$\langle x,y\rangle$
```

### 求和

```markdown
$\sum_{i=1}^{n}c_i v_i$
```

### 线性组合

```markdown
$p=c_1v_1+\cdots+c_nv_n$
```

---

## 六、文字与字体命令

以下写法可以正常使用。

### `\text{}`

````markdown
```math
x=0\quad \text{或}\quad x=1
```
````

### `\mathrm{}`

````markdown
```math
\mathrm{rank}(A)
```
````

### `\mathbf{}`

````markdown
```math
\mathbf{x}
```
````

### `\mathbb{}`

````markdown
```math
\mathbb{R}^3
```
````

---

## 七、`span` 的兼容写法

当前实测中，下面两种写法能够在 GitHub 和 Typora 1.13.6 中正常渲染。

### 简单直立字体

````markdown
```math
\mathrm{span}(v_1,\ldots,v_n)
```
````

### 按数学算子处理

````markdown
```math
\mathop{\mathrm{span}}(v_1,\ldots,v_n)
```
````

对于正式线性代数笔记，优先采用第二种，因为它在语义上更接近“数学算子”。

---

## 八、特殊符号

以下内容已经可以正常使用：

```markdown
$v_1,\quad v_{10}$
```

```markdown
$\{x\in\mathbb{R}:x>0\}$
```

```markdown
$v_1,v_2,\ldots,v_n$
```

多行公式中的换行也可以正常工作：

````markdown
```math
\begin{aligned}
a&=b+c\\
d&=e+f
\end{aligned}
```
````

---

## 九、Markdown 结构中嵌入公式

### 列表

```markdown
- 第一项：$Ax=b$
- 第二项：$\det(A)\neq 0$
- 第三项：$\mathbb{R}^n$
```

### 引用

```markdown
> 若 $\det(A)\neq 0$，则 $A$ 可逆。
```

### 表格

```markdown
| 对象 | 数学表达 |
|---|---|
| 矩阵方程 | $Ax=b$ |
| 行列式 | $\det(A)$ |
| 核 | $\ker(A)$ |
| 实数空间 | $\mathbb{R}^n$ |
```

这些组合在 GitHub 中均能够正常显示。

---

## 十、复杂矩阵

较大的矩阵同样可以正常放入 `math` 代码块：

````markdown
```math
A=
\begin{bmatrix}
a_{11} & a_{12} & \cdots & a_{1n}\\
a_{21} & a_{22} & \cdots & a_{2n}\\
\vdots & \vdots & \ddots & \vdots\\
a_{m1} & a_{m2} & \cdots & a_{mn}
\end{bmatrix}
```
````

---

## 十一、当前项目建议

根据本轮实测，`linear-algebra-notes` 暂定采用以下规则：

1. 行内公式使用 `$...$`。
2. 块级公式优先使用 GitHub 风格的 `math` 代码块。
3. 矩阵、多行方程、分段函数等复杂内容统一放入 `math` 代码块。
4. `span` 优先写成 `\mathop{\mathrm{span}}(...)`。
5. 只使用已经在 Typora 1.13.6 和 GitHub 中共同验证通过的数学命令。
6. GitHub 作为最终渲染验收标准，Typora 作为本地编辑与预览工具。

---

## 十二、已知不兼容情况

当前测试中已经确认存在两类兼容问题：

- 某些 MathJax 命令在 Typora 中可以使用，但 GitHub 会主动禁止。
- 使用传统块级数学定界符时，个别包含 Markdown 特殊字符的复杂公式可能被 GitHub 的 Markdown 解析层干扰。

因此正式笔记不采用这些存在已知兼容风险的写法。
