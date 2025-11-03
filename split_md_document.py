# split_md_document.py
import os
import sys
from pathlib import Path


def split_markdown_file(input_file, output_dir=None):
    """
    将 Markdown 文件对半分割成两个文件

    Args:
        input_file (str): 输入的 Markdown 文件路径
        output_dir (str): 输出目录，默认为输入文件同目录
    """
    # 读取原始文件
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 按行分割内容
    lines = content.splitlines(keepends=True)
    total_lines = len(lines)

    # 计算分割点
    mid_point = total_lines // 2

    # 分割成两部分
    first_half = lines[:mid_point]
    second_half = lines[mid_point:]

    # 确定输出目录
    if output_dir is None:
        output_dir = Path(input_file).parent
    else:
        os.makedirs(output_dir, exist_ok=True)

    # 获取文件名（不含扩展名）
    file_stem = Path(input_file).stem
    file_extension = Path(input_file).suffix

    # 创建输出文件路径
    first_file = os.path.join(output_dir, f"{file_stem}_part1{file_extension}")
    second_file = os.path.join(output_dir, f"{file_stem}_part2{file_extension}")

    # 写入第一部分
    with open(first_file, 'w', encoding='utf-8') as f:
        f.writelines(first_half)

    # 写入第二部分
    with open(second_file, 'w', encoding='utf-8') as f:
        f.writelines(second_half)

    print(f"✅ 文件已成功分割:")
    print(f"  - 第一部分: {first_file} ({len(first_half)} 行)")
    print(f"  - 第二部分: {second_file} ({len(second_half)} 行)")


def split_all_md_files_in_directory(input_dir, output_dir=None):
    """
    分割目录中的所有 Markdown 文件

    Args:
        input_dir (str): 包含 Markdown 文件的目录
        output_dir (str): 输出目录
    """
    input_path = Path(input_dir)
    md_files = list(input_path.glob("*.md"))

    if not md_files:
        print("⚠️  目录中未找到 Markdown 文件")
        return

    for md_file in md_files:
        print(f"\n🔍 正在处理: {md_file.name}")
        split_markdown_file(str(md_file), output_dir)


if __name__ == "__main__":

    input_path = "d:\\Downloads\\langchain_docs_output\\langchain_docs_output\\langchain.md"
    output_dir = "d:\\Downloads\\langchain_docs_output"

    if os.path.isfile(input_path):
        # 处理单个文件
        split_markdown_file(input_path, output_dir)
    elif os.path.isdir(input_path):
        # 处理整个目录
        split_all_md_files_in_directory(input_path, output_dir)
    else:
        print(f"❌ 错误: 路径不存在: {input_path}")
        sys.exit(1)
