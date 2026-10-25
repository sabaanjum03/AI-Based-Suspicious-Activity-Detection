# import streamlit as st
# import tempfile
# import base64
# from utils.inference_utils import run_action_recognition

# # =========================
# # PAGE CONFIG
# # =========================
# st.set_page_config(page_title="Action Recognition", layout="centered")

# st.title("🎥 Action Recognition App")
# st.write("Upload a video to detect suspicious activities 🚨")

# # =========================
# # 🔊 ALERT SOUND FUNCTION
# # =========================
# def play_alert_sound():
#     try:
#         with open("alert.mp3", "rb") as f:
#             data = f.read()
#             b64 = base64.b64encode(data).decode()
#             audio_html = f"""
#             <audio autoplay>
#                 <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
#             </audio>
#             """
#             st.markdown(audio_html, unsafe_allow_html=True)
#     except Exception:
#         st.warning("⚠️ Alert sound file not found (alert.mp3)")

# # =========================
# # 📤 FILE UPLOAD
# # =========================
# uploaded_file = st.file_uploader("Upload a video", type=["mp4", "avi", "mov"])

# if uploaded_file is not None:
#     st.video(uploaded_file)

#     # Save uploaded video temporarily
#     tfile = tempfile.NamedTemporaryFile(delete=False)
#     tfile.write(uploaded_file.read())

#     # =========================
#     # ⏳ RUN MODEL
#     # =========================
#     with st.spinner("Processing video... Please wait ⏳"):
#         result = run_action_recognition(
#             source=tfile.name,
#             flip=False
#         )

#     st.success("✅ Processing Complete!")

#     # =========================
#     # ❌ ERROR HANDLING
#     # =========================
#     if "error" in result:
#         st.error(result["error"])

#     else:
#         st.divider()

#         # =========================
#         # 🚨 ALERT SECTION
#         # =========================
#         if result.get("alert"):
#             st.error(
#                 f"🚨 ALERT: {result['alert_label']} detected "
#                 f"({result['alert_conf']*100:.2f}%)"
#             )
#             play_alert_sound()  # 🔊 SOUND ALERT
#         else:
#             st.success("✅ No threat detected")

#         st.divider()

#         # =========================
#         # 📊 PREDICTIONS
#         # =========================
#         st.subheader("🔍 Predictions")

#         col1, col2, col3 = st.columns(3)

#         col1.metric("Top 1", result['top_1'][0], f"{result['top_1'][1]*100:.2f}%")
#         col2.metric("Top 2", result['top_2'][0], f"{result['top_2'][1]*100:.2f}%")
#         col3.metric("Top 3", result['top_3'][0], f"{result['top_3'][1]*100:.2f}%")















import os
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"
import streamlit as st
import tempfile
import base64
import datetime
import smtplib
from email.mime.text import MIMEText

from utils.inference_utils import run_action_recognition

# =========================
# 🔥 FIREBASE SETUP
# =========================
import firebase_admin
from firebase_admin import credentials, db

if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_key.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://surviellence-e6327-default-rtdb.firebaseio.com/'
    })

# =========================
# 📧 EMAIL CONFIG
# =========================
EMAIL_SENDER = "sabaanjum9880@gmail.com"
EMAIL_PASSWORD = "qdwrlksmbfnqidob"   # 🔥 replace this
EMAIL_RECEIVER = "sabaanjum9880@gmail.com"

# =========================
# 🔊 ALERT SOUND FUNCTION
# =========================
def play_alert_sound():
    try:
        with open("alert.mp3", "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            st.markdown(f"""
            <audio autoplay>
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """, unsafe_allow_html=True)
    except:
        st.warning("⚠️ alert.mp3 not found")

# =========================
# ☁️ FIREBASE FUNCTION
# =========================
def send_to_firebase(label, confidence):
    ref = db.reference("alerts")

    data = {
        "label": label,
        "confidence": float(confidence),
        "timestamp": str(datetime.datetime.now())
    }

    ref.push(data)

# =========================
# 📧 EMAIL FUNCTION
# =========================
def send_email_alert(label, confidence):
    subject = "🚨 ALERT: Suspicious Activity Detected"

    body = f"""
ALERT DETECTED!

Activity: {label}
Confidence: {confidence*100:.2f}%

Time: {datetime.datetime.now()}
"""

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
    except Exception as e:
        st.error(f"Email failed: {e}")

# =========================
# 🎥 STREAMLIT UI
# =========================
st.set_page_config(page_title="Action Recognition", layout="centered")

st.title("🎥 Action Recognition App")
st.write("Upload a video to detect suspicious activities 🚨")

uploaded_file = st.file_uploader("Upload a video", type=["mp4", "avi", "mov"])

if uploaded_file is not None:
    st.video(uploaded_file)

    # Save file temporarily
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())

    # Run model
    with st.spinner("⏳ Processing video..."):
        result = run_action_recognition(
            source=tfile.name,
            flip=False
        )

    st.success("✅ Processing Complete!")

    # =========================
    # ❌ ERROR HANDLING
    # =========================
    if "error" in result:
        st.error(result["error"])

    else:
        st.divider()

        # =========================
        # 🚨 ALERT SYSTEM
        # =========================
        if result.get("alert"):
            st.error(
                f"🚨 ALERT: {result['alert_label']} detected "
                f"({result['alert_conf']*100:.2f}%)"
            )

            # 🔊 Sound
            play_alert_sound()

            # ☁️ Firebase
            send_to_firebase(result['alert_label'], result['alert_conf'])

            # 📧 Email
            send_email_alert(result['alert_label'], result['alert_conf'])

        else:
            st.success("✅ No threat detected")

        st.divider()

        # =========================
        # 📊 PREDICTIONS
        # =========================
        st.subheader("🔍 Predictions")

        col1, col2, col3 = st.columns(3)

        col1.metric("Top 1", result['top_1'][0], f"{result['top_1'][1]*100:.2f}%")
        col2.metric("Top 2", result['top_2'][0], f"{result['top_2'][1]*100:.2f}%")
        col3.metric("Top 3", result['top_3'][0], f"{result['top_3'][1]*100:.2f}%")



