# CybrVault Local
**Secure File Encryption & Storage — Locally Powered, Streamlit-Based**

CybrVault is a lightweight Python + Streamlit project that lets users securely **upload, encrypt, and decrypt** files of any format.  
Each file’s encryption key is stored safely in a **MySQL database**, mapped to the user account that owns it.

---

## Features
- **User authentication** (signup/login system)
- **Encrypt any file type** (MP3, MP4, MKV, TXT, PDF, DOCX, XLSX, PPTX, ODT, CSV, etc.)
- **Per-user encryption keys** stored in a MySQL database
- **Fernet symmetric encryption** (via the `cryptography` library)
- **Decrypt & download** your files safely
- **Local-first privacy** — nothing leaves your machine

---

## Tech Stack
| Component | Technology |
|------------|-------------|
| UI | [Streamlit](https://streamlit.io) |
| Database | MySQL |
| Encryption | Python `cryptography.fernet` |
| Auth | Basic username/password (SHA256) |
| Language | Python 3.10+ |

---

## Installation

### Clone this repository
```bash
git clone https://github.com/yourusername/cybrvault.git
cd cybrvault
python -m venv .venv
source .venv/bin/activate     # On Linux/macOS
.venv\Scripts\activate        # On Windows
pip install -r requirements.txt
```
Make sure that MySQL has been properly configured in your system.
Edit the db.py file to match your MySQL credentials.

Run the app by running:
```bash
streamlit run app.py
```
