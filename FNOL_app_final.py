import base64
import streamlit as st
import sys
import html as html_lib
import re
from datetime import datetime, timedelta, timezone
from textwrap import dedent

sys.path.insert(0, r"C:\Users\user\claims_ui")

from kognitos_data import (
    get_claim_runs,
    get_run_details,
    extract_claim_data
)


# ============================================================
# PAGE
# ============================================================

st.set_page_config(
    page_title="Claims Assistant",
    page_icon="K",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# HTML HELPER
# ============================================================

def html(content):
    return st.html(dedent(content).strip())


def safe(value):
    return html_lib.escape(str(value or ""))


# ============================================================
# CSS
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

.stApp {
    background:#f5f6f9;
    color:#132238;
}

.block-container {
    padding:0 32px 40px 32px;
    max-width:1900px;
}

/* FNOL DASHBOARD TOP IDENTITY STRIP */

.topstrip {
    display:flex;
    align-items:center;
    justify-content:space-between;
    padding:14px 30px;
    margin:0 -32px 22px -32px;
    background:#ffffff;
    border-bottom:1px solid #E1E4EA;
    box-sizing:border-box;
}

.brand {
    display:flex;
    align-items:center;
    gap:10px;
}

.brand-mark {
    width:30px;
    height:30px;
    border-radius:8px;
    background:linear-gradient(135deg,#565B66,#3A3D45);
    display:flex;
    align-items:center;
    justify-content:center;
    color:white;
    font-family:'Space Grotesk',sans-serif;
    font-weight:700;
    font-size:14px;
    flex-shrink:0;
}

.brand-text {
    line-height:1.15;
}

.brand-text .t1 {
    font-family:'Space Grotesk',sans-serif;
    font-weight:600;
    font-size:13.5px;
    color:#24262B;
}

.brand-text .t2 {
    font-size:10.5px;
    color:#8992A3;
    letter-spacing:.03em;
}

.user-chip {
    display:flex;
    align-items:center;
    gap:9px;
    padding:6px 4px;
}

.user-avatar {
    width:28px;
    height:28px;
    border-radius:50%;
    background:#565B66;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:11px;
    font-weight:700;
    color:#fff;
    font-family:'Space Grotesk',sans-serif;
    flex-shrink:0;
}

.user-meta .u1 {
    font-size:12.5px;
    font-weight:600;
    color:#24262B;
}

.user-meta .u2 {
    font-size:10.5px;
    color:#8992A3;
}

/* TOP HEADER */

.app-top-header {
    height: 76px;
    background: #ffffff;
    margin: -0px -32px 24px -32px;
    padding: 0 34px;
    border-bottom: 1px solid #dfe3e8;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-sizing: border-box;
}

.app-brand {
    display: flex;
    align-items: center;
    gap: 12px;
}

.app-logo {
    width: 34px;
    height: 34px;
    border-radius: 9px;
    background: #4b5565;
    color: #ffffff;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 17px;
}

.app-title {
    font-size: 15px;
    font-weight: 700;
    color: #172235;
    line-height: 18px;
}

.app-subtitle {
    font-size: 12px;
    color: #70809a;
    line-height: 15px;
}

.app-user {
    display: flex;
    align-items: center;
    gap: 10px;
}

.user-avatar {
    width: 34px;
    height: 34px;
    border-radius: 50%;
    background: #596273;
    color: #ffffff;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 11px;
}

.user-name {
    font-size: 13px;
    font-weight: 700;
    color: #172235;
}

.user-role {
    font-size: 11px;
    color: #70809a;
}


/* HEADER */

.app-header {
    height:78px;
    background:#ffffff;
    margin:0 -32px 26px -32px;
    padding:0 34px;
    border-bottom:1px solid #dfe3e8;
    display:flex;
    align-items:center;
    justify-content:space-between;
    box-sizing:border-box;
}

.brand {
    display:flex;
    align-items:center;
    gap:12px;
}

.logo {
    width:34px;
    height:34px;
    border-radius:9px;
    background:#4b5565;
    color:white;
    display:flex;
    align-items:center;
    justify-content:center;
    font-weight:700;
    font-size:17px;
}

.brand-name {
    font-size:15px;
    font-weight:700;
    color:#172235;
}

.brand-sub {
    font-size:12px;
    color:#70809a;
}

.profile {
    display:flex;
    align-items:center;
    gap:10px;
}

.avatar {
    width:34px;
    height:34px;
    border-radius:50%;
    background:#596273;
    color:white;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:11px;
    font-weight:700;
}

.profile-name {
    font-size:13px;
    font-weight:700;
    color:#172235;
}

.profile-role {
    font-size:11px;
    color:#718096;
}

/* TITLE */

.page-title {
    font-size:24px;
    font-weight:700;
    color:#152338;
    margin-bottom:3px;
}

.page-subtitle {
    font-size:14px;
    color:#52657e;
}

.live {
    text-align:right;
    font-size:12px;
    color:#7890aa;
}

.live-dot {
    color:#17995b;
    font-size:16px;
}

/* CARDS */

.card {
    background:#ffffff;
    border:1px solid #dce2e9;
    border-radius:11px;
    padding:16px 18px;
    height:94px;
    box-sizing:border-box;
}

.card.primary {
    border:2px solid #2379a5;
}

.card-label {
    font-size:12px;
    font-weight:700;
    color:#56677f;
    letter-spacing:.2px;
}

.card-number {
    font-size:29px;
    font-weight:500;
    color:#152338;
    margin-top:8px;
}

.card-number.red {
    color:#d2382d;
}

.dot-blue {color:#277ba2;}
.dot-green {color:#269b61;}
.dot-orange {color:#c17b0b;}
.dot-red {color:#c63d32;}

/* FILTER */

.search-box {
    background:white;
    border:1px solid #d8dee6;
    border-radius:9px;
    padding:10px 14px;
}

/* TABLE */

.claim-table {
    background:white;
    border:1px solid #dce2e9;
    border-radius:12px;
    overflow:hidden;
}

.table-header {
    display:grid;
    grid-template-columns:
        1.25fr
        1.55fr
        1.15fr
        .90fr
        .85fr
        1.05fr
        .85fr
        1.80fr
        .55fr;
    padding:11px 18px;
    background:#ffffff;
    border-bottom:1px solid #dce2e9;
    color:#718198;
    font-size:11px;
    font-weight:700;
    letter-spacing:.5px;
    box-sizing:border-box;
}

.claim-row {
    display:grid;
    grid-template-columns:
        1.25fr
        1.55fr
        1.15fr
        .90fr
        .85fr
        1.05fr
        .85fr
        1.80fr
        .55fr;
    padding:14px 18px;
    border-bottom:1px solid #e6e9ee;
    align-items:center;
    min-height:70px;
    box-sizing:border-box;
}

.claim-row:hover {
    background:#fafbfd;
}

.claim-name {
    font-size:14px;
    font-weight:700;
    color:#142238;
}

.claim-id {
    font-size:11px;
    color:#73839a;
    margin-top:3px;
}

.org-name {
    font-size:13px;
    color:#263c58;
}

.org-location {
    font-size:11px;
    color:#8190a5;
    margin-top:3px;
}

.received {
    font-size:13px;
    color:#233954;
}

.received-relative {
    font-size:12px;
    color:#172238;
    margin-top:2px;
}

.mode {
    background:#eef1f5;
    color:#56657a;
    padding:5px 9px;
    border-radius:7px;
    display:inline-block;
    font-size:11px;
}

.doc {
    display:inline-flex;
    width:24px;
    height:24px;
    border-radius:6px;
    align-items:center;
    justify-content:center;
    margin-right:3px;
    font-size:11px;
    font-weight:700;
    box-sizing:border-box;
}

.doc-ok {
    background:#e8f7f0;
    color:#219b62;
    border:1px solid #bfe8d3;
}

.doc-missing {
    background:#fff0ef;
    color:#d4483c;
    border:1px solid #f2c5c0;
}

.doc-warning {
    background:#fff7e7;
    color:#c47a00;
    border:1px solid #f1d08b;
}

.doc-neutral {
    background:#f1f3f5;
    color:#8a95a5;
    border:1px solid #dfe3e8;
}

.status {
    display:inline-block;
    padding:6px 10px;
    border-radius:14px;
    font-size:11px;
    font-weight:600;
    white-space:nowrap;
}

.status-registered {
    background:#e5f6ed;
    color:#258c5a;
}

.status-waiting {
    background:#fff2dc;
    color:#ad710b;
}

.status-hitl {
    background:#fde9e7;
    color:#c53c32;
}

.hitl-no {
    background:#eef1f5;
    color:#68768a;
    padding:6px 12px;
    border-radius:7px;
    font-size:11px;
}

.hitl-yes {
    background:#fff0ef;
    color:#d3463b;
    border:1px solid #f2c0bb;
    padding:5px 12px;
    border-radius:7px;
    font-size:11px;
}

.notes {
    color:#6e7e94;
    font-size:12px;
    line-height:1.35;
}

.view-btn {
    display:inline-block;
    background:#e9f2f7;
    color:#12618c !important;
    padding:7px 11px;
    border-radius:7px;
    font-weight:700;
    font-size:12px;
    text-align:center;
    text-decoration:none !important;
    white-space:nowrap;
}

.view-btn:hover {
    background:#dcecf5;
}

div[data-testid="stButton"] button {
    border:none !important;
    background:#e9f2f7 !important;
    color:#12618c !important;
    border-radius:7px !important;
    font-size:12px !important;
    font-weight:700 !important;
    padding:5px 10px !important;
    min-height:30px !important;
}

div[data-testid="stButton"] button:hover {
    background:#dcecf5 !important;
}

/* RADIO */

div[data-testid="stRadio"] > div {
    gap:8px;
}

div[data-testid="stRadio"] label {
    font-size:13px !important;
}

/* DETAIL */

.detail-card {
    background:white;
    border:1px solid #dce2e9;
    border-radius:12px;
    padding:22px;
    margin-top:18px;
}

.detail-label {
    font-size:11px;
    color:#7a889b;
    text-transform:uppercase;
    font-weight:700;
}

.detail-value {
    font-size:15px;
    color:#18283d;
    margin-top:4px;
    margin-bottom:15px;
}


/* ============================================================
   CLAIM DETAILS RIGHT-SIDE DRAWER
   ============================================================ */

@keyframes kDrawerIn { from {transform:translateX(100%);} to {transform:translateX(0);} }
@keyframes kFadeIn { from {opacity:0;} to {opacity:1;} }

.drawer-overlay {
    position:fixed !important;
    top:0; left:0; right:0; bottom:0;
    width:100vw !important; height:100vh !important;
    background:rgba(20,27,46,.38);
    z-index:9998;
    display:block;
    animation:kFadeIn .18s ease;
}

/* Older Streamlit hides zero-height st.html blocks; keep the overlay's container. */
div[data-testid="stElementContainer"]:has(.drawer-overlay) { display:block !important; }

.sr-only {
    position:absolute; width:1px; height:1px; overflow:hidden; clip:rect(0 0 0 0); white-space:nowrap;
}

.st-key-detail_drawer {
    position:fixed !important;
    top:0 !important;
    right:0 !important;
    bottom:0 !important;
    width:min(720px, 94vw) !important;
    max-width:94vw !important;
    height:100vh !important;
    z-index:9999 !important;
    background:#F4F5F8 !important;
    box-shadow:-16px 0 40px rgba(20,27,46,.18) !important;
    padding:0 !important;
    gap:0 !important;
    overflow-y:auto !important;
    overflow-x:hidden !important;
    box-sizing:border-box !important;
    animation:kDrawerIn .22s ease;
    font-family:'Inter',sans-serif;
    color:#1B2233;
}

.st-key-detail_drawer [data-testid="stVerticalBlock"] { gap:0 !important; }
.st-key-detail_drawer [data-testid="stElementContainer"] {
    margin:0 !important; width:100% !important; max-width:100% !important;
}
.st-key-detail_drawer .stHtml { width:100% !important; }
.st-key-detail_drawer .mono { font-family:'JetBrains Mono',monospace; }

/* Header (sticky) — sticky goes on Streamlit's layout wrapper */
/* Works across Streamlit versions (with or without a wrapper div) */
.st-key-detail_drawer > .st-key-drawer_head,
.st-key-detail_drawer > div:has(.st-key-drawer_head) {
    position:sticky !important; top:0; z-index:5; flex-shrink:0;
}
.st-key-drawer_head {
    position:relative;
    background:#FFFFFF;
    border-bottom:1px solid #E1E4EA;
}
.dh { padding:20px 26px; }
.dh-top {
    display:flex; justify-content:space-between; align-items:flex-start;
    margin-bottom:14px; gap:16px;
}
.dh-title {
    font-family:'Space Grotesk',sans-serif; font-size:19px; font-weight:600; color:#24262B;
}
.dh-id { font-size:11.5px; color:#8992A3; margin-top:2px; }
.sg { display:grid; grid-template-columns:repeat(3,1fr); gap:12px 20px; }
.sg-label {
    font-size:10px; text-transform:uppercase; letter-spacing:.05em;
    color:#8992A3; font-weight:600; margin-bottom:2px;
}
.sg-value { font-size:13px; color:#1B2233; font-weight:500; }

.dh-back {
    display:inline-flex; align-items:center; gap:6px; margin-bottom:12px;
    font-size:12px; font-weight:600; color:#2C6E8E !important; text-decoration:none !important;
    padding:4px 8px 4px 4px; border-radius:6px;
}
.dh-back:hover { background:#E7F0F4; }
.dh-right { display:flex; align-items:center; gap:10px; flex-shrink:0; }
.dh-close {
    width:30px; height:30px; border-radius:8px; border:1px solid #E1E4EA; background:#FFFFFF;
    display:flex; align-items:center; justify-content:center; color:#5B6472 !important;
    text-decoration:none !important; font-size:15px; line-height:1;
}
.dh-close:hover { background:#EDEFF3; }

/* Status badge */
.sbadge {
    display:inline-flex; align-items:center; gap:6px; font-size:11.5px; font-weight:600;
    padding:4px 10px 4px 8px; border-radius:20px; white-space:nowrap;
}
.sbadge .sdot { width:6px; height:6px; border-radius:50%; }
.sb-approved { background:#E5F5ED; color:#1E8E5A; } .sb-approved .sdot { background:#1E8E5A; }
.sb-waiting  { background:#FBF0DD; color:#B8720A; } .sb-waiting .sdot  { background:#B8720A; }
.sb-hitl     { background:#FBE7E4; color:#C0392B; } .sb-hitl .sdot     { background:#C0392B; }

/* Body */
.st-key-detail_drawer > .st-key-drawer_body,
.st-key-detail_drawer > div:has(.st-key-drawer_body) { flex:1 0 auto !important; }
.st-key-drawer_body { padding:20px 26px 30px !important; }
.st-key-drawer_head, .st-key-drawer_body, .st-key-drawer_actions {
    box-sizing:border-box !important; width:100% !important; max-width:100% !important;
}

.alert-box {
    border-radius:10px; padding:13px 15px; font-size:12.5px; line-height:1.55;
    display:flex; gap:10px; margin-bottom:16px;
}
.alert-box.amber { background:#FBF0DD; border:1px solid #F0DBAF; color:#7A4E06; }
.alert-box.red   { background:#FBE7E4; border:1px solid #F2C9C3; color:#8A2A20; }
.alert-box.green { background:#E5F5ED; border:1px solid #C3E5D3; color:#125A38; }
.alert-box svg { width:16px; height:16px; flex-shrink:0; margin-top:1px; }
.alert-box b { font-weight:700; }
.alert-box .sla { margin-top:6px; font-family:'JetBrains Mono',monospace; font-size:11.5px; }

.panel {
    background:#FFFFFF; border:1px solid #E1E4EA; border-radius:12px;
    margin-bottom:16px; overflow:hidden;
}
.panel-head {
    padding:13px 18px; border-bottom:1px solid #EDEFF3;
    display:flex; align-items:center; justify-content:space-between;
}
.panel-title {
    font-family:'Space Grotesk',sans-serif; font-size:13.5px; font-weight:600;
    color:#24262B; display:flex; align-items:center; gap:8px;
}
.panel-body { padding:16px 18px; }


/* Document tabs — pure CSS (radio inputs), identical in every Streamlit version */
.doc-tabs-wrap { padding:16px 18px; }
.doc-tabs-wrap > input[type="radio"] { position:absolute; opacity:0; pointer-events:none; }
.doc-tabs {
    display:flex; gap:4px; padding:4px; background:#EDEFF3; border-radius:9px; margin-bottom:14px;
}
.doc-tab {
    flex:1; text-align:center; padding:8px 6px; border-radius:7px; font-size:12px; font-weight:600;
    cursor:pointer; color:#5B6472; display:flex; align-items:center; justify-content:center; gap:6px;
    user-select:none; margin:0;
}
.doc-tab:hover { color:#24262B; }
.doc-tab-flag { width:7px; height:7px; border-radius:50%; flex-shrink:0; background:#C7CCD8; }
.doc-tab-flag.ok { background:#1E8E5A; }
.doc-tab-flag.warn { background:#B8720A; }
.doc-tab-flag.bad { background:#C0392B; }
.doc-pane { display:none; }
#dt-froi:checked ~ .doc-tabs label[for="dt-froi"],
#dt-fmr:checked ~ .doc-tabs label[for="dt-fmr"],
#dt-emp:checked ~ .doc-tabs label[for="dt-emp"] {
    background:#FFFFFF; color:#24262B; box-shadow:0 1px 2px rgba(20,27,46,.08);
}
#dt-froi:checked ~ .doc-pane-froi,
#dt-fmr:checked ~ .doc-pane-fmr,
#dt-emp:checked ~ .doc-pane-emp { display:block; }

.doc-render { border:1px solid #E1E4EA; border-radius:9px; overflow:hidden; background:#FBFBFB; }
.doc-letterhead {
    background:#24262B; color:#fff; padding:12px 16px;
    display:flex; justify-content:space-between; align-items:center;
}
.doc-letterhead .dtitle { font-family:'Space Grotesk',sans-serif; font-size:13px; font-weight:600; }
.doc-letterhead .dsub { font-size:10px; color:#98A2B8; font-family:'JetBrains Mono',monospace; }
.doc-fields { padding:14px 16px; display:grid; grid-template-columns:1fr 1fr; gap:10px 16px; }
.doc-field { padding:9px 10px; border-radius:7px; border-left:3px solid #E1E4EA; background:#FFFFFF; }
.doc-field.conf-hi  { border-color:#1E8E5A; }
.doc-field.conf-mid { border-color:#B8720A; }
.doc-field.conf-lo  { border-color:#C0392B; }
.df-label {
    font-size:9.5px; text-transform:uppercase; letter-spacing:.04em; color:#8992A3; font-weight:600;
}
.df-row { display:flex; justify-content:space-between; align-items:baseline; gap:8px; margin-top:2px; }
.df-value { font-size:12.5px; color:#1B2233; font-weight:500; }
.df-conf { font-size:9.5px; font-family:'JetBrains Mono',monospace; font-weight:600; flex-shrink:0; }
.df-conf.conf-hi { color:#1E8E5A; } .df-conf.conf-mid { color:#B8720A; } .df-conf.conf-lo { color:#C0392B; }
.doc-empty { padding:34px 20px; text-align:center; }
.doc-empty svg { width:34px; height:34px; color:#8992A3; margin-bottom:10px; }
.doc-empty .de-title { font-size:13px; font-weight:600; color:#1B2233; margin-bottom:4px; }
.doc-empty .de-sub { font-size:12px; color:#5B6472; max-width:340px; margin:0 auto; line-height:1.5; }

/* Icons (CSS masks — st.html strips inline SVG) */
.ic { display:inline-block; width:15px; height:15px; flex-shrink:0; background-color:currentColor; -webkit-mask:var(--ic) center/contain no-repeat; mask:var(--ic) center/contain no-repeat; }
.ic-check { --ic:url("data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A//www.w3.org/2000/svg%22%20viewBox%3D%220%200%2024%2024%22%20fill%3D%22none%22%20stroke%3D%22black%22%20stroke-width%3D%222%22%20stroke-linecap%3D%22round%22%20stroke-linejoin%3D%22round%22%3E%3Cpath%20d%3D%22M20%206L9%2017l-5-5%22/%3E%3C/svg%3E"); }
.ic-warn { --ic:url("data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A//www.w3.org/2000/svg%22%20viewBox%3D%220%200%2024%2024%22%20fill%3D%22none%22%20stroke%3D%22black%22%20stroke-width%3D%222%22%20stroke-linecap%3D%22round%22%20stroke-linejoin%3D%22round%22%3E%3Cpath%20d%3D%22M12%209v4M12%2017h.01M10.3%203.86L1.82%2018a2%202%200%20001.71%203h16.94a2%202%200%20001.71-3L13.7%203.86a2%202%200%2000-3.4%200z%22/%3E%3C/svg%3E"); }
.ic-alert { --ic:url("data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A//www.w3.org/2000/svg%22%20viewBox%3D%220%200%2024%2024%22%20fill%3D%22none%22%20stroke%3D%22black%22%20stroke-width%3D%222%22%20stroke-linecap%3D%22round%22%20stroke-linejoin%3D%22round%22%3E%3Ccircle%20cx%3D%2212%22%20cy%3D%2212%22%20r%3D%2210%22/%3E%3Cpath%20d%3D%22M12%208v5M12%2016h.01%22/%3E%3C/svg%3E"); }
.ic-docs { --ic:url("data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A//www.w3.org/2000/svg%22%20viewBox%3D%220%200%2024%2024%22%20fill%3D%22none%22%20stroke%3D%22black%22%20stroke-width%3D%222%22%20stroke-linecap%3D%22round%22%20stroke-linejoin%3D%22round%22%3E%3Crect%20x%3D%223%22%20y%3D%224%22%20width%3D%2218%22%20height%3D%2216%22%20rx%3D%222%22/%3E%3Cpath%20d%3D%22M3%2010h18%22/%3E%3C/svg%3E"); }
.ic-xval { --ic:url("data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A//www.w3.org/2000/svg%22%20viewBox%3D%220%200%2024%2024%22%20fill%3D%22none%22%20stroke%3D%22black%22%20stroke-width%3D%222%22%20stroke-linecap%3D%22round%22%20stroke-linejoin%3D%22round%22%3E%3Cpath%20d%3D%22M9%2011l3%203L22%204%22/%3E%3Cpath%20d%3D%22M21%2012v7a2%202%200%2001-2%202H5a2%202%200%2001-2-2V5a2%202%200%20012-2h11%22/%3E%3C/svg%3E"); }
.ic-clock { --ic:url("data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A//www.w3.org/2000/svg%22%20viewBox%3D%220%200%2024%2024%22%20fill%3D%22none%22%20stroke%3D%22black%22%20stroke-width%3D%222%22%20stroke-linecap%3D%22round%22%20stroke-linejoin%3D%22round%22%3E%3Ccircle%20cx%3D%2212%22%20cy%3D%2212%22%20r%3D%229%22/%3E%3Cpath%20d%3D%22M12%207v5l3%202%22/%3E%3C/svg%3E"); }
.ic-list { --ic:url("data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A//www.w3.org/2000/svg%22%20viewBox%3D%220%200%2024%2024%22%20fill%3D%22none%22%20stroke%3D%22black%22%20stroke-width%3D%222%22%20stroke-linecap%3D%22round%22%20stroke-linejoin%3D%22round%22%3E%3Cpath%20d%3D%22M3%2012h18M3%206h18M3%2018h18%22/%3E%3C/svg%3E"); }
.ic-tick { --ic:url("data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A//www.w3.org/2000/svg%22%20viewBox%3D%220%200%2024%2024%22%20fill%3D%22none%22%20stroke%3D%22black%22%20stroke-width%3D%223%22%20stroke-linecap%3D%22round%22%20stroke-linejoin%3D%22round%22%3E%3Cpath%20d%3D%22M20%206L9%2017l-5-5%22/%3E%3C/svg%3E"); }
.ic-cross { --ic:url("data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A//www.w3.org/2000/svg%22%20viewBox%3D%220%200%2024%2024%22%20fill%3D%22none%22%20stroke%3D%22black%22%20stroke-width%3D%223%22%20stroke-linecap%3D%22round%22%20stroke-linejoin%3D%22round%22%3E%3Cpath%20d%3D%22M18%206L6%2018M6%206l12%2012%22/%3E%3C/svg%3E"); }
.ic-docmiss { --ic:url("data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A//www.w3.org/2000/svg%22%20viewBox%3D%220%200%2024%2024%22%20fill%3D%22none%22%20stroke%3D%22black%22%20stroke-width%3D%221.6%22%20stroke-linecap%3D%22round%22%20stroke-linejoin%3D%22round%22%3E%3Cpath%20d%3D%22M14%202H6a2%202%200%2000-2%202v16a2%202%200%20002%202h12a2%202%200%20002-2V8z%22/%3E%3Cpath%20d%3D%22M14%202v6h6%22/%3E%3Cpath%20d%3D%22M12%2018v-6M9.5%2015.5h5%22/%3E%3C/svg%3E"); }
.ic-docok { --ic:url("data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A//www.w3.org/2000/svg%22%20viewBox%3D%220%200%2024%2024%22%20fill%3D%22none%22%20stroke%3D%22black%22%20stroke-width%3D%221.6%22%20stroke-linecap%3D%22round%22%20stroke-linejoin%3D%22round%22%3E%3Cpath%20d%3D%22M14%202H6a2%202%200%2000-2%202v16a2%202%200%20002%202h12a2%202%200%20002-2V8z%22/%3E%3Cpath%20d%3D%22M14%202v6h6%22/%3E%3Cpath%20d%3D%22M9%2015l2%202%204-4%22/%3E%3C/svg%3E"); }
.alert-box .ic { width:16px; height:16px; margin-top:1px; }
.xval-icon .ic { width:10px; height:10px; } .xval-icon.pass .ic { color:#1E8E5A; } .xval-icon.fail .ic { color:#C0392B; }
.tl-dot.done .ic { width:11px; height:11px; color:#fff; }
.doc-empty .ic { width:34px; height:34px; color:#8992A3; margin-bottom:10px; }
.panel-title .ic { color:#24262B; }

/* Cross-document validation */
.xval-row {
    display:flex; align-items:flex-start; gap:10px; padding:9px 0; border-bottom:1px solid #EDEFF3;
}
.xval-row:last-child { border-bottom:none; }
.xval-icon {
    width:18px; height:18px; border-radius:50%; flex-shrink:0;
    display:flex; align-items:center; justify-content:center; margin-top:1px;
}
.xval-icon.pass { background:#E5F5ED; } .xval-icon.fail { background:#FBE7E4; }
.xval-icon svg { width:10px; height:10px; }
.xval-icon.pass svg { stroke:#1E8E5A; } .xval-icon.fail svg { stroke:#C0392B; }
.xval-text { font-size:12.5px; color:#1B2233; line-height:1.45; }

/* Timeline */
.timeline { display:flex; flex-direction:column; }
.tl-step { display:flex; gap:12px; padding:9px 0; position:relative; }
.tl-step:not(:last-child)::before {
    content:''; position:absolute; left:9px; top:26px; bottom:-9px; width:1.5px; background:#E1E4EA;
}
.tl-dot {
    width:19px; height:19px; border-radius:50%; flex-shrink:0;
    display:flex; align-items:center; justify-content:center; margin-top:1px; z-index:1;
    box-sizing:border-box;
}
.tl-dot.done { background:#1E8E5A; }
.tl-dot.done svg { width:11px; height:11px; stroke:#fff; }
.tl-dot.blocked { background:#FBE7E4; border:2px solid #C0392B; }
.tl-dot.pending { background:#FFFFFF; border:2px solid #E1E4EA; }
.tl-content { flex:1; padding-top:1px; }
.tl-label { font-size:12.5px; font-weight:600; color:#1B2233; }
.tl-label.pending-text { color:#8992A3; font-weight:500; }
.tl-time { font-size:11px; color:#8992A3; margin-top:1px; font-family:'JetBrains Mono',monospace; }
.tl-note { font-size:11.5px; color:#5B6472; margin-top:3px; line-height:1.4; }

/* Activity log */
.activity-log { display:flex; flex-direction:column; gap:10px; }
.act-row { display:flex; gap:10px; }
.act-dot { width:6px; height:6px; border-radius:50%; background:#8992A3; margin-top:6px; flex-shrink:0; }
.act-text { font-size:12px; color:#5B6472; }
.ic-mail { --ic:url("data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A//www.w3.org/2000/svg%22%20viewBox%3D%220%200%2024%2024%22%20fill%3D%22none%22%20stroke%3D%22black%22%20stroke-width%3D%222%22%20stroke-linecap%3D%22round%22%20stroke-linejoin%3D%22round%22%3E%3Crect%20x%3D%223%22%20y%3D%225%22%20width%3D%2218%22%20height%3D%2214%22%20rx%3D%222%22/%3E%3Cpath%20d%3D%22M3%207l9%206%209-6%22/%3E%3C/svg%3E"); }

/* Email drafts preview */
.panel-sub { font-size:11px; color:#8992A3; }
.mail-list { display:flex; flex-direction:column; gap:10px; }
.mail { border:1px solid #E1E4EA; border-radius:9px; background:#FBFBFB; overflow:hidden; }
.mail summary {
    list-style:none; cursor:pointer; padding:10px 12px; display:flex; flex-wrap:wrap;
    align-items:center; gap:6px 8px; font-size:12px;
}
.mail summary::-webkit-details-marker { display:none; }
.mail summary::before { content:'▸'; color:#8992A3; font-size:11px; transition:transform .15s; }
.mail[open] summary::before { transform:rotate(90deg); }
.mail-btn { font-weight:600; color:#24262B; }
.mail-scn {
    font-size:10px; font-weight:600; color:#2C6E8E; background:#E7F0F4;
    padding:2px 7px; border-radius:10px;
}
.mail-subj { flex-basis:100%; padding-left:17px; color:#5B6472; font-size:11.5px; }
.mail-meta {
    padding:8px 14px; border-top:1px solid #EDEFF3; font-size:11.5px; color:#5B6472; background:#FFFFFF;
}
.mail-meta b { color:#24262B; font-weight:600; }
.mail-body {
    padding:14px; background:#FFFFFF; border-top:1px solid #EDEFF3; white-space:pre-wrap;
    font-size:12.5px; line-height:1.55; color:#1B2233;
}

.act-time { font-size:10.5px; color:#8992A3; font-family:'JetBrains Mono',monospace; margin-top:1px; }

/* Action bar (sticky bottom) */
.st-key-detail_drawer > .st-key-drawer_actions,
.st-key-detail_drawer > div:has(.st-key-drawer_actions) {
    position:sticky !important; bottom:0; z-index:5; flex-shrink:0;
}
.st-key-detail_drawer .st-key-drawer_actions {
    background:#FFFFFF; border-top:1px solid #E1E4EA;
    padding:14px 26px !important;
    flex-direction:row !important; flex-wrap:nowrap !important; gap:9px !important;
    align-items:center !important;
}
.st-key-detail_drawer .st-key-drawer_actions > div { width:auto !important; flex:1 1 auto !important; min-width:0; }
.st-key-detail_drawer .st-key-drawer_actions > div.st-key-act_approve { flex:1.6 1 auto !important; }
.st-key-drawer_actions div[data-testid="stButton"],
.st-key-drawer_actions div[data-testid="stButton"] button { width:100% !important; }
.st-key-drawer_actions div[data-testid="stButton"] button {
    border-radius:8px !important; padding:9px 14px !important; min-height:44px !important;
    white-space:normal !important; line-height:1.25 !important; gap:7px !important;
    font-family:'Inter',sans-serif !important; font-size:12.5px !important; font-weight:600 !important;
    box-shadow:none !important;
}
.st-key-drawer_actions div[data-testid="stButton"] button p {
    font-size:12.5px !important; font-weight:600 !important;
}
.st-key-act_approve div[data-testid="stButton"] button {
    background:#24262B !important; color:#FFFFFF !important; border:none !important;
}
.st-key-act_approve div[data-testid="stButton"] button:hover { background:#242E48 !important; }
.st-key-act_approve div[data-testid="stButton"] button:disabled {
    background:#C7CCD8 !important; color:#FFFFFF !important; cursor:not-allowed !important;
}
.st-key-act_reminder div[data-testid="stButton"] button {
    background:#FFFFFF !important; color:#1B2233 !important; border:1px solid #E1E4EA !important;
}
.st-key-act_reminder div[data-testid="stButton"] button:hover { background:#EDEFF3 !important; }
.st-key-act_escalate div[data-testid="stButton"] button {
    background:#FBE7E4 !important; color:#C0392B !important; border:none !important;
}
.st-key-act_escalate div[data-testid="stButton"] button:hover { background:#F5D6D0 !important; }
.st-key-drawer_actions div[data-testid="stButton"] button:disabled { opacity:.65; cursor:progress !important; }

.routed-bar {
    display:flex; align-items:center; gap:10px; width:100%;
    font-size:12.5px; color:#125A38; font-weight:600;
}
.routed-bar .ic { width:16px; height:16px; color:#1E8E5A; }
.routed-bar .rb-sub { font-weight:400; color:#5B6472; font-size:12px; }

</style>
""", unsafe_allow_html=True)


# ============================================================
# TOP HEADER — FNOL DASHBOARD DESIGN
# ============================================================

html("""
<div class="topstrip">
    <div class="brand">
        <div class="brand-mark">K</div>
        <div class="brand-text">
            <div class="t1">Claims Assistant</div>
            <div class="t2">FNOL Intake · Workers' Comp</div>
        </div>
    </div>

    <div class="user-chip">
        <div class="user-avatar">DR</div>
        <div class="user-meta">
            <div class="u1">Dante Reyes</div>
            <div class="u2">Claims Handler · WC Team</div>
        </div>
    </div>
</div>
""")

# ============================================================
# UI DATA COLLECTION
# ============================================================

UI_DATA_COLLECTION_ID = "FSL8rka5SKjk4_mfY0tPu"


def get_ui_data_for_run(token, run_id):
    """Fetch UI_DATA for the specified Kognitos run."""

    import requests

    ORG_ID = "xdk36l7E1GbrEvfvYWgdq"
    WORKSPACE_ID = "wPQCXTbwgibi9E4HknJTZ"

    base = (
        f"https://app.us-1.kognitos.com/api/v1/"
        f"organizations/{ORG_ID}/"
        f"workspaces/{WORKSPACE_ID}/"
        f"collections/{UI_DATA_COLLECTION_ID}"
    )

    url = f"{base}/rows:query"

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
    }

    payload = {
        "page_size": 100,
        "stage": "COLLECTION_STAGE_DRAFT",
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=20,
        )

        if response.status_code != 200:
            return None

        data = response.json()

        for row in data.get("rows", []):

            fields = row.get("fields", {})

            run_id_field = fields.get("RUN_ID", {})

            if isinstance(run_id_field, dict):
                stored_run_id = run_id_field.get("text", "")
            else:
                stored_run_id = str(run_id_field)

            if (
                str(stored_run_id).strip()
                == str(run_id).strip()
            ):

                record = {}

                for key, value in fields.items():

                    if isinstance(value, dict):

                        if "text" in value:
                            record[key] = value["text"]

                        elif "number" in value:
                            record[key] = value["number"].get(
                                "lo", 0
                            )

                        else:
                            record[key] = ""

                    else:
                        record[key] = value

                return record

    except Exception:
        return None

    return None


def normalize_ui_data(record):
    """
    Normalize a Kognitos UI_DATA row into the fields consumed by
    the Claims UI.
    """

    if not record:
        return None

    # Some APIs wrap values in {text: ...}; unwrap those values.
    def value(key):
        v = record.get(key, "")

        if isinstance(v, dict):
            if "text" in v:
                return v["text"]
            if "value" in v:
                return v["value"]

        return v if v is not None else ""

    # Keep every extra UI_DATA column (policy number, sender, per-field
    # values/confidence, ...) so the detail drawer can use them when present.
    extras = {
        str(k).upper(): ("" if value(k) is None else value(k))
        for k in record.keys()
    }

    return {
        **extras,
        "FNOL_NUMBER": str(value("FNOL_NUMBER")),
        "CLAIMANT": str(value("CLAIMANT")),
        "EMPLOYER": str(value("EMPLOYER")),
        "ORGANIZATION_ADDRESS": str(value("ORGANIZATION_ADDRESS")),
        "DATE_OF_INJURY": str(value("DATE_OF_INJURY")),
        "INJURY": str(value("INJURY")),
        "FROI_STATUS": str(value("FROI_STATUS")).upper(),
        "FMR_STATUS": str(value("FMR_STATUS")).upper(),
        "SUPERVISOR_STATUS": str(value("SUPERVISOR_STATUS")).upper(),
        "OVERALL_STATUS": str(value("OVERALL_STATUS")).upper(),
        "HITL_INVOKED": str(value("HITL_INVOKED")).upper(),
        "NOTES": str(value("NOTES")),
        "RUN_ID": str(value("RUN_ID")),
    }


# ============================================================
# SESSION STATE
# ============================================================

if "show_detail" not in st.session_state:
    st.session_state.show_detail = False

if "selected_run" not in st.session_state:
    st.session_state.selected_run = None


# ============================================================
# HANDLE VIEW SELECTION
# ============================================================

selected_from_url = st.query_params.get("selected_run")

if selected_from_url:
    st.session_state.selected_run = str(selected_from_url)
    st.session_state.show_detail = True



# ============================================================
# TOKEN
# ============================================================

try:
    TOKEN = st.secrets["KOGNITOS_API_KEY"]
except Exception:
    st.error(
        "Kognitos API key is not configured. "
        "Please check .streamlit/secrets.toml."
    )
    st.stop()


# ============================================================
# LOAD RUNS
# ============================================================

@st.cache_data(ttl=30, show_spinner=False)
def load_claim_runs(token):
    return get_claim_runs(
        token,
        page_size=100
    )


try:
    response = load_claim_runs(TOKEN)

    runs = response.get("runs", [])

except Exception as e:
    st.error(f"Unable to retrieve Kognitos data: {e}")
    st.stop()



def clean_notes(reason):
    """
    Convert Kognitos internal stop/failure messages
    into clean business-friendly notes for the UI.
    """

    if not reason:
        return "No issues flagged"

    reason = str(reason)

    missing = []

    if "FMR:MISSING" in reason:
        missing.append("First Medical Report")

    if "FROI:MISSING" in reason:
        missing.append("First Report of Injury")

    if "Supervisor:MISSING" in reason:
        missing.append("Supervisor Report")

    if missing:
        if len(missing) == 1:
            return f"Missing {missing[0]}"

        if len(missing) == 2:
            return f"Missing {missing[0]} and {missing[1]}"

        return "Missing " + ", ".join(missing[:-1]) + \
               " and " + missing[-1]

    return "No issues flagged"


@st.cache_data(ttl=60, show_spinner=False)
def load_run_details(token, run_id):
    return get_run_details(
        token,
        run_id
    )


def relative_time(value):
    """Convert a Kognitos timestamp into a business-friendly relative time."""
    if not value:
        return ""

    try:
        from datetime import datetime, timezone

        value = str(value).replace("Z", "+00:00")
        created = datetime.fromisoformat(value)

        if created.tzinfo is None:
            created = created.replace(tzinfo=timezone.utc)

        now = datetime.now(timezone.utc)
        seconds = max(0, int((now - created).total_seconds()))

        if seconds < 60:
            return "just now"

        minutes = seconds // 60

        if minutes < 60:
            return f"{minutes}m ago"

        hours = minutes // 60

        if hours < 24:
            return f"{hours}h ago"

        days = hours // 24

        if days < 7:
            return f"{days}d ago"

        weeks = days // 7

        if weeks < 5:
            return f"{weeks}w ago"

        return f"{days // 30}mo ago"

    except Exception:
        return ""


IST = timezone(timedelta(hours=5, minutes=30))


def parse_ts(value):
    """Parse a Kognitos ISO timestamp (Z / nanoseconds tolerated) into an aware UTC datetime."""
    if not value:
        return None
    try:
        s = str(value).strip().replace("Z", "+00:00")
        # Trim fractional seconds beyond microseconds (e.g. nanoseconds).
        s = re.sub(r"(\.\d{6})\d+", r"\1", s)
        dt = datetime.fromisoformat(s)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except Exception:
        return None


# ============================================================
# PROCESS RUNS
# ============================================================

records = []
action_runs = []  # reminder / HITL escalation / registration runs started from this dashboard

ACTION_SUBJECT_KINDS = {
    "Reminder": "reminder",
    "HITL Escalation": "escalate",
    "FNOL Registered": "register",
}


def _input_strings(node, key):
    """String values of input `key` anywhere in a Kognitos inputs structure."""
    if isinstance(node, dict):
        for k, v in node.items():
            if str(k).lower() == key:
                if isinstance(v, str):
                    yield v
                elif isinstance(v, dict):
                    for kk in ("text", "value", "string", "string_value", "stringValue"):
                        if isinstance(v.get(kk), str):
                            yield v[kk]
                            break
            else:
                yield from _input_strings(v, key)
    elif isinstance(node, list):
        for item in node:
            yield from _input_strings(item, key)


# Runs whose Kognitos stop reason marks them as notification / housekeeping runs.
# They are never shown in the queue or counted in the KPIs.
HIDDEN_STOP_REASONS = (
    r"^\s*HITL Escalation",
    r"^\s*Reminder email sent",
    r"^\s*Skipping self-generated notification",
)


def run_stop_reason(run):
    try:
        outputs = ((run.get("state") or {}).get("completed") or {}).get("outputs") or {}
        sr = outputs.get("__stop_reason__") or {}
        return str(sr.get("text", "") if isinstance(sr, dict) else sr)
    except Exception:
        return ""


def is_hidden_stop_reason(reason):
    return any(re.search(p, reason or "", re.I) for p in HIDDEN_STOP_REASONS)


def action_from_stop_reason(run, reason):
    """'HITL Escalation – FNOL-… – Name|…' -> escalation record (if it names a claim)."""
    head = (reason or "").split("|")[0].strip()
    for label, kind in ACTION_SUBJECT_KINDS.items():
        if head.startswith(label + " – "):
            parts = head.split(" – ")
            ref = parts[1].strip() if len(parts) > 1 else ""
            if not ref or ref in ("—", "-"):
                return None
            emails = re.findall(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+", reason)
            return {
                "kind": kind, "ref": ref, "subject": head,
                "to": emails[0] if emails else "",
                "k_run": run.get("name", "").split("/")[-1],
                "created": parse_ts(run.get("create_time")),
                "state": "failed" if "|failure|" in reason.lower() else "completed",
            }
    return None


def detect_action_run(run, details):
    """
    If this run was started by a dashboard button (its subject input starts with
    "Reminder – ", "HITL Escalation – " or "FNOL Registered – "), describe it.
    Only the run's inputs are checked, so employer replies ("Re: Reminder – …")
    stay in the queue.
    """
    sources = [
        (details or {}).get("user_inputs") or {},
        run.get("user_inputs") or {},
        run.get("inputs") or {},
    ]
    for src in sources:
        for subj in _input_strings(src, "subject"):
            for label, kind in ACTION_SUBJECT_KINDS.items():
                if subj.startswith(label + " – "):
                    parts = subj.split(" – ")
                    state = run.get("state", {}) or {}
                    return {
                        "kind": kind,
                        "ref": parts[1].strip() if len(parts) > 1 else "",
                        "subject": subj,
                        "to": next(_input_strings(src, "from_address"), ""),
                        "k_run": run.get("name", "").split("/")[-1],
                        "created": parse_ts(run.get("create_time")),
                        "state": next(
                            (x for x in ("completed", "failed", "waiting", "running", "pending")
                             if x in state), "unknown"
                        ),
                    }
    return None


for run in runs:

    run_id = run.get("name", "").split("/")[-1]

    try:
        details = load_run_details(
            TOKEN,
            run_id
        )

        claim = extract_claim_data(details)

    except Exception:
        details = {}
        claim = {}

    try:
        _act = detect_action_run(run, details)
    except Exception:
        _act = None
    if _act:
        action_runs.append(_act)  # a handler action, not a new claim
        continue

    _reason = run_stop_reason(run)
    if is_hidden_stop_reason(_reason):
        # Reminder / HITL escalation / self-generated notification run — not a claim.
        _act = action_from_stop_reason(run, _reason)
        if _act:
            action_runs.append(_act)  # still counts toward the claim's HITL status
        continue

    state = run.get("state", {})

    if "completed" in state:
        status = "Completed"
    elif "running" in state:
        status = "Running"
    else:
        status = "Unknown"

    has_claim = bool(
        claim.get("FNOL Number")
        or claim.get("Claimant")
    )

    stop_reason = ""

    try:
        completed = state.get("completed", {})
        outputs = completed.get("outputs", {})

        stop_reason = str(
            outputs.get(
                "__stop_reason__",
                {}
            ).get(
                "text",
                ""
            )
        )

    except Exception:
        pass

    if "Failure" in stop_reason or "MISSING" in stop_reason:
        queue_status = "HITL Invoked"
        hitl_value = "Yes"
        notes = clean_notes(stop_reason)

    elif has_claim:
        queue_status = "Claim Registered"
        hitl_value = "No"
        notes = "No issues flagged"

    else:
        queue_status = "Waiting for Info"
        hitl_value = "No"
        notes = "Awaiting required claim information"

    attachments = []

    try:
        attachments = (
            details
            .get("user_inputs", {})
            .get("attachments", {})
            .get("list", {})
            .get("items", [])
        )
    except Exception:
        pass

    records.append({
        "run_id": run_id,
        "created": (
            (
                __import__("datetime").datetime.fromisoformat(
                    run.get("create_time", "").replace("Z", "")
                )
                + __import__("datetime").timedelta(
                    hours=5,
                    minutes=30
                )
            ).strftime("%b %d, %I:%M %p")
            if run.get("create_time")
            else ""
        ),
        "created_dt": parse_ts(run.get("create_time")),
        "updated_dt": parse_ts(run.get("update_time")),
        "version": run.get("stage_version", ""),
        "status": status,
        "claim": claim,
        "details": details,
        "attachments": attachments,
        "queue_status": queue_status,
        "hitl": hitl_value,
        "notes": notes,
        "ui_data": None
    })


@st.cache_data(ttl=60, show_spinner=False)
def load_ui_data(token, run_id):
    return get_ui_data_for_run(
        token,
        run_id
    )


# ============================================================
# ENRICH RUNS FROM UI_DATA
# ============================================================

# IMPORTANT:
# This must happen AFTER records are populated.
# UI_DATA is the source of truth for dashboard claim/document/status fields.

for r in records:

    try:
        ui_raw = load_ui_data(
            TOKEN,
            r["run_id"]
        )

        ui = normalize_ui_data(ui_raw)
        r["ui_data"] = ui

        if ui:

            # UI_DATA is authoritative for dashboard claim fields.
            # Blank values must remain blank — never fall back to RUN_ID.
            r["claim"]["Claimant"] = ui.get("CLAIMANT", "")
            r["claim"]["FNOL Number"] = ui.get("FNOL_NUMBER", "")
            r["claim"]["Employer"] = ui.get("EMPLOYER", "")
            r["claim"]["Organization Address"] = ui.get(
                "ORGANIZATION_ADDRESS",
                ""
            )
            r["claim"]["Date of Injury"] = ui.get(
                "DATE_OF_INJURY",
                ""
            )
            r["claim"]["Injury"] = ui.get(
                "INJURY",
                ""
            )

            # UI status is authoritative.
            overall = ui.get("OVERALL_STATUS", "").upper()

            if overall == "PROCESSED":
                r["queue_status"] = "Claim Registered"

            elif overall == "DOCUMENTS_MISSING":
                r["queue_status"] = "Waiting for Info"

            elif overall == "VALIDATION_FAILED":
                r["queue_status"] = "HITL Invoked"

            # HITL flag comes from UI_DATA.
            if ui.get("HITL_INVOKED"):
                r["hitl"] = (
                    "Yes"
                    if ui["HITL_INVOKED"] == "YES"
                    else "No"
                )

            # Business reason only — never show email ID/subject.
            if ui.get("NOTES"):
                r["notes"] = ui["NOTES"]

    except Exception:
        # Keep the run visible even if UI_DATA cannot be read.
        r["ui_data"] = None


# ============================================================
# HANDLER ACTIONS (drawer buttons)
# ============================================================

HANDLER_NAME = "Dante Reyes"
SLA_HOURS = 48

# ------------------------------------------------------------
# Kognitos workflow configuration (.streamlit/secrets.toml)
# ------------------------------------------------------------
# Every drawer button starts a Kognitos automation. The email drafts live in
# those automations; this app only starts them and passes the claim details.
#
# Nothing is required: by default the app finds each automation in your
# workspace by its name:
#   Send Reminder to Employer  -> name contains "reminder"
#   Escalate to HITL Now       -> name contains "hitl" or "escalat"
#   Mark as Claim Registered   -> name contains "register" or "rout"
#
# To pin a specific automation (recommended once it works), add its ID or its
# exact name in Kognitos:
#   KOGNITOS_REMINDER_AUTOMATION = "..."
#   KOGNITOS_ESCALATE_AUTOMATION = "..."
#   KOGNITOS_REGISTER_AUTOMATION = "..."
#
# Stage: the published version is tried first, then the draft. To force one:
#   KOGNITOS_INVOKE_STAGE = "AUTOMATION_STAGE_DRAFT"   # or ..._PUBLISHED

KOGNITOS_ORG_ID = "xdk36l7E1GbrEvfvYWgdq"
KOGNITOS_WORKSPACE_ID = "wPQCXTbwgibi9E4HknJTZ"
KOGNITOS_API_BASE = (
    "https://app.us-1.kognitos.com/api/v1/"
    f"organizations/{KOGNITOS_ORG_ID}/workspaces/{KOGNITOS_WORKSPACE_ID}"
)

RUN_POLL_SECONDS = 8  # how long to wait for the email run to finish before returning

# Reminder and HITL escalation emails go to this address (demo mailbox).
# Set to "" to email the claim's employer contact (Submitted By) instead.
REMINDER_EMAIL_TO = "demokog36@gmail.com"

ACTION_META = {
    "register": {
        "secrets": ["KOGNITOS_REGISTER_AUTOMATION", "KOGNITOS_REGISTER_AUTOMATION_ID"],
        "keywords": ["register", "rout"],
        "label": "claim registration & routing",
        "log": "Claim registered and routed to claim handler by {h}",
        "toast_done": "Claim registered and routed to claim handler.",
        "toast_started": "Claim registration started in Kognitos.",
    },
    "reminder": {
        "secrets": ["KOGNITOS_REMINDER_AUTOMATION", "KOGNITOS_REMINDER_AUTOMATION_ID"],
        # Employer reminder email automation (Kognitos draft):
        # app.us-1.kognitos.com/.../drafts/mYAw57j8GrQR0ixlWtkUz/edit
        "default_automation": "mYAw57j8GrQR0ixlWtkUz",
        "default_stage": "AUTOMATION_STAGE_DRAFT",
        "keywords": ["reminder"],
        "label": "employer reminder email",
        "log": "Reminder email sent to {to} via Kognitos by {h}",
        "toast_done": "Reminder email sent to {to}.",
        "toast_started": "Reminder email to {to} started in Kognitos.",
    },
    "escalate": {
        "secrets": ["KOGNITOS_ESCALATE_AUTOMATION", "KOGNITOS_ESCALATE_AUTOMATION_ID"],
        # Same Workers' Compensation Claims Processor draft (holds the HITL email draft).
        "default_automation": "mYAw57j8GrQR0ixlWtkUz",
        "default_stage": "AUTOMATION_STAGE_DRAFT",
        "keywords": ["hitl", "escalat"],
        "label": "HITL escalation",
        "log": "Escalated to Human-in-the-Loop review by {h}; HITL email sent via Kognitos",
        "toast_done": "Claim escalated to HITL — notification email sent.",
        "toast_started": "Claim escalated to HITL — notification started in Kognitos.",
    },
}

STAGES = ["AUTOMATION_STAGE_PUBLISHED", "AUTOMATION_STAGE_DRAFT"]

# Claim values the app can supply, and the input names a Kognitos automation
# might use for each (compared lower-case, letters/digits only).
INPUT_ALIASES = {
    "email": ["email", "to", "recipient", "recipientemail", "employeremail", "senderemail",
              "submittedby", "useremail", "emailaddress", "contactemail", "sender", "from",
              "toemail", "mailto"],
    "claimant": ["claimant", "claimantname", "employeename", "employee", "injuredworker",
                 "workername", "name"],
    "fnol": ["fnol", "fnolnumber", "fnolid", "claimid", "claimnumber", "claim", "claimno"],
    "employer": ["employer", "employername", "organization", "organisation", "company",
                 "companyname", "org"],
    "notes": ["notes", "reason", "missingdocuments", "missingdocs", "missinginfo",
              "missinginformation", "message", "details", "comment", "comments", "issue"],
    "date_of_injury": ["dateofinjury", "injurydate", "doi"],
    "injury": ["injury", "injurytype", "injurydescription"],
    "policy": ["policy", "policynumber", "policyno"],
    "run_id": ["runid", "sourcerunid", "intakerunid"],
    "handler": ["handler", "handlername", "escalatedby", "requestedby", "sentby"],
    "action": ["action", "actiontype"],
}

EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")


def _secret(name, default=""):
    try:
        return str(st.secrets.get(name, default) or default).strip()
    except Exception:
        return default


def _norm(s):
    return re.sub(r"[^a-z0-9]", "", str(s).lower())


def _k_headers():
    return {
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }


def _k_error(resp):
    try:
        data = resp.json()
        detail = data.get("message") or data.get("error") or resp.text
    except Exception:
        detail = resp.text
    return f"Kognitos returned {resp.status_code}: {str(detail)[:220]}"


def _automation_summary(raw):
    name = str(raw.get("name", ""))
    title = (
        raw.get("display_name") or raw.get("displayName") or raw.get("title")
        or raw.get("label") or name.split("/")[-1]
    )
    return {
        "id": name.split("/")[-1] or str(raw.get("id", "")),
        "title": str(title),
        "description": str(raw.get("description", "")),
        "raw": raw,
    }


@st.cache_data(ttl=300, show_spinner=False)
def list_kognitos_automations(token):
    """All automations in the workspace (cached 5 min). Empty list if not available."""
    import requests

    out, page_token = [], None
    for _ in range(10):
        params = {"page_size": 100}
        if page_token:
            params["page_token"] = page_token
        try:
            resp = requests.get(
                f"{KOGNITOS_API_BASE}/automations",
                headers=_k_headers(), params=params, timeout=20,
            )
        except Exception:
            break
        if resp.status_code != 200:
            break
        data = resp.json() or {}
        items = data.get("automations")
        if items is None:  # tolerate other list keys
            items = next((v for v in data.values() if isinstance(v, list)), [])
        out.extend(_automation_summary(a) for a in items if isinstance(a, dict))
        page_token = data.get("next_page_token")
        if not page_token:
            break
    return out


@st.cache_data(ttl=300, show_spinner=False)
def get_kognitos_automation(token, automation_id, first_stage=""):
    import requests

    order = ([first_stage] if first_stage else []) + [x for x in STAGES if x != first_stage]
    for stage in order:
        try:
            resp = requests.get(
                f"{KOGNITOS_API_BASE}/automations/{automation_id}",
                headers=_k_headers(), params={"stage": stage}, timeout=20,
            )
        except Exception:
            return None
        if resp.status_code == 200:
            return resp.json()
    return None


def resolve_automation(action):
    """Return (automation_id, automation_raw_or_None, error_or_None)."""
    meta = ACTION_META[action]
    configured = next((v for v in (_secret(k) for k in meta["secrets"]) if v), "") \
        or meta.get("default_automation", "") \
        or _secret("KOGNITOS_ACTION_AUTOMATION_ID")
    autos = list_kognitos_automations(TOKEN)

    if configured:
        for a in autos:
            if configured == a["id"] or _norm(configured) == _norm(a["title"]):
                return a["id"], a["raw"], None
        if " " not in configured:  # treat as an ID even if it wasn't listed
            return configured, None, None
        return None, None, (
            f"No Kognitos automation named “{configured}” was found in this workspace."
        )

    matches = [
        a for a in autos
        if any(k in f"{a['title']} {a['description']}".lower() for k in meta["keywords"])
    ]
    if len(matches) == 1:
        return matches[0]["id"], matches[0]["raw"], None
    if len(matches) > 1:
        names = ", ".join(f"“{a['title']}”" for a in matches[:5])
        return None, None, (
            f"Several automations could handle the {meta['label']} ({names}). "
            f"Set {meta['secrets'][0]} in secrets.toml to the one to use."
        )
    return None, None, (
        f"No Kognitos automation for the {meta['label']} was found"
        + ("" if autos else " (the workspace's automation list could not be read)")
        + f". Set {meta['secrets'][0]} in .streamlit/secrets.toml to its ID or name."
    )


def declared_input_names(raw):
    """Input names the automation declares, if its definition exposes them."""
    names = []

    def walk(node, under_input=False):
        if isinstance(node, dict):
            for k, v in node.items():
                key_is_input = "input" in str(k).lower()
                if key_is_input and isinstance(v, dict) and str(k).lower() in (
                    "default_inputs", "defaultinputs", "inputs"
                ):
                    names.extend(str(x) for x in v.keys())
                elif key_is_input and isinstance(v, list):
                    for item in v:
                        if isinstance(item, dict) and item.get("name"):
                            names.append(str(item["name"]))
                        elif isinstance(item, str):
                            names.append(item)
                else:
                    walk(v, under_input or key_is_input)
        elif isinstance(node, list):
            for item in node:
                walk(item, under_input)

    walk(raw or {})
    seen, out = set(), []
    for n in names:
        if n not in seen:
            seen.add(n)
            out.append(n)
    return out


def build_inputs(raw, values):
    """Map claim values onto the automation's declared inputs (or send all)."""
    declared = declared_input_names(raw)
    if not declared:
        return {k.upper(): v for k, v in values.items() if v}

    inputs = {}
    for name in declared:
        n = _norm(name)
        key = next((k for k, al in INPUT_ALIASES.items() if n in al), None)
        if key is None:
            key = next(
                (k for k, al in INPUT_ALIASES.items() if any(len(a) >= 5 and a in n for a in al)),
                None,
            )
        if key and values.get(key):
            inputs[name] = values[key]
    return inputs


# ------------------------------------------------------------
# Email drafts (match the drafts in Kognitos) + processor inputs
# ------------------------------------------------------------

# Subjects of emails started from this dashboard. Runs with these subjects are
# handler actions, not new claims, so they are kept out of the intake queue.
ACTION_SUBJECT_PREFIXES = ("Reminder – ", "HITL Escalation – ", "FNOL Registered – ")

DOC_LONG = {
    "froi": "First Report of Injury (FROI)",
    "fmr": "First Medical Report (FMR)",
    "emp": "Employer Confirmation form",
}
DOC_SHORT = {"froi": "FROI", "fmr": "FMR", "emp": "Employer Confirmation form"}
DOC_MISSING = {
    "froi": "First Report of Injury (FROI)",
    "fmr": "First Medical Report (FMR)",
    "emp": "Employer Injury Confirmation / Acknowledgment document",
}
DOC_MISSING_LOWER = {
    "froi": "First Report of Injury",
    "fmr": "First Medical Report",
    "emp": "employer confirmation",
}
DOC_TITLES = DOC_MISSING  # backwards compatibility


def _long_date(value):
    """'2026-08-11' / '08/11/2026' -> 'August 11, 2026' (unchanged if unparseable)."""
    s = str(value or "").strip()
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y", "%B %d, %Y", "%b %d, %Y"):
        try:
            d = datetime.strptime(s, fmt)
            return f"{d.strftime('%B')} {d.day}, {d.year}"
        except ValueError:
            continue
    return s


def _join(items):
    items = [i for i in items if i]
    if len(items) <= 1:
        return "".join(items)
    if len(items) == 2:
        return f"{items[0]} and {items[1]}"
    return ", ".join(items[:-1]) + f", and {items[-1]}"


def _person(name):
    name = str(name or "").strip()
    return name.title() if name and (name.isupper() or name.islower()) else name


def _injury(text):
    """'Burn – forearm' -> 'Burn – Forearm' (keeps the claim's own wording)."""
    return " ".join(w[:1].upper() + w[1:] for w in str(text or "").split(" "))


def email_scenario(action, p):
    """1 = registered, 2 = reminder (awaiting docs), 3 = HITL / SLA exceeded."""
    if action == "register":
        return 1
    if action == "escalate" or p.get("status") == "HITL Invoked":
        return 3
    return 2


def compose_email(action, p):
    """
    Subject + body for a handler action, built from the three email templates
    (Scenario 1/2/3) and filled with the selected claim's real data.
    """
    scenario = email_scenario(action, p)
    fnol = p.get("fnol") or "—"
    ref = p.get("fnol") or f"Ref {p.get('run_id', '')}"  # links the action run back to this claim
    claimant = _person(p.get("claimant")) or "the claimant"
    employer = p.get("employer") or ""
    greeting = f"Dear {employer} HR Team," if employer else "Dear HR Team,"
    received = p.get("received_keys") or []
    missing = p.get("missing_keys") or []

    facts = (
        f"FNOL Number: {fnol}\n"
        f"Claimant: {claimant}\n"
        f"Date of Injury: {_long_date(p.get('date_of_injury')) or '—'}\n"
        f"Employer: {employer or '—'}\n"
        f"Injury: {_injury(p.get('injury')) or '—'}"
    )
    sign = "Kind regards,\n\nClaims Administration Team"

    rec_long = _join([DOC_LONG[k] for k in received]) or "submitted documents"
    rec_short = _join([DOC_SHORT[k] for k in received]) or "submitted documents"
    verb = "has" if len(received) == 1 else "have"
    miss_long = _join([DOC_MISSING[k] for k in missing])
    miss_lower = _join([DOC_MISSING_LOWER[k] for k in missing])
    doc_word = "documents" if len(missing) > 1 else "document"

    opening = (
        f"{greeting}\n\n"
        f"Thank you for submitting the {rec_long} for the workplace injury involving {claimant}.\n"
        f"We acknowledge receipt of the submitted documents and confirm that the {rec_short} "
        f"{verb} been successfully verified. The FNOL has been registered under the following "
        "reference number:\n\n"
        f"{facts}\n\n"
    )

    if scenario == 1:
        forms = "all three forms" if len(received) == 3 else "the submitted forms"
        subject = f"FNOL Registered – {ref} – {claimant}"
        body = (
            f"{greeting}\n\n"
            f"Thank you for submitting the {rec_long} for the workplace injury involving {claimant}.\n"
            f"We acknowledge receipt of {forms} and confirm that the required information has been "
            "received and validated. The First Notice of Loss (FNOL) has been registered under the "
            "following reference number:\n\n"
            f"{facts}\n\n"
            "Please retain the above FNOL number for all future correspondence regarding this claim.\n"
            "Thank you for your prompt submission and cooperation.\n\n"
            f"{sign}"
        )

    elif scenario == 2:
        subject = f"Reminder – {ref} – Pending {miss_long or 'claim information'}"
        awaiting = (
            f"To complete the FNOL submission, we are still awaiting the {miss_long}. "
            f"Please provide the missing {doc_word} at your earliest convenience so that the "
            "claim record can be completed.\n\n"
            if missing else
            "To complete the FNOL submission, we are still awaiting the following information: "
            f"{p.get('notes') or 'required claim information'}. Please provide it at your earliest "
            "convenience so that the claim record can be completed.\n\n"
        )
        body = (
            opening + awaiting
            + f"Please reference {fnol} in any future correspondence regarding this claim.\n"
            "Thank you for your prompt attention and cooperation.\n\n"
            f"{sign}"
        )

    else:  # scenario 3
        prefix = "Reminder" if action == "reminder" else "HITL Escalation"
        subject = f"{prefix} – {ref} – {claimant}"
        if missing:
            awaiting = f"To complete the FNOL submission, we are still awaiting the {miss_long}.\n"
            provide = f"Please provide the missing {miss_lower} at the earliest opportunity"
        else:
            awaiting = (
                "During validation the following issue was identified: "
                f"{p.get('notes') or 'the submitted information could not be validated'}.\n"
            )
            provide = "Please provide the corrected information at the earliest opportunity"
        escalation = (
            f"Please note that the submission deadline of {p.get('sla_deadline')} has passed, and "
            "the matter has therefore been escalated for Human-in-the-Loop review."
            if p.get("sla_overdue") and p.get("sla_deadline") else
            "Please note that the matter has been escalated for Human-in-the-Loop review."
        )
        body = (
            opening + awaiting
            + f"{escalation} Manual handler action is now required before the claim can proceed.\n\n"
            f"{provide} and reference {fnol} in any related correspondence.\n"
            "Thank you for your prompt attention and cooperation.\n\n"
            f"{sign}"
        )

    return subject, body


# Inputs the Workers' Compensation Claims Processor requires (from Kognitos).
PROCESSOR_INPUTS = ["from_address", "subject", "attachments", "claimant", "employer", "fnol", "notes"]

SUBJECT_NAMES = {"subject", "emailsubject", "mailsubject", "title"}
BODY_NAMES = {"body", "emailbody", "mailbody", "message", "content", "draft", "emailtext",
              "emaildraft", "text", "mailcontent"}
ATTACHMENT_NAMES = {"attachments", "attachment", "files", "documents", "docs"}


def _text(v):
    return {"text": str(v if v is not None else "")}


def value_for_input(name, action, p, subject, body):
    """Typed Kognitos value for one input name, or None if the app has nothing for it."""
    n = _norm(name)
    if n in ATTACHMENT_NAMES:
        original = (p.get("intake_inputs") or {}).get(name)
        return original if isinstance(original, dict) and original else {"list": {"items": []}}
    if n in SUBJECT_NAMES:
        return _text(subject)
    if n in BODY_NAMES:
        return _text(body)
    if n in ("fromaddress", "replyto", "replytoaddress"):
        return _text(p.get("email", ""))

    values = {
        "email": p.get("email", ""), "claimant": p.get("claimant", ""),
        "fnol": p.get("fnol", ""), "employer": p.get("employer", ""),
        "notes": p.get("notes", ""), "date_of_injury": p.get("date_of_injury", ""),
        "injury": p.get("injury", ""), "policy": p.get("policy", ""),
        "run_id": p.get("run_id", ""), "handler": HANDLER_NAME, "action": action.upper(),
    }
    key = next((k for k, al in INPUT_ALIASES.items() if n in al), None)
    if key and values.get(key):
        return _text(values[key])

    for k, v in (p.get("ui") or {}).items():  # any UI_DATA column with the same name
        if _norm(k) == n and str(v).strip():
            return _text(v)
    return None


EMAIL_BODY_INPUT = "email_body"  # add a text input with this name in Kognitos to send the app's email text


def build_processor_inputs(action, p, extra_required=(), include_body=True):
    """
    Inputs for the claims processor: the original intake run's inputs (already
    typed by Kognitos), with recipient / subject / claim fields replaced for
    this action, plus anything Kognitos reported as missing.
    """
    import copy

    subject, body = compose_email(action, p)
    inputs = copy.deepcopy(p.get("intake_inputs") or {})
    names = list(inputs.keys())
    wanted = list(PROCESSOR_INPUTS) + list(extra_required)
    if include_body:
        wanted.append(EMAIL_BODY_INPUT)
    for nm in wanted:
        if nm not in names:
            names.append(nm)

    fallback_notes = {
        "reminder": "Reminder sent to employer for missing documents.",
        "escalate": "Escalated to Human-in-the-Loop review by claims handler.",
        "register": "Claim registered and routed to claim handler.",
    }[action]
    for nm in names:
        v = value_for_input(nm, action, p, subject, body)
        if v is None and _norm(nm) in INPUT_ALIASES["notes"]:
            v = _text(fallback_notes)
        if v is not None:
            inputs[nm] = v
        elif nm not in inputs:
            inputs[nm] = _text("N/A")  # required by Kognitos; the app has no value for it
    return inputs, subject, body


def missing_inputs_from_error(text):
    m = re.search(
        r"missing required input\(s\):\s*([A-Za-z_]\w*(?:\s*,\s*[A-Za-z_]\w*)*)",
        text or "", re.I,
    )
    return [x.strip() for x in m.group(1).split(",")] if m else []


def _run_state(token, automation_id, run_id):
    import requests

    try:
        resp = requests.get(
            f"{KOGNITOS_API_BASE}/automations/{automation_id}/runs/{run_id}",
            headers=_k_headers(), timeout=15,
        )
    except Exception:
        return "unknown", ""
    if resp.status_code != 200:
        return "unknown", ""
    state = (resp.json() or {}).get("state", {}) or {}
    for s in ("completed", "failed", "waiting", "running", "pending"):
        if s in state:
            detail = state.get(s) or {}
            reason = ""
            if isinstance(detail, dict):
                reason = str(
                    detail.get("description") or detail.get("message")
                    or detail.get("reason") or ""
                )
            return s, reason
    return "unknown", ""


def invoke_kognitos_action(action, payload):
    """
    Start the Kognitos automation for a handler action and wait briefly for it.
    Returns a dict: ok, state, run_id, message, automation.
    """
    import requests
    import time

    automation_id, raw, err = resolve_automation(action)
    if err:
        return {"ok": False, "message": err}

    if raw is None:
        raw = get_kognitos_automation(
            TOKEN, automation_id, ACTION_META[action].get("default_stage", "")
        )
    title = _automation_summary(raw)["title"] if raw else automation_id

    forced = _secret("KOGNITOS_INVOKE_STAGE")
    preferred = ACTION_META[action].get("default_stage")
    if forced:
        stages = [forced]
    elif preferred:
        stages = [preferred]
    else:
        stages = STAGES

    errors, run_name, extra, include_body = [], "", [], True
    for stage in stages:
        for _attempt in range(4):
            inputs, subject, body_text = build_processor_inputs(
                action, payload, extra, include_body
            )
            try:
                resp = requests.post(
                    f"{KOGNITOS_API_BASE}/automations/{automation_id}:invoke",
                    headers=_k_headers(),
                    json={"stage": stage, "inputs": inputs},
                    timeout=30,
                )
            except Exception as exc:
                return {"ok": False, "message": f"Could not reach Kognitos: {exc}"}

            if resp.status_code in (200, 201):
                try:
                    run_name = str((resp.json() or {}).get("run_id", ""))
                except Exception:
                    run_name = ""
                break

            last_err = _k_error(resp)
            if resp.status_code in (401, 403):
                return {"ok": False, "message": last_err}

            if (
                include_body and resp.status_code == 400
                and EMAIL_BODY_INPUT in last_err and "missing required" not in last_err.lower()
            ):
                include_body = False  # automation has no email_body input yet; send without it
                continue

            newly_missing = [m for m in missing_inputs_from_error(last_err) if m not in extra]
            if resp.status_code == 400 and newly_missing:
                extra.extend(newly_missing)  # add them and try again
                continue
            errors.append(f"[{stage.replace('AUTOMATION_STAGE_', '').lower()}] {last_err}")
            break
        if run_name:
            break

    if not run_name:
        return {
            "ok": False,
            "message": f"“{title}” ({automation_id}) could not be started. " + " · ".join(errors),
        }

    k_run = run_name.split("/")[-1]

    # Wait briefly so the handler knows whether the email actually went out.
    state, reason = "pending", ""
    deadline = time.time() + RUN_POLL_SECONDS
    while time.time() < deadline:
        state, reason = _run_state(TOKEN, automation_id, k_run)
        if state in ("completed", "failed", "waiting"):
            break
        time.sleep(1.5)

    if state == "failed":
        return {
            "ok": False,
            "message": f"“{title}” failed in Kognitos (run {k_run}). {reason}".strip(),
        }

    return {"ok": True, "state": state, "run_id": k_run, "automation": title,
            "subject": subject}


@st.cache_resource
def action_store():
    """
    Handler actions keyed by run_id, kept so the dashboard reflects an action
    immediately — before the Kognitos automation updates UI_DATA.
    Survives page reloads for the life of the Streamlit server process.
    """
    return {}


def _entry(run_id):
    return action_store().setdefault(run_id, {"activity": []})


def run_action(action, payload):
    """Button callback: trigger Kognitos first; update the UI only if it worked."""
    if action in ("reminder", "escalate") and REMINDER_EMAIL_TO:
        payload = {**payload, "email": REMINDER_EMAIL_TO}

    run_id = payload["run_id"]
    meta = ACTION_META[action]
    result = invoke_kognitos_action(action, payload)

    now = datetime.now(timezone.utc)

    if not result["ok"]:
        if action == "escalate":
            # Escalation is the handler's decision: change the status even if the email failed.
            e = _entry(run_id)
            e["ui_overall_at_action"] = payload.get("overall", "")
            e.update(queue_status="HITL Invoked", hitl="Yes", manual_escalated=True)
            e["activity"].append((
                f"Escalated to Human-in-the-Loop review by {HANDLER_NAME}. "
                f"HITL email was NOT sent — {result['message']}", now,
            ))
            st.session_state.pending_toast = (
                f"Escalated to HITL, but the email was not sent — {result['message']}", "warn"
            )
        else:
            st.session_state.pending_toast = (f"Not sent — {result['message']}", "error")
        return

    e = _entry(run_id)
    e["ui_overall_at_action"] = payload.get("overall", "")

    if action == "register":
        e.update(queue_status="Claim Registered", hitl="No",
                 notes="No issues flagged", manual_approved=now)
    elif action == "escalate":
        e.update(queue_status="HITL Invoked", hitl="Yes", manual_escalated=True)
    elif action == "reminder":
        e["last_reminder"] = now

    to = payload.get("email") or "the employer"
    done = result["state"] == "completed"
    log = meta["log"].format(h=HANDLER_NAME, to=to)
    if result["state"] == "waiting":
        log += " — waiting for input in Kognitos"
    elif not done:
        log += " — run in progress"
    log += f" (Kognitos run {result['run_id']})."
    if result.get("subject"):
        log += f" Subject: “{result['subject']}”."
    e["activity"].append((log, now))

    load_ui_data.clear()      # pick up UI_DATA changes made by the automation
    load_claim_runs.clear()   # pick up the new action run (keeps the status after restarts)
    toast = meta["toast_done" if done else "toast_started"].format(to=to)
    st.session_state.pending_toast = (toast, "ok")


if st.session_state.get("pending_toast"):
    text, kind = st.session_state.pop("pending_toast")
    st.toast(text, icon={
        "ok": ":material/check_circle:", "warn": ":material/warning:"
    }.get(kind, ":material/error:"))


# Apply handler actions recorded in Kognitos (survive restarts / redeploys).
def _claim_ref_matches(r, ref):
    fnol_no = str((r.get("claim") or {}).get("FNOL Number", "")).strip()
    return bool(ref) and (ref == fnol_no or ref == f"Ref {r['run_id']}")


_epoch = datetime.min.replace(tzinfo=timezone.utc)
for act in sorted(action_runs, key=lambda a: a["created"] or _epoch):
    for r in records:
        if not _claim_ref_matches(r, act["ref"]):
            continue
        r.setdefault("k_actions", []).append(act)
        if act["kind"] == "escalate" and r["queue_status"] == "Waiting for Info":
            r["orig_notes"] = r.get("orig_notes") or r["notes"]
            r["queue_status"] = "HITL Invoked"
            r["hitl"] = "Yes"
            r["escalated_by_handler"] = act["created"]
        elif act["kind"] == "register":
            r["orig_notes"] = r.get("orig_notes") or r["notes"]
            r["queue_status"] = "Claim Registered"
            r["hitl"] = "No"
            r["notes"] = "No issues flagged"
            r["registered_by_handler"] = act["created"]


# Apply handler actions from this session on top (instant feedback).
for r in records:
    a = action_store().get(r["run_id"])
    if not a:
        continue

    current_overall = str((r.get("ui_data") or {}).get("OVERALL_STATUS", "")).upper()
    if current_overall and current_overall != a.get("ui_overall_at_action", current_overall):
        # Kognitos has since updated UI_DATA — it is the source of truth again.
        for k in ("queue_status", "hitl", "notes", "manual_approved", "manual_escalated"):
            a.pop(k, None)
        a["ui_overall_at_action"] = current_overall

    r["manual"] = a
    r["orig_notes"] = r.get("orig_notes") or r["notes"]
    if a.get("queue_status"):
        r["queue_status"] = a["queue_status"]
    if a.get("hitl"):
        r["hitl"] = a["hitl"]
    if a.get("notes"):
        r["notes"] = a["notes"]


# ============================================================
# COUNTS
# ============================================================

# ALL relevant runs are used for dashboard counts.
total = len(records)

registered = sum(
    1 for r in records
    if r["queue_status"] == "Claim Registered"
)

waiting = sum(
    1 for r in records
    if r["queue_status"] == "Waiting for Info"
)

hitl_count = sum(
    1 for r in records
    if r["queue_status"] == "HITL Invoked"
)


# ============================================================
# TITLE
# ============================================================

title_col, live_col = st.columns([5, 1])

with title_col:

    html("""
    <div class="page-title">FNOL Intake Queue</div>
    <div class="page-subtitle">
        Submissions received via email and processed by the
        Kognitos AI Copilot before handler review.
    </div>
    """)

with live_col:

    html("""
    <div class="live">
        <span class="live-dot">●</span>
        Live · synced moments ago
    </div>
    """)


st.markdown("<br>", unsafe_allow_html=True)


# ============================================================
# SUMMARY CARDS
# ============================================================

c1, c2, c3, c4 = st.columns(4)

with c1:

    html(f"""
    <div class="card primary">
        <div class="card-label">
            <span class="dot-blue">■</span>
            &nbsp;TOTAL IN QUEUE
        </div>
        <div class="card-number">{total}</div>
    </div>
    """)

with c2:

    html(f"""
    <div class="card">
        <div class="card-label">
            <span class="dot-green">■</span>
            &nbsp;CLAIM REGISTERED TODAY
        </div>
        <div class="card-number">{registered}</div>
    </div>
    """)

with c3:

    html(f"""
    <div class="card">
        <div class="card-label">
            <span class="dot-orange">■</span>
            &nbsp;AWAITING INFO
        </div>
        <div class="card-number">{waiting}</div>
    </div>
    """)

with c4:

    html(f"""
    <div class="card">
        <div class="card-label">
            <span class="dot-red">■</span>
            &nbsp;HITL REQUIRED
        </div>
        <div class="card-number red">{hitl_count}</div>
    </div>
    """)


st.markdown("<br>", unsafe_allow_html=True)


# ============================================================
# SEARCH / FILTER
# ============================================================

search_col, filter_col, count_col = st.columns([3, 5, 2])

with search_col:

    search = st.text_input(
        "Search",
        placeholder="Search claimant, organization, or claim ID...",
        label_visibility="collapsed"
    )

with filter_col:

    filter_choice = st.radio(
        "Status",
        [
            "All",
            "Claim Registered",
            "Waiting for Info",
            "HITL Invoked"
        ],
        horizontal=True,
        label_visibility="collapsed"
    )

with count_col:

    html(f"""
    <div style="
        text-align:right;
        padding-top:9px;
        color:#718198;
        font-size:12px;">
        Showing {min(10, len(records))} of {len(records)} submissions
    </div>
    """)


# ============================================================
# FILTER
# ============================================================

# Only the 10 most recent runs are displayed.
# Counts above continue to use ALL relevant runs.
display_records = records[:10]

filtered = display_records

if filter_choice != "All":

    filtered = [
        r for r in filtered
        if r["queue_status"] == filter_choice
    ]

if search:

    q = search.lower()

    filtered = [
        r for r in filtered
        if (
            q in r["run_id"].lower()
            or q in str(r["claim"]).lower()
            or q in r["notes"].lower()
        )
    ]


# ============================================================
# TABLE
# ============================================================

html("""
<div class="claim-table">

    <div class="table-header">
        <div>CLAIMANT</div>
        <div>ORGANIZATION</div>
        <div>FNOL RECEIVED</div>
        <div>MODE</div>
        <div>DOCUMENTS</div>
        <div>STATUS</div>
        <div>HITL INVOKED</div>
        <div>NOTES</div>
        <div></div>
    </div>

</div>
""")


# ============================================================
# ROWS
# ============================================================

for r in filtered:

    claim = r["claim"]

    claimant = claim.get(
        "Claimant",
        ""
    )

    fnol = claim.get(
        "FNOL Number",
        ""
    )

    employer = claim.get(
        "Employer",
        ""
    )

    organization_address = claim.get(
        "Organization Address",
        ""
    )

    created = r["created"]

    try:

        dt = datetime.fromisoformat(
            created.replace(
                "Z",
                "+00:00"
            )
        )

        received = dt.strftime(
            "%b %d, %I:%M %p"
        )

    except Exception:

        received = created

    # ============================================================
    # UI_DATA — SOURCE OF TRUTH FOR DASHBOARD DISPLAY
    # ============================================================

    ui = r.get("ui_data") or {}

    claimant = str(
        ui.get("CLAIMANT", "")
    ).strip()

    fnol = str(
        ui.get("FNOL_NUMBER", "")
    ).strip()

    organization = str(
        ui.get("EMPLOYER", "")
    ).strip()

    organization_address = str(
        ui.get("ORGANIZATION_ADDRESS", "")
    ).strip()


    # ============================================================
    # DOCUMENT STATUS
    # ============================================================

    def ui_doc_class(status):

        status = str(
            status or ""
        ).strip().upper()

        if status == "VALID":
            return "doc-ok"

        if status == "MISSING":
            return "doc-missing"

        if status == "ATTENTION":
            return "doc-warning"

        return "doc-neutral"


    froi_status = ui.get(
        "FROI_STATUS",
        ""
    )

    fmr_status = ui.get(
        "FMR_STATUS",
        ""
    )

    supervisor_status = ui.get(
        "SUPERVISOR_STATUS",
        ""
    )


    documents_html = f"""
        <span class="doc {ui_doc_class(froi_status)}">F</span>
        <span class="doc {ui_doc_class(fmr_status)}">F</span>
        <span class="doc {ui_doc_class(supervisor_status)}">E</span>
    """

    # Status
    if r["queue_status"] == "Claim Registered":

        status_html = """
        <span class="status status-registered">
            ● Claim Registered
        </span>
        """

    elif r["queue_status"] == "HITL Invoked":

        status_html = """
        <span class="status status-hitl">
            ● HITL Invoked
        </span>
        """

    else:

        status_html = """
        <span class="status status-waiting">
            ● Waiting for Info
        </span>
        """

    # Never display technical RUN_ID in the business UI.
    claimant_display = (
        claimant.upper()
        if claimant
        else ""
    )

    # FNOL is optional. If not generated, keep it blank.
    claim_id = fnol if fnol else ""

    # --------------------------------------------------------
    # ROW
    # --------------------------------------------------------

    html(f"""
    <div class="claim-row">

        <div>
            <div class="claim-name">
                {safe(claimant_display)}
            </div>
            <div class="claim-id">
                {safe(claim_id)}
            </div>
        </div>

        <div>
            <div class="org-name">
                {safe(organization)}
            </div>
            <div class="org-location">
                {safe(organization_address)}
            </div>
        </div>

        <div>
            <div class="received">
                {safe(received)}
            </div>
            <div class="received-relative">
                {safe(relative_time(r["created_dt"].isoformat() if r.get("created_dt") else ""))}
            </div>
        </div>

        <div>
            <span class="mode">✉ Email</span>
        </div>

        <div>
            {documents_html}
        </div>

        <div>
            {status_html}
        </div>

        <div>
            <span class="{'hitl-yes' if r['hitl'] == 'Yes' else 'hitl-no'}">
                {r['hitl']}
            </span>
        </div>

        <div>
            <div class="notes">
                {safe(r["notes"])}
            </div>
        </div>

        <div>
            <a class="view-btn"
               href="?selected_run={safe(r['run_id'])}"
               target="_self">
                View →
            </a>
        </div>

    </div>
    """)






# ============================================================
# DETAIL VIEW — RIGHT-SIDE CLAIM DRAWER
# ============================================================

ICON_CHECK = '<span class="ic ic-check"></span>'
ICON_WARN = '<span class="ic ic-warn"></span>'
ICON_ALERT = '<span class="ic ic-alert"></span>'
ICON_DOCS = '<span class="ic ic-docs"></span>'
ICON_XVAL = '<span class="ic ic-xval"></span>'
ICON_CLOCK = '<span class="ic ic-clock"></span>'
ICON_LIST = '<span class="ic ic-list"></span>'
ICON_MAIL = '<span class="ic ic-mail"></span>'
ICON_TICK = '<span class="ic ic-tick"></span>'
ICON_CROSS = '<span class="ic ic-cross"></span>'
ICON_DOC_MISSING = '<span class="ic ic-docmiss"></span>'
ICON_DOC_OK = '<span class="ic ic-docok"></span>'

STEP_LABELS = [
    "Claim Submitted",
    "Data Extraction (AI)",
    "Mandatory Document Check",
    "Cross-Document Verification",
    "Data Storage & Audit Log",
    "Completeness & Accuracy Check",
    "Policy & Business Rule Validation",
    "Claim Routing / Employer Communication",
]

# Per-document field specs: (label, candidate keys in UI_DATA / extracted claim).
# Document-specific keys are tried first; shared claim keys are fallbacks.
DOC_SPECS = {
    "froi": {
        "tab": "FROI",
        "title": "First Report of Injury (FROI)",
        "status_key": "FROI_STATUS",
        "missing_text": "First Report of Injury not received with this submission.",
        "fields": [
            ("Employee Name", ["FROI_EMPLOYEE_NAME", "CLAIMANT", "Claimant"]),
            ("Date of Injury", ["FROI_DATE_OF_INJURY", "DATE_OF_INJURY", "Date of Injury"]),
            ("Location", ["FROI_LOCATION", "INJURY_LOCATION", "Location"]),
            ("Body Part", ["FROI_BODY_PART", "BODY_PART", "Body Part"]),
            ("Injury Description", ["FROI_INJURY_DESCRIPTION", "INJURY_DESCRIPTION", "INJURY", "Injury"]),
            ("Reported By", ["FROI_REPORTED_BY", "REPORTED_BY", "Reported By"]),
        ],
    },
    "fmr": {
        "tab": "FMR",
        "title": "First Medical Report (FMR)",
        "status_key": "FMR_STATUS",
        "missing_text": "First Medical Report not received with this submission.",
        "fields": [
            ("Patient Name", ["FMR_PATIENT_NAME", "PATIENT_NAME", "CLAIMANT", "Claimant"]),
            ("Provider", ["FMR_PROVIDER", "PROVIDER", "Provider"]),
            ("Date of Treatment", ["FMR_DATE_OF_TREATMENT", "DATE_OF_TREATMENT", "Date of Treatment"]),
            ("Diagnosis", ["FMR_DIAGNOSIS", "DIAGNOSIS", "Diagnosis"]),
            ("Treatment", ["FMR_TREATMENT", "TREATMENT", "Treatment"]),
            ("Return to Work", ["FMR_RETURN_TO_WORK", "RETURN_TO_WORK", "Return to Work"]),
        ],
    },
    "emp": {
        "tab": "Employer Confirmation",
        "title": "Employer Confirmation",
        "status_key": "SUPERVISOR_STATUS",
        "missing_text": "Employer injury confirmation / acknowledgment not received with this submission.",
        "fields": [
            ("Employer", ["EMP_EMPLOYER", "EMPLOYER", "Employer"]),
            ("Authorized Signer", ["EMP_AUTHORIZED_SIGNER", "AUTHORIZED_SIGNER", "SUPERVISOR_NAME", "Authorized Signer"]),
            ("Confirmation Date", ["EMP_CONFIRMATION_DATE", "CONFIRMATION_DATE", "Confirmation Date"]),
            ("Statement", ["EMP_STATEMENT", "SUPERVISOR_STATEMENT", "Statement"]),
        ],
    },
}


def fmt_dt(dt):
    """Aug 12, 08:14 AM (IST)."""
    return dt.astimezone(IST).strftime("%b %d, %I:%M %p") if dt else "—"


def fmt_short(dt):
    """08/12 08:14 (IST)."""
    return dt.astimezone(IST).strftime("%m/%d %H:%M") if dt else ""


def lookup(sources, keys):
    """Return (value, key) for the first non-empty key across the sources."""
    for src in sources:
        for k in keys:
            for kk in (k, str(k).upper()):
                v = src.get(kk) if isinstance(src, dict) else None
                if v not in (None, "") and str(v).strip():
                    return str(v).strip(), kk
    return "", None


def confidence_for(ui, key):
    """Field confidence (0–100) if Kognitos provides <KEY>_CONFIDENCE."""
    if not key:
        return None
    for suffix in ("_CONFIDENCE", "_CONF"):
        raw = ui.get(f"{str(key).upper()}{suffix}")
        if raw in (None, ""):
            continue
        try:
            c = float(str(raw).replace("%", ""))
            return int(round(c * 100 if c <= 1 else c))
        except ValueError:
            continue
    return None


def conf_class(c):
    return "conf-hi" if c >= 90 else "conf-mid" if c >= 75 else "conf-lo"


def doc_state(status):
    s = str(status or "").upper()
    if s == "VALID":
        return "ok"
    if s == "MISSING":
        return "missing"
    if s == "ATTENTION":
        return "warn"
    return "unknown"


def build_doc(key, ui, claim):
    spec = DOC_SPECS[key]
    state = doc_state(ui.get(spec["status_key"]))
    fields = []
    if state != "missing":
        for label, keys in spec["fields"]:
            val, found = lookup([ui, claim], keys)
            if val:
                fields.append((label, val, confidence_for(ui, found)))
    flag = {"ok": "ok", "warn": "warn", "missing": "bad"}.get(state, "unknown")
    if any(c is not None and c < 75 for _, _, c in fields):
        flag = "bad"
    elif flag == "ok" and any(c is not None and c < 90 for _, _, c in fields):
        flag = "warn"
    return {"key": key, "spec": spec, "state": state, "fields": fields, "flag": flag}


def render_doc_html(doc):
    spec = doc["spec"]
    if doc["state"] == "missing":
        return f"""
        <div class="doc-render">
            <div class="doc-letterhead"><div class="dtitle">{safe(spec['title'])}</div><div class="dsub">NOT RECEIVED</div></div>
            <div class="doc-empty">{ICON_DOC_MISSING}
                <div class="de-title">Document not received</div>
                <div class="de-sub">{safe(spec['missing_text'])}</div>
            </div>
        </div>"""

    has_conf = any(c is not None for _, _, c in doc["fields"])
    sub = "AI-EXTRACTED · FIELD CONFIDENCE SHOWN" if has_conf else "AI-EXTRACTED"

    if not doc["fields"]:
        msg = (
            "Document received. Extracted field details are not available for this run."
            if doc["state"] in ("ok", "warn")
            else "Document status has not been reported yet."
        )
        return f"""
        <div class="doc-render">
            <div class="doc-letterhead"><div class="dtitle">{safe(spec['title'])}</div><div class="dsub">{sub}</div></div>
            <div class="doc-empty">{ICON_DOC_OK}
                <div class="de-title">{'Received' if doc['state'] in ('ok', 'warn') else 'Pending'}</div>
                <div class="de-sub">{msg}</div>
            </div>
        </div>"""

    default_cls = {"ok": "conf-hi", "warn": "conf-mid"}.get(doc["state"], "")
    cells = []
    for label, val, c in doc["fields"]:
        cls = conf_class(c) if c is not None else default_cls
        conf_html = f'<div class="df-conf {cls}">{c}%</div>' if c is not None else ""
        cells.append(f"""
            <div class="doc-field {cls}">
                <div class="df-label">{safe(label)}</div>
                <div class="df-row"><div class="df-value">{safe(val)}</div>{conf_html}</div>
            </div>""")
    return f"""
    <div class="doc-render">
        <div class="doc-letterhead"><div class="dtitle">{safe(spec['title'])}</div><div class="dsub">{sub}</div></div>
        <div class="doc-fields">{''.join(cells)}</div>
    </div>"""


def build_xval(rec, docs, overall):
    rows = []
    status = rec["queue_status"]
    missing = [d for d in docs.values() if d["state"] == "missing"]
    attention = [d for d in docs.values() if d["state"] == "warn" or d["flag"] == "bad" and d["state"] != "missing"]
    present = [d for d in docs.values() if d["state"] in ("ok", "warn")]
    manual = rec.get("manual") or {}

    if overall == "PROCESSED" and not missing and not attention:
        rows += [
            ("pass", "FROI and FMR employee names match."),
            ("pass", "Date of injury on FROI aligns with treatment date on FMR."),
            ("pass", "Injury details consistent across documents."),
        ]
    else:
        if present and overall != "VALIDATION_FAILED":
            names = ", ".join(d["spec"]["tab"] for d in present)
            rows.append(("pass", f"{names} received and verified."))
        for d in missing:
            rows.append(("fail", f"{d['spec']['title']} required for Workers' Compensation intake is missing."))
        for d in attention:
            rows.append(("fail", f"{d['spec']['title']}: one or more fields fall below the extraction confidence threshold and require manual verification."))
        if overall == "VALIDATION_FAILED":
            rows.append(("fail", rec.get("orig_notes") or rec.get("notes") or "Cross-document validation failed — human review required."))

    if manual.get("manual_approved"):
        rows.append(("pass", f"Reviewed and approved manually by {HANDLER_NAME}."))

    if not rows:
        rows.append(("pass" if status == "Claim Registered" else "fail",
                     "Validation results are not yet available for this run."))
    return rows


def build_timeline(rec, docs, overall):
    created = rec.get("created_dt")
    updated = rec.get("updated_dt")
    status = rec["queue_status"]
    manual = rec.get("manual") or {}
    missing = [d["spec"]["tab"] for d in docs.values() if d["state"] == "missing"]
    attention = [d["spec"]["tab"] for d in docs.values() if d["state"] == "warn"]

    steps = [["pending", None, None] for _ in STEP_LABELS]  # state, time, note
    steps[0] = ["done", created, None]

    if overall == "PROCESSED" or (status == "Claim Registered" and not manual.get("manual_approved")):
        for i in range(1, 8):
            steps[i] = ["done", None, None]
        steps[7][1] = updated
    else:
        steps[1] = ["done", None, None]
        if missing:
            steps[2] = ["blocked", None, f"Mandatory Document Check — {', '.join(missing)} missing"]
            steps[7] = ["done", updated, None]  # request for missing info sent
        elif attention:
            steps[2] = ["done", None, None]
            steps[3] = ["blocked", None, f"Cross-Document Verification — low-confidence fields in {', '.join(attention)}"]
        elif overall == "VALIDATION_FAILED" or status == "HITL Invoked":
            steps[2] = ["done", None, None]
            steps[3] = ["blocked", None, rec.get("orig_notes") or rec.get("notes") or "Validation failed"]

    if manual.get("manual_approved"):
        for s in steps:
            if s[0] in ("pending", "blocked"):
                s[0], s[1], s[2] = "done", manual["manual_approved"], None
    return steps


def render_timeline_html(steps):
    out = []
    for i, (state, t, note) in enumerate(steps):
        dot = (
            f'<div class="tl-dot done">{ICON_TICK}</div>' if state == "done"
            else '<div class="tl-dot blocked"></div>' if state == "blocked"
            else '<div class="tl-dot pending"></div>'
        )
        extra = ""
        if state == "done" and t:
            extra = f'<div class="tl-time">{fmt_short(t)}</div>'
        elif state == "blocked" and note:
            extra = f'<div class="tl-note">Blocked — {safe(note)}</div>'
        out.append(f"""
        <div class="tl-step">{dot}
            <div class="tl-content">
                <div class="tl-label {'pending-text' if state == 'pending' else ''}">{safe(STEP_LABELS[i])}</div>
                {extra}
            </div>
        </div>""")
    return f'<div class="timeline">{"".join(out)}</div>'


def build_activity(rec, overall):
    created = rec.get("created_dt")
    updated = rec.get("updated_dt")
    status = rec["queue_status"]
    manual = rec.get("manual") or {}
    notes = rec.get("orig_notes") or rec.get("notes") or ""

    items = [("Claim submitted via email intake.", created)]
    if rec.get("ui_data"):
        items.append(("AI extraction and document validation completed.", updated))
    if overall == "PROCESSED":
        items.append(("All mandatory documents verified; cross-validation passed. Claim registered.", updated))
    elif overall == "DOCUMENTS_MISSING":
        items.append((notes or "Required documents missing — request sent for missing information.", updated))
    elif overall == "VALIDATION_FAILED":
        items.append((f"Escalated to Human-in-the-Loop review. {notes}".strip(), updated))
    k_ids = []
    for act in rec.get("k_actions", []):
        to = act.get("to") or "the employer"
        text = {
            "reminder": f"Reminder email sent to {to} via Kognitos",
            "escalate": f"Escalated to Human-in-the-Loop review; HITL email sent to {to} via Kognitos",
            "register": "Claim registered and routed to claim handler via Kognitos",
        }[act["kind"]]
        if act["state"] == "failed":
            text += " — the email run FAILED in Kognitos"
        elif act["state"] in ("running", "pending"):
            text += " — run in progress"
        text += f" (Kognitos run {act['k_run']})."
        items.append((text, act["created"]))
        k_ids.append(act["k_run"])
    for text, t in manual.get("activity", []):
        if any(k and k in text for k in k_ids):
            continue  # already listed from Kognitos
        items.append((text, t))
    items.sort(key=lambda it: it[1] or datetime.min.replace(tzinfo=timezone.utc))
    return items


def render_activity_html(items):
    rows = "".join(
        f"""<div class="act-row"><div class="act-dot"></div><div>
                <div class="act-text">{safe(text)}</div>
                {f'<div class="act-time">{fmt_short(t)}</div>' if t else ''}
            </div></div>"""
        for text, t in items
    )
    return f'<div class="activity-log">{rows}</div>'


def render_alert_html(rec):
    status = rec["queue_status"]
    notes = rec.get("notes") or ""
    created = rec.get("created_dt")
    deadline = created + timedelta(hours=SLA_HOURS) if created else None
    now = datetime.now(timezone.utc)

    if status == "Waiting for Info":
        sla = (
            f'<div class="sla">SLA deadline: {fmt_dt(deadline)} · handler review not required unless deadline is exceeded</div>'
            if deadline else ""
        )
        return f"""<div class="alert-box amber">{ICON_WARN}
            <div><b>Action needed:</b> {safe(notes or 'Required claim information is still pending.')}{sla}</div></div>"""

    if status == "HITL Invoked":
        if deadline and now > deadline:
            sla = f'<div class="sla">SLA deadline was: {fmt_dt(deadline)} — now overdue. Manual handler action required to proceed.</div>'
        elif deadline:
            sla = f'<div class="sla">SLA deadline: {fmt_dt(deadline)} · manual handler action required to proceed.</div>'
        else:
            sla = ""
        return f"""<div class="alert-box red">{ICON_ALERT}
            <div><b>Human-in-the-loop review required:</b> {safe(notes or 'Validation failed.')}{sla}</div></div>"""

    return f"""<div class="alert-box green">{ICON_CHECK}
        <div>All mandatory documents received and validated. Claim registered and routed to claim handler — no handler action required.</div></div>"""


if st.session_state.get("show_detail", False):

    selected_id = str(st.session_state.get("selected_run") or "").strip()

    selected = next(
        (r for r in records if str(r.get("run_id", "")).strip() == selected_id),
        None,
    )

    if selected is None:
        st.error("Selected claim could not be found.")
        st.stop()

    run_id = selected["run_id"]
    claim = selected.get("claim") or {}
    ui = selected.get("ui_data") or {}
    overall = str(ui.get("OVERALL_STATUS", "")).upper()
    status = selected["queue_status"]

    claimant, _ = lookup([ui, claim], ["CLAIMANT", "Claimant"])
    fnol, _ = lookup([ui, claim], ["FNOL_NUMBER", "FNOL Number"])
    employer, _ = lookup([ui, claim], ["EMPLOYER", "Employer"])
    address, _ = lookup([ui, claim], ["ORGANIZATION_ADDRESS", "Organization Address"])
    injury_date, _ = lookup([ui, claim], ["DATE_OF_INJURY", "Date of Injury"])
    injury, _ = lookup([ui, claim], ["INJURY_TYPE", "INJURY", "Injury Type", "Injury"])
    policy, _ = lookup([ui, claim], ["POLICY_NUMBER", "Policy Number", "POLICY"])
    sender, _ = lookup([ui, claim], ["SUBMITTED_BY", "SENDER", "SENDER_EMAIL", "FROM", "Submitted By", "Sender"])

    docs = {k: build_doc(k, ui, claim) for k in ("froi", "fmr", "emp")}

    badge_cls, badge_label = {
        "Claim Registered": ("sb-approved", "Claim Registered"),
        "HITL Invoked": ("sb-hitl", "HITL Invoked"),
    }.get(status, ("sb-waiting", "Waiting for Info"))

    id_line = " · ".join(
        p for p in [fnol, " — ".join(x for x in [employer, address] if x)] if p
    )

    # Payload passed to Kognitos for every action on this claim.
    # Employer contact for reminder emails: UI_DATA sender, else the intake email's sender.
    contact_email = sender if EMAIL_RE.fullmatch(sender or "") else ""
    if not contact_email:
        m = EMAIL_RE.search(sender or "") or EMAIL_RE.search(
            str((selected.get("details") or {}).get("user_inputs", ""))
        )
        contact_email = m.group(0) if m else ""

    payload = {
        "run_id": run_id,
        "fnol": fnol,
        "claimant": claimant,
        "employer": employer,
        "email": contact_email,
        "date_of_injury": injury_date,
        "injury": injury,
        "policy": policy,
        "notes": selected.get("orig_notes") or selected.get("notes") or "",
        "overall": overall,
        # For the claims processor / email drafts
        "ui": ui,
        "intake_inputs": (selected.get("details") or {}).get("user_inputs") or {},
        "status": status,
        "missing_keys": [k for k, d in docs.items() if d["state"] == "missing"],
        "received_keys": [k for k, d in docs.items() if d["state"] in ("ok", "warn")],
        "sla_deadline": (
            f"{_long_date((selected['created_dt'] + timedelta(hours=SLA_HOURS)).astimezone(IST).strftime('%Y-%m-%d'))}"
            f" at {(selected['created_dt'] + timedelta(hours=SLA_HOURS)).astimezone(IST).strftime('%I:%M %p').lstrip('0')}"
            if selected.get("created_dt") else ""
        ),
        "sla_overdue": bool(
            selected.get("created_dt")
            and datetime.now(timezone.utc) > selected["created_dt"] + timedelta(hours=SLA_HOURS)
        ),
    }

    # Click outside the drawer returns to the queue.
    html('<a class="drawer-overlay" href="?" target="_self"><span class="sr-only">Back to claims queue</span></a>')

    with st.container(key="detail_drawer"):

        # ---------------- HEADER ----------------
        with st.container(key="drawer_head"):
            html(f"""
            <div class="dh">
                <a class="dh-back" href="?" target="_self">&larr; Back to Claims Queue</a>
                <div class="dh-top">
                    <div>
                        <div class="dh-title">{safe(claimant.upper() if claimant else 'Claim')}</div>
                        <div class="dh-id mono">{safe(id_line)}</div>
                    </div>
                    <div class="dh-right">
                        <span class="sbadge {badge_cls}"><span class="sdot"></span>{badge_label}</span>
                        <a class="dh-close" href="?" target="_self" title="Close" aria-label="Close">&#10005;</a>
                    </div>
                </div>
                <div class="sg">
                    <div><div class="sg-label">Policy Number</div><div class="sg-value mono">{safe(policy or '—')}</div></div>
                    <div><div class="sg-label">Date of Injury</div><div class="sg-value">{safe(injury_date or '—')}</div></div>
                    <div><div class="sg-label">Injury Type</div><div class="sg-value">{safe(injury or '—')}</div></div>
                    <div><div class="sg-label">Received Via</div><div class="sg-value">Email</div></div>
                    <div><div class="sg-label">Submitted By</div><div class="sg-value">{safe(sender or '—')}</div></div>
                    <div><div class="sg-label">FNOL Received</div><div class="sg-value mono">{safe(fmt_dt(selected.get('created_dt')))}</div></div>
                </div>
            </div>
            """)

        # ---------------- BODY ----------------
        with st.container(key="drawer_body"):

            html(render_alert_html(selected))

            # Documents panel — CSS-only tabs (instant switching, no rerun)
            radios = "".join(
                f'<input type="radio" name="doctab" id="dt-{k}" {"checked" if k == "froi" else ""}>'
                for k in ("froi", "fmr", "emp")
            )
            tabs = "".join(
                f'<label class="doc-tab" for="dt-{k}">'
                f'<span class="doc-tab-flag {docs[k]["flag"]}"></span>{safe(DOC_SPECS[k]["tab"])}</label>'
                for k in ("froi", "fmr", "emp")
            )
            panes = "".join(
                f'<div class="doc-pane doc-pane-{k}">{render_doc_html(docs[k])}</div>'
                for k in ("froi", "fmr", "emp")
            )
            html(f"""
            <div class="panel">
                <div class="panel-head"><div class="panel-title">{ICON_DOCS} Documents</div></div>
                <div class="doc-tabs-wrap">
                    {radios}
                    <div class="doc-tabs">{tabs}</div>
                    {panes}
                </div>
            </div>
            """)

            xval_rows = "".join(
                f"""<div class="xval-row">
                        <div class="xval-icon {r}">{ICON_TICK if r == 'pass' else ICON_CROSS}</div>
                        <div class="xval-text">{safe(text)}</div>
                    </div>"""
                for r, text in build_xval(selected, docs, overall)
            )

            html(f"""
            <div class="panel">
                <div class="panel-head"><div class="panel-title">{ICON_XVAL} Cross-Document Validation</div></div>
                <div class="panel-body">{xval_rows}</div>
            </div>
            """)

            html(f"""
            <div class="panel">
                <div class="panel-head"><div class="panel-title">{ICON_CLOCK} Processing Timeline</div></div>
                <div class="panel-body">{render_timeline_html(build_timeline(selected, docs, overall))}</div>
            </div>
            """)

            # Email drafts — exactly what each button sends for THIS claim.
            previews = []
            if status in ("Waiting for Info", "HITL Invoked"):
                to_addr = REMINDER_EMAIL_TO or payload["email"] or "employer contact"
                previews.append(("Send Reminder to Employer", "reminder"))
                if status == "Waiting for Info":
                    previews.append(("Escalate to HITL Now", "escalate"))
                mails = ""
                for label, act in previews:
                    subj, body_txt = compose_email(act, payload)
                    mails += f"""
                    <details class="mail">
                        <summary>
                            <span class="mail-btn">{safe(label)}</span>
                            <span class="mail-scn">Scenario {email_scenario(act, payload)}</span>
                            <span class="mail-subj">{safe(subj)}</span>
                        </summary>
                        <div class="mail-meta"><b>To:</b> {safe(to_addr)} &nbsp;·&nbsp; <b>Subject:</b> {safe(subj)}</div>
                        <div class="mail-body">{safe(body_txt)}</div>
                    </details>"""
                html(f"""
                <div class="panel">
                    <div class="panel-head">
                        <div class="panel-title">{ICON_MAIL} Email Drafts</div>
                        <div class="panel-sub">Filled from this claim · sent via Kognitos</div>
                    </div>
                    <div class="panel-body mail-list">{mails}</div>
                </div>
                """)

            html(f"""
            <div class="panel">
                <div class="panel-head"><div class="panel-title">{ICON_LIST} Activity Log</div></div>
                <div class="panel-body">{render_activity_html(build_activity(selected, overall))}</div>
            </div>
            """)

        # ---------------- ACTION BAR (per status) ----------------
        #   Claim Registered  -> routing status only, no actions
        #   Waiting for Info  -> Register & Route · Send Reminder · Escalate to HITL
        #   HITL Invoked      -> Register & Route · Send Reminder
        with st.container(key="drawer_actions"):

            if status == "Claim Registered":
                manual = selected.get("manual") or {}
                handler_reg = manual.get("manual_approved") or selected.get("registered_by_handler")
                when = handler_reg or selected.get("updated_dt")
                by = "by claims handler" if handler_reg else "automatically by Kognitos"
                html(f"""
                <div class="routed-bar">
                    {ICON_CHECK}
                    <div>Claim registered &amp; routed to claim handler
                        <div class="rb-sub">Routed {by}{f' · {fmt_dt(when)}' if when else ''}</div>
                    </div>
                </div>
                """)

            else:
                clicked = None

                if st.button(
                    "Mark as Claim Registered & Route to Claim Handler",
                    icon=":material/check:",
                    key="act_approve",
                ):
                    clicked = "register"

                if st.button(
                    "Send Reminder to Employer",
                    icon=":material/notifications:",
                    key="act_reminder",
                ):
                    clicked = "reminder"

                if status == "Waiting for Info":
                    if st.button(
                        "Escalate to HITL Now",
                        icon=":material/error:",
                        key="act_escalate",
                    ):
                        clicked = "escalate"

                if clicked:
                    with st.spinner({
                        "register": "Registering claim in Kognitos…",
                        "reminder": "Sending reminder email via Kognitos…",
                        "escalate": "Escalating to HITL and sending email via Kognitos…",
                    }[clicked]):
                        run_action(clicked, payload)
                    st.rerun()
