"""extract_event.py DIR STEM OUT.json [EVT] — real rows of one event across the eic2ai CSV files, the input of
make_page.py (the CSV Example Event page).

DIR holds the 18 <STEM>.<role>.csv files of one conversion (eic2ai --compress none). Picks, unless EVT is given, an event whose first
Λ decays to n π⁰ (lam_decay 2), with a calorimeter hit of a π⁰ photon, a calo_clusters cluster with two or more
links, and a reconstructed electron. Writes per-file counts (columns, rows) and the chosen event's rows, column
subsets only, as JSON. Needs pandas. event.json next to this script came from the 2026-11 Sullivan 9×100 file
reco-2026-11-9x100-0001, first 100 events, event 0.
"""
import json
import sys
import pandas as pd

directory, stem, out_path = sys.argv[1:4]
chosen = int(sys.argv[4]) if len(sys.argv) > 4 else None


def load(role, **kw):
    return pd.read_csv(f"{directory}/{stem}.{role}.csv", **kw)


roles = ["event_index", "mc_particles", "mc_dis", "mcpart_lambda", "trk_hits", "cal_hits", "calo_clusters",
         "reco_particles", "reco_dis", "reco_ff_lambda", "lambda_acceptance", "comb_candidates", "comb_candidates_events",
         "acceptance_ppim", "acceptance_ppim_prot_hits", "acceptance_ppim_pimin_hits", "acceptance_npi0", "combinatorics_ppim"]
counts = {}
for role in roles:
    header = open(f"{directory}/{stem}.{role}.csv").readline().rstrip("\n").split(",")
    n_rows = sum(1 for _ in open(f"{directory}/{stem}.{role}.csv")) - 1
    counts[role] = {"columns": len(header), "rows": n_rows, "header": header}

mcp = load("mc_particles")
lam = load("mcpart_lambda")
cal = load("cal_hits")
trk = load("trk_hits")
clu = load("calo_clusters")
rdis = load("reco_dis")
mdis = load("mc_dis")
rpart = load("reco_particles")

first = lam[lam.lam_is_first == 1]
if chosen is None:
    npi0 = set(first[first.lam_decay == 2].evt)
    photon_hits = cal[(cal.prt_pdg == 22) & (cal.prt_primary_pdg == 3122) & (cal.prt_primary_child_pdg == 111)]
    links = clu.groupby(["evt", "clu_collection", "clu_index"]).size()
    multi = set(links[links >= 2].reset_index().evt)
    with_elec = set(rdis[rdis.elec_index >= 0].evt)
    candidates = sorted(npi0 & set(photon_hits.evt) & multi & with_elec)
    print("candidate events:", candidates[:20])
    chosen = candidates[0]
evt = chosen

e_mcp = mcp[mcp.evt == evt]
example = {"evt": int(evt), "stem": stem}
example["mc_particles_rows"] = int(len(e_mcp))
example["mc_particles_by_status"] = {str(k): int(v) for k, v in e_mcp.prt_gen_status.value_counts().items()}
mcp_cols = ["evt", "prt_index", "prt_pdg", "prt_gen_status", "prt_energy", "prt_mom_z", "prt_vtx_pos_z", "prt_end_pos_z",
            "prt_n_daughters", "prt_parent_index"]
generator = e_mcp[e_mcp.prt_gen_status != 0]
example["mc_generator"] = generator[mcp_cols].to_dict("records")

# the first Λ, its daughters, the π⁰ photons
lam_row = first[first.evt == evt].iloc[0]
lam_index = int(lam_row.lam_index)
daughters = e_mcp[e_mcp.prt_parent_index == lam_index]
pi0 = daughters[daughters.prt_pdg == 111]
photons = e_mcp[e_mcp.prt_parent_index.isin(pi0.prt_index)] if len(pi0) else e_mcp.iloc[0:0]
example["mc_lambda_chain"] = pd.concat([e_mcp[e_mcp.prt_index == lam_index], daughters, photons])[mcp_cols].to_dict("records")
example["mc_geant4_by_pdg"] = {str(k): int(v) for k, v in e_mcp[e_mcp.prt_gen_status == 0].prt_pdg.value_counts().head(8).items()}

lam_cols = ["evt", "lam_is_first", "lam_decay", "lam_index", "lam_mom_z", "lam_end_pos_z", "neut_index", "pizero_index",
            "gamone_index", "gamtwo_index"]
example["mcpart_lambda"] = lam[lam.evt == evt][lam_cols].to_dict("records")

