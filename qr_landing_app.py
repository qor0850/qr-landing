
import streamlit as st
from urllib.parse import urlencode

# -----------------------------
# Config
# -----------------------------
st.set_page_config(
    page_title="QR Landing",
    page_icon="📇",
    layout="wide",
)

# ======== USER SETTINGS (EDIT HERE) ========
PROFILE_NAME = "백XX"
TAGLINE = "자동화개발자 | RPA·AI·교육"
PROFILE_PHOTO_URL = ""  # Optional: link to a hosted image (png/jpg), or leave empty

# Video URLs (YouTube recommended). You can also put direct mp4 links.
SHORTS_VIDEO_URL = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # 1분 이내 쇼츠/리일스 느낌
CAREER_VIDEO_URL = "https://www.youtube.com/watch?v=oHg5SJYRHA0"  # 2~3분 경력 소개

# Contact & Location
PHONE_NUMBER = "+82-10-0000-0000"      # tel: 링크로 사용
EMAIL_ADDRESS = "you@example.com"      # mailto: 링크로 사용
KAKAO_CHANNEL_URL = "https://pf.kakao.com/_yourchannel"  # 카카오톡 채널(선택)
INSTAGRAM_URL = "https://www.instagram.com/your_instagram"  # 인스타그램(선택)
NAVER_MAPS_URL = "https://naver.me/xxxx"   # 네이버지도 공유 링크(선택)
RESERVATION_URL = ""  # 네이버 예약/폼/캘린더 등 (선택)

# Colors (high-contrast for accessibility)
COLOR_1 = "#2F80ED"  # Blue
COLOR_2 = "#27AE60"  # Green
COLOR_3 = "#F2994A"  # Orange
COLOR_4 = "#EB5757"  # Red
TEXT_COLOR = "#FFFFFF"

# ===========================================

# -----------------------------
# Helpers
# -----------------------------
def set_route(route: str):
    # write into st.query_params so URL reflects state
    st.query_params["route"] = route

def get_route() -> str:
    # use new stable API
    params = st.query_params
    if "route" in params and params["route"]:
        return params["route"]
    # fallback to 'home'
    return "home"

def back_to_home():
    st.markdown(f"[⬅️ 홈으로](?{urlencode({'route':'home'})})")

def contact_buttons():
    cols = st.columns(2)
    with cols[0]:
        st.link_button("📞 전화하기", f"tel:{PHONE_NUMBER}")
    with cols[1]:
        st.link_button("✉️ 이메일", f"mailto:{EMAIL_ADDRESS}")
    if KAKAO_CHANNEL_URL:
        st.link_button("💬 카카오톡 채널", KAKAO_CHANNEL_URL, use_container_width=True)
    if INSTAGRAM_URL:
        st.link_button("📷 인스타그램", INSTAGRAM_URL, use_container_width=True)
    if RESERVATION_URL:
        st.link_button("🗓 예약하기", RESERVATION_URL, use_container_width=True)
    if NAVER_MAPS_URL:
        st.link_button("📍 위치(네이버지도)", NAVER_MAPS_URL, use_container_width=True)

# -----------------------------
# CSS (full-screen 4-tile menu)
# -----------------------------
GLOBAL_CSS = f"""
<style>
/* Remove extra paddings for true full-screen tiles */
.appview-container .main .block-container {{
    padding-top: 0rem;
    padding-bottom: 0rem;
}}
/* Full-viewport menu grid */
.menu-grid {{
    height: 100vh;
    width: 100vw;
    margin: 0;
    padding: 0;
    display: flex;
    flex-direction: column;
}}
.menu-card {{
    height: 25vh;     /* Each tile = 25% viewport height */
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    font-weight: 800;
    font-size: clamp(20px, 5vw, 28px); /* Responsive large text */
    letter-spacing: 0.4px;
    color: {TEXT_COLOR};
    user-select: none;
    text-decoration: none !important;
}}
.menu-card:active {{
    filter: brightness(0.95);
    transform: scale(0.996);
}}
.menu-1 {{ background: {COLOR_1}; }}
.menu-2 {{ background: {COLOR_2}; }}
.menu-3 {{ background: {COLOR_3}; }}
.menu-4 {{ background: {COLOR_4}; }}

/* Make anchor fill the tile area */
.menu-card a {{
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;
    text-decoration: none !important;
    color: {TEXT_COLOR} !important;
}}
/* Large emoji icon spacing */
.menu-icon {{
    margin-right: 12px;
    font-size: 1.2em;
}}

/* Content pages spacing */
.content {{
    padding: 16px 8px 32px;
}}

.info-card {{
    border-radius: 16px;
    padding: 16px;
    background: #ffffff;
    box-shadow: 0 8px 20px rgba(0,0,0,0.06);
    border: 1px solid rgba(0,0,0,0.05);
}}
.info-title {{
    font-weight: 700;
    margin-bottom: 8px;
}}
.info-row {{
    margin: 6px 0;
    line-height: 1.6;
    font-size: 16px;
}}
.badge {{
    display:inline-block;
    background:#f2f4f7;
    padding:2px 8px;
    border-radius:999px;
    font-size:12px;
    margin-left:6px;
    vertical-align: middle;
}}
</style>
"""
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

