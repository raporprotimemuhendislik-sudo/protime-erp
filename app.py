with col1:
    st.subheader("📦 Katalog Ürünleri")
    conn = get_db_connection()
    rows = conn.execute("SELECT id, marka, urun_adi, nakit_usd FROM urunler WHERE modul=?", (aktif_modul,)).fetchall()
    conn.close()
    
    # Ürünleri liste şeklinde küçük satırlar halinde göster
    for r in rows:
        # Satır yapısı: [Marka - Ürün] [Fiyat] [Sil] [Ekle]
        row_col = st.columns([4, 2, 1, 1])
        row_col[0].write(f"**{r[1]}** - {r[2]}")
        row_col[1].write(f"${r[3]:.2f}")
        
        # Silme butonu (Kırmızı çöp kutusu)
        if row_col[2].button("🗑️", key=f"del_{r[0]}"):
            conn = get_db_connection()
            conn.execute("DELETE FROM urunler WHERE id=?", (r[0],))
            conn.commit()
            conn.close()
            st.rerun()
            
        # Ekleme butonu (Yeşil artı)
        if row_col[3].button("➕", key=f"add_{r[0]}"):
            st.session_state.paket.append({"marka": r[1], "urun": r[2], "n_usd": r[3]})
            st.rerun()
