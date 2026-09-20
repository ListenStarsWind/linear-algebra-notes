# Typora 1.13.6 与 GitHub 数学公式书写规范

本文记录 `linear-algebra-notes` 当前已经实际验证可用的 Markdown / 数学公式写法。

目标不是让 Typora 与 GitHub 在字体、颜色、间距等视觉细节上完全一致，而是保证：

> 同一份 Markdown 在 Typora 1.13.6 和 GitHub 中都能稳定表达相同的数学内容。

GitHub 作为最终渲染验收标准，Typora 作为本地编辑与预览工具。

---

## 一、行内公式

正文中的行内公式使用：

```markdown
$...$
```

例如：

```markdown
矩阵方程写成 $Ax=b$ 。
```

实际效果：

矩阵方程写成 $Ax=b$ 。

### 中文正文中的空格约定

为了让 GitHub 稳定识别行内数学公式，正文中统一让公式与前后中文文本之间保留一个半角空格。

推荐：

```markdown
当 $c+d=1$ 时，点 $p$ 位于对应的仿射空间中。
```

标题中如果包含公式，也采用同样规则：

```markdown
## 一个很容易误判的例子： $\frac12(u+v+w)$
```

因此，本项目统一采用下面这种形式：

```text
中文文字 + 半角空格 + $公式$ + 半角空格 + 中文文字
```

如果公式本身位于句首、表格单元格开头等位置，则不需要额外补前导空格。

---

## 二、块级公式

正式笔记中的块级公式统一优先使用 GitHub 风格的 `math` fenced block。

写法：

````markdown
```math
Ax=b
```
````

实际效果：

```math
Ax=b
```

对于矩阵、多行方程、分段函数、较长推导等内容，也统一使用这种形式。

例如：

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

实际效果：

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

当前项目中，块级数学公式默认采用 `math` fenced block，不再把 `$$ ... $$` 作为正式规范。

---

## 三、矩阵环境

以下矩阵环境已经在 Typora 1.13.6 与 GitHub 中验证可用。

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
x^2, & x\ge0\\
-x, & x<0
\end{cases}
```
````

这两种环境可以正常用于联立方程、分段函数以及需要对齐的多行推导。

---

## 五、线性代数常用写法

以下写法已经可以正常用于当前笔记。

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

以下命令已经验证可用。

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

## 七、`span` 的统一写法

当前项目中的 `span` 统一写成：

````markdown
```math
\mathop{\mathrm{span}}(v_1,\ldots,v_n)
```
````

实际效果：

```math
\mathop{\mathrm{span}}(v_1,\ldots,v_n)
```

行内形式同理：

```markdown
$\mathop{\mathrm{span}}(u,v)$
```

例如：

```markdown
两个向量生成的平面记作 $\mathop{\mathrm{span}}(u,v)$ 。
```

---

## 八、特殊符号

以下写法已经可以正常使用。

### 下标

```markdown
$v_1,\quad v_{10}$
```

### 集合

```markdown
$\{x\in\mathbb{R}:x>0\}$
```

### 省略号

```markdown
$v_1,v_2,\ldots,v_n$
```

### 多行换行

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
- 第一项： $Ax=b$
- 第二项： $\det(A)\neq0$
- 第三项： $\mathbb{R}^n$
```

### 引用

```markdown
> 若 $\det(A)\neq0$ ，则 $A$ 可逆。
```

### 表格

表格中使用行内公式：

```markdown
| 对象 | 数学表达 |
|---|---|
| 矩阵方程 | $Ax=b$ |
| 行列式 | $\det(A)$ |
| 核 | $\ker(A)$ |
| 实数空间 | $\mathbb{R}^n$ |
```

表格单元格中不使用块级数学公式。

---

## 十、复杂矩阵

较大的矩阵继续使用 `math` fenced block。

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

实际效果：

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

## 十一、项目统一规则

当前 `linear-algebra-notes` 统一采用以下约定：

1. 行内公式使用 `$...$`。
2. 行内公式与前后中文正文之间保留一个半角空格。
3. 标题中出现行内公式时，同样遵守空格规则。
4. 块级公式统一优先使用 `math` fenced block。
5. 矩阵、多行方程、分段函数和较长推导全部使用 `math` fenced block。
6. `span` 统一写成 `\mathop{\mathrm{span}}(...)`。
7. 表格中只使用行内公式。
8. GitHub 作为最终渲染验收标准。
9. Typora 主题只负责本地视觉效果，不作为 Markdown 兼容性的判断依据。

---

## 十二、写作时的简单判断方法

写正文时：

```markdown
文字 $公式$ 文字
```

写独立公式时：

````markdown
```math
公式
```
````

写矩阵或多行推导时：

````markdown
```math
\begin{aligned}
...
\end{aligned}
```
````

只要优先遵循这三种形式，当前线性代数笔记中绝大多数数学内容都可以稳定地同时在 Typora 1.13.6 和 GitHub 中显示。
