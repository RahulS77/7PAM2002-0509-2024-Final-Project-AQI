# Masters-Final-Project-AQI

## How to Run It
### Open in Colab
- **Download** `7PAM2002_0509_2024_Rahul_Shah.ipynb` from this repo.
- **Upload** to Google Colab via **"File > Upload Notebook"**.
- Or, click this badge:  
  [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1ZinhYwBctHqqJKCIeA76GF3J9T2wu9Uv)

### Run It
- Hit **"Runtime > Run All"** (or `Ctrl+F9`)

### Requirements
- No install needed-Colab proloads all libraries.
- Ensure Colab's runtime is Python 3 (default).

## 🔐 Environment Variables (`.env` file)

The `download.py` script requires a `.env` file to manage API credentials securely. This file should be located in the project root and **must not be committed** to version control.

### 📝 Example `.env` file

```env
# EPA AQS API credentials
API_KEY=apiKeyFromUsEPA
EMAIL=emailUsedToSignUpOnUsEPA
