"""Figure 2. Reactivity-persistence-mobility trilemma (first-principles models)."""
import numpy as np
from style import *

# ---------- (a) geometric external SSA ----------
rho = 1.5e6  # g m^-3 skeletal-envelope density ~1.5 g cm^-3
d = np.logspace(-8, -3, 400)  # m
ssa_ext = 6.0 / (rho * d)  # m2 g-1

# ---------- (b) size-scaled persistence (hypothesis) ----------
mrt_ref = 556.0  # yr, recalcitrant pool, Wang et al. 2016 meta-analysis
d_ref = 1e-3  # m (mm-scale conventional biochar)
f_lab, mrt_lab = 0.03, 108 / 365.0  # labile pool (Wang et al. 2016)
t = 100.0

def remaining(dd, beta):
    k = (1 / mrt_ref) * (d_ref / dd) ** beta
    kl = (1 / mrt_lab)
    return f_lab * np.exp(-kl * t) + (1 - f_lab) * np.exp(-k * t)

# ---------- (c) colloid filtration theory (Tufenkji & Elimelech 2004) ----------
kB, T, mu = 1.380649e-23, 298.15, 8.9e-4
A = 1e-20
dc, eps = 0.5e-3, 0.40          # coarse sand collector, porosity
U = 1.0 / 86400                  # Darcy velocity 1 m/day
rp_dens, rf = 1500.0, 998.0
g = 9.81
gam = (1 - eps) ** (1 / 3)
As = 2 * (1 - gam ** 5) / (2 - 3 * gam + 3 * gam ** 5 - 2 * gam ** 6)

def eta0(dp):
    ap = dp / 2
    NR = dp / dc
    Dinf = kB * T / (3 * np.pi * mu * dp)
    NPe = U * dc / Dinf
    NvdW = A / (kB * T)
    NA = A / (12 * np.pi * mu * ap ** 2 * U)
    NG = (2 / 9) * ap ** 2 * (rp_dens - rf) * g / (mu * U)
    eD = 2.4 * As ** (1 / 3) * NR ** -0.081 * NPe ** -0.715 * NvdW ** 0.052
    eI = 0.55 * As * NR ** 1.675 * NA ** 0.125
    eG = 0.22 * NR ** -0.24 * NG ** 1.11 * NvdW ** 0.053
    return eD + eI + eG

dp = np.logspace(-8, -5, 400)
def L999(dp, alpha):
    return -(2 * dc / (3 * (1 - eps) * alpha * eta0(dp))) * np.log(1e-3)

if __name__ == "__main__":
    fig, axs = plt.subplots(1, 3, figsize=(180 * MM, 62 * MM))
    fig.subplots_adjust(wspace=0.42)

    ax = axs[0]
    ax.axhspan(1, 500, color=C["grid"], lw=0, zorder=0)
    ax.text(1.4e3, 260, "typical BET range,\npyrolytic biochar\n(mostly internal pores)",
            fontsize=6.0, color=C["ink2"], va="top")
    ax.loglog(d * 1e9, ssa_ext, color=C["blue"], lw=1.6, zorder=3)
    ax.axvline(100, color=C["ink2"], lw=0.6, ls=(0, (3, 2)))
    ax.axhline(1300, color=C["red"], lw=0.8, ls=(0, (1, 1.5)))
    ax.text(1.3e1, 1450, "1300 m$^2$ g$^{-1}$ claim", color=C["red"], fontsize=6.3)
    ax.plot([100], [6 / (rho * 1e-7)], "o", ms=4, color=C["blue"], mec="white", mew=0.6, zorder=4)
    ax.annotate("100 nm sphere:\n%.0f m$^2$ g$^{-1}$ external" % (6 / (rho * 1e-7)),
                xy=(100, 40), xytext=(400, 3), fontsize=6.3, color=C["ink"],
                arrowprops=dict(arrowstyle="-", lw=0.5, color=C["ink2"]))
    ax.set_xlabel("Particle diameter (nm)")
    ax.set_ylabel("External specific surface area (m$^2$ g$^{-1}$)")
    ax.set_xlim(10, 1e6); ax.set_ylim(1e-2, 1e4)
    ax.set_title("Reactivity: geometric surface", loc="left", color=C["ink"])
    panel(ax, "a", -0.26)

    ax = axs[1]
    dd = np.logspace(-8, -3, 400)
    for beta, col, lab, xy in [(0, C["ink2"], r"$\beta$ = 0 (size-independent)", (14, 84)),
                           (0.15, C["aqua"], r"$\beta$ = 0.15", (14, 53)),
                           (0.30, C["orange"], r"$\beta$ = 0.30", (12, 10)),
                           (0.50, C["red"], r"$\beta$ = 0.50", (1.3e5, 6))]:
        ax.semilogx(dd * 1e9, 100 * remaining(dd, beta), color=col, lw=1.4)
        ax.text(xy[0], xy[1], lab, color=C["ink"], fontsize=6.4, ha="left")
    ax.axvline(100, color=C["ink2"], lw=0.6, ls=(0, (3, 2)))
    ax.set_xlabel("Particle diameter (nm)")
    ax.set_ylabel("Biochar-C remaining after 100 yr (%)")
    ax.set_ylim(0, 100); ax.set_xlim(10, 1e6)
    ax.set_title("Persistence: size-scaled decay", loc="left", color=C["ink"])
    panel(ax, "b", -0.22)

    ax = axs[2]
    for alpha, col in [(1e-3, C["red"]), (1e-2, C["orange"]), (1e-1, C["blue"])]:
        ax.loglog(dp * 1e9, L999(dp, alpha), color=col, lw=1.4)
        ax.text(700, L999(7e-7, alpha) * 1.5, r"$\alpha$ = %g" % alpha, fontsize=6.4, color=C["ink"], ha="center")
    ax.axhline(1.0, color=C["ink2"], lw=0.6, ls=(0, (3, 2)))
    ax.text(12, 1.15, "root zone (1 m)", fontsize=6.2, color=C["ink2"])
    ax.axvline(100, color=C["ink2"], lw=0.6, ls=(0, (3, 2)))
    ax.set_xlabel("Particle diameter (nm)")
    ax.set_ylabel("Travel distance for 99.9% removal (m)")
    ax.set_xlim(10, 1e4)
    ax.set_ylim(1.5e-2, 6e2)
    ax.set_title("Mobility: filtration in coarse sand", loc="left", color=C["ink"])
    panel(ax, "c", -0.24)
    save(fig, "Fig2_trilemma")

    # numbers for text
    print("SSA_ext 100nm", 6 / (rho * 1e-7), "10nm", 6 / (rho * 1e-8))
    for b in [0, .15, .3, .5]:
        print("beta", b, "rem100nm", remaining(1e-7, b), "MRT", mrt_ref / (d_ref / 1e-7) ** b)
    for a in [1e-3, 1e-2, 1e-1]:
        for x in [1e-8, 1e-7, 1e-6, 2e-6]:
            print("alpha", a, "dp", x, "eta0 %.3g" % eta0(x), "L %.3g m" % L999(x, a))
    i = np.argmin(eta0(dp)); print("min eta at", dp[i])
