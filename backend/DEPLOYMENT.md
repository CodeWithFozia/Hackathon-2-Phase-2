# Deployment Guide: Hugging Face Spaces

This guide will walk you through deploying the Todo App backend to Hugging Face Spaces.

## Prerequisites

1. A Hugging Face account (sign up at https://huggingface.co)
2. Git installed on your machine
3. A Neon PostgreSQL database (get one free at https://neon.tech)

## Step 1: Prepare Your Space

1. Go to https://huggingface.co/spaces/fouziabibi/todo
2. If the Space doesn't exist, create a new Space:
   - Click "Create new Space"
   - Name: `todo`
   - License: MIT
   - SDK: Docker
   - Make it Public or Private as needed

## Step 2: Set Up Environment Variables

In your Hugging Face Space settings:

1. Go to **Settings** → **Variables and secrets**
2. Add the following secrets:

```
DATABASE_URL=postgresql://neondb_owner:npg_Debr7jpMYk2R@ep-bitter-mode-ah28dkfm-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require
JWT_SECRET=your-super-secret-jwt-key-change-in-production-use-openssl-rand-hex-32
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=15
BCRYPT_ROUNDS=12
DEBUG=false
LOG_LEVEL=info
API_HOST=0.0.0.0
API_PORT=7860
```

**IMPORTANT**:
- Generate a strong JWT_SECRET using: `openssl rand -hex 32`
- Use your actual Neon database URL
- Never commit these secrets to Git

## Step 3: Deploy to Hugging Face Spaces

### Option A: Using Git (Recommended)

```bash
# Navigate to your backend directory
cd backend

# Initialize git if not already done
git init

# Add Hugging Face Space as remote
git remote add space https://huggingface.co/spaces/fouziabibi/todo

# Copy the Space README
cp SPACE_README.md README.md

# Add all files
git add .

# Commit
git commit -m "Initial deployment of Todo API backend"

# Push to Hugging Face Space
git push space main
```

### Option B: Using Hugging Face Web Interface

1. Go to your Space: https://huggingface.co/spaces/fouziabibi/todo
2. Click on **Files** → **Add file** → **Upload files**
3. Upload all files from the `backend` directory:
   - `Dockerfile`
   - `requirements.txt`
   - `src/` directory (all files)
   - `.dockerignore`
   - `README.md` (use SPACE_README.md content)
   - `alembic/` directory (if using migrations)

4. Make sure the README.md has the proper frontmatter at the top:
```yaml
---
title: Todo API Backend
emoji: 📝
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
app_port: 7860
---
```

## Step 4: Verify Deployment

1. Wait for the Space to build (this may take 5-10 minutes)
2. Check the build logs in the Space interface
3. Once deployed, test the endpoints:

```bash
# Health check
curl https://fouziabibi-todo.hf.space/health

# API documentation
# Visit: https://fouziabibi-todo.hf.space/docs
```

## Step 5: Update Frontend Configuration

Update your frontend `.env.local` to point to the deployed backend:

```bash
NEXT_PUBLIC_API_URL=https://fouziabibi-todo.hf.space
```

## Troubleshooting

### Build Fails

1. Check the build logs in the Space interface
2. Verify all dependencies are in `requirements.txt`
3. Ensure Dockerfile is correct
4. Check that environment variables are set

### Database Connection Issues

1. Verify DATABASE_URL is correct in Space settings
2. Check that Neon database is accessible
3. Ensure SSL mode is set correctly: `?sslmode=require`
4. Check Neon database logs

### CORS Errors

1. Verify frontend URL is in the CORS origins list in `src/main.py`
2. Check that `allow_credentials=True` is set
3. Ensure frontend is sending requests with proper headers

### Port Issues

1. Hugging Face Spaces uses port 7860 by default
2. Verify `app_port: 7860` in README.md frontmatter
3. Check Dockerfile exposes port 7860
4. Ensure uvicorn runs on port 7860

## Monitoring

### View Logs

1. Go to your Space
2. Click on **Logs** tab
3. Monitor real-time application logs

### Check Health

```bash
curl https://fouziabibi-todo.hf.space/health
```

Expected response:
```json
{"status":"healthy"}
```

## Updating the Deployment

To update your deployed backend:

```bash
# Make your changes
# Commit them
git add .
git commit -m "Update: description of changes"

# Push to Hugging Face Space
git push space main
```

The Space will automatically rebuild and redeploy.

## Security Best Practices

1. ✅ Use strong JWT_SECRET (32+ characters, random)
2. ✅ Never commit secrets to Git
3. ✅ Use environment variables for all sensitive data
4. ✅ Enable SSL for database connections
5. ✅ Set DEBUG=false in production
6. ✅ Restrict CORS origins to your frontend URL only
7. ✅ Use HTTPS for all API requests
8. ✅ Implement rate limiting (future enhancement)

## Next Steps

1. Test all API endpoints using the Swagger UI
2. Update frontend to use the deployed backend URL
3. Deploy frontend to Hugging Face Spaces or Vercel
4. Set up monitoring and alerts
5. Consider adding rate limiting
6. Implement API key authentication for additional security

## Support

- Hugging Face Spaces Documentation: https://huggingface.co/docs/hub/spaces
- FastAPI Documentation: https://fastapi.tiangolo.com
- Neon Documentation: https://neon.tech/docs

---

🎉 Your Todo App backend is now deployed on Hugging Face Spaces!
