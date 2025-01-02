import streamlit as st
import requests
from PIL import Image

# API URL'si
API_URL = "http://127.0.0.1:8000"  # Backend'inizin çalıştığı URL'i buraya yazın

# Özel CSS ekleme
def inject_custom_css():
    st.markdown(
        """
        <style>
        /* Genel sayfa stilini ayarla */
        body {
            background-color: #003300;  /* Çam yeşili arka plan */
            font-family: 'Arial', sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        /* Ana kapsayıcı stilini ayarla */
        .container {
            text-align: center;
            max-width: 400px;
            width: 100%;
        }
        /* Logo stilini ayarla */
        .logo {
            width: 250px;  /* Logo genişliği */
            margin-bottom: 10px;
            margin-left: 50px;  /* Logoyu sağa 50 piksel kaydır */
        }
        /* Buton stilini ayarla */
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            font-size: 16px;
            padding: 12px 24px;
            border-radius: 8px;
            border: none;
            transition: background-color 0.3s ease;
            width: 100%;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
        /* Input alanları stilini ayarla */
        .stTextInput>div>div>input {
            background-color: #f9f9f9;
            color: #333;
            border-radius: 8px;
            border: 1px solid #ddd;
            padding: 10px;
        }
        /* Uyarı mesajları stilini ayarla */
        .stAlert {
            border-radius: 8px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Login fonksiyonu
def login(username, password):
    data = {
        "username": username,
        "password": password,
        "grant_type": "password"  # OAuth2 gereksinimi
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    try:
        response = requests.post(f"{API_URL}/token", data=data, headers=headers)
        if response.status_code == 200:
            return response.json()["access_token"]
        else:
            st.error(f"Login failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"API connection error: {e}")
        return None

# Login sayfası
def show_login():
    inject_custom_css()  # Özel CSS ekle

    # Logo yükle
    logo = Image.open("Digital (1).png")

    # Ana kapsayıcı
    st.markdown('<div class="container">', unsafe_allow_html=True)

    # Logo
    st.image(logo, width=250)  # Logo genişliğini ayarlayabilirsiniz

    # Giriş formu
    username = st.text_input("Username")  # "Kullanıcı Adı" yerine "Username"
    password = st.text_input("Password", type="password")  # "Şifre" yerine "Password"

    if st.button("Login"):
        if username and password:
            token = login(username, password)
            if token:
                st.session_state.token = token
                st.session_state.current_page = "dashboard"
                st.rerun()
            else:
                st.error("Invalid username or password.")
        else:
            st.warning("Please enter username and password.")

    st.markdown('</div>', unsafe_allow_html=True)  # Ana kapsayıcı kapat