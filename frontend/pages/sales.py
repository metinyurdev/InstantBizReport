import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# API URL'si
API_URL = "http://127.0.0.1:8000"  # Backend'inizin çalıştığı URL'i buraya yazın

# Özel CSS ekleme
def inject_custom_css():
    st.markdown(
        """
        <style>
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            font-size: 16px;
            padding: 10px 24px;
            border-radius: 8px;
            border: none;
            transition: background-color 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
        .stTitle {
            color: #4CAF50;
        }
        .stHeader {
            color: #4CAF50;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Arial yazı tipini kaydet (Windows'ta genellikle bu yol kullanılır)
pdfmetrics.registerFont(TTFont('Arial', 'C:/Windows/Fonts/arial.ttf'))

# DataFrame'i PDF olarak kaydetme fonksiyonu
def save_dataframe_as_pdf(df, filename):
    pdf = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # Başlık ekleme (Arial yazı tipi kullan)
    title_style = styles['Title']
    title_style.fontName = 'Arial'  # Arial yazı tipi
    title = Paragraph("Sales Data", title_style)
    elements.append(title)

    # DataFrame'i tablo olarak ekleme
    table_data = [df.columns.to_list()] + df.values.tolist()
    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Arial'),  # Başlık için Arial
        ('FONTNAME', (0, 1), (-1, -1), 'Arial'),  # Veriler için Arial
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(table)

    # PDF'i oluşturma
    pdf.build(elements)

# Sales sayfası
def show_sales():
    inject_custom_css()  # Özel CSS ekle
    st.title("Sales Page")
    st.write("You can see sales data in different ways.")

    # Sales verilerini API'den çek
    response = requests.get(f"{API_URL}/sales", headers={"Authorization": f"Bearer {st.session_state.token}"})
    if response.status_code == 200:
        sales_data = response.json().get("sales", [])  # "sales" anahtarındaki verileri al
        if isinstance(sales_data, list) and len(sales_data) > 0:
            # Verileri pandas DataFrame'e dönüştür
            df = pd.DataFrame(sales_data)

            # Tablo Gösterimi
            st.subheader("Show Table")
            st.table(df)

            # DataFrame Gösterimi
            st.subheader("Show DataFrame")
            st.dataframe(df)

            # Görselleştirme Seçenekleri
            st.subheader("Visualize Data")
            visualization_option = st.selectbox(
                "Select Visualization Option",
                ["Bar Chart", "Pie Chart"],
            )

            if visualization_option == "Bar Chart":
                if "amount" in df.columns and "product" in df.columns:
                    fig = px.bar(df, x="product", y="amount", title="Sales Distribution by Product")
                    st.plotly_chart(fig)
                else:
                    st.warning("Verilerde 'product' veya 'amount' sütunu bulunamadı.")

            elif visualization_option == "Pie Chart":
                if "amount" in df.columns and "product" in df.columns:
                    fig = px.pie(df, values="amount", names="product", title="Sales Distribution by Product")
                    st.plotly_chart(fig)
                else:
                    st.warning("Verilerde 'product' veya 'amount' sütunu bulunamadı.")

            # PDF Olarak İndirme Butonu
            if st.button("Download Data as PDF"):
                filename = "sales_data.pdf"
                save_dataframe_as_pdf(df, filename)
                with open(filename, "rb") as file:
                    btn = st.download_button(
                        label="Click to Download",
                        data=file,
                        file_name=filename,
                        mime="application/octet-stream"
                    )
        else:
            st.warning("Sales verisi bulunamadı veya boş bir liste döndü.")
    else:
        st.error(f"Sales verileri alınamadı: {response.status_code} - {response.text}")

    # Dashboard'a geri dön butonu
    if st.button("🔙 Back to Dashboard"):
        st.session_state.current_page = "dashboard"
        st.rerun()