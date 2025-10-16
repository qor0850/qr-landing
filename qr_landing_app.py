import streamlit as st
from urllib.parse import urlencode
from datetime import datetime
import pandas as pd
from openai import OpenAI
import re

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
MBTI_SHEET_URL = "https://docs.google.com/spreadsheets/d/1GJ1gQfkArBmiI4Kus8Isl8mkCIGMxNLSb9Bw6KvKSVU/export?format=csv&gid=0"

# Video URLs (YouTube recommended)
SHORTS_VIDEO_URL = "https://raw.githubusercontent.com/qor0850/streamlit-shorts/main/shots.mp4"

# -----------------------------
# 데이터 로드 (5분마다 자동 갱신)
# -----------------------------
@st.cache_data(ttl=300)  # 5분마다 초기화
def load_profile_sheet(url):
    ...

@st.cache_data(ttl=300)  # 5분마다 초기화
def load_career_sheet(url):
    ...

@st.cache_data(ttl=300)
def load_mbti_sheet(url):
    return pd.read_csv(url, encoding="utf-8-sig")

mbti_data = load_mbti_sheet(MBTI_SHEET_URL)
# -----------------------------
# 데이터 로드
# -----------------------------
@st.cache_data
def load_profile_sheet(url):
    df = pd.read_csv(url)
    keys = df.iloc[:, 0].astype(str).str.strip()
    # 공백 제거 + 소문자 변환
    keys = keys.str.lower().str.replace(" ", "")
    vals = df.iloc[:, 1].astype(str).str.strip()
    return dict(zip(keys, vals))

@st.cache_data
def load_career_sheet(url):
    return pd.read_csv(url)

def get_mbti_summary(mbti_code):
    row = mbti_data[mbti_data["MBTI"] == mbti_code.upper()]
    if row.empty:
        return None

    # ✅ 엑셀 컬럼 구조 그대로 출력
    return f"""
    ### 🌟 {row['MBTI'].values[0]} ({row['별칭'].values[0]})
    **주요 특징**: {row['주요 특징'].values[0]}  
    **강점**: {row['강점'].values[0]}  
    **약점**: {row['약점'].values[0]}  
    **잘 맞는 분야**: {row['잘 맞는 분야'].values[0]}  
    (출처: MBTI 시트)
    """
    #
    # row = mbti_data[mbti_data["MBTI"] == mbti_code.upper()]
    # if row.empty:
    #     return "해당 MBTI 데이터가 없습니다."
    #
    # return f"""
    # 🌟 {row['MBTI'].values[0]} ({row['별칭'].values[0]})
    # - 주요 특징: {row['주요 특징'].values[0]}
    # - 강점: {row['강점'].values[0]}
    # - 약점: {row['약점'].values[0]}
    # - 대인관계: {row['대인관계'].values[0]}
    # - 잘 맞는 분야: {row['잘 맞는 분야'].values[0]}
    # """


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
    # if "카카오채널" in profile_data and profile_data["카카오채널"]:
    #     st.link_button("💬 카카오톡 채널", profile_data["카카오채널"], use_container_width=True)
    # if "인스타그램" in profile_data and profile_data["인스타그램"]:
    #     st.link_button("📷 인스타그램", profile_data["인스타그램"], use_container_width=True)
    # if "예약URL" in profile_data and profile_data["예약URL"]:
    #     st.link_button("🗓 예약하기", profile_data["예약URL"], use_container_width=True)
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

