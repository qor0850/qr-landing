import streamlit as st
from urllib.parse import urlencode
from datetime import datetime
import pandas as pd
from openai import OpenAI

# -----------------------------
# OpenAI 설정
# -----------------------------
client = OpenAI(api_key=st.secrets["api_key"])
# -----------------------------
# Config
# -----------------------------
st.set_page_config(
    page_title="QR Landing",
    page_icon="📇",
    layout="wide",
)

# -----------------------------
# Google Sheets URL
# -----------------------------
PROFILE_SHEET_URL = "https://docs.google.com/spreadsheets/d/1eOApzLbogOSx68xf7d3Wj0xs-7acj9HKLDM5GXMR4P0/export?format=csv&gid=0"
CAREER_SHEET_URL = "https://docs.google.com/spreadsheets/d/18ohr0sXHqPYu0Bzk8UCQUsKGNCIUHoAEQm0FA7IrdKA/export?format=csv&gid=0"

# Video URLs (YouTube recommended)
SHORTS_VIDEO_URL = "https://raw.githubusercontent.com/qor0850/streamlit-shorts/main/shots.mp4"

# -----------------------------
# 데이터 로드
# -----------------------------
@st.cache_data
def load_profile_sheet(url):
    df = pd.read_csv(url)
    keys = df.iloc[:, 0].astype(str).str.strip()
    vals = df.iloc[:, 1].astype(str).str.strip()
    return dict(zip(keys, vals))

@st.cache_data
def load_career_sheet(url):
    return pd.read_csv(url)

profile_data = load_profile_sheet(PROFILE_SHEET_URL)
career_data = load_career_sheet(CAREER_SHEET_URL)

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
    st.markdown(f"[⬅️ 홈으로](?{urlencode({'route': 'home'})})")

def parse_birth_info(birth_str: str, gender_str: str = ""):
    try:
        yy = int(birth_str[0:2])
        mm = int(birth_str[2:4])
        dd = int(birth_str[4:6])

        current_year = datetime.today().year
        year = 2000 + yy if (2000 + yy) <= current_year else 1900 + yy

        birth_date = datetime(year, mm, dd)
        today = datetime.today()
        age = today.year - birth_date.year - (
                (today.month, today.day) < (birth_date.month, birth_date.day)
        )

        gender = gender_str if gender_str else "-"
        return year, mm, dd, gender, age
    except Exception:
        return "-", "-", "-", "-", "-"

def contact_buttons():
    cols = st.columns(2)
    with cols[0]:
        st.link_button("📞 전화하기", f"tel:{profile_data.get('연락처','')}")
    with cols[1]:
        st.link_button("✉️ 이메일", f"mailto:{profile_data.get('이메일','')}")
    if "카카오채널" in profile_data and profile_data["카카오채널"]:
        st.link_button("💬 카카오톡 채널", profile_data["카카오채널"], use_container_width=True)
    if "인스타그램" in profile_data and profile_data["인스타그램"]:
        st.link_button("📷 인스타그램", profile_data["인스타그램"], use_container_width=True)
    if "예약URL" in profile_data and profile_data["예약URL"]:
        st.link_button("🗓 예약하기", profile_data["예약URL"], use_container_width=True)
    if "지도URL" in profile_data and profile_data["지도URL"]:
        st.link_button("📍 위치(네이버지도)", profile_data["지도URL"], use_container_width=True)

