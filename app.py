import streamlit as st
import time
from gtts import gTTS
from io import BytesIO

# --- 0. 系統與視覺配置 ---
st.set_page_config(page_title="Unit 11: O Sa'osi II", page_icon="💰", layout="centered")

# 進階 CSS 設計
st.markdown("""
    <style>
    /* 全局字體優化 */
    body {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    
    /* 單字卡片設計 */
    .word-card {
        background: linear-gradient(135deg, #ffffff 0%, #f3f4f6 100%);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 15px;
        border-bottom: 4px solid #FFD700; /* 金幣黃底線 */
        transition: transform 0.2s;
    }
    .word-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0,0,0,0.15);
    }
    .emoji-icon {
        font-size: 48px;
        margin-bottom: 10px;
    }
    .amis-text {
        font-size: 22px;
        font-weight: bold;
        color: #2c3e50;
    }
    .chinese-text {
        font-size: 16px;
        color: #7f8c8d;
    }
    
    /* 句子區塊設計 */
    .sentence-box {
        background-color: #E3F2FD; /* 淡藍背景 */
        border-left: 5px solid #2196F3;
        padding: 15px;
        margin: 10px 0;
        border-radius: 0 10px 10px 0;
    }
    
    /* 互動按鈕優化 */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        font-size: 20px;
        font-weight: 600;
        background-color: #FFECB3;
        color: #5D4037;
        border: 2px solid #FFC107;
        padding: 12px;
    }
    .stButton>button:hover {
        background-color: #FFD54F;
        border-color: #FFA000;
    }
    
    /* 進度條顏色 */
    .stProgress > div > div > div > div {
        background-color: #FBC02D;
    }
    </style>
""", unsafe_allow_html=True)

# --- 1. 教學內容資料庫 ---
# 10 個核心詞彙
vocab_data = [
    {"amis": "'Enem", "chi": "六 (數字)", "icon": "6️⃣", "type": "num"},
    {"amis": "Pito", "chi": "七 (7)", "icon": "7️⃣", "type": "num"},
    {"amis": "Falo", "chi": "八 (8)", "icon": "8️⃣", "type": "num"},
    {"amis": "Siwa", "chi": "九 (9)", "icon": "9️⃣", "type": "num"},
    {"amis": "Mo^etep", "chi": "十 (10)", "icon": "🔟", "type": "num"},
    {"amis": "Safaw cecay", "chi": "十一 (11)", "icon": "1️⃣1️⃣", "type": "num"},
    {"amis": "Safaw tosa", "chi": "十二 (12)", "icon": "1️⃣2️⃣", "type": "num"},
    {"amis": "Isot", "chi": "二十 (20)", "icon": "2️⃣0️⃣", "type": "num"},
    {"amis": "Payso", "chi": "錢 / 硬幣", "icon": "💰", "type": "noun"},
    {"amis": "Toki", "chi": "時間 / 鐘", "icon": "⏰", "type": "noun"},
]

# 5 個核心句型 (修正 'A'enem ko wawa)
sentences = [
    {"amis": "Pina ko payso?", "chi": "有多少錢？", "icon": "🤔"},
    {"amis": "'A'enem ko wawa.", "chi": "有六個小孩。", "icon": "👶"},
    {"amis": "Safaw tosa ko toki.", "chi": "現在十二點鐘。", "icon": "🕛"},
    {"amis": "Mo^etep ko payso no mako.", "chi": "我有十元。", "icon": "💵"},
    {"amis": "Pito ko foting.", "chi": "有七條魚。", "icon": "🐟"},
]

# --- 2. 工具函數 ---
def play_audio(text):
    try:
        # 使用印尼語 (id) 發音引擎，韻律較接近阿美語
        tts = gTTS(text=text, lang='id') 
        fp = BytesIO()
        tts.write_to_fp(fp)
        st.audio(fp, format='audio/mp3')
    except Exception as e:
        st.error(f"語音生成錯誤: {e}")

# 初始化 Session State
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'stage' not in st.session_state:
    st.session_state.stage = 0

# --- 3. 主介面設計 ---
st.markdown("<h1 style='text-align: center; color: #Fbc02d;'>Unit 11: O Sa'osi II</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>進階數字與金錢：學會算錢與看時間</p>", unsafe_allow_html=True)

# 進度條
progress = min(1.0, st.session_state.stage / 3)
st.progress(progress)

# 分頁籤
tab1, tab2 = st.tabs(["📚 圖卡學習 (Learning)", "🎮 闖關挑戰 (Challenge)"])

