"""Figure 4. Verified sorption capacities, mass vs molar basis, and HSAB hardness."""
import numpy as np
from style import *

M = dict(Cu=63.546, Hg=200.59, Pb=207.2, Cd=112.41, Ni=58.693)
data = [  # label, metal, qmax mg/g, source
    ("Nano-MnO$_2$–biochar · Cu$^{2+}$", "Cu", 142.02, "Zhou et al. 2017"),
    ("PANI–magnetic biochar · Hg$^{2+}$", "Hg", 141.89, "Kareem et al. 2025"),
    ("PANI–magnetic biochar · Cu$^{2+}$", "Cu", 124.78, "Kareem et al. 2025"),
    ("KMnO$_4$-hickory biochar · Pb$^{2+}$", "Pb", 153.1, "Wang H. et al. 2015"),
    ("Nano-MnO$_2$ alone · Cu$^{2+}$", "Cu", 93.91, "Zhou et al. 2017"),
    ("Ball-milled bagasse BC · Ni$^{2+}$", "Ni", 650e-3 * 58.693, "Lyu et al. 2018"),
    ("KMnO$_4$-hickory biochar · Cu$^{2+}$", "Cu", 34.2, "Wang H. et al. 2015"),
    ("KMnO$_4$-hickory biochar · Cd$^{2+}$", "Cd", 28.1, "Wang H. et al. 2015"),
    ("Pristine biochar · Cu$^{2+}$", "Cu", 26.88, "Zhou et al. 2017"),
]
for r in data:
    pass
mass = np.array([r[2] for r in data])
mol = np.array([r[2] / M[r[1]] for r in data])

# Pearson (1988) absolute hardness, eV
hard = [("Al$^{3+}$", 45.8, "h"), ("Mg$^{2+}$", 32.6, "h"), ("Ca$^{2+}$", 19.5, "h"),
        ("Fe$^{3+}$", 13.1, "h"), ("Zn$^{2+}$", 10.9, "b"), ("Cd$^{2+}$", 10.3, "s"),
        ("Mn$^{2+}$", 9.0, "h"), ("Ni$^{2+}$", 8.5, "b"), ("Pb$^{2+}$", 8.5, "b"),
        ("Cu$^{2+}$", 8.3, "b"), ("Hg$^{2+}$", 7.7, "s"), ("Fe$^{2+}$", 7.3, "b"),
        ("Cu$^{+}$", 6.3, "s")]
hcol = dict(h=C["blue"], b=C["yellow"], s=C["red"])

if __name__ == "__main__":
    fig = plt.figure(figsize=(180 * MM, 72 * MM))
    gs = fig.add_gridspec(1, 3, width_ratios=[1, 1, 0.9], wspace=0.12)
    order = np.argsort(mass)
    yy = np.arange(len(data))
    ax1 = fig.add_subplot(gs[0, 0]); ax2 = fig.add_subplot(gs[0, 1], sharey=ax1)
    ax1.barh(yy, mass[order], color=C["blue"], height=0.62, edgecolor="white")
    ax2.barh(yy, mol[order], color=C["violet"], height=0.62, edgecolor="white")
    ax1.set_yticks(yy); ax1.set_yticklabels([data[i][0] for i in order], fontsize=6.3)
    plt.setp(ax2.get_yticklabels(), visible=False)
    for a in (ax1, ax2): a.tick_params(axis="y", length=0)
    for y_, i in zip(yy, order):
        ax1.text(mass[i] + 2, y_, "%.1f" % mass[i], va="center", fontsize=6.2)
        ax2.text(mol[i] + 0.03, y_, "%.2f" % mol[i], va="center", fontsize=6.2)
    rank_mol = (-mol).argsort().argsort() + 1
    ax1.set_xlim(0, 185); ax2.set_xlim(0, 2.75)
    ax1.set_xlabel("$q_{max}$ (mg g$^{-1}$)"); ax2.set_xlabel("$q_{max}$ (mmol g$^{-1}$)")
    ax1.set_title("Mass basis", loc="left"); ax2.set_title("Molar basis", loc="left")
    panel(ax1, "a", -1.05)

    ax3 = fig.add_subplot(gs[0, 2])
    fig.subplots_adjust(right=0.98)
    pos = ax3.get_position(); ax3.set_position([pos.x0 + 0.07, pos.y0, pos.width - 0.07, pos.height])
    hs = sorted(hard, key=lambda r: r[1])
    y3 = np.arange(len(hs))
    ax3.hlines(y3, 0, [h[1] for h in hs], color=C["grid"], lw=1.0)
    for y_, h in zip(y3, hs):
        ax3.plot(h[1], y_, "o", ms=5, color=hcol[h[2]], mec="white", mew=0.7)
    ax3.set_yticks(y3); ax3.set_yticklabels([h[0] for h in hs], fontsize=6.6)
    ax3.tick_params(axis="y", length=0)
    ax3.set_xscale("log"); ax3.set_xlim(5, 60)
    from matplotlib.ticker import NullFormatter
    ax3.set_xticks([5, 10, 20, 50]); ax3.set_xticklabels(["5", "10", "20", "50"]); ax3.xaxis.set_minor_formatter(NullFormatter())
    ax3.set_xlabel("Absolute hardness $\\eta$ (eV)")
    ax3.set_title("HSAB hardness", loc="left")
    for k, lab, yv in [("h", "hard (Pearson class)", 2.2), ("b", "borderline", 1.2), ("s", "soft", 0.2)]:
        ax3.plot(22, yv, "o", ms=4.5, color=hcol[k], mec="white", mew=0.6)
        ax3.text(25, yv, lab, va="center", fontsize=6.2)
    panel(ax3, "b", -0.42)
    save(fig, "Fig4_sorption_hsab")
    for i in range(len(data)):
        print(data[i][0], data[i][2], round(mol[i], 3), "molar rank", rank_mol[i])
