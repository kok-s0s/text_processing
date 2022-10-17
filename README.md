# Text Processing

## Python

**must be python3**

### 开发环境

- VSCode
- python3 编译器

### Package 包

- pylint
- black
- os
- shutil
- sys
- time
- xlwt
- csv

### Google Python Style Guide

[styleguide | Style guides for Google-originated open-source projects](https://google.github.io/styleguide/pyguide.html)

## 目的以及解决思路

### 目的

将所给的一个文件夹，处理其中所有指定的 `.aim` 文件，根据数据需求，处理其中的数据，筛选出数据，然后根据需求，将相同参数所测的数据最终归到一个同参数的 `.cvs` 文件里，然后存放于脚本执行的同级目录下一个叫 `target_data_csv` 的文件夹里。

### 解决思路

可参看我所画的[图](./handle.drawio)，需要在 VSCode 下安装 `Draw.io Integration` 插件才能打开。

## 如何使用

可直接在终端环境下用 python 编译器直接输入以下命令来运行脚本（Windows 环境）

```python
python all_processes.py
```

注意使用 WSL （Windows Subsystem for Linux）或者 macOS 时，所使用的 python 编译器是以下指令

```python
python3 all_processes.py
```

仅仅是 python 编译器的别名不同罢了