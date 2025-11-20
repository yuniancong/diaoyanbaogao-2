#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
整合所有PPT页面为单一HTML文件
"""

import html
import os

# 定义所有要整合的页面
pages = [
    "ppt_manual/page-01-overview.html",
    "ppt_manual/page-02-product-sic-context.html",
    "ppt_manual/page-03-product-sic-customer.html",
    "ppt_manual/page-04-product-sic-competitor-company.html",
    "ppt_manual/page-05-product-igbt-summary.html",
    "ppt_manual/page-06-products-camera-led.html",
    "ppt_manual/page-07-products-sensor-mcu.html",
    "ppt_manual/page-08-sales-scenarios.html",
]

# HTML头部
html_header = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>比亚迪半导体销售情报支持手册 - 完整版</title>
    <style>
        body {
            margin: 0;
            padding: 8px;
            background-color: #f0f0f0;
        }
        .merged-iframe {
            display: block;
            width: 100%;
            border: 1px solid #ccc;
            box-sizing: border-box;
            margin-bottom: 16px;
        }
        .header {
            background: linear-gradient(45deg, #e60012, #c50010);
            color: white;
            padding: 20px;
            text-align: center;
            margin-bottom: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .header h1 {
            margin: 0;
            font-size: 28px;
        }
        .header p {
            margin: 10px 0 0 0;
            font-size: 14px;
            opacity: 0.9;
        }
        .page-info {
            background: white;
            padding: 10px 15px;
            margin-bottom: 8px;
            border-left: 4px solid #e60012;
            border-radius: 4px;
            font-size: 14px;
            color: #333;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>📘 比亚迪半导体销售情报支持手册</h1>
        <p>BYD Semiconductor Market Intelligence & Sales Manual</p>
        <p style="margin-top: 5px;">手工制作 | 总结性内容 | 基于4C分析框架 | v2.0完整版</p>
    </div>
"""

# 页面信息标签
page_labels = [
    "第1部分：手册概览与产品矩阵",
    "第2部分：SiC产品 - C1情境分析",
    "第3部分：SiC产品 - C2客户情报",
    "第4部分：SiC产品 - C3竞争对手 & C4公司能力",
    "第5部分：IGBT产品综合分析",
    "第6部分：摄像头模组 & LED产品",
    "第7部分：电流传感器 & MCU产品",
    "第8部分：销售场景剧本 & 快速响应机制",
]

# 生成iframe内容
iframe_html = ""
for idx, page_path in enumerate(pages):
    print(f"正在处理: {page_path}")

    # 读取页面内容
    with open(page_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 转义HTML内容用于srcdoc
    escaped_content = html.escape(content, quote=True)

    # 添加页面信息标签
    if idx < len(page_labels):
        iframe_html += f'    <div class="page-info">{page_labels[idx]}</div>\n'

    # 添加iframe
    iframe_html += f'''    <iframe
                        id="page-{idx+1}"
                        class="merged-iframe"
                        srcdoc="{escaped_content}"
                        frameborder="0"
                        scrolling="no"
                        width="100%"
                        onload="resizeIframe(this)">
                    </iframe>

'''

# HTML尾部（包含自动调整iframe高度的JS）
html_footer = """    <script>
        function resizeIframe(iframe) {
            try {
                const iframeDoc = iframe.contentDocument || iframe.contentWindow.document;
                if (iframeDoc.body) {
                    const height = iframeDoc.body.scrollHeight;
                    iframe.style.height = height + 'px';
                }
            } catch (e) {
                console.error('无法调整iframe高度:', e);
            }
        }

        // 页面加载完成后再次调整所有iframe高度
        window.addEventListener('load', function() {
            const iframes = document.querySelectorAll('.merged-iframe');
            iframes.forEach(function(iframe) {
                resizeIframe(iframe);
            });
        });
    </script>
</body>
</html>"""

# 组合完整HTML
full_html = html_header + iframe_html + html_footer

# 写入输出文件
output_file = "销售手册完整版-手工制作.html"
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(full_html)

print(f"\n✓ 整合完成！输出文件: {output_file}")
print(f"  总共整合了 {len(pages)} 个页面")
print(f"  文件大小: {len(full_html):,} 字节")
