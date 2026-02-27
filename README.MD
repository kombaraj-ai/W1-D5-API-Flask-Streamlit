# Week 1 -> Day 5 -> API, REST, Flask & Streamlit 

---
## Table of Contents

*   [What is an API - Application Programming Interface](#what-is-an-api-application-programming-interface)
    *   [REST API vs SOAP vs GraphQL](#rest-api-vs-soap-vs-graphql)
    *   [REST API Deep Dive](#rest-api-deep-dive)
        *   [HTTP Methods](#http-methods)
        *   [HTTP Status Codes](#http-status-codes)
*   [Python Flask](#python-flask)
*   [Streamlit Framework](#streamlit-framework)
    *   [Streamlit Modules](#streamlit-modules)
*   [Assignment - Student Management System](Assignment.md)


## What is an API (Application Programming Interface)?

An **API** is a set of rules and protocols that allows one software application to communicate with another. Think of it as a **waiter in a restaurant** — you (the client) don't go into the kitchen (the server) yourself; instead, you give your order to the waiter (API), who fetches what you need and brings it back.

APIs define:
- **What requests** can be made
- **How** to make them (format, method)
- **What responses** to expect

APIs are used everywhere — from fetching weather data, processing payments, logging into apps with Google, to powering mobile applications.

---

## REST API vs SOAP vs GraphQL

| Feature | REST API | SOAP | GraphQL |
|---|---|---|---|
| **Full Form** | Representational State Transfer | Simple Object Access Protocol | Graph Query Language |
| **Data Format** | JSON, XML | XML only | JSON |
| **Protocol** | HTTP | HTTP, SMTP, TCP | HTTP |
| **Flexibility** | Moderate | Rigid / Strict | Highly flexible |
| **Learning Curve** | Easy | Steep | Moderate |
| **Performance** | Fast | Slower (XML overhead) | Efficient |
| **Best For** | Web & mobile apps | Enterprise, banking, legacy | Complex queries, microservices |
| **Error Handling** | HTTP status codes | Built-in fault element | Custom error object |
| **Security** | HTTPS, OAuth | WS-Security (built-in) | HTTPS, OAuth |
| **Caching** | Supported natively | Not straightforward | Requires custom setup |

---

## REST API Deep Dive

### What is REST?

REST (Representational State Transfer) is an **architectural style** for designing networked applications. It uses standard HTTP methods to perform CRUD (Create, Read, Update, Delete) operations on resources identified by URLs.

### REST Principles
- **Stateless** — Each request contains all information needed; server stores no client state.
- **Client-Server** — UI and backend are separated.
- **Uniform Interface** — Consistent way to interact with resources.
- **Resource-Based** — Everything is a resource (user, product, order) accessed via a URL.
- **Cacheable** — Responses can be cached for performance.

---

### HTTP Methods

| Method | Purpose | Example URL | Description |
|---|---|---|---|
| **GET** | Read | `GET /users` | Retrieve a list of users |
| **GET** | Read | `GET /users/1` | Retrieve a specific user |
| **POST** | Create | `POST /users` | Create a new user |
| **PUT** | Update (full) | `PUT /users/1` | Replace all data of user 1 |
| **PATCH** | Update (partial) | `PATCH /users/1` | Update specific fields of user 1 |
| **DELETE** | Delete | `DELETE /users/1` | Delete user 1 |

---

### HTTP Status Codes

Status codes are 3-digit numbers returned by the server to indicate the result of the request.

#### 1xx — Informational
| Code | Name | Meaning |
|---|---|---|
| 100 | Continue | Request received, continue sending |

#### 2xx — Success
| Code | Name | Meaning |
|---|---|---|
| 200 | OK | Request succeeded |
| 201 | Created | Resource created successfully |
| 204 | No Content | Success but no body returned (e.g., DELETE) |

#### 3xx — Redirection
| Code | Name | Meaning |
|---|---|---|
| 301 | Moved Permanently | Resource moved to a new URL |
| 304 | Not Modified | Cached version is still valid |

#### 4xx — Client Errors
| Code | Name | Meaning |
|---|---|---|
| 400 | Bad Request | Invalid request syntax |
| 401 | Unauthorized | Authentication required |
| 403 | Forbidden | No permission to access |
| 404 | Not Found | Resource doesn't exist |
| 405 | Method Not Allowed | HTTP method not supported |
| 422 | Unprocessable Entity | Validation error |
| 429 | Too Many Requests | Rate limit exceeded |

#### 5xx — Server Errors
| Code | Name | Meaning |
|---|---|---|
| 500 | Internal Server Error | Generic server failure |
| 502 | Bad Gateway | Invalid response from upstream server |
| 503 | Service Unavailable | Server is down or overloaded |
| 504 | Gateway Timeout | Upstream server timed out |

---

## Python Flask

### What is Flask?

**Flask** is a lightweight, micro web framework for Python. It's designed to be simple and easy to use, making it ideal for building REST APIs and web applications quickly.

**Key Features:**
- Minimal and unopinionated (you choose how to structure things)
- Built-in development server and debugger
- Supports extensions for databases, authentication, etc.
- Widely used for building REST APIs

### Installation

```bash
pip install flask
```

### Hello World Flask Application

```python
# app.py
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)
```

**Run the app:**
```bash
python app.py
```
Open `http://127.0.0.1:5000/` in your browser.

### Simple REST API with Flask

```python
from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample data
users = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"}
]

# GET all users
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)

# GET single user
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((u for u in users if u['id'] == user_id), None)
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404

# POST create user
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = {"id": len(users) + 1, "name": data['name']}
    users.append(new_user)
    return jsonify(new_user), 201

if __name__ == '__main__':
    app.run(debug=True)
```

---

## Streamlit Framework

### What is Streamlit?

**Streamlit** is an open-source Python framework that lets you build **interactive web apps and dashboards** for data science and machine learning — all in pure Python, with no HTML, CSS, or JavaScript needed.

**Why Streamlit?**
- Build data apps in minutes
- Auto-refreshes when you save the script
- Perfect for ML demos, data dashboards, and prototypes
- Large component ecosystem

### Installation

```bash
pip install streamlit
```

**Verify installation:**
```bash
streamlit --version
```

**Run a Streamlit app:**
```bash
streamlit run app.py
```

This opens your app in the browser at `http://localhost:8501`.

---

## Streamlit Modules

### 6.1 Text & Rich Content

Used to display headings, paragraphs, markdown, code, and formatted text.

```python
import streamlit as st

st.title("My App Title")
st.header("This is a Header")
st.subheader("This is a Subheader")
st.text("Plain text display")
st.markdown("**Bold**, *Italic*, and `code` using Markdown")
st.code("print('Hello, World!')", language='python')
st.latex(r"E = mc^2")
st.caption("This is a caption (small text)")
st.divider()  # Horizontal rule
```

---

### 6.2 Input Widgets

Used to collect user inputs interactively.

```python
import streamlit as st

# Text input
name = st.text_input("Enter your name", placeholder="John Doe")

# Number input
age = st.number_input("Enter your age", min_value=1, max_value=120, value=25)

# Slider
score = st.slider("Select a score", 0, 100, 50)

# Checkbox
agree = st.checkbox("I agree to terms")

# Radio button
color = st.radio("Choose a color", ["Red", "Green", "Blue"])

# Select box (dropdown)
city = st.selectbox("Select your city", ["Chennai", "Mumbai", "Delhi"])

# Multi-select
languages = st.multiselect("Select languages", ["Python", "Java", "C++", "JavaScript"])

# Button
if st.button("Submit"):
    st.success(f"Hello {name}! Age: {age}")

# Date input
from datetime import date
dob = st.date_input("Your date of birth", date(1990, 1, 1))

# Text area
feedback = st.text_area("Leave your feedback")
```

---

### 6.3 Charts & Graphs

Streamlit supports built-in charts and integrates with popular libraries.

```python
import streamlit as st
import pandas as pd
import numpy as np

# Sample data
df = pd.DataFrame(np.random.randn(20, 3), columns=["A", "B", "C"])

# Line chart
st.subheader("Line Chart")
st.line_chart(df)

# Bar chart
st.subheader("Bar Chart")
st.bar_chart(df)

# Area chart
st.subheader("Area Chart")
st.area_chart(df)

# Scatter chart (using Altair via st.altair_chart or plotly)
import plotly.express as px
fig = px.scatter(df, x="A", y="B", color="C", title="Scatter Plot")
st.plotly_chart(fig)

# Map chart (requires lat/lon columns)
map_data = pd.DataFrame(
    np.random.randn(100, 2) / [50, 50] + [13.08, 80.27],  # Chennai coordinates
    columns=["lat", "lon"]
)
st.map(map_data)
```

---

### 6.4 Media & Files

Used to display images, audio, video, and handle file uploads/downloads.

```python
import streamlit as st

# Display image from URL
st.image("https://picsum.photos/400/200", caption="Sample Image", use_column_width=True)

# Display image from local file
# st.image("local_image.png", caption="Local Image")

# Audio
# st.audio("audio.mp3")

# Video
# st.video("video.mp4")

# File Uploader
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
if uploaded_file is not None:
    import pandas as pd
    df = pd.read_csv(uploaded_file)
    st.dataframe(df)

# File Download Button
st.download_button(
    label="Download Sample Text",
    data="Hello, this is downloadable content!",
    file_name="sample.txt",
    mime="text/plain"
)
```

---

### 6.5 Data Display

Used to display tables, DataFrames, metrics, and JSON data.

```python
import streamlit as st
import pandas as pd
import numpy as np

df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [25, 30, 35],
    "Score": [88.5, 92.0, 76.3]
})

# Interactive DataFrame (sortable, filterable)
st.subheader("Interactive DataFrame")
st.dataframe(df, use_container_width=True)

# Static table
st.subheader("Static Table")
st.table(df)

# Metric display
st.subheader("Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Temperature", "38°C", "+2°C")
col2.metric("Humidity", "65%", "-5%")
col3.metric("Wind Speed", "15 km/h", "+3 km/h")

# JSON display
st.subheader("JSON Data")
st.json({"name": "Alice", "age": 25, "city": "Chennai"})
```

---

### 6.6 Layout & Containers

Used to organize app content using columns, sidebars, tabs, expanders, and containers.

```python
import streamlit as st

# ----- Sidebar -----
with st.sidebar:
    st.header("Sidebar Menu")
    page = st.selectbox("Navigate to", ["Home", "About", "Contact"])
    theme = st.radio("Theme", ["Light", "Dark"])

# ----- Columns -----
st.subheader("Columns Layout")
col1, col2, col3 = st.columns(3)
with col1:
    st.info("Column 1 content")
with col2:
    st.success("Column 2 content")
with col3:
    st.warning("Column 3 content")

# ----- Tabs -----
st.subheader("Tabs Layout")
tab1, tab2, tab3 = st.tabs(["Overview", "Details", "Settings"])
with tab1:
    st.write("Welcome to the Overview tab!")
with tab2:
    st.write("Detailed information goes here.")
with tab3:
    st.write("Configure your settings here.")

# ----- Expander -----
with st.expander("Click to expand for more info"):
    st.write("This content is hidden until the user clicks to expand.")
    st.image("https://picsum.photos/300/150")

# ----- Container -----
with st.container():
    st.write("This is inside a container")
    st.bar_chart([1, 4, 2, 7, 3])

# ----- Empty placeholder -----
placeholder = st.empty()
placeholder.text("Loading...")
import time
time.sleep(1)
placeholder.success("Loaded!")
```

---

## 7. Hello World Streamlit Application

The simplest possible Streamlit app:

```python
# hello_streamlit.py
import streamlit as st

st.title("Hello, World! 👋")
st.write("Welcome to my first Streamlit app!")

name = st.text_input("What's your name?")
if name:
    st.success(f"Hello, {name}! Great to meet you! 🎉")
```

**Run it:**
```bash
streamlit run hello_streamlit.py
```

Your app opens automatically at `http://localhost:8501`.

---

## Quick Reference Summary

| Topic | Key Takeaway |
|---|---|
| **API** | Interface for software-to-software communication |
| **REST** | HTTP-based, uses JSON, most popular for web APIs |
| **SOAP** | XML-based, strict, used in enterprise/banking |
| **GraphQL** | Query exactly what you need, flexible |
| **Flask** | Lightweight Python web framework for APIs |
| **Streamlit** | Build data apps in Python with no HTML/CSS |
| **HTTP Methods** | GET, POST, PUT, PATCH, DELETE |
| **Status Codes** | 2xx=Success, 4xx=Client Error, 5xx=Server Error |
