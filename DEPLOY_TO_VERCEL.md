# 🚀 Deploy Todo App to Vercel - Simple Guide

## Your Project URLs
- **GitHub Repo:** https://github.com/CodeWithFozia/Hackathon-2-Phase-2
- **Backend API (Live):** https://fouziabibi-todo.hf.space ✅
- **Frontend (To Deploy):** https://hackathon-2-phase-2-neyo.vercel.app/

---

## 📋 Step-by-Step Deployment

### Step 1: Go to Vercel Dashboard
Open this link: **https://vercel.com/new**

### Step 2: Import Your GitHub Repository

1. Click **"Import Git Repository"**
2. If you don't see your repo, click **"Adjust GitHub App Permissions"**
3. Select repository: **CodeWithFozia/Hackathon-2-Phase-2**
4. Click **"Import"**

### Step 3: Configure Project Settings

**CRITICAL: Set these EXACT values:**

```
Project Name: hackathon-2-phase-2-neyo
Framework Preset: Next.js
Root Directory: full_stack_todo_frontend    ⚠️ MUST SET THIS!
```

**Build & Development Settings:**
```
Build Command: npm run build
Output Directory: .next
Install Command: npm install
Development Command: npm run dev
```

### Step 4: Add Environment Variable

Click **"Environment Variables"** section:

```
Name: NEXT_PUBLIC_API_URL
Value: https://fouziabibi-todo.hf.space
```

Select: ✅ Production ✅ Preview ✅ Development

### Step 5: Deploy

1. Click **"Deploy"** button
2. Wait 2-3 minutes for build
3. You'll see: "Building..." → "Deploying..." → "Ready"

---

## ✅ Verify Deployment

After deployment completes, test these URLs:

1. **Homepage:** https://hackathon-2-phase-2-neyo.vercel.app/
2. **Sign Up:** https://hackathon-2-phase-2-neyo.vercel.app/signup
3. **Sign In:** https://hackathon-2-phase-2-neyo.vercel.app/signin
4. **Tasks:** https://hackathon-2-phase-2-neyo.vercel.app/tasks

---

## 🔧 If You See 404 Error

The most common issue is **wrong Root Directory**. Fix it:

1. Go to your project on Vercel
2. Click **Settings** → **General**
3. Find **"Root Directory"**
4. Click **"Edit"**
5. Enter: `full_stack_todo_frontend`
6. Click **"Save"**
7. Go to **Deployments** → Click **"Redeploy"**

---

## 📱 What You Should See After Deployment

**Homepage (/):**
- Welcome message
- "Get Started" button
- Links to Sign Up / Sign In

**Sign Up Page (/signup):**
- Email input
- Password input
- "Sign Up" button

**Sign In Page (/signin):**
- Email input
- Password input
- "Sign In" button

**Tasks Page (/tasks):**
- List of tasks (after login)
- "Create Task" button
- Task cards with checkboxes

---

## 🎯 Quick Checklist

Before deploying, make sure:

- ✅ GitHub repo is public or Vercel has access
- ✅ Root Directory is set to `full_stack_todo_frontend`
- ✅ Environment variable `NEXT_PUBLIC_API_URL` is added
- ✅ Framework is set to Next.js
- ✅ Build command is `npm run build`

---

## 🆘 Still Having Issues?

If deployment fails, check the **Build Logs**:

1. Go to your project on Vercel
2. Click **"Deployments"**
3. Click on the failed deployment
4. Read the error message in the logs
5. Share the error with me for help

---

## 📞 Need Help?

Share with me:
1. Screenshot of Vercel project settings
2. Build logs if deployment fails
3. The exact error message you see

Your backend is already working perfectly at https://fouziabibi-todo.hf.space!
We just need to get the frontend deployed correctly.