# === Tab 1: 學習模式 ===
with tab1:
    st.subheader("📝 核心單字 (Vocabulary)")
    
    col1, col2 = st.columns(2)
    for i, word in enumerate(vocab_data):
        with (col1 if i % 2 == 0 else col2):
            st.markdown(f"""
            <div class="word-card">
                <div class="emoji-icon">{word['icon']}</div>
                <div class="amis-text">{word['amis']}</div>
                <div class="chinese-text">{word['chi']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"🔊 聽發音", key=f"btn_{word['amis']}"):
                play_audio(word['amis'])

    st.markdown("---")
    st.subheader("🗣️ 實用句型 (Sentences)")
    
    for s in sentences:
        st.markdown(f"""
        <div class="sentence-box">
            <div style="font-size: 20px; font-weight: bold; color: #1565C0;">
                {s['icon']} {s['amis']}
            </div>
            <div style="font-size: 16px; color: #555; margin-top: 5px;">
                {s['chi']}
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"▶️ 播放句型", key=f"s_btn_{s['amis'][:5]}"):
            play_audio(s['amis'])

# === Tab 2: 挑戰模式 ===
with tab2:
    st.markdown("### 互動測驗")
    
    # Stage 0: 聽力辨識 (純數字 'Enem)
    if st.session_state.stage == 0:
        st.info("👂 第一關：聽音辨位")
        st.write("請仔細聽，我唸的是哪個數字？")
        
        # 題目：'Enem (6)
        if st.button("🎧 播放題目音檔"):
            play_audio("'Enem")
            
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("8 (Falo)"): 
                st.error("不對喔，Falo 是 8")
        with c2:
            if st.button("6 ('Enem)"):
                st.balloons()
                st.success("🎉 Correct! 'Enem 是 6")
                time.sleep(1.5)
                st.session_state.score += 100
                st.session_state.stage += 1
                st.rerun()
        with c3:
            if st.button("9 (Siwa)"): 
                st.error("不對喔，Siwa 是 9")

    # Stage 1: 視覺計數 (算人，使用 'A'enem)
    elif st.session_state.stage == 1:
        st.info("👀 第二關：數數看")
        st.write("**Q: Pina ko wawa? (有幾個小孩？)**")
        
        # 視覺化顯示 6 個小孩
        st.markdown("<div style='font-size: 40px; text-align: center; letter-spacing: 10px; margin: 20px 0;'>👶 👶 👶 👶 👶 👶</div>", unsafe_allow_html=True)
        
        # 選項修正為 'A'enem
        opts = ["Mo^etep (10)", "'A'enem (6)", "Pito (7)"]
        choice = st.radio("請選擇正確的阿美語數字（注意是算人喔）：", opts)
        
        if st.button("送出答案"):
            if "'A'enem" in choice:
                st.balloons()
                st.success("答對了！ 'A'enem ko wawa. (有六個小孩)")
                time.sleep(1.5)
                st.session_state.score += 100
                st.session_state.stage += 1
                st.rerun()
            else:
                st.error("再數一次看看！(提示：5 + 1)")

    # Stage 2: 時鐘與時間
    elif st.session_state.stage == 2:
        st.info("⏰ 第三關：看時間")
        
        # 題目：Safaw tosa
        st.markdown("#### Q: Safaw tosa ko toki.")
        play_audio("Safaw tosa ko toki")
        
        st.write("請問這句話是什麼意思？")
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("<div style='font-size: 80px; text-align: center;'>🕛</div>", unsafe_allow_html=True)
            if st.button("現在是十二點鐘"):
                st.balloons()
                st.success("太棒了！Safaw tosa 是 12。")
                time.sleep(1.5)
                st.session_state.score += 100
                st.session_state.stage += 1
                st.rerun()
        with c2:
            st.markdown("<div style='font-size: 80px; text-align: center;'>🕙</div>", unsafe_allow_html=True)
            if st.button("現在是十點鐘"):
                st.error("十點是 Mo^etep ko toki 喔！")

    # 完成畫面
    else:
        st.markdown(f"""
        <div style='text-align: center; padding: 30px; background-color: #FFF9C4; border-radius: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
            <h1 style='color: #F57F17;'>🏆 單元完成！</h1>
            <h3 style='color: #333;'>你的得分：{st.session_state.score}</h3>
            <p style='font-size: 18px; color: #555;'>你已經學會數錢和看時間了！</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 重新練習 Unit 11"):
            st.session_state.score = 0
            st.session_state.stage = 0
            st.rerun()
