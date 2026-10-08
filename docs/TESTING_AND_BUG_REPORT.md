# PharmaIQ — Software Verification & Validation Report

**Scope:** Test case design, test case analysis, manual testing, bug detection, bug analysis, and bug repair for the PharmaIQ platform (FastAPI backend, ML engine, React frontend, Docker/CI).

| Item | Before V&V | After V&V |
|---|---|---|
| Automated tests | 16 (all passing — but against stub code) | **82** (all passing) |
| Backend statement coverage | 29 % | **72 %** |
| Manual test cases executed | 0 | **24** (16 API + 5 data/AI + 3 UI, all passing) |
| Defects found and fixed | — | **36** (34 pre-existing + 2 introduced during repair, both caught by testing) |
| Values shown in the app taken from the datasets | almost none (hard-coded) | **all** dashboards, KPIs, charts, monitoring, anomalies, explanations, AI answers |
| Patient-risk model accuracy | chance level (labels were random) | **85 %** |
| Trial-dropout model accuracy | chance level (labels were random) | **86 %** |

---

## 1. How to run the system and the tests

```bash
# 1. Backend dependencies (from the repo root)
python -m venv backend/venv
backend/venv/Scripts/pip install -r backend/requirements.txt      # Windows
# source backend/venv/bin/activate && pip install -r backend/requirements.txt   # Linux/macOS

# 2. Train the ML models (required for /api/ml/* endpoints)
backend/venv/Scripts/python -m ml_engine.training.train_all

# 3. Run the automated test suite (from the repo root)
backend/venv/Scripts/python -m pytest

# 4. Start the API for manual testing (from backend/)
cd backend && venv/Scripts/python -m uvicorn app.main:app --port 8000
#    Interactive API console (used for manual testing): http://localhost:8000/docs

# 5. Start the frontend (from frontend/)
npm install && npm run dev        # http://localhost:5173
```

---

## 2. Test strategy

| Level | What was tested | Tool |
|---|---|---|
| Unit | Scoring rules, ML training data, K-Means label mapping, upload filename sanitising | pytest |
| Integration / API | Every REST endpoint through FastAPI's `TestClient` | pytest + TestClient |
| System (manual) | Live server over HTTP, browser UI | Swagger UI (`/docs`), curl, browser |
| Security | CORS, path traversal, file type/size, token replay, brute-force rate limit | manual + pytest |
| Regression | One automated test per fixed defect (`backend/tests/test_regressions.py`) | pytest |
| Build / deploy | Frontend `tsc` + `vite build`, Dockerfile, CI workflows | npm, GitHub Actions |

### 2.1 Test design techniques used

| Technique | Where it was applied | Example |
|---|---|---|
| **Equivalence Partitioning (EP)** | Patient age, completion rate, file types | age ∈ {invalid < 0}, {valid 0–120}, {invalid > 120}; file ∈ {.pdf/.txt/.csv} vs {anything else} |
| **Boundary Value Analysis (BVA)** | All numeric thresholds | age −1 / 0 / 120 / 121; engagement 80 / 79.9 / 60 / 59.9; marketing spend 25 000 / 25 001; `limit` 0 / 1 / 500 / 501 |
| **Decision table** | Doctor segmentation, dropout reason | (missed visits ≥ 2) → "Multiple missed visits"; else (side effects = HIGH) → "Severe side effects"; else → "Engagement and adherence risk" |
| **State transition** | Token lifecycle | login → refresh (token₁ → token₂) → replay token₁ ⇒ must be **rejected** |
| **Error guessing** | Security | filenames `../../evil.txt`, `..\..\evil.txt`; foreign CORS origin; using an access token as a refresh token |
| **Negative testing** | All POST endpoints | missing required fields, wrong types, out-of-range values must return **422**, not 200 |

---

## 3. Test case analysis (findings about the *original* tests)

The original 16 tests all passed, yet the application's core features did not work. Analysis of why:

1. **Assertions checked only that a key existed, not its value.**
   `assert 'category' in data` passed against a stub returning `{"risk_score": 0, "category": "Pending ML Integration"}`. A test that cannot fail does not verify anything.
2. **Tests encoded the wrong contract.** `POST /api/predict/patient-risk` was tested with only `{"patient_id": 101}` — no clinical data — so the test *required* the endpoint to ignore its inputs.
3. **No negative or boundary tests.** Nothing checked that invalid data (age = −500) was rejected.
4. **The ML layer was tested only by import** (`model is not None`), never by prediction, so untrained models and the broken training package went unnoticed.
5. **No security tests** (CORS, uploads, tokens).
6. **Low coverage (29 %)**; whole modules (uploads, auth refresh, ML services) never executed.

