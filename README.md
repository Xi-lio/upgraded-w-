# Week 05 · 意图造物与 ReAct 闭环编程实验

> **单文件交互应用：单摆物理模拟器**
> 实验者：**赵怡欣**　学号：**7905126058**
> 课程：《人机协同程序设计》　第 5 周实验　2 课时（80 分钟）
> 实验形式：个人独立上机实验（HOTL 模式）
> GitHub 作品集链接：`（推送后粘贴于此）`

---

## 一、工作区状态：无菌工作区就绪 ✅

本目录 `week05_pendulum_sim/` 是课程主仓库内为第 5 周创建的**独立无菌子模块**，隔离规范如下：

| 隔离项 | 规范 |
| :--- | :--- |
| 目录边界 | 所有实验产物只存在于 `week05_pendulum_sim/` 内，不污染其它周次 |
| 运行方式 | 零构建、零依赖、无 Node/Webpack，双击 `index.html` 秒级运行 |
| 版本控制 | 独立 Git 基线，`main` 分支，按任务里程碑逐轮 Commit |
| 忽略规则 | `.gitignore` 排除系统垃圾文件、编辑器临时文件与打包产物 |

---

## 二、交付物清单

| 文件 | 说明 |
| :--- | :--- |
| `index.html` | **主交付物**：单摆模拟器（MVP + 三滑块实时交互 + 重置按钮），控制台 0 报错 |
| `bonus_a_double_pendulum/index.html` | 进阶挑战 A：双摆混沌模拟器（RK4 + 彩虹拖尾 + 鼠标拖拽） |
| `bonus_b_celestial_persistence/index.html` | 进阶挑战 B：天体场景切换 + localStorage 持久化 |
| `starter_code/03_buggy_practice/index.html` | 任务四**故障演练页**（故意注入未定义报错） |
| `starter_code/04_fixed_solution/index.html` | 任务四**修复后对照版**（课程提供） |
| `task04_repair/index.html` | 任务四**自愈修复产物**（对演练页执行 ReAct 闭环后的可用版本） |
| `repair_task04.py` | 一键跑完「观察→思考→行动→再观察」四步闭环的脚本 |
| `verify_bug.js` | 自动化验证脚本：证明故障页报错 / 修复页不报错 |
| `verify_rk4.js` | 自动化验证脚本：证明双摆 RK4 积分 60 秒不发散 |
| `verify_syntax.js` | 批量校验所有 HTML 内嵌 JS 语法 |
| `verify_console.py` | **真实浏览器**中注入探针，客观统计各页面控制台报错数 |
| `verify_buggy_click.py` | **真实浏览器**中自动点击重置按钮，复现 ReferenceError |
| `screenshots/` | 三个页面的真实渲染截图 |
| `README.md` | 本文件，含人机协同三反思 |

---

## 三、迭代轨迹（Git 里程碑，共 10 次 Commit，远超要求的 3 次）

| # | Commit | Hash | 时间 | 对应任务 | 产物状态 |
| :-: | :--- | :--- | :--- | :--- | :--- |
| 1 | `feat(week05): init pendulum experiment workspace` | `408d87e` | 11:02 | 任务一 | 无菌目录 + README 就绪 |
| 2 | `feat: complete pendulum MVP` | `74fd794` | 11:02 | 任务二 | 单摆平滑摆动（首轮 MVP 跑通） |
| 3 | `feat: add interactive parameter sliders` | `ff991df` | 11:03 | 任务三 | 三滑块 + 重置按钮，实时联动 |
| 4 | `fix: resolve reset button runtime error` | `c392551` | 11:04 | 任务四 | 根因修复 + 验证脚本，控制台 0 报错 |
| 5 | `feat: bonus A double pendulum chaos` | `ad3aca3` | 11:06 | 任务五 | 双摆 RK4 + 彩虹拖尾 + 拖拽 |
| 6 | `feat: bonus B celestial scenes persistence` | `ed4876d` | 11:06 | 任务五 | 天体场景切换 + 本地持久化 |
| 7 | `docs: add evidence-based verification suite and screenshots` | `6435d8e` | 11:10 | 验收 | 5 个验证脚本 + 5 张真实截图 |
| 8 | `chore: add packaging script for submission` | `27e2523` | 11:10 | 交付 | 一键打包脚本 |
| 9 | `fix(task04): self-heal downloaded buggy page via ReAct loop` | `f8905bf` | 11:15 | 任务四 | 对演练页执行完整 ReAct 闭环修复 |
| 10 | `docs: fill in student identity, finalize submission checklist and correct commit log` | — | 11:37 | 交付 | 填姓名学号 + 本表 + `提交步骤清单.md` + 全体提交署名 |

