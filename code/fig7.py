"""Figure 7. How many environments are needed to detect a 'buffering' amendment?
Monte-Carlo power for a one-sided test that the amendment lowers the Finlay-Wilkinson slope:
regress D_e = (amended - control) on environmental index I_e; H0 slope >= 0."""
import numpy as np
from scipy import stats
from style import *

rng = np.random.default_rng(7)
G, R = 6, 3
sig_plot = 0.22           # plot-level residual SD (t/ha)
sd_I = 0.55               # SD of environmental index across sites (t/ha)
nE = np.array([3, 4, 5, 6, 8, 10, 12, 15, 20, 25, 30])
NSIM = 4000

def power(dB, n, sig_ae):
    se_mean = np.sqrt(2) * sig_plot / np.sqrt(G * R)
    sd_D = np.sqrt(se_mean ** 2 + 2 * sig_ae ** 2)
    hits = 0
    I = rng.normal(0, sd_I, (NSIM, n))
    D = 0.15 + dB * I + rng.normal(0, sd_D, (NSIM, n))
    Ic = I - I.mean(1, keepdims=True)
    b = (Ic * (D - D.mean(1, keepdims=True))).sum(1) / (Ic ** 2).sum(1)
    res = D - D.mean(1, keepdims=True) - b[:, None] * Ic
    se = np.sqrt((res ** 2).sum(1) / (n - 2) / (Ic ** 2).sum(1))
    t = b / se
    crit = stats.t.ppf(0.05, n - 2)
    return (t < crit).mean()

if __name__ == "__main__":
    fig, axs = plt.subplots(1, 2, figsize=(180 * MM, 62 * MM))
    fig.subplots_adjust(wspace=0.32)
    ax = axs[0]
    res = {}
    for dB, col in [(-0.15, C["orange"]), (-0.27, C["blue"]), (-0.40, C["violet"])]:
        p = [power(dB, n, 0.10) for n in nE]
        res[dB] = p
        ax.plot(nE, p, "-o", color=col, ms=3.5, lw=1.4, mec="white", mew=0.5,
                label=(r"$\Delta b$ = %.2f" % dB).replace("-", "−"))
    ax.axhline(0.8, color=C["ink2"], lw=0.6, ls=(0, (3, 2)))
    ax.text(2.6, 0.82, "80% power", fontsize=6.2, ha="left", color=C["ink2"])
    ax.set_xlabel("Number of environments (site-years)")
    ax.set_ylabel("Power (one-sided, α = 0.05)")
    ax.set_ylim(0, 1.02); ax.set_xlim(2, 31)
    ax.legend(loc="lower right", title="true slope reduction", title_fontsize=6.2)
    ax.set_title("Power to detect hydro-structural buffering", loc="left")
    panel(ax, "a", -0.17)

    ax = axs[1]
    dBs = np.linspace(-0.10, -0.50, 9)
    for sae, col, lab in [(0.05, C["aqua"], "low"), (0.10, C["blue"], "moderate"), (0.20, C["red"], "high")]:
        need = []
        for dB in dBs:
            nn = np.nan
            for n in range(3, 61):
                if power(dB, n, sae) >= 0.8:
                    nn = n; break
            need.append(nn)
        ax.plot(-dBs, need, "-o", color=col, ms=3.5, lw=1.4, mec="white", mew=0.5,
                label=r"$\sigma_{AE}$ = %.2f t ha$^{-1}$ (%s)" % (sae, lab))
        print(sae, list(zip(np.round(-dBs, 2), need)))
    ax.axhline(1, color=C["red"], lw=0.6, ls=(0, (1, 1.5)))
    ax.text(0.085, 2.2, "a single pot trial or site (n = 1) cannot estimate b", fontsize=6.0,
            ha="left", color=C["red"])
    ax.set_xlabel(r"True reduction in Finlay–Wilkinson slope ($-\Delta b$)")
    ax.set_ylabel("Environments needed for 80% power")
    ax.set_ylim(0, 62)
    ax.legend(loc="upper right", title="unexplained amendment × environment SD", title_fontsize=6.2)
    ax.set_title("Design requirement", loc="left")
    panel(ax, "b", -0.17)
    save(fig, "Fig9_power")
    for k, v in res.items():
        print(k, [round(x, 2) for x in v])
