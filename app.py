# app.py - Pharmacy Voice Agent
# Handles Retell AI webhooks and pharmacy patient data collection

from flask import Flask, request, jsonify
import json
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# File paths
DATA_FILE = "data.json"
NOTIFICATIONS_FILE = "notifications.txt"


def load_data():
    """Load pharmacy patient data from JSON file"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"patients": []}


def save_data(data):
    """Save pharmacy patient data to JSON file"""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


def notify_team(patient_data):
    """Send notifications to pharmacy team via console and file"""
    timestamp = datetime.now().strftime("%I:%M %p")

    # Console notification with emoji for visibility
    print("\n" + "=" * 50)
    print("🚨 NEW PHARMACY PATIENT CALL RECEIVED!")
    print("=" * 50)
    print(f"📞 Name: {patient_data.get('name', 'N/A')}")
    print(f"🎂 DOB: {patient_data.get('date_of_birth', 'N/A')}")
    print(f"📱 Phone: {patient_data.get('phone', 'N/A')}")
    print(f"🩺 Reason: {patient_data.get('reason', 'N/A')}")
    print(f"⏰ Time: {timestamp}")
    print("=" * 50)

    # File notification for persistence
    with open(NOTIFICATIONS_FILE, "a") as f:
        f.write(f"\n[{datetime.now().isoformat()}] NEW PHARMACY PATIENT CALL\n")
        f.write(f"Name: {patient_data.get('name', 'N/A')}\n")
        f.write(f"DOB: {patient_data.get('date_of_birth', 'N/A')}\n")
        f.write(f"Phone: {patient_data.get('phone', 'N/A')}\n")
        f.write(f"Reason: {patient_data.get('reason', 'N/A')}\n")
        f.write(f"Timestamp: {timestamp}\n")
        f.write("-" * 50 + "\n")


def check_prescription_status(patient_data):
    """
    Future enhancement: Check prescription status in pharmacy system
    This is a placeholder for integration with pharmacy management systems
    """
    # In a real implementation, this would query the pharmacy system API
    # For MVP, we'll just return a placeholder status
    return {
        "status": "ready_for_pickup",
        "prescription_id": "RX12345",
        "last_filled": datetime.now().strftime("%Y-%m-%d"),
        "refills_remaining": 3
    }


@app.route("/webhook", methods=["POST"])
def retell_webhook():
    """Main webhook endpoint for Retell AI pharmacy voice agent"""
    try:
        # Get data from Retell
        request_data = request.get_json()
        print(f"📥 Received webhook data: {request_data}")

        # Handle different types of webhook events
        if request_data and "event" in request_data:
            event_type = request_data["event"]

            if event_type == "call_started":
                print("📞 Pharmacy call started")
                return jsonify({"status": "call_started"})

            elif event_type == "call_ended":
                print("📞 Pharmacy call ended")
                return jsonify({"status": "call_ended"})

        # Handle function calls (when AI collects patient data)
        if "function_call" in request_data:
            function_name = request_data["function_call"].get("name")

            if function_name == "save_data":
                patient_data = request_data["function_call"].get("arguments", {})

                # Load existing data
                data = load_data()

                # Add new patient with auto-increment ID
                patient_data["id"] = len(data["patients"]) + 1
                patient_data["timestamp"] = datetime.now().isoformat()
                
                # Future enhancement: Check prescription status
                # prescription_status = check_prescription_status(patient_data)
                # patient_data["prescription_status"] = prescription_status
                
                data["patients"].append(patient_data)

                # Save to JSON file
                save_data(data)
                print(f"💾 Saved pharmacy patient data: {patient_data}")

                # Notify pharmacy team (console + file)
                notify_team(patient_data)

                return jsonify(
                    {"success": True, "message": "Pharmacy patient data saved successfully"}
                )

        # Default response for other webhook events
        return jsonify({"status": "received"})

    except Exception as e:
        error_msg = f"Error processing pharmacy webhook: {str(e)}"
        print(f"❌ {error_msg}")
        return jsonify({"error": error_msg}), 500


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify(
        {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "service": "Pharmacy Voice Agent",
        }
    )


@app.route("/patients", methods=["GET"])
def get_patients():
    """Get all pharmacy patients (for debugging)"""
    try:
        data = load_data()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/notifications", methods=["GET"])
def get_notifications():
    """Get pharmacy notification log (for debugging)"""
    try:
        if os.path.exists(NOTIFICATIONS_FILE):
            with open(NOTIFICATIONS_FILE, "r") as f:
                return {"notifications": f.read()}
        return {"notifications": "No pharmacy notifications yet"}
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print("🚀 Starting Pharmacy Voice Agent...")
    print(f"📁 Data file: {DATA_FILE}")
    print(f"📝 Notifications file: {NOTIFICATIONS_FILE}")
    print("🌐 Health check: http://localhost:5001/health")
    print("👥 Patients endpoint: http://localhost:5001/patients")
    print("📋 Notifications endpoint: http://localhost:5001/notifications")
    print("-" * 50)

    app.run(host="0.0.0.0", port=5001, debug=True)
