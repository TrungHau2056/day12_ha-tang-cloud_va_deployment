# Day 12 Delivery Checklist - Final Submission Status

Student Name: Tran Trung Hau  
Student ID: 2A202600317  
Date: 17/04/2026

---

## 1) Overall Status

- Current verified progress from workspace: In progress
- Completed core production code: Yes
- Missing mandatory submission files: No
- Estimated completion if submit now: 95/100 (cloud deploy completed, screenshots and repo access check pending)

---

## 2) Deliverable Checklist

### A. Mission Answers (40 points)

- [x] MISSION_ANSWERS.md exists
- [x] Answered all parts 1 -> 5
- [x] Included command outputs and explanations

Current state:
- File MISSION_ANSWERS.md created at repository root.

### B. Full Source Code - Lab 06 Complete (60 points)

- [x] 06-lab-complete/app/main.py
- [x] 06-lab-complete/app/config.py
- [x] 06-lab-complete/app/auth.py
- [x] 06-lab-complete/app/rate_limiter.py
- [x] 06-lab-complete/app/cost_guard.py
- [x] utils/mock_llm.py
- [x] 06-lab-complete/Dockerfile
- [x] 06-lab-complete/docker-compose.yml
- [x] 06-lab-complete/requirements.txt
- [x] 06-lab-complete/.env.example
- [x] 06-lab-complete/.dockerignore
- [x] 06-lab-complete/railway.toml
- [x] 06-lab-complete/render.yaml
- [x] 06-lab-complete/README.md

Feature verification notes:
- [x] Multi-stage Dockerfile present
- [x] API key authentication implemented
- [x] Rate limiting implemented
- [x] Cost guard implemented
- [x] Health and readiness checks present
- [x] Graceful shutdown logic present
- [x] Stateless-ready compose stack present (agent + redis)
- [x] .env.example and .dockerignore present

Runtime evidence already recorded:
- [x] python check_production_ready.py -> 20/20 checks passed
- [x] GET /health -> 200
- [x] POST /ask with X-API-Key -> 200
- [x] docker compose ps -> agent and redis healthy

### C. Service Domain Link / Cloud Deployment

- [x] DEPLOYMENT.md exists
- [x] Public URL added
- [x] Platform added (Railway or Render or Cloud Run)
- [x] Public endpoint tests documented
- [x] Environment variables documented
- [x] Screenshots attached

Current state:
- DEPLOYMENT.md created at repository root.
- Public URL deployed on Railway: https://day12-production-1d49.up.railway.app
- Public URL deployed on Render: https://day12-ha-tang-cloud-va-deployment-5ld8.onrender.com/
- screenshots/ folder contains deployment and endpoint evidence images.

---

## 3) Pre-Submission Gate

- [ ] Repository is public or instructor has access
- [x] MISSION_ANSWERS.md completed
- [x] DEPLOYMENT.md completed with working public URL
- [x] Source code organized in 06-lab-complete/app/
- [x] README exists with setup instructions
- [x] No hardcoded secrets (based on checker result)
- [x] Public URL reachable from outside local network
- [x] Screenshots included
- [ ] Commit history cleaned and readable

---

## 4) Verification Commands (Windows PowerShell)

```powershell
docker compose up -d --force-recreate

Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing

$line = Get-Content ".env.local" | Where-Object { $_ -match '^AGENT_API_KEY=' } | Select-Object -First 1
$apiKey = ($line -split '=',2)[1].Trim().Trim('"')
Invoke-WebRequest -Uri "http://localhost:8000/ask" -Method Post `
  -Headers @{ "X-API-Key" = $apiKey } `
  -ContentType "application/json" `
  -Body '{"question":"What is deployment?"}' -UseBasicParsing

python .\check_production_ready.py
docker compose ps
```

---

## 5) Immediate Actions To Finish Submission

1. Set repository visibility/access for instructor.
2. Push latest commit history and perform final submission check.

---

## 6) Supporting Files Created

- MISSION_ANSWERS.md created and filled.
- DEPLOYMENT.md created and filled with working public URL.
- screenshots/README.md created with screenshot naming guide.
