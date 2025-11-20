#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
比亚迪半导体销售手册Markdown拆分工具 - 第二至第四批
处理剩余所有内容：产品6、场景剧本、快速响应机制、工具箱
"""

import os

# 定义拆分边界（第二批到第四批）
SPLIT_CONFIG_BATCH2_4 = [
    # 第二批：产品6
    {
        'filename': '06_product-mcu.md',
        'start_line': 4328,
        'end_line': 5626,
        'description': '产品6：MCU（微控制单元）',
        'batch': 2
    },

    # 第三批：销售场景剧本（6个场景）
    {
        'filename': '07_scenario-01-price-negotiation.md',
        'start_line': 5627,
        'end_line': 5802,
        'description': '场景1：客户砍价到底线以下',
        'batch': 3
    },
    {
        'filename': '08_scenario-02-competitor-attack.md',
        'start_line': 5803,
        'end_line': 6000,
        'description': '场景2：竞品挖墙脚，如何保住份额',
        'batch': 3
    },
    {
        'filename': '09_scenario-03-exclusive-supply.md',
        'start_line': 6001,
        'end_line': 6213,
        'description': '场景3：大客户要求独家供应',
        'batch': 3
    },
    {
        'filename': '10_scenario-04-technical-test-fail.md',
        'start_line': 6214,
        'end_line': 6445,
        'description': '场景4：技术测试不通过',
        'batch': 3
    },
    {
        'filename': '11_scenario-05-quality-complaint.md',
        'start_line': 6446,
        'end_line': 6672,
        'description': '场景5：客户投诉质量问题',
        'batch': 3
    },
    {
        'filename': '12_scenario-06-new-customer-cold-start.md',
        'start_line': 6673,
        'end_line': 7277,
        'description': '场景6：新客户冷启动（0→1突破）',
        'batch': 3
    },

    # 第四批：快速响应机制和工具箱
    {
        'filename': '13_rapid-response-mechanism.md',
        'start_line': 7278,
        'end_line': 7759,
        'description': '第三部分：快速响应机制',
        'batch': 4
    },
    {
        'filename': '14_intelligence-toolbox.md',
        'start_line': 7760,
        'end_line': 8245,
        'description': '第四部分：情报工具箱',
        'batch': 4
    }
]

def split_markdown(source_file, output_dir='./split_output'):
    """
    拆分Markdown文件（第二至第四批）

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
    print(f"\n本次处理：第二批（产品6）+ 第三批（6个场景）+ 第四批（机制+工具箱）")
    print("="*70)

    # 按批次分组
    batches = {}
    for config in SPLIT_CONFIG_BATCH2_4:
        batch_num = config['batch']
        if batch_num not in batches:
            batches[batch_num] = []
        batches[batch_num].append(config)

    # 按批次执行拆分
    for batch_num in sorted(batches.keys()):
        print(f"\n{'='*70}")
        print(f"📦 第{batch_num}批 开始处理...")
        print(f"{'='*70}")

        for config in batches[batch_num]:
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
批次: 第{batch_num}批
生成时间: 2025-11-20
来源: 比亚迪半导体销售情报支持手册
-->

"""

            # 写入文件
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(header)
                f.writelines(content)

            print(f"   ✅ 已生成: {output_file}")

    # 更新索引文件
    update_readme(output_dir)

    print(f"\n{'='*70}")
    print(f"🎉 拆分完成！共生成{len(SPLIT_CONFIG_BATCH2_4)}个新文件到 {output_dir}/")
    print(f"{'='*70}")


def update_readme(output_dir):
    """更新README索引文件，包含所有批次"""
    index_file = os.path.join(output_dir, 'README.md')

    with open(index_file, 'w', encoding='utf-8') as f:
        f.write("# 比亚迪半导体销售手册 - 拆分文件索引\n\n")
        f.write("## 📊 完整内容索引\n\n")
        f.write("本索引包含手册的所有拆分文件（4个批次）\n\n")

        # 第一批（已有）
        f.write("### 第一批：手册概览 + 产品1-5\n\n")
        f.write("| 文件 | 描述 | 行范围 |\n")
        f.write("|------|------|--------|\n")
        f.write("| `00_overview-intro.md` | 手册概览、使用说明、4C框架 | 1-115 |\n")
        f.write("| `01_product-sic.md` | 产品1：碳化硅（SiC）功率器件 | 116-918 |\n")
        f.write("| `02_product-igbt.md` | 产品2：IGBT（绝缘栅双极型晶体管） | 919-2037 |\n")
        f.write("| `03_product-camera.md` | 产品3：摄像头模组 | 2038-3007 |\n")
        f.write("| `04_product-led.md` | 产品4：车规级LED | 3008-3848 |\n")
        f.write("| `05_product-current-sensor.md` | 产品5：电流传感器 | 3849-4327 |\n\n")

        # 第二批
        f.write("### 第二批：产品6\n\n")
        f.write("| 文件 | 描述 | 行范围 |\n")
        f.write("|------|------|--------|\n")
        f.write("| `06_product-mcu.md` | 产品6：MCU（微控制单元） | 4328-5626 |\n\n")

        # 第三批
        f.write("### 第三批：销售场景剧本（6个场景）\n\n")
        f.write("| 文件 | 描述 | 行范围 |\n")
        f.write("|------|------|--------|\n")
        for config in SPLIT_CONFIG_BATCH2_4:
            if config['batch'] == 3:
                f.write(f"| `{config['filename']}` | {config['description']} | {config['start_line']}-{config['end_line']} |\n")
        f.write("\n")

        # 第四批
        f.write("### 第四批：快速响应机制 + 情报工具箱\n\n")
        f.write("| 文件 | 描述 | 行范围 |\n")
        f.write("|------|------|--------|\n")
        for config in SPLIT_CONFIG_BATCH2_4:
            if config['batch'] == 4:
                f.write(f"| `{config['filename']}` | {config['description']} | {config['start_line']}-{config['end_line']} |\n")
        f.write("\n")

        # 统计信息
        f.write("## 📈 统计信息\n\n")
        f.write("- **源文件总行数**: 8,245行\n")
        f.write("- **拆分文件总数**: 14个文件\n")
        f.write("- **覆盖范围**: 100%（全部内容）\n")
        f.write("- **批次数量**: 4批\n\n")

        f.write("## 🔧 拆分标准\n\n")
        f.write("- **边界识别**: 基于章节标题（`# 产品X：...`、`## 场景X：...`）进行分割\n")
        f.write("- **内容完整性**: 每个场景/章节保持独立完整\n")
        f.write("- **数据表格**: 保留所有原始表格和数据\n")
        f.write("- **Mermaid图表**: 保留流程图和图表代码\n")

    print(f"\n📑 索引文件已更新: {index_file}")


if __name__ == '__main__':
    split_markdown('销售手册cladue.md')
