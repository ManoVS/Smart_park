# 🚗 Smart Parking System

A full-stack parking management system with QR code generation, real-time dashboard, and cloud deployment capabilities.

## 📋 Features

✅ **Ticket Generation** - Generate unique parking tickets
✅ **QR Code Generation** - Create QR codes with slot and ticket info
✅ **Real-time Dashboard** - Monitor parking slots (green/red)
✅ **Cloud Database** - Supabase integration for persistent data
✅ **Modern UI** - Responsive design with gradient aesthetics
✅ **Public Deployment** - Deploy to Vercel for public access

## 🛠️ Tech Stack

**Backend:**
- Flask (Python web framework)
- Supabase (PostgreSQL database)
- QRCode + Pillow (QR generation)
- OpenCV + PyZBar (QR scanning)

**Frontend:**
- HTML5
- CSS3 (Modern gradients and animations)
- Vanilla JavaScript (ES6+)

**Deployment:**
- Vercel (Backend & Frontend hosting)
- Supabase (Database)

## 🚀 Quick Start

### Local Development

1. **Clone/Setup**:
```bash
cd Web
python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
```

2. **Configure Supabase**:
   - Get `SUPABASE_URL` and `SUPABASE_KEY` from Supabase dashboard
   - Update `backend/.env`:
   ```
   SUPABASE_URL=your_url
   SUPABASE_KEY=your_key
   ```

3. **Run Backend**:
```bash
python backend/app.py
```

4. **Run Frontend** (in another terminal):
```bash
cd frontend
python3 -m http.server 3000
```

5. **Access**: Open `http://localhost:3000`

## 📦 Project Structure

```
Web/
├── backend/
│   ├── app.py              # Flask API server
│   ├── qr_scanner.py       # QR scanning utility
│   ├── requirements.txt     # Python dependencies
│   └── .env                # Environment variables
├── frontend/
│   ├── index.html          # Main UI
│   ├── style.css           # Modern styling
│   └── app.js              # JavaScript logic
├── vercel.json             # Vercel configuration
├── .env.example            # Environment template
├── .gitignore              # Git ignore rules
└── DEPLOYMENT_GUIDE.md     # Detailed deployment steps
```

## 📖 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/generate_ticket` | GET | Generate a new parking ticket |
| `/generate_qr/<slot>/<ticket>` | GET | Generate QR code for parking |
| `/dashboard` | GET | Get active parking records |
| `/clear/<ticket>` | DELETE | Clear a parking record |
| `/health` | GET | Health check |

## 🌐 Deployment to Vercel

See [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) for complete instructions.

### Quick Deploy:
1. Push code to GitHub
2. Connect repository to Vercel
3. Add environment variables (SUPABASE_URL, SUPABASE_KEY)
4. Deploy (automatic on git push)

## 📱 Database Schema

**tickets table:**
- id (Primary Key)
- ticket (Unique)
- active (Integer)
- created_at (Timestamp)

**parked_vehicles table:**
- id (Primary Key)
- ticket (Foreign Key)
- slot (Integer)
- active (Integer)
- created_at (Timestamp)
- updated_at (Timestamp)

## 🔐 Security Notes

- All API calls include CORS headers
- Supabase provides built-in authentication
- Enable Row Level Security for production
- Use environment variables for sensitive data

## 📝 License

MIT License - Feel free to use for your projects!

## 🤝 Support

For issues or questions, check:
- DEPLOYMENT_GUIDE.md
- Backend logs on Vercel
- Supabase database logs
