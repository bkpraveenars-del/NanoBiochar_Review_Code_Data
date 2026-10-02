"""Figure 5. Evidence-graded synergy-antagonism matrix."""
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from style import *

levers = ["Size reduction (<100 nm)", "Surface oxidation (–COOH, quinones)",
          "MnO$_2$ loading", "Fe$_3$O$_4$ loading", "Fe(III) oxyhydroxide loading",
          "Mg/Al-LDH intercalation", "N/S-donor grafting (amine, thiol)"]
outcomes = ["Persistence of\nchar-C", "Rhizodeposit\ncapture / −priming", "CH$_4$\nmitigation",
            "N$_2$O\nmitigation", "Cationic metal\nimmobilisation", "Oxyanion\nimmobilisation",
            "Colloid\nretention", "Eco-safety"]
# score (-2..+2), evidence grade (A meta-analysis/field; B replicated lab; C single/limited; D inference)
S = [
    [(-1, "C"), (1, "C"), (0, "C"), (1, "C"), (1, "B"), (0, "C"), (-2, "B"), (-1, "C")],
    [(-1, "C"), (1, "C"), (0, "D"), (1, "B"), (1, "B"), (-1, "B"), (-1, "B"), (0, "D")],
    [(-1, "C"), (0, "D"), (1, "C"), (-1, "D"), (2, "B"), (2, "B"), (1, "C"), (-1, "C")],
    [(0, "D"), (1, "C"), (-1, "B"), (0, "D"), (1, "B"), (2, "B"), (1, "C"), (0, "C")],
    [(1, "C"), (1, "C"), (1, "C"), (0, "D"), (1, "B"), (2, "A"), (1, "C"), (0, "C")],
    [(0, "D"), (1, "C"), (0, "D"), (0, "D"), (1, "B"), (2, "B"), (1, "C"), (0, "C")],
    [(0, "D"), (0, "D"), (0, "D"), (0, "D"), (2, "B"), (0, "C"), (0, "D"), (-1, "D")],
]
cmap = LinearSegmentedColormap.from_list("div", ["#c8312f", "#ef9a98", "#f2f1ed", "#8fb8ea", "#1f5fae"])

if __name__ == "__main__":
    fig, ax = plt.subplots(figsize=(180 * MM, 82 * MM))
    Z = np.array([[c[0] for c in r] for r in S], float)
    ax.imshow(Z, cmap=cmap, vmin=-2.4, vmax=2.4, aspect="auto")
    for i in range(Z.shape[0]):
        for j in range(Z.shape[1]):
            sc, gr = S[i][j]
            txt = ("+%d" % sc if sc > 0 else ("%d" % sc if sc < 0 else "0"))
            col = "white" if abs(sc) == 2 else C["ink"]
            ax.text(j, i - 0.08, txt.replace("-", "−"), ha="center", va="center", fontsize=7.6, fontweight="bold", color=col)
            ax.text(j, i + 0.27, gr, ha="center", va="center", fontsize=5.8, color=col)
    ax.set_xticks(range(len(outcomes))); ax.set_xticklabels(outcomes, fontsize=6.6)
    ax.xaxis.tick_top()
    ax.set_yticks(range(len(levers))); ax.set_yticklabels(levers, fontsize=6.8)
    ax.set_xticks(np.arange(-.5, len(outcomes)), minor=True)
    ax.set_yticks(np.arange(-.5, len(levers)), minor=True)
    ax.grid(which="minor", color="white", linewidth=2)
    ax.tick_params(which="both", length=0)
    for s in ax.spines.values(): s.set_visible(False)
    # legend strip
    cax = fig.add_axes([0.80, 0.03, 0.17, 0.035])
    cax.imshow(np.array([[-2, -1, 0, 1, 2]]), cmap=cmap, vmin=-2.4, vmax=2.4, aspect="auto")
    cax.set_xticks(range(5)); cax.set_xticklabels(["−2", "−1", "0", "+1", "+2"], fontsize=6.2)
    cax.set_yticks([]); cax.tick_params(length=0)
    for s in cax.spines.values(): s.set_visible(False)
    fig.text(0.80, 0.085, "antagonism  ←  effect  →  synergy", fontsize=6.0, color=C["ink2"])
    fig.text(0.02, 0.035, "Evidence grade: A, meta-analysis or multi-site field data; B, replicated laboratory studies; "
             "C, single or few studies; D, mechanistic inference only.", fontsize=6.0, color=C["ink2"])
    fig.subplots_adjust(left=0.25, right=0.99, top=0.84, bottom=0.14)
    save(fig, "Fig5_synergy_matrix")
