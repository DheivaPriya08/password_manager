# 🔐 Password Manager Web App

A minimal password manager built with Python, Gradio, and FastAPI.  
This project securely stores user credentials in an encrypted format and offers a simple web-based interface to add and view them.

---

## 📌 Purpose

This application was developed as a **personal learning and portfolio project**. It demonstrates:

- Full-stack Python web development
- Secure password encryption
- Interactive UI with Gradio
- Deployment readiness (locally or via platforms like Render)

> ⚠️ Not intended for production use. Do **not** store real passwords.

---

## ✨ Features

- 🔒 **Encryption** using Fernet from `cryptography`  
- 📋 **Add & view** website credentials  
- 📁 **CSV file storage** with encrypted password fields  
- ⚡ **Instant UI** using Gradio blocks

---

## 🛠️ Tech Stack

| Layer      | Tools                    |
|------------|--------------------------|
| Language   | Python 3                 |
| UI         | [Gradio](https://password-manager-1-qsvy.onrender.com/gradio)       |
| Backend    | FastAPI + Uvicorn        |
| Security   | Cryptography (Fernet)    |
| Storage    | Pandas + CSV             |

---

## 🔧 Setup Instructions

1. **Clone the repo**:
   ```bash
   git clone https://github.com/DheivaPriya08/password_manager.git
   cd password_manager
