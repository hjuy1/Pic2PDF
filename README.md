# Pic2PDF - 图片转PDF工具

## 项目简介

Pic2PDF 是一个基于 Python 的实用工具，可以将图片文件（JPG/PNG）批量转换为 PDF 文件。该工具支持调整图片尺寸和 DPI，并能递归处理目录中的所有图片文件夹。

## 功能特点

- 支持 JPG 和 PNG 格式的图片文件转换，转换后的 PDF 文件名为源图片所在的文件夹名
- 可自定义输出 PDF 的宽度和 DPI 分辨率
- 自动扫描并处理指定目录下的所有子目录
- 支持批量转换，可一次处理多个文件夹
- 可选择转换后是否删除原始图片文件
- 自动调整图片尺寸以保持一致的输出质量

## 使用场景

- 将扫描的文档图片合并为 PDF 文件
- 将漫画或图书图片整理为 PDF 电子书
- 批量处理大量图片并转换为便于查看的 PDF 格式
- 标准化图片尺寸和分辨率后生成统一格式的 PDF 文件

## 安装依赖

在使用此工具前，需要安装以下 Python 库：

```bash
pip install Pillow
```

## 使用方法

1. 修改 [pic2pdf.py] 文件末尾的主函数部分，设置正确的路径：

```python
if __name__ == "__main__":
    # 设置图片所在的基础目录和输出PDF的目录
    base_dir = Path(r"your_image_directory_path")
    out_dir = Path(r"your_output_directory_path")
    
    # 创建 Pic2PDF 实例，可选设置 width 和 dpi 参数
    toPDF = Pic2PDF(base_dir=base_dir, out_dir=out_dir, width=1080, dpi=96)
    
    # 执行转换，del_old 参数控制是否删除原始图片
    toPDF.main(del_old=False)
```

2. 运行脚本：

```bash
python pic2pdf.py
```

## 注意事项

- 确保输入目录中的图片格式为 JPG 或 PNG
- 输出目录需要有写入权限
- 如果设置了 `del_old=True`，原始图片文件将被永久删除，请谨慎使用
- 工具会自动保持图片的宽高比，在调整尺寸时不会造成图片变形
- 因为转换后的 PDF 文件名为源图片所在的文件夹名，需保证该文件夹名唯一，不然会被覆盖

## API 说明

### Pic2PDF 类

主要的处理类，包含以下参数：
- `base_dir`: Path 类型，待处理的图片所在目录
- `out_dir`: Path 类型，转换后的 PDF 文件保存位置
- `width`: int 类型（可选），转换后图片的宽度
- `dpi`: int 类型（可选），转换后图片的 DPI

### 主要方法

- `adjust_size(pic_path, target_width, target_dpi)`: 调整单个图片的尺寸和 DPI
- `get_size(img_dir)`: 获取图片文件夹中图片的最小宽度和最大 DPI
- `pic2pdf(img_dir, del_old)`: 将指定文件夹中的所有图片转换为一个 PDF 文件
- `main(del_old)`: 检测 base_dir 下所有子目录并执行转换

## 依赖库列表

- Python 3.10+
- Pillow (PIL) - 图片处理库
- pathlib - Python 标准库，用于路径处理
- dataclasses - Python 标准库，用于数据类定义
