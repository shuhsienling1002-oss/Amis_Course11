import streamlit as st
import time
import os
from gtts import gTTS
from io import BytesIO
import random

# --- 0. 系統配置 ---
st.set_page_config(page_title="Unit 11: O Sa'osi II", page_icon="💰", layout="centered")

# CSS 優化
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        font-size: 20px;
        background-color: #E0F7FA;
        color: #006064;
        border: 2px solid #00BCD4;
        padding: 10px;
        margin-top: 5px;
    }
    .stButton>button:hover {
        background-color: #B2EBF2;
        transform: scale(1.02);
    }
    .vocab-card {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 10px;
        border-left: 5px solid #00BCD4;
    }
    </style>
""", unsafe_allow_html=True)

# --- 1. 內容資料庫 (Unit 11) ---
# 難度升級：詞彙量增加至 10 個
vocab_list = {
    "Enem": "六 (6)",
    "Pito": "七 (7)",
    "Falo": "八 (8)",
    "Siwa": "九 (9)",
    "Mo^tep": "十 (10)",
    "Safaw-cecay": "十一 (11)",
    "Safaw-tosa": "十二 (12)",
    "Isot": "二十 (20)",
    "Payso": "錢",
    "Pina": "多少 (複習)"
}

# 難度升級：句子增加至 5 句，並包含前 10 單元的詞彙 (如 wawa, foting)
sentences = [
    {"amis": "Pina ko payso?", "chinese": "有多少錢？", "audio": "u11_s1"},
    {"amis": "Enem ko wawa.", "chinese": "有六個小孩。", "audio": "u11_s2"},
    {"amis": "Pito ko foting.", "chinese": "有七條魚。", "audio": "u11_s3"},
    {"amis": "Mo^tep ko payso no mako.", "chinese": "我有十元。", "audio": "u11_s4"},
    {"amis": "Safaw-tosa ko jam.", "chinese": "現在十二點鐘。", "audio": "u11_s5"},
]

# --- 2. 核心函數 ---
def play_audio(text, filename_base):
    # 實際部署時建議預先生成音檔，此處為即時生成模擬
    tts = gTTS(text=text, lang='ja') # 近似發音
    fp = BytesIO()
    tts.write_to_fp(fp)
    st.audio(fp, format='audio/mp3')

# 初始化 Session
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'current_q' not in st.session_state:
    st.session_state.current_q = 0

# --- 3. 介面呈現 ---
st.markdown("<h1 style='text-align: center; color: #0097A7;'>Unit 11: O Sa'osi II (進階數字)</h1>", unsafe_allow_html=True)
st.progress((st.session_state.current_q / 3) if st.session_state.current_q < 3 else 1.0)

# 分頁邏輯
tab1, tab2 = st.tabs(["📖 詞彙與句型", "🎮 闖關挑戰"])

with tab1:
    st.subheader("📝 單字表 (Vocabulary)")
    cols = st.columns(2)
    for i, (amis, chi) in enumerate(vocab_list.items()):
        with cols[i % 2]:
            st.markdown(f"""
            <div class="vocab-card">
                <div style="font-size: 24px; font-weight: bold; color: #333;">{amis}</div>
                <div style="font-size: 18px; color: #666;">{chi}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"🔊 聽 {amis}", key=f"btn_{amis}"):
                play_audio(amis, f"u11_{amis}")

    st.markdown("---")
    st.subheader("🗣️ 句型練習 (Sentences)")
    for s in sentences:
        st.markdown(f"**{s['amis']}** ({s['chinese']})")
        if st.button(f"▶️ 播放", key=s['audio']):
            play_audio(s['amis'], s['audio'])

with tab2:
    if st.session_state.current_q == 0:
        st.info("第一關：聽力測驗 (聽數字)")
        play_audio("Falo", "u11_q_falo")
        
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("6 (Enem)"): st.error("不對喔！")
        with c2:
            if st.button("8 (Falo)"): 
                st.success("Correct! Falo 是 8")
                time.sleep(1)
                st.session_state.score += 100
                st.session_state.current_q += 1
                st.rerun()
        with c3:
            if st.button("10 (Mo^tep)"): st.error("不對喔！")

    elif st.session_state.current_q == 1:
        st.info("第二關：情境應用 (錢)")
        st.markdown("### Q: Pina ko payso? (這裡有多少錢？)")
        st.markdown("💰 **$20**")
        
        opts = ["Mo^tep (10)", "Isot (20)", "Siwa (9)"]
        choice = st.radio("請選擇阿美語：", opts)
        
        if st.button("送出答案"):
            if "Isot" in choice:
                st.balloons()
                st.session_state.score += 100
                st.session_state.current_q += 1
                st.rerun()
            else:
                st.error("再算一次！Isot 是 20 喔。")

    elif st.session_state.current_q == 2:
        st.info("第三關：句子重組")
        st.markdown("請選出正確的句子：**「有七個小孩」**")
        st.caption("提示：Recall Unit 3 'wawa' (小孩)")
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Pito ko wawa"):
                st.success("太棒了！Pito (7) + Wawa (小孩)")
                time.sleep(1)
                st.session_state.score += 100
                st.session_state.current_q += 1
                st.rerun()
        with c2:
            if st.button("Enem ko wawa"): st.error("Enem 是 6 喔！")

    else:
        st.success(f"🎉 恭喜完成 Unit 11！總分：{st.session_state.score}")
        if st.button("重玩一次"):
            st.session_state.score = 0
            st.session_state.current_q = 0
            st.rerun()
