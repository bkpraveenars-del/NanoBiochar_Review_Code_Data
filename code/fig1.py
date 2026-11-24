"""Figure 1 (revised). Organising framework: how particle-size reduction and mineral loading of
biochar could alter the fate of root-derived carbon in a degraded dryland soil, with the
evidence currently available for each fate."""
import numpy as np
from matplotlib.patches import FancyBboxPatch, Polygon, Circle, FancyArrowPatch
from matplotlib.path import Path
from matplotlib.patches import PathPatch
from style import *

fig, ax = plt.subplots(figsize=(180 * MM, 118 * MM))
ax.set_xlim(0, 100); ax.set_ylim(0, 65.5); ax.axis("off")

ROOT, ROOTE = "#d8b48a", "#8a6440"
EXU = "#e9a23b"
SOIL = "#f4efe6"


def header(x, y, w, h, text, col):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=1.0",
                                fc=col, ec="none", zorder=3))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=7.0, fontweight="bold",
            color="white", zorder=4)


def card(x, y, w, h, title, body, col, tag=None, tagcol=None, fs=5.9):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=1.0",
                                fc="white", ec=col, lw=1.1, zorder=3))
    ax.add_patch(FancyBboxPatch((x, y + h - 0.35), 1.1, 0.35, boxstyle="square,pad=0", fc=col, ec="none", zorder=4))
    ax.text(x + 1.3, y + h - 1.55, title, ha="left", va="center", fontsize=6.6, fontweight="bold",
            color=col, zorder=4)
    ax.text(x + 1.3, y + h - 3.0, body, ha="left", va="top", fontsize=fs, color=C["ink"],
            linespacing=1.35, zorder=4)
    if tag:
        ax.text(x + w - 1.0, y + h - 1.55, tag, ha="right", va="center", fontsize=5.2, color="white",
                zorder=5, bbox=dict(boxstyle="round,pad=0.25,rounding_size=0.6", fc=tagcol, ec="none"))


# ---------------- column A: root inputs (with a drawn root) ----------------
header(1, 60.5, 24, 4.2, "ROOT INPUTS", "#7a5a3c")
ax.add_patch(FancyBboxPatch((1, 15.2), 24, 44.6, boxstyle="round,pad=0,rounding_size=1.0",
                            fc=SOIL, ec="#cdbfa8", lw=0.8, zorder=1))
# soil surface and stem base
ax.plot([2.2, 23.8], [56.0, 56.0], color="#a08868", lw=0.8, zorder=2)
ax.add_patch(Polygon([[12.4, 59.4], [13.6, 59.4], [13.5, 56.0], [12.5, 56.0]], closed=True,
                     fc="#7da05a", ec="#55733c", lw=0.5, zorder=3))
# tapering tap root
xs = np.linspace(0, 1, 40)
cx = 13.0 + 0.9 * np.sin(xs * 3.2)
cy = 56.0 - xs * 19.5
wid = 0.75 * (1 - xs) + 0.12
left = np.c_[cx - wid, cy]; right = np.c_[cx + wid, cy][::-1]
ax.add_patch(Polygon(np.r_[left, right], closed=True, fc=ROOT, ec=ROOTE, lw=0.5, zorder=3))


def lateral(x0, y0, x1, y1, bend, lw):
    verts = [(x0, y0), ((x0 + x1) / 2, (y0 + y1) / 2 + bend), (x1, y1)]
    ax.add_patch(PathPatch(Path(verts, [Path.MOVETO, Path.CURVE3, Path.CURVE3]), fc="none",
                           ec=ROOTE, lw=lw + 0.5, capstyle="round", zorder=3))
    ax.add_patch(PathPatch(Path(verts, [Path.MOVETO, Path.CURVE3, Path.CURVE3]), fc="none",
                           ec=ROOT, lw=lw, capstyle="round", zorder=3))
    # root hairs and exudate halo near the tip
    rng = np.random.default_rng(int(abs(x1 * 13 + y1 * 7)))
    for k in range(6):
        t = 0.55 + 0.07 * k
        px = (1 - t) ** 2 * x0 + 2 * (1 - t) * t * (x0 + x1) / 2 + t ** 2 * x1
        py = (1 - t) ** 2 * y0 + 2 * (1 - t) * t * ((y0 + y1) / 2 + bend) + t ** 2 * y1
        ang = rng.uniform(0, 2 * np.pi)
        ax.plot([px, px + 0.55 * np.cos(ang)], [py, py + 0.55 * np.sin(ang)], color=ROOTE, lw=0.25, zorder=3)
    for k in range(7):
        ax.add_patch(Circle((x1 + rng.normal(0, 0.7), y1 + rng.normal(0, 0.7)), 0.22, fc=EXU, ec="none",
                            alpha=0.85, zorder=2))


for (x0, y0, x1, y1, b, lw) in [(13.2, 52.3, 5.0, 48.3, 1.1, 1.3), (13.6, 50.3, 21.5, 46.3, 0.9, 1.3),
                                (13.9, 46.6, 6.0, 41.8, 0.7, 1.1), (14.0, 44.2, 21.0, 40.2, 0.6, 1.0),
                                (13.6, 41.0, 8.0, 37.8, 0.5, 0.9), (13.4, 39.0, 18.5, 35.8, 0.4, 0.8)]:
    lateral(x0, y0, x1, y1, b, lw)
for k in range(10):
    ax.add_patch(Circle((13.0 + 0.9 * np.sin(3.2) + np.random.default_rng(k).normal(0, 0.8),
                         36.4 + np.random.default_rng(k + 50).normal(0, 0.7)), 0.22, fc=EXU, ec="none",
                        alpha=0.85, zorder=2))
