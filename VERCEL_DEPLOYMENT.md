# Vercel Deployment Configuration

This project deploys the Next.js frontend from the `full_stack_todo_frontend` directory.

## Quick Deploy to Vercel

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/CodeWithFozia/Hackathon-2-Phase-2&project-name=hackathon-2-phase-2&root-directory=full_stack_todo_frontend&env=NEXT_PUBLIC_API_URL&envDescription=Backend%20API%20URL&envLink=https://fouziabibi-todo.hf.space)

## Manual Deployment Steps

### 1. Import Project to Vercel

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click **"Add New..."** → **"Project"**
3. Import: `CodeWithFozia/Hackathon-2-Phase-2`

### 2. Configure Build Settings

**IMPORTANT:** Set these exact values:

```
Root Directory: full_stack_todo_frontend
Framework Preset: Next.js
Build Command: npm run build
Output Directory: .next
Install Command: npm install
```

### 3. Environment Variables

Add this environment variable:

```
NEXT_PUBLIC_API_URL=https://fouziabibi-todo.hf.space
```

### 4. Deploy

Click **"Deploy"** and wait for the build to complete.

## Troubleshooting 404 Error

If you see a 404 error, the most common cause is:

**❌ Wrong Root Directory**
- Vercel is trying to deploy from the repository root
- The Next.js app is in `full_stack_todo_frontend` subdirectory

**✅ Fix:**
1. Go to your Vercel project settings
2. Navigate to **Settings** → **General**
3. Find **Root Directory**
4. Set it to: `full_stack_todo_frontend`
5. Save and redeploy

## Current Deployment

- **Frontend URL:** https://hackathon-2-phase-2-neyo.vercel.app/
- **Backend API:** https://fouziabibi-todo.hf.space
- **GitHub Repo:** https://github.com/CodeWithFozia/Hackathon-2-Phase-2

## Project Structure

```
Hackathon-2-Phase-2/
├── backend/                    # FastAPI backend (deployed to HF Spaces)
├── full_stack_todo_frontend/   # Next.js frontend (deploy THIS to Vercel)
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── next.config.ts
├── frontend/                   # Old frontend (ignore)
└── vercel.json                 # Root config (points to subdirectory)
```

## Verification

After deployment, test these URLs:

- Homepage: https://hackathon-2-phase-2-neyo.vercel.app/
- Sign Up: https://hackathon-2-phase-2-neyo.vercel.app/signup
- Sign In: https://hackathon-2-phase-2-neyo.vercel.app/signin
- Tasks: https://hackathon-2-phase-2-neyo.vercel.app/tasks