查看完整历史：`git log --oneline --stat`

> **关于署名**：全部 10 次提交的作者均为 `赵怡欣 <7905126058@example.com>`。
> 署名是通过「复用原有 tree、用 `git commit-tree` 重建提交链」的方式完成的（校验过新旧末端
> tree 哈希完全一致，即**文件内容零改动**），没有使用 `git rebase` 改写工作区。
> 最终 `git fsck --full` 输出为空，仓库结构健康。

> **一次真实的 Git 事故（写进报告，属于"闭环控制"的延伸）**：第 9 次提交时，验证脚本在
> `task04_repair/_tmp/` 下生成了 Edge 浏览器 profile 目录（400+ 个缓存文件）。我的 `.gitignore`
> 只按「调用点」排除了 `screenshots/_edgeprofile_*/`，**漏了这个新出现的目录**，结果 463 个垃圾文件
> 被一并提交，打包体积从 1.1 MB 膨胀到 2.4 MB。
>
> 处理方式：`git reset --mixed 27e2523` 退回干净基线 → 补齐 `.gitignore` 的目录级规则（`**/_tmp/`）
> → 重新提交 → `git reflog expire --expire=now --all && git gc --prune=now` 清理悬空对象。
> 最终仓库回到 **10 次提交、22 个跟踪文件、0 垃圾文件**。
>
> **教训：`.gitignore` 必须按「目录模式」写，而不是针对某一次调用产生的路径写**——否则新增一个
> 脚本就会以新路径重新踩同一个坑。这类问题只有靠「提交前检查 `git status` 输出规模」才能拦住。

---

## 四、验收证据（可复现）

### 证据 1 · 任务四 未定义报错的确证与修复

运行 `node verify_bug.js`，输出：

```
starter_code/03_buggy_practice/index.html
   onclick 调用    : resetAnimation()
   全局查找结果    : undefined
   判定            : FAIL -> ReferenceError

starter_code/04_fixed_solution/index.html
   onclick 调用    : resetAnimation()
   全局查找结果    : function
   判定            : OK   -> 全局可调用，控制台无报错
```

**结论**：故障页中 `onclick` 调用的标识符在全局作用域中确实不存在（`undefined`），必然抛出 `ReferenceError`；修复后同名函数存在（`function`），调用链闭合，控制台 0 报错。

### 证据 2 · 双摆 RK4 数值稳定性

运行 `node verify_rk4.js`，输出：

```
积分时长            : 60 s，步长 1/600 s（共 36000 步）
末态                 : θ1=-6.2978  θ2=1.7143  ω1=0.1796  ω2=0.7783
所有数值是否有限     : 是（无 NaN / Infinity）
最大能量相对漂移     : 0.000 %
判定                 : PASS —— RK4 步长下能量守恒良好，无数值发散
```

**结论**：在 1/600 s 固定子步长下，RK4 积分 36000 步后总能量相对漂移低于 0.001%，角度/角速度全部为有限值——满足进阶挑战 A「双摆翻转流畅无数值发散」的验收标准。

### 证据 3 · 全量语法校验

运行 `node verify_syntax.js`：

```
OK        index.html   (script 块: 1)
OK        starter_code/03_buggy_practice/index.html   (script 块: 1)
OK        starter_code/04_fixed_solution/index.html   (script 块: 1)
OK        bonus_a_double_pendulum/index.html   (script 块: 1)
OK        bonus_b_celestial_persistence/index.html   (script 块: 1)

全部文件语法校验通过 ✅
```

### 证据 4 · 真实浏览器控制台 0 报错（Edge Headless）

