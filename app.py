import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import requests

# ================= FIREBASE =================
FIREBASE_DB_URL = "https://projet-final-database-default-rtdb.europe-west1.firebasedatabase.app/"

# ⚠️ ICI TU COLLES LE CONTENU DE firebase_key.json
cred = credentials.Certificate({
    "type": "service_account",
    "project_id": "TON_PROJECT_ID",
    "private_key_id": "projet-final-database",
    "private_key_id": "1a370cc3420610dd21676e4e83434ac06e0f75b8",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQChR52jvzSeI68g\n5+tSi/e8t24dnFiMebyjNKxjgGDS3jQZTWJ5HQx7QSghG1gKUU0hPmcZwKm6j0RI\nO3XGLa7Ny3c++BFExdaXM0f8X1+/lNpabK+rePGUwYsmpCtTIz30Y0OhZw60/sSz\nHa1GYl5P3yEGj4rACxtQSdMv1DpVG4l+lvAaGLTimSXaXM4yhvHL5MmZsU3kQAQQ\nWel+RiEBTBc2Rsj6JEhzYi5Ox6fNRCa74Eg1Bfb5DdapVasJtyvwFD48rxh4tlgr\ntOAyXpKsTv3QpRnbTRtEByMx06ckry2pdYwWG+p8GvKo2Z3tEKSYpdGFkI6UcNHy\nRuhvIuvnAgMBAAECggEASlXGaEdEWtEqsnmCoqjltiM7i0VZIOIpWnX4MOJmfjqx\ne6oJxbXoX1TwSJYgVZ0UdkqbXajJ8jV/bOWPCplatPrfSvQujWq8VjNqLf3NlXFn\n1P68V0Xm3z/3wYcweuDG+QHZlaZ5Bl5Yzg/TIhpLyveWcr4tXweffrmQL77bZgcQ\nW0PpdTVr6prUfc9QnKnkk4JHRgljHsS/wMKbVShWERgtqMftkISMAnbhgyv38iwN\n3mVmYXEpcLWUlkt0OyJQsXq+aZq2FNQM4gjzj0+QKF7aslLO1gL1+8rVZath+9k0\nTi9cgIqd+mwHEZXF10WlwR7/+0NdOGRXaFvyAeaI8QKBgQDORZEMtjofERo0l0K1\n2vcasP5245opxPAcZ3xstimABOZg49w6Hx9739ssntZ/cpLW0O7QrV+gaHNablqS\nHv4YpK8mzzPW39QepbgOfRjTCIM4Fo5K7lMiHfqnd43K+UaSrsXYv17e0qcNcITN\nT7XtVRM55Rt/XRYWWxI/4Y/sEQKBgQDIKUlx3dNhVjH+LUSK8xlmb2AefoF5vm9/\n4QR4vKO1veV4evBOuLGuLBDGvkPSXrffGViGV14J+At78GaI3vAluaJKVpf8IsMm\nOrW2kI/c2oxxQDkLwsBiu3OpGkz7YqA4o/tA6QUnp43kfGqiaJoSC7y4e2w+3nSW\nY1CFZmkwdwKBgFqMPUVIRTFYD5nggJ9WFL05zyqfdRA67HB7mSobuRIClKMZw5Yc\nDXUSaqMmwuBFimIUa5FdWioPT/v1j3qvcjmdKWou8QG1VedyNd7eWWRiSz/23tXT\n0tiaMmsLV0ovrSQ85orkTyAfdse2igWapTEe9IaopS5+zXBY4CT8vnIRAoGASxfK\nORDau7rFuLEs9OAtGFQSgH4/fvgmBpjZv54t4QIkM+YTf8Uky842YQmCkkr8upNc\ntdHTMvQ/Arl3DkRtXgndy/veuzYjdpUyFRL5FgdcByTsAfCHksL2qmt2lB01NOq4\nWWrSh0UCI8VVkCakHr8OhzuuqYt1u/H4hIOeVRMCgYAMX8yMIctPvXpO8qxSX+Rl\nuM38eiJET+zv+4gu1uw8G4wHA+5T0iTNCx7hT4Jbt45rBmNt0Fzl/XFFQLT4ujkL\ny8t7PQLThA3bcKA/jCpiGOs4K3HGs4OdEDaww4YIRgWzjmsmULZZyphJ0yfNbrdN\ntDQ+YhcJUILn36mosh1/eQ==\n-----END PRIVATE KEY-----\n",
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

st.set_page_config(page_title="Smart Desk Assistant", layout="center")
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
col1, col2, col3, col4 = st.columns(4)
col1.metric("Température (°C)", temp)
col2.metric("Humidité (%)", hum)
col3.metric("Luminosité", lum)
col4.metric("Mode", mode)

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
colS1, colS2 = st.columns(2)

if colS1.button("Ouvrir fenêtre"):
    send("SERVO_OPEN")

if colS2.button("Fermer fenêtre"):
    send("SERVO_CLOSE")

st.divider()

# ================= BUZZER =================
st.subheader("Buzzer")
colB1, colB2 = st.columns(2)

if colB1.button("Buzzer ON"):
    send("BUZZER_ON")

if colB2.button("Buzzer OFF"):
    send("BUZZER_OFF")

st.divider()

# ================= LEDS =================
st.subheader("LEDs")
colL1, colL2, colL3, colL4 = st.columns(4)

if colL1.button("Rouge ON"):
    send("LED_RED_ON")

if colL2.button("Rouge OFF"):
    send("LED_RED_OFF")

if colL3.button("Jaune ON"):
    send("LED_YELLOW_ON")

if colL4.button("Jaune OFF"):
    send("LED_YELLOW_OFF")

st.divider()

# ================= RGB PWM =================
st.subheader("RGB (PWM)")

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
