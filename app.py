import html
import json
from pathlib import Path

import streamlit as st

from sami_processor import process_document
from faizan_analysis import analyze_documents
from muteeba_matching import run_full_analysis, adapt_analysis_output


BASE_DIR = Path(__file__).resolve().parent
ASSETS = BASE_DIR / "assets"

st.set_page_config(
    page_title="TenderWise AI",
    page_icon=str(ASSETS / "logo_icon.png"),
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------------------
# Theme
# ---------------------------------------------------------------------
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --red: #E52521;
    --red-dark: #B91C1C;
    --black: #111111;
    --text: #202020;
    --muted: #6B6B6B;
    --line: #E9E9E9;
    --soft: #F7F7F7;
    --white: #FFFFFF;
    --green: #15803D;
    --amber: #B7791F;
}

#MainMenu, footer, header { visibility: hidden; }
div[data-testid="stToolbar"] { display: none; }
.stApp { background: #FFFFFF; }
html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    color: var(--text);
}

.main .block-container {
    max-width: 1180px;
    padding: 92px 34px 70px;
}

[data-testid="stFileUploader"] {
    background: #FAFAFA;
    border: 1.5px dashed #D7D7D7;
    border-radius: 16px;
    padding: 8px;
    transition: border-color .15s ease, box-shadow .15s ease, background .15s ease;
}
[data-testid="stFileUploader"]:hover {
    border-color: var(--red);
    background: #FFF9F9;
    box-shadow: 0 5px 18px rgba(17,17,17,.05);
}
[data-testid="stFileUploader"] section {
    border: 0 !important;
    background: transparent !important;
}

.stButton > button, .stDownloadButton > button {
    border-radius: 10px !important;
    min-height: 44px !important;
    font-weight: 700 !important;
    border: 1px solid var(--red) !important;
    background: var(--red) !important;
    color: white !important;
    box-shadow: 0 5px 14px rgba(229,37,33,.16) !important;
}
.stButton > button:hover, .stDownloadButton > button:hover {
    background: var(--red-dark) !important;
    border-color: var(--red-dark) !important;
}
.stDownloadButton > button {
    background: #111111 !important;
    border-color: #111111 !important;
    box-shadow: none !important;
}

div[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid var(--line);
    border-radius: 14px;
    padding: 16px 18px;
    box-shadow: 0 2px 10px rgba(17,17,17,.035);
}
div[data-testid="stMetricLabel"] {
    color: var(--muted) !important;
    font-weight: 600 !important;
    font-size: 12px !important;
}
div[data-testid="stMetricValue"] {
    color: var(--black) !important;
    font-weight: 800 !important;
}

div[data-testid="stTabs"] button {
    font-weight: 650 !important;
    color: #707070 !important;
}
div[data-testid="stTabs"] button[aria-selected="true"] {
    color: var(--red) !important;
    border-bottom: 2px solid var(--red) !important;
}

.streamlit-expanderHeader {
    background: #FAFAFA !important;
    border: 1px solid var(--line) !important;
    border-radius: 10px !important;
    font-weight: 650 !important;
}

[data-testid="stProgressBar"] > div > div > div > div {
    background: var(--red) !important;
}

.app-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 24px;
    min-height: 64px;
    padding-bottom: 20px;
    border-bottom: 1px solid var(--line);
}
.brand {
    display: flex;
    align-items: center;
    gap: 11px;
}
.brand-name {
    font-size: 24px;
    line-height: 1;
    font-weight: 800;
    letter-spacing: -0.7px;
    color: var(--black);
}
.brand-name span { color: var(--red); }
.brand-mark {
    width: 42px;
    height: 42px;
    object-fit: contain;
}
.header-note {
    color: #858585;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: .3px;
    text-transform: uppercase;
}

.hero {
    padding: 43px 0 31px;
}
.hero-kicker {
    color: var(--red);
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 1.4px;
    text-transform: uppercase;
    margin-bottom: 10px;
}
.hero h1 {
    margin: 0;
    color: var(--black);
    font-size: 40px;
    line-height: 1.08;
    letter-spacing: -1.5px;
    font-weight: 800;
}
.hero p {
    max-width: 790px;
    margin: 16px 0 0;
    color: #656565;
    font-size: 16px;
    line-height: 1.65;
}

