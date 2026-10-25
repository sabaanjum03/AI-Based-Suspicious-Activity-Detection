# import cv2
# import numpy as np
# import time
# import collections
# from tensorflow.keras.models import load_model
# import utils.notebook_utils as utils

# # Load models ONCE
# decoder = load_model('Models/classifier_lstm_e19.h5', compile=False)
# encoder = load_model('Models/feature_extractor_inceptionv3.h5', compile=False)

# IMG_SIZE = (299, 224)
# MAX_SEQ_LENGTH = 32

# class_vocab = ['Abuse', 'Arson', 'Assault', 'Burglary', 'Explosion',
#                'Fighting', 'Normal', 'RoadAccidents', 'Robbery', 'Shooting']


# def run_action_recognition(source, flip=False):
#     player = utils.VideoPlayer(source, flip=flip, fps=30)
#     player.start()

#     encoder_output = []
#     decoded_labels = ["", "", ""]
#     decoded_probs = [0, 0, 0]

#     counter = 0

#     try:
#         while True:
#             frame, _ = player.next()

#             if frame is None:
#                 break

#             counter += 1

#             preprocessed = cv2.resize(frame, IMG_SIZE)
#             preprocessed = preprocessed[:, :, [2, 1, 0]]

#             if counter % 2 == 0:
#                 features = encoder.predict(preprocessed[None, ...])[0]
#                 encoder_output.append(features)

#                 if len(encoder_output) == MAX_SEQ_LENGTH:
#                     encoder_output_np = np.array(encoder_output)[None, ...]
#                     probabilities = decoder.predict(encoder_output_np)[0]

#                     top_indices = np.argsort(probabilities)[::-1][:3]

#                     for i, idx in enumerate(top_indices):
#                         decoded_labels[i] = class_vocab[idx]
#                         decoded_probs[i] = float(probabilities[idx])

#                     encoder_output = []

#         player.stop()

#         return {
#             "top_1": (decoded_labels[0], decoded_probs[0]),
#             "top_2": (decoded_labels[1], decoded_probs[1]),
#             "top_3": (decoded_labels[2], decoded_probs[2]),
#         }

#     except Exception as e:
#         player.stop()
#         return {"error": str(e)}





import cv2
import numpy as np
import time
from tensorflow.keras.models import load_model
import utils.notebook_utils as utils

# =========================
# LOAD MODELS (ONLY ONCE)
# =========================
decoder = load_model('Models/classifier_lstm_e19.h5', compile=False)
encoder = load_model('Models/feature_extractor_inceptionv3.h5', compile=False)

# =========================
# CONFIG
# =========================
IMG_SIZE = (299, 224)
MAX_SEQ_LENGTH = 32

class_vocab = [
    'Abuse', 'Arson', 'Assault', 'Burglary', 'Explosion',
    'Fighting', 'Normal', 'RoadAccidents', 'Robbery', 'Shooting'
]

# 🚨 ALERT SETTINGS
ALERT_CLASSES = ["Fighting", "Abuse", "Robbery", "Assault","Explosion",  "Shooting","RoadAccidents"]
ALERT_THRESHOLD = 0.6   # 60% confidence


# =========================
# MAIN FUNCTION
# =========================
def run_action_recognition(source, flip=False):
    player = utils.VideoPlayer(source, flip=flip, fps=30)
    player.start()

    encoder_output = []
    decoded_labels = ["", "", ""]
    decoded_probs = [0, 0, 0]

    counter = 0

    # 🚨 Alert variables
    alert_triggered = False
    alert_label = None
    alert_conf = 0

    try:
        while True:
            frame, _ = player.next()

            if frame is None:
                break

            counter += 1

            # Preprocess
            preprocessed = cv2.resize(frame, IMG_SIZE)
            preprocessed = preprocessed[:, :, [2, 1, 0]]  # BGR → RGB

            # Process every 2nd frame
            if counter % 2 == 0:
                features = encoder.predict(preprocessed[None, ...], verbose=0)[0]
                encoder_output.append(features)

                # When enough frames collected → predict
                if len(encoder_output) == MAX_SEQ_LENGTH:
                    encoder_output_np = np.array(encoder_output)[None, ...]
                    probabilities = decoder.predict(encoder_output_np, verbose=0)[0]

                    top_indices = np.argsort(probabilities)[::-1][:3]

                    for i, idx in enumerate(top_indices):
                        decoded_labels[i] = class_vocab[idx]
                        decoded_probs[i] = float(probabilities[idx])

                    # 🚨 ALERT CHECK (TOP PREDICTION)
                    if (
                        decoded_labels[0] in ALERT_CLASSES and
                        decoded_probs[0] >= ALERT_THRESHOLD
                    ):
                        alert_triggered = True
                        alert_label = decoded_labels[0]
                        alert_conf = decoded_probs[0]

                    encoder_output = []

        player.stop()

        return {
            "top_1": (decoded_labels[0], decoded_probs[0]),
            "top_2": (decoded_labels[1], decoded_probs[1]),
            "top_3": (decoded_labels[2], decoded_probs[2]),
            "alert": alert_triggered,
            "alert_label": alert_label,
            "alert_conf": alert_conf
        }

    except Exception as e:
        player.stop()
        return {"error": str(e)}