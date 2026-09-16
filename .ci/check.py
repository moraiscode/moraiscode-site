#!/usr/bin/env python3
"""CI: sanidade dos arquivos estáticos antes do deploy."""
import sys, glob, re

problems = []
html_files = glob.glob('**/*.html', recursive=True)
if not html_files:
    problems.append('nenhum HTML encontrado')

for path in html_files:
    raw = open(path, encoding='utf-8', errors='replace').read()
    if re.search(r'^(<<<<<<<|=======|>>>>>>>)', raw, re.M):
        problems.append(f'{path}: marcadores de conflito git')
    low = raw.lstrip().lower()
    if not (low.startswith('<!doctype html') or low.startswith('<html')):
        problems.append(f'{path}: nao comeca com doctype/html')
    for tag in ('html', 'head', 'body'):
        if f'</{tag}>' not in low:
            problems.append(f'{path}: falta </{tag}>')

required = ['index.html', 'curriculo/index.html', 'css/style.css', 'assets/foto.webp']
for req in required:
    try:
        open(req, 'rb').close()
    except FileNotFoundError:
        problems.append(f'arquivo obrigatorio ausente: {req}')

print(f'HTML verificados: {len(html_files)}')
if problems:
    print('\n'.join('ERRO: ' + p for p in problems))
    sys.exit(1)
print('CI OK')
