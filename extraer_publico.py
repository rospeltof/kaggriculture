"""Extrae el main.py de notebooks publicos de Kaggriculture SIN ejecutar su codigo.

Formatos vistos: %%writefile; cadenas base85/base64 (con o sin saltos de linea)
comprimidas con zlib/gzip/lzma; tar/tar.gz con main.py; trozos acumulados con
X_PARTS.append(...) en varias celdas; ''.join((...)); diccionarios FILES/PAYLOADS
{nombre: blob}. Todo se lee con ast.literal_eval.

Uso: extraer_publico.py <carpeta_notebook> [...]   -> escribe <carpeta>/main.py
Imprime tamano y sha256 (normalizado a LF) para comparar con agentes conocidos.
"""
import ast, base64, gzip, hashlib, io, json, lzma, sys, tarfile, zlib, glob
from collections import defaultdict


def bytes_de(x):
    s = x.encode() if isinstance(x, str) else x
    yield s
    for dec in (base64.b85decode, base64.b64decode):
        try:
            yield dec(b"".join(s.split()))
        except Exception:
            pass


def textos(raw):
    for f in (lambda b: b, zlib.decompress, gzip.decompress, lzma.decompress):
        try:
            b = f(raw)
        except Exception:
            continue
        try:
            with tarfile.open(fileobj=io.BytesIO(b)) as tf:
                for m in tf.getmembers():
                    if m.isfile() and m.name.endswith("main.py"):
                        yield tf.extractfile(m).read()
            continue
        except Exception:
            pass
        cab = b[:300].lstrip()
        if cab.startswith((b"#", b"import", b"from", b'"""', b"'''")) and b"def " in b:
            yield b


def literales(src, partes):
    try:
        t = ast.parse(src)
    except SyntaxError:
        return
    for n in ast.walk(t):
        v = None
        if isinstance(n, ast.Assign):
            try:
                v = ast.literal_eval(n.value)
            except Exception:
                v = None
        elif isinstance(n, ast.Call) and getattr(n.func, "attr", "") == "append" and n.args and isinstance(n.func.value, ast.Name):
            try:
                partes[n.func.value.id].append(ast.literal_eval(n.args[0]))
            except Exception:
                pass
            continue
        elif isinstance(n, ast.Call) and getattr(n.func, "attr", "") == "join" and n.args:
            try:
                p = ast.literal_eval(n.args[0])
                v = "".join(p) if p and isinstance(p[0], str) else b"".join(p)
            except Exception:
                v = None
        if isinstance(v, dict):
            for x in v.values():
                if isinstance(x, (str, bytes)) and len(x) > 5000:
                    yield x
        elif isinstance(v, (str, bytes)) and len(v) > 5000:
            yield v


def extraer(d):
    nb = glob.glob(f"{d}/*.ipynb")
    if not nb:
        return None
    celdas = ["".join(c["source"]) for c in json.load(open(nb[0]))["cells"] if c["cell_type"] == "code"]
    got, partes = {}, defaultdict(list)
    for s in celdas:
        if s.lstrip().startswith("%%writefile") and "main.py" in s.split("\n", 1)[0]:
            b = s.split("\n", 1)[1].encode()
            got[hashlib.sha256(b.replace(b"\r\n", b"\n")).hexdigest()] = b
            continue
        for x in literales(s, partes):
            for raw in bytes_de(x):
                for b in textos(raw):
                    got[hashlib.sha256(b.replace(b"\r\n", b"\n")).hexdigest()] = b
    for nombre, ps in partes.items():
        if ps and all(isinstance(p, str) for p in ps):
            for raw in bytes_de("".join(ps)):
                for b in textos(raw):
                    got[hashlib.sha256(b.replace(b"\r\n", b"\n")).hexdigest()] = b
    if not got:
        return None
    h, b = max(got.items(), key=lambda kv: len(kv[1]))
    open(f"{d}/main.py", "wb").write(b)
    return h, len(b), len(got)


if __name__ == "__main__":
    for d in sys.argv[1:]:
        r = extraer(d.rstrip("/"))
        print(f"{d:45s} " + (f"{r[1]:8d} B  sha_lf {r[0][:12]}  ({r[2]} candidatos)" if r else "SIN EXTRAER"))
