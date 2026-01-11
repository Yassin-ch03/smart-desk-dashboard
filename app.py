import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import requests

# ================= FIREBASE =================
FIREBASE_DB_URL = "https://projet-final-database-default-rtdb.europe-west1.firebasedatabase.app/"

cred = credentials.Certificate({
    "type": "service_account",
    "project_id": "TON_PROJECT_ID",
    "private_key_id": "projet-final-database",
    "private_key_id": "1a370cc3420610dd21676e4e83434ac06e0f75b8",
    "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-fbsvc@projet-final-database.iam.gserviceaccount.com",
    "client_id": "118338313290699967428",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40projet-final-database.iam.gserviceaccount.com"
})

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {
        "databaseURL": FIREBASE_DB_URL
    })
# ============================================

NODE_RED_URL = "https://nodered.yassinfyn.work.gd/desk/control"

def send(cmd):
    try:
        r = requests.post(NODE_RED_URL, json={"cmd": cmd}, timeout=3)
        if r.status_code != 200:
            st.error("Erreur Node-RED")
    except Exception as e:
        st.error(f"Erreur réseau : {e}")

# ================= INTERFACE =================
st.set_page_config(page_title="Smart Desk Assistant", layout="centered")
st.title("🧠 Smart Desk Assistant")

# ================= LECTURE FIREBASE =================
ref = db.reference("/last")
data = ref.get()

if not data:
    st.warning("Aucune donnée reçue")
    st.stop()

last_key = list(data.keys())[-1]
d = data[last_key]

temp = d.get("temp", 0)
hum  = d.get("hum", 0)
lum  = d.get("lum", 0)
mode = d.get("mode", "N/A")

# ================= AFFICHAGE CAPTEURS =================
st.header("📊 Données des capteurs")
st.metric("Température (°C)", temp)
st.metric("Humidité (%)", hum)
st.metric("Luminosité", lum)
st.metric("Mode", mode)

st.divider()

# ================= ETAT =================
st.subheader("🚦 État du système")

if temp > 27:
    st.error("Température trop élevée")
elif lum < 30:
    st.warning("Luminosité faible")
else:
    st.success("Conditions normales")

st.divider()

# ================= SERVO =================
st.subheader("🪟 Fenêtre (Servo)")

if st.button("Ouvrir fenêtre"):
    send("SERVO_OPEN")

if st.button("Fermer fenêtre"):
    send("SERVO_CLOSE")

st.divider()

# ================= BUZZER =================
st.subheader("🔊 Buzzer")

if st.button("Buzzer ON"):
    send("BUZZER_ON")

if st.button("Buzzer OFF"):
    send("BUZZER_OFF")

st.divider()

# ================= LEDS =================
st.subheader("💡 LEDs")

if st.button("Rouge ON"):
    send("LED_RED_ON")

if st.button("Rouge OFF"):
    send("LED_RED_OFF")

if st.button("Jaune ON"):
    send("LED_YELLOW_ON")

if st.button("Jaune OFF"):
    send("LED_YELLOW_OFF")

st.divider()

# ================= RGB PWM =================
st.subheader("🌈 RGB (PWM)")

r = st.slider("Rouge", 0, 255, 0)
g = st.slider("Vert", 0, 255, 0)
b = st.slider("Bleu", 0, 255, 0)

if st.button("Appliquer couleur RGB"):
    send(f"RGB_SET:{r},{g},{b}")

if st.button("RGB OFF"):
    send("RGB_OFF")

st.divider()

# ================= CLEAR =================
if st.button("Tout éteindre"):
    send("CLEAR")
