# 基于GitHub仓库的部署与开发指南

本文介绍如何通过克隆GitHub仓库来部署VeighNa，以及如何在修改代码后即时生效、持续迭代。

> **适用场景：** 需要对VeighNa框架本身进行二次开发或定制改造，并希望借助Git进行版本管理的用户。

---

## 一、前置准备

### 1.1 安装Git

- **Windows：** 下载并安装 [Git for Windows](https://git-scm.com/download/win)
- **Ubuntu：** `sudo apt-get install git`
- **macOS：** `brew install git` 或通过 Xcode 命令行工具自动安装

### 1.2 准备Python环境

需要 Python 3.10 以上的 64 位版本，推荐使用 Python 3.13。

```bash
python --version   # 确认版本 >= 3.10
```

### 1.3 安装 uv（推荐包管理工具）

```bash
pip install uv
```

---

## 二、Fork并克隆仓库

### 2.1 Fork仓库（可选，用于保存自己的修改）

1. 打开 [https://github.com/vnpy/vnpy](https://github.com/vnpy/vnpy)
2. 点击右上角 **Fork** 按钮，将仓库复制到自己的账号下
3. 后续所有修改都提交到自己的 Fork，方便管理

如果不需要维护自己的修改历史，也可以直接克隆原始仓库（跳过此步）。

### 2.2 克隆仓库到本地

```bash
# 克隆自己Fork的仓库（推荐）
git clone https://github.com/你的GitHub用户名/vnpy.git
cd vnpy

# 或者直接克隆官方仓库（只读）
git clone https://github.com/vnpy/vnpy.git
cd vnpy
```

### 2.3 添加官方仓库为上游（Fork用户）

```bash
# 添加官方仓库为 upstream，方便后续同步官方更新
git remote add upstream https://github.com/vnpy/vnpy.git
git remote -v   # 确认 origin（你的Fork）和 upstream（官方）都存在
```

---

## 三、安装依赖

VeighNa 的关键依赖是 `ta-lib`，需要根据操作系统单独处理。

### 3.1 Windows 安装依赖

```bat
:: 在仓库根目录下执行
install.bat
```

或手动安装：

```bat
python -m pip install --upgrade pip wheel --index-url https://pypi.vnpy.com
python -m pip install --extra-index-url https://pypi.vnpy.com ta_lib==0.6.4
```

### 3.2 Ubuntu 安装依赖

```bash
# 安装编译工具
sudo apt-get update
sudo apt-get install build-essential

# 执行一键安装脚本（安装 ta-lib 并配置中文编码）
sudo bash install.sh
```

### 3.3 macOS 安装依赖

```bash
# 使用 Homebrew 安装 ta-lib 底层库
brew install ta-lib

# 安装 Python 包
pip install numpy==2.2.3 --index-url https://pypi.vnpy.com
pip install ta-lib==0.6.4 --index-url https://pypi.vnpy.com
```

---

## 四、以开发模式安装（核心步骤）

**开发模式**（Editable Install）是实现"修改代码后立即生效"的关键。使用 `-e` 参数安装后，Python 直接读取仓库中的源代码，无需每次修改后重新安装。

```bash
# 基础安装（仅核心功能）
pip install -e .

# 包含 AI 量化模块（alpha 模块）
pip install -e ".[alpha]"

# 包含开发工具（ruff、mypy 等）
pip install -e ".[alpha,dev]"

# 使用 uv（更快）
uv pip install -e ".[alpha,dev]" --index=https://pypi.vnpy.com
```

> **原理说明：** `-e`（editable）模式会在 site-packages 中创建一个指向当前仓库目录的链接，而非复制文件。因此修改仓库中的 `.py` 文件后，下次运行时会自动加载最新代码，**无需重新执行安装命令**。

---

## 五、配置并启动VeighNa Trader

### 5.1 复制启动脚本

```bash
# 将示例启动脚本复制到自定义目录
cp examples/veighna_trader/run.py ~/my_trader/run.py
cd ~/my_trader
```

### 5.2 修改 run.py，选择所需接口和模块

根据实际需求编辑 `run.py`，取消注释需要的接口和应用模块：

```python
from vnpy.event import EventEngine
from vnpy.trader.engine import MainEngine
from vnpy.trader.ui import MainWindow, create_qapp

# 选择交易接口（取消注释需要的）
from vnpy_ctp import CtpGateway           # CTP期货
# from vnpy_tts import TtsGateway         # TTS仿真
# from vnpy_ib import IbGateway           # Interactive Brokers

# 选择应用模块（取消注释需要的）
from vnpy_ctastrategy import CtaStrategyApp
from vnpy_ctabacktester import CtaBacktesterApp
from vnpy_datamanager import DataManagerApp
# from vnpy_riskmanager import RiskManagerApp


def main():
    qapp = create_qapp()
    event_engine = EventEngine()
    main_engine = MainEngine(event_engine)

    # 添加交易接口
    main_engine.add_gateway(CtpGateway)

    # 添加应用模块
    main_engine.add_app(CtaStrategyApp)
    main_engine.add_app(CtaBacktesterApp)
    main_engine.add_app(DataManagerApp)

    main_window = MainWindow(main_engine, event_engine)
    main_window.showMaximized()
    qapp.exec()


if __name__ == "__main__":
    main()
```

### 5.3 启动交易平台

```bash
python run.py
```

---

## 六、修改代码并使更改生效

得益于开发模式安装，修改 `vnpy/` 目录下的任何 Python 文件后，**重启应用即可生效**，无需重新安装。

### 典型修改场景

| 修改内容 | 文件位置 | 是否需要重新安装 |
|---------|---------|--------------|
| 修改交易逻辑、策略 | `vnpy/trader/` | ❌ 无需重装，重启即可 |
| 修改 GUI 界面控件 | `vnpy/trader/ui/widget.py` | ❌ 无需重装，重启即可 |
| 修改主窗口布局 | `vnpy/trader/ui/mainwindow.py` | ❌ 无需重装，重启即可 |
| 修改图表模块 | `vnpy/chart/` | ❌ 无需重装，重启即可 |
| 添加新的 Python 文件 | `vnpy/` 任意位置 | ❌ 无需重装，重启即可 |
| 修改 `pyproject.toml` 中的依赖 | `pyproject.toml` | ✅ 需重新执行 `pip install -e .` |
| 修改国际化文本（`.po` 文件） | `vnpy/trader/locale/` | ✅ 需重新执行 `pip install -e .` |

---

## 七、代码质量检查

修改代码后，提交前建议运行代码检查：

```bash
# 代码风格检查
ruff check .

# 静态类型检查
mypy vnpy

# 运行现有测试
pytest tests/
```

---

## 八、提交修改到GitHub

### 8.1 查看修改内容

```bash
git status           # 查看哪些文件被修改
git diff             # 查看具体改动内容
```

### 8.2 暂存并提交

```bash
git add vnpy/trader/ui/widget.py   # 添加指定文件
# 或
git add .                           # 添加所有修改

git commit -m "feat: 修改交易控件，增加自定义价格输入验证"
```

**提交信息规范建议：**

| 前缀 | 含义 |
|-----|------|
| `feat:` | 新增功能 |
| `fix:` | 修复 Bug |
| `docs:` | 文档更新 |
| `refactor:` | 代码重构 |
| `style:` | 代码格式调整 |

### 8.3 推送到GitHub

```bash
git push origin master   # 推送到主分支
# 或推送到功能分支
git push origin feature/my-custom-widget
```

---

## 九、同步官方最新更新

当官方仓库有新的更新时，将其合并到自己的Fork：

```bash
# 1. 拉取官方最新代码
git fetch upstream

# 2. 切换到本地主分支
git checkout master

# 3. 将官方更新合并到本地
git merge upstream/master

# 4. 如有冲突，手动解决后提交
# git add .
# git commit -m "merge: 合并官方最新更新"

# 5. 推送同步结果到自己的Fork
git push origin master
```

> **注意：** 合并后，如果 `pyproject.toml` 的依赖发生了变化，需要重新运行 `pip install -e .` 更新依赖。

---

## 十、GitHub Actions 自动化CI

项目已内置 `.github/workflows/pythonapp.yml`，每次向GitHub推送代码时，将自动执行：

1. **代码风格检查**（ruff）
2. **静态类型检查**（mypy）
3. **构建打包**（uv build）

可在 GitHub 仓库页面的 **Actions** 标签页查看每次推送的检查结果。若检查失败，请根据错误信息修复后重新推送。

---

## 十一、完整工作流程总结

```
1. Fork官方仓库 → 2. git clone到本地
        ↓
3. 安装依赖（ta-lib等）
        ↓
4. pip install -e . （开发模式安装）
        ↓
5. 配置并启动 python run.py
        ↓
6. 修改 vnpy/ 下的代码
        ↓
7. 重启应用验证效果
        ↓
8. ruff check + mypy 代码检查
        ↓
9. git add + git commit + git push
        ↓
10. GitHub Actions 自动运行CI检查
        ↓
11. （定期）git fetch upstream + git merge 同步官方更新
```

---

## 常见问题

### Q：修改了代码但运行时没有生效？

确认是否使用了开发模式安装：

```bash
pip show vnpy   # 查看 Location 字段，应指向你的仓库目录
```

如果 Location 指向 `site-packages` 而非仓库目录，请重新执行：

```bash
pip install -e .
```

### Q：合并官方更新后出现依赖错误？

```bash
pip install -e ".[alpha,dev]" --index-url https://pypi.vnpy.com
```

### Q：如何在不同机器上同步同一份代码？

所有机器都从同一个GitHub仓库克隆，修改后 `push` 到GitHub，其他机器 `pull` 即可：

```bash
git pull origin master
```

### Q：ta-lib 安装失败？

Windows 用户可使用 VeighNa 官方 PyPI 镜像的预编译版本：

```bash
pip install ta-lib==0.6.4 --extra-index-url https://pypi.vnpy.com
```

Ubuntu 用户需要从源码编译，参考 [Ubuntu安装指南](ubuntu_install.md) 中的 ta-lib 安装步骤。
