"""Figure 7. Gated biometrical translation pipeline (redrawn from the author's draft SVG with
non-overlapping gates, explicit feedback loops and the static/dynamic stability bifurcation)."""
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Polygon
from style import *

fig, ax = plt.subplots(figsize=(180 * MM, 150 * MM))
ax.set_xlim(0, 100); ax.set_ylim(0, 125); ax.axis("off")
NAVY, GREEN = "#2f4f6f", C["green"]

def phase(y, h, title, lines, col=NAVY):
    ax.add_patch(FancyBboxPatch((10, y), 62, h, boxstyle="round,pad=0,rounding_size=1.6",
                                fc="#f5f7f9", ec=col, lw=0.9))
    ax.add_patch(FancyBboxPatch((10, y + h - 5.2), 62, 5.2, boxstyle="round,pad=0,rounding_size=1.6",
                                fc=col, ec=col, lw=0.9))
    ax.text(12, y + h - 2.6, title, va="center", fontsize=7.0, fontweight="bold", color="white")
    for k, (lab, txt) in enumerate(lines):
        yy = y + h - 8.4 - k * 3.9
        ax.text(12.5, yy, lab, fontsize=6.2, fontweight="bold", color=C["ink"], va="center")
        ax.text(24.5, yy, txt, fontsize=6.2, color=C["ink2"], va="center")

def gate(yc, l1, l2):
    w, h = 15, 6.0
    ax.add_patch(Polygon([(41 - w, yc), (41, yc + h), (41 + w, yc), (41, yc - h)], closed=True,
                         fc="white", ec=NAVY, lw=1.0, zorder=3))
    ax.text(41, yc + 1.3, l1, ha="center", va="center", fontsize=6.2, fontweight="bold", color=C["ink"], zorder=4)
    ax.text(41, yc - 1.7, l2, ha="center", va="center", fontsize=5.6, color=C["ink2"], zorder=4)

def arrow(p, q, col=NAVY, rad=0.0, ls="-"):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=8, lw=1.0, color=col,
                                 connectionstyle="arc3,rad=%s" % rad, ls=ls, zorder=2))

def loop(yfrom, yto, label):
    ax.plot([56, 82, 82], [yfrom, yfrom, yto], color=C["red"], lw=1.0)
    arrow((82, yto), (72.4, yto), col=C["red"])
    ax.text(83.5, (yfrom + yto) / 2, label, fontsize=5.8, color=C["red"], va="center", rotation=90, ha="center")
    ax.text(58, yfrom + 1.2, "NO", fontsize=5.8, fontweight="bold", color=C["red"])

# Phase 1
phase(104, 19, "PHASE 1 · Physicochemical and kinetic validation",
      [("Inputs", "size distribution; BET split into external and micropore area"),
       ("", "point of zero charge; EAC/EDC; sorption isotherms and kinetics"),
       ("Output", "rate gain per unit synthesis energy (Eq. 9 inventory)")])
gate(96, "Kinetic gain justifies", "the synthesis energy?")
arrow((41, 104), (41, 102.1))
loop(96, 113.5, "redesign")
arrow((41, 90), (41, 86.6)); ax.text(42.2, 88.3, "YES", fontsize=5.8, fontweight="bold", color=GREEN)

# Phase 2
phase(67.5, 19, "PHASE 2 · Mechanistic proof (microcosm, pot, lysimeter)",
      [("Carbon", "$^{13}$C-labelled char and pulse labelling; priming by Eq. (5)"),
       ("Gases", "$^{15}$N gas flux, product ratio r (Eq. 8); mcrA, nosZ I/II"),
       ("Metals", "EXAFS/XANES speciation; leachate colloids (BPCA)")])
gate(59.5, "Mechanisms verified", "and conflicts tested?")
arrow((41, 67.5), (41, 65.6))
loop(59.5, 77, "refine")
arrow((41, 53.5), (41, 50.1)); ax.text(42.2, 51.8, "YES", fontsize=5.8, fontweight="bold", color=GREEN)

# Phase 3
phase(31, 19, "PHASE 3 · Multi-environment trials (G × A × E)",
      [("Design", "split-plot: amendment main plots, genotypes sub-plots"),
       ("Network", "≥ 10–12 site-years spanning the aridity gradient"),
       ("Covariates", "rainfall, PET, texture, salinity, Eh, char-C tracing")])
gate(23, "Data sufficient?", "power ≥ 0.8 (Fig. 9)")
arrow((41, 31), (41, 29.1))
loop(23, 40.5, "add site-years")
arrow((41, 17), (41, 14.6)); ax.text(35.5, 15.4, "YES", fontsize=5.8, fontweight="bold", color=GREEN)

# bifurcation
ax.text(41, 12.9, "Define the biological question first", ha="center", fontsize=6.4, fontweight="bold", color=C["ink"])
for x, title, l1, l2, col in [(2, "PATH A · Hydro-structural buffering (static stability)",
                               "A × E term; Finlay–Wilkinson b < 1; lower S²", "success = flatter response in dry sites", C["blue"]),
                              (51, "PATH B · Agronomic adaptation (dynamic stability)",
                               "AMMI (ASV, WAASB), YSI, GGE, FA mixed models", "low ASV ≠ biological buffering", C["orange"])]:
    ax.add_patch(FancyBboxPatch((x, 0.8), 47, 10.2, boxstyle="round,pad=0,rounding_size=1.4",
                                fc="white", ec=col, lw=1.1))
    ax.text(x + 1.5, 8.6, title, fontsize=6.1, fontweight="bold", color=C["ink"], va="center")
    ax.text(x + 1.5, 5.3, l1, fontsize=5.9, color=C["ink2"], va="center")
    ax.text(x + 1.5, 2.6, l2, fontsize=5.9, color=C["red"] if "≠" in l2 else C["ink2"], va="center",
            fontweight="bold" if "≠" in l2 else "normal")
arrow((28, 12.9), (25.5, 11.2)); arrow((54, 12.9), (74.5, 11.2))
save(fig, "Fig7_translation_pipeline")