# -----------------------------
# Views
# -----------------------------
def view_home():
    # Full-screen senior-friendly 4-tile menu (width 100%, height 25% each)
    st.markdown(
        f"""
        <div class="menu-grid">
            <div class="menu-card menu-1">
                <a href="?{urlencode({"route": "about"})}"><span class="menu-icon">🧑</span>소개</a>
            </div>
            <div class="menu-card menu-2">
                <a href="?{urlencode({"route": "shorts"})}"><span class="menu-icon">🎬</span>쇼츠 영상</a>
            </div>
            <div class="menu-card menu-3">
                <a href="?{urlencode({"route": "career"})}"><span class="menu-icon">🏆</span>경력 영상</a>
            </div>
            <div class="menu-card menu-4">
                <a href="?{urlencode({"route": "contact"})}"><span class="menu-icon">📍</span>예약·연락/위치</a>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def view_about():
    back_to_home()
    st.markdown('<div class="content">', unsafe_allow_html=True)
    st.markdown("## 소개 (About Me)")

    if PROFILE_PHOTO_URL:
        st.image(PROFILE_PHOTO_URL, width=140)

    # Structured intro content per user's request
    st.markdown(
        """
        <div class="info-card">
            <div class="info-title">기본 정보</div>
            <div class="info-row">👤 <b>이름</b>: 백XX</div>
            <div class="info-row">🎂 <b>나이</b>: 34세</div>
            <div class="info-row">💼 <b>직업</b>: 자동화개발자</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="info-card">
            <div class="info-title">경력</div>
            <div class="info-row">• 삼성전자 RPA 개발·운영 <span class="badge">2018 ~ 2022</span></div>
            <div class="info-row">• 삼성전자 DS 현업 교육 <span class="badge">2023 ~ 2025.08</span></div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()
    st.markdown("### 연락")
    contact_buttons()
    st.markdown('</div>', unsafe_allow_html=True)

def view_shorts():
    back_to_home()
    st.markdown('<div class="content">', unsafe_allow_html=True)
    st.markdown("## 쇼츠 / 리일스")
    st.markdown("가볍게 볼 수 있는 1분 내외의 짧은 영상입니다.")
    st.video(SHORTS_VIDEO_URL)
    st.markdown('</div>', unsafe_allow_html=True)

def view_career():
    back_to_home()
    st.markdown('<div class="content">', unsafe_allow_html=True)
    st.markdown("## 경력 소개 (2~3분)")
    st.markdown("""
- 주요 프로젝트/교육/협업 사례를 영상으로 정리했습니다.
- 신뢰와 전문성을 한 번에 확인하세요.
""")
    st.video(CAREER_VIDEO_URL)
    st.markdown('</div>', unsafe_allow_html=True)

def view_contact():
    back_to_home()
    st.markdown('<div class="content">', unsafe_allow_html=True)
    st.markdown("## 예약 & 연락 / 위치")
    contact_buttons()
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# App Router
# -----------------------------
route = get_route()

if route == "home":
    view_home()
elif route == "about":
    view_about()
elif route == "shorts":
    view_shorts()
elif route == "career":
    view_career()
elif route == "contact":
    view_contact()
else:
    set_route("home")
    view_home()

# Small footer
st.caption(f"© {PROFILE_NAME} — 모바일 퍼스트 QR 랜딩")