# -----------------------------
# CSS
# -----------------------------
GLOBAL_CSS = """
<style>
.appview-container .main .block-container { padding-top: 0rem; padding-bottom: 0rem; }
.menu-grid { height: 100vh; width: 100%; display: flex; flex-direction: column; justify-content: center; align-items: center; }
.menu-card { height: 25vh; width: 100%; display: flex; align-items: center; justify-content: center; text-align: center; font-weight: 800; font-size: clamp(20px, 5vw, 28px); letter-spacing: 0.4px; color: #FFFFFF; user-select: none; text-decoration: none !important; }
.menu-card:active { filter: brightness(0.95); transform: scale(0.996); }
.menu-1 { background: #2F80ED; }
.menu-2 { background: #27AE60; }
.menu-3 { background: #F2994A; }
.menu-4 { background: #EB5757; }
.menu-card a { display: flex; align-items: center; justify-content: center; width: 100%; height: 100%; text-decoration: none !important; color: #FFFFFF !important; }
.menu-icon { margin-right: 12px; font-size: 1.2em; }
.content { padding: 16px 8px 32px; }
.info-card { border-radius: 16px; padding: 16px; background: #ffffff; box-shadow: 0 8px 20px rgba(0,0,0,0.06); border: 1px solid rgba(0,0,0,0.05); }
.info-title { font-weight: 700; margin-bottom: 8px; }
.info-row { margin: 6px 0; line-height: 1.6; font-size: 16px; }
.badge { display:inline-block; background:#f2f4f7; padding:2px 8px; border-radius:999px; font-size:12px; margin-left:6px; vertical-align: middle; }
</style>
"""
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

# -----------------------------
# Career 요약 & Context 생성
# -----------------------------
def summarize_career(df, max_len=300):
    summary_lines = []
    for _, row in df.iterrows():
        detail = str(row["상세 내용"]).replace("\\n", "\n")
        if len(detail) > max_len:
            detail = detail[:max_len] + "..."
        summary_lines.append(
            f"- {row['기간']} | {row['회사/기관']} | {row['직무']} | {detail}"
        )
    return "\n".join(summary_lines)

def build_context(profile, career_df):
    lines = []
    lines.append("### [프로필]")
    for k, v in profile.items():
        lines.append(f"{k}: {v}")

    lines.append("\n### [경력 요약]")
    lines.append(summarize_career(career_df, max_len=300))

    return "\n".join(lines)

# -----------------------------
# GPT 답변 함수
# -----------------------------
def get_openai_answer(user_input, profile, career_df):
    profile_name = profile.get('이름', '사용자')
    context = build_context(profile, career_df)

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        f"너는 {profile_name}님의 자기소개 챗봇입니다.\n"
                        f"아래 프로필(자기소개 시트)과 경력 요약(경력기술서 시트)을 참고해서만 답변하세요.\n"
                        f"답변은 핵심만, 3~4문장 이내로 간결하게 작성하세요.\n"
                        f"출처는 '(출처: 자기소개/경력기술서)' 라고 반드시 답변 마지막에 붙이세요.\n\n{context}"
                    )
                },
                {"role": "user", "content": user_input}
            ],
            temperature=0.5,
            max_tokens=250
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"오류 발생: {e}"

# -----------------------------
# Views
# -----------------------------
def view_home():
    st.markdown(f"""
        <div class="menu-grid">
            <div class="menu-card menu-1">
                <a href="?{urlencode({'route': 'about'})}"><span class="menu-icon">🧑</span>소개</a>
            </div>
            <div class="menu-card menu-2">
                <a href="?{urlencode({'route': 'shorts'})}"><span class="menu-icon">🎬</span>쇼츠 영상</a>
            </div>
            <div class="menu-card menu-3">
                <a href="?{urlencode({'route': 'career'})}"><span class="menu-icon">🏆</span>경력 상세</a>
            </div>
            <div class="menu-card menu-4">
                <a href="?{urlencode({'route': 'contact'})}"><span class="menu-icon">📍</span>질문</a>
            </div>
        </div>
    """, unsafe_allow_html=True)

