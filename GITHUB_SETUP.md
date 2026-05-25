# 🚀 Pushing OpenScholar to GitHub

This guide walks you through pushing the project to a **new** GitHub repo at https://github.com/Gnaneswar99/openscholar.

---

## Step 1 — Create the GitHub repo

1. Go to https://github.com/new
2. Fill in:
   - **Repository name:** `openscholar`
   - **Description:** `Autonomous multi-agent research platform built with FastAPI, Next.js 14, LangGraph, and Anthropic Claude.`
   - **Visibility:** **Public** ⬅ important for portfolio
   - **❌ DO NOT** check "Add a README file"
   - **❌ DO NOT** add a `.gitignore`
   - **❌ DO NOT** add a license
3. Click **"Create repository"**

> The project already has all three of these files. Adding them on GitHub creates merge conflicts on first push.

---

## Step 2 — Extract the zip and open a terminal

1. Extract `openscholar.zip` somewhere clean — e.g., `C:\Users\gnane\Projects\openscholar`
2. Open **PowerShell**
3. Navigate into the extracted folder:

```powershell
cd C:\Users\gnane\Projects\openscholar
```

4. Verify you see these files/folders:

```powershell
ls
```

Expected output: `backend/`, `frontend/`, `docker-compose.yml`, `README.md`, `.env.example`, `LICENSE`, `.github/`

---

## Step 3 — Configure Git (one time only)

If you've never configured Git on this machine:

```powershell
git config --global user.name "Gnaneswar99"
git config --global user.email "your-github-email@example.com"
```

Use the **same email** that's on your GitHub account.

---

## Step 4 — Initialize Git, commit, push

Run these one at a time:

```powershell
git init
git branch -M main
git add .
git status
```

`git status` should show ~50 files staged. If `node_modules/`, `.venv/`, or `.env` show up, **stop** and check that `.gitignore` is in place.

```powershell
git commit -m "feat: Phase 1 - OpenScholar foundation (FastAPI + Next.js + Docker)"
git remote add origin https://github.com/Gnaneswar99/openscholar.git
git push -u origin main
```

---

## Step 5 — When Git asks for credentials

- **Username:** `Gnaneswar99`
- **Password:** ⚠️ **Not your GitHub password — your Personal Access Token (PAT)**

### How to get a PAT (do this before pushing):

1. Open https://github.com/settings/tokens
2. Click **"Generate new token"** → **"Generate new token (classic)"**
3. Settings:
   - **Note:** `cli-push-openscholar`
   - **Expiration:** `90 days`
   - **Scopes:** ✅ check **`repo`** (full control of private repos)
4. Click **"Generate token"** at the bottom
5. **COPY the token immediately** (starts with `ghp_...`) — you only see it once
6. When the terminal asks for password, **paste the token**

> Pasted passwords don't appear on screen in PowerShell. That's normal — just paste and hit Enter.

---

## Step 6 — Verify

Open https://github.com/Gnaneswar99/openscholar — you should see all files, and the README should render beautifully with badges, Mermaid diagrams, and the table of contents.

---

## After pushing — make the repo shine

### 1. Add description and topics on the repo page

Click ⚙ next to "About" on the right side of the repo page:
- **Description:** "Autonomous multi-agent research platform built with FastAPI, Next.js 14, LangGraph, and Anthropic Claude."
- **Topics:** `ai-agent`, `multi-agent`, `langgraph`, `anthropic`, `claude`, `fastapi`, `nextjs`, `typescript`, `rag`, `python`, `docker`

### 2. Pin the repo to your profile

Profile → Customize your pins → tick `openscholar`.

### 3. Personalize the LICENSE

Edit `LICENSE` and replace `Gnaneswar` with your full real name. Same for `README.md` author section if needed. Then:
```powershell
git add LICENSE README.md
git commit -m "docs: update author info"
git push
```

### 4. Wait for CI to pass

Open https://github.com/Gnaneswar99/openscholar/actions — backend CI, frontend CI, and CodeQL should all run automatically. Each green checkmark adds credibility.

---

## Troubleshooting

**`fatal: remote origin already exists`**
```powershell
git remote remove origin
git remote add origin https://github.com/Gnaneswar99/openscholar.git
```

**`Updates were rejected because the remote contains work that you do not have`**
You accidentally added a README/license to the GitHub side. Easiest fix: delete the GitHub repo (Settings → Danger Zone) and re-create it empty.

**`Support for password authentication was removed`**
You used your GitHub password. Use a Personal Access Token instead (Step 5).

**File too large**
Run `git rm -r --cached node_modules .venv __pycache__` before re-committing.

---

## Next step after pushing

Reply to me with:
> "Pushed: https://github.com/Gnaneswar99/openscholar — do Phase 2"

And I'll build the **single-agent research MVP** — Tavily web search + Claude → the first version where you ask a real question and get back a real, cited answer.
