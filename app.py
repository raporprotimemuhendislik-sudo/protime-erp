import streamlit as st
import requests
import sqlite3
import io
import os
from datetime import datetime
from zoneinfo import ZoneInfo
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# --- PDF OLUŞTURMA (FATURA FORMATI) ---
def pdf_olustur(paket, toplam, baslik, birim, kur=None):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=50, leftMargin=50, topMargin=50, bottomMargin=50)
    elements = []
    styles = getSampleStyleSheet()

    # Logo ekleme
    if os.path.exists("logo.png"):
        img = Image("logo.png", width=150, height=50)
        elements.append(img)
    
    # Firma Bilgileri
    firma_bilgi = """
    <b>PROTIME MÜHENDİSLİK</b><br/>
    Küçük Kayaş Mah. 19 Mayıs Bulvarı 222/A Mamak / ANKARA<br/>
    Tel: 0530 135 89 86 - 0533 285 10 31
    """
    elements.append(Paragraph(firma_bilgi, styles['Normal']))
    elements.append(Paragraph("<br/><br/>", styles['Normal']))
    
    # Başlık
    elements.append(Paragraph(baslik, styles['Title']))
    elements.append(Paragraph("<br/>", styles['Normal']))
    
    # Tablo
    data = [["Marka", "Ürün", "Fiyat"]]
    for item in paket:
        data.append([item['marka'], item['urun'], f"{item['fiyat']:.2f} {birim}"])
    data.append(["", "TOPLAM", f"{toplam:,.2f} {birim}"])
    
    if kur:
        data.append(["", "TOPLAM TL (Kur: {})".format(kur), f"{(toplam*kur):,.2f} TL"])
    
    table = Table(data, colWidths=[120, 200, 80])
    table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('ALIGN', (2,0), (2,-1), 'RIGHT')
    ]))
    elements.append(table)
    
    doc.build(elements)
    return buffer

# --- GERİ KALAN KISIMLAR ---
# Veritabanı ve Arayüz aynıdır...
# ... (PDF_olustur fonksiyonunu yukarıdaki ile değiştirip devamını önceki kodunla birleştirmen yeterli)
