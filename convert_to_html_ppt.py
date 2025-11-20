#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
比亚迪半导体销售手册 - Markdown转HTML PPT工具
将拆分后的markdown文件转换为网页PPT格式
"""

import os
import re
from pathlib import Path

class MarkdownToPPT:
    """Markdown到HTML PPT转换器"""

    def __init__(self, css_file='ppt_output/byd-theme.css'):
        self.css_file = css_file
        self.mermaid_count = 0

    def convert_file(self, md_file, output_file):
        """
        转换单个markdown文件为HTML PPT

        Args:
            md_file: 输入的markdown文件路径
            output_file: 输出的HTML文件路径
        """
        print(f"📖 正在转换: {md_file}")

        # 读取markdown内容
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # 移除元信息注释
        content = re.sub(r'<!--[\s\S]*?-->', '', content, count=1)

        # 转换为HTML
        html_body = self.markdown_to_html(content)

        # 生成完整的HTML文档
        html_doc = self.create_html_document(html_body, md_file)

        # 写入文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_doc)

        print(f"✅ 已生成: {output_file}")

    def markdown_to_html(self, content):
        """将markdown内容转换为HTML"""
        html = content

        # 处理Mermaid图表（保留原样，添加div包裹）
        html = re.sub(
            r'```mermaid\n(.*?)\n```',
            lambda m: f'<div class="mermaid">\n{m.group(1)}\n</div>',
            html,
            flags=re.DOTALL
        )

        # 处理代码块
        html = re.sub(
            r'```(\w+)?\n(.*?)\n```',
            lambda m: f'<pre><code class="language-{m.group(1) or ""}">{self.escape_html(m.group(2))}</code></pre>',
            html,
            flags=re.DOTALL
        )

        # 处理表格（先提取表格，单独处理）
        tables = []
        def extract_table(match):
            tables.append(match.group(0))
            return f'___TABLE_{len(tables)-1}___'

        # 匹配markdown表格
        table_pattern = r'(\|.+\|[\n\r]+\|[\s:-]+\|[\n\r]+(?:\|.+\|[\n\r]+)*)'
        html = re.sub(table_pattern, extract_table, html)

        # 处理标题
        html = re.sub(r'^# (.+)$', r'<h1 class="page-title">\1</h1>', html, flags=re.MULTILINE)
        html = re.sub(r'^## (.+)$', r'<h2 class="section-title">\1</h2>', html, flags=re.MULTILINE)
        html = re.sub(r'^### (.+)$', r'<h3 class="subsection-title">\1</h3>', html, flags=re.MULTILINE)
        html = re.sub(r'^#### (.+)$', r'<h4>\1</h4>', html, flags=re.MULTILINE)

        # 处理分割线
        html = re.sub(r'^---+$', '<hr>', html, flags=re.MULTILINE)

        # 处理引用块
        html = re.sub(
            r'^> (.+)$',
            r'<blockquote>\1</blockquote>',
            html,
            flags=re.MULTILINE
        )

        # 处理强调框（特殊格式）
        html = re.sub(
            r'\*\*💡 (.+?):\*\*',
            r'<div class="highlight-box"><strong>💡 \1:</strong>',
            html
        )
        # 在下一个段落后关闭
        html = re.sub(
            r'(💡 .+?:</strong>.*?)(\n\n---|\n\n##|\n\n###|$)',
            r'\1</div>\2',
            html,
            flags=re.DOTALL
        )

        # 处理列表
        html = self.convert_lists(html)

        # 处理粗体和斜体
        html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
        html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)

        # 处理行内代码
        html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)

        # 处理链接
        html = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', html)

        # 处理段落
        html = re.sub(r'\n\n+', '\n</p>\n<p>\n', html)
        html = '<p>\n' + html + '\n</p>'

        # 清理空段落
        html = re.sub(r'<p>\s*</p>', '', html)

        # 还原表格并转换
        for i, table in enumerate(tables):
            html_table = self.convert_table(table)
            html = html.replace(f'___TABLE_{i}___', html_table)

        return html

    def convert_table(self, md_table):
        """将markdown表格转换为HTML表格"""
        lines = md_table.strip().split('\n')
        if len(lines) < 2:
            return md_table

        # 解析表头
        header_cells = [cell.strip() for cell in lines[0].split('|')[1:-1]]

        # 跳过分隔行
        # 解析数据行
        data_rows = []
        for line in lines[2:]:
            cells = [cell.strip() for cell in line.split('|')[1:-1]]
            data_rows.append(cells)

        # 生成HTML
        html = '<table class="data-table">\n'
        html += '  <thead>\n    <tr>\n'
        for cell in header_cells:
            html += f'      <th>{cell}</th>\n'
        html += '    </tr>\n  </thead>\n'

        html += '  <tbody>\n'
        for row in data_rows:
            html += '    <tr>\n'
            for cell in row:
                html += f'      <td>{cell}</td>\n'
            html += '    </tr>\n'
        html += '  </tbody>\n'
        html += '</table>\n'

        return html

    def convert_lists(self, html):
        """转换markdown列表为HTML"""
        # 处理无序列表
        in_ul = False
        lines = html.split('\n')
        result = []

        for line in lines:
            # 检测列表项
            if re.match(r'^[\s]*[-*+] (.+)$', line):
                match = re.match(r'^([\s]*)[-*+] (.+)$', line)
                if not in_ul:
                    result.append('<ul class="bullet-list">')
                    in_ul = True
                result.append(f'  <li>{match.group(2)}</li>')
            else:
                if in_ul:
                    result.append('</ul>')
                    in_ul = False
                result.append(line)

        if in_ul:
            result.append('</ul>')

        return '\n'.join(result)

    def escape_html(self, text):
        """转义HTML特殊字符"""
        return (text
                .replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;')
                .replace('"', '&quot;')
                .replace("'", '&#39;'))

    def create_html_document(self, body_content, source_file):
        """创建完整的HTML文档"""
        filename = Path(source_file).stem

        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>比亚迪半导体销售手册 - {filename}</title>
  <link rel="stylesheet" href="byd-theme.css">
  <script type="module">
    import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
    mermaid.initialize({{
      startOnLoad: true,
      theme: 'default',
      themeVariables: {{
        primaryColor: '#C8102E',
        primaryTextColor: '#fff',
        primaryBorderColor: '#A00D24',
        lineColor: '#666',
        secondaryColor: '#E6153A',
        tertiaryColor: '#FFE5E9'
      }}
    }});
  </script>
</head>
<body>
  <div class="ppt-container">
    <div class="page animate-fade-in">
      {body_content}
    </div>
  </div>
</body>
</html>"""
        return html


def batch_convert(input_dir='split_output', output_dir='ppt_output'):
    """批量转换所有markdown文件"""
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)

    # 获取所有markdown文件
    md_files = sorted(Path(input_dir).glob('*.md'))
    md_files = [f for f in md_files if f.name != 'README.md']

    if not md_files:
        print("❌ 未找到markdown文件")
        return

    print(f"📚 找到 {len(md_files)} 个markdown文件")
    print("="*60)

    converter = MarkdownToPPT()

    for md_file in md_files:
        # 生成输出文件名
        output_file = Path(output_dir) / f"{md_file.stem}.html"
        converter.convert_file(str(md_file), str(output_file))

    print("="*60)
    print(f"🎉 转换完成！所有文件已保存到 {output_dir}/")
    print(f"\n📋 生成的文件:")
    for html_file in sorted(Path(output_dir).glob('*.html')):
        print(f"  - {html_file.name}")


if __name__ == '__main__':
    batch_convert()
