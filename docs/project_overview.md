# VeighNa 项目概览：GUI、功能与技术栈

本文档详细回答以下三个问题：
1. **VeighNa 是否实现了 GUI（图形用户界面）？**
2. **该项目可以实现哪些功能？**
3. **项目具体使用了什么技术进行开发？**

---

## 一、GUI 图形用户界面

**是的，VeighNa 拥有完整的图形用户界面实现。**

### 1.1 GUI 框架

VeighNa 使用 **PySide6**（Qt for Python 官方绑定，版本 6.8.2.1）作为 GUI 框架，配合以下辅助库：

| 库名 | 版本要求 | 用途 |
|------|---------|------|
| PySide6 | 6.8.2.1 | 核心 GUI 框架（Qt 6） |
| pyqtgraph | ≥0.13.7 | 高性能金融图表（K 线、行情） |
| qdarkstyle | ≥3.2.3 | 深色主题界面风格 |
| plotly | ≥6.0.0 | 交互式数据可视化 |

### 1.2 GUI 模块结构

所有 GUI 源码位于 `vnpy/trader/ui/` 目录：

```
vnpy/trader/ui/
├── __init__.py       # 导出 MainWindow、create_qapp 等
├── qt.py             # Qt 应用初始化、深色主题配置、全局异常捕获
├── mainwindow.py     # 主交易窗口（MainWindow）
├── widget.py         # 全套自定义交易控件
└── ico/              # 应用图标资源
```

### 1.3 主窗口功能（MainWindow）

主窗口 `MainWindow` 继承自 `QtWidgets.QMainWindow`，包含以下面板：

| 面板 | 位置 | 功能 |
|------|-----|------|
| 交易（TradingWidget） | 左侧 | 下单操作：合约选择、价格、数量、方向、类型 |
| 行情（TickMonitor） | 右侧 | 实时 Tick 行情展示 |
| 委托（OrderMonitor） | 右侧 | 所有委托记录 |
| 活动委托（ActiveOrderMonitor） | 右侧（与委托标签页合并） | 未成交委托，支持快速撤单 |
| 成交（TradeMonitor） | 右侧 | 成交记录 |
| 日志（LogMonitor） | 下方 | 系统运行日志 |
| 资金（AccountMonitor） | 下方 | 账户资金信息 |
| 持仓（PositionMonitor） | 下方 | 当前持仓明细 |

菜单栏包含：
- **系统菜单**：连接各类交易接口（Gateway）、退出
- **功能菜单**：动态加载已添加的策略/应用模块
- **配置菜单**：全局参数编辑
- **帮助菜单**：合约查询、还原窗口、测试邮件、社区论坛、关于

### 1.4 K 线图表（Chart 模块）

`vnpy/chart/` 提供专业级 K 线图表，基于 pyqtgraph 渲染：

```
vnpy/chart/
├── widget.py   # ChartWidget：主图表控件
├── item.py     # CandleItem（K 线）、VolumeItem（成交量）
├── manager.py  # 数据管理器
├── base.py     # 基础定义
└── axis.py     # 坐标轴
```

- 支持大数据量高性能渲染
- 支持实时数据动态追加更新
- 支持 Tick 数据与 K 线联动显示

### 1.5 启动示例

```python
from vnpy.event import EventEngine
from vnpy.trader.engine import MainEngine
from vnpy.trader.ui import MainWindow, create_qapp

from vnpy_ctp import CtpGateway
from vnpy_ctastrategy import CtaStrategyApp
from vnpy_ctabacktester import CtaBacktesterApp

def main():
    qapp = create_qapp()                      # 创建 Qt 应用（含深色主题）

    event_engine = EventEngine()
    main_engine = MainEngine(event_engine)

    main_engine.add_gateway(CtpGateway)       # 添加期货交易接口
    main_engine.add_app(CtaStrategyApp)       # 添加 CTA 策略模块
    main_engine.add_app(CtaBacktesterApp)     # 添加 CTA 回测模块

    main_window = MainWindow(main_engine, event_engine)
    main_window.showMaximized()               # 最大化显示

    qapp.exec()

if __name__ == "__main__":
    main()
```

---

## 二、项目可以实现的功能

### 2.1 多接口实时交易

VeighNa 支持 **国内外 25+ 交易接口**，覆盖多类交易品种：

**国内市场接口：**

| 接口名称 | 品种覆盖 |
|---------|---------|
| CTP（上期所标准接口） | 国内期货、期权 |
| CTP Mini | 国内期货、期权 |
| CTP 证券（sopt） | ETF 期权 |
| 飞马（Femas） | 国内期货 |
| 恒生 UFT | 国内期货、ETF 期权 |
| 易盛（Esunny） | 国内期货、黄金 TD |
| 顶点 HTS | ETF 期权 |
| 中泰 XTP | A 股证券、ETF 期权 |
| 华鑫奇点（TORA） | A 股证券、ETF 期权 |
| TTS（仿真） | 国内期货仿真 |

