# Subseta Montserrat para os caracteres usados nas paginas e devolve woff2 em base64.
import base64, io, sys
from fontTools.subset import Subsetter, Options
from fontTools.ttLib import TTFont

# PT-BR completo (com acentos), digitos, pontuacao usada nas pecas.
CHARS = (
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "abcdefghijklmnopqrstuvwxyz"
    "0123456789"
    "ÁÀÂÃÄÉÊÈËÍÎÌÏÓÔÕÒÖÚÛÙÜÇÑ"
    "áàâãäéêèëíîìïóôõòöúûùüçñ"
    " .,;:!?'\"()[]{}-–—/&%°ºª@#+*·•…”“’‘"
)

def subset(src, weight):
    font = TTFont(src)
    opts = Options()
    opts.flavor = "woff2"
    opts.desubroutinize = True
    opts.layout_features = ["kern", "liga", "calt"]
    opts.name_IDs = []
    opts.notdef_outline = True
    opts.recalc_bounds = True
    sub = Subsetter(options=opts)
    sub.populate(text=CHARS)
    sub.subset(font)
    buf = io.BytesIO()
    font.flavor = "woff2"
    font.save(buf)
    data = buf.getvalue()
    b64 = base64.b64encode(data).decode("ascii")
    print(f"/* {weight}: {len(data)} bytes crus, {len(b64)} em base64 */", file=sys.stderr)
    return b64

F = "C:/Windows/Fonts/"
out = {}
for nome, arq, peso in [
    ("black", "Montserrat-Black.otf", 900),
    ("semibold", "Montserrat-SemiBold.otf", 600),
    ("medium", "Montserrat-Medium.otf", 500),
]:
    out[nome] = (subset(F + arq, nome), peso)

with open(sys.argv[1], "w", encoding="utf-8") as f:
    for nome, (b64, peso) in out.items():
        f.write(f"@font-face{{font-family:Montserrat;font-style:normal;font-weight:{peso};"
                f"font-display:swap;src:url(data:font/woff2;base64,{b64}) format('woff2')}}\n")
print("escrito em", sys.argv[1], file=sys.stderr)
