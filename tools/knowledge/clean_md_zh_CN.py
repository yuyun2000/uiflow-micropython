import os

MD_ROOT = os.path.join('docs', 'zh_CN_md')

def is_short_file(filepath, min_chars=20):
    with open(filepath, encoding='utf-8') as f:
        content = f.read()
    # 只统计非空白字符
    return len(''.join(content.split())) < min_chars

def main():
    for root, _, files in os.walk(MD_ROOT):
        for f in files:
            if f.endswith('.md'):
                full_path = os.path.join(root, f)
                # 删除 index.md
                if f == 'index.md':
                    os.remove(full_path)
                    print(f"Deleted index: {os.path.relpath(full_path, MD_ROOT)}")
                    continue
                # 删除内容小于20字的文件
                if is_short_file(full_path):
                    os.remove(full_path)
                    print(f"Deleted short: {os.path.relpath(full_path, MD_ROOT)}")

if __name__ == '__main__':
    main()
