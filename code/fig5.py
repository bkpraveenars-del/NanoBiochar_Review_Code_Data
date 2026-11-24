"""Figure 5. Evidence-graded synergy-antagonism matrix for an aerobic, coarse-textured,
alkaline dryland soil (revised). Data and cell-level sources: matrix_data.py / ESM Table S1."""
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Rectangle
from style import *
from matrix_data import levers, outcomes, S, FLOODED_COL

cmap = LinearSegmentedColormap.from_list("div", ["#c8312f", "#ef9a98", "#f2f1ed", "#8fb8ea", "#1f5fae"])
MED = {"w": "aq", "s": "soil", "f": "field", "m": "inf"}

if __name__ == "__main__":
    fig, ax = plt.subplots(figsize=(180 * MM, 92 * MM))
    Z = np.array([[c[0] for c in r] for r in S], float)
    ax.imshow(Z, cmap=cmap, vmin=-2.4, vmax=2.4, aspect="auto")
    for i in range(Z.shape[0]):
        for j in range(Z.shape[1]):
            sc, gr, med = S[i][j][:3]
            txt = ("+%d" % sc if sc > 0 else ("%d" % sc if sc < 0 else "0"))
            col = "white" if abs(sc) == 2 else C["ink"]
            ax.text(j, i - 0.12, txt.replace("-", "−"), ha="center", va="center", fontsize=7.6,
                    fontweight="bold", color=col, zorder=5)
            ax.text(j, i + 0.27, "%s · %s" % (gr, MED[med]), ha="center", va="center", fontsize=5.4, color=col, zorder=5)
    # hatch the flooded-soil column: outside the target (aerobic dryland) soil
    ax.add_patch(Rectangle((FLOODED_COL - 0.5, -0.5), 1, Z.shape[0], facecolor="white", alpha=0.55,
                           linewidth=0, zorder=2))
    ax.add_patch(Rectangle((FLOODED_COL - 0.5, -0.5), 1, Z.shape[0], fill=False, hatch="///",
                           edgecolor="#d2d1cc", linewidth=0, zorder=2.5))
    ax.set_xticks(range(len(outcomes))); ax.set_xticklabels(outcomes, fontsize=6.4)
    ax.xaxis.tick_top()
    ax.set_yticks(range(len(levers))); ax.set_yticklabels(levers, fontsize=6.8)
    ax.set_xticks(np.arange(-.5, len(outcomes)), minor=True)
    ax.set_yticks(np.arange(-.5, len(levers)), minor=True)
    ax.grid(which="minor", color="white", linewidth=2)
    ax.tick_params(which="both", length=0)
    for s in ax.spines.values(): s.set_visible(False)
    cax = fig.add_axes([0.80, 0.035, 0.17, 0.032])
    cax.imshow(np.array([[-2, -1, 0, 1, 2]]), cmap=cmap, vmin=-2.4, vmax=2.4, aspect="auto")
    cax.set_xticks(range(5)); cax.set_xticklabels(["−2", "−1", "0", "+1", "+2"], fontsize=6.2)
    cax.set_yticks([]); cax.tick_params(length=0)
    for s in cax.spines.values(): s.set_visible(False)
    fig.text(0.80, 0.083, "antagonism  ←  effect  →  synergy", fontsize=6.0, color=C["ink2"])
    fig.text(0.02, 0.07, "Evidence grade: A, meta-analysis or multi-site field data; B, replicated laboratory studies; "
             "C, single or few studies; D, inference only.", fontsize=5.9, color=C["ink2"])
    fig.text(0.02, 0.035, "Medium: aq, aqueous batch; soil, soil incubation, pot or packed column; field; inf, no direct test. "
             "Hatched column: flooded soils only.", fontsize=5.9, color=C["ink2"])
    fig.subplots_adjust(left=0.25, right=0.99, top=0.84, bottom=0.15)
    save(fig, "Fig5_synergy_matrix")