**海外市场接口：**

| 接口名称 | 品种覆盖 |
|---------|---------|
| Interactive Brokers（IB） | 全球证券、期货、期权、贵金属 |
| 易盛 9.0 外盘（Tap） | 海外期货 |
| 直达期货（DA） | 海外期货 |

### 2.2 量化策略模块（App）

| 模块名称 | 核心功能 |
|---------|---------|
| **CTA 策略**（cta_strategy） | CTA 策略实时运行，细粒度委托控制，支持高频策略 |
| **CTA 回测**（cta_backtester） | 图形化 CTA 回测分析、参数优化（无需 Jupyter） |
| **价差交易**（spread_trading） | 自定义价差合约、算法交易与自动策略两种模式 |
| **期权交易**（option_master） | 期权定价（BS/BAW 等）、隐含波动率曲面、希腊值风险 |
| **组合策略**（portfolio_strategy） | 多合约 Alpha 策略，历史回测 + 实盘自动交易 |
| **算法交易**（algo_trading） | TWAP、Sniper、Iceberg、BestLimit 等智能算法 |
| **脚本策略**（script_trader） | 多标的脚本策略，支持命令行 REPL 交易 |
| **本地仿真**（paper_account） | 纯本地撮合，无需连接仿真环境 |
| **K 线图表**（chart_wizard） | 基于历史数据 + 实时 Tick 的 K 线图表展示 |
| **组合管理**（portfolio_manager） | 子账户管理、委托成交记录、每日盈亏统计 |
| **RPC 服务**（rpc_service） | 多进程分布式架构，统一行情交易路由 |
| **数据管理**（data_manager） | 历史数据树形查看、CSV 导入导出 |
| **行情记录**（data_recorder） | 图形化配置实时录制 Tick/K 线到数据库 |
| **风险管理**（risk_manager） | 流控、下单数量、活动委托、撤单总数等前端风控 |
| **Web 交易**（web_trader） | REST + WebSocket B-S 架构 Web 服务器 |
| **Excel RTD**（excel_rtd） | Excel 实时数据推送（行情、持仓、合约） |

### 2.3 AI 量化模块（vnpy.alpha — v4.0 新增）

专为机器学习量化策略设计的一站式解决方案：

```
vnpy/alpha/
├── dataset/    # 因子特征工程
│   ├── datasets/alpha_158.py   # 微软 Qlib 的 158 个股票因子
│   ├── datasets/alpha_101.py   # WorldQuant 101 个 Alpha 因子
│   └── *_function.py           # 时序/截面/技术指标计算函数
├── model/      # ML 模型训练
│   ├── models/lasso_model.py   # Lasso 回归（L1 正则化特征选择）
│   ├── models/lgb_model.py     # LightGBM（梯度提升决策树）
│   └── models/mlp_model.py     # MLP 多层感知机神经网络
├── strategy/   # 策略开发模板
│   ├── cross_sectional/        # 截面多标的策略
│   └── time_series/            # 时序单标的策略
└── lab.py      # 投研流程管理（数据→训练→信号→回测全链路）
```

**Jupyter Notebook 示例（`examples/alpha_research/`）：**
- `research_workflow_lasso.ipynb`：Lasso 回归量化投研工作流
- `research_workflow_lgb.ipynb`：LightGBM 梯度提升树量化投研工作流
- `research_workflow_mlp.ipynb`：MLP 神经网络深度学习量化投研工作流

### 2.4 数据库支持

| 类型 | 数据库 | 特点 |
|------|-------|------|
| SQL | SQLite | 默认，轻量级，无需配置 |
| SQL | MySQL | 主流关系型数据库，兼容 TiDB |
| SQL | PostgreSQL | 功能丰富，支持扩展插件 |
| NoSQL | DolphinDB | 高性能分布式时序数据库，超低延迟 |
| NoSQL | TDengine | 分布式时序数据库，内置流式计算 |
| NoSQL | MongoDB | 文档型数据库，热数据内存缓存 |

### 2.5 数据服务接口

| 数据服务 | 品种覆盖 |
|---------|---------|
| 迅投研（xt） | 股票、期货、期权、可转债、ETF |
| 米筐 RQData | 股票、期货、期权、基金、债券、黄金 TD |
| TuShare | 股票、期货、期权、基金 |
| 万得 Wind | 股票、期货、基金、债券 |
| 同花顺 iFinD | 股票、期货、基金、债券 |
| 天勤 TQSDK | 期货 |
| 掘金（GM） | 股票 |
| Polygon | 股票、期货、期权（海外） |

---

## 三、开发技术栈

### 3.1 编程语言与运行环境