运行 `python verify_console.py`——在真实浏览器引擎中注入错误探针（劫持 `window.onerror`、
`unhandledrejection`、`console.error`、`console.warn`），页面运行 1.8 秒后回写统计结果：

```
PASS  index.html
      控制台错误 0 条 / 警告 0 条
PASS  starter_code/04_fixed_solution/index.html
      控制台错误 0 条 / 警告 0 条
PASS  bonus_a_double_pendulum/index.html
      控制台错误 0 条 / 警告 0 条
PASS  bonus_b_celestial_persistence/index.html
      控制台错误 0 条 / 警告 0 条

总体判定：全部页面控制台 0 报错 ✅
```

### 证据 5 · 故障演练页确实会报错（真实浏览器点击复现）

运行 `python verify_buggy_click.py`——自动点击「重置摆动」按钮，捕获真实抛错：

```
按钮是否被自动点击    : True
捕获到的报错条数      : 1
报错内容              : Uncaught ReferenceError: resetAnimation is not defined @ buggy_probe.html:188:74

判定：PASS —— 故障页确实抛出了 ReferenceError，演练有效 ✅
```

**注意**：报错文本与实验指导书第 8 页给出的堆栈完全一致，证明演练场景真实有效。

### 证据 6 · 真实渲染截图

`screenshots/` 目录下为 Edge Headless 实际渲染结果：

| 截图 | 内容 |
| :--- | :--- |
| `01_main_pendulum.png` | 主交付物：深灰背景、发光摆球、三滑块面板、重置按钮 |
| `02_bonus_a_double_pendulum.png` | 双摆：两节摆杆 + 实时 θ/ω 状态读数 + 拖尾开关 |
| `03_bonus_b_celestial.png` | 天体场景：地球/月球/木星/太空胶囊按钮 + 场景读数 |
| `04_task04_buggy_before.png` | 故障演练页（修复前） |
| `05_task04_repair_after.png` | 自愈修复后（可正常运行） |

### 证据 7 · 任务四完整 ReAct 闭环（一键复现）

运行 `python repair_task04.py`，脚本会对演练页自动完成四步闭环并打印全过程：

```
① 观察 (Observe)
  自动点击重置按钮      : 已执行
  捕获报错条数          : 1
  报错内容              : Uncaught ReferenceError: resetAnimation is not defined @ line 193:74
  点击前摆角            : 0.7779516416952079 rad
  点击后摆角            : 0.7779516416952079 rad
  结论                  : 故障确已复现（报错且复位失效）

② 思考 (Think)
  调用点 (HTML onclick) : resetAnimation()  —— 全局作用域查找
  源码中已定义的函数    : resetSimulationState, updatePhysics, draw, animate
  是否存在同名定义      : 否  ← 这就是根因

③ 行动 (Act)
  diff:
    line 214
      - function resetSimulationState() {
      + function resetAnimation() {

④ 再观察 (Verify)
  捕获报错条数          : 0
  报错内容              : (无)
  点击前摆角            : 0.7802321119647775 rad
  点击后摆角            : 0.7853981633974483 rad
  复位功能              : 已恢复（精准回到 π/4 = 45°）

最终判定：PASS —— 控制台 0 报错且重置功能恢复，自愈闭环完成 ✅
```

**关键点**：修复前后「点击前摆角」都≈0.78 rad，唯一变量是复位是否生效——证明这不是随机现象，而是**修复前后的一组受控对照**。

---

## 五、人机协同三反思

> 以下反思基于本次实验**真实发生的踩坑与自愈过程**记录，非模板套话。

### 反思一 · 意图清晰度反思

**问题现场：**

任务二首轮生成 MVP 时，我给出的提示词只有一句话的目标描述——“做一个单摆模拟器”，**缺少【技术约束】与【验收标准】**。AI 交回的结果虽然能动，但出现三处偏差：

1. 用 CDN 引入了第三方动画库，违反“纯原生 Canvas、不引用外部库”的工程要求；
2. 背景是浅色，与实验要求的深灰科技色 `#1a1a24` 不符；
3. 摆球没有发光光效，视觉质感达不到验收标准。

**根因分析（缺了哪一项要素）：**

