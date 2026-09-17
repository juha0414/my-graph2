import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# 1. 기본 설정
# --------------------------------------------------

st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")
st.write(
    "1년간 박스오피스 10위권에 든 영화 가운데 "
    "이 기간에 개봉한 216편의 데이터를 살펴봅니다."
)


# --------------------------------------------------
# 2. 데이터 불러오기
# --------------------------------------------------

DATA_URL = (
    "https://raw.githubusercontent.com/greatsong/modudata/"
    "main/data/kobis_movies.csv"
)

try:
    df = pd.read_csv(DATA_URL)
except Exception as e:
    st.error("데이터를 불러오는 중 오류가 발생했습니다.")
    st.exception(e)
    st.stop()


# --------------------------------------------------
# 3. 데이터 전처리
# --------------------------------------------------

# 장르가 여러 개일 경우 첫 번째 장르만 사용
df["genre"] = (
    df["genre"]
    .fillna("미상")
    .astype(str)
    .str.split("|")
    .str[0]
    .str.strip()
)

# 숫자형 데이터 변환
numeric_columns = [
    "first_scrn",
    "first_show",
    "first_week_audi",
    "total_audi",
    "days_in_top10"
]

for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")


# --------------------------------------------------
# 4. 첫 번째 그래프
#    장르별 영화 편수 - 도넛 그래프
# --------------------------------------------------

st.divider()

st.header("1️⃣ 장르별 영화 편수")

genre_count = (
    df["genre"]
    .value_counts()
    .reset_index()
)

genre_count.columns = ["장르", "영화 편수"]

fig = px.pie(
    genre_count,
    names="장르",
    values="영화 편수",
    hole=0.45,
    title="장르별 영화 편수",
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

st.info(
    "이 그래프로 알 수 있는 것: "
    "어떤 장르의 영화가 전체 216편 가운데 많이 포함되어 있는지 알 수 있습니다."
)
