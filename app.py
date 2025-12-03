import streamlit as st
from db import create_user, check_login, get_db_connection, store_key, get_key, init_db
from encryption import generate_key, encrypt_file, decrypt_file
import os

st.set_page_config(page_title="CybrVault")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_id = None

st.title("CybrVault — Secure File Storage")

get_db_connection(create_db=True)
init_db()

if not st.session_state.logged_in:
    choice = st.radio("Login / Signup", ["Login", "Signup"])
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if choice == "Signup" and st.button("Create Account"):
        try:
            create_user(username, password)
            st.success("Account created! Please login.")
        except Exception as e:
            st.error(f"Error: {e}")
    
    if choice == "Login" and st.button("Login"):
        user_id = check_login(username, password)
        if user_id:
            st.session_state.logged_in = True
            st.session_state.user_id = user_id
            st.rerun()
        else:
            st.error("Invalid username or password")

else:
    st.success("Logged in successfully!")
    st.write("---")

if st.session_state.logged_in:
    if st.session_state.logged_in:
        col_encrypt, col_decrypt = st.columns(2)

        with col_encrypt:
            st.subheader("Encrypt a File")
            uploaded_file = st.file_uploader(
                "Upload a file to encrypt",
                type=["mp3", "mp4", "mkv", "txt", "csv", "xlsx", "docx", "pptx", "pdf", "jpg", "png"],
                key="upload_new"
            )

            if uploaded_file and st.button("Encrypt File"):
                os.makedirs("vault", exist_ok=True)
                file_path = os.path.join("vault", uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                key = generate_key()
                encrypt_file(file_path, key)
                os.remove(file_path)

                try:
                    store_key(st.session_state.user_id, uploaded_file.name, key)
                    st.success(f"{uploaded_file.name} encrypted and key saved successfully.")

                    enc_filename = uploaded_file.name + ".enc"
                    enc_path = os.path.join("vault", enc_filename)
                    with open(enc_path, "rb") as ef:
                        enc_data = ef.read()

                    st.download_button(
                        label="Download Encrypted File",
                        data=enc_data,
                        file_name=enc_filename,
                        mime="application/octet-stream"
                    )
                except Exception as e:
                    st.error(f"Error saving key: {e}")

        with col_decrypt:
            from db import get_user_files

            st.subheader("Decrypt Existing Files")

            user_files = get_user_files(st.session_state.user_id)
            if not user_files:
                st.info("No encrypted files yet.")
            else:
                chosen_orig_name = st.selectbox("Pick a file to decrypt", user_files)
                if st.button("Decrypt & Download"):
                    enc_path = os.path.join("vault", f"{chosen_orig_name}.enc")
                    secrkey_str = get_key(st.session_state.user_id, chosen_orig_name)

                    if not secrkey_str:
                        st.error("No key found for this file.")
                    else:
                        try:
                            key_bytes = secrkey_str.encode()
                            out_name = f"decrypted_{chosen_orig_name}"
                            out_path = os.path.join("vault", out_name)

                            decrypt_file(enc_path, key_bytes, out_path)
                            with open(out_path, "rb") as f:
                                data = f.read()

                            st.success(f"{chosen_orig_name} decrypted and ready to download.")
                            st.download_button(
                                label="Download decrypted file",
                                data=data,
                                file_name=chosen_orig_name,
                                mime="application/octet-stream"
                            )

                            os.remove(out_path)
                        except Exception as e:
                            st.error("Decryption failed.")

    st.divider()
    st.subheader("OR upload an encrypted file to decrypt")

    uploaded_enc = st.file_uploader("Upload a `.enc` file", type=["enc"], key="upload_enc")

    if uploaded_enc and st.button("Decrypt Uploaded File", key="decrypt_uploaded"):
        os.makedirs("vault", exist_ok=True)
        enc_temp_path = os.path.join("vault", uploaded_enc.name)
        with open(enc_temp_path, "wb") as f:
            f.write(uploaded_enc.getbuffer())

        orig_name = uploaded_enc.name[:-4]

        secrkey_str = get_key(st.session_state.user_id, orig_name)
        if not secrkey_str:
            st.error("No key found for this file.")
        else:
            try:
                key_bytes = secrkey_str.encode()
                out_name = f"decrypted_{orig_name}"
                out_path = os.path.join("vault", out_name)

                decrypt_file(enc_temp_path, key_bytes, out_path)

                with open(out_path, "rb") as f:
                    data = f.read()

                st.success(f"{orig_name} decrypted successfully.")
                st.download_button(
                    label="Download Decrypted File",
                    data=data,
                    file_name=orig_name,
                    mime="application/octet-stream"
                )

                try:
                    os.remove(out_path)
                except Exception:
                    pass

            except Exception as e:
                st.error("Decryption failed.")

with st.sidebar:
    st.title("Menu")

    page = st.radio("Navigate", ["About", "FAQs", "Contact Us"])

    if page == "About":
        st.markdown("""
        ### About CybrVault
        CybrVault is a lightweight encryption-based file storage app built with Streamlit and Python.
        It allows users to:
        - Securely upload and encrypt files
        - Decrypt only with user-specific keys
        - Keep data local or host it on the cloud

        Built by Akshat Rakesh, Praneil Kaware & Ashwin Ravi
        """)

    elif page == "FAQs":
        st.markdown("""
        ### Frequently Asked Questions

        1. What file types can I encrypt?
        You can encrypt any document, image, audio, or video such as .pdf, .docx, .mp4, .jpg, etc.

        2. Where are my files stored?
        Locally inside a folder called vault/.

        3. Is my data sent online?
        No. Everything happens locally unless you decide to host the app online.

        4. I forgot my password — can I recover my files?
        No. The encryption uses SHA256 for password and key hashing, which cannot be recovered if forgotten.
        """)

    elif page == "Contact Us":
        st.markdown("""
        ### Contact
        Have feedback or found a bug?
        - GitHub: github.com/akshrk1/cybrvault
        - Project Issues: github.com/akshrk1/cybrvault/issues
        """)
