"""Figure 6. Bipartite network view of the evidence-graded synergy-antagonism matrix (redrawn
and completed from the author's draft SVG: all 36 non-zero links, aligned nodes, graded line style)."""
import numpy as np
from matplotlib.path import Path
from matplotlib.patches import PathPatch, FancyBboxPatch
from matplotlib.lines import Line2D
from style import *
from fig5 import levers, outcomes, S

outs = [o.replace("\n", " ") for o in outcomes]
fig, ax = plt.subplots(figsize=(180 * MM, 120 * MM))
ax.set_xlim(0, 100); ax.set_ylim(-9, 100); ax.axis("off")

nl, no = len(levers), len(outs)
yl = np.linspace(88, 8, nl)
yo = np.linspace(88, 8, no)
xL, xR, bw, bh = 2, 66, 32, 6.4
style = {"A": "-", "B": "-", "C": (0, (5, 2.5)), "D": (0, (1.2, 2))}

# edges first (drawn beneath nodes); weaker evidence drawn first
edges = []
for i in range(nl):
    for j in range(no):
        sc, gr = S[i][j]
        if sc != 0:
            edges.append((gr, i, j, sc))
edges.sort(key=lambda e: "DCBA".index(e[0]))
x0, x1 = xL + bw, xR
for gr, i, j, sc in edges:
    col = C["blue"] if sc > 0 else C["red"]
    verts = [(x0, yl[i]), (x0 + 12, yl[i]), (x1 - 12, yo[j]), (x1, yo[j])]
    p = PathPatch(Path(verts, [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4]),
                  fc="none", ec=col, lw=0.9 * abs(sc) + 0.3, ls=style[gr],
                  alpha=0.85 if gr in "AB" else 0.55, capstyle="round", zorder=2)
    ax.add_patch(p)

def node(x, y, label, sub=None, side="L", tally=None):
    ax.add_patch(FancyBboxPatch((x, y - bh / 2), bw, bh, boxstyle="round,pad=0,rounding_size=1.2",
                                fc="white", ec=C["ink2"], lw=0.7, zorder=3))
    ax.text(x + bw / 2, y + (0.9 if tally else 0), label, ha="center", va="center", fontsize=6.2,
            fontweight="bold", color=C["ink"], zorder=4)
    if tally:
        ax.text(x + bw / 2, y - 1.7, tally, ha="center", va="center", fontsize=5.4, color=C["ink2"], zorder=4)

for i, lab in enumerate(levers):
    pos = sum(1 for s, g in S[i] if s > 0); neg = sum(1 for s, g in S[i] if s < 0)
    node(xL, yl[i], lab.replace(" (<100 nm)", " (<100 nm)"), tally="%d synerg%s · %d antagonism%s" % (pos, "y" if pos == 1 else "ies", neg, "" if neg == 1 else "s"))
for j, lab in enumerate(outs):
    net = sum(S[i][j][0] for i in range(nl))
    node(xR, yo[j], lab, tally=("net score %+d" % net).replace("-", "−"))

ax.text(xL + bw / 2, 96, "ENGINEERING LEVERS", ha="center", fontsize=7.4, fontweight="bold", color=C["ink"])
ax.text(xR + bw / 2, 96, "ECOSYSTEM FUNCTIONS", ha="center", fontsize=7.4, fontweight="bold", color=C["ink"])

h = [Line2D([], [], color=C["blue"], lw=2.1, label="synergy"),
     Line2D([], [], color=C["red"], lw=2.1, label="antagonism"),
     Line2D([], [], color=C["ink2"], lw=1.2, label="score ±1"),
     Line2D([], [], color=C["ink2"], lw=2.1, label="score ±2"),
     Line2D([], [], color=C["ink2"], lw=1.4, ls="-", label="grade A/B"),
     Line2D([], [], color=C["ink2"], lw=1.4, ls=(0, (5, 2.5)), label="grade C"),
     Line2D([], [], color=C["ink2"], lw=1.4, ls=(0, (1.2, 2)), label="grade D")]
ax.legend(handles=h, loc="lower center", bbox_to_anchor=(0.5, -0.02), ncol=7, fontsize=6.0,
          handlelength=2.4, columnspacing=1.2, frameon=False)
save(fig, "Fig6_bipartite_network")
