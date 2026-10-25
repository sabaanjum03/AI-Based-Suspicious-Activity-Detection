# AI-Based Suspicious Activity Detection

A video-based action-recognition application built with Python,
TensorFlow/Keras, OpenCV, and Streamlit. Upload a video to view the
model's top predictions. When the configured alert rule is triggered,
the app can play an alert sound, save an alert to Firebase Realtime
Database, and send an email notification.

> **Disclaimer:** This is an academic/demo project. Predictions may be
> wrong; do not rely on it as the sole basis for real-world security
> decisions.

## Features

-   Upload MP4, AVI, or MOV videos.
-   Run action recognition using the trained models.
-   Display the top three predicted classes and confidence scores.
-   Play `alert.mp3` when an alert is triggered.
-   Store alert records in Firebase Realtime Database.
-   Send email notifications through Gmail SMTP when configured.

## Project structure

Based on the project structure shown in VS Code; adjust names if your
local files differ.

``` text
AI_PROJECT/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── alert.mp3
├── assets/
├── Data/
├── Models/
│   ├── classifier_lstm.h5
│   ├── classifier_lstm_e19.h5
│   ├── feature_extractor_inceptionv3.h5
│   └── ... other model files ...
├── notebooks/
│   ├── prepare_dataset.ipynb
│   ├── training.ipynb
│   └── inference.ipynb
└── utils/
    ├── inference_utils.py
    └── notebook_utils.py
```

## Requirements

-   Git
-   Python version compatible with your TensorFlow release
-   Firebase Realtime Database credentials if database alerts are
    enabled
-   Gmail App Password if email alerts are enabled

Your screenshots showed TensorFlow 2.10.0. TensorFlow 2.10 is generally
used with Python 3.7--3.10 and NumPy versions below 1.24. A common
starting point for that environment is Python 3.10 with NumPy 1.23.5.
Confirm the full dependency set against your code before publishing.

## Installation

### 1. Clone the repository

Replace the placeholders with your GitHub username and repository name:

``` bash
git clone https://github.com/<your-username>/<your-repository>.git
cd <your-repository>
```

Alternatively, download the repository ZIP from GitHub and extract it.

### 2. Create a virtual environment

**Windows PowerShell:**

``` powershell
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS/Linux:**

``` bash
python3.10 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

If `requirements.txt` exists:

``` bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If you are still preparing `requirements.txt`, the main app dependencies
may include:

``` bash
python -m pip install streamlit numpy==1.23.5 opencv-python tensorflow==2.10.0 firebase-admin
```

Install any additional packages imported by your code. TensorFlow 2.10
does not support Python 3.11+, so use a compatible Python version for
that release.

### 4. Configure Firebase (optional)

1.  Create or select a Firebase project.
2.  Enable Realtime Database and copy its database URL.
3.  Create a service-account key.
4.  Store the JSON key locally, outside version control.
5.  Update the app to read credentials and the database URL from
    environment variables or Streamlit secrets.

**Never commit `firebase_key.json` to GitHub.** If a service-account key
has already been pushed publicly, revoke it and create a new one. The
current app code should be updated to avoid hard-coded credentials and
database configuration.

### 5. Configure email alerts (optional)

For Gmail SMTP, use a Google **App Password** (with 2-Step Verification
enabled), not your normal account password. Store sender, receiver, and
password settings in environment variables or Streamlit secrets, not
directly in source code.

**Security notice:** An email App Password was present in the code
shared during project discussion. If it is real, revoke it immediately
and create a new one. Do not upload it to GitHub.

### 6. Check model and sound files

Confirm that the model files expected by `utils/inference_utils.py`
exist in `Models/`, with filenames and capitalization matching the code.
Confirm that `alert.mp3` exists at the path expected by `app.py`.

If model weights are not included, document how to obtain them or train
them before running inference. Large datasets, videos, and model files
may need to be kept outside GitHub or distributed using Git LFS, subject
to file size and licensing.

### 7. Run the app

From the project root (the folder containing `app.py`):

``` bash
python -m streamlit run app.py
```

Open the local URL printed by Streamlit, usually
`http://localhost:8501`. Upload a supported video and review the
predictions and alert status. Stop the app with `Ctrl+C`.

## Troubleshooting

### `ModuleNotFoundError: No module named 'tensorflow'`

Install dependencies in the same Python environment used to launch
Streamlit:

``` bash
python -m pip install tensorflow==2.10.0
python -c "import sys; print(sys.executable)"
```

In VS Code, the notebook kernel and terminal can use different Python
installations. Select the same virtual environment for both.

### `ImportError: numpy.core.multiarray failed to import`

This can indicate incompatible or damaged NumPy/OpenCV/TensorFlow
installations. Check versions first:

``` bash
python -m pip show numpy tensorflow opencv-python
```

For TensorFlow 2.10, try a compatible NumPy version:

``` bash
python -m pip install --force-reinstall numpy==1.23.5
python -m pip install --force-reinstall opencv-python
```

Restart the terminal/kernel and test:

``` bash
python -c "import numpy, cv2, tensorflow as tf; print(numpy.__version__, cv2.__version__, tf.__version__)"
```

If the error remains, create a clean virtual environment and install the
dependencies together rather than randomly upgrading NumPy.

### `NameError: name 'load_model' is not defined`

In the notebook cell that loads models, add this before calling
`load_model`:

``` python
from tensorflow.keras.models import load_model
```

Use paths that are correct for the notebook's working directory. The
Streamlit app may load models through `utils/inference_utils.py`, so you
do not need to run the notebook to start the app.

### `ModuleNotFoundError: No module named 'moviepy'`

If dataset preparation requires MoviePy, install it into the active
notebook environment:

``` bash
python -m pip install moviepy
```

Choose a version compatible with the notebook imports. The app may not
require MoviePy if it is only used during dataset preparation.

### Firebase or email alerts fail

Check the database URL, service-account permissions, database rules,
Gmail App Password, and SMTP configuration. A notification failure does
not necessarily mean video inference failed.

## How it works

1.  The user uploads a video through Streamlit.
2.  `app.py` passes the temporary video path to
    `run_action_recognition()` in `utils/inference_utils.py`.
3.  The inference utility processes the video and returns prediction
    labels, confidence scores, and alert information.
4.  The interface displays the top three predictions.
5.  If the configured alert rule is triggered, the app attempts to play
    a sound, write to Firebase, and send an email.



## Technologies

Python · Streamlit · TensorFlow/Keras · OpenCV · NumPy · Firebase
Realtime Database · SMTP/Gmail · Jupyter Notebook


## License

This project is developed for educational and final-year project purposes. Please check the licenses of third-party libraries, pretrained models, and datasets before using or redistributing them.

## Author

**Saba Anjum**

- GitHub: [@sabaanjum03](https://github.com/sabaanjum03)
- Project: AI-Based Suspicious Activity Detection

Developed using Python, Streamlit, TensorFlow/Keras, and OpenCV.