ax.add_patch(Circle((3.0, 33.2), 0.35, fc=EXU, ec="none", zorder=4))
ax.text(4.0, 33.2, "exudates", fontsize=5.4, va="center", color=C["ink2"], zorder=4)
ax.text(2.2, 31.4, "LMW organic acids (oxalate,\ncitrate, malate), sugars, amino\nacids, mucilage, sloughed cells",
        fontsize=5.6, va="top", color=C["ink"], linespacing=1.35, zorder=4)
ax.text(2.2, 24.6, "Moderate drought: more C per g\nroot; extreme drought: variable.\nForms MAOM more efficiently\nthan aboveground inputs.",
        fontsize=5.6, va="top", color=C["ink2"], linespacing=1.35, zorder=4)

# ---------------- column B: the two engineering levers ----------------
header(27, 60.5, 30, 4.2, "TWO ENGINEERING LEVERS", "#3c4f73")
card(27, 39.3, 30, 20.5, "Particle-size reduction",
     "Faster access to surface that already exists\ninside the char; geometric external area is\nonly ≈40 m$^2$ g$^{-1}$ at 100 nm.\nRaises char-C loss (mm-scale data) and\nparticle mobility (column data).\nFaster exudate capture: untested.",
     C["blue"], fs=5.7)
card(27, 15.2, 30, 22.6, "Mineral loading",
     "Fe/Al–OH: ligand exchange with\ncarboxylates (inner-sphere bonds);\nCa$^{2+}$ bridges in calcareous soil.\nMnO$_x$: oxidises phenolic C.\nLDH: anion exchange, but carbonate takes\nthe interlayer.\nExudate retention on hybrids: untested.",
     C["aqua"], fs=5.7)

# flux arrows from roots to levers and from levers to fates
for (y0, y1) in [(46.0, 49.0), (30.0, 26.0)]:
    ax.add_patch(FancyArrowPatch((23.6, y0), (26.6, y1), arrowstyle="-|>", mutation_scale=8,
                                 color=EXU, lw=1.6, zorder=4))
ax.add_patch(FancyArrowPatch((57.4, 49.0), (59.2, 49.0), arrowstyle="-|>", mutation_scale=8,
                             color=C["ink2"], lw=1.0, zorder=4))
ax.add_patch(FancyArrowPatch((57.4, 26.0), (59.2, 26.0), arrowstyle="-|>", mutation_scale=8,
                             color=C["ink2"], lw=1.0, zorder=4))

# ---------------- column C: fates of root-derived carbon ----------------
header(59.5, 60.5, 39.5, 4.2, "FATES OF ROOT-DERIVED CARBON", "#2f6b5c")
fates = [
    ("Retained", "inner-sphere or Ca-bridged on surfaces, occluded in\nmicroaggregates or enzyme-excluding micropores;\nturnover slows if binding survives wetting cycles",
     "#1f7a63", "bulk char, field, Ferralsol", "#1f7a63"),
    ("Mineralised", "microbial uptake within hours; priming of native\nSOC while the labile char fraction is consumed",
     C["orange"], "bulk char, lab + field", "#b2502a"),
    ("Released", "oxalate strips mineral-bound C; Fe(III) is\nreduced when wet; drying–rewetting pulses",
     C["red"], "natural minerals, not hybrids", "#b33433"),
    ("Exported", "colloid leaching and wind erosion: lost from\nthe plot's SOC stock even if stored elsewhere",
     "#6b6a66", "columns, wind tunnel", "#6b6a66"),
]
y = 49.6
for (t, b, col, tag, tcol) in fates:
    card(59.5, y, 39.5, 10.2, t, b, col, tag=tag, tagcol=tcol, fs=5.7)
    y -= 11.45

# ---------------- bottom band: dryland modifiers and what to measure ----------------
ax.add_patch(FancyBboxPatch((1, 6.7), 98, 7.4, boxstyle="round,pad=0,rounding_size=1.0",
                            fc="#fbf6ec", ec="#d9c9a6", lw=0.8, zorder=1))
ax.text(2.2, 12.6, "DRYLAND MODIFIERS", fontsize=6.4, fontweight="bold", color="#7a5a3c", va="center")
chips = ["coarse texture: low\nmineral capacity for MAOM", "pH 8–9 above the\nPZC of most Fe oxides",
         "CaCO$_3$: Ca$^{2+}$ bridges,\nbut carbonate competes", "drying–rewetting\nC pulses",
         "salinity and\nsodicity", "wind and leaching\nremove fine particles"]
x = 2.2
wch = [19.0, 16.0, 17.5, 13.5, 11.5, 17.5]
for c, w in zip(chips, wch):
    ax.add_patch(FancyBboxPatch((x, 7.4), w - 0.8, 4.0, boxstyle="round,pad=0,rounding_size=0.8",
                                fc="white", ec="#d9c9a6", lw=0.6, zorder=2))
    ax.text(x + (w - 0.8) / 2, 9.4, c, ha="center", va="center", fontsize=5.4, color=C["ink"],
            linespacing=1.25, zorder=3)
    x += w

ax.add_patch(FancyBboxPatch((1, 0.4), 98, 5.4, boxstyle="round,pad=0,rounding_size=1.0",
                            fc="#eef3f9", ec="#b9cbe2", lw=0.8, zorder=1))
ax.text(2.2, 3.1, "WHAT A TEST MUST MEASURE", fontsize=6.4, fontweight="bold", color="#3c4f73", va="center")
ax.text(29.0, 3.1, "$^{13}$CO$_2$-pulse-labelled root C in each soil fraction  ·  char C removed from every fraction (BPCA or isotopes)\n"
        "SOC stock to fixed depth on equivalent soil mass  ·  particle export  ·  yield slope across sites and years",
        fontsize=5.7, va="center", color=C["ink"], linespacing=1.4)

save(fig, "Fig1_framework")
