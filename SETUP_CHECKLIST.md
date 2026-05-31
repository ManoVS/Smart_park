# 🚀 Deployment Checklist

## ✅ Prerequisites

- [ ] Supabase account (supabase.com)
- [ ] Vercel account (vercel.com)
- [ ] GitHub account (github.com)

## 🗄️ Step 1: Set Up Supabase (5 minutes)

### Create Database Tables

1. Go to supabase.com dashboard
2. Create a new project or use existing
3. Go to **SQL Editor** and run:

```sql
CREATE TABLE tickets (
  id BIGSERIAL PRIMARY KEY,
  ticket INTEGER UNIQUE NOT NULL,
  active INTEGER DEFAULT 0,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE parked_vehicles (
  id BIGSERIAL PRIMARY KEY,
  ticket INTEGER UNIQUE NOT NULL REFERENCES tickets(ticket),
  slot INTEGER NOT NULL,
  active INTEGER DEFAULT 1,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_tickets_ticket ON tickets(ticket DESC);
CREATE INDEX idx_parked_vehicles_ticket ON parked_vehicles(ticket);
CREATE INDEX idx_parked_vehicles_active ON parked_vehicles(active);
```

### Get Credentials

1. Go to **Settings** → **API**
2. Copy **Project URL** → Save as SUPABASE_URL
3. Copy **Anon Key** → Save as SUPABASE_KEY

## 💻 Step 2: Local Testing (10 minutes)

```bash
# Install dependencies
cd /home/manoranjan-seker/Web
python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt

# Update backend/.env
# Add your SUPABASE_URL and SUPABASE_KEY

# Terminal 1 - Run Backend
python backend/app.py

# Terminal 2 - Run Frontend
cd frontend
python3 -m http.server 3000

# Open http://localhost:3000
```

## 🌐 Step 3: Deploy to Vercel (10 minutes)

### Option A: Using Vercel CLI

```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy
cd /home/manoranjan-seker/Web
vercel

# Add environment variables when prompted
# SUPABASE_URL: your_url
# SUPABASE_KEY: your_key
```

### Option B: Using GitHub + Vercel Dashboard

1. **Initialize Git**:
```bash
cd /home/manoranjan-seker/Web
git init
git add .
git commit -m "Smart Parking System"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/parking-system.git
git push -u origin main
```

2. **Connect to Vercel**:
   - Go to vercel.com
   - Click "New Project"
   - Import your GitHub repository
   - Select "Other" framework

3. **Add Environment Variables** in Vercel Dashboard:
   - `SUPABASE_URL`: Your Supabase project URL
   - `SUPABASE_KEY`: Your Supabase anon key

4. **Deploy**: Click "Deploy" button

## ✨ Step 4: Update Frontend (2 minutes)

The frontend automatically detects the environment! 

If manually updating, in `frontend/app.js`, change:
```javascript
const API_BASE = window.location.origin;
```

## 📊 After Deployment

1. **Test your app** at `https://your-project.vercel.app`
2. **Monitor** Supabase dashboard for data
3. **Check** Vercel logs if issues occur
4. **Share** your public URL!

## 🆘 Troubleshooting

### "Cannot connect to database"
- Verify SUPABASE_URL and SUPABASE_KEY in .env
- Check tables exist in Supabase
- Check Vercel environment variables

### "CORS errors"
- Ensure frontend uses correct API_BASE
- Backend CORS is already configured

### "QR codes not showing"
- Check Pillow library is installed
- Verify image mimetype (should be image/png)

## 📞 Support

- Check DEPLOYMENT_GUIDE.md for detailed steps
- Check Vercel dashboard for build/runtime logs
- Check Supabase dashboard for database errors

---

**Your app will be live at**: `https://YOUR-PROJECT.vercel.app` 🎉