**Corrective action:** tests now assert exact expected values (e.g. risk score 84.3 → `HIGH`), include EP/BVA/negative cases, train and exercise real models, and add one regression test per defect.

---

## 4. Manual test cases

Executed against the running server (`uvicorn`, port 8000) via Swagger UI / curl, and against the React UI in a browser. "Before" is the result on the original code; "After" is the result after repair.

### TC-01 — API health check
| Field | Value |
|---|---|
| Module | Platform |
| Precondition | Backend started |
| Steps | `GET /health` |
| Expected | 200, `{"status":"healthy"}` |
| Before | 200 ✔ |
| After | 200 `{"status":"healthy","environment":"development"}` — **PASS** |

### TC-02 — Login with valid credentials
| Field | Value |
|---|---|
| Module | Authentication |
| Steps | `POST /api/auth/token` body `{"username":"admin","password":"AdminPass123!"}` |
| Expected | 200 with `access_token`, `refresh_token`, `role = ADMIN` |
| Before / After | 200 ✔ / 200 ✔ — **PASS** |

### TC-03 — Login with invalid password (negative)
| Field | Value |
|---|---|
| Steps | `POST /api/auth/token` body `{"username":"admin","password":"nope"}` |
| Expected | 401 "Incorrect username or password" |
| Before / After | 401 ✔ / 401 ✔ — **PASS** |

### TC-04 — Protected endpoint requires a token
| Field | Value |
|---|---|
| Steps | (a) `GET /api/auth/me` with no header; (b) same with `Authorization: Bearer <access_token from TC-02>` |
| Expected | (a) 401; (b) 200 with username/role/email |
| After | (a) 401 "Not authenticated"; (b) 200 `{"username":"admin","role":"ADMIN",…}` — **PASS** |

### TC-05 — Patient risk prediction, valid high-risk patient
| Field | Value |
|---|---|
| Module | Patient analytics |
| Steps | `POST /api/predict/patient-risk` body `{"age":72,"glucose_level":190,"previous_visits":9}` |
| Expected | 200, `risk_score = 84.3`, `category = HIGH` (0.4·0.72 + 0.3·0.95 + 0.3·0.9 = 0.843) |
| Before | 200 `{"risk_score":0,"category":"Pending ML Integration"}` — **FAIL (BUG-01)** |
| After | 200 `{"risk_score":84.3,"category":"HIGH","recommended_action":"Immediate follow-up required"}` — **PASS** |

### TC-06 — Patient age boundary values (BVA)
| Input age | Expected | Before | After |
|---|---|---|---|
| −1 | 422 | 200 (accepted) ✘ | 422 ✔ |
| 0 | 200 | 200 | 200, score 18.0 LOW ✔ |
| 120 | 200 | 200 | 200, score 58.0 MEDIUM ✔ |
| 121 | 422 | 200 (accepted) ✘ | 422 ✔ |

Other fields: `glucose_level = 100`, `previous_visits = 1`. **Result: PASS after fix (BUG-05).**

### TC-07 — Patient risk with missing required fields (negative)
| Field | Value |
|---|---|
| Steps | `POST /api/predict/patient-risk` body `{"patient_id":101}` |
| Expected | 422 listing missing `age`, `glucose_level`, `previous_visits` |
| Before | 200 with stub result — **FAIL** |
| After | 422 "Field required" for each missing field — **PASS** |

### TC-08 — Clinical trial dropout prediction (decision table + range check)
| Input | Expected | Before | After |
|---|---|---|---|
| `{"completion_rate":40,"previous_missed_visits":3,"side_effects":"HIGH"}` | 200, 64.0 %, `HIGH`, reason "Multiple missed visits" | 200 `{"dropout_probability":0,"status":"Model Integration Pending"}` ✘ | 200, 64.0, HIGH, "Multiple missed visits" ✔ |
| `{"completion_rate":140,"previous_missed_visits":0}` | 422 (rate > 100 %) | 200 ✘ | 422 ✔ |

### TC-09 — Sales forecast and stock recommendation (BVA on spend threshold)
| Input | Expected | Before | After |
|---|---|---|---|
| 100 units, spend 1 000 | +10 %, stock **110** | stub text "Future ML Forecasting Module"; the unused real implementation returned 15 000 ✘ | +10 %, 110 ✔ |
| 100 units, spend **25 000** | +10 % (threshold is "> 25 000") | stub ✘ | +10 %, 110 ✔ |
| 100 units, spend **25 001** | +18 %, stock 118 | stub ✘ | +18 %, 118 ✔ |

