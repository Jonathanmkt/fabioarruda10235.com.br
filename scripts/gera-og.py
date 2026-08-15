# Gera o card 1200x630 que o WhatsApp/Facebook/Telegram exibem ao compartilhar o link.
# Rode a partir da raiz do repositorio do site:  python scripts/gera-og.py
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

W, H = 1200, 630
AZUL_FUNDO = (8, 21, 43)
AZUL_TOPO = (16, 42, 82)
AMARELO = (245, 165, 36)
VERMELHO = (217, 45, 32)
BRANCO = (238, 243, 251)
SUAVE = (157, 176, 204)

F = "C:/Windows/Fonts/"
def fonte(arq, tam):
    return ImageFont.truetype(F + arq, tam)

def fundo():
    """Gradiente vertical + brilho radial no topo, igual ao CSS da pagina."""
    img = Image.new("RGB", (W, H), AZUL_FUNDO)
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        if t < 0.55:
            k = t / 0.55
            c = tuple(int(a + (b - a) * k) for a, b in zip((10, 24, 48), AZUL_FUNDO))
        else:
            k = (t - 0.55) / 0.45
            c = tuple(int(a + (b - a) * k) for a, b in zip(AZUL_FUNDO, (6, 15, 32)))
        d.line([(0, y), (W, y)], fill=c)
    # brilho radial no topo-esquerda, onde fica o retrato
    brilho = Image.new("L", (W, H), 0)
    ImageDraw.Draw(brilho).ellipse([-260, -420, 900, 470], fill=90)
    brilho = brilho.filter(ImageFilter.GaussianBlur(150))
    img = Image.composite(Image.new("RGB", (W, H), AZUL_TOPO), img, brilho)
    return img

