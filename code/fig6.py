"""Figure 6 + Table 6. Simulated multi-environment trial (G x A x E) analysed by
ANOVA variance partitioning, Finlay-Wilkinson regression and AMMI (ASV, YSI).
Data are SIMULATED to demonstrate the analytical pipeline; they are not evidence."""
import numpy as np, json, os
from scipy import stats
from style import *

rng = np.random.default_rng(2026)
G, A, E, R = 6, 3, 8, 3
amend = ["Control", "Bulk biochar", "Engineered NBC"]
delta = np.array([0.0, 0.07, 0.16])          # hypothesised gain in effective water supply
W = np.array([0.22, 0.30, 0.38, 0.48, 0.58, 0.70, 0.84, 1.00])  # env water-supply index
envlab = ["E%d" % (i + 1) for i in range(E)]
Ypot = np.array([4.2, 4.6, 5.0, 4.4, 4.8, 5.3])     # t/ha
Kg = np.array([0.30, 0.38, 0.45, 0.26, 0.34, 0.50])  # drought sensitivity (half-saturation)

def f(w, k):
    return (w / (k + w)) * (1 + k)

Y = np.zeros((G, A, E, R))
ge = rng.normal(0, 0.12, (G, E))
ae = rng.normal(0, 0.05, (A, E))
blk = rng.normal(0, 0.10, (E, R))
for g in range(G):
    for a in range(A):
        weff = W + delta[a] * (1 - W)
        mu = Ypot[g] * f(weff, Kg[g])
        for e in range(E):
            Y[g, a, e, :] = mu[e] + ge[g, e] + ae[a, e] + blk[e] + rng.normal(0, 0.22, R)

# ---------------- ANOVA (RCBD within each environment; fixed-effects partition) ----------
gm = Y.mean()
m_g = Y.mean(axis=(1, 2, 3)); m_a = Y.mean(axis=(0, 2, 3)); m_e = Y.mean(axis=(0, 1, 3))
m_ga = Y.mean(axis=(2, 3)); m_ge = Y.mean(axis=(1, 3)); m_ae = Y.mean(axis=(0, 3))
m_gae = Y.mean(axis=3); m_er = Y.mean(axis=(0, 1))
ss = {}
ss["E"] = G * A * R * ((m_e - gm) ** 2).sum()
ss["R(E)"] = G * A * ((m_er - m_e[:, None]) ** 2).sum()
ss["G"] = A * E * R * ((m_g - gm) ** 2).sum()
ss["A"] = G * E * R * ((m_a - gm) ** 2).sum()
ss["G×A"] = E * R * ((m_ga - m_g[:, None] - m_a[None, :] + gm) ** 2).sum()
ss["G×E"] = A * R * ((m_ge - m_g[:, None] - m_e[None, :] + gm) ** 2).sum()
ss["A×E"] = G * R * ((m_ae - m_a[:, None] - m_e[None, :] + gm) ** 2).sum()
ss["G×A×E"] = R * ((m_gae - m_ga[:, :, None] - m_ge[:, None, :] - m_ae[None, :, :]
                   + m_g[:, None, None] + m_a[None, :, None] + m_e[None, None, :] - gm) ** 2).sum()
ss_tot = ((Y - gm) ** 2).sum()
ss["Error"] = ss_tot - sum(ss.values())
df = {"E": E - 1, "R(E)": E * (R - 1), "G": G - 1, "A": A - 1, "G×A": (G - 1) * (A - 1),
      "G×E": (G - 1) * (E - 1), "A×E": (A - 1) * (E - 1), "G×A×E": (G - 1) * (A - 1) * (E - 1)}
df["Error"] = G * A * E * R - 1 - sum(df.values())
ms_err = ss["Error"] / df["Error"]
anova = []
for k in ["E", "R(E)", "G", "A", "G×A", "G×E", "A×E", "G×A×E", "Error"]:
    ms = ss[k] / df[k]
    den = ss["R(E)"] / df["R(E)"] if k == "E" else ms_err
    Fv = ms / den if k != "Error" else np.nan
    dfd = df["R(E)"] if k == "E" else df["Error"]
    p = stats.f.sf(Fv, df[k], dfd) if k != "Error" else np.nan
    anova.append((k, df[k], ss[k], ms, Fv, p, 100 * ss[k] / ss_tot))

# ---------------- AMMI on entry (G x A) x E means ----------------
ent = [(g, a) for a in range(A) for g in range(G)]
M = np.array([m_gae[g, a, :] for g, a in ent])          # 18 x 8
n_ent = M.shape[0]
em = M.mean(1); evm = M.mean(0); mm = M.mean()
I = M - em[:, None] - evm[None, :] + mm
U, s, Vt = np.linalg.svd(I, full_matrices=False)
lam2 = s ** 2
ss_int = R * lam2                                      # on plot basis
ss_int_total = R * (I ** 2).sum()
k = len(s)
ipca_df = [n_ent + E - 1 - 2 * (i + 1) for i in range(4)]
ms_err_ent = ms_err
ipca = []
for i in range(4):
    msi = ss_int[i] / ipca_df[i]
    Fi = msi / ms_err_ent
    ipca.append((i + 1, ipca_df[i], ss_int[i], 100 * ss_int[i] / ss_int_total, Fi, stats.f.sf(Fi, ipca_df[i], df["Error"])))
