from flask import Flask, send_file, jsonify, request
from flask_cors import CORS
import qrcode
import json
from io import BytesIO
import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "DELETE"], "allow_headers": ["Content-Type"]}}, supports_credentials=True)

# Initialize Supabase lazily so the app can start even if env vars are missing
SUPABASE_URL = os.getenv("SUPABASE_URL") or os.getenv("NEXT_PUBLIC_SUPABASE_URL")
SUPABASE_KEY = (
    os.getenv("SUPABASE_KEY")
    or os.getenv("SUPABASE_ANON_KEY")
    or os.getenv("SUPABASE_SERVICE_ROLE_KEY")
)

supabase = None

def get_supabase():
    global supabase
    if supabase is not None:
        return supabase
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise RuntimeError(
            "Missing Supabase credentials. Set SUPABASE_URL and SUPABASE_KEY "
            "(or SUPABASE_ANON_KEY) in your environment."
        )
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    return supabase

# Ticket counter (stored in Supabase)
def get_next_ticket():
    try:
        client = get_supabase()
        response = client.table("tickets").select("*").order("ticket", desc=True).limit(1).execute()
        if response.data:
            return response.data[0]["ticket"] + 1
        return 1000
    except Exception as e:
        print(f"Error getting next ticket: {e}")
        return 1000

@app.route('/generate_ticket', methods=['GET'])
def generate_ticket():
    try:
        ticket_num = get_next_ticket()
        
        # Insert ticket into database
        client = get_supabase()
        client.table("tickets").insert({
            "ticket": ticket_num,
            "active": 0
        }).execute()
        
        return jsonify({"ticket": ticket_num})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/generate_qr/<int:slot>/<int:ticket>', methods=['GET', 'OPTIONS'])
def generate_qr(slot, ticket):
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Methods", "GET, OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        return response
    
    try:
        # Create QR code data
        qr_data = {
            "slot": slot,
            "ticket": ticket
        }
        
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=2,
        )
        qr.add_data(json.dumps(qr_data))
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Save to bytes
        img_io = BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)
        
        # Store parking record in database
        client = get_supabase()
        client.table("parked_vehicles").upsert({
            "ticket": ticket,
            "slot": slot,
            "active": 1
        }).execute()
        
        return send_file(img_io, mimetype='image/png')
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/dashboard', methods=['GET'])
def dashboard():
    try:
        client = get_supabase()
        response = client.table("parked_vehicles").select("*").eq("active", 1).execute()
        vehicles = response.data if response.data else []
        return jsonify(vehicles)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/clear/<int:ticket>', methods=['DELETE'])
def clear_slot(ticket):
    try:
        client = get_supabase()
        client.table("parked_vehicles").update({"active": 0}).eq("ticket", ticket).execute()
        return jsonify({"success": True})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000, use_reloader=False)
