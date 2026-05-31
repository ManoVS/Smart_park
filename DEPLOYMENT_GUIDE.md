# Smart Parking System - Deployment Guide

## Step 1: Set Up Supabase Database

### 1.1 Create Database Tables

Go to your Supabase dashboard and run the following SQL in the SQL editor:

```sql
-- Create tickets table
CREATE TABLE tickets (
  id BIGSERIAL PRIMARY KEY,
  ticket INTEGER UNIQUE NOT NULL,
  active INTEGER DEFAULT 0,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Create parked_vehicles table
CREATE TABLE parked_vehicles (
  id BIGSERIAL PRIMARY KEY,
  ticket INTEGER UNIQUE NOT NULL REFERENCES tickets(ticket),
  slot INTEGER NOT NULL,
  active INTEGER DEFAULT 1,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes for better query performance
CREATE INDEX idx_tickets_ticket ON tickets(ticket DESC);
CREATE INDEX idx_parked_vehicles_ticket ON parked_vehicles(ticket);
CREATE INDEX idx_parked_vehicles_active ON parked_vehicles(active);
```

### 1.2 Get Your Credentials

1. Go to **Settings** → **API** in your Supabase dashboard
2. Copy your **Project URL** (SUPABASE_URL)
3. Copy your **Anon Key** (SUPABASE_KEY)

## Step 2: Update Environment Variables

### Local Development

1. Update `/backend/.env`:
```
SUPABASE_URL=your_project_url
SUPABASE_KEY=your_anon_key
```

2. Install dependencies:
```bash
pip install -r backend/requirements.txt
```

3. Run locally:
```bash
python backend/app.py
```

## Step 3: Deploy to Vercel

### 3.1 Prerequisites
- GitHub account
- Vercel account (vercel.com)

### 3.2 Deployment Steps

1. **Push to GitHub**:
```bash
git init
git add .
git commit -m "Initial commit"
git push -u origin main
```

2. **Connect to Vercel**:
   - Go to vercel.com
   - Click "New Project"
   - Import your GitHub repository
   - Select "Other" for the framework

3. **Configure Environment Variables**:
   - In Vercel project settings, add Environment Variables:
     - `SUPABASE_URL`: Your Supabase project URL
     - `SUPABASE_KEY`: Your Supabase anon key

4. **Deploy**:
   - Vercel will automatically build and deploy
   - Your app will be available at `https://your-project.vercel.app`

### 3.3 Update Frontend API Endpoints

After deployment, update your frontend to use the Vercel URL:

In `/frontend/app.js`, replace:
```javascript
"http://localhost:8000"
```

With:
```javascript
"https://your-project.vercel.app"
```

Or use environment-based URLs:
```javascript
const API_BASE = window.location.origin;
```

## Step 4: Enable Row Level Security (Optional but Recommended)

In Supabase, enable RLS on your tables for security:

```sql
-- Enable RLS
ALTER TABLE tickets ENABLE ROW LEVEL SECURITY;
ALTER TABLE parked_vehicles ENABLE ROW LEVEL SECURITY;

-- Create policies for public access (for demo)
CREATE POLICY "Allow public read" ON tickets FOR SELECT USING (true);
CREATE POLICY "Allow public insert" ON tickets FOR INSERT WITH CHECK (true);
CREATE POLICY "Allow public read" ON parked_vehicles FOR SELECT USING (true);
CREATE POLICY "Allow public insert/update" ON parked_vehicles FOR INSERT WITH CHECK (true);
CREATE POLICY "Allow public update" ON parked_vehicles FOR UPDATE USING (true);
```

## Troubleshooting

### Issue: Database connection errors
- Check Supabase URL and Key are correct
- Verify tables exist in Supabase
- Check Vercel logs for detailed errors

### Issue: CORS errors
- Ensure CORS is properly configured in Flask
- Frontend should use the same domain as backend

### Issue: QR codes not displaying
- Check that Pillow library is installed
- Verify image mimetype is correct (image/png)

## Useful Links

- [Supabase Documentation](https://supabase.com/docs)
- [Vercel Documentation](https://vercel.com/docs)
- [Flask Documentation](https://flask.palletsprojects.com/)
