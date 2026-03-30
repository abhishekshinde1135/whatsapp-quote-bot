import requests
from twilio.rest import Client
import schedule
import time

# === YOUR KEYS ===
TWILIO_SID    = "your_twilio_sid_here"
TWILIO_TOKEN  = "your_twilio_auth_token_here"
API_NINJA_KEY = "your_api_ninjas_key_here"
FROM_WHATSAPP = "whatsapp:+14155238886"   # Twilio sandbox number
TO_WHATSAPP   = "whatsapp:+91XXXXXXXXXX"  # Your WhatsApp number

def get_quote():
    res = requests.get(
        "https://api.api-ninjas.com/v1/quotes",
        headers={"X-Api-Key": API_NINJA_KEY}
    )
    if res.status_code == 200 and res.text.strip():
        data = res.json()
        return f'💡 *Daily Quote*\n\n"{data[0]["quote"]}"\n\n— _{data[0]["author"]}_'
    return "Could not fetch quote today."

def send_whatsapp_quote():
    client = Client(TWILIO_SID, TWILIO_TOKEN)
    message = get_quote()
    client.messages.create(
        body=message,
        from_=FROM_WHATSAPP,
        to=TO_WHATSAPP
    )
    print("✅ Quote sent!")

# Send every day at 8:00 AM
schedule.every().day.at("6:00").do(send_whatsapp_quote)

print("🤖 Bot running... Waiting to send daily quote.")
while True:
    schedule.run_pending()
    time.sleep(60)