### TC-10 — Doctor segmentation boundaries
| Engagement score | Expected segment | After |
|---|---|---|
| 80 | Segment A (High Value) | Segment A ✔ |
| 79.9 | Segment B (Growth) | Segment B ✔ |
| 60 | Segment B | Segment B ✔ |
| 59.9 | Segment C (Low Engagement) | Segment C ✔ |

Before: every input returned `{"segment":"KMeans Model Pending"}` — **FAIL (BUG-01)**.

### TC-11 — Patient list and pagination
| Steps | Expected | Before | After |
|---|---|---|---|
| `GET /api/patients?limit=2` | 2 real patient records + `total` | `{"patients":[]}` ✘ | 2 records, `total: 1000` ✔ |
| `GET /api/patients?limit=0` | 422 | n/a (no paging) | 422 ✔ |

### TC-12 — ML model prediction (trained ensemble)
| Field | Value |
|---|---|
| Precondition | `python -m ml_engine.training.train_all` has been run |
| Steps | `POST /api/ml/patient-risk` body `{"age":72,"previous_visits":9,"treatment_duration":12,"glucose_level":190,"blood_pressure_systolic":160,"blood_pressure_diastolic":100}` |
| Expected | 200 with `risk_probability` and `risk_category`, no `error` key |
| Before | **200** `{"error":"This StandardScaler instance is not fitted yet…","risk_category":"UNKNOWN"}` — error hidden behind a success code (BUG-02/03/04) |
| After | 200 `{"risk_probability":0.996,"risk_category":"HIGH",…}` — **PASS**. If models are missing, now returns **503** with instructions instead of a fake 200. |

### TC-13 — Document upload security (error guessing)
| Input file | Expected | Before | After |
|---|---|---|---|
| `payload.exe` | 415 Unsupported type | Accepted and written to disk ✘ | 415 ✔ |
| filename `../../note.txt` | Stored as `backend/documents/note.txt` only | Filename passed through unsanitised into `os.path.join` → written outside the upload folder ✘ | Saved as `note.txt` inside `documents/`; nothing written to the repo root ✔ |
| empty `empty.txt` | 400 | Accepted ✘ | 400 ✔ |

### TC-14 — CORS policy
| Request `Origin` header | Expected `Access-Control-Allow-Origin` | Before | After |
|---|---|---|---|
| `http://evil.example` | *(absent)* | `http://evil.example` **with** `allow-credentials: true` ✘ | absent ✔ |
| `http://localhost:5173` | `http://localhost:5173` | ✔ | ✔ |

### TC-15 — Refresh token replay (state transition)
| Step | Expected | Before | After |
|---|---|---|---|
| Refresh with token₁ | 200, returns **new** token₂ | 200, returned the *same* token₁ ✘ | 200, token₂ ✔ |
| Refresh again with token₁ | 401 revoked | 200 (token₁ reusable for 7 days) ✘ | 401 "Refresh token has been revoked" ✔ |

### TC-16 — MLOps run with unknown pipeline name
| Field | Value |
|---|---|
| Steps | `POST /api/mlops/run-pipeline?pipeline=bogus` |
| Expected | 404 listing valid pipelines |
| Before | 200 `{"status":"completed","pipeline":"bogus",…}` — false success ✘ |
| After | 404 "Unknown pipeline "bogus". Expected one of: all, doctor, patient, sales, trial." — **PASS** |

### Running the manual test cases in the web app

