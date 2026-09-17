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

# 장르가 여러 개라면 첫 번째 장르만 사용
# 예: 액션|범죄|스릴러 → 액션
df["genre"] = (
    df["genre"]
    .fillna("미상")
    .astype(str)
    .str.split("|")
    .str[0]
    .str.strip()
)

# 총 관객을 숫자로 변환
df["total_audi"] = pd.to_numeric(
    df["total_audi"],
    errors="coerce"
)


# ==================================================
# 4. 첫 번째 그래프
#    장르별 영화 편수 도넛 그래프
# ==================================================

st.divider()

st.header("1️⃣ 장르별 영화 편수")

# 장르별 영화 편수 계산
genre_count = (
    df["genre"]
    .value_counts()
    .reset_index()
)

genre_count.columns = [
    "장르",
    "영화 편수"
]


# 도넛 그래프
fig1 = px.pie(
    genre_count,
    names="장르",
    values="영화 편수",
    hole=0.45,
    title="장르별 영화 편수"
)

# 마우스를 올렸을 때 표시되는 정보
fig1.update_traces(
    textposition="inside",
    textinfo="percent",
    hovertemplate=(
        "<b>%{label}</b><br>"
        "영화 편수: %{value}편<br>"
        "비율: %{percent}<extra></extra>"
    )
)

fig1.update_layout(
    height=550,
    legend_title="장르"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)


# ==================================================
# 5. 첫 번째 그래프 해석 입력
# ==================================================

st.subheader("📌 이 그래프로 알 수 있는 것")

answer1 = st.text_area(
    "그래프를 보고 알 수 있는 내용을 한 문장으로 작성하세요.",
    placeholder="여기에 직접 작성하세요.",
    height=100,
    key="answer1"
)


# ==================================================
# 6. 두 번째 그래프
#    장르 안에 영화를 넣은 트리맵
# ==================================================

st.divider()

st.header("2️⃣ 장르별 영화와 총 관객")

# 트리맵에 사용할 데이터
treemap_df = df.dropna(
    subset=["genre", "movieNm", "total_audi"]
).copy()

# 트리맵 생성
# 첫 번째 단계: 장르
# 두 번째 단계: 영화명
# 칸의 크기: 총 관객
fig2 = px.treemap(
    treemap_df,
    path=["genre", "movieNm"],
    values="total_audi",
    title="장르별 영화와 총 관객"
)

# 마우스를 올렸을 때 영화명과 총 관객 표시
fig2.update_traces(
    hovertemplate=(
        "<b>%{label}</b><br>"
        "총 관객: %{value:,.0f}명"
        "<extra></extra>"
    )
)

fig2.update_layout(
    height=700
)

st.plotly_chart(
    fig2,
    use_container_width=True
)


# ==================================================
# 7. 두 번째 그래프 해석 입력
# ==================================================

st.subheader("📌 이 그래프로 알 수 있는 것")

answer2 = st.text_area(
    "그래프를 보고 알 수 있는 내용을 한 문장으로 작성하세요.",
    placeholder="여기에 직접 작성하세요.",
    height=100,
    key="answer2"
)


# ==================================================
# 8. 장르별 영화 편수 데이터
# ==================================================

with st.expander("장르별 영화 편수 데이터 보기"):
    st.dataframe(
        genre_count,
        use_container_width=True,
        hide_index=True
    )
    
