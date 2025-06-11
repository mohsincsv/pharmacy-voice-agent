#!/usr/bin/env python
# test_webhook.py - Test script for simulating Retell AI webhook calls

import requests
import json
import argparse
import os
from datetime import datetime

# Default webhook URL when running locally
DEFAULT_WEBHOOK_URL = "http://localhost:5001/webhook"

# Sample patient data for testing
SAMPLE_PATIENT = {
    "name": "John Doe",
    "date_of_birth": "01/15/1980",
    "phone": "555-123-4567",
    "reason": "Prescription refill"
}

def simulate_call_started(webhook_url):
    """Simulate a call_started event from Retell AI"""
    payload = {
        "event": "call_started",
        "call_id": "test-call-123",
        "timestamp": datetime.now().isoformat()
    }
    
    print(f"📞 Simulating call_started event...")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    response = requests.post(webhook_url, json=payload)
    
    print(f"Response status: {response.status_code}")
    print(f"Response body: {response.json()}")
    
    return response

def simulate_call_ended(webhook_url):
    """Simulate a call_ended event from Retell AI"""
    payload = {
        "event": "call_ended",
        "call_id": "test-call-123",
        "duration": 120,  # 2 minutes
        "timestamp": datetime.now().isoformat()
    }
    
    print(f"📞 Simulating call_ended event...")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    response = requests.post(webhook_url, json=payload)
    
    print(f"Response status: {response.status_code}")
    print(f"Response body: {response.json()}")
    
    return response

def simulate_save_data(webhook_url, patient_data=None):
    """Simulate a save_data function call from Retell AI"""
    if patient_data is None:
        patient_data = SAMPLE_PATIENT
    
    payload = {
        "function_call": {
            "name": "save_data",
            "arguments": patient_data
        },
        "call_id": "test-call-123",
        "timestamp": datetime.now().isoformat()
    }
    
    print(f"💾 Simulating save_data function call...")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    response = requests.post(webhook_url, json=payload)
    
    print(f"Response status: {response.status_code}")
    print(f"Response body: {response.json()}")
    
    # Check if data was saved to data.json
    if os.path.exists("data.json"):
        try:
            with open("data.json", "r") as f:
                saved_data = json.load(f)
                print("\n✅ Data saved to data.json:")
                print(json.dumps(saved_data, indent=2))
        except Exception as e:
            print(f"\n❌ Error reading data.json: {str(e)}")
    else:
        print("\n⚠️ Warning: data.json file not found")
    
    return response

def simulate_custom_payload(webhook_url, payload_file):
    """Simulate a custom webhook payload from a JSON file"""
    try:
        with open(payload_file, "r") as f:
            payload = json.load(f)
        
        print(f"🔧 Simulating custom webhook payload from {payload_file}...")
        print(f"Payload: {json.dumps(payload, indent=2)}")
        
        response = requests.post(webhook_url, json=payload)
        
        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.json()}")
        
        return response
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

def simulate_full_call_flow(webhook_url):
    """Simulate a complete call flow: started -> save_data -> ended"""
    print("🔄 Simulating full call flow...\n")
    
    # Step 1: Call started
    simulate_call_started(webhook_url)
    print("\n" + "-" * 50 + "\n")
    
    # Step 2: Save data
    simulate_save_data(webhook_url)
    print("\n" + "-" * 50 + "\n")
    
    # Step 3: Call ended
    simulate_call_ended(webhook_url)
    
    print("\n✅ Full call flow simulation completed!")

def main():
    """Main entry point with command line argument parsing"""
    parser = argparse.ArgumentParser(description="Test script for simulating Retell AI webhook calls for pharmacy voice agent")
    
    parser.add_argument("--url", default=DEFAULT_WEBHOOK_URL,
                        help=f"Webhook URL (default: {DEFAULT_WEBHOOK_URL})")
    
    parser.add_argument("--action", choices=["start", "end", "save", "flow", "custom"],
                        default="flow", help="Action to simulate (default: flow)")
    
    parser.add_argument("--name", help="Patient name (for save action)")
    parser.add_argument("--dob", help="Patient date of birth (for save action)")
    parser.add_argument("--phone", help="Patient phone number (for save action)")
    parser.add_argument("--reason", help="Patient visit reason (for save action)")
    
    parser.add_argument("--payload", help="JSON file with custom payload (for custom action)")
    
    args = parser.parse_args()
    
    # Handle custom patient data if provided
    if args.action == "save" and (args.name or args.dob or args.phone or args.reason):
        patient_data = SAMPLE_PATIENT.copy()
        if args.name:
            patient_data["name"] = args.name
        if args.dob:
            patient_data["date_of_birth"] = args.dob
        if args.phone:
            patient_data["phone"] = args.phone
        if args.reason:
            patient_data["reason"] = args.reason
    else:
        patient_data = None
    
    # Execute the requested action
    if args.action == "start":
        simulate_call_started(args.url)
    elif args.action == "end":
        simulate_call_ended(args.url)
    elif args.action == "save":
        simulate_save_data(args.url, patient_data)
    elif args.action == "flow":
        simulate_full_call_flow(args.url)
    elif args.action == "custom":
        if not args.payload:
            print("❌ Error: --payload file is required for custom action")
            return
        simulate_custom_payload(args.url, args.payload)

if __name__ == "__main__":
    main()
