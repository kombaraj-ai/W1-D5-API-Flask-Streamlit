# Assignment - Student Management System

> **Stack:** Python · Flask · Streamlit · JSON

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Technology Stack](#2-technology-stack)
3. [Project Structure](#3-project-structure)
4. [Prerequisites & Installation](#4-prerequisites--installation)
5. [Running the Application](#5-running-the-application)
6. [API Reference](#6-api-reference)
   - 6.1 [Data Model](#61-data-model)
   - 6.2 [Base URL](#62-base-url)
   - 6.3 [GET — Retrieve Students](#63-get--retrieve-students)
   - 6.4 [POST — Create a Student](#64-post--create-a-student)
   - 6.5 [PUT — Update a Student](#65-put--update-a-student)
   - 6.6 [DELETE — Remove a Student](#66-delete--remove-a-student)
   - 6.7 [Health Check](#67-health-check)
7. [HTTP Status Code Reference](#7-http-status-code-reference)
8. [Sample Dataset](#8-sample-dataset)
9. [Streamlit UI — User Guide](#9-streamlit-ui--user-guide)
10. [Response Format](#10-response-format)
11. [Error Handling](#11-error-handling)
12. [Testing with External Tools](#12-testing-with-external-tools)
13. [Troubleshooting](#13-troubleshooting)
14. [Project Limitations & Future Improvements](#14-project-limitations--future-improvements)
15. [Glossary](#15-glossary)

---

## 1. Project Overview

The **Student Management System REST API** is a full-stack learning project designed to demonstrate how REST APIs work in practice. It combines a **Flask** backend that exposes CRUD endpoints with a **Streamlit** frontend that provides an interactive, browser-based interface to test every operation — no Postman or command-line knowledge required.

### Purpose

This project serves as a hands-on teaching tool for:

- Understanding RESTful API principles (resources, HTTP methods, status codes)
- Learning how Flask routes handle different HTTP verbs
- Exploring how a frontend communicates with a backend over HTTP
- Practicing Create, Read, Update, and Delete (CRUD) operations on a real dataset

### What the Application Does

| Capability | Description |
|---|---|
| View all students | Fetch and display all 10 pre-loaded student records in a live table |
| View a single student | Look up any student by their unique ID |
| Add a new student | Submit a form to create a new record that persists to the JSON database |
| Update a student | Edit any field of an existing student; changes are saved immediately |
| Delete a student | Remove a student record permanently after a confirmation step |
| API health check | Verify the Flask server is running with one click |

---

## 2. Technology Stack

| Layer | Technology | Version | Role |
|---|---|---|---|
| **Backend API** | Python Flask | 3.x | REST API server, route handling, JSON I/O |
| **Frontend UI** | Streamlit | Latest | Interactive browser-based API tester |
| **HTTP Client** | Requests | Latest | Streamlit → Flask communication |
| **Database** | JSON File | — | Flat-file persistent storage |
| **Language** | Python | 3.8+ | All application code |

### Why These Technologies?

**Flask** was chosen for its minimalism — it exposes just what is needed to define routes and handle HTTP verbs without hiding the mechanics behind heavy frameworks. This makes it ideal for learning API fundamentals.

**Streamlit** was chosen because it turns pure Python into an interactive web UI without requiring any HTML, CSS, or JavaScript knowledge. It lets learners focus on API behaviour rather than frontend engineering.

**JSON flat-file storage** was chosen deliberately over a database engine to keep the setup dependency-free and to make it easy to inspect, edit, and reset the data at any time.

---

## 3. Project Structure

```
student-api-project/
│
├── flask_api.py          # Flask REST API — all route definitions and logic
├── streamlit_app.py      # Streamlit UI — interactive front-end API tester
├── students.json         # Persistent data store — all student records

```

### File Responsibilities

**`flask_api.py`**  
The API server. Defines five endpoints mapped to HTTP methods (GET, POST, PUT, DELETE). Reads from and writes to `students.json`. Runs on port `5000` by default.

**`streamlit_app.py`**  
The UI client. Communicates with the Flask API over HTTP using the `requests` library. Organized into tabs — one per HTTP method — plus a guide tab and a persistent sidebar.

**`students.json`**  
The data layer. A plain JSON array of student objects. Modified directly by the Flask API on every POST, PUT, and DELETE request. No database engine is required.

---

## 4. Prerequisites & Installation

### Install Dependencies

All three packages can be installed with a single command:

```bash
pip install flask streamlit requests
```

### Optional: Virtual Environment (Recommended)

Using a virtual environment keeps your project dependencies isolated:

```bash
# Create virtual environment
python -m venv venv

# Activate — macOS / Linux
source venv/bin/activate

# Activate — Windows
venv\Scripts\activate

# Install packages inside the virtual environment
pip install flask streamlit requests
```

---

## 5. Running the Application

The application requires **two servers running simultaneously** — the Flask API and the Streamlit UI. Open two separate terminal windows.

### Step 1 — Start the Flask API Server

In **Terminal 1**, navigate to the project folder and run:

```bash
python flask_api.py
```

**Expected output:**

```
 * Serving Flask app 'flask_api'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

> ⚠️ Keep this terminal open. The API must remain running for the Streamlit UI to work.

### Step 2 — Start the Streamlit UI

In **Terminal 2**, from the same project folder, run:

```bash
streamlit run streamlit_app.py
```

**Expected output:**

```
  You can now view your Streamlit app in your browser.
  Local URL:  http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

Your default browser will open automatically at `http://localhost:8501`.

### Step 3 — Verify the Connection

In the Streamlit sidebar, click the **"🔍 Check API Health"** button.

- ✅ **"Flask API is online!"** — Both servers are connected and ready.
- ❌ **"Flask API is offline"** — The Flask server in Terminal 1 is not running. Go back to Step 1.

### Stopping the Application

To stop either server, press `Ctrl + C` in the corresponding terminal window.

---

## 6. API Reference

### 6.1 Data Model

Each student record contains the following fields:

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `student_id` | `string` | ✅ Yes | Unique identifier for the student | `"STU001"` |
| `student_name` | `string` | ✅ Yes | Full name of the student | `"Arun Kumar"` |
| `years_of_experience` | `integer` | ✅ Yes | Total professional experience in years | `3` |
| `company_name` | `string` | ✅ Yes | Current or most recent employer | `"Infosys"` |

**Example Record:**

```json
{
  "student_id": "STU001",
  "student_name": "Arun Kumar",
  "years_of_experience": 3,
  "company_name": "Infosys"
}
```

### 6.2 Base URL

```
http://127.0.0.1:5000
```

All endpoints are relative to this base URL.

---

### 6.3 GET — Retrieve Students

#### Get All Students

```
GET /students
```

Returns the complete list of all student records.

**Request**

```bash
curl http://127.0.0.1:5000/students
```

**Response — 200 OK**

```json
{
  "status": "success",
  "count": 10,
  "data": [
    {
      "student_id": "STU001",
      "student_name": "Arun Kumar",
      "years_of_experience": 3,
      "company_name": "Infosys"
    },
    ...
  ]
}
```

---

#### Get a Single Student

```
GET /students/{student_id}
```

Returns a single student matching the given ID.

**Path Parameter**

| Parameter | Type | Description |
|---|---|---|
| `student_id` | `string` | The unique student ID (e.g. `STU001`) |

**Request**

```bash
curl http://127.0.0.1:5000/students/STU001
```

**Response — 200 OK**

```json
{
  "status": "success",
  "data": {
    "student_id": "STU001",
    "student_name": "Arun Kumar",
    "years_of_experience": 3,
    "company_name": "Infosys"
  }
}
```

**Response — 404 Not Found**

```json
{
  "status": "error",
  "message": "Student 'STU999' not found"
}
```

---

### 6.4 POST — Create a Student

```
POST /students
```

Creates a new student record. The `student_id` must be unique and all four fields are required.

**Request Headers**

```
Content-Type: application/json
```

**Request Body**

```json
{
  "student_id": "STU011",
  "student_name": "Rahul Verma",
  "years_of_experience": 2,
  "company_name": "Google India"
}
```

**Request**

```bash
curl -X POST http://127.0.0.1:5000/students \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "STU011",
    "student_name": "Rahul Verma",
    "years_of_experience": 2,
    "company_name": "Google India"
  }'
```

**Response — 201 Created**

```json
{
  "status": "success",
  "message": "Student created",
  "data": {
    "student_id": "STU011",
    "student_name": "Rahul Verma",
    "years_of_experience": 2,
    "company_name": "Google India"
  }
}
```

**Response — 409 Conflict** *(ID already exists)*

```json
{
  "status": "error",
  "message": "Student ID 'STU011' already exists"
}
```

**Response — 400 Bad Request** *(missing fields)*

```json
{
  "status": "error",
  "message": "Missing fields: ['company_name']"
}
```

---

### 6.5 PUT — Update a Student

```
PUT /students/{student_id}
```

Updates an existing student's details. The `student_id` in the URL identifies the record. Any combination of the three updatable fields can be provided; omitted fields retain their existing values.

**Path Parameter**

| Parameter | Type | Description |
|---|---|---|
| `student_id` | `string` | ID of the student to update |

**Updatable Fields**

| Field | Type | Description |
|---|---|---|
| `student_name` | `string` | Updated full name |
| `years_of_experience` | `integer` | Updated experience count |
| `company_name` | `string` | Updated company name |

**Request**

```bash
curl -X PUT http://127.0.0.1:5000/students/STU003 \
  -H "Content-Type: application/json" \
  -d '{
    "student_name": "Ravi Chandran",
    "years_of_experience": 4,
    "company_name": "Infosys"
  }'
```

**Response — 200 OK**

```json
{
  "status": "success",
  "message": "Student updated",
  "data": {
    "student_id": "STU003",
    "student_name": "Ravi Chandran",
    "years_of_experience": 4,
    "company_name": "Infosys"
  }
}
```

**Response — 404 Not Found**

```json
{
  "status": "error",
  "message": "Student 'STU003' not found"
}
```

---

### 6.6 DELETE — Remove a Student

```
DELETE /students/{student_id}
```

Permanently removes a student record from the database. **This operation cannot be undone.**

**Path Parameter**

| Parameter | Type | Description |
|---|---|---|
| `student_id` | `string` | ID of the student to delete |

**Request**

```bash
curl -X DELETE http://127.0.0.1:5000/students/STU010
```

**Response — 200 OK**

```json
{
  "status": "success",
  "message": "Student 'STU010' deleted"
}
```

**Response — 404 Not Found**

```json
{
  "status": "error",
  "message": "Student 'STU010' not found"
}
```

---

### 6.7 Health Check

```
GET /health
```

A lightweight endpoint to confirm the Flask server is running. Used by the Streamlit sidebar health check button.

**Request**

```bash
curl http://127.0.0.1:5000/health
```

**Response — 200 OK**

```json
{
  "status": "ok",
  "message": "Flask API is running"
}
```

---

## 7. HTTP Status Code Reference

Every API response includes an HTTP status code. The table below lists all codes used by this application.

| Code | Name | When It Occurs |
|---|---|---|
| **200** | OK | Successful GET, PUT, or DELETE |
| **201** | Created | Successful POST (new student created) |
| **400** | Bad Request | Missing required fields or invalid JSON body |
| **404** | Not Found | Student ID does not exist in the database |
| **409** | Conflict | Attempt to POST a student ID that already exists |
| **500** | Internal Server Error | Unexpected server-side failure |

### Reading Status Codes in the UI

The Streamlit response panel uses colour coding to make status codes immediately recognisable:

- 🟢 **Green (2xx)** — The request succeeded
- 🔴 **Red (4xx)** — The request had a problem (client-side error)
- 🟡 **Yellow (5xx)** — The server encountered an error

---

## 8. Sample Dataset

The application ships with 10 pre-loaded student records in `students.json`.

| Student ID | Student Name | Experience (Yrs) | Company |
|---|---|---|---|
| STU001 | Arun Kumar | 3 | Infosys |
| STU002 | Priya Sharma | 5 | TCS |
| STU003 | Ravi Chandran | 1 | Wipro |
| STU004 | Deepa Nair | 7 | HCL Technologies |
| STU005 | Mohammed Farooq | 4 | Cognizant |
| STU006 | Sneha Patel | 2 | Tech Mahindra |
| STU007 | Vikram Singh | 6 | Accenture |
| STU008 | Lakshmi Menon | 0 | Freshworks |
| STU009 | Karthik Rajan | 9 | Zoho Corporation |
| STU010 | Ananya Bose | 3 | IBM India |

> **Tip:** To reset the database to its original state, simply replace the contents of `students.json` with the 10 records above, or keep a backup copy of the original file.

---

## 9. Streamlit UI — User Guide

The Streamlit application at `http://localhost:8501` is organized into a **persistent sidebar** and **five tabs**.

### 9.1 Sidebar & Health Check

The sidebar is always visible regardless of which tab is active.

| Sidebar Element | Description |
|---|---|
| Quick Start Guide | Four-step setup summary |
| Status Code Legend | Colour-coded reference for 200, 201, 404, etc. |
| API Endpoints | At-a-glance list of all available endpoints |
| 🔍 Check API Health button | Sends `GET /health` and shows online/offline status |

**Always click "Check API Health" first** before using any other tab to confirm the Flask server is reachable.

---

### 9.2 GET Tab

**Purpose:** Retrieve student records from the API.

**Mode 1 — All Students**

1. Select the **"All Students"** radio option.
2. Click **▶ Fetch All Students**.
3. The response panel shows the full JSON response.
4. A formatted, sortable **table view** renders automatically below the response.

**Mode 2 — Single Student by ID**

1. Select the **"Single Student by ID"** radio option.
2. Type a Student ID in the input field (e.g. `STU001`).
3. Click **▶ Fetch Student**.
4. The response shows the matched record, or a `404` error if the ID does not exist.

**What to look for:**
- `"status": "success"` and `"count": 10` confirm the data is loading correctly.
- Try `STU999` intentionally to observe the `404 Not Found` error response.

---

### 9.3 POST Tab

**Purpose:** Add a new student record to the database.

**Steps:**

1. Fill in all four fields:
   - **Student ID** — Must be unique (e.g. `STU011`). Using an existing ID returns `409 Conflict`.
   - **Student Name** — Full name of the student.
   - **Years of Experience** — Use the number spinner; minimum is `0`.
   - **Company Name** — Current or most recent employer.
2. Expand **"📋 Request Body Preview"** to inspect the JSON that will be sent.
3. Click **▶ Create Student**.
4. A `201 Created` response confirms the record was saved to `students.json`.

**Validation behaviour:**
- Leaving any field blank will show a warning before the request is sent.
- Submitting a duplicate `student_id` returns `409 Conflict` from the API.

---

### 9.4 PUT Tab

**Purpose:** Update an existing student's details.

**Steps:**

1. Enter the **Student ID** of the record to modify (e.g. `STU003`).
2. Click **🔍 Load Current Data** — this fetches the student's existing values and pre-fills the form fields automatically.
3. Edit any combination of: Student Name, Years of Experience, Company Name.
4. Expand **"📋 Request Body Preview"** to confirm the changes.
5. Click **▶ Update Student**.
6. A `200 OK` response with the updated record confirms the save was successful.

> **Tip:** Always use "Load Current Data" before editing. It pre-fills the form with live values from the database, preventing accidental data loss from empty fields.

---

### 9.5 DELETE Tab

**Purpose:** Permanently remove a student record.

**Steps:**

1. Enter the **Student ID** to delete (e.g. `STU010`).
2. Click **🔍 Preview Student** — this shows the student's current record so you can confirm it is the correct one before proceeding.
3. Read the warning: *"Deletion is permanent and cannot be undone."*
4. Check the **confirmation checkbox** to enable the delete button.
5. Click **▶ Delete Student**.
6. A `200 OK` response and a 🎈 balloons animation confirm the deletion.

> ⚠️ **Warning:** There is no undo. Once deleted, the record is removed from `students.json`. To restore it, add it back manually via the POST tab or by editing `students.json` directly.

---

### 9.6 How to Use Tab

The **📘 How to Use** tab is an in-app guide covering:

- Prerequisites and installation commands
- Project folder structure
- Step-by-step setup instructions
- What to do for each HTTP method tab
- How to read the response panel
- A sample data table with ready-to-use Student IDs

---

## 10. Response Format

All API responses — success and error — follow a consistent JSON envelope format.

### Success Response Structure

```json
{
  "status": "success",
  "message": "Optional human-readable message",
  "count": 10,
  "data": { ... }
}
```

| Field | Presence | Description |
|---|---|---|
| `status` | Always | `"success"` or `"error"` |
| `message` | Sometimes | Human-readable summary of the outcome |
| `count` | GET /students only | Total number of records returned |
| `data` | On success | The student object or array |

### Error Response Structure

```json
{
  "status": "error",
  "message": "Student 'STU999' not found"
}
```

| Field | Presence | Description |
|---|---|---|
| `status` | Always | `"error"` |
| `message` | Always | Describes what went wrong |

---

## 11. Error Handling

The application handles both client-side and connectivity errors gracefully.

### API-Level Errors

| Scenario | HTTP Code | Error Message |
|---|---|---|
| Student ID not found | `404` | `"Student 'STUXXX' not found"` |
| Duplicate Student ID on POST | `409` | `"Student ID 'STUXXX' already exists"` |
| Missing required fields | `400` | `"Missing fields: ['field_name']"` |
| Non-JSON request body | `400` | `"Request body must be JSON"` |

### UI-Level Errors

| Scenario | Behaviour |
|---|---|
| Flask API is not running | Response panel shows `"Cannot connect to Flask API"` |
| Empty required form fields | Streamlit warning shown; request is not sent |
| Network timeout | Requests library 5-second timeout; error shown in response panel |

---

## 12. Testing with External Tools

In addition to the Streamlit UI, the API can be tested directly using standard developer tools.

### Using cURL (Terminal)

```bash
# Get all students
curl http://127.0.0.1:5000/students

# Get single student
curl http://127.0.0.1:5000/students/STU001

# Create a student
curl -X POST http://127.0.0.1:5000/students \
  -H "Content-Type: application/json" \
  -d '{"student_id":"STU011","student_name":"Rahul Verma","years_of_experience":2,"company_name":"Google India"}'

# Update a student
curl -X PUT http://127.0.0.1:5000/students/STU001 \
  -H "Content-Type: application/json" \
  -d '{"student_name":"Arun Kumar","years_of_experience":5,"company_name":"Microsoft India"}'

# Delete a student
curl -X DELETE http://127.0.0.1:5000/students/STU010
```

### Using Python (requests library)

```python
import requests

BASE = "http://127.0.0.1:5000"

# GET all
r = requests.get(f"{BASE}/students")
print(r.json())

# POST
r = requests.post(f"{BASE}/students", json={
    "student_id": "STU011",
    "student_name": "Rahul Verma",
    "years_of_experience": 2,
    "company_name": "Google India"
})
print(r.status_code, r.json())

# PUT
r = requests.put(f"{BASE}/students/STU001", json={
    "years_of_experience": 6
})
print(r.status_code, r.json())

# DELETE
r = requests.delete(f"{BASE}/students/STU010")
print(r.status_code, r.json())
```

### Using Postman

1. Open Postman and create a new request.
2. Set the method (GET / POST / PUT / DELETE) from the dropdown.
3. Enter the URL: `http://127.0.0.1:5000/students`
4. For POST and PUT, go to the **Body** tab → select **raw** → choose **JSON** from the dropdown → paste your JSON payload.
5. Click **Send**.

---

## 13. Troubleshooting

### Flask server won't start

**Symptom:** `Address already in use` or `Port 5000 is in use`

**Solution:** Another process is using port 5000. Either stop that process or change the port in `flask_api.py`:

```python
# Change the last line in flask_api.py
app.run(debug=True, port=5001)   # Use any available port
```

If you change the port, also update the `BASE_URL` variable at the top of `streamlit_app.py`:

```python
BASE_URL = "http://127.0.0.1:5001"
```

---

### Streamlit shows "Cannot connect to Flask API"

**Cause:** The Flask server in Terminal 1 is not running.

**Solution:** Open Terminal 1 and run `python flask_api.py`. Wait until you see `Running on http://127.0.0.1:5000`, then retry in the Streamlit UI.

---

### `ModuleNotFoundError: No module named 'flask'`

**Solution:** Install the missing package:

```bash
pip install flask
```

If using a virtual environment, make sure it is activated before running the install and before starting either server.

---

### Changes not saving to `students.json`

**Possible causes and solutions:**

- The `students.json` file may be open in another application and locked. Close it and retry.
- The file may have become corrupted. Replace it with a fresh JSON array of student records.
- The Flask process may not have write permissions to the file. Check folder permissions.

---

### Streamlit page is blank or not loading

**Solution:** Stop the Streamlit process with `Ctrl + C` and restart it:

```bash
streamlit run streamlit_app.py
```

If the browser does not open automatically, navigate manually to `http://localhost:8501`.

---

### PUT form fields are empty after clicking "Load Current Data"

**Cause:** The Student ID entered does not exist.

**Solution:** Confirm the ID exists first by looking it up in the GET tab. Try IDs from `STU001` to `STU010`.

---

## 14. Project Limitations & Future Improvements

### Current Limitations

| Limitation | Description |
|---|---|
| Flat-file storage | `students.json` is not suitable for concurrent users or large datasets |
| No authentication | All endpoints are publicly accessible with no API key or login required |
| No pagination | `GET /students` always returns all records regardless of dataset size |
| No search/filter | There is no query parameter support to filter by name or company |
| Development server only | Flask's built-in server is not suitable for production deployment |
| No input sanitisation | Student ID and name fields accept any string value |

### Suggested Future Improvements

**Short-term:**
- Add query parameters for filtering, e.g. `GET /students?company=Infosys`
- Validate that `student_id` follows a specific format (e.g. `STU` prefix + 3 digits)
- Add a `PATCH` endpoint for partial updates (currently PUT handles partial updates too)

**Medium-term:**
- Replace `students.json` with a **SQLite** or **PostgreSQL** database using SQLAlchemy
- Add pagination support: `GET /students?page=1&limit=5`
- Implement basic **API key authentication**

**Long-term:**
- Generate interactive API documentation with **Swagger / OpenAPI** (`flask-smorest` or `flasgger`)
- Containerise with **Docker** for one-command deployment
- Add unit and integration tests using `pytest` and `Flask`'s test client
- Deploy to a cloud platform (Render, Railway, or AWS)

---

## 15. Glossary

| Term | Definition |
|---|---|
| **API** | Application Programming Interface — a set of rules that allows software components to communicate with each other |
| **REST** | Representational State Transfer — an architectural style for APIs that uses standard HTTP methods and stateless communication |
| **Endpoint** | A specific URL that the API exposes to perform an action (e.g. `/students/STU001`) |
| **HTTP Method** | The action being performed on a resource: GET (read), POST (create), PUT (update), DELETE (remove) |
| **HTTP Status Code** | A 3-digit number in every API response indicating the outcome of the request |
| **CRUD** | Create, Read, Update, Delete — the four fundamental data operations |
| **JSON** | JavaScript Object Notation — a lightweight, human-readable data format used to exchange information between the API and clients |
| **Payload / Request Body** | The JSON data sent along with a POST or PUT request |
| **Flask** | A lightweight Python web framework used to build web applications and APIs |
| **Streamlit** | An open-source Python framework for building interactive web applications for data and machine learning |
| **Route** | A URL pattern mapped to a Python function in Flask (e.g. `@app.route("/students")`) |
| **Base URL** | The root address of the API: `http://127.0.0.1:5000` |
| **Resource** | A data entity exposed by the API — in this project, a *student* is the resource |
| **Client** | The application making requests to the API — in this project, the Streamlit app is the client |
| **Server** | The application responding to requests — in this project, the Flask app is the server |
| **Flat-file Database** | A simple data store that uses a plain file (here, `students.json`) instead of a dedicated database engine |

---

*End of Document*

---

> **Project developed as a learning tool for REST API concepts using Python Flask and Streamlit.**  
> For questions or improvements, extend the codebase following the suggestions in Section 14.