sc_ent = U[:, :2] * np.sqrt(s[:2])
sc_env = Vt[:2, :].T * np.sqrt(s[:2])
# sign so that the NBC/drought direction is positive-down irrelevant; keep raw
ASV = np.sqrt((ss_int[0] / ss_int[1] * sc_ent[:, 0]) ** 2 + sc_ent[:, 1] ** 2)
rank_asv = stats.rankdata(ASV)
rank_y = stats.rankdata(-em)
YSI = rank_asv + rank_y
# WAASB (Olivoto et al. 2019) using all significant IPCAs (here first 2 for demo)
ep = lam2 / lam2.sum()
nk = 3
WAASB = (np.abs(U[:, :nk] * np.sqrt(s[:nk])) * ep[:nk]).sum(1) / ep[:nk].sum()
# Finlay-Wilkinson
Ie = evm - mm
bFW = np.array([np.polyfit(Ie, M[i], 1)[0] for i in range(n_ent)])
s2d = np.array([np.var(M[i] - np.polyval(np.polyfit(Ie, M[i], 1), Ie), ddof=2) for i in range(n_ent)])

entlab = ["G%d·%s" % (g + 1, ["C", "B", "N"][a]) for g, a in ent]
amcol = [C["ink2"], C["orange"], C["blue"]]
amk = ["o", "s", "D"]

if __name__ == "__main__":
    fig, axs = plt.subplots(1, 3, figsize=(180 * MM, 64 * MM),
                            gridspec_kw=dict(width_ratios=[1, 1.15, 0.9]))
    fig.subplots_adjust(wspace=0.42)
    ax = axs[0]
    xs = np.linspace(Ie.min() - 0.1, Ie.max() + 0.1, 10)
    for a in range(A):
        ya = m_ae[a]
        b, c0 = np.polyfit(Ie, ya, 1)
        ax.plot(Ie, ya, amk[a], ms=4, color=amcol[a], mec="white", mew=0.5)
        ax.plot(xs, b * xs + c0, color=amcol[a], lw=1.3, label="%s (b = %.2f)" % (amend[a], b))
    ax.legend(loc="lower right", handlelength=0.9, fontsize=5.7, borderaxespad=0.1, handletextpad=0.4)
    ax.set_xlim(xs[0] - 0.1, xs[-1] + 0.1)
    ax.set_xlabel("Environmental index (t ha$^{-1}$)")
    ax.set_ylabel("Mean grain yield (t ha$^{-1}$)")
    ax.set_title("Finlay–Wilkinson response", loc="left")
    panel(ax, "a", -0.24)

    ax = axs[1]
    ax.axhline(0, color=C["ink2"], lw=0.6)
    ax.axvline(mm, color=C["ink2"], lw=0.6, ls=(0, (3, 2)))
    for i, (g, a) in enumerate(ent):
        ax.plot(em[i], sc_ent[i, 0], amk[a], ms=4.5, color=amcol[a], mec="white", mew=0.5, zorder=3)
    for j in range(E):
        ax.plot(evm[j], sc_env[j, 0], "^", ms=5, color=C["green"], mec="white", mew=0.5, zorder=3)
        ax.text(evm[j], sc_env[j, 0] + 0.045, envlab[j], fontsize=5.8, ha="center", color=C["ink"])
    for a in range(A):
        ax.plot([], [], amk[a], color=amcol[a], ms=4.5, label=amend[a])
    ax.plot([], [], "^", color=C["green"], ms=5, label="Environment")
    ax.legend(loc="upper right", handletextpad=0.3, borderaxespad=0.1, fontsize=6.0, labelspacing=0.3)
    ax.set_xlabel("Mean yield (t ha$^{-1}$)")
    ax.set_ylabel("IPCA1 score (t ha$^{-1}$)$^{1/2}$")
    ax.set_title("AMMI1 biplot", loc="left")
    panel(ax, "b", -0.22)

    ax = axs[2]
    for a in range(A):
        idx = [i for i, (g, aa) in enumerate(ent) if aa == a]
        jit = np.linspace(-0.12, 0.12, len(idx))
        ax.plot(a + jit, ASV[idx], amk[a], ms=4.5, color=amcol[a], mec="white", mew=0.5)
        ax.plot([a - 0.25, a + 0.25], [np.median(ASV[idx])] * 2, color=C["ink"], lw=1.2)
    ax.set_xticks(range(A)); ax.set_xticklabels(["Control", "Bulk BC", "NBC"])
    ax.set_ylabel("AMMI stability value (ASV)")
    ax.set_xlim(-0.6, 2.6)
    ax.set_title("Stability by amendment", loc="left")
    panel(ax, "c", -0.3)
    save(fig, "Fig8_simulated_MET")

    out = dict(anova=[[a[0], int(a[1]), round(a[2], 2), round(a[3], 3), None if np.isnan(a[4]) else round(a[4], 2),
                       None if np.isnan(a[5]) else float("%.2g" % a[5]), round(a[6], 1)] for a in anova],
               ipca=[[i[0], int(i[1]), round(i[2], 2), round(i[3], 1), round(i[4], 2), float("%.2g" % i[5])] for i in ipca],
               entries=[[entlab[i], round(em[i], 2), round(sc_ent[i, 0], 3), round(sc_ent[i, 1], 3), round(ASV[i], 3),
                         int(rank_asv[i]), int(rank_y[i]), int(YSI[i]), round(WAASB[i], 3), round(bFW[i], 2)] for i in range(n_ent)],
               amend_means=[round(x, 2) for x in m_a], b_amend=[round(np.polyfit(Ie, m_ae[a], 1)[0], 2) for a in range(A)],
               med_asv=[round(float(np.median(ASV[[i for i, (g, aa) in enumerate(ent) if aa == a]])), 3) for a in range(A)],
               cv=round(100 * np.sqrt(ms_err) / gm, 1), grand=round(gm, 2), env_means=[round(x, 2) for x in m_e])
    json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "met_results.json"), "w"), indent=1, ensure_ascii=False)
    print(json.dumps(out, ensure_ascii=False)[:3000])
