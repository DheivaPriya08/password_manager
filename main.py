import gradio as gr
from fastapi import FastAPI
import pandas as pd
import sqlite3
from cryptography.fernet import Fernet
import os
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

DB_FILE = "vault.db"
SALT_FILE = "salt.bin"
ITERATIONS = 390000
cipher = None
is_authenticated = False

def derive_key(master_password):
    if not os.path.exists(SALT_FILE):
        with open(SALT_FILE, "wb") as f:
            f.write(os.urandom(16))
    with open(SALT_FILE, "rb") as f:
        salt = f.read()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(), length=32, salt=salt,
        iterations=ITERATIONS, backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(master_password.encode()))

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS vault (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                website TEXT NOT NULL,
                username TEXT NOT NULL,
                password BLOB NOT NULL
            )
        ''')

def authenticate(master_password):
    global cipher, is_authenticated
    try:
        key = derive_key(master_password)
        cipher = Fernet(key)
        _ = load_vault()
        is_authenticated = True
        return "🔓 Vault unlocked", load_vault()
    except Exception:
        is_authenticated = False
        return "❌ Invalid master password", []

def add_entry(website, username, password):
    if not is_authenticated:
        return "🔒 Authenticate first", []
    encrypted_pw = cipher.encrypt(password.encode())
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("INSERT INTO vault (website, username, password) VALUES (?, ?, ?)",
                     (website, username, encrypted_pw))
    return "✅ Entry added", load_vault()

def load_vault():
    if not is_authenticated:
        return []
    with sqlite3.connect(DB_FILE) as conn:
        df = pd.read_sql_query("SELECT website, username, password FROM vault", conn)
    df["password"] = df["password"].apply(lambda p: cipher.decrypt(p).decode())
    return df

def build_ui():
    with gr.Blocks() as demo:
        gr.Markdown("## 🔐 Web Password Manager")

        mp_input = gr.Textbox(label="Master Password", type="password")
        unlock_btn = gr.Button("Unlock Vault")
        unlock_status = gr.Textbox(label="Status", interactive=False)
        vault_table = gr.Dataframe(label="Vault", interactive=False)

        website = gr.Textbox(label="Website")
        username = gr.Textbox(label="Username")
        password = gr.Textbox(label="Password", type="password")
        add_btn = gr.Button("Add Entry")
        status = gr.Textbox(label="Entry Status", interactive=False)

        unlock_btn.click(authenticate, inputs=[mp_input], outputs=[unlock_status, vault_table])
        add_btn.click(add_entry, inputs=[website, username, password], outputs=[status, vault_table])
    return demo

init_db()
app = FastAPI()

@app.get("/")
def root():
    return {"status": "running", "message": "visit /gradio for the UI"}

@app.get("/gradio")
def gradio_ui():
    return build_ui().launch(share=False, inline=True)