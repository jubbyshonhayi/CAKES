# CAKES - Multi-tenant Student Management System

This repository now contains a Django-based Student Management System designed for **strict school-level tenant isolation**.

## Stack
- **Backend**: Django (class-based views + Django auth)
- **Frontend**: Django templates (HTML/CSS)
- **Development DB**: SQLite
- **Production-ready path**: PostgreSQL-compatible schema and query design

## Architecture Decisions

### 1) Multi-tenant isolation strategy
- Each `School` is a tenant.
- Every school user is linked to exactly one school (`accounts.User.school`).
- Every `Student` row is linked to a `School` (`students.Student.school`).
- All student reads are scoped through `Student.objects.for_user(request.user)` to enforce tenant filtering at the query level.
- Student CRUD views use `get_queryset()` with tenant scoping, which blocks IDOR attempts on object detail/update/delete.

### 2) Role model
- **Superuser/Admin**
  - Manages schools and users via Django admin.
  - Cannot manage students directly (student model intentionally not registered in admin).
- **School user**
  - Authenticated via Django auth.
  - Full CRUD access only for students in their own school.

### 3) Authorization approach
- Route/view-level guard: `SchoolUserRequiredMixin` blocks access unless user is an active school user.
- Query-level guard: `StudentQuerySet.for_user()` always filters by `school_id`.
- Model-level data integrity:
  - Unique constraints per school (`email`, `enrollment_number`).
  - Foreign keys with relational integrity.

### 4) Scalability choices
- Composite indexes on student table by `(school, last_name, first_name)`, `(school, enrollment_number)`, `(school, email)`.
- Narrow, indexed foreign keys (`school_id`) for high-cardinality tenant partitions.
- Avoided hard-coded school IDs; everything derives from authenticated user context.
- Pagination enabled for student list.

## Project Structure
- `sms_project/` – Django project config (`settings.py`, `urls.py`)
- `schools/` – Tenant model and admin management
- `accounts/` – Custom user model linked to school
- `students/` – Student domain models, forms, CBV CRUD, tenant enforcement
- `templates/` – Shared and student UI templates

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Migration notes: SQLite -> PostgreSQL
1. Install driver: `pip install psycopg[binary]` (or `psycopg2-binary`).
2. Update `DATABASES` in `sms_project/settings.py` to `django.db.backends.postgresql`.
3. Provide credentials via environment variables.
4. Run `python manage.py migrate` against PostgreSQL.
5. Keep existing indexes/constraints; they are fully compatible and important for tenant-scoped performance.
6. For very large scale:
   - add read replicas,
   - consider table partitioning by `school_id`,
   - add caching for repeated school-scoped list queries,
   - use background workers for heavy imports/exports.

## Admin workflow
- Admin logs into `/admin/`.
- Creates/updates schools.
- Creates users and assigns each non-superuser to one school.
- School users log in at `/accounts/login/` and manage students in their own tenant scope only.
