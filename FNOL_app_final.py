import base64
import streamlit as st
import sys
import html as html_lib
from datetime import datetime
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

.st-key-detail_drawer {
    position:fixed !important;
    top:0 !important;
    right:0 !important;
    bottom:0 !important;
    width:720px !important;
    max-width:94vw !important;
    height:100vh !important;
    z-index:9999 !important;
    background:#ffffff !important;
    border-left:1px solid #dce2e9 !important;
    box-shadow:-8px 0 30px rgba(20,34,56,.15) !important;
    padding:24px !important;
    overflow-y:auto !important;
    box-sizing:border-box !important;
}

.st-key-detail_drawer > div {
    max-width:none !important;
}

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

    return {
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


# ============================================================
# PROCESS RUNS
# ============================================================

records = []

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
                {safe(relative_time(r.get("created", "")))}
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
# DETAIL VIEW
# ============================================================



if st.session_state.get("show_detail", False):

    selected_id = str(
        st.session_state.get("selected_run") or ""
    ).strip()

    selected = next(
        (
            r for r in records
            if str(r.get("run_id", "")).strip() == selected_id
        ),
        None
    )

    if selected is None:
        st.error("Selected claim could not be found.")
        st.stop()

    with st.container(key="detail_drawer"):
        claim = selected.get("claim") or {}
        ui = selected.get("ui_data") or {}

        claimant = ui.get("CLAIMANT", "") or claim.get("Claimant", "")
        fnol = ui.get("FNOL_NUMBER", "") or claim.get("FNOL Number", "")
        employer = ui.get("EMPLOYER", "") or claim.get("Employer", "")
        address = (
            ui.get("ORGANIZATION_ADDRESS", "")
            or claim.get("Organization Address", "")
        )
        injury_date = (
            ui.get("DATE_OF_INJURY", "")
            or claim.get("Date of Injury", "")
        )
        injury = ui.get("INJURY", "") or claim.get("Injury", "")

        overall = ui.get("OVERALL_STATUS", "").upper()

        if overall == "PROCESSED":
            status = "Claim Registered"
        elif overall == "DOCUMENTS_MISSING":
            status = "Waiting for Info"
        elif overall == "VALIDATION_FAILED":
            status = "HITL Invoked"
        else:
            status = selected.get("queue_status", "Processing")

        froi = ui.get("FROI_STATUS", "").upper()
        fmr = ui.get("FMR_STATUS", "").upper()
        supervisor = ui.get("SUPERVISOR_STATUS", "").upper()

        # --------------------------------------------------------
        # HEADER
        # --------------------------------------------------------

        st.markdown("## Claim Details")

        if st.button("← Back to Claims", key="detail_back"):
            st.session_state.show_detail = False
            st.session_state.selected_run = None
            st.query_params.clear()
            st.rerun()

        st.divider()

        c1, c2 = st.columns([4, 1])

        with c1:
            st.markdown(
                f"### {claimant.upper() if claimant else 'Claim'}"
            )

            if fnol:
                st.caption(f"FNOL: {fnol}")

            if employer:
                st.caption(employer)

            if address:
                st.caption(address)

        with c2:
            st.success(status)

        # --------------------------------------------------------
        # CLAIM INFORMATION
        # --------------------------------------------------------

        st.markdown("### Claim Information")

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.caption("FNOL NUMBER")
            st.write(fnol or "—")

        with c2:
            st.caption("CLAIMANT")
            st.write(claimant or "—")

        with c3:
            st.caption("DATE OF INJURY")
            st.write(injury_date or "—")

        with c4:
            st.caption("EMPLOYER")
            st.write(employer or "—")

        c1, c2 = st.columns(2)

        with c1:
            st.caption("ORGANIZATION ADDRESS")
            st.write(address or "—")

        with c2:
            st.caption("INJURY")
            st.write(injury or "—")

        # --------------------------------------------------------
        # DOCUMENTS
        # --------------------------------------------------------

        st.markdown("### Documents")

        d1, d2, d3 = st.columns(3)

        with d1:
            if froi == "VALID":
                st.success("FROI — VALID")
            elif froi == "MISSING":
                st.error("FROI — MISSING")
            else:
                st.warning(f"FROI — {froi or 'UNKNOWN'}")

        with d2:
            if fmr == "VALID":
                st.success("FMR — VALID")
            elif fmr == "MISSING":
                st.error("FMR — MISSING")
            else:
                st.warning(f"FMR — {fmr or 'UNKNOWN'}")

        with d3:
            if supervisor == "VALID":
                st.success("Employer Confirmation — VALID")
            elif supervisor == "MISSING":
                st.error("Employer Confirmation — MISSING")
            else:
                st.warning(
                    f"Employer Confirmation — "
                    f"{supervisor or 'UNKNOWN'}"
                )

        # --------------------------------------------------------
        # NOTES
        # --------------------------------------------------------

        st.markdown("### Processing Notes")

        notes = ui.get("NOTES", "") or selected.get(
            "notes",
            "No issues flagged."
        )

        st.info(notes)

        # --------------------------------------------------------
        # VALIDATION
        # --------------------------------------------------------

        st.markdown("### Cross-Document Validation")

        if overall == "PROCESSED":

            st.success(
                "✓ Required documents received and validated."
            )

            st.success(
                "✓ Employee information reviewed across documents."
            )

            st.success(
                "✓ Date and injury information reviewed."
            )

        elif overall == "DOCUMENTS_MISSING":

            st.warning(
                "Required information/documents are still pending."
            )

        elif overall == "VALIDATION_FAILED":

            st.error(
                "Human review is required before claim processing can continue."
            )

        # --------------------------------------------------------
        # PROCESSING TIMELINE
        # --------------------------------------------------------

        st.markdown("### Processing Timeline")

        timeline = [
            "Claim Submitted",
            "Data Extraction (AI)",
            "Mandatory Document Check",
            "Cross-Document Verification",
            "Policy & Business Rule Validation",
        ]

        for item in timeline:
            st.write(f"✓ {item}")

        # --------------------------------------------------------
        # ACTIVITY LOG
        # --------------------------------------------------------

        st.markdown("### Activity Log")

        st.write("Claim submitted via email intake.")
        st.write("AI extraction and document validation completed.")
        st.write(notes)

