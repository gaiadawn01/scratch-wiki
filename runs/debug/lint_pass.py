import sys, os
base = os.path.abspath('.')
def check():
    # Collect all md pages
    pages = []
    for p in [base, 'entities', 'concepts', 'queries', 'raw', '_archive']:
        dp = os.path.join(base, p) if p != base else base
        for root, d, f in os.walk(base):
            for f2 in f:
                if f2.endswith('.md'):
                    pages.append(os.path.join(root, f2))
    # index.md links
    links = set()
    idx = os.path.join(base, 'index.md')
    with open(idx) as fh:
        content = fh.read()
    import re
    for m in re.findall(r'\[(.*?)\]', content):
        links.add(m)
    # Orphan check: every entity/concept page must appear in index links
    for pg in sorted(pages):
        name = os.path.basename(pg)
        base_name = name.replace('.md', '').replace('_', '-')
        print(pg, '|', 'linked' if base_name in links or name in links else 'NOT-LINKED', '|', links)
check()
