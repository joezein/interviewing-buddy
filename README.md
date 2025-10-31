# Interview Buddy for Soal Labs

A minimal, opinionated interview companion that helps Soal Labs interviewers run the "Punchy" full-stack engineer framework, capture structured notes, and roll everything into consistent hiring signals. The stack is split into a FastAPI backend, a Next.js frontend, shared Postgres storage, container-friendly packaging, and Terraform IaC for AWS.

## Highlights
- **Hardcoded framework**: The Soal Labs full-stack interview playbook (questions, scenarios, scoring cues, weights) lives in `backend/app/templates/soal_labs_full_stack.py` and seeds every session.
- **Multi-step workflow**: Interviewers spin up sessions, record notes & 0–5 scores for each phase, toggle completion, and write an overall recommendation.
- **Internal auth**: Email/password login with JWTs. First user auto-promoted to admin, subsequent users require an admin token.
- **Postgres persistence**: Users, interview sessions, and per-step notes/scores are stored in Postgres via async SQLAlchemy models.
- **Minimalist UI**: Black-and-white interface inspired by shadcn/Stripe keeps focus on the content; built in Next.js App Router with a simple auth context.
- **Container + IaC ready**: Dockerfiles + Compose for local dev, Terraform (ECS Fargate + RDS + ALBs) for AWS deployment.

## Project Structure

```
backend/           FastAPI service (auth, interviews, templates)
frontend/          Next.js 14 App Router UI
infra/terraform/   AWS infrastructure as code (ECS, RDS, ALB)
docker-compose.yml Local orchestration (backend, frontend, Postgres)
```

### Backend quick tour
- `app/main.py` – FastAPI bootstrap, CORS, startup hook (auto migrations + optional superuser seed).
- `app/models.py` – SQLAlchemy models (`User`, `InterviewSession`, `InterviewStep`).
- `app/templates/` – Hardcoded Soal Labs interview blueprint, exposed via `/interviews/templates`.
- `app/routers/` – Auth (`/auth/login`, `/auth/register`), user admin, interview CRUD.
- `app/auth.py` – Password hashing, JWT issuance, dependency helpers (including optional auth for first-run).

### Frontend quick tour
- `src/app/login` – Internal-only sign-in form.
- `src/app/dashboard` – Launch new interviews, list sessions, framework snapshot.
- `src/app/interviews/[id]` – Step-by-step interview workspace with notes & scoring controls.
- `src/context/AuthContext.tsx` – Token storage, current user hydration, guards.
- `src/lib/api.ts` – Fetch helpers that respect the configured API base.

### Terraform quick tour
- Creates an ECS Fargate cluster (frontend + backend services), dual ALBs, and a Postgres RDS instance.
- Backend runs behind `/api` root path (set by `ROOT_PATH` env). Frontend consumes it via ALB DNS.
- Variables accept pre-existing VPC + subnet IDs so you can drop into existing networking.

## Running locally with Docker Compose

```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env.local  # optional override for dev

docker compose up --build
```

Services:
- API: `http://localhost:8000`
- Frontend: `http://localhost:3000`
- Postgres: `localhost:5432` (user/password `postgres`)

On first boot, create a superuser:

```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@soal.labs","password":"changeme123","full_name":"Admin"}'
```

Subsequent users must include an admin bearer token when calling `/auth/register`.

## Running locally without Docker

### Backend
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # adjust DATABASE_URL if not using docker-compose
uvicorn app.main:app --reload
```

Ensure Postgres is running and accessible via `DATABASE_URL`.

### Frontend
```bash
cd frontend
npm install
cp .env.example .env.local  # sets NEXT_PUBLIC_API_BASE_URL
npm run dev
```

## API overview

All endpoints live under `/` (or `/api` if `ROOT_PATH=/api`):

- `POST /auth/login` – Form-encoded login, returns JWT.
- `POST /auth/register` – Create user (first request open, afterwards admin-only).
- `GET /users/me` – Current user profile.
- `GET /users/` – Admin-only user list.
- `GET /interviews/templates` – Hardcoded Soal Labs framework metadata.
- `POST /interviews/sessions` – Create interview session (auto-seeds steps).
- `GET /interviews/sessions` – Paginated sessions for interviewer (admins see all).
- `GET /interviews/sessions/{id}` – Session detail plus steps.
- `PATCH /interviews/sessions/{id}` – Update status/summary/overall score.
- `PATCH /interviews/sessions/{id}/steps/{step_id}` – Update notes, score, completion for a phase.

## Terraform deployment (AWS)

1. Build & push Docker images to ECR (or any registry) and note the image URIs.
2. Provide VPC + subnet IDs (public for ALBs, private for ECS + RDS) that have internet/NAT access.
3. Populate `terraform.tfvars` (see `terraform.tfvars.example`).
4. Apply:

```bash
cd infra/terraform
terraform init
terraform plan -var-file="terraform.tfvars"
terraform apply -var-file="terraform.tfvars"
```

Outputs include:
- `frontend_endpoint` – ALB DNS for the Next.js app.
- `backend_endpoint` – ALB DNS for the FastAPI API (served under `/api`).
- `database_endpoint` – RDS hostname for migrations/ops.

> ⚠️ **Root path**: In Terraform the backend is configured with `ROOT_PATH=/api` and the frontend consumes `http://<backend-alb>/api`. If you swap load balancers, update these env vars accordingly.

## Security & auth notes
- Passwords hashed with bcrypt (`passlib`).
- JWTs (HS256) expire after 90 minutes by default.
- Admins can toggle user activity and roles.
- Only authenticated users can create/read/update interview data.

## Extensibility ideas
- Add multiple interview templates & RBAC to gate visibility.
- Introduce scoring analytics + weighted summary calculations.
- Build async interview builder UI to edit hardcoded framework.
- Add email notifications or Slack exports per stage.
- Extend Terraform to provision HTTPS certificates (ACM) and Route53 records.

## Troubleshooting
- **Cannot register second user** – include `Authorization: Bearer <admin token>` header.
- **Frontend 401s** – ensure `NEXT_PUBLIC_API_BASE_URL` matches backend (including `/api` when running behind ALB).
- **ECS tasks unhealthy** – check CloudWatch log groups (`/ecs/...-backend` / `...-frontend`) and RDS security group ingress.
- **Local DB schema** – tables are auto-created on FastAPI startup; ensure Postgres is reachable.

---

Made for Soal Labs interviewers to stay punchy, empathetic, and consistent.
