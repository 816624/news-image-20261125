#!/usr/bin/env python3
"""Draw the 25 November 2026 world-news summary image (1024x1024).

Newspaper front-page layout: masthead, lead story, two secondary stories,
three tertiary stories, and an "ALSO TODAY" strip. All text is drawn from
the verified news list for Wednesday 25 November 2026. Deterministic output:
no timestamps, no randomness, no network.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (250, 247, 240)
NAVY = (16, 35, 63)
RED = (178, 34, 34)
GOLD = (232, 196, 105)
INK = (20, 20, 20)
GREY = (90, 90, 90)
STRIP = (237, 232, 220)
RULE = (200, 192, 175)

SERIF_B = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"


def make_image():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    def f(path, size):
        return ImageFont.truetype(path, size)

    def wrap(text, font, max_w):
        words = text.split()
        lines, cur = [], ""
        for w in words:
            t = (cur + " " + w).strip()
            if d.textlength(t, font=font) <= max_w:
                cur = t
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        return lines

    def block(x, y, lines, font, fill, spacing=6):
        for ln in lines:
            d.text((x, y), ln, font=font, fill=fill)
            y += font.size + spacing
        return y

    def hline(y, color=RULE, width=2):
        d.line([(40, y), (W - 40, y)], fill=color, width=width)

    # ---- Masthead ----
    d.rectangle([0, 0, W, 132], fill=NAVY)
    d.text((40, 26), "T H E   W O R L D   I N   O N E   P I C T U R E",
           font=f(SANS_B, 24), fill=GOLD)
    d.text((40, 60), "WEDNESDAY, 25 NOVEMBER 2026",
           font=f(SERIF_B, 50), fill=(255, 255, 255))
    d.rectangle([0, 132, W, 138], fill=RED)

    # ---- Lead story: Hormuz (ends by 448) ----
    y = 150
    d.text((40, y), "IRAN WAR  \u00b7  STRAIT OF HORMUZ", font=f(SANS_B, 21), fill=RED)
    y = 178
    for ln in ["MINES BLAST", "TANKERS IN HORMUZ"]:
        d.text((40, y), ln, font=f(SERIF_B, 70), fill=INK)
        y += 78
    y += 6
    sub = ("Iran says two oil tankers struck naval mines and caught fire in the "
           "strait. Houthis hit Saudi Arabia's Ras Tanura refinery and a Riyadh "
           "tower, injuring 11, as the US weighs strikes on Iran's leaders.")
    y = block(40, y, wrap(sub, f(SANS, 24), W - 80), f(SANS, 24), (40, 40, 40), 7)
    print("lead ends at", y)
    hline(448)

    # ---- Row 2: two stories (ends by 656) ----
    y0 = 466
    col_w = 452
    for x, kick, head, body in [
        (40, "MARKETS", "Asia stocks plunge, Dow tops 50,000",
         "KOSPI dives 6.2% and the Nikkei falls 2.8% as the AI rally cracks. "
         "The Dow closes above 50,000 for the first time."),
        (532, "UKRAINE", "Drones set two Russian refineries ablaze",
         "Ukrainian drones hit Rosneft's Syzran and Kuibyshev plants in Samara. "
         "Russia strikes Kyiv and Odesa overnight, killing three."),
    ]:
        d.text((x, y0), kick, font=f(SANS_B, 18), fill=RED)
        yy = block(x, y0 + 26, wrap(head, f(SERIF_B, 31), col_w),
                   f(SERIF_B, 31), INK, 4)
        end = block(x, yy + 6, wrap(body, f(SANS, 20), col_w),
                    f(SANS, 20), (45, 45, 45), 4)
        print("row2 col ends at", end)
    hline(656)

    # ---- Row 3: three stories (ends by 840) ----
    y0 = 672
    col_w = 293
    for x, kick, head, body in [
        (40, "NVIDIA", "Huang says sorry, in therapy",
         "Nvidia's reinstated chief apologises to staff, says he is in therapy; "
         "shares slide 5.9%."),
        (365, "HUAWEI", "Huawei guilty on 10 counts",
         "Brooklyn jury convicts Huawei of bank fraud, sanctions breaches, "
         "trade-secret theft."),
        (690, "GAZA", "Hamas security chief killed",
         "An Israeli strike kills Hamas colonel Abuelouf, his wife and two "
         "children in Gaza City."),
    ]:
        d.text((x, y0), kick, font=f(SANS_B, 17), fill=RED)
        yy = block(x, y0 + 24, wrap(head, f(SERIF_B, 26), col_w),
                   f(SERIF_B, 26), INK, 3)
        end = block(x, yy + 4, wrap(body, f(SANS, 18), col_w),
                    f(SANS, 18), (45, 45, 45), 4)
        print("row3 col ends at", end)

    # ---- Also today strip (840-972) ----
    d.rounded_rectangle([40, 840, W - 40, 972], radius=10, fill=STRIP)
    d.text((58, 850), "ALSO TODAY", font=f(SANS_B, 19), fill=RED)
    also = ("Sudan: RSF drone strikes kill 19 civilians  \u00b7  Dell AI server sales up 291% "
            "to $22bn in record quarter  \u00b7  Poland seeks a permanent US base after Russian "
            "incursions  \u00b7  Australia\u2013Solomons treaty bars foreign military bases  \u00b7  "
            "Shenzhou-24 docks with China's Tiangong station  \u00b7  Trump awards Giuliani the "
            "Medal of Freedom")
    end = block(58, 876, wrap(also, f(SANS, 18), W - 116), f(SANS, 18), (50, 50, 50), 4)
    print("also strip ends at", end)

    # ---- Footer ----
    d.text((W // 2, 984), "25 NOVEMBER 2026  \u2014  THE WORLD IN ONE IMAGE",
           font=f(SANS_B, 17), fill=GREY, anchor="ma")

    return img


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/newsimg25/entry.png"
    os.makedirs(os.path.dirname(out), exist_ok=True)
    im = make_image()
    im.save(out, optimize=True)
    print("saved", im.size, "bytes:", os.path.getsize(out))