.upload-heading {
    font-size: 20px;
    font-weight: 800;
    color: var(--black);
    margin: 12px 0 5px;
}
.upload-sub {
    color: var(--muted);
    font-size: 13px;
    margin-bottom: 14px;
}
.file-card {
    margin-top: 9px;
    padding: 11px 13px;
    border: 1px solid #E8E8E8;
    border-radius: 10px;
    background: #FFFFFF;
    font-size: 12px;
    color: #555;
}
.file-card strong { color: #202020; }

.section {
    margin-top: 38px;
}
.section-head {
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    gap: 16px;
    margin-bottom: 15px;
}
.section-title {
    font-size: 21px;
    line-height: 1.2;
    font-weight: 800;
    color: var(--black);
    letter-spacing: -.35px;
}
.section-caption {
    color: #888;
    font-size: 12px;
}

.process-shell {
    border: 1px solid var(--line);
    border-radius: 16px;
    padding: 22px 24px;
    background: #FFFFFF;
    box-shadow: 0 8px 28px rgba(17,17,17,.045);
    margin-top: 24px;
}
.process-top {
    display: flex;
    justify-content: space-between;
    gap: 18px;
    align-items: center;
    margin-bottom: 14px;
}
.process-title {
    font-size: 15px;
    font-weight: 750;
    color: var(--black);
}
.process-percent {
    font-size: 13px;
    font-weight: 750;
    color: var(--red);
}
.progress-track {
    height: 5px;
    width: 100%;
    background: #EEEEEE;
    border-radius: 10px;
    margin-bottom: 20px;
    overflow: hidden;
}
.progress-fill {
    height: 100%;
    background: #E52521;
    border-radius: 10px;
    transition: width .25s ease;
}

.progress-0 { width: 0%; }
.progress-5 { width: 5%; }
.progress-10 { width: 10%; }
.progress-15 { width: 15%; }
.progress-20 { width: 20%; }
.progress-25 { width: 25%; }
.progress-30 { width: 30%; }
.progress-35 { width: 35%; }
.progress-40 { width: 40%; }
.progress-45 { width: 45%; }
.progress-50 { width: 50%; }
.progress-55 { width: 55%; }
.progress-60 { width: 60%; }
.progress-65 { width: 65%; }
.progress-70 { width: 70%; }
.progress-75 { width: 75%; }
.progress-80 { width: 80%; }
.progress-85 { width: 85%; }
.progress-90 { width: 90%; }
.progress-95 { width: 95%; }
.progress-100 { width: 100%; }
.step {
    display: grid;
    grid-template-columns: 32px 1fr auto;
    align-items: center;
    gap: 12px;
    min-height: 47px;
    position: relative;
}
.step:not(:last-child)::before {
    content: "";
    position: absolute;
    left: 15px;
    top: 31px;
    height: 28px;
    width: 2px;
    background: #ECECEC;
}
.step-dot {
    width: 30px;
    height: 30px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 11px;
    font-weight: 800;
    background: #F0F0F0;
    color: #999;
    border: 1px solid #E1E1E1;
    z-index: 1;
}
.step.done .step-dot, .step.active .step-dot {
    background: var(--red);
    border-color: var(--red);
    color: #FFFFFF;
}
.step.active .step-dot {
    box-shadow: 0 0 0 5px rgba(229,37,33,.10);
}
.step-name {
    font-size: 13px;
    font-weight: 650;
    color: #9A9A9A;
}
.step.done .step-name, .step.active .step-name {
    color: var(--black);
}
.step-state {
    font-size: 11px;
    color: #A0A0A0;
    font-weight: 600;
}
.step.done .step-state { color: var(--green); }
.step.active .step-state { color: var(--red); }

.decision {
    border: 1px solid var(--line);
    border-radius: 16px;
    background: #FFFFFF;
    padding: 25px 27px;
    box-shadow: 0 8px 30px rgba(17,17,17,.05);
}
.decision-label {
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    color: #888;
    font-weight: 800;
}
.decision-value {
    font-size: 30px;
    font-weight: 850;
    letter-spacing: -.8px;
    margin: 7px 0 6px;
}
.decision-reason {
    color: #555;
    font-size: 14px;
    line-height: 1.6;
    max-width: 820px;
}

.badge {
    display: inline-block;
    padding: 4px 9px;
    border-radius: 999px;
    font-size: 10px;
    line-height: 1.2;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: .4px;
    white-space: nowrap;
}
.badge-matched { color: #126A34; background: #EAF7EF; }
.badge-missing { color: #B42318; background: #FFF0EF; }
.badge-unclear { color: #8A5A00; background: #FFF7E5; }
.badge-mandatory { color: #B42318; background: #FFF0EF; }
.badge-important { color: #8A5A00; background: #FFF7E5; }
.badge-optional { color: #555; background: #F0F0F0; }

.req {
    border: 1px solid var(--line);
    border-radius: 13px;
    background: #FFFFFF;
    padding: 16px 18px;
    margin: 0 0 11px;
    box-shadow: 0 2px 8px rgba(17,17,17,.025);
}
.req:hover { box-shadow: 0 5px 18px rgba(17,17,17,.06); }
.req-top {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 16px;
}
.req-title {
    color: var(--black);
    font-size: 14px;
    font-weight: 750;
    line-height: 1.45;
}
.req-meta {
    color: #8A8A8A;
    font-size: 11px;
    margin-top: 5px;
}
.req-detail {
    color: #555;
    font-size: 12px;
    line-height: 1.55;
    margin-top: 10px;
}
.req-detail b { color: #222; }

.risk {
    border: 1px solid var(--line);
    border-left: 4px solid #111;
    border-radius: 12px;
    padding: 15px 17px;
    margin-bottom: 10px;
    background: #FFFFFF;
}
.risk.high { border-left-color: var(--red); }
.risk.medium { border-left-color: #D89B24; }
.risk.low { border-left-color: var(--green); }
.risk-title { font-size: 14px; font-weight: 750; color: var(--black); }
.risk-text { font-size: 12px; color: #5F5F5F; line-height: 1.55; margin-top: 5px; }

.check-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 16px;
    padding: 14px 16px;
    border: 1px solid var(--line);
    border-radius: 12px;
    margin-bottom: 9px;
    background: #FFFFFF;
}
.check-name { font-size: 13px; font-weight: 700; color: var(--black); }
.check-action { font-size: 11px; color: #777; margin-top: 4px; }
.check-done { color: #126A34; background: #EAF7EF; }
.check-pending { color: #B42318; background: #FFF0EF; }

.empty {
    border: 1px dashed #D8D8D8;
    border-radius: 12px;
    padding: 22px;
    color: #888;
    font-size: 13px;
    text-align: center;
    background: #FAFAFA;
}

.footer-line {
    margin-top: 48px;
    padding-top: 18px;
    border-top: 1px solid var(--line);
    color: #999;
    font-size: 11px;
    text-align: center;
}
</style>
""",
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------
def esc(value):
    return html.escape(str(value if value is not None else ""))


def render_process(current, progress, detail=""):
    steps = [
        "Upload & extract",
        "Analyze & match",
        "Decision & report",
    ]

    rows = []
    for i, label in enumerate(steps, 1):
        if i < current:
            state, state_text, mark = "done", "Complete", "✓"
        elif i == current:
            state, state_text, mark = "active", "Processing", str(i)
        else:
            state, state_text, mark = "", "Waiting", str(i)

        rows.append(
            f"""
<div class="step {state}">
    <div class="step-dot">{mark}</div>
    <div class="step-name">{esc(label)}</div>
    <div class="step-state">{state_text}</div>
</div>
"""
        )

    progress_class = f"progress-{max(0, min(100, int(round(progress / 5) * 5)))}"

    return f"""
<div class="process-shell">
    <div class="process-top">
        <div class="process-title">{esc(detail or "Processing documents")}</div>
        <div class="process-percent">{progress}%</div>
    </div>
    <div class="progress-track">
        <div class="progress-fill {progress_class}"></div>
    </div>
    {''.join(rows)}
</div>
"""
def status_badge(status):
    cls = {
        "Matched": "badge-matched",
        "Missing": "badge-missing",
        "Unclear": "badge-unclear",
    }.get(status, "badge-unclear")
    return f'<span class="badge {cls}">{esc(status)}</span>'


def priority_badge(priority):
    cls = {
        "Mandatory": "badge-mandatory",
        "Important": "badge-important",
        "Optional": "badge-optional",
    }.get(priority, "badge-optional")
    return f'<span class="badge {cls}">{esc(priority)}</span>'


def render_requirement(r):
    return f"""
    <div class="req">
        <div class="req-top">
            <div>
                <div class="req-title">{esc(r.get("requirement", "Requirement"))}</div>
                <div class="req-meta">
                    {esc(r.get("category", "Other"))} &nbsp;·&nbsp; {priority_badge(r.get("priority", "Unclear"))}
                </div>
            </div>
            {status_badge(r.get("status", "Unclear"))}
        </div>
        <div class="req-detail">
            <b>Company evidence:</b> {esc(r.get("company_evidence", "None found"))}<br>
            <b>Assessment:</b> {esc(r.get("reason", "No explanation available."))}
        </div>
    </div>
    """


def render_risk(item, level):
    return f"""
    <div class="risk {level}">
        <div class="risk-title">{esc(item.get("risk", "Risk"))}</div>
        <div class="risk-text"><b>Impact:</b> {esc(item.get("impact", "Not specified"))}</div>
        <div class="risk-text"><b>Reason:</b> {esc(item.get("reason", "Not specified"))}</div>
    </div>
    """


def render_check_item(item):
    checked = item.get("status") == "checked"
    cls = "check-done" if checked else "check-pending"
    label = "Ready" if checked else "Action needed"
    return f"""
    <div class="check-item">
        <div>
            <div class="check-name">{esc(item.get("item", "Checklist item"))}</div>
            <div class="check-action">{esc(item.get("action", ""))}</div>
        </div>
        <span class="badge {cls}">{label}</span>
    </div>
    """


# ---------------------------------------------------------------------
# Header + intro
# ---------------------------------------------------------------------
st.markdown(
    f"""
    <div class="app-header">
        <div class="brand">
            <div class="brand-name">Tender<span>Wise</span> AI</div>
            <img class="brand-mark" src="data:image/png;base64,{__import__('base64').b64encode((ASSETS / 'logo_icon.png').read_bytes()).decode()}">
        </div>
        <div class="header-note">Bid readiness workspace</div>
    </div>

    <div class="hero">
        <div class="hero-kicker">Tender intelligence</div>
        <h1>Turn tender documents into a clear bid decision.</h1>
        <p>
            Upload the tender and your company profile. TenderWise extracts the requirements,
            compares them with your capabilities, evaluates risks, and produces a structured
            bid recommendation with supporting evidence.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------
# Upload
# ---------------------------------------------------------------------
st.markdown(
    '<div class="section-head"><div class="section-title">Upload documents</div>'
    '<div class="section-caption">PDF files only</div></div>',
    unsafe_allow_html=True,
)

left, right = st.columns(2, gap="large")

with left:
    st.markdown(
        '<div class="upload-heading">Tender document</div>'
        '<div class="upload-sub">The tender, RFP, RFQ, or procurement document you want to evaluate.</div>',
        unsafe_allow_html=True,
    )
    tender_file = st.file_uploader(
        "Tender PDF",
        type=["pdf"],
        key="tender_pdf",
        label_visibility="collapsed",
    )
    if tender_file:
        st.markdown(
            f'<div class="file-card"><strong>{esc(tender_file.name)}</strong> '
            f'&nbsp;·&nbsp; {round(tender_file.size / 1024, 1)} KB</div>',
            unsafe_allow_html=True,
        )

with right:
    st.markdown(
        '<div class="upload-heading">Company profile</div>'
        '<div class="upload-sub">Your company profile, capabilities, experience, and supporting information.</div>',
        unsafe_allow_html=True,
    )
    company_file = st.file_uploader(
        "Company Profile PDF",
        type=["pdf"],
        key="company_pdf",
        label_visibility="collapsed",
    )
    if company_file:
        st.markdown(
            f'<div class="file-card"><strong>{esc(company_file.name)}</strong> '
            f'&nbsp;·&nbsp; {round(company_file.size / 1024, 1)} KB</div>',
            unsafe_allow_html=True,
        )

st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

if tender_file and company_file:
    if st.button("Analyze documents", use_container_width=True, type="primary"):
        process_box = st.empty()
        progress = st.progress(0)

        try:
            process_box.markdown(
                render_process(1, 10, "Reading and extracting both PDF files"),
                unsafe_allow_html=True,
            )
            progress.progress(10)

            tender_data = process_document(tender_file, tender_file.name)
            company_data = process_document(company_file, company_file.name)

            process_box.markdown(
                render_process(1, 25, "Documents extracted successfully"),
                unsafe_allow_html=True,
            )
            progress.progress(25)

            analysis_result = analyze_documents(tender_data, company_data)

            process_box.markdown(
                render_process(2, 45, "Analyzing and matching requirements"),
                unsafe_allow_html=True,
            )
            progress.progress(45)

            def pipeline_update(stage):
                mapping = {
                    "matching": (2, 50, "Matching tender requirements"),
                    "compliance": (2, 62, "Calculating compliance"),
                    "risks": (3, 72, "Assessing bid risks"),
                    "decision": (3, 82, "Making the bid decision"),
                    "report": (3, 92, "Generating the analysis report"),
                    "checklist": (3, 97, "Building the submission checklist"),
                }
                if stage in mapping:
                    step, pct, text = mapping[stage]
                    progress.progress(pct)
                    process_box.markdown(
                        render_process(step, pct, text),
                        unsafe_allow_html=True,
                    )

            adapted_input = adapt_analysis_output(analysis_result)
            final_result = run_full_analysis(
                adapted_input,
                progress_callback=pipeline_update
            )

            progress.progress(100)
            process_box.markdown(
                render_process(3, 100, "Analysis complete"),
                unsafe_allow_html=True,
            )

            st.session_state["analysis_bundle"] = {
                "analysis_result": analysis_result,
                "final_result": final_result,
            }
        except Exception as e:
            process_box.empty()
            progress.empty()
            st.error(f"Analysis could not be completed: {e}")

bundle = st.session_state.get("analysis_bundle")

# ---------------------------------------------------------------------
# Results
# ---------------------------------------------------------------------
if bundle:
    analysis_result = bundle["analysis_result"]
    final_result = bundle["final_result"]
    compliance = final_result.get("compliance", {})
    decision = final_result.get("decision", {})
    risks = final_result.get("risks", {})
    matched_results = final_result.get("matched_results", [])
    checklist = final_result.get("checklist", [])
    report = final_result.get("report", {})

    st.markdown(
        '<div class="section"><div class="section-head">'
        '<div class="section-title">Bid readiness result</div>'
        '<div class="section-caption">Generated from the uploaded documents</div>'
        '</div></div>',
        unsafe_allow_html=True,
    )

    decision_name = decision.get("decision", "UNAVAILABLE")
    decision_class = {
        "BID": "#15803D",
        "CONDITIONAL BID": "#B7791F",
        "NO-BID": "#C21F1F",
    }.get(decision_name, "#222222")

    st.markdown(
        f"""
        <div class="decision">
            <div class="decision-label">Recommendation</div>
            <div class="decision-value" style="color:{decision_class};">{esc(decision_name)}</div>
            <div class="decision-reason">{esc(decision.get("reason", "No recommendation reason available."))}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section"><div class="section-head">'
        '<div class="section-title">Compliance overview</div>'
        '<div class="section-caption">Requirement matching summary</div>'
        '</div></div>',
        unsafe_allow_html=True,
    )
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Compliance", f"{compliance.get('compliance_percentage', 0)}%")
    m2.metric("Matched", compliance.get("matched", 0))
    m3.metric("Missing", compliance.get("missing", 0))
    m4.metric("Unclear", compliance.get("unclear", 0))

    # Requirement matching
    st.markdown(
        '<div class="section"><div class="section-head">'
        '<div class="section-title">Requirement matching</div>'
        '<div class="section-caption">Evidence-backed comparison</div>'
        '</div></div>',
        unsafe_allow_html=True,
    )

    if matched_results:
        req_tabs = st.tabs(["All", "Matched", "Missing", "Unclear"])
        filters = [None, "Matched", "Missing", "Unclear"]
        for tab, wanted in zip(req_tabs, filters):
            with tab:
                items = [
                    r for r in matched_results
                    if wanted is None or r.get("status") == wanted
                ]
                if not items:
                    st.markdown('<div class="empty">No requirements in this category.</div>', unsafe_allow_html=True)
                else:
                    for r in items:
                        st.markdown(render_requirement(r), unsafe_allow_html=True)
    else:
        st.markdown('<div class="empty">No requirement matching results were generated.</div>', unsafe_allow_html=True)

    # Risks
    st.markdown(
        '<div class="section"><div class="section-head">'
        '<div class="section-title">Risk analysis</div>'
        '<div class="section-caption">Issues that may affect the bid decision</div>'
        '</div></div>',
        unsafe_allow_html=True,
    )
    risk_tabs = st.tabs(["High", "Medium", "Low"])
    for tab, key, level in zip(
        risk_tabs,
        ["high_risks", "medium_risks", "low_risks"],
        ["high", "medium", "low"],
    ):
        with tab:
            items = risks.get(key, [])
            if not items:
                st.markdown('<div class="empty">No risks identified at this level.</div>', unsafe_allow_html=True)
            else:
                for item in items:
                    st.markdown(render_risk(item, level), unsafe_allow_html=True)

    # Report
    st.markdown(
        '<div class="section"><div class="section-head">'
        '<div class="section-title">Analysis report</div>'
        '<div class="section-caption">Structured AI-generated findings</div>'
        '</div></div>',
        unsafe_allow_html=True,
    )
    report_sections = [
        ("Executive Summary", "executive_summary"),
        ("Tender Overview", "tender_overview"),
        ("Company Overview", "company_overview"),
        ("Compliance Summary", "compliance_summary"),
        ("Matched Requirements", "matched_requirements"),
        ("Missing Requirements", "missing_requirements"),
        ("Unclear Requirements", "unclear_requirements"),
        ("Risk Analysis", "risk_analysis"),
        ("Bid Recommendation", "bid_recommendation"),
        ("Key Reasons", "key_reasons"),
        ("Recommended Actions", "recommended_actions"),
    ]
    for title, key in report_sections:
        value = report.get(key)
        if value:
            with st.expander(title):
                st.write(value)
        else:
            with st.expander(title):
                st.caption("No content was generated for this section.")

    # Checklist + download
    st.markdown(
        '<div class="section"><div class="section-head">'
        '<div class="section-title">Submission checklist</div>'
        '<div class="section-caption">Documents and actions requiring attention</div>'
        '</div></div>',
        unsafe_allow_html=True,
    )
    if checklist:
        for item in checklist:
            st.markdown(render_check_item(item), unsafe_allow_html=True)
    else:
        st.markdown('<div class="empty">No checklist items were generated.</div>', unsafe_allow_html=True)

    full_output = {
        "tender_analysis": analysis_result.get("tender_analysis"),
        "company_analysis": analysis_result.get("company_analysis"),
        "bid_readiness_analysis": final_result,
    }
    final_json = json.dumps(full_output, indent=2, ensure_ascii=False)

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    st.download_button(
        "Download full result",
        data=final_json,
        file_name="tenderwise_full_analysis.json",
        mime="application/json",
        use_container_width=True,
    )

    st.markdown(
        '<div class="footer-line">TenderWise AI · Analyze · Match · Decide</div>',
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        '<div class="footer-line">Upload both PDFs to start the bid-readiness analysis.</div>',
        unsafe_allow_html=True,
    )
