#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
合并所有详细页面为单一HTML文件
"""

import re
from pathlib import Path

# 定义要合并的文件列表（按顺序）
html_files = [
    'page-01-overview.html',
    'page-02-product-sic-context.html',
    'page-03-product-sic-customer.html',
    'page-04-product-sic-competitor-company.html',
    'page-05-product-igbt-summary.html',
    'page-06-products-camera-led.html',
    'page-07-products-sensor-mcu.html',
    'page-08-sales-scenarios.html',
    'page-09-scenario-12-detail.html',
    'page-10-scenario-34-detail.html',
    'page-11-scenario-56-detail.html',
    'page-12-scenario-78-detail.html',
    'page-13-rapid-response.html',
    'page-14-intelligence-toolbox.html'
]

def extract_pages(html_content):
    """提取HTML文件中所有的.page div内容"""
    # 提取body标签之间的内容
    body_match = re.search(r'<body>(.*?)</body>', html_content, re.DOTALL)
    if not body_match:
        return []

    body_content = body_match.group(1)

    # 分割并提取所有的 <div class="page"> 块
    # 使用更灵活的正则表达式来匹配完整的page div
    pages = []
    page_pattern = r'<div class="page">.*?</div>\s*(?=<!--|\n\n|<div class="page">|$)'

    # 使用简单的字符串分割方法
    parts = body_content.split('<div class="page">')
    for i, part in enumerate(parts):
        if i == 0:
            continue  # 跳过第一个空部分
        # 找到这个div的结束位置（需要匹配嵌套的div）
        div_count = 1
        pos = 0
        while pos < len(part) and div_count > 0:
            if part[pos:pos+4] == '<div':
                div_count += 1
            elif part[pos:pos+6] == '</div>':
                div_count -= 1
                if div_count == 0:
                    page_html = '<div class="page">' + part[:pos+6]
                    pages.append(page_html)
                    break
            pos += 1

    return pages

def extract_head(html_content):
    """提取HTML文件的head部分"""
    match = re.search(r'<head>(.*?)</head>', html_content, re.DOTALL)
    return match.group(1) if match else ''

def main():
    script_dir = Path(__file__).parent
    all_pages = []

    print("开始合并HTML文件...")

    # 读取第一个文件的head部分
    first_file = script_dir / html_files[0]
    with open(first_file, 'r', encoding='utf-8') as f:
        first_content = f.read()
        head_content = extract_head(first_content)

    # 遍历所有文件，提取页面内容
    for html_file in html_files:
        file_path = script_dir / html_file
        print(f"处理文件: {html_file}")

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            pages = extract_pages(content)
            all_pages.extend(pages)
            print(f"  提取了 {len(pages)} 个页面")

    print(f"\n总共提取了 {len(all_pages)} 个页面")

    # 生成合并后的HTML
    output_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
{head_content}
    <title>比亚迪半导体销售手册 - 完整版 | BYD Semiconductor Sales Manual</title>
</head>
<body>

{chr(10).join(all_pages)}

</body>
</html>"""

    # 写入输出文件
    output_file = script_dir / 'sales-manual-complete.html'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(output_html)

    print(f"\n✓ 合并完成！输出文件: {output_file}")
    print(f"✓ 总页数: {len(all_pages)}")

if __name__ == '__main__':
    main()
