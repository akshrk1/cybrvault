# CybrVault Web
**Secure File Encryption & Storage — Cloud-Ready, Streamlit-Based**

CybrVault is a lightweight Python + Streamlit project that lets users securely **upload, encrypt, and decrypt** files of any format.  
Each file’s encryption key is stored safely in a **MySQL database**, mapped to the user account that owns it.  
Files are stored on the cloud platform **Railway**.

Access the live app here: [https://cybrvault.streamlit.app](https://cybrvault.streamlit.app)

---

## Features
- **User authentication** (signup/login system)
- **Encrypt any file type** (MP3, MP4, MKV, TXT, PDF, DOCX, XLSX, PPTX, ODT, CSV, etc.)
- **Per-user encryption keys** stored in a MySQL database
- **Fernet symmetric encryption** (via the `cryptography` library)
- **Decrypt & download** your files safely
- **Cloud-enabled deployment** — host the app and database online
- **Optional local storage** — files can still be stored on the server if you prefer

---

## Tech Stack
| Component | Technology |
|------------|-------------|
| UI | [Streamlit](https://streamlit.io) |
| Database | MySQL (Railway's implementation) |
| Encryption | Python `cryptography.fernet` |
| Auth | Basic username/password (SHA256) |
| Language | Python 3.10+ |
