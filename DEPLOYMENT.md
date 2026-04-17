# Deployment Report - Day 12

Student Name: Tran Trung Hau  
Student ID: 2A202600317  
Date: 17/04/2026

---

## 1) Platform

Deployed platforms: Railway and Render (both successful).

- Railway config: 06-lab-complete/railway.toml
- Render config: 06-lab-complete/render.yaml

Current status: Production service is running on Railway and Render.

---

## 2) Public URL

- Railway URL: https://day12-production-1d49.up.railway.app
- Render URL: https://day12-ha-tang-cloud-va-deployment-5ld8.onrender.com/

---

## 3) Environment Variables

Set these variables in the cloud platform dashboard:

- PORT=8000
- ENVIRONMENT=production
- APP_NAME=Production AI Agent
- APP_VERSION=1.0.0
- OPENAI_API_KEY=<secret>
- AGENT_API_KEY=<secret>
- JWT_SECRET=<secret>
- RATE_LIMIT_PER_MINUTE=20
- DAILY_BUDGET_USD=5.0
- REDIS_URL=<platform redis url>
- ALLOWED_ORIGINS=<frontend domain or *>

---

## 4) Deployment Steps

### Railway

```bash
cd 06-lab-complete
railway login
railway init
railway link
railway up
railway domain
```

Executed result:
- Deploy complete
- Healthcheck path /health succeeded
- Service started and accepted requests

### Render

1. Push repository to GitHub.
2. Open Render dashboard.
3. New -> Blueprint.
4. Connect repo and select render.yaml.
5. Set environment variables.
6. Deploy and copy generated URL.

---

## 5) Endpoint Test Checklist (Public)

Executed tests on public domains:

```bash
# Railway - Health
curl https://day12-production-1d49.up.railway.app/health

# Railway - Readiness
curl https://day12-production-1d49.up.railway.app/ready

# Railway - Ask endpoint
curl https://day12-production-1d49.up.railway.app/ask -X POST \
  -H "X-API-Key: <configured-api-key>" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is deployment?"}'

# Render - Health
curl https://day12-ha-tang-cloud-va-deployment-5ld8.onrender.com/health

# Render - Readiness
curl https://day12-ha-tang-cloud-va-deployment-5ld8.onrender.com/ready

# Render - Ask without API key (expected unauthorized)
curl https://day12-ha-tang-cloud-va-deployment-5ld8.onrender.com/ask -X POST \
  -H "Content-Type: application/json" \
  -d '{"question": "What is deployment?"}'
```

Observed results:
- /health -> HTTP 200
- /ready -> HTTP 200
- /ask with valid API key -> HTTP 200
- /ask without API key -> HTTP 401 (security behavior confirmed)

---

## 6) Local Validation Evidence (Already Completed)

- Production checker: 20/20 checks passed.
- Local /health test: HTTP 200.
- Local /ask test with API key: HTTP 200.
- Docker compose stack healthy (agent + redis).

---

## 7) Screenshots Required

Store images in screenshots/:

1. Cloud dashboard showing successful deploy
2. Browser or curl output for /health
3. Browser or curl output for /ask with API key

---

## 8) Final Submission Status

- Deployment report file: Completed
- Cloud configuration: Completed
- Public URL: Completed
- Public endpoint evidence: Completed
- Screenshots: Added in screenshots/ folder
