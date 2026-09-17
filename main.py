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
# 예: 액션|범죄|스릴러 → 액션
df["genre"] = (
    df["genre"]
    .fillna("미상")
    .astype(str)
    .str.split("|")
    .str[0]
    .str.strip()
)

# 총 관객을 숫자형으로 변환
df["total_audi"] = pd.to_numeric(
    df["total_audi"],
    errors="coerce"
)


# ==================================================
# 4. 첫 번째 그래프
#    장르별 영화 편수 - 도넛 그래프
# ==================================================

st.divider()

st.header("1️⃣ 장르별 영화 편수")

genre_count = (
    df["genre"]
    .value_counts()
    .reset_index()
)

genre_count.columns = [
    "장르",
    "영화 편수"
]

fig1 = px.pie(
    genre_count,
    names="장르",
    values="영화 편수",
    hole=0.45,
    title="장르별 영화 편수"
)

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
# 5. 첫 번째 그래프 - 직접 작성
# ==================================================

st.subheader("📌 이 그래프로 알 수 있는 것")

answer1 = st.text_area(
    "그래프를 보고 알 수 있는 내용을 한 문장으로 작성하세요.",
    placeholder="여기에 직접 작성하세요.",
    height=100,
    key="answer1"
)

if answer1:
    st.info(answer1)


# ==================================================
# 6. 두 번째 그래프
#    장르별 영화와 총 관객 - 트리맵
# ==================================================

st.divider()

st.header("2️⃣ 장르별 영화와 총 관객")

treemap_df = df.dropna(
    subset=["genre", "movieNm", "total_audi"]
).copy()

fig2 = px.treemap(
    treemap_df,
    path=["genre", "movieNm"],
    values="total_audi",
    title="장르별 영화와 총 관객"
)

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
# 7. 두 번째 그래프 - 직접 작성
# ==================================================

st.subheader("📌 이 그래프로 알 수 있는 것")

answer2 = st.text_area(
    "그래프를 보고 알 수 있는 내용을 한 문장으로 작성하세요.",
    placeholder="여기에 직접 작성하세요.",
    height=100,
    key="answer2"
)

if answer2:
    st.info(answer2)


# ==================================================
# 8. 세 번째 그래프
#    총 관객 히스토그램
# ==================================================

st.divider()

st.header("3️⃣ 영화별 총 관객 분포")

hist_df = df.dropna(
    subset=["movieNm", "total_audi"]
).copy()

fig3 = px.histogram(
    hist_df,
    x="total_audi",
    nbins=20,
    title="영화별 총 관객 분포",
    labels={
        "total_audi": "총 관객 수",
        "count": "영화 편수"
    }
)

fig3.update_traces(
    hovertemplate=(
        "총 관객 구간: %{x}<br>"
        "영화 편수: %{y}편"
        "<extra></extra>"
    )
)

fig3.update_layout(
    height=550,
    xaxis_title="총 관객 수",
    yaxis_title="영화 편수"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)


# ==================================================
# 9. 세 번째 그래프 - 자동 분석 문구
# ==================================================

st.subheader("📌 이 그래프로 알 수 있는 것")

# 히스토그램의 구간 계산
min_audi = hist_df["total_audi"].min()
max_audi = hist_df["total_audi"].max()

bins = 20

if max_audi > min_audi:

    bin_width = (max_audi - min_audi) / bins

    hist_df["관객 구간"] = pd.cut(
        hist_df["total_audi"],
        bins=bins,
        include_lowest=True
    )

    bin_counts = (
        hist_df["관객 구간"]
        .value_counts()
        .sort_index()
    )

    # 영화가 가장 많이 몰린 구간
    most_common_bin = bin_counts.idxmax()
    most_common_count = bin_counts.max()

    # 가장 관객이 많은 영화
    max_movie_row = hist_df.loc[
        hist_df["total_audi"].idxmax()
    ]

    max_movie_name = max_movie_row["movieNm"]
    max_movie_audi = int(max_movie_row["total_audi"])

    # 구간의 시작값과 끝값
    bin_start = int(most_common_bin.left)
    bin_end = int(most_common_bin.right)

    st.write(
        f"대부분의 영화는 총 관객 약 "
        f"{bin_start:,}명~{bin_end:,}명 구간에 몰려 있으며, "
        f"가장 관객이 많은 영화는 **{max_movie_name}**으로 "
        f"총 관객은 **{max_movie_audi:,}명**이다."
    )

else:

    max_movie_row = hist_df.loc[
        hist_df["total_audi"].idxmax()
    ]

    max_movie_name = max_movie_row["movieNm"]
    max_movie_audi = int(max_movie_row["total_audi"])

    st.write(
        f"총 관객 수가 모두 같은 데이터이며, "
        f"가장 관객이 많은 영화는 **{max_movie_name}**으로 "
        f"총 관객은 **{max_movie_audi:,}명**이다."
    )


# ==================================================
# 10. 세 번째 그래프 - 직접 작성할 수 있는 칸
# ==================================================

st.text_area(
    "이 그래프에 대해 추가로 알 수 있는 내용을 직접 작성하세요.",
    placeholder="여기에 추가로 분석한 내용을 작성하세요.",
    height=100,
    key="answer3"
)


# ==================================================
# 11. 장르별 영화 편수 데이터
# ==================================================

with st.expander("장르별 영화 편수 데이터 보기"):

    st.dataframe(
        genre_count,
        use_container_width=True,
        hide_index=True
    )
    
