import streamlit as st
import pandas as pd
import plotly.express as px


# ==================================================
# 1. 기본 설정
# ==================================================

st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")

st.write(
    "1년간 박스오피스 10위권에 든 영화 가운데 "
    "이 기간에 개봉한 216편의 데이터를 이용해 영화 데이터를 살펴봅니다."
)


# ==================================================
# 2. 데이터 불러오기
# ==================================================

DATA_URL = (
    "https://raw.githubusercontent.com/greatsong/modudata/"
    "main/data/kobis_movies.csv"
)

try:
    df = pd.read_csv(DATA_URL)

except Exception as e:
    st.error("데이터를 불러오지 못했습니다.")
    st.exception(e)
    st.stop()


# ==================================================
# 3. 데이터 전처리
# ==================================================

# 여러 장르가 "|"로 연결되어 있다면 첫 번째 장르만 사용
df["genre"] = (
    df["genre"]
    .fillna("미상")
    .astype(str)
    .str.split("|")
    .str[0]
    .str.strip()
)


# ==================================================
# 4. 첫 번째 그래프
# ==================================================

st.divider()

st.header("1️⃣ 장르별 영화 편수")


# 장르별 영화 편수 계산
genre_count = (
    df["genre"]
    .value_counts()
    .reset_index()
)

genre_count.columns = ["장르", "영화 편수"]


# ==================================================
# 5. 도넛 그래프
# ==================================================

fig = px.pie(
    genre_count,
    names="장르",
    values="영화 편수",
    hole=0.45,
    title="장르별 영화 편수"
)

fig.update_traces(
    textposition="inside",
    textinfo="percent",
    hovertemplate=(
        "<b>%{label}</b><br>"
        "영화 편수: %{value}편<br>"
        "비율: %{percent}<extra></extra>"
    )
)

fig.update_layout(
    height=550,
    legend_title="장르"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ==================================================
# 6. 이 그래프로 알 수 있는 것
# ==================================================

st.subheader("📌 이 그래프로 알 수 있는 것")

user_answer = st.text_area(
    "그래프를 보고 알 수 있는 내용을 한 문장으로 작성하세요.",
    placeholder="예: 액션 장르의 영화가 가장 많은 비중을 차지한다.",
    height=100
)

if user_answer:
    st.write("✏️ 작성한 내용")
    st.info(user_answer)


# ==================================================
# 7. 장르별 데이터 확인
# ==================================================

with st.expander("장르별 영화 편수 데이터 보기"):
    st.dataframe(
        genre_count,
        use_container_width=True,
        hide_index=True
    )
