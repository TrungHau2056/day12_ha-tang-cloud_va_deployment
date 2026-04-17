# Mission Answers - Day 12

Student Name: Tran Trung Hau  
Student ID: 2A202600317  
Date: 17/04/2026

---

## Mission 1 - Localhost vs Production

### 1.1 Anti-patterns found in basic version
Source inspected: 01-localhost-vs-production/develop/app.py

1. Hardcoded OPENAI key in source code.
2. Hardcoded DATABASE_URL with username/password.
3. Debug mode enabled by default.
4. No health endpoint for liveness probe.
5. Host bound to localhost only (not container/cloud friendly).
6. Port fixed to 8000 (not from env).
7. Logs secrets via print statement.

### 1.2 Why advanced version is production-ready
Source inspected: 01-localhost-vs-production/production/app.py

- Uses environment variables for config.
- Has structured logging instead of plain prints.
- Adds /health and /ready endpoints.
- Handles SIGTERM for graceful shutdown.
- Binds host to 0.0.0.0 and reads port from env.

### 1.3 Commands and observed results
```powershell
cd 01-localhost-vs-production/develop
pip install -r requirements.txt
python app.py
```
Result: Basic endpoint works locally, but has multiple production anti-patterns listed above.

---

## Mission 2 - Docker Containerization

### 2.1 Basic Dockerfile understanding
Source inspected: 02-docker/develop/Dockerfile

- Base image: python:3.11
- Working directory: /app
- requirements copied first to maximize Docker layer cache reuse.
- CMD defines runtime command when container starts.

### 2.2 Multi-stage build benefits
Source inspected: 02-docker/production/Dockerfile

- Stage builder installs dependencies and build tools.
- Stage runtime copies only runtime artifacts.
- Final image is smaller, cleaner, and safer.
- Runs as non-root user (security best practice).
- Includes HEALTHCHECK instruction.

### 2.3 Docker Compose architecture
Source inspected: 02-docker/production/docker-compose.yml

Stack components:
1. agent (FastAPI)
2. redis (cache/rate data)
3. qdrant (vector store)
4. nginx (reverse proxy/load balancer)

Observed outcome: Compose provides full service orchestration and health-based startup order.

---

## Mission 3 - Cloud Deployment

### 3.1 Deployment assets prepared
- Railway config available: 03-cloud-deployment/railway/railway.toml
- Render config available: 03-cloud-deployment/render/render.yaml
- Lab complete configs available:
  - 06-lab-complete/railway.toml
  - 06-lab-complete/render.yaml

### 3.2 Environment variables strategy
Configured via platform dashboard/CLI, not hardcoded in source:
- PORT
- ENVIRONMENT
- OPENAI_API_KEY
- AGENT_API_KEY
- JWT_SECRET
- RATE_LIMIT_PER_MINUTE
- DAILY_BUDGET_USD
- REDIS_URL

### 3.3 Public deployment test
Current status: Pending final cloud push from student account.

- Public URL: TBD
- Public health test: TBD
- Public ask test: TBD

---

## Mission 4 - API Security

### 4.1 Authentication implementation
Source inspected: 06-lab-complete/app/auth.py and 06-lab-complete/app/main.py

- API key is required in X-API-Key header.
- Missing/invalid key returns HTTP 401.

### 4.2 Rate limiting implementation
Source inspected: 06-lab-complete/app/main.py and 06-lab-complete/app/rate_limiter.py

- Request rate is bounded per bucket window.
- Exceeding limit returns HTTP 429 with Retry-After.

### 4.3 Cost guard implementation
Source inspected: 06-lab-complete/app/main.py and 06-lab-complete/app/cost_guard.py

- Tracks token cost and enforces daily budget.
- Exceeding budget returns HTTP 503.

### 4.4 Local test evidence (recorded)
- GET /health -> 200
- POST /ask with valid X-API-Key -> 200
- Production checker -> 20/20 passed

---

## Mission 5 - Scaling and Reliability

### 5.1 Health and readiness probes
Source inspected: 06-lab-complete/app/main.py

- /health for liveness.
- /ready for readiness routing control.

### 5.2 Graceful shutdown
- SIGTERM handler is registered.
- Uvicorn configured with timeout_graceful_shutdown=30.

### 5.3 Stateless and scale-ready design
- Redis service defined in compose stack.
- App can run with multiple workers.
- Deployment config supports restart policy and health checks.

### 5.4 Validation evidence
```powershell
cd 06-lab-complete
python .\check_production_ready.py
```
Recorded result: 20/20 checks passed (100%).

---

## Final Reflection

- Biggest challenge: Converting localhost assumptions into cloud-safe config and runtime behavior.
- What I learned: 12-factor config, container hardening, API protection, and reliability probes.
- Next improvement: Complete public cloud deployment report with URL and screenshots.
