"""Figure 1. Conceptual framework: from synthesis to field-validated function."""
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from style import *

fig, ax = plt.subplots(figsize=(180 * MM, 104 * MM))
ax.set_xlim(0, 100); ax.set_ylim(0, 60); ax.axis("off")

cols = [
    ("1  Synthesis", C["violet"], [
        ("Top-down", "planetary / high-energy\nball milling;\nultrasonication"),
        ("Bottom-up", "co-precipitation;\nhydrothermal synthesis;\nin situ KMnO$_4$ reduction"),
        ("Activation", "KOH / steam; drives BET\nabove ~1000 m$^2$ g$^{-1}$")]),
    ("2  Architectures", C["blue"], [
        ("Pristine NBC", "<100 nm, O-rich edges"),
        ("Metal-oxide hybrids", "MnO$_2$-, Fe$_3$O$_4$-,\nFeOOH-NBC"),
        ("LDH / ligand hybrids", "Mg/Al-LDH; amine, thiol\n(N/S donors)")]),
    ("3  Mechanisms", C["aqua"], [
        ("Sorption chemistry", "inner-sphere\ncomplexation; HSAB-\nmatched ligands"),
        ("Electron exchange", "EDC/EAC cycling; DIET;\nstoichiometric oxide\nreduction"),
        ("Organo-mineral", "cation bridging; ligand\nexchange; Fe–C\ncoprecipitates")]),
    ("4  Functions", C["orange"], [
        ("Carbon", "rhizodeposit capture vs\nchar-C persistence"),
        ("Greenhouse gases", "N$_2$O ↓ (nosZ);\nCH$_4$ ↓ or ↑ (acceptor\nvs conductor)"),
        ("Metals & colloids", "immobilisation vs\ncolloid-facilitated\ntransport")]),
    ("5  Field translation", C["red"], [
        ("Multi-environment", "G × A × E trials,\nsplit-plot, ≥10\nsite-years"),
        ("Stability models", "AMMI (ASV, WAASB),\nFinlay–Wilkinson b,\nfactor-analytic models"),
        ("Accounting", "net CO$_2$-eq incl.\nsynthesis energy;\nrisk monitoring")]),
]
x0, w, gap = 1.0, 18.2, 1.75
top = 52.5
for i, (title, col, boxes) in enumerate(cols):
    x = x0 + i * (w + gap)
    ax.add_patch(FancyBboxPatch((x, top), w, 5.2, boxstyle="round,pad=0,rounding_size=1.2",
                                fc=col, ec="none"))
    ax.text(x + w / 2, top + 2.6, title, ha="center", va="center", fontsize=7.0,
            fontweight="bold", color="white")
    for j, (h, body) in enumerate(boxes):
        y = top - 2.0 - (j + 1) * 12.4
        ax.add_patch(FancyBboxPatch((x, y), w, 11.2, boxstyle="round,pad=0,rounding_size=1.0",
                                    fc="#f6f5f1", ec=col, lw=0.9))
        ax.text(x + 1.2, y + 9.0, h, fontsize=6.0, fontweight="bold", color=C["ink"], va="center")
        ax.text(x + 1.2, y + 3.9, body, fontsize=5.3, color=C["ink2"], va="center", linespacing=1.3)
    if i < len(cols) - 1:
        xa = x + w + 0.15
        ax.add_patch(FancyArrowPatch((xa - 0.1, top + 2.6), (xa + gap - 0.1, top + 2.6), arrowstyle="-|>",
                                     mutation_scale=9, lw=1.0, color=C["ink2"]))

# trade-off banner
ax.add_patch(FancyBboxPatch((1.0, 0.6), 98.0, 7.6, boxstyle="round,pad=0,rounding_size=1.0",
                            fc="white", ec=C["ink2"], lw=0.7, ls=(0, (3, 2))))
ax.text(50, 6.0, "Design envelope (the nano-trilemma)", ha="center", fontsize=6.8,
        fontweight="bold", color=C["ink"])
ax.text(50, 2.9, "smaller particle → reactive surface ↑  ·  oxidative persistence ↓  ·  colloidal mobility ↑ "
        "(unless attachment efficiency α is engineered up)", ha="center", fontsize=5.9, color=C["ink2"])
save(fig, "Fig1_framework")
