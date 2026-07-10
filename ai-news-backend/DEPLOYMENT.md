# EntropyGate AI — Production Deployment Guide

**Version:** O1
**Date:** 2026-07-08

---

## Architecture

```
Internet
   │
   ▼
Nginx (reverse proxy, rate limiting, HTTPS)
   │
   ▼
FastAPI (api:8000)       Celery Worker       Celery Beat
   │                          │                   │
   ├── SQLite/PostgreSQL      ├── Redis           └── Redis
   ├── Redis                                              
   └── Disk (backups, logs, uploads)
```

---

## Prerequisites

- Docker 24+ & Docker Compose v2
- 2GB RAM, 10GB disk minimum
- Domain name (for HTTPS)

---

## Quick Start

```bash
# 1. Clone & configure
cp .env.production .env
# Edit .env: set SECRET_KEY, LLM_API_KEY, CORS_ORIGINS

# 2. Start
docker compose -f docker-compose.prod.yml up -d

# 3. Verify
curl http://localhost:8000/health
python scripts/health_check.py --verbose

# 4. Stop
docker compose -f docker-compose.prod.yml down
```

---

## HTTPS Setup

```bash
# Using Let's Encrypt
certbot certonly --standalone -d entropygate.ai -d api.entropygate.ai

# Copy certs
cp /etc/letsencrypt/live/entropygate.ai/fullchain.pem certs/
cp /etc/letsencrypt/live/entropygate.ai/privkey.pem certs/

# Uncomment HTTPS section in nginx.conf, then:
docker compose -f docker-compose.prod.yml restart nginx
```

---

## Backup & Restore

### Automatic
```bash
# Daily backup via backup service (docker-compose.prod.yml)
# Or manually:
python backup.py
```

### Restore
```bash
python backup.py --restore backups/ainews_20260708_120000.db
```

### Rollback
```bash
# Rollback code
git checkout <previous-tag>
docker compose -f docker-compose.prod.yml up -d --build

# Rollback DB
python backup.py --restore <backup-file>
```

---

## Monitoring

### Health Check
```bash
python scripts/health_check.py --verbose   # Human readable
python scripts/health_check.py --json      # Machine readable (exit code 0/1/2)
```

### What to monitor
| Metric | Tool | Alert if |
|--------|------|----------|
| Disk free | health_check.py | < 1GB |
| DB size | health_check.py | > 500MB |
| Backup age | health_check.py | > 1 day |
| Memory | health_check.py | > 80% |
| API response | /health endpoint | !200 |
| Worker ping | celery inspect | timeout |

---

## CI Validation

```bash
# Pre-deploy validation (run on every PR)
python scripts/ci_validate.py       # Golden replay + drift check
python scripts/verify_e2.py         # Projection library
python scripts/verify_e3.py         # Knowledge graph
python scripts/verify_e4.py         # Intelligence feeds
python scripts/verify_e5.py         # API + SDK
python scripts/health_check.py      # System health

# All must exit 0
```

---

## Production Checklist

- [ ] .env configured with production secrets
- [ ] HTTPS certs installed
- [ ] CORS origins restricted
- [ ] Rate limiting enabled
- [ ] Log rotation configured (max 50MB x 3 files)
- [ ] Backup service running
- [ ] Health check passing
- [ ] CI validation passing
- [ ] Golden replay passing
- [ ] Monitoring alerts configured

---

## Emergency Contacts

- Runtime Owner: Core Team
- Architecture Board: arch@ai-kos.dev
- Security: security@ai-kos.dev
