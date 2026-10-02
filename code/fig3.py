"""Figure 3. Redox thermodynamics and the electron budget of 'redox poising'."""
import numpy as np
from style import *

F = 96485.0
# ---- (a) E'(pH 7) of terminal electron-accepting couples (V vs SHE) ----
# MnO2/Mn2+: E0 = 1.23 V, 2e-, 4H+ ; [Mn2+] 1e-3..1e-6 M
def E_mno2(mn):
    return 1.23 - 0.05916 * 2 * 7 - 0.02958 * np.log10(mn)
# Fe(III) phases -> Fe2+ (1 e-, 3H+): ferrihydrite E0 ~1.06, goethite E0 ~0.67 ; [Fe2+]=1e-5
def E_fe(E0, fe=1e-5):
    return E0 - 0.05916 * 3 * 7 - 0.05916 * np.log10(fe)
# magnetite Fe3O4 + 8H+ + 2e- -> 3Fe2+ ; E0 0.88-1.08 (dGf Fe2+ dataset dependent)
def E_mag(E0, fe=1e-5):
    return E0 - 0.02958 * (3 * np.log10(fe) + 8 * 7)

couples = [  # label, low, high, colour-key
    ("N$_2$O / N$_2$", 1.355, 1.355, "n"),
    ("O$_2$ / H$_2$O", 0.816, 0.816, "o"),
    ("NO$_3^-$ / N$_2$", 0.75, 0.75, "n"),
    ("MnO$_2$ / Mn$^{2+}$", E_mno2(1e-3), E_mno2(1e-6), "m"),
    ("NO$_3^-$ / NO$_2^-$", 0.43, 0.43, "n"),
    ("Fe(III) oxyhydroxides / Fe$^{2+}$", E_fe(0.67), E_fe(1.06), "f"),
    ("SO$_4^{2-}$ / HS$^-$", -0.217, -0.217, "o"),
    ("Fe$_3$O$_4$ / Fe$^{2+}$", E_mag(0.88), E_mag(1.08), "f"),
    ("CO$_2$ / CH$_4$", -0.244, -0.244, "c"),
    ("H$^+$ / H$_2$", -0.414, -0.414, "o"),
]
colmap = dict(n=C["blue"], o=C["ink2"], m=C["violet"], f=C["orange"], c=C["red"])

# ---- (b) electron budget per hectare per season ----
CH4_kg = 300.0  # kg CH4 ha-1 season-1, continuously flooded rice (typical 100-500)
flux = CH4_kg * 1e3 / 16.04 * 8 / 1e3  # kmol e- ha-1
cap_mno2 = 2 / 86.94 * 1e3   # kmol e- per t
cap_mag = 2 / 231.53 * 1e3   # kmol e- per t (2 Fe(III) per formula unit)
eac = 0.5                    # mmol e- g-1 biochar (reported ~0.1-2)
cap_bc = eac                 # kmol e- per t per redox cycle
rows = [
    ("Seasonal methanogenic electron flow\n(300 kg CH$_4$ ha$^{-1}$)", flux, C["red"]),
    ("1 t MnO$_2$ (Mn$^{IV}$→Mn$^{II}$, one pass)", cap_mno2, C["violet"]),
    ("1 t Fe$_3$O$_4$ (2 Fe$^{III}$, one pass)", cap_mag, C["orange"]),
    ("5 t composite, 20% MnO$_2$ (one pass)", 5 * 0.2 * cap_mno2 + 5 * 0.8 * cap_bc, C["violet"]),
    ("10 t biochar, EAC 0.5 mmol g$^{-1}$, 1 cycle", 10 * cap_bc, C["aqua"]),
    ("10 t biochar, 10 re-oxidation cycles", 10 * cap_bc * 10, C["aqua"]),
]

if __name__ == "__main__":
    fig, axs = plt.subplots(1, 2, figsize=(180 * MM, 78 * MM),
                            gridspec_kw=dict(width_ratios=[1, 1.35]))
    fig.subplots_adjust(wspace=1.05)
    ax = axs[0]
    cs = sorted(couples, key=lambda r: (r[1] + r[2]) / 2)
    yy = np.arange(len(cs))
    ax.axvspan(-0.30, -0.15, color="#fbe3e2", lw=0, zorder=0)
    ax.text(-0.225, len(cs) - 0.35, "CH$_4$\nwindow", fontsize=5.8, color=C["red"], ha="center", va="bottom")
    for y_, (lab, lo, hi, k) in zip(yy, cs):
        if abs(hi - lo) > 1e-3:
            ax.plot([lo, hi], [y_, y_], color=colmap[k], lw=3.2, solid_capstyle="round", zorder=3)
        else:
            ax.plot([lo], [y_], "o", ms=4.6, color=colmap[k], mec="white", mew=0.7, zorder=3)
    ax.set_yticks(yy); ax.set_yticklabels([r[0] for r in cs], fontsize=6.4)
    ax.tick_params(axis="y", length=0)
    ax.axvline(0, color=C["grid"], lw=0.6, zorder=0)
    ax.set_xlim(-0.55, 1.5); ax.set_ylim(-0.6, len(cs) + 0.4)
    ax.set_xlabel(r"$E^{\circ\prime}$ at pH 7 (V vs SHE)")
    ax.set_title("Thermodynamic ladder of acceptors", loc="left")
    panel(ax, "a", -0.75)

    ax = axs[1]
    labs = [r[0] for r in rows][::-1]
    vals = [r[1] for r in rows][::-1]
    cols = [r[2] for r in rows][::-1]
    yy = np.arange(len(rows))
    ax.barh(yy, vals, color=cols, height=0.62, edgecolor="white", linewidth=1.0)
    for y_, v in zip(yy, vals):
        ax.text(v + 3, y_, "%.0f" % v if v >= 10 else "%.1f" % v, va="center", fontsize=6.6, color=C["ink"])
    ax.axvline(flux, color=C["red"], lw=0.7, ls=(0, (3, 2)))
    ax.set_yticks(yy); ax.set_yticklabels(labs, fontsize=6.4)
    ax.set_xlabel("Electrons (kmol e$^-$ ha$^{-1}$)")
    ax.set_xlim(0, 190)
    ax.tick_params(axis="y", length=0)
    ax.set_title("Electron budget of 'redox poising'", loc="left")
    panel(ax, "b", -0.78)
    save(fig, "Fig3_redox_budget")
    print("flux kmol e/ha", flux, "MnO2 t needed", flux / cap_mno2, "Fe3O4 t needed", flux / cap_mag,
          "biochar t per cycle", flux / cap_bc)
    print("MnO2 E range", E_mno2(1e-3), E_mno2(1e-6), "Fe", E_fe(0.67), E_fe(1.06), "mag", E_mag(0.88), E_mag(1.08))
    print("caps", cap_mno2, cap_mag, "composite", 5 * 0.2 * cap_mno2 + 5 * 0.8 * cap_bc)