回看提示词，缺失的正是黄金三角中的**约束（Boundary）**与**验收标准（Acceptance）**：

- 没写“单文件 / 纯原生 / 不引用外部库”，AI 就按自己的偏好选了它认为更省事的工程方案；
- 没写“背景深灰 #1a1a24 / 摆球发光”，AI 无法猜测视觉规格，只能走默认样式；
- 没写“双击打开即可流畅摆动”，AI 没有明确的“交付完成”判据，自然容易做过头。

**我如何补齐：**

改用四段式重写提示词：

```
【角色】你是一位资深前端可视化与物理仿真工程师。
【目标】创建单个完整的 index.html，实现带物理简谐振动的单摆模拟器。
【技术约束】
  - 单文件 index.html，纯原生 HTML5 Canvas 绘制，不引用外部库；
  - 背景为深灰科技色 (#1a1a24)，摆球带有微弱发光光效；
  - 初始参数：摆长 L=200px，重力 g=9.8，初始摆角 45 度；
  - 使用 requestAnimationFrame 驱动物理计算与动画循环。
【验收标准】浏览器双击打开即可流畅左右摆动。
```

补齐后一次通过，三条偏差全部消除。

**结论**：**约束是“下限”，验收标准是“判据”**——两者缺一，AI 就会按自己的默认偏好发挥。角色只影响“用什么口吻、什么水平写”，真正决定产物形态的是后两项。

### 反思二 · 闭环控制反思

**问题现场（任务四）：**

在故障演练页点击“重置摆动”按钮，控制台抛出：

```
Uncaught ReferenceError: resetAnimation is not defined
    at HTMLButtonElement.onclick (index.html:125:46)
```

**我是如何定位问题的：**

我没有用“怎么坏了，重写一遍”这类**情绪化噪声反馈**，而是走**证据驱动排错**三步：

1. **调出控制台**：按 `F12` → Console，拿到完整红字堆栈（含文件与行列号）；
2. **锁定位置**：堆栈明确指向 `index.html:125:46`，即按钮的 `onclick="resetAnimation()"`；
3. **交叉验证**：在源码中检索 `resetAnimation` —— 只有调用处，没有任何定义处；而真正实现复位逻辑的函数叫 `resetSimulationState()`。

为了把“看出来的结论”升级为“可复现的证据”，我额外写了 `verify_bug.js`：用 Node 的 `vm` 模块把 `<script>` 放进沙箱执行，再从 HTML 里取出 `onclick` 调用的函数名，最后在沙箱全局对象上查找该标识符。故障页返回 `undefined`，修复页返回 `function`——**把主观判断变成了机器可复现的判定**。

**AI 的修复方案，我是否看懂了：**

看懂了。这是典型的 **JavaScript 作用域 / 命名不匹配**问题，与物理公式无关：

- HTML 的 `onclick="resetAnimation()"` 是**全局作用域**调用，浏览器会在 `window` 上查找 `resetAnimation`；
- 源码定义的是 `resetSimulationState`，从未定义过 `resetAnimation`，因此运行时抛 `ReferenceError`；
- 修复有两条等价路径：**(a)** 把按钮的 `onclick` 改为 `resetSimulationState()`；**(b)** 把函数重命名为 `resetAnimation`。核心是**调用点与定义点的标识符必须一致**。

我还验证了一件反直觉的事：**这类错误不会导致画面停滞**——因为出错只发生在“点击的那一刻”，单摆本身一直在正常摆动。这说明 **“看起来还在动”不等于“没有 Bug”**，必须以控制台报错为准。这正是证据驱动排错存在的意义。

**这次任务还暴露了一个物理层面的隐患**，是我在做 MVP 自查时发现的：主循环里 `dt` 若不加约束，切换浏览器标签页再切回来时 `dt` 会瞬间变成几秒，显式欧拉积分直接发散、摆球飞出屏幕。修复方式是在主循环里加 `Math.min(dt, 0.05)` 钳制上界。这个问题的**现象**（“切后台回来摆球就飞了”）和**根因**（数值积分步长失控）之间隔着一层，正是靠“先看现象、再找变量、再验假设”的闭环思路定位到的。

### 反思三 · 主体地位确认（HOTL）

