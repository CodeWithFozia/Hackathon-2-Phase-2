---
title: Todo API Backend
emoji: 📝
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
app_port: 7860
---

# Todo App Backend API

FastAPI backend for the Todo application with JWT authentication and task management.

## 🚀 Live API

- **API Base URL**: https://fouziabibi-todo.hf.space
- **API Documentation**: https://fouziabibi-todo.hf.space/docs
- **Health Check**: https://fouziabibi-todo.hf.space/health

## Features

- 🔐 JWT-based authentication (signup/signin)
- ✅ Full CRUD operations for tasks
- 👤 User isolation (users can only access their own tasks)
- 📄 Pagination support
- 🗄️ PostgreSQL database (Neon Serverless)
- 🚀 FastAPI with automatic API documentation

## API Endpoints

### Authentication
- `POST /auth/signup` - Register a new user
- `POST /auth/signin` - Authenticate user

### Tasks (Requires Authentication)
- `GET /users/{user_id}/tasks` - List all tasks (paginated)
- `POST /users/{user_id}/tasks` - Create a new task
- `GET /users/{user_id}/tasks/{task_id}` - Get a specific task
- `PUT /users/{user_id}/tasks/{task_id}` - Update a task
- `PATCH /users/{user_id}/tasks/{task_id}` - Partially update a task
- `DELETE /users/{user_id}/tasks/{task_id}` - Delete a task

### Health Check
- `GET /health` - Check API health status

## Quick Start

### Example: Create a User

```bash
curl -X POST "https://fouziabibi-todo.hf.space/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"securepassword"}'
```

### Example: Sign In

```bash
curl -X POST "https://fouziabibi-todo.hf.space/auth/signin" \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"securepassword"}'
```

### Example: Create a Task

```bash
curl -X POST "https://fouziabibi-todo.hf.space/users/{user_id}/tasks" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{"title":"Buy groceries","description":"Milk, eggs, bread"}'
```

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL (Neon Serverless)
- **ORM**: SQLModel
- **Authentication**: JWT with bcrypt password hashing
- **Validation**: Pydantic v2
- **Deployment**: Docker on Hugging Face Spaces

## Environment Variables

The following environment variables are configured in the Space settings:

- `DATABASE_URL` - PostgreSQL connection string
- `JWT_SECRET` - Secret key for JWT token generation
- `JWT_ALGORITHM` - Algorithm for JWT (HS256)
- `JWT_EXPIRATION_MINUTES` - Token expiration time
- `BCRYPT_ROUNDS` - Bcrypt hashing rounds
- `DEBUG` - Debug mode (false in production)
- `LOG_LEVEL` - Logging level (info)

## CORS Configuration

The API accepts requests from:
- Local development: `http://localhost:3000`, `http://localhost:3001`
- Hugging Face Spaces frontend
- All origins (for testing - should be restricted in production)

## Database

This backend uses **Neon Serverless PostgreSQL**. The database tables are automatically created on startup using SQLModel.

### Database Schema

**Users Table:**
- `id` (UUID, Primary Key)
- `email` (String, Unique)
- `password_hash` (String)
- `created_at` (DateTime)
- `updated_at` (DateTime)

**Tasks Table:**
- `id` (UUID, Primary Key)
- `user_id` (UUID, Foreign Key)
- `title` (String, max 255 chars)
- `description` (String, optional)
- `is_completed` (Boolean)
- `created_at` (DateTime)
- `updated_at` (DateTime)

## Local Development

```bash
# Clone the repository
git clone https://huggingface.co/spaces/fouziabibi/todo
cd todo

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Run the server
python -m uvicorn src.main:app --reload --port 8001
```

## License

MIT

---

Built with ❤️ using FastAPI and deployed on Hugging Face Spaces