def retrato(caminho, diam, zoom=1.0):
    """Retrato circular com anel em degrade amarelo->vermelho."""
    src = Image.open(caminho).convert("RGB")
    lado = int(min(src.size) / zoom)
    cx, cy = src.width // 2, int(src.height * 0.47)  # rosto fica acima do centro
    cy = max(lado // 2, min(cy, src.height - lado // 2))
    src = src.crop((cx - lado // 2, cy - lado // 2, cx + lado // 2, cy + lado // 2))
    # retrato feito em ambiente escuro nao le bem em card pequeno: normaliza o brilho
    cinza = src.convert("L")
    media = sum(i * n for i, n in enumerate(cinza.histogram())) / (cinza.width * cinza.height)
    if media < 110:
        fator = min(1.85, 118 / max(media, 1))
        src = ImageEnhance.Brightness(src).enhance(fator)
        src = ImageEnhance.Contrast(src).enhance(1.10)

    # ampliacao 4x em duas etapas + realce, porque a origem e 150x150
    src = src.resize((lado * 2, lado * 2), Image.LANCZOS)
    src = src.filter(ImageFilter.UnsharpMask(radius=2, percent=55, threshold=3))
    src = src.resize((diam, diam), Image.LANCZOS)
    src = src.filter(ImageFilter.UnsharpMask(radius=1.2, percent=45, threshold=3))

    ss = 4  # supersampling para borda lisa
    mask = Image.new("L", (diam * ss, diam * ss), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, diam * ss - 1, diam * ss - 1], fill=255)
    mask = mask.resize((diam, diam), Image.LANCZOS)

    anel_l = 11
    total = diam + anel_l * 2
    anel = Image.new("RGB", (total, total), AZUL_FUNDO)
    da = ImageDraw.Draw(anel)
    for y in range(total):       # degrade diagonal amarelo -> vermelho
        for x in range(0, total, 6):
            k = min(1.0, max(0.0, (x + y) / (total * 1.6)))
            da.rectangle([x, y, x + 5, y], fill=tuple(
                int(a + (b - a) * k) for a, b in zip(AMARELO, VERMELHO)))
    am = Image.new("L", (total * ss, total * ss), 0)
    ImageDraw.Draw(am).ellipse([0, 0, total * ss - 1, total * ss - 1], fill=255)
    am = am.resize((total, total), Image.LANCZOS)

    placa = Image.new("RGBA", (total, total), (0, 0, 0, 0))
    placa.paste(anel, (0, 0), am)
    aro = Image.new("RGB", (diam + 8, diam + 8), AZUL_FUNDO)
    arom = Image.new("L", ((diam + 8) * ss, (diam + 8) * ss), 0)
    ImageDraw.Draw(arom).ellipse([0, 0, (diam + 8) * ss - 1, (diam + 8) * ss - 1], fill=255)
    arom = arom.resize((diam + 8, diam + 8), Image.LANCZOS)
    placa.paste(aro, (anel_l - 4, anel_l - 4), arom)
    placa.paste(src, (anel_l, anel_l), mask)
    return placa

def espacado(d, xy, texto, f, fill, tracking):
    """Desenha com espacamento entre letras e devolve a largura total."""
    x, y = xy
    for ch in texto:
        d.text((x, y), ch, font=f, fill=fill)
        x += d.textlength(ch, font=f) + tracking
    return x - tracking - xy[0]

def largura_espacada(d, texto, f, tracking):
    return sum(d.textlength(c, font=f) + tracking for c in texto) - tracking

def gerar(cfg, destino):
    img = fundo()
    d = ImageDraw.Draw(img)

    MARGEM = 64
    RODAPE_H = 74                      # faixa reservada ao dominio, ninguem invade
    f_cargo = fonte("Montserrat-Bold.otf", 32)
    f_nome  = fonte("Montserrat-Black.otf", 86)
    f_sub   = fonte("Montserrat-Medium.otf", 28)
    f_num   = fonte("Montserrat-Black.otf", 58)
    f_lema  = fonte("Montserrat-SemiBold.otf", 29)
    f_dom   = fonte("Montserrat-Medium.otf", 23)

    # --- 1. medir o bloco de texto ANTES de desenhar, para centralizar de verdade
    NUM_PAD_X, NUM_PAD_Y, NUM_TRACK = 28, 15, 3
    tem_num = bool(cfg.get("numero"))
    h_cargo, gap1 = 44, 12
    h_nome,  gap2 = 100, 4
    h_sub,   gap3 = 40, 22
    h_num = (58 + NUM_PAD_Y * 2) if tem_num else 0
    gap4 = 24 if tem_num else 0
    h_lema = 40
    f_tag = fonte("Montserrat-SemiBold.otf", 23)
    tem_tag = bool(cfg.get("tag"))
    h_tag, gap5 = (52, 22) if tem_tag else (0, 0)
    h_texto = (h_cargo + gap1 + h_nome + gap2 + h_sub + gap3
               + h_num + gap4 + h_lema + gap5 + h_tag)

    diam = 300
    ret = retrato(cfg["foto"], diam, zoom=1.14)

    area_h = H - RODAPE_H              # altura util, fora a faixa do rodape
    ry = (area_h - ret.height) // 2
    y = (area_h - h_texto) // 2
    rx = MARGEM + 28
    x = rx + ret.width + 60

    # --- 2. conferir que o texto cabe na largura, antes de desenhar
    disponivel = W - x - MARGEM
    for rotulo, txt, f, tr in [("nome", cfg["nome"], f_nome, 0),
                               ("cargo", cfg["cargo"].upper(), f_cargo, 4.0),
                               ("lema", cfg["lema"], f_lema, 0),
                               ("sub", cfg["sub"], f_sub, 0)]:
        larg = largura_espacada(d, txt, f, tr) if tr else d.textlength(txt, font=f)
        if larg > disponivel:
            raise SystemExit(
                f"ERRO: '{rotulo}' mede {larg:.0f}px e so cabem {disponivel}px. "
                f"Encurte o texto ou baixe o corpo da fonte.")

    # sombra do retrato
    sombra = Image.new("L", (W, H), 0)
    ImageDraw.Draw(sombra).ellipse(
        [rx + 8, ry + 26, rx + ret.width + 8, ry + ret.height + 26], fill=120)
    sombra = sombra.filter(ImageFilter.GaussianBlur(28))
    img = Image.composite(Image.new("RGB", (W, H), (0, 0, 0)), img, sombra)
    d = ImageDraw.Draw(img)
    img.paste(ret, (rx, ry), ret)

    # 1. CARGO — o titulo mais importante da peca
    espacado(d, (x, y), cfg["cargo"].upper(), f_cargo, AMARELO, 4.0)
    y += h_cargo + gap1

    # 2. NOME — o ativo de marca
    d.text((x, y), cfg["nome"], font=f_nome, fill=BRANCO)
    y += h_nome + gap2

    # 3. partido + uf
    d.text((x, y), cfg["sub"], font=f_sub, fill=SUAVE)
    y += h_sub + gap3

    # 4. NUMERO DE URNA — bloco solido, so quando ha numero confirmado
    if tem_num:
        tn = cfg["numero"]
        lw = largura_espacada(d, tn, f_num, NUM_TRACK)
        d.rounded_rectangle([x, y, x + lw + NUM_PAD_X * 2, y + h_num],
                            radius=15, fill=AMARELO)
        espacado(d, (x + NUM_PAD_X, y + NUM_PAD_Y - 8), tn, f_num, (12, 26, 51), NUM_TRACK)
        y += h_num + gap4

    # 5. slogan
    d.text((x, y), cfg["lema"], font=f_lema, fill=BRANCO)
    y += h_lema + gap5

    # 6. base territorial — em eleicao proporcional, territorio e informacao de voto
    if tem_tag:
        tw = d.textlength(cfg["tag"], font=f_tag)
        d.rounded_rectangle([x, y, x + tw + 44, y + h_tag - 8], radius=26,
                            outline=(70, 96, 138), width=2)
        d.text((x + 22, y + 10), cfg["tag"], font=f_tag, fill=SUAVE)

    # rodape: faixa propria, separada por um filete — nao colide com nada acima
    fy = H - RODAPE_H
    d.line([(MARGEM, fy), (W - MARGEM, fy)], fill=(255, 255, 255, 20), width=1)
    d.rectangle([MARGEM, fy, W - MARGEM, fy], fill=(30, 48, 80))
    espacado(d, (MARGEM + 28, fy + 26), cfg["dominio"], f_dom, (128, 148, 178), 1.6)

    img.save(destino, "JPEG", quality=88, optimize=True, progressive=True)
    print(f"{destino}  {img.width}x{img.height}")


# ---------------------------------------------------------------------------
# Os dados desta peca. Mudou nome, numero, slogan ou foto? Mude aqui e rode:
#     python scripts/gera-og.py
# ---------------------------------------------------------------------------
CFG = {
    "foto":     "assets/fabio.jpg",
    "cargo":    "Deputado Estadual",
    "nome":     "Fábio Arruda",
    "sub":      "Republicanos · São Paulo",
    "numero":   "10235",
    "lema":     "Trabalho, experiência e compromisso.",
    "tag":      "",
    "dominio":  "fabioarruda10235.com.br",
}

if __name__ == "__main__":
    gerar(CFG, "assets/og.jpg")
