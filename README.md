# moraiscode-site

Site institucional **moraiscode.com** — home e `/curriculo`, versionados com CI/CD.

## Pipeline

```
push na main
   │
   ├── CI  (GitHub Actions · .ci/check.py)
   │     valida HTML, doctype, tags de fechamento,
   │     marcadores de conflito git e arquivos obrigatórios
   │
   └── CD  (webhook GitHub → Hostinger)
         o servidor faz git fetch/reset e copia os arquivos
         versionados para o docroot
         │
         └── smoke test (Actions)
               confere HTTP 200 na home e no /curriculo
               após o deploy
```

## Estrutura

| Caminho | Descrição |
| --- | --- |
| `index.html` | Home (hero "Engenheiro de Software" + barra em verde terminal) |
| `curriculo/index.html` | Currículo |
| `css/style.css` | Estilos compartilhados |
| `assets/foto.webp` | Foto do hero |
| `.htaccess` | Regras do Apache (301 www→non-www, expiração, tipos) |
| `curriculo.md/.txt/.pdf` | Currículo em formatos alternativos |
| `robots.txt`, `llms.txt` | SEO e descrição para LLMs |

## Como editar

1. `git pull origin main`
2. edite os arquivos
3. `git add` + `git commit` + `git push origin main`
4. o webhook publica sozinho — confira o smoke test na aba **Actions**

## ⚠️ Regra

Depois do CD ligado, **edição direta no servidor é sobrescrita** no próximo deploy.
Sempre altere pelo repositório.

## Deploy manual (emergência)

```bash
ssh -p 65002 u985643746@45.137.159.188 \
  'cd ~/deploys/moraiscode-site && git fetch -q origin main && git reset -q --hard origin/main && git ls-files -z | xargs -0 cp --parents -t ~/domains/moraiscode.com/public_html/'
```