mdis_cols = ["evt", "xbj", "q2", "y_d", "w", "tprime"]
example["mc_dis"] = mdis[mdis.evt == evt][[c for c in mdis_cols if c in mdis.columns]].to_dict("records")

hit_cols = ["evt", "cal_hit_system_name", "cal_hit_energy", "cal_hit_time", "sim_energy", "n_contrib", "prt_index", "prt_pdg",
            "prt_gen_status", "prt_primary_index", "prt_primary_pdg", "prt_primary_child_index", "prt_primary_child_pdg"]
e_cal = cal[cal.evt == evt]
example["cal_hits_rows"] = int(len(e_cal))
example["cal_hits_by_system"] = {str(k): int(v) for k, v in e_cal.cal_hit_system_name.value_counts().items()}
photon_hits = e_cal[(e_cal.prt_pdg == 22) & (e_cal.prt_primary_child_pdg == 111)].sort_values("cal_hit_energy", ascending=False)
electron_hits = e_cal[(e_cal.prt_pdg == 11) & (e_cal.prt_gen_status == 1)].sort_values("cal_hit_energy", ascending=False)
neutron_hits = e_cal[(e_cal.prt_primary_child_pdg == 2112)].sort_values("cal_hit_energy", ascending=False)
example["cal_hits_examples"] = pd.concat([electron_hits.head(1), photon_hits.head(2), neutron_hits.head(1)])[hit_cols].to_dict("records")

trk_cols = ["evt", "hit_index", "trk_hit_system_name", "trk_hit_pos_z", "trk_hit_edep", "prt_index", "prt_pdg", "prt_gen_status",
            "prt_primary_index", "prt_primary_pdg", "prt_primary_child_index", "prt_primary_child_pdg"]
e_trk = trk[trk.evt == evt]
example["trk_hits_rows"] = int(len(e_trk))
example["trk_hits_by_system"] = {str(k): int(v) for k, v in e_trk.trk_hit_system_name.value_counts().items()}
example["trk_hits_examples"] = pd.concat([e_trk[e_trk.prt_pdg == 11].head(1), e_trk[e_trk.prt_primary_child_pdg != 0].head(1),
                                          e_trk[e_trk.prt_pdg == 321].head(1)])[trk_cols].to_dict("records")

clu_cols = ["evt", "clu_collection", "clu_index", "clu_link_index", "clu_energy", "clu_nhits", "clu_assoc_weight", "prt_index",
            "prt_pdg", "prt_primary_pdg", "prt_primary_child_pdg"]
e_clu = clu[clu.evt == evt]
example["calo_clusters_rows"] = int(len(e_clu))
example["calo_clusters_clusters"] = int(e_clu.groupby(["clu_collection", "clu_index"]).ngroups)
example["calo_clusters_by_collection"] = {str(k): int(v) for k, v in e_clu.groupby("clu_collection").clu_index.nunique().items()}
links = e_clu.groupby(["clu_collection", "clu_index"]).clu_link_index.transform("size")
multi = e_clu[(links >= 2) & e_clu.clu_collection.str.contains("B0ECal|ZDC")]
if multi.empty:
    multi = e_clu[links >= 2]
first_cluster = multi.iloc[0]
cluster_rows = e_clu[(e_clu.clu_collection == first_cluster.clu_collection) & (e_clu.clu_index == first_cluster.clu_index)]
example["calo_clusters_example"] = cluster_rows[clu_cols].to_dict("records")

rp_cols = ["evt", "rec_index", "rec_pdg", "rec_charge", "rec_energy", "rec_mom_z", "rec_n_clusters", "rec_n_tracks"]
example["reco_particles"] = rpart[rpart.evt == evt][rp_cols].to_dict("records")

rd_cols = ["evt", "mc_x", "mc_q2", "electron_x", "electron_q2", "da_x", "da_q2", "elec_index", "elec_energy", "mc_elec_index",
           "mc_lam_index", "mc_lam_decay", "mc_true_t", "mc_lam_exp_t", "elec_epz_n_candidates", "mc_vtx_pos_z"]
example["reco_dis"] = rdis[rdis.evt == evt][rd_cols].to_dict("records")

json.dump({"counts": counts, "events": int(mcp.evt.nunique()), "example": example}, open(out_path, "w"), indent=1, default=float)
print("event", evt, "| mc_particles rows", len(e_mcp), "| cal_hits", len(e_cal), "| trk_hits", len(e_trk), "| clusters", example["calo_clusters_clusters"])
