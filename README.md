# Pharmacy Voice Agent

A voice agent service that receives phone-call from patients vai Retell AI, stores the caller’s details in a JSON file, and prints a notification so pharmacy staff know a patient called.

The agent lives entirely on your machine (or a small cloud server).

---

## How it Works

1. Patient calls your Retell phone number.  
2. Retell’s AI collects four fields: **name**, **date of birth**, **phone**, **reason for visit**.  
3. When all fields are gathered Retell sends an HTTPS POST to `/webhook`.  
4. `app.py`:
   - adds an `id` and timestamp
   - appends the record to `data.json`
   - writes a summary line to `notifications.txt`
   - prints the same summary to the console

---

## Running Locally

```bash
python app.py
```

The service starts on `http://localhost:5001`.

### Expose to Retell (optional)

```bash
ngrok http 5001
```

Use the HTTPS forwarding URL and append `/webhook`.  
Example: `https://abc123.ngrok.io/webhook`

---

## Retell Agent Configuration

1. **Prompt**

   ```
   You are a pharmacy phone assistant. Collect:
   1. Patient name
   2. Date of birth
   3. Phone number
   4. Reason for call

   When all four are collected call the function save_data and end the call politely.
   ```

2. **Function**

   ```json
   {
     "name": "save_data",
     "description": "Store caller information",
     "parameters": {
       "type": "object",
       "properties": {
         "name": { "type": "string" },
         "date_of_birth": { "type": "string" },
         "phone": { "type": "string" },
         "reason": { "type": "string" }
       },
       "required": ["name", "date_of_birth", "phone", "reason"]
     }
   }
   ```

3. Set the webhook URL to your tunnel or server: `/webhook`.

---

## Endpoints

| Method | Path              | Purpose                       |
|--------|-------------------|-------------------------------|
| GET    | `/health`         | Basic health check            |
| GET    | `/patients`       | Dump of `data.json`           |
| GET    | `/notifications`  | Contents of `notifications.txt` |
| POST   | `/webhook`        | Retell AI calls this endpoint |

---

## Local Test without a Phone

A helper script (if present) can simulate the Retell payload:

```bash
./test_webhook.py --action flow
```

It sends:

1. `call_started`  
2. `save_data` with sample patient  
3. `call_ended`

Check the console output, `data.json`, and `notifications.txt` to confirm everything works.

---

## Resetting Data

To start fresh during development:

```bash
echo '{ "patients": [] }' > data.json
> notifications.txt  # truncate the file
```

---

That’s it. Start the server, point Retell to `/webhook`, and watch new calls appear in real time.