| 项目 | 说明 |
|-----|------|
| **语言** | Python 3.10 / 3.11 / 3.12 / 3.13（64 位） |
| **平台** | Windows 11+ / Ubuntu 22.04 LTS+ / macOS |
| **版本管理** | hatchling（构建工具）、PEP 517/518 标准 |

### 3.2 核心架构技术

| 技术 | 说明 |
|-----|------|
| **事件驱动架构** | 自研 `EventEngine`，多线程异步事件分发，1 秒定时心跳 |
| **插件化设计** | `BaseGateway`（交易接口）、`BaseApp`（应用模块）、`BaseEngine`（引擎）抽象基类 |
| **分布式 RPC** | ZMQ（pyzmq ≥26.3.0）实现跨进程通信，支持多客户端并发 |
| **异步 REST/WS** | 协程异步 IO（asyncio），高并发实时请求处理 |

### 3.3 GUI 技术栈详细

```
GUI 层次结构
│
├── PySide6 (Qt 6)          ← 核心窗口系统、事件循环、控件
│   ├── QtWidgets           ← QMainWindow、QDockWidget、QTableWidget 等
│   ├── QtCore              ← 信号/槽、QSettings、QThread
│   └── QtGui               ← QIcon、QFont、QColor、QAction
│
├── qdarkstyle              ← 深色主题 CSS 样式表（专业金融 UI 风格）
│
├── pyqtgraph               ← 高性能 K 线图表（GPU 加速渲染）
│   ├── ChartWidget         ← 主图表控件
│   ├── CandleItem          ← K 线绘制
│   └── VolumeItem          ← 成交量绘制
│
└── plotly                  ← 交互式可视化（投研报告、因子分析）
```

### 3.4 数据处理技术

| 库 | 版本 | 用途 |
|---|-----|------|
| pandas | ≥2.2.3 | 时序数据处理与分析 |
| numpy | ≥2.2.3 | 数值计算 |
| polars | ≥1.26.0 | 高性能 DataFrame（alpha 模块） |
| ta-lib | ≥0.6.4 | 技术指标计算（MA、MACD、RSI 等） |
| pyarrow | ≥19.0.1 | 高效数据序列化存储 |

### 3.5 机器学习技术

| 库 | 版本 | 用途 |
|---|-----|------|
| scikit-learn | ≥1.6.1 | 经典机器学习算法（Lasso 等） |
| lightgbm | ≥4.6.0 | 梯度提升决策树（高效大数据集） |
| torch (PyTorch) | ≥2.6.0 | 深度学习（MLP 神经网络） |
| scipy | ≥1.15.2 | 科学计算、统计分析 |
| alphalens-reloaded | ≥0.4.5 | 因子分析与评估 |

### 3.6 优化与计算

| 库 | 版本 | 用途 |
|---|-----|------|
| deap | ≥1.4.2 | 遗传算法参数优化（策略参数寻优） |
| tqdm | — | 进度条显示 |
| nbformat | — | Jupyter Notebook 格式处理 |

### 3.7 工具与基础设施

| 库/工具 | 版本 | 用途 |
|--------|-----|------|
| loguru | ≥0.7.3 | 结构化日志记录 |
| tzlocal | — | 时区处理 |
| pyzmq | ≥26.3.0 | ZeroMQ 分布式消息通信 |
| Babel | ≥2.17.0 | 国际化（i18n）编译，支持中英文 |

### 3.8 代码质量工具

| 工具 | 配置 | 用途 |
|-----|-----|------|
| ruff | target: py310 | 代码风格检查（`ruff check .`） |
| mypy | disallow_untyped_defs=true | 静态类型检查（`mypy vnpy`） |
| pytest | — | 单元测试框架 |

---

## 四、总结对比

| 维度 | 内容 |
|-----|------|
| **是否有 GUI** | ✅ 有，基于 PySide6（Qt 6），完整的专业交易界面 |
| **GUI 特点** | 深色主题、可停靠面板、实时 K 线图表、完全可定制 |
| **核心功能** | 实时交易、策略回测、算法交易、期权定价、组合管理、风险控制 |
| **AI/ML 功能** | 因子工程（158+101 因子）、模型训练（Lasso/LGB/MLP）、策略回测 |
| **数据支持** | 6 种数据库 + 9 种数据服务接口 |
| **交易接口** | 25+ 国内外交易接口 |
| **架构模式** | 事件驱动 + 插件化 + 可选分布式 RPC |
| **编程语言** | Python 3.10+，严格类型注解 |
| **GUI 框架** | PySide6 6.8.2.1（Qt 6 官方 Python 绑定） |
| **图表引擎** | pyqtgraph（实时高性能）+ plotly（交互式分析） |
| **ML 框架** | scikit-learn + LightGBM + PyTorch |
