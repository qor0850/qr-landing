
import streamlit as st

# Standalone About page (direct access)
st.set_page_config(page_title="소개 | About Me", page_icon="🧑", layout="centered")

# ---- USER SETTINGS ----
PROFILE_NAME = "백XX"
TAGLINE = "자동화개발자 | RPA·AI·교육"
PROFILE_PHOTO_URL = ""  # Optional
PHONE_NUMBER = "+82-10-0000-0000"
EMAIL_ADDRESS = "you@example.com"
KAKAO_CHANNEL_URL = "https://pf.kakao.com/_yourchannel"
INSTAGRAM_URL = "https://www.instagram.com/your_instagram"

# ---- UI ----
st.markdown("# 소개 (About Me)")
if PROFILE_PHOTO_URL:
    st.image(PROFILE_PHOTO_URL, width=160)
st.write(f"**{PROFILE_NAME}**")
st.write(f"*{TAGLINE}*")

st.markdown("---")

st.markdown("### 기본 정보")
st.write("👤 **이름**: 백XX")
st.write("🎂 **나이**: 34세")
st.write("💼 **직업**: 자동화개발자")

st.markdown("### 경력")
st.write("• 삼성전자 RPA 개발·운영 (2018 ~ 2022)")
st.write("• 삼성전자 DS 현업 교육 (2023 ~ 2025.08)")

st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    st.link_button("📞 전화하기", f"tel:{PHONE_NUMBER}")
with col2:
    st.link_button("✉️ 이메일", f"mailto:{EMAIL_ADDRESS}")

if KAKAO_CHANNEL_URL:
    st.link_button("💬 카카오톡 채널", KAKAO_CHANNEL_URL, use_container_width=True)
if INSTAGRAM_URL:
    st.link_button("📷 인스타그램", INSTAGRAM_URL, use_container_width=True)

st.caption("© {name} — 소개 페이지".format(name=PROFILE_NAME))