def view_about():
    back_to_home()
    st.markdown('<div class="content">', unsafe_allow_html=True)
    st.markdown("## 소개 (About Me)")

    birth_str = profile_data.get("생년월일", "")
    gender_str = profile_data.get("성별", "")
    year, mm, dd, gender, age = parse_birth_info(birth_str, gender_str)

    if isinstance(year, int) and isinstance(mm, int) and isinstance(dd, int):
        birth_display = f"{year}-{mm:02d}-{dd:02d} ({gender})"
    else:
        birth_display = f"{birth_str} ({gender})"

    st.markdown(f"""
        <div class="info-card">
            <div class="info-title">기본 정보</div>
            <div class="info-row">👤 이름: {profile_data.get('이름', '-')}</div>
            <div class="info-row">🎂 생년월일: {birth_display}</div>
            <div class="info-row">📏 나이: {age}세</div>
            <div class="info-row">💼 직업: {profile_data.get('직업', '-')}</div>
            <div class="info-row">🏷 한줄 소개: {profile_data.get('한줄 소개 /태그라인', '-')}</div>
            <div class="info-row">📍 사는곳: {profile_data.get('사는곳', '-')}</div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.markdown("### 연락")
    contact_buttons()
    st.markdown('</div>', unsafe_allow_html=True)

def view_shorts():
    back_to_home()
    st.markdown('<div class="content">', unsafe_allow_html=True)
    st.markdown("## 쇼츠 / 리일스")
    st.video(SHORTS_VIDEO_URL)  # ✅ 변수 그대로 사용
    st.markdown('</div>', unsafe_allow_html=True)

def view_career():
    back_to_home()
    st.markdown("## 경력 상세")

    for _, row in career_data.iterrows():
        detail = str(row["상세 내용"]).replace("\\n", "\n")
        st.markdown(f"""
        - 📅 **{row['기간']}**  
          🏢 {row['회사/기관']}  
          💼 {row['직무']}  
          📝 {detail}
        """)
        st.divider()

def view_contact():
    back_to_home()
    st.markdown('<div class="content">', unsafe_allow_html=True)
    st.markdown("## 챗봇 & 연락 / 위치")

    # FAQ 퀵버튼
    faq = [
        "간단히 자기소개 해주세요",
        "경력/프로젝트를 알려주세요",
        "나이가 어떻게 되나요",
        "사는곳이 어디에요",
    ]
    st.caption("빠른 질문:")
    faq_cols = st.columns(len(faq))
    for i, q in enumerate(faq):
        if faq_cols[i].button(q, key=f"faq_btn_{i}"):
            st.session_state["contact_draft"] = q
            st.rerun()

    if "contact_chat_history" not in st.session_state:
        st.session_state.contact_chat_history = []
    if "contact_question_count" not in st.session_state:
        st.session_state.contact_question_count = 0
    if "contact_draft" not in st.session_state:
        st.session_state.contact_draft = ""

    MAX_Q = 3

    if st.session_state.contact_question_count >= MAX_Q:
        st.warning(f"질문은 최대 {MAX_Q}회까지 가능합니다.")
    else:
        with st.form(key="contact_chat_form"):
            user_input = st.text_input(
                "질문을 입력하세요:",
                value=st.session_state.contact_draft
            )
            col1, col2 = st.columns([1, 1])
            with col1:
                submit_button = st.form_submit_button("전송")
            with col2:
                reset_button = st.form_submit_button("초기화")

        if submit_button and user_input.strip():
            answer = get_openai_answer(user_input.strip(), profile_data, career_data)
            st.session_state.contact_chat_history.append(
                {"user": user_input.strip(), "bot": answer}
            )
            st.session_state.contact_question_count += 1
            st.session_state.contact_draft = ""

        if reset_button:
            st.session_state.contact_chat_history = []
            st.session_state.contact_question_count = 0
            st.session_state.contact_draft = ""
            st.rerun()

    if st.session_state.contact_chat_history:
        st.divider()
        for chat in reversed(st.session_state.contact_chat_history):
            st.markdown(f"**나:** {chat['user']}")
            st.markdown(f"**챗봇:** {chat['bot']}")
            st.markdown("---")

    st.divider()
    st.markdown("### 연락")
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

# Footer
st.caption(f"© {profile_data.get('이름','')} — 자기소개")
