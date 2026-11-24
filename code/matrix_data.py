"""Evidence-graded synergy-antagonism matrix (revised version, used by fig5.py, fig5b.py
and make_table_s1.py).

Scores are for an aerobic, coarse-textured, alkaline-to-calcareous dryland soil, except the
CH4 column, which applies only to flooded soils (irrigated rice) and is shown hatched.

Each cell: (score, grade, medium, original_score, original_grade, basis)
  score  : -2..+2 (antagonism .. synergy)
  grade  : A meta-analysis or multi-site field data; B replicated laboratory studies;
           C single or few studies; D mechanistic inference only (no direct test on the lever)
  medium : w aqueous batch; s soil incubation, pot or packed column; f field; m inference only
  original_score/grade : values in the first submission (for the audit trail in ESM Table S1)
"""

levers = ["Size reduction (<100 nm)", "Surface oxidation (–COOH, quinones)",
          "MnO$_2$ (birnessite) loading", "Fe$_3$O$_4$ loading", "Fe(III) oxyhydroxide loading",
          "Mg/Al-LDH loading", "N/S-donor grafting (amine, thiol)"]
levers_plain = ["Size reduction (<100 nm)", "Surface oxidation (–COOH, quinones)",
                "MnO2 (birnessite) loading", "Fe3O4 loading", "Fe(III) oxyhydroxide loading",
                "Mg/Al-LDH loading", "N/S-donor grafting (amine, thiol)"]
outcomes = ["Persistence\nof char-C", "Rhizodeposit\nretention", "CH$_4$ mitigation\n(flooded only)",
            "N$_2$O\nmitigation", "Cationic metal\nimmobilisation", "Oxyanion\nimmobilisation",
            "Colloid\nretention", "Eco-safety"]
outcomes_plain = ["Persistence of char-C", "Rhizodeposit retention / negative priming",
                  "CH4 mitigation (flooded soils only)", "N2O mitigation",
                  "Cationic metal immobilisation", "Oxyanion immobilisation",
                  "Colloid retention", "Eco-safety"]
FLOODED_COL = 2

D0 = "No study isolates this lever for this function; no effect expected from mechanism."