/* 🎨 파스텔 톤 적용 */
.menu-1 { background: #A8D8EA; }  /* 파스텔 블루 */
.menu-2 { background: #B8E0D2; }  /* 파스텔 민트 */
.menu-3 { background: #FBC4AB; }  /* 파스텔 코랄 */
.menu-4 { background: #FFB5E8; }  /* 파스텔 핑크 */

.menu-card a { display: flex; align-items: center; justify-content: center; width: 100%; height: 100%; text-decoration: none !important; color: #333333 !important; } /* 글씨는 진한 회색으로 */
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
# MBTI 요약 함수
# -----------------------------
def get_mbti_summary(mbti_code):
    row = mbti_data[mbti_data["MBTI"] == mbti_code.upper()]
    if row.empty:
        return None

    return f"""
    🌟 {row['MBTI'].values[0]} ({row['별칭'].values[0]})
    - 주요 특징: {row['주요 특징'].values[0]}
    - 강점: {row['강점'].values[0]}
    - 약점: {row['약점'].values[0]}
    - 잘 맞는 분야: {row['잘 맞는 분야'].values[0]}
    (출처: MBTI 시트)
    """
# -----------------------------
# GPT 답변 함수
# -----------------------------
def get_openai_answer(user_input, profile, career_df):
    profile_name = profile.get('이름', '사용자')
    context = build_context(profile, career_df)

    # MBTI 관련 질문일 경우
    mbti_keywords = ["mbti", "성격", "유형"]
    if any(k in user_input.lower() for k in mbti_keywords):
        my_mbti = profile.get("mbti", "").upper()  # ✅ 프로필 시트에서 내 MBTI 가져오기

        if my_mbti and my_mbti in mbti_data["MBTI"].values:
            summary = get_mbti_summary(my_mbti)

            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": (
                            f"너는 MBTI 성격 전문가 챗봇입니다.\n"
                            f"아래 MBTI 정보를 참고해서 사용자에게 설명해줘.\n"
                            f"출처는 '(출처: MBTI 시트)' 라고 반드시 마지막에 붙여."
                        )},
                        {"role": "user", "content": f"내 MBTI({my_mbti}) 특징을 쉽게 요약해서 설명해줘:\n\n{summary}"}
                    ],
                    temperature=0.6,
                    max_tokens=300
                )
                explanation = response.choices[0].message.content.strip()

                # ✅ 내 MBTI만 출력
                st.markdown(summary)
                st.markdown("💡 추가 설명:")
                st.markdown(explanation)
                return None
            except Exception as e:
                return summary + f"\n\n(추가 설명 오류: {e})"
        else:
            return "⚠️ 프로필에 MBTI 정보가 없습니다. (출처: MBTI 시트)"

    # 일반 질문 → 기본 프로필 기반
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
    st.markdown("""
        <div style="text-align:center; padding:20px; margin-bottom:20px;">
            <h2>⚙️ 이 사이트는 다음 기술로 제작되었습니다</h2>
            <p style="font-size:16px; line-height:1.6;">
                🖥  <b>Streamlit</b> → 웹 UI/UX 제작<br>
                📊 <b>Google Sheets + Pandas</b> → 데이터 관리 및 불러오기<br>
                🤖 <b>OpenAI GPT API</b> → 챗봇 응답 생성 및 장소 추천 로직 구현<br>
                🎨 <b>HTML + CSS</b> → UI 커스터마이징<br>
                💾 <b>Session State</b> → 대화 기록, 질문 횟수 제한 관리<br>
                ☁️ <b>Streamlit Cloud + GitHub</b> → 배포 및 운영, Secrets 통한 보안 관리<br>
                🌎 <b>지도 검색 API + 자동 링크 생성</b> → 맛집·여행지 관련 지도 URL 동적 생성<br>
                🍽️ <b>GPT + 지역 선택 UI</b> → 지역 기반 맛집·여행지 추천 엔진 구축
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="menu-grid">
            <div class="menu-card menu-1">
                <a href="?{urlencode({'route': 'about'})}"><span class="menu-icon">🧑</span>소개</a>
            </div>
            <div class="menu-card menu-2">
                <a href="?{urlencode({'route': 'career'})}"><span class="menu-icon">🎬</span>경력 상세</a>
            </div>
            <div class="menu-card menu-3">
                <a href="?{urlencode({'route': 'contact'})}"><span class="menu-icon">🏆</span>질문</a>
            </div>
            <div class="menu-card menu-4">
                <a href="?{urlencode({'route': 'etc'})}"><span class="menu-icon">📍</span>기타</a>
            </div>
        </div>
    """, unsafe_allow_html=True)

def view_about():
    back_to_home()
    st.markdown('<div class="content">', unsafe_allow_html=True)
    st.markdown("## 소개 (About Me)")
    
    # ✅ 프로필 사진
    profile_img_url = "https://raw.githubusercontent.com/qor0850/qr-landing/main/baekmin.jpg"
                        
    if profile_img_url:
        st.markdown(
            f"""
            <div style="text-align:center; margin-bottom:20px;">
                <img src="{profile_img_url}" alt="프로필 사진"
                     onerror="this.onerror=null; this.src='https://via.placeholder.com/200?text=준비중';"
                     style="width:200px; height:200px;
                            object-fit:cover; box-shadow:0 4px 10px rgba(0,0,0,0.2);">
                <div style="font-size:14px; color:gray; margin-top:8px;">(사진이 표시되지 않으면 준비중입니다)</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # ✅ 기본 정보 표시
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
                <div class="info-row">🏷 한 줄 소개: {profile_data.get('한줄소개', '-')}</div>
                <div class="info-row">🛠 사용 RPA툴: {profile_data.get('사용rpa툴', '-')}</div>
                <div class="info-row">📍 사는곳: {profile_data.get('사는곳', '-')}</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    st.markdown("### 연락")
    contact_buttons()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # back_to_home()
    # st.markdown('<div class="content">', unsafe_allow_html=True)
    # st.markdown("## 소개 (About Me)")

    # birth_str = profile_data.get("생년월일", "")
    # gender_str = profile_data.get("성별", "")
    # year, mm, dd, gender, age = parse_birth_info(birth_str, gender_str)

    # if isinstance(year, int) and isinstance(mm, int) and isinstance(dd, int):
    #     birth_display = f"{year}-{mm:02d}-{dd:02d} ({gender})"
    # else:
    #     birth_display = f"{birth_str} ({gender})"

    # st.markdown(f"""
    #     <div class="info-card">
    #         <div class="info-title">기본 정보</div>
    #         <div class="info-row">👤 이름: {profile_data.get('이름', '-')}</div>
    #         <div class="info-row">🎂 생년월일: {birth_display}</div>
    #         <div class="info-row">📏 나이: {age}세</div>
    #         <div class="info-row">💼 직업: {profile_data.get('직업', '-')}</div>
    #         <div class="info-row">🏷 한 줄 소개: {profile_data.get('한줄소개', '-')}</div>
    #         <div class="info-row">🛠 사용 RPA툴: {profile_data.get('사용rpa툴', '-')}</div>
    #         <div class="info-row">📍 사는곳: {profile_data.get('사는곳', '-')}</div>
    #     </div>
    #     """, unsafe_allow_html=True)

    # st.divider()
    # st.markdown("### 연락")
    # contact_buttons()
    

# def view_shorts():
#     back_to_home()
#     st.markdown('<div class="content">', unsafe_allow_html=True)
#     st.markdown("## 쇼츠 / 리일스")

#     video_html = f"""
#     <div style="display: flex; justify-content: center; align-items: center; height: 100vh;">
#         <video controls style="height: 50vh; max-width: 90%;">
#             <source src="{SHORTS_VIDEO_URL}" type="video/mp4">
#             브라우저가 동영상을 지원하지 않습니다.
#         </video>
#     </div>
#     """
#     st.markdown(video_html, unsafe_allow_html=True)

#     st.markdown('</div>', unsafe_allow_html=True)

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



    st.divider()
    st.markdown("### 연락")
    contact_buttons()
    st.markdown('</div>', unsafe_allow_html=True)

    # ✅ 여기 안내 문구 추가
    st.caption("⏱️ 구글 시트 데이터는 5분마다 자동 갱신됩니다.")

    # FAQ 퀵버튼
    faq = [
        "간단히 자기소개 해주세요",
        "경력/프로젝트를 알려주세요",
        "MBTI가 어떻게 되나요?",
        "취미는 뭐에요?",
        "사는곳이 어디에요"
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

def view_etc():
    back_to_home()
    st.markdown("## 📎 주요 도시 맛집 / 여행지 추천")

    # ✅ 1단계: 시/도 선택
    sido_list = [
        "서울특별시", "부산광역시", "대구광역시", "인천광역시", "광주광역시",
        "대전광역시", "울산광역시", "세종특별자치시", "경기도", "강원특별자치도",
        "충청북도", "충청남도", "전라북도", "전라남도", "경상북도", "경상남도", "제주특별자치도"
    ]
    sido = st.selectbox("📍 1단계: 시/도 선택", sido_list)

    # ✅ 2단계: 주요 도시 선택
    city_options = {
        "서울특별시": ["강남구", "송파구", "마포구", "종로구"],
        "부산광역시": ["해운대구", "남구", "중구", "수영구"],
        "대구광역시": ["중구", "수성구", "달서구"],
        "인천광역시": ["남동구", "연수구", "중구"],
        "광주광역시": ["동구", "서구", "북구"],
        "대전광역시": ["유성구", "서구", "중구"],
        "울산광역시": ["남구", "동구", "중구"],
        "세종특별자치시": ["세종시"],
        "경기도": ["수원시", "성남시", "용인시", "고양시", "부천시"],
        "강원특별자치도": ["춘천시", "강릉시", "원주시"],
        "충청북도": ["청주시", "충주시"],
        "충청남도": ["천안시", "아산시", "공주시"],
        "전라북도": ["전주시", "익산시"],
        "전라남도": ["목포시", "여수시", "순천시"],
        "경상북도": ["포항시", "경주시", "구미시"],
        "경상남도": ["창원시", "김해시", "진주시"],
        "제주특별자치도": ["제주시", "서귀포시"]
    }
    city_list = city_options.get(sido, [])
    city = st.selectbox("📍 2단계: 주요 도시 선택", city_list)

    # ✅ 3단계: 동 선택 (5개만 예시)
    dong_options = {
        "강남구": ["역삼동", "논현동", "신사동", "대치동", "청담동"],
        "송파구": ["잠실동", "문정동", "방이동", "가락동", "석촌동"],
        "마포구": ["홍대입구동", "상수동", "망원동", "연남동", "공덕동"],
        "종로구": ["삼청동", "인사동", "익선동", "부암동", "평창동"],
        "해운대구": ["중동", "좌동", "우동", "송정동", "재송동"],
        "남구": ["대연동", "문현동", "용호동", "용당동", "우암동"],
        "중구": ["남포동", "광복동", "보수동", "동광동", "대청동"],
        "수영구": ["광안동", "남천동", "수영동", "망미동", "민락동"],
        "수원시": ["영통동", "매탄동", "인계동", "팔달동", "권선동"],
        "성남시": ["분당동", "야탑동", "정자동", "수내동", "이매동"],
        "전주시": ["효자동", "중화산동", "금암동", "서신동", "인후동"],
        "포항시": ["장성동", "죽도동", "두호동", "양덕동", "상도동"],
        "창원시": ["상남동", "용호동", "성산동", "반송동", "중앙동"],
        "제주시": ["연동", "이도동", "노형동", "화북동", "삼양동"],
    }
    dong_list = dong_options.get(city, [])
    dong = st.selectbox("📍 3단계: 동 선택 (대표 5곳)", dong_list)

    # ✅ 추천 종류 선택
    category = st.radio("🍽️ 추천 종류를 선택하세요", ["맛집 추천 🍲", "여행지 추천 🏝️"])

    # ✅ 추천 버튼
    if st.button("🔍 추천 보기"):
        full_location = f"{sido} {city} {dong}"
        with st.spinner("AI가 추천 중입니다..."):
            result = get_place_recommendation(full_location, category)
            st.markdown(result)

        # ✅ 관련 링크 자동 생성
        keyword = "맛집" if "맛집" in category else "여행지"
        naver_map_url = f"https://map.naver.com/p/search/{full_location}%20{keyword}"
        kakao_map_url = f"https://map.kakao.com/?q={full_location}%20{keyword}"
        google_map_url = f"https://www.google.com/maps/search/{full_location}+{keyword}"




def get_place_recommendation(location, category):
    """GPT가 맛집/여행지를 추천하고, 종류·소개·메인음식(또는 대표볼거리)·주소·관련링크를 함께 출력"""
    try:
        # ✅ GPT에게 명확한 출력 형식 요청
        if "맛집" in category:
            prompt = f"""
            {location} 지역의 현지인 추천 맛집 3곳을 아래 형식으로 소개해줘.
            반드시 아래 형식 그대로 출력해:
            1. 식당이름 | 음식 종류 | 한 줄 소개 | 대표 메뉴 | 주소
            (예: 백민식당 | 한식 | 김치찌개가 맛있는 현지식당 | 김치찌개 | 서울 송파구 문정동 123-4)
            """
        else:
            prompt = f"""
            {location} 지역에서 하루 여행 코스로 좋은 여행지 3곳을 아래 형식으로 소개해줘.
            반드시 아래 형식 그대로 출력해:
            1. 장소이름 | 특징 | 한 줄 설명 | 대표 볼거리 | 주소
            (예: 오죽헌 | 역사유적지 | 퇴계 이황의 생가로 유명한 유적지 | 유물전시관 | 강원 강릉시 율곡로 3139)
            """

        # ✅ GPT 호출
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "너는 한국 맛집 및 여행지 추천 전문가야. 반드시 지정된 형식을 지켜."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=800
        )

        raw_text = response.choices[0].message.content.strip()
        lines = [l.strip() for l in raw_text.split("\n") if l.strip()]

        # ✅ 추천 결과 제목
        result_md = "### 🍽️ 추천 결과\n\n"

        for line in lines:
            # 1️⃣ 숫자 및 기호 제거
            clean_line = re.sub(r"^\d+\.\s*", "", line)
            # 2️⃣ 구분자 보정 (– 또는 - → |)
            clean_line = clean_line.replace("–", "|").replace("-", "|")
            # 3️⃣ 파이프 기준 분리
            parts = [p.strip() for p in clean_line.split("|") if p.strip()]

            # 4️⃣ 필드 보완 (5개 미만일 경우 '정보 없음' 채움)
            while len(parts) < 5:
                parts.append("정보 없음")

            name, kind, desc, main, addr = parts[:5]

            # 5️⃣ 지도 링크 자동 생성
            from urllib.parse import quote_plus
            qname = quote_plus(name)
            naver_url  = f"https://map.naver.com/p/search/{qname}"
            kakao_url  = f"https://map.kakao.com/?q={qname}"
            google_url = f"https://www.google.com/maps/search/{qname}"

            # 6️⃣ 출력 구성
            result_md += f"🍴 **{name}**  \n"
            result_md += f"📍 종류: {kind}  \n"
            result_md += f"💬 소개: {desc}  \n"
            result_md += f"🍛 메인 음식: {main}  \n" if "맛집" in category else f"🎯 대표 볼거리: {main}  \n"
            result_md += f"🏠 주소: {addr}  \n"
            result_md += f"🔗 [네이버 지도]({naver_url}) | 🗺️ [카카오맵]({kakao_url}) | 🌍 [Google Maps]({google_url})\n\n"

        # 7️⃣ 결과 반환
        return result_md if lines else "⚠️ 추천 정보를 불러오지 못했습니다. 다시 시도해주세요."

    except Exception as e:
        return f"⚠️ 추천을 불러오는 중 오류 발생: {e}"

# -----------------------------
# App Router
# -----------------------------
route = get_route()

if route == "home":
    view_home()
elif route == "about":
    view_about()
elif route == "career":
    view_career()
elif route == "contact":
    view_contact()
elif route == "etc":
    view_etc()
else:
    set_route("home")
    view_home()

# Footer
st.caption(f"© {profile_data.get('이름','')} — 자기소개")
