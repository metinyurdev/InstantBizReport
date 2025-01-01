import streamlit as st
import requests
from PIL import Image

# API URL'si
API_URL = "http://localhost"  # Backend'inizin çalıştığı URL'i buraya yazın

# Özel CSS ekleme
def inject_custom_css():
    st.markdown(
        """
        <style>
        /* Genel sayfa stilini ayarla */
        body {
            background-color: #2E8B57;  
            font-family: 'Arial', sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        /* Ana container stilini ayarla */
        .container {
            text-align: center;
            max-width: 400px;
            width: 100%;
        }
        /* Logo stilini ayarla */
        .logo {
            width: 300px;  /* Logo genişliği */
            margin-bottom: 20px;
        }
        /* Buton stilini ayarla */
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            font-size: 20px;
            padding: 20px 40px;
            border-radius: 12px;
            border: none;
            transition: background-color 0.3s ease;
            width: 100%;
            margin: 10px 0;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
        /* Logout buton stilini ayarla */
        .logout-button {
            position: fixed;
            bottom: 10px;
            left: 10px;
            font-size: 14px;
            padding: 10px 20px;
            background-color: #ff4b4b;
            color: white;
            border-radius: 8px;
            border: none;
            cursor: pointer;
        }
        .logout-button:hover {
            background-color: #ff0000;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# User Info butonu için işlev
def show_user_info():
    response = requests.get(f"{API_URL}/users/me", headers={"Authorization": f"Bearer {st.session_state.token}"})
    if response.status_code == 200:
        user_info = response.json()
        st.write(f"**Kullanıcı:** {user_info.get('user', 'Bilgi Yok')}")
    else:
        st.error(f"Kullanıcı bilgileri alınamadı: {response.status_code} - {response.text}")

# Logout işlevi
def logout():
    response = requests.post(f"{API_URL}/logout", headers={"Authorization": f"Bearer {st.session_state.token}"})
    if response.status_code == 200:
        st.session_state.token = None
        st.session_state.current_page = "login"
        st.rerun()
    else:
        st.error(f"Çıkış yapılamadı: {response.status_code} - {response.text}")

# Dashboard sayfası
def show_dashboard():
    inject_custom_css()  # Özel CSS ekle

    # Logo yükle
    logo = Image.open("Digital (1).png")

    # Ana container
    st.markdown('<div class="container">', unsafe_allow_html=True)

    # Logo göster
    st.image(logo, width=300)  # Logo genişliğini ayarlayabilirsiniz

    # Butonları düzenle (büyük ve alt alta)
    if st.button("📊 Sales"):
        st.session_state.current_page = "sales"
        st.rerun()

    if st.button("👤 Personals"):
        st.session_state.current_page = "personals"
        st.rerun()

    if st.button("💰 Finance"):
        st.session_state.current_page = "finance"
        st.rerun()

    if st.button("👤 User Info"):
        show_user_info()

    st.markdown('</div>', unsafe_allow_html=True)

    # Logout butonunu ekle
    if st.button("🚪 Logout", key="logout", help="Çıkış yap"):
        logout()

