#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
比亚迪半导体销售手册Markdown拆分工具
按产品线将大文件拆分为可管理的小文件，便于后续转换为网页PPT
"""

import os

# 定义拆分边界（基于实际文件分析）
SPLIT_CONFIG = [
    {
        'filename': '00_overview-intro.md',
        'start_line': 1,
        'end_line': 115,
        'description': '手册概览、使用说明、4C框架'
    },
    {
        'filename': '01_product-sic.md',
        'start_line': 116,
        'end_line': 918,
        'description': '产品1：碳化硅（SiC）功率器件'
    },
    {
        'filename': '02_product-igbt.md',
        'start_line': 919,
        'end_line': 2037,
        'description': '产品2：IGBT（绝缘栅双极型晶体管）'
    },
    {
        'filename': '03_product-camera.md',
        'start_line': 2038,
        'end_line': 3007,
        'description': '产品3：摄像头模组'
    },
    {
        'filename': '04_product-led.md',
        'start_line': 3008,
        'end_line': 3848,
        'description': '产品4：车规级LED'
    },
    {
        'filename': '05_product-current-sensor.md',
        'start_line': 3849,
        'end_line': 4327,
        'description': '产品5：电流传感器'
    }
]

def split_markdown(source_file, output_dir='./split_output'):
    """
    拆分Markdown文件

    Args:
        source_file: 源文件路径
        output_dir: 输出目录
    """
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)

    # 读取源文件
    print(f"📖 正在读取源文件: {source_file}")
    with open(source_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    total_lines = len(lines)
    print(f"✅ 文件总行数: {total_lines}")

    # 执行拆分
    for config in SPLIT_CONFIG:
        output_file = os.path.join(output_dir, config['filename'])
        start = config['start_line'] - 1  # 转换为0索引
        end = config['end_line']

        print(f"\n📄 正在生成: {config['filename']}")
        print(f"   描述: {config['description']}")
        print(f"   行范围: {config['start_line']}-{config['end_line']} ({end - start}行)")

        # 提取内容
        content = lines[start:end]

        # 添加文件头部元信息
        header = f"""<!--
文件: {config['filename']}
描述: {config['description']}
原始行范围: {config['start_line']}-{config['end_line']}
生成时间: 2025-11-20
来源: 比亚迪半导体销售情报支持手册
-->

"""

        # 写入文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(header)
            f.writelines(content)

        print(f"   ✅ 已生成: {output_file}")

    # 生成索引文件
    index_file = os.path.join(output_dir, 'README.md')
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write("# 比亚迪半导体销售手册 - 拆分文件索引\n\n")
        f.write("## 第一批内容（Overview + 产品1-5）\n\n")
        f.write("本批次包含手册的核心产品情报部分，适合转换为网页PPT展示。\n\n")
        f.write("| 文件 | 描述 | 行范围 | 建议PPT页数 |\n")
        f.write("|------|------|--------|------------|\n")

        for config in SPLIT_CONFIG:
            line_count = config['end_line'] - config['start_line'] + 1
            suggested_pages = max(2, line_count // 150)  # 每150行约1页PPT
            f.write(f"| `{config['filename']}` | {config['description']} | {config['start_line']}-{config['end_line']} | ~{suggested_pages}页 |\n")

        f.write("\n## 拆分标准\n\n")
        f.write("- **边界识别**: 基于章节标题（`# 产品X：...`）进行分割\n")
        f.write("- **内容完整性**: 保持4C结构（Context/Customer/Competitor/Company）完整\n")
        f.write("- **数据表格**: 保留所有原始表格和数据，确保信息准确\n")
        f.write("- **Mermaid图表**: 保留流程图和图表代码，便于网页渲染\n\n")
        f.write("## 后续批次\n\n")
        f.write("- **第二批**: 产品6（MCU）\n")
        f.write("- **第三批**: 销售场景剧本（8个场景）\n")
        f.write("- **第四批**: 快速响应机制 + 情报工具箱\n")

    print(f"\n📑 索引文件已生成: {index_file}")
    print(f"\n🎉 拆分完成！共生成{len(SPLIT_CONFIG)}个文件到 {output_dir}/")

if __name__ == '__main__':
    split_markdown('销售手册cladue.md')