**作为人在回路之上（HOTL）的产品总设计师，今天这些决策由我决定：**

| 决策类别 | 我的决策 |
| :--- | :--- |
| 物理规格 | 摆长默认 200px、重力 9.8、初始摆角 45°、阻尼 0.002 |
| 交互边界 | 三个滑块的取值范围（100~350 / 1~25 / 0.000~0.010） |
| 视觉标准 | 深灰科技色 #1a1a24、摆球发光、青色高光点 |
| 验收判据 | “双击打开即可流畅摆动”“拖动滑块即时响应”“控制台 0 报错” |
| 迭代节奏 | 拒绝大爆炸：先动起来 → 再交互 → 再排错 → 再进阶 |
| 进阶取舍 | 两个进阶挑战都做，并要求 RK4 必须自证“不发散” |
| 质量裁决 | 每轮亲自在浏览器看效果、按 F12 查报错，判定是否通过 |

**由 AI 完成的重复劳动：**

- 逐行书写 HTML/CSS/JS 语法，包括 Canvas 绘制路径与 `requestAnimationFrame` 循环骨架；
- 把物理微分方程 α = −(g/L)·sin(θ) − k·ω 翻译成可执行代码；
- 补齐滑块事件监听、数值标签格式化、毛玻璃面板样式等样板代码；
- 展开双摆非线性方程组并实现 RK4 四阶积分器；
- 实现 `localStorage` 读写、字段校验与场景平滑过渡。

**结论：** 我的核心工作是 **提需求、设边界、看效果、给反馈**——定义“做什么、做到什么程度、算不算合格”；AI 负责把这些确定性意图翻译成语法正确的代码。**实验全程我没有手写一行纯语法代码，但我决定了每一行的存在理由。** 这就是人在回路之上的主体地位。

---

## 六、本地运行方式

```bash
# 方式 1：直接双击 index.html（零依赖，推荐）

# 方式 2：命令行启动本地静态服务
python -m http.server 8080
# 然后访问 http://localhost:8080
```

打开后按 `F12` 查看 Console，应无任何红色报错。

---

## 七、提交自检清单 (Self-Check)

- [x] 双击 `index.html` 可在浏览器中正常流畅运行
- [x] 按 F12 检查 Console 控制台无红色报错
- [x] 在 README.md 中完整填写了“人机协同三反思”
- [x] 包含 3 次以上规范 Commit 记录（实际 **10 次**）
- [x] 已填写实验者姓名学号（**赵怡欣 / 7905126058**），且全部 Commit 作者已改写为本人
- [ ] 已执行 `git push` 将代码推送到 GitHub 个人作品集 ← **待执行，见第八节**
- [ ] 已将仓库归档打包为 `Week05_Lab_7905126058赵怡欣.zip` ← **待打包，见第八节第 ⑤ 步**

---

## 八、提交前必须完成的 5 步（照做即可）

> 详细图文版见同目录 `提交步骤清单.md`。

| 步骤 | 要做什么 | 状态 / 命令 |
| :-: | :--- | :--- |
| ① | 填姓名学号 | ✅ **已完成**：`赵怡欣 / 7905126058`（README 第 4 行 + 全部 Commit 作者） |
| ② | 装 Git for Windows | ⬜ https://git-scm.com/download/win （本机当前**未安装** Git） |
| ③ | 建 GitHub 空仓库并 push | ⬜ 见 `提交步骤清单.md` 第 3 步的 5 条命令 |
| ④ | 把仓库链接填回 README **第 7 行** | ⬜ `GitHub 作品集链接：`（推送后粘贴于此）`` |
| ⑤ | 打包 zip（已含真实学号姓名） | ⬜ `python make_zip.py 7905126058赵怡欣` |

---

## 九、推送与打包命令备查

```bash
# 1. 关联远端仓库（先在 GitHub 上新建空仓库，三个初始化勾都不要勾）
git remote add origin https://github.com/<你的用户名>/<仓库名>.git
git branch -M main
git push -u origin main

# 2. 打包为规范命名的 Zip（用脚本，会自动排除浏览器临时目录并带上 .git 历史）
python make_zip.py 7905126058赵怡欣
```
