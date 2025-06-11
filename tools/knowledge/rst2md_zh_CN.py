import os
import re

SRC_ROOT = os.path.join('docs', 'zh_CN')
DST_ROOT = os.path.join('docs', 'zh_CN_md')

def rst_heading_to_md(lines):
    """
    将 reStructuredText 标题转换为 markdown 标题
    """
    md_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        # 检查下一个非空行是否为下划线式标题
        if i + 1 < len(lines):
            next_line = lines[i + 1]
            if re.match(r'^[=~\-\^"`#\*\+]{3,}$', next_line.strip()) and len(next_line.strip()) >= len(line.strip()):
                level_map = {
                    '=': '#',
                    '-': '##',
                    '~': '###',
                    '^': '####',
                    '"': '#####',
                    '`': '######',
                    '#': '######',
                    '*': '######',
                    '+': '######',
                }
                ch = next_line.strip()[0]
                md_level = level_map.get(ch, '#')
                md_lines.append(f"{md_level} {line.strip()}\n")
                i += 2
                continue
        md_lines.append(line)
        i += 1
    return md_lines

def rst_to_md(rst_text):
    """
    简单 rst 转 md
    """
    lines = rst_text.splitlines()
    # 标题转换
    lines = rst_heading_to_md(lines)
    md = []
    in_code = False
    for line in lines:
        # 代码块
        if line.strip().startswith('::'):
            in_code = True
            md.append('```')
            continue
        if in_code:
            if line.strip() == '':
                in_code = False
                md.append('```')
            else:
                md.append(line)
            continue
        # 列表
        if re.match(r'^\s*[\*\-\+]\s+', line):
            md.append(re.sub(r'^(\s*)[\*\-\+]\s+', r'\1- ', line))
            continue
        # 有序列表
        if re.match(r'^\s*\d+\.\s+', line):
            md.append(line)
            continue
        # 块引用
        if line.strip().startswith('.. '):
            # 注释掉 rst 指令
            md.append(f'<!-- {line.strip()} -->')
            continue
        # 其他
        md.append(line)
    # 结尾补全代码块
    if in_code:
        md.append('```')
    return '\n'.join(md)

def convert_rst_to_md(src_path, dst_path):
    with open(src_path, encoding='utf-8') as f:
        rst_text = f.read()
    md_text = rst_to_md(rst_text)
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    with open(dst_path, 'w', encoding='utf-8') as f:
        f.write(md_text)

def main():
    for root, _, files in os.walk(SRC_ROOT):
        for f in files:
            if f.endswith('.rst'):
                rel_path = os.path.relpath(os.path.join(root, f), SRC_ROOT)
                dst_file = os.path.join(DST_ROOT, rel_path).replace('.rst', '.md')
                convert_rst_to_md(os.path.join(root, f), dst_file)
                print(f"Converted: {rel_path} -> {os.path.relpath(dst_file, DST_ROOT)}")

if __name__ == '__main__':
    main()
