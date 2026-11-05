# THREADS_AI_CORE // Serverless GitHub Automation Suite

A production-ready **Instagram Threads Auto-Posting and Monitoring Web Application** built **ONLY using the GitHub Ecosystem**:
- **Backend Automation:** Pure **GitHub Actions** cron workflow (`0 * * * *`) running Python 3.11 with **Google Gemini AI** and the official **Meta Threads Graph API**.
- **Frontend Hosting:** 100% Free & Serverless **GitHub Pages** static dashboard with Apple Dark aesthetic and a **Stealth Security Gateway**.

---

## 🏗️ System Architecture

```
┌────────────────────────────────────────────────────────┐
│                   Google AI Studio                     │
│               Gemini AI (gemini-2.5-flash)             │
│   Strict Character Constraint: 300 - 350 Characters    │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│              GitHub Actions Cron Workflow              │
│               (.github/workflows/auto_post.yml)        │
│  - Scheduled: Every 1 Hour (0 * * * *)                 │
│  - Executes: python script.py                          │
│  - Step A: Create Threads Container                    │
│  - Step B: Publish Threads Container                   │
│  - Persistence: Commits updated posts_log.json         │
└─────────────┬────────────────────────────┬─────────────┘
              │                            │
              ▼                            ▼
┌───────────────────────────┐ ┌──────────────────────────┐
│  Meta Threads Graph API   │ │       GitHub Pages       │
│  - Free 250 Posts / Day   │ │       (index.html)       │
│  - Health & Wellness Niche│ │  - Apple Glassmorphism   │
│  - 2-Step Container Pub   │ │  - Stealth 3-Try Shield  │
│                           │ │  - Live JSON Log Parser  │
│                           │ │  - 300-350 Range Badges  │
└───────────────────────────┘ └──────────────────────────┘
```

---

## 📦 Project Structure

```
.
├── .github/
│   └── workflows/
│       └── auto_post.yml   # Hourly GitHub Actions cron & commit pipeline
├── index.html              # Apple-inspired static dashboard for GitHub Pages
├── script.py               # Gemini AI generation & Threads Graph API publisher
├── posts_log.json          # Structured historical dispatch log store
├── requirements.txt        # Python dependencies (google-genai, requests)
└── README.md               # Setup and configuration guide
```

---

## 🚀 Step-by-Step Setup Guide

### 1. Push Repository to GitHub
If you haven't pushed this project to GitHub yet, run:
```bash
git init
git add .
git commit -m "feat: initial commit for threads github automation"
git branch -M main
git remote add origin https://github.com/<YOUR-USERNAME>/<YOUR-REPO-NAME>.git
git push -u origin main
```

---

### 2. Configure GitHub Repository Secrets
GitHub Actions securely accesses your API credentials via Secrets:
1. Go to your repository on GitHub.
2. Click **Settings** (tab at top).
3. In the left sidebar, navigate to **Secrets and variables** ➔ **Actions**.
4. Click the green button **"New repository secret"** and add the following 3 secrets:

| Secret Name | Value Description |
| :--- | :--- |
| `GEMINI_API_KEY` | Your Google Gemini API Key (`AQ.Ab8RN6I59...`) |
| `THREADS_ACCESS_TOKEN` | Your Meta Threads Graph API Long-Lived Token |
| `THREADS_USER_ID` | Your Threads User ID (`29410042778679242`) |
| `GEMINI_MODEL` *(Optional)* | Default: `gemini-2.5-flash` (auto-falls back to `gemini-3.8-flash`) |

---

### 3. Enable GitHub Actions Write Permissions (Crucial Step!)
The GitHub Actions bot needs permission to commit `posts_log.json` back to your repo:
1. In your repository on GitHub, go to **Settings** ➔ **Actions** ➔ **General**.
2. Scroll down to **"Workflow permissions"**.
3. Select **"Read and write permissions"**.
4. Check the box **"Allow GitHub Actions to create and approve pull requests"**.
5. Click **Save**.

---

### 4. Enable GitHub Pages Hosting
1. Go to **Settings** ➔ **Pages** in your repository.
2. Under **"Build and deployment"** ➔ **Source**, select **"Deploy from a branch"**.
3. Under **Branch**, select **`main`** and folder **`/ (root)`**.
4. Click **Save**.
5. After 1–2 minutes, your live dashboard will be accessible at:
   👉 `https://<YOUR-USERNAME>.github.io/<YOUR-REPO-NAME>/`

---

### 5. Stealth Security Gateway (Secret Access)
When opening your GitHub Pages dashboard, a client-side Apple-style security gateway will greet you:
- **Secret Email:** `1`
- **Secret Password:** ` ` *(Single space character)*

> **🔒 Unlock Mechanism:**
> 1. Enter `1` and a single space ` `, then click **Authenticate Access**.
> 2. Attempts 1 and 2 will show a generic message: *"Invalid email or password format."*
> 3. On the **exact 3rd consecutive attempt**, the shield unlocks and reveals the live monitoring dashboard!
> 4. Click **"Lock Session ⎋"** in the header to re-lock the portal at any time.

---

### 6. Manual Testing (Workflow Dispatch)
You don't have to wait 1 hour to test the first post:
1. In your GitHub repository, click the **Actions** tab.
2. In the left sidebar, click **Instagram Threads Auto-Poster**.
3. Click the **Run workflow** dropdown on the right and click **Run workflow**.
4. Watch the workflow execute in ~20 seconds:
   - Gemini AI generates the 300–350 char wellness insight.
   - Meta Threads Graph API publishes it.
   - `posts_log.json` is updated and committed automatically.
5. Visit your GitHub Pages dashboard to view the new live entry!