S = [
    # 1 Size reduction
    [(-1, "C", "s", -1, "C", "Finer (<0.42 mm) char mineralised 2–54% more CO2-C than >2 mm pellets of the same char in 8 of 8 soil × feedstock combinations over 50 d (Sigua et al. 2014); oxidation scales with accessible surface (Zimmerman 2010). No nanoscale data; exponent β unmeasured."),
     (1, "D", "m", 1, "C", "Milling speeds sorption kinetics (Lyu et al. 2018, Ni(II), aqueous), so faster capture of short-lived exudate solutes is plausible. No study has measured exudate retention or root-derived C turnover as a function of char particle size. Regraded C→D."),
     (0, "D", "m", 0, "C", "No CH4 study compares nano- and bulk char of the same material. Regraded C→D."),
     (1, "D", "m", 1, "C", "NBC lowered N2O mainly in pot and saline-soil studies against untreated controls (Sultan et al. 2024); no same-char bulk-versus-nano comparison traced, so the effect cannot be attributed to size. Regraded C→D."),
     (1, "B", "w", 1, "B", "Ball milling raised Ni(II) sorption 2–25-fold for the same chars through faster intraparticle diffusion and new O-groups (Lyu et al. 2018); aqueous batch only."),
     (0, "D", "m", 0, "C", "Milling adds oxygenated (negative) groups that do not favour oxyanions; no direct test. Regraded C→D."),
     (-2, "B", "s", -2, "B", "Nano-sized biochar particles travelled further than micrometre particles of the same char in saturated sand columns (Wang et al. 2013); colloid filtration theory (Eq. 3)."),
     (-1, "D", "m", -1, "C", "Persistent free radicals in biochar inhibited germination and seedling growth (Liao et al. 2014); that milling increases radical exposure is inferred, not tested. Regraded C→D.")],
    # 2 Surface oxidation
    [(-1, "C", "s", -1, "C", "Higher O:C ratio predicts shorter biochar half-life across incubation studies (Spokas 2010)."),
     (1, "D", "m", 1, "C", "Carboxylates can bind exudate-derived C through Ca2+ bridges in calcareous soils (mechanism established for SOM: Rowley et al. 2018); not tested for oxidised char. Regraded C→D."),
     (0, "D", "m", 0, "D", D0),
     (1, "C", "s", 1, "B", "Biochar lowered the N2O/(N2O+N2) ratio in 14 soils, attributed to acid buffering and electron shuttling (Cayuela et al. 2013). Acid buffering does not operate at alkaline pH, so only the electron-shuttle part applies in dryland soils. Regraded B→C."),
     (1, "B", "w", 1, "B", "Carboxyl and phenolic groups complex Pb(II), Cu(II) and Cd(II) (review: Li et al. 2017); aqueous."),
     (-1, "B", "s", -1, "B", "Added negative charge repels anions; across 48 studies, biochar often increased As mobility in soil (Arabi et al. 2021)."),
     (-1, "C", "s", -1, "B", "Oxidation raises negative surface charge and lowers attachment efficiency α (Eq. 3); aged biochar colloids altered Tl(I) co-transport in quartz sand depending on ageing degree and pH (Yang et al. 2024). Regraded B→C."),
     (0, "D", "m", 0, "D", D0)],
    # 3 MnO2
    [(-1, "D", "m", -1, "C", "Mn(III/IV) oxides oxidise lignin-derived phenols and drive long-term litter decomposition (Keiluweit et al. 2015a); oxidation of the char itself not tested. Regraded C→D."),
     (0, "D", "m", 0, "D", "Mn oxides may both sorb and oxidise exudate C; net direction unknown."),
     (1, "D", "m", 1, "C", "Mn(IV) is a thermodynamically favourable acceptor that should outcompete methanogens (Eq. 6, Fig. 3); no CH4 data traced for MnO2–char. Flooded soils only. Regraded C→D."),
     (-1, "D", "m", -1, "D", "Cu(II) sequestration (2.2 mmol g−1; Zhou et al. 2017) could limit Cu supply to NosZ (Richardson et al. 2009); untested."),
     (2, "B", "w", 2, "B", "Cu(II) 142.02 vs 26.88 mg g−1 for pristine char (Zhou et al. 2017); Pb(II) 153.1 mg g−1 (Wang et al. 2015a); Pb(II) 47 g kg−1 on birnessite–char (Wang et al. 2015c); aqueous."),
     (1, "B", "w", 2, "B", "Birnessite–char raised As(V) sorption from 0.20 to 0.91 g kg−1 (Wang et al. 2015c); birnessite oxidises As(III) to As(V) (Scott and Morgan 1995). Oxyanion sorption on oxides weakens above pH 8.5 (Smedley and Kinniburgh 2002), so the score is lowered for alkaline soils (+2→+1)."),
     (0, "D", "m", 1, "C", "Birnessite is negatively charged above pH ≈ 2 (Kosmulski 2009), so it cannot raise α by charge reversal; original +1 not supported (+1→0)."),
     (0, "D", "m", -1, "C", "Mn2+ release requires reductive dissolution, which is minor in aerobic alkaline soils; −1 would apply under flooding (−1→0 for drylands).")],
    # 4 Fe3O4
    [(0, "D", "m", 0, "D", D0),
     (1, "D", "m", 1, "C", "Fe oxides bind dissolved organic C by ligand exchange (Kleber et al. 2021); magnetite–char not tested with exudates. Regraded C→D."),
     (-1, "B", "s", -1, "B", "Magnetite and hematite accelerated methanogenesis through electric syntrophy in paddy-soil enrichments (Kato et al. 2012). Flooded soils only."),
     (0, "D", "m", 0, "D", D0),
     (1, "B", "w", 1, "B", "Magnetic biochars sorb divalent metals (review: Yi et al. 2020); aqueous."),
     (1, "B", "w", 2, "B", "Magnetic (hematite-derived) biochar retained As(V) in batch tests (Wang et al. 2015b); weaker at alkaline pH (Smedley and Kinniburgh 2002) (+2→+1)."),
     (0, "D", "m", 1, "C", "Magnetite PZC ≈ 6.5 (Kosmulski 2009) lies below dryland soil pH, so the surface is negative and does not raise α (+1→0)."),
     (0, "D", "m", 0, "C", D0)],
    # 5 Fe(III) oxyhydroxide
    [(1, "D", "m", 1, "C", "Fe(III) phases are stable in aerobic soils, and Fe-bound C is lost mainly when Fe(III) is reduced (Huang and Hall 2017); protection of the char itself is inferred. Regraded C→D."),
     (1, "D", "m", 1, "C", "Strong analogue evidence: exudates formed stable C on reactive minerals but depleted MAOC on low-activity clays (Liang et al. 2023); oxalate exudates release mineral-bound C (Keiluweit et al. 2015b). Not tested on Fe-loaded char. Regraded C→D."),
     (1, "C", "s", 1, "C", "Goethite-modified biochar cut CH4 by 26.3% in a Cd-contaminated paddy (Wang et al. 2025); ferrihydrite at 15–30 g kg−1 cut CH4 by 43–84% in rice microcosms (Jäckel and Schnell 2000). Flooded soils only."),
     (0, "D", "m", 0, "D", D0),
     (1, "B", "s", 1, "B", "FeCl3-modified straw chars immobilised Cd(II) in a Cd–As soil incubation (Wang et al. 2020)."),
     (2, "B", "s", 2, "A", "Fe(III) oxyhydroxides bind As(V) as bidentate inner-sphere complexes (EXAFS; Waychunas et al. 1993); FeCl3-modified char cut TCLP-extractable As(V) by 95% after a 10-d soil incubation (Wang et al. 2020), whereas pristine char often mobilises As (Arabi et al. 2021). No meta-analysis or multi-site field study of Fe-loaded char exists, so the original grade A is withdrawn (A→B). Ferrihydrite PZC ≈ 8 (Kosmulski 2009): sorption weakens but remains strongest among the levers at pH 8–8.5."),
     (0, "D", "m", 1, "C", "At pH above the PZC of goethite and ferrihydrite (≈7.5–9; Kosmulski 2009) the oxide surface is not positively charged, so α is not raised in alkaline soils (+1→0)."),
     (0, "D", "m", 0, "C", D0)],
    # 6 LDH
    [(0, "D", "m", 0, "D", D0),
     (1, "D", "m", 1, "C", "Anion exchange could retain carboxylates, but carbonate is strongly preferred in the interlayer (Goh et al. 2008). Regraded C→D."),
     (0, "D", "m", 0, "D", D0),
     (0, "D", "m", 0, "D", D0),
     (1, "C", "w", 1, "B", "Surface hydroxyls and precipitation retain divalent cations (review of modified chars: Li et al. 2017); no replicated LDH–char cation study traced. Regraded B→C."),
     (1, "B", "w", 2, "B", "MgAl-LDH–char removed phosphate in batch tests (Zhang et al. 2013); carbonate outcompetes other anions for LDH interlayers (Goh et al. 2008), so exchange capacity is expected to be lower in calcareous soils (+2→+1)."),
     (1, "D", "m", 1, "C", "Permanent positive layer charge persists at alkaline pH and should raise α; no transport test of LDH–char traced. Regraded C→D."),
     (0, "D", "m", 0, "C", D0)],
    # 7 N/S grafting
    [(0, "D", "m", 0, "D", D0),
     (0, "D", "m", 0, "D", D0),
     (0, "D", "m", 0, "D", D0),
     (0, "D", "m", 0, "D", D0),
     (2, "C", "w", 2, "B", "Polyaniline–magnetic char: Hg(II) 141.89 and Cu(II) 124.78 mg g−1 (Kareem et al. 2025); single study cited. Regraded B→C."),
     (0, "D", "m", 0, "C", D0),
     (0, "D", "m", 0, "D", D0),
     (-1, "D", "m", -1, "D", "Leachable oligomers; durability of grafted ligands in soil untested.")],
]

assert len(S) == len(levers) and all(len(r) == len(outcomes) for r in S)
