# Variables Used in Login and Auth System

## frontend/templates/login.html
- email (form input name)
- password (form input name)

## backend/routes/auth.py
- email (form parameter)
- password (form parameter)
- user (authenticated user object)
- user_email (session variable)
- message (error message)
- request (FastAPI request object)
- db (database session)
- BASE_DIR (path to backend directory)
- FRONTEND_DIR (path to frontend directory)
- templates (Jinja2 templates object)

## backend/services/auth_service.py
- db (database session)
- email (user email)
- password (user password)
- user (user object)
- session_id (session identifier)
- request (FastAPI request object)

## backend/models.py (User model related , stored in database)
- id (user ID)
- email (user email)
- password (user password)
- role (user role, default "student")
- reported_items (relationship to items reported by user)
- claims (relationship to claims made by user)
  