Every API test case above can also be run from the React web app (`npm run dev` in `frontend/`, then http://localhost:5173). Each form shows the HTTP status badge, the endpoint called, and the server's response or validation messages; "Raw request and response" shows the exact JSON (passwords masked). Inputs deliberately have no browser-side limits, so invalid values reach the server and its validation can be shown.

| Page (sidebar) | Form | Test cases |
|---|---|---|
| Any page | "API healthy" badge in the sidebar | TC-01 |
| Login & Tokens | Log in; Who am I (with / without token); Refresh; Replay old refresh token | TC-02, TC-03, TC-04, TC-15 |
| Patient Analytics | Patient risk calculator (rule-based and ML model buttons) | TC-05, TC-06, TC-07, TC-12 |
| Patient Analytics | Patient records (limit / offset) | TC-11 |
| Clinical Trials | Trial dropout predictor | TC-08 |
| Sales Intelligence | Stock forecast | TC-09 |
| Doctor Segmentation | Doctor segment calculator (80 / 79.9 / 60 / 59.9 shortcuts) | TC-10 |
| AI Assistant | Upload document | TC-13 |
| AI Assistant | Ask / example questions; upload then ask | TC-17, TC-18, TC-19 |
| Dashboard (and every analytics page) | KPI cards and charts; "Refresh data" | TC-20, TC-21 |
| Executive Dashboard | MLOps pipeline runner | TC-16 |

TC-14 (CORS) cannot be shown from inside the app, because the browser always sends the app's own origin; run it with `curl.exe -i -H "Origin: http://evil.example" http://localhost:8000/health`.

### Data and AI assistant test cases (web app)

| ID | Technique | Steps | Expected | Before fix | After fix |
|---|---|---|---|---|---|
| TC-17 | Positive (oracle = the CSV) | AI Assistant → "Which region generated maximum sales?" | The region with the largest revenue sum in `pharma_sales.csv` (South, $12.28M, 25.5%), labelled "Computed from datasets" | `"[Fallback summary] 20 0 obj 8722 endobj"` — raw PDF bytes ✘ | South, $12.28M, table of all regions, source `pharma_sales.csv` — **PASS** |
| TC-18 | Positive | Upload a TXT stating "The Chennai trial site reported 12 serious adverse events", then ask "How many serious adverse events did the Chennai site report?" | Answer quotes the sentence with "12", source = the uploaded file | Index lost on restart; PDFs unreadable ✘ | "The Chennai trial site reported 12 serious adverse events…" [file] — **PASS** |
| TC-19 | Negative | Ask "What is the capital of France?" | Honest "no match" message plus example questions, not invented text | Dumped an unrelated chunk ✘ | "I couldn't match that…", example chips shown — **PASS** |
| TC-20 | Oracle comparison | Dashboard KPI "Total Patients" and "High-risk" vs counting rows in `patients.csv` | 1,000 patients, 732 high risk (73.2%) | Hard-coded 1,920 / 314 ✘ | 1,000 / 732 (73.2%) — **PASS** |
| TC-21 | State change (live data) | Copy `doctors.csv` as a backup, delete one data row, click "Refresh data" on Doctor Segmentation, then restore the backup | "Doctors" KPI drops by 1 without restarting the API, then returns | Values never changed (hard-coded) ✘ | **PASS** in the automated equivalent `test_dataset_changes_are_picked_up_without_restart` (file edited → next request returns the new row count); run the manual steps live to demonstrate |

### UI manual tests (browser, http://localhost:5173)

| ID | Steps | Expected | Result |
|---|---|---|---|
| TC-UI-01 | AI Assistant → click the example "Which trial phase has the highest dropout rate?" | Answer with source file and supporting table appears in the conversation | **PASS** (Phase 3, 52.4%) |
| TC-UI-02 | AI Assistant → choose a `.exe` file | Message shows the server reason: "Upload failed: Unsupported file type ".exe"…" | Before: generic "Upload failed. Please try again." — After: **PASS** |
| TC-UI-03 | Choose the same file twice in a row | Second selection triggers another upload attempt | Before: nothing happened — After: **PASS** |

### Manual test summary

| Total | Passed (after fix) | Failed before fix |
|---|---|---|
| 16 API + 5 data/AI + 3 UI = **24** | **24** | **19** (TC-05 … TC-21, TC-UI-02, TC-UI-03) |

---

## 5. Bug reports

Severity scale: **Critical** (feature unusable / exploitable), **High** (wrong results or security weakness), **Medium** (incorrect behaviour with workaround), **Low** (minor / maintainability), **Cosmetic**.

| ID | Title | Severity | Area | Detected by |
|---|---|---|---|---|
| BUG-01 | Prediction and list endpoints are stubs returning 0 / empty lists | Critical | Backend | Manual TC-05/08/09/10/11 |
| BUG-02 | ML training package cannot be imported — models can never be trained | Critical | ML engine | Running training |
| BUG-03 | ML failures returned as HTTP 200 with an `error` field | High | Backend | Manual TC-12 |
| BUG-04 | Model path resolved relative to current directory | High | Backend | Code review + TC-12 |
| BUG-05 | No input validation (negative ages, rates > 100 %) | High | Backend | BVA TC-06/08 |
| BUG-06 | CORS reflects any origin with credentials | High | Security | TC-14 |
| BUG-07 | Upload path traversal; no file type, size or empty checks | Critical | Security | Error guessing TC-13 |
| BUG-08 | RAG router written but never registered (404) | Medium | Backend | Endpoint probe |
| BUG-09 | `schemas.py` / `models.py` / `database.py` shadowed by packages; working route files dead | Medium | Backend | Root-cause analysis of BUG-01 |
| BUG-10 | Users have roles (`DATA_SCIENTIST`, `BUSINESS_USER`) missing from the RBAC tables | Medium | Security | Code review |
| BUG-11 | Login rate limiter keyed by username only → anyone can lock out any account | Medium | Security | Code review |
| BUG-12 | Unknown MLOps pipeline reported as "completed" | Medium | Backend | TC-16 |
| BUG-13 | Explainability accepts patient ID ≤ 0 | Low | Backend | Negative testing |
| BUG-14 | Docker image omits modules imported at startup → container crashes | High | Deployment | Dockerfile review |
| BUG-15 | Stock recommendation floored at 15 000 units regardless of demand | Medium | Business logic | TC-09 |
| BUG-16 | Empty AI question loads the embedding model (network download) before being rejected | Low | Performance | Probe |
| BUG-17 | Training labels generated randomly → models learn noise | High | ML | Training-data analysis |
| BUG-18 | K-Means cluster IDs mapped to fixed labels → "High Value" may be the worst doctors | High | ML | Model analysis |
| BUG-19 | JWT secret defined twice with different hard-coded defaults; read before `.env` loads | Medium | Security | Code review |
| BUG-20 | Refresh tokens never rotated or revoked | Medium | Security | TC-15 |
| BUG-21 | Kafka fallback `print`s patient data to stdout | Low | Privacy | Code review |
| BUG-22 | Frontend API URL hard-coded to `localhost:8000` | Low | Frontend | Code review |
| BUG-23 | Frontend hides server error messages; same file cannot be re-selected | Low | Frontend | TC-UI-02/03 |
| BUG-24 | Patient "Disease Distribution" chart squashed by a 200 px left margin | Cosmetic | Frontend | Visual inspection |
| BUG-25 | Deprecated APIs (`.dict()`, `declarative_base`, `HTTP_413_REQUEST_ENTITY_TOO_LARGE`) | Low | Maintainability | Warnings |
| BUG-26 | *(introduced during repair)* `ceil(100 × 1.1)` = 111 due to floating-point error | Medium | Business logic | **Regression test** |
| BUG-27 | `GET /api/ai/status` crashes with HTTP 500 (AttributeError) | High | AI assistant | Endpoint probe |
| BUG-28 | Uploaded PDFs indexed as raw file bytes (`20 0 obj … endobj`), so every answer was garbage | Critical | AI assistant | Manual test TC-17 |
| BUG-29 | When OpenAI fails (account has no credits) the answer is a raw "[Fallback summary]" dump; the old LLM helper used the removed `openai.ChatCompletion` API | High | AI assistant | Manual test + OpenAI error inspection |
| BUG-30 | Document index kept only in memory (lost on every restart); re-uploading a file duplicated it | Medium | AI assistant | Code review |
| BUG-31 | Assistant could not answer anything about the datasets; every response carried the fixed text "Increase HCP engagement campaign" | High | AI assistant | Manual test TC-17 |
| BUG-32 | Backend returned hard-coded values: dashboard KPIs (1,920 patients vs 1,000 in the data), monitoring (91 % for every model), anomalies (always "none"), recommendations (fixed text), explainability (risk decided by odd/even patient ID) | High | Backend (validation) | Oracle comparison TC-20 |
| BUG-33 | Every frontend chart and KPI was a static array (e.g. "81 % completion" vs 49.3 % in the data) | High | Frontend (validation) | Oracle comparison TC-20 |
| BUG-34 | *(introduced during repair)* the assistant read "highest" as the side-effect value "HIGH" and silently filtered to 278 of 800 records | Medium | AI assistant | **Manual test** of the new analyst |
| BUG-35 | Document chunking discarded line breaks, so list/Q&A documents lost their structure | Low | AI assistant | Manual test TC-18 |
| BUG-36 | Pie charts drew no slices when the browser paused animations (hidden window, print) | Cosmetic | Frontend | UI inspection |

---

## 6. Bug analysis (root cause → fix)

### BUG-01 / BUG-09 — Core endpoints were stubs (Critical)
- **Symptom:** every prediction returned `0` / "Pending ML Integration"; every list returned `[]`.
- **Root cause:** two parallel sets of route files existed. `main.py` registered the stub set (`patient_routes.py` …). The working set (`patients.py` …) imported from `app/schemas.py`, but Python resolves `app.schemas` to the **package** `app/schemas/`, so the module file was unreachable. Mounting the working routes would have crashed with `ImportError`, so the stubs stayed.
- **Fix:** moved the real scoring rules into `app/ml/*.py` with validated schemas in `app/schemas/prediction_schema.py`; added `app/services/data_service.py` to serve the CSV datasets with pagination; rewrote the four registered route modules; deleted the 11 dead/shadowed files.
- **Lesson:** the existing tests checked key presence only, so they passed against the stubs (see §3).

### BUG-02 — Training package broken (Critical)
- **Root cause:** `ml_engine/training/__init__.py` did `from .train_patient_model import main`, but no training script defined `main`. Any `python -m ml_engine.training.…` raised `ImportError`. There was also no doctor-model training script.
- **Fix:** added `main = train_…` aliases, `train_doctor_model.py`, and `train_all.py`; training writes to an absolute `ml_engine/saved_models` path. CI now trains models before running tests.

### BUG-03 / BUG-04 — Hidden ML failures (High)
- **Root cause:** each service wrapped prediction in `except Exception: return {'error': …}`, so FastAPI returned 200. Models were loaded from `'ml_engine/saved_models/'` relative to the working directory — from `backend/` that is `backend/ml_engine/saved_models`, which never exists.
- **Fix:** `MODEL_PATH` is resolved against the repo root in `config.py`; services raise `ModelNotTrainedError` → **503** with instructions; other failures → **500**. Models load once instead of on every request.

### BUG-05 — No input validation (High)
- **Fix:** Pydantic `Field(ge=…, le=…)` bounds on every request model (age 0–120, glucose 20–600, rates 0–100, side effects as an enum, pagination 1–500, etc.). Invalid input now returns **422** with a field-level message.

### BUG-06 — CORS (High, security)
- **Root cause:** `allow_origins=[…, '*']` with `allow_credentials=True`. Starlette then echoes back *any* requesting origin, so a malicious website could make authenticated calls from a logged-in user's browser.
- **Fix:** origins come from the `CORS_ORIGINS` env variable; `'*'` is filtered out.

### BUG-07 — Path traversal in uploads (Critical, security)
- **Root cause:** `os.path.join(upload_dir, file.filename)` used the client-supplied name. A filename of `../../x` writes outside the folder (and could overwrite source files). There were also no type, size or empty-file checks, so the endpoint accepted executables.
- **Fix:** new `app/utils/uploads.py` — `PureWindowsPath(name).name` strips both `/` and `\` path parts; extension allowlist (`.pdf .txt .csv`) → 415; size limit (10 MB, configurable) → 413; empty file → 400. Used by both `/api/ai/upload` and `/api/rag/ingest`.

### BUG-10 / BUG-11 / BUG-19 / BUG-20 — Authentication hardening (Medium, security)
- **BUG-10:** added `DATA_SCIENTIST` and `BUSINESS_USER` to `ROLES` and `ROLE_PERMISSIONS`.
- **BUG-11:** the rate-limit key is now `client IP + username`, so one client cannot exhaust another's login budget.
- **BUG-19:** `security.py` now imports `SECRET_KEY` from `config.py` (one definition, loaded after `.env`).
- **BUG-20:** `/refresh` checks the token against the last issued one, issues a new refresh token, and rejects replays with 401.

### BUG-14 — Docker image crashes at startup (High)
- **Root cause:** `anomaly_routes.py` imports the root-level `anomaly_detection.py` and `recommendation_routes.py` imports `recommendation_engine/`, but the Dockerfile copied only `backend/`, `ml_engine/` and `database/`.
- **Fix:** the Dockerfile copies both modules and the CSV datasets, and trains models at build time.

### BUG-15 / BUG-26 — Stock recommendation (Medium)
- **BUG-15:** `max(15000, units × growth)` recommended 15 000 units for a product selling 100. The floor was removed.
- **BUG-26 (found by our own regression test):** the first fix used `math.ceil(100 * 1.1)`. In floating point, `100 * 1.1 = 110.00000000000001`, so the result was **111**. The new test `test_sales_forecast_does_not_overstock_small_products` failed and exposed it. Replaced with exact integer ceiling division `-(-units * (100 + growth) // 100)`. This shows why every fix needs a regression test.

### BUG-17 — Random training labels (High, ML)
- **Root cause:** `'risk': np.random.randint(0, 2, n)` — labels were independent of features, so any accuracy was chance.
- **Fix:** labels are derived from clinically plausible drivers (age, glucose, blood pressure, visits) plus Gaussian noise; the sales target is now a function of historical sales, spend and season. Result: patient model **85 %** accuracy, trial model **86 %**, sales R² **0.986**. A unit test checks that older patients are labelled high-risk more often than younger ones.

### BUG-18 — K-Means label mapping (High, ML)
- **Root cause:** K-Means assigns cluster numbers arbitrarily, but the code mapped `0 → "High Value"`, `1 → "Growth"`, `2 → "Low Engagement"`. Depending on initialisation, the least-engaged doctors could be labelled "High Value".
- **Fix:** after training, clusters are ranked by mean engagement score and that ranking (`cluster_rank`) is saved with the model. The test trains, saves, reloads, and checks that a 92-engagement doctor is "High Value" and a 35-engagement doctor is "Low Engagement".

### Remaining minor fixes
- **BUG-08:** registered `rag_router` in `main.py`.
- **BUG-12:** whitelist `{all, patient, trial, sales, doctor}`; unknown → 404.
- **BUG-13:** `Path(..., ge=0)` on the patient ID (dataset IDs start at 0), plus 404 for IDs not in `patients.csv`.
- **BUG-16:** validate the question before calling `get_engine()`.
- **BUG-21:** log via `logger.warning` without the message body.
- **BUG-22:** `VITE_API_URL` env variable (`frontend/.env.example`).
- **BUG-23:** `getErrorMessage()` helper shows FastAPI's `detail`; the file input is reset after each selection.
- **BUG-24:** chart margin 200 → 10.
- **BUG-25:** `.model_dump()`, `sqlalchemy.orm.declarative_base`, `HTTP_413_CONTENT_TOO_LARGE`.

### BUG-27 … BUG-31 — The AI assistant did not work (Critical)
- **Symptoms:** status page HTTP 500; answers like `"[Fallback summary] 20 0 obj 8722 endobj"`.
- **Root causes (one per bug):** the status route read `engine.vector_db`, which the pipeline engine did not have (27); `DocumentProcessor` opened PDFs as UTF-8 text, so the index held PDF syntax, not words (28); the configured OpenAI account returns *429 – no credits*, and the code's only fallback was to paste the first retrieved chunk (29); the FAISS index lived in memory only (30); nothing in the assistant could read the datasets (31).
- **Fix:** the assistant is now three layers. (1) `DatasetAnalyst` (`app/ai_assistant/analytics_agent.py`) understands the domain, metric, grouping and filters in a question and computes the answer live from the CSVs with pandas. (2) `RAGEngine` parses PDF/TXT/CSV properly (PyPDF2), keeps a persistent index in `ml_engine/saved_models/doc_index.pkl`, replaces a document's chunks on re-upload, and returns the best-matching passage. (3) `LLMService` is optional: it only rephrases the computed facts, and after an authentication or "no credits" error it is switched off instead of slowing every answer. Each response says where it came from (`mode`: dataset / documents / help, plus `+openai` when phrased by the model) and lists its source files.
- **Oracle:** the expected answer is computed independently from the CSV in the tests (`test_ai_answers_sales_question_from_dataset`, `test_ai_counts_high_risk_patients`).

### BUG-32 / BUG-33 — Hard-coded values everywhere (High, validation)
- **Symptom:** the dashboard said 1,920 patients; `patients.csv` has 1,000. Monitoring showed 91 % for all four models. Anomaly detection always said "none".
- **Root cause:** endpoints and React pages returned literal numbers written in the code, so the software could pass verification (it returned *a* value) while failing validation (the value did not describe the data).
- **Fix:** `app/services/data_service.py` loads the CSVs with a cache keyed on file modification time (edits show up without restarting); `app/services/analytics_service.py` computes every KPI, breakdown, forecast (linear trend over the last 12 complete months) and data-driven recommendation; `anomaly_service.py` uses real statistics (z-score on daily sales, Mahalanobis distance on patient profiles, two-proportion z-test on trial dropout); monitoring reads the metrics each training run writes to `metrics.json` and measures data drift with a Population Stability Index; explainability fits a logistic regression on `patients.csv` and reports each feature's contribution. Every React page now fetches `/api/analytics/*` and labels the source file.
- **Tests:** `backend/tests/test_analytics_api.py` recomputes each number from the CSV with pandas and compares.

### BUG-34 — "highest" read as "HIGH" (found by manual testing of the fix)
- The new analyst matched keywords by prefix, so the side-effect value `HIGH` matched inside "highest" and the answer was computed over 278 of 800 participants. Fixed with whole-word matching for filter values; regression test `test_ai_superlative_is_not_read_as_a_filter`. Like BUG-26, this shows a repair introducing a defect that testing caught before release.

---

## 7. Bug repair and fix methodology

Each defect went through the same six-step process:

```
 1. DETECT      Run the system (manual test / endpoint probe / training run / code review)
 2. REPRODUCE   Minimal input that shows the failure, recorded as "Before" result
 3. ROOT CAUSE  Ask "why" until reaching the actual faulty line, not the symptom
                (e.g. BUG-01 symptom "risk = 0" → stub routes → working routes unmounted
                 → schemas.py shadowed by schemas/ package)
 4. FIX         Change the cause, smallest correct change; remove dead duplicates
 5. REGRESSION  Write an automated test that FAILS on the old code and PASSES on the new
                (backend/tests/test_regressions.py, tagged with the BUG id)
 6. VERIFY      Full suite + manual re-test on the live server + record "After" result
```

**Why step 5 matters:** while fixing BUG-15, the new regression test caught BUG-26 — a floating-point error introduced by the fix itself. Without the test, the repair would have shipped a new defect.

### Bug report template (used for each entry in §5)

| Field | Content |
|---|---|
| ID / Title | BUG-xx — one-line summary |
| Severity / Priority | Critical / High / Medium / Low / Cosmetic |
| Environment | OS, Python 3.14, branch, commit |
| Steps to reproduce | Exact request or UI actions |
| Expected result | Per requirement |
| Actual result | Observed output (copied verbatim) |
| Root cause | File + line + explanation |
| Fix | What changed and why |
| Regression test | Test name |
| Status | Open → Fixed → Verified |

---

## 8. Traceability matrix

| Requirement | Manual TC | Automated test(s) | Bugs |
|---|---|---|---|
| Patient risk scoring | TC-05, TC-06, TC-07 | `test_patient_risk_*` | BUG-01, 05 |
| Clinical trial dropout | TC-08 | `test_trial_dropout_*` | BUG-01, 05 |
| Sales forecasting | TC-09 | `test_sales_forecast_*` | BUG-01, 15, 26 |
| Doctor segmentation | TC-10 | `test_doctor_segment_boundaries`, `test_doctor_segments_follow_engagement` | BUG-01, 18 |
| Dataset browsing | TC-11 | `test_patient_list_*`, `test_sales_list_*` | BUG-01 |
| ML model predictions | TC-12 | `test_untrained_model_returns_503`, `test_ml_patient_risk_with_trained_model`, `test_training_package_imports` | BUG-02, 03, 04, 17 |
| Secure document upload | TC-13, TC-UI-02/03 | `test_upload_*` | BUG-07, 23 |
| Authentication | TC-02, 03, 04, 15 | `test_refresh_token_*`, `test_login_rate_limit_returns_429`, `test_every_user_role_has_permissions` | BUG-10, 11, 19, 20 |
| Browser security | TC-14 | `test_cors_*` | BUG-06 |
| MLOps | TC-16 | `test_unknown_mlops_pipeline_returns_404` | BUG-12 |
| AI assistant | TC-17, 18, 19, TC-UI-01 | `test_ai_*`, `test_chunking_keeps_lines`, `test_openai_failure_falls_back_and_stops_retrying` | BUG-27 … 31, 34, 35 |
| Dashboards show the real data | TC-20, TC-21 | `test_overview_matches_datasets`, `test_dashboard_kpis_are_computed`, `test_sales_region_breakdown`, `test_trial_dropout_by_phase`, `test_doctor_segments_use_rule_thresholds`, `test_dataset_changes_are_picked_up_without_restart` | BUG-32, 33 |
| Explainability | (web app, Patient Analytics) | `test_explainability_patient_endpoint`, `test_explainability_unknown_patient_returns_404` | BUG-13, 32 |

---

## 9. Known limitations (not defects in code, but not production-ready)

Monitoring, explainability and all dashboards were placeholders in the first round of repairs; they now use the real data (BUG-32/33). What remains:

- **OpenAI phrasing** needs credit on the configured OpenAI account (it currently returns *429 – no credits*). The assistant works without it; when credit is added and the API restarted, answers are additionally phrased by the model.
- **The AI assistant's question understanding is rule-based** (keywords for domain, metric, grouping and filters). It covers the questions the datasets can answer, but unusual phrasings may fall back to the "no match" help message.
- **Demo users** have passwords hard-coded in `app/utils/security.py`; a real deployment needs a user database with salted hashing (bcrypt/argon2) and a strong `SECRET_KEY` from the environment.
- **Training data is synthetic.** Accuracy figures describe the pipeline's correctness, not real-world clinical performance.
- The frontend bundle is 686 kB (Vite warns above 500 kB); code-splitting would help load time.
