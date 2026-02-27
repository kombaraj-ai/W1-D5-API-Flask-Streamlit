"""
Streamlit Frontend — Student REST API Tester
Make sure flask_api.py is running on port 5000 before using this app.
"""

import streamlit as st
import requests
import json
import pandas as pd
from datetime import datetime

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Student API Tester",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Sora:wght@300;400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Sora', sans-serif;
}

/* App background */
.stApp {
    background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    color: #e8e8f0;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: rgba(15, 12, 41, 0.95) !important;
    border-right: 1px solid rgba(139, 92, 246, 0.3);
}

/* Cards */
.api-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(139,92,246,0.25);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    backdrop-filter: blur(10px);
}

/* Method badges */
.badge-get    { background:#10b981; color:#fff; padding:4px 12px; border-radius:20px; font-family:'JetBrains Mono',monospace; font-size:0.75rem; font-weight:700; }
.badge-post   { background:#3b82f6; color:#fff; padding:4px 12px; border-radius:20px; font-family:'JetBrains Mono',monospace; font-size:0.75rem; font-weight:700; }
.badge-put    { background:#f59e0b; color:#fff; padding:4px 12px; border-radius:20px; font-family:'JetBrains Mono',monospace; font-size:0.75rem; font-weight:700; }
.badge-delete { background:#ef4444; color:#fff; padding:4px 12px; border-radius:20px; font-family:'JetBrains Mono',monospace; font-size:0.75rem; font-weight:700; }

/* Response panel */
.response-box {
    background: #0d0d1a;
    border: 1px solid rgba(139,92,246,0.4);
    border-radius: 12px;
    padding: 1.2rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
    color: #a78bfa;
    white-space: pre-wrap;
    word-break: break-all;
}

.status-2xx { color: #10b981; font-weight: 700; }
.status-4xx { color: #ef4444; font-weight: 700; }
.status-5xx { color: #f59e0b; font-weight: 700; }

/* Guide boxes */
.guide-step {
    background: rgba(139,92,246,0.1);
    border-left: 4px solid #8b5cf6;
    padding: 0.8rem 1rem;
    border-radius: 0 8px 8px 0;
    margin-bottom: 0.6rem;
    font-size: 0.9rem;
}

/* Input labels */
label { color: #c4b5fd !important; font-size: 0.85rem !important; }

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #4f46e5) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Sora', sans-serif !important;
    font-weight: 600 !important;
    padding: 0.5rem 1.5rem !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 15px rgba(124,58,237,0.4) !important;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    border: 1px solid rgba(139,92,246,0.3);
    border-radius: 10px;
}

/* Title */
h1 { 
    font-family: 'Sora', sans-serif !important; 
    color: #c4b5fd !important;
    font-weight: 700 !important;
}
h2, h3 { color: #a78bfa !important; }
</style>
""", unsafe_allow_html=True)

# ── Config ────────────────────────────────────────────────────────────────────
BASE_URL = "http://127.0.0.1:5000"

# ── Helpers ───────────────────────────────────────────────────────────────────

def make_request(method, endpoint, payload=None):
    url = BASE_URL + endpoint
    ts  = datetime.now().strftime("%H:%M:%S")
    try:
        if method == "GET":
            r = requests.get(url, timeout=5)
        elif method == "POST":
            r = requests.post(url, json=payload, timeout=5)
        elif method == "PUT":
            r = requests.put(url, json=payload, timeout=5)
        elif method == "DELETE":
            r = requests.delete(url, timeout=5)
        return r.status_code, r.json(), url, ts
    except requests.exceptions.ConnectionError:
        return 0, {"error": "❌ Cannot connect to Flask API. Is flask_api.py running on port 5000?"}, url, ts
    except Exception as e:
        return 0, {"error": str(e)}, url, ts


def status_color(code):
    if 200 <= code < 300: return "status-2xx"
    if 400 <= code < 500: return "status-4xx"
    return "status-5xx"


def render_response(status_code, data, url, ts):
    color_cls = status_color(status_code)
    status_label = f"HTTP {status_code}" if status_code else "Connection Error"
    st.markdown(f"""
    <div class="response-box">
<span style="color:#6b7280">── Response ──────────────────────────────────────</span>
<span style="color:#64748b">🕐 {ts}   🔗 {url}</span>
<span class="{color_cls}">Status: {status_label}</span>

{json.dumps(data, indent=2)}
    </div>
    """, unsafe_allow_html=True)


# ── Sidebar — Guide ───────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎓 Student API Tester")
    st.markdown("---")

    st.markdown("### 📖 Quick Start Guide")

    st.markdown("""
    <div class="guide-step">
    <strong>Step 1 — Start Flask API</strong><br>
    Open a terminal and run:<br>
    <code>python flask_api.py</code>
    </div>

    <div class="guide-step">
    <strong>Step 2 — Launch this app</strong><br>
    In another terminal run:<br>
    <code>streamlit run streamlit_app.py</code>
    </div>

    <div class="guide-step">
    <strong>Step 3 — Pick an operation</strong><br>
    Use the tabs in the main panel to test GET, POST, PUT, DELETE.
    </div>

    <div class="guide-step">
    <strong>Step 4 — Read the response</strong><br>
    HTTP Status + JSON body appear below each action button.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🔑 Status Codes")
    st.markdown("""
    - 🟢 **200** OK  
    - 🟢 **201** Created  
    - 🔴 **404** Not Found  
    - 🔴 **409** Already Exists  
    - 🔴 **400** Bad Request  
    """)

    st.markdown("---")
    st.markdown("### 🌐 API Endpoints")
    st.code("""GET    /students
GET    /students/<id>
POST   /students
PUT    /students/<id>
DELETE /students/<id>
GET    /health""", language="text")

    # Health check in sidebar
    st.markdown("---")
    if st.button("🔍 Check API Health"):
        code, data, url, ts = make_request("GET", "/health")
        if code == 200:
            st.success("✅ Flask API is online!")
        else:
            st.error("❌ Flask API is offline")


# ── Main Header ───────────────────────────────────────────────────────────────
st.markdown("# 🎓 Student Management System")
st.markdown("*A hands-on tool to explore GET, POST, PUT and DELETE operations*")
st.markdown("---")

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab_get, tab_post, tab_put, tab_delete, tab_guide = st.tabs([
    "🟢  GET", "🔵  POST", "🟡  PUT", "🔴  DELETE", "📘  How to Use"
])

# ════════════════════════════════════════════════════════════════════════════════
# GET TAB
# ════════════════════════════════════════════════════════════════════════════════
with tab_get:
    st.markdown('<div class="api-card">', unsafe_allow_html=True)
    st.markdown('<span class="badge-get">GET</span> &nbsp; Retrieve student records', unsafe_allow_html=True)
    st.markdown("")

    mode = st.radio("Fetch", ["All Students", "Single Student by ID"], horizontal=True)

    if mode == "All Students":
        st.markdown("**Endpoint:** `GET /students`")
        if st.button("▶ Fetch All Students"):
            code, data, url, ts = make_request("GET", "/students")
            render_response(code, data, url, ts)

            if code == 200 and "data" in data:
                st.markdown("#### 📊 Table View")
                df = pd.DataFrame(data["data"])
                st.dataframe(df, use_container_width=True, hide_index=True)

    else:
        st.markdown("**Endpoint:** `GET /students/{student_id}`")
        sid = st.text_input("Student ID", placeholder="e.g. STU001")
        if st.button("▶ Fetch Student"):
            if sid.strip():
                code, data, url, ts = make_request("GET", f"/students/{sid.strip()}")
                render_response(code, data, url, ts)
            else:
                st.warning("Please enter a Student ID.")
    st.markdown("</div>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════
# POST TAB
# ════════════════════════════════════════════════════════════════════════════════
with tab_post:
    st.markdown('<div class="api-card">', unsafe_allow_html=True)
    st.markdown('<span class="badge-post">POST</span> &nbsp; Create a new student', unsafe_allow_html=True)
    st.markdown("**Endpoint:** `POST /students`")
    st.markdown("")

    col1, col2 = st.columns(2)
    with col1:
        new_id   = st.text_input("Student ID *", placeholder="e.g. STU011")
        new_name = st.text_input("Student Name *", placeholder="e.g. Rahul Verma")
    with col2:
        new_exp  = st.number_input("Years of Experience *", min_value=0, max_value=50, value=0)
        new_comp = st.text_input("Company Name *", placeholder="e.g. Google India")

    # Live JSON preview
    payload = {
        "student_id":          new_id,
        "student_name":        new_name,
        "years_of_experience": new_exp,
        "company_name":        new_comp,
    }
    with st.expander("📋 Request Body Preview (JSON)"):
        st.code(json.dumps(payload, indent=2), language="json")

    if st.button("▶ Create Student"):
        if all([new_id.strip(), new_name.strip(), new_comp.strip()]):
            code, data, url, ts = make_request("POST", "/students", payload)
            render_response(code, data, url, ts)
        else:
            st.warning("Please fill in all required fields (*).")
    st.markdown("</div>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════
# PUT TAB
# ════════════════════════════════════════════════════════════════════════════════
with tab_put:
    st.markdown('<div class="api-card">', unsafe_allow_html=True)
    st.markdown('<span class="badge-put">PUT</span> &nbsp; Update an existing student', unsafe_allow_html=True)
    st.markdown("**Endpoint:** `PUT /students/{student_id}`")
    st.markdown("")

    put_id = st.text_input("Student ID to Update *", placeholder="e.g. STU003")

    # Optionally auto-load current values
    if st.button("🔍 Load Current Data"):
        if put_id.strip():
            code, data, url, ts = make_request("GET", f"/students/{put_id.strip()}")
            if code == 200:
                st.session_state["put_name"] = data["data"]["student_name"]
                st.session_state["put_exp"]  = data["data"]["years_of_experience"]
                st.session_state["put_comp"] = data["data"]["company_name"]
                st.success("✅ Current data loaded into fields below.")
            else:
                st.error(f"Student '{put_id}' not found.")
        else:
            st.warning("Enter a Student ID first.")

    col1, col2 = st.columns(2)
    with col1:
        put_name = st.text_input("New Student Name", value=st.session_state.get("put_name", ""), placeholder="Updated name")
        put_exp  = st.number_input("New Years of Experience", min_value=0, max_value=50, value=st.session_state.get("put_exp", 0))
    with col2:
        put_comp = st.text_input("New Company Name", value=st.session_state.get("put_comp", ""), placeholder="Updated company")

    put_payload = {
        "student_name":        put_name,
        "years_of_experience": put_exp,
        "company_name":        put_comp,
    }
    with st.expander("📋 Request Body Preview (JSON)"):
        st.code(json.dumps(put_payload, indent=2), language="json")

    if st.button("▶ Update Student"):
        if put_id.strip():
            code, data, url, ts = make_request("PUT", f"/students/{put_id.strip()}", put_payload)
            render_response(code, data, url, ts)
        else:
            st.warning("Please enter the Student ID to update.")
    st.markdown("</div>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════
# DELETE TAB
# ════════════════════════════════════════════════════════════════════════════════
with tab_delete:
    st.markdown('<div class="api-card">', unsafe_allow_html=True)
    st.markdown('<span class="badge-delete">DELETE</span> &nbsp; Remove a student record', unsafe_allow_html=True)
    st.markdown("**Endpoint:** `DELETE /students/{student_id}`")
    st.markdown("")

    del_id = st.text_input("Student ID to Delete *", placeholder="e.g. STU005")

    # Preview the student before deleting
    if st.button("🔍 Preview Student"):
        if del_id.strip():
            code, data, url, ts = make_request("GET", f"/students/{del_id.strip()}")
            render_response(code, data, url, ts)
        else:
            st.warning("Enter a Student ID first.")

    st.markdown("")
    st.warning("⚠️ Deletion is permanent and cannot be undone.")

    confirm = st.checkbox(f"I confirm I want to delete student **{del_id or '...'}**")

    if st.button("▶ Delete Student", disabled=not confirm):
        if del_id.strip():
            code, data, url, ts = make_request("DELETE", f"/students/{del_id.strip()}")
            render_response(code, data, url, ts)
            if code == 200:
                st.balloons()
        else:
            st.warning("Please enter a Student ID to delete.")
    st.markdown("</div>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════
# HOW TO USE TAB
# ════════════════════════════════════════════════════════════════════════════════
with tab_guide:
    st.markdown("## 📘 How to Use This Application")
    st.markdown("*A step-by-step guide for new users*")
    st.markdown("---")

    col_a, col_b = st.columns([1, 1])

    with col_a:
        st.markdown("### 🚀 Getting Started")
        st.markdown("""
**1. Prerequisites**  
Make sure you have Python installed with these packages:
```bash
pip install flask streamlit requests
```

**2. Project Structure**
```
project/
├── flask_api.py       ← Flask REST API server
├── streamlit_app.py   ← This Streamlit UI
└── students.json      ← Student data (auto-managed)
```

**3. Start the Flask API**  
Open **Terminal 1** and run:
```bash
python flask_api.py
```
You should see:
```
 * Running on http://127.0.0.1:5000
```

**4. Start the Streamlit App**  
Open **Terminal 2** and run:
```bash
streamlit run streamlit_app.py
```
Your browser will open at `http://localhost:8501`

**5. Verify Connection**  
Click **"Check API Health"** in the sidebar.  
You should see ✅ Flask API is online!
        """)

    with col_b:
        st.markdown("### 🧪 Testing Each Operation")

        st.markdown("""
**🟢 GET — Read Data**  
- *All students*: Click the `🟢 GET` tab → select "All Students" → click **Fetch All Students**  
- *Single student*: Select "Single Student by ID" → type `STU001` → click **Fetch Student**

---

**🔵 POST — Create a Student**  
- Go to `🔵 POST` tab  
- Fill in: Student ID (`STU011`), Name, Experience, Company  
- Preview the JSON body by expanding **Request Body Preview**  
- Click **Create Student**  
- ✅ Expect `HTTP 201 Created`  
- ❌ Using an existing ID gives `HTTP 409 Conflict`

---

**🟡 PUT — Update a Student**  
- Go to `🟡 PUT` tab  
- Enter the Student ID (e.g. `STU003`)  
- Click **Load Current Data** to auto-fill existing values  
- Modify any field and click **Update Student**  
- ✅ Expect `HTTP 200 OK`

---

**🔴 DELETE — Remove a Student**  
- Go to `🔴 DELETE` tab  
- Enter the Student ID (e.g. `STU010`)  
- Click **Preview Student** to verify before deleting  
- Check the confirmation checkbox  
- Click **Delete Student**  
- ✅ Expect `HTTP 200 OK` + 🎈 balloons animation
        """)

    st.markdown("---")
    st.markdown("### 📊 Understanding the Response Panel")
    st.markdown("""
Every API call shows a **response panel** with:

| Field | Meaning |
|---|---|
| 🕐 Timestamp | When the request was made |
| 🔗 URL | The full endpoint that was called |
| Status | HTTP status code (200, 201, 404, etc.) |
| JSON body | The server's response data |

**Color coding:**  
🟢 Green = 2xx Success &nbsp;&nbsp; 🔴 Red = 4xx Client Error &nbsp;&nbsp; 🟡 Yellow = 5xx Server Error
    """)

    st.markdown("---")
    st.markdown("### 💡 Sample Student IDs to Try")
    sample_data = {
        "Student ID": ["STU001","STU002","STU003","STU004","STU005"],
        "Name": ["Arun Kumar","Priya Sharma","Ravi Chandran","Deepa Nair","Mohammed Farooq"],
        "Experience": ["3 yrs","5 yrs","1 yr","7 yrs","4 yrs"],
        "Company": ["Infosys","TCS","Wipro","HCL Technologies","Cognizant"]
    }
    st.dataframe(pd.DataFrame(sample_data), use_container_width=True, hide_index=True)
