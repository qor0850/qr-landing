import streamlit as st
from urllib.parse import urlencode
from datetime import datetime

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

# Video URLs (YouTube recommended)
SHORTS_VIDEO_URL = "https://raw.githubusercontent.com/qor0850/streamlit-shorts/main/shots.mp4"
CAREER_VIDEO_URL = "https://www.youtube.com/watch?v=oHg5SJYRHA0"

# Contact & Location
PHONE_NUMBER = "+82-10-0000-0000"
EMAIL_ADDRESS = "you@example.com"
KAKAO_CHANNEL_URL = "https://pf.kakao.com/_yourchannel"
INSTAGRAM_URL = "https://www.instagram.com/your_instagram"
NAVER_MAPS_URL = "https://naver.me/FTML1DNz"
RESERVATION_URL = ""

# Colors
COLOR_1 = "#2F80ED"
COLOR_2 = "#27AE60"
COLOR_3 = "#F2994A"
COLOR_4 = "#EB5757"
TEXT_COLOR = "#FFFFFF"

# 생년월일 + 성별 (자동)
BIRTH_INPUT = "920601-1"  # YYMMDD-X 형식

# ===========================================
# -----------------------------
# Helpers
# -----------------------------
def set_route(route: str):
    st.query_params["route"] = route

def get_route() -> str:
    params = st.query_params
    if "route" in params and params["route"]:
        return params["route"]
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

def parse_birth_info(birth_str: str):
    yy = int(birth_str[0:2])
    mm = int(birth_str[2:4])
    dd = int(birth_str[4:6])
    gender_code = int(birth_str.split("-")[1][0])

    # 1900/2000 세기 구분
    if gender_code in [1, 2]:
        year = 1900 + yy
    else:
        year = 2000 + yy

    birth_date = datetime(year, mm, dd)
    today = datetime.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    gender = "남" if gender_code % 2 == 1 else "여"
    return year, mm, dd, gender, age

# -----------------------------
# CSS
# -----------------------------
GLOBAL_CSS = f"""
<style>
.appview-container .main .block-container {{
    padding-top: 0rem;
    padding-bottom: 0rem;
}}
.menu-grid {{
    height: 100vh;
    width: 100%; /* Changed from 100vw to 100% to prevent overflow */
    margin: 0;
    padding: 0;
    display: flex;
    flex-direction: column;
    justify-content: center;   /* 세로 가운데 */
    align-items: center;       /* 가로 가운데 */
}}
.menu-card {{
    height: 25vh;
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    font-weight: 800;
    font-size: clamp(20px, 5vw, 28px);
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
.menu-card a {{
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;
    text-decoration: none !important;
    color: {TEXT_COLOR} !important;
}}
.menu-icon {{
    margin-right: 12px;
    font-size: 1.2em;
}}
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
                <a href="?{urlencode({"route": "career"})}"><span class="menu-icon">🏆</span>상세 영상</a>
            </div>
            <div class="menu-card menu-4">
                <a href="?{urlencode({"route": "contact"})}"><span class="menu-icon">📍</span>질문</a>
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

    # 생년월일 + 성별 계산
    year, mm, dd, gender, age = parse_birth_info(BIRTH_INPUT)

    # 기본 정보 카드
    st.markdown(
        f"""
        <div class="info-card">
            <div class="info-title">기본 정보</div>
            <div class="info-row">👤 <b>이름</b>: {PROFILE_NAME}</div>
            <div class="info-row">🎂 <b>생년월일</b>: {year}-{mm:02d}-{dd:02d} ({gender})</div>
            <div class="info-row">📏 <b>나이</b>: {age}세</div>
            <div class="info-row">💼 <b>직업</b>: 자동화개발자</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # 경력 카드
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

    # 세로 9:16 비율로 맞춘 영상 (가운데 정렬)
    st.markdown(
        f"""
            <div style="display: flex; justify-content: center; margin-top: 16px;">
                <video style="width: 360px; aspect-ratio: 9 / 16; border-radius: 12px;" 
                       controls autoplay loop muted>
                    <source src="{SHORTS_VIDEO_URL}" type="video/mp4">
                    Your browser does not support the video tag.
                </video>
            </div>
            """,
        unsafe_allow_html=True
    )

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
