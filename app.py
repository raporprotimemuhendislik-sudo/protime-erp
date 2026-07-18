with c1:
    st.subheader("📦 Katalog (Küçük Liste)")
    
    # 1. Scroll edilebilir konteyner oluştur
    with st.container(height=300):  # height=300 kutunun yüksekliğini belirler
        conn = get_db_connection()
        rows = conn.execute("SELECT id, marka, urun_adi, nakit_usd FROM urunler WHERE modul=?", (aktif_modul,)).fetchall()
        
        for r in rows:
            cols = st.columns([3, 2, 1, 1])
            cols[0].caption(f"{r[1]} - {r[2]}")
            cols[1].caption(f"${r[3]}")
            
            # Silme ve Ekleme butonları
            if cols[2].button("🗑️", key=f"del_{r[0]}"):
                conn.execute("DELETE FROM urunler WHERE id=?", (r[0],))
                conn.commit()
                st.rerun()
            if cols[3].button("➕", key=f"add_{r[0]}"):
                st.session_state.paket.append({"marka": r[1], "urun": r[2], "n_usd": r[3]})
                st.rerun()
        conn.close()
