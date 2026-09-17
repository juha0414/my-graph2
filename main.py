import streamlit as st
import requests
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

st.title("영화 데이터 그래프 도감 2 - 분포와 관계")


# --------------------------------------------------
# 2. 데이터 불러오기
# --------------------------------------------------

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"

df = pd.read_csv(DATA_URL)


# --------------------------------------------------
# 3. 데이터 전처리
# --------------------------------------------------

# 장르가 여러 개라면 첫 번째 장르만 사용
df["genre"] = (
    df["genre"]
    .fillna("미상")
    .astype(str)
    .str.split("|")
    .str[0]
    .str.strip()
)

# 숫자형 데이터 변환
df["first_scrn"] = pd.to_numeric(
    df["first_scrn"],
    errors="coerce"
)

df["total_audi"] = pd.to_numeric(
    df["total_audi"],
    errors="coerce"
)


# --------------------------------------------------
# 4. 첫 번째 그래프 - 장르별 영화 편수 도넛
# --------------------------------------------------

st.header("1️⃣ 장르별 영화 편수")

genre_count = (
    df["genre"]
    .value_counts()
    .reset_index()
)

genre_count.columns = ["장르", "영화 편수"]

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

st.plotly_chart(
    fig1,
    use_container_width=True
)

st.subheader("📌 이 그래프로 알 수 있는 것")

answer1 = st.text_area(
    "그래프를 보고 알 수 있는 내용을 한 문장으로 작성하세요.",
    placeholder="여기에 직접 작성하세요.",
    height=100,
    key="answer1"
)

if answer1:
    st.info(answer1)


# --------------------------------------------------
# 5. 두 번째 그래프 - 장르별 영화와 총 관객 트리맵
# --------------------------------------------------

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

st.subheader("📌 이 그래프로 알 수 있는 것")

answer2 = st.text_area(
    "그래프를 보고 알 수 있는 내용을 한 문장으로 작성하세요.",
    placeholder="여기에 직접 작성하세요.",
    height=100,
    key="answer2"
)

if answer2:
    st.info(answer2)


# --------------------------------------------------
# 6. 세 번째 그래프 - 총 관객 히스토그램
# --------------------------------------------------

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


# --------------------------------------------------
# 7. 세 번째 그래프에서 알 수 있는 것
# --------------------------------------------------

st.subheader("📌 이 그래프로 알 수 있는 것")

min_audi = hist_df["total_audi"].min()
max_audi = hist_df["total_audi"].max()
bins = 20

if max_audi > min_audi:

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

    most_common_bin = bin_counts.idxmax()

    max_movie_row = hist_df.loc[
        hist_df["total_audi"].idxmax()
    ]

    max_movie_name = max_movie_row["movieNm"]
    max_movie_audi = int(max_movie_row["total_audi"])

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


answer3 = st.text_area(
    "이 그래프에 대해 추가로 알 수 있는 내용을 직접 작성하세요.",
    placeholder="여기에 추가로 분석한 내용을 작성하세요.",
    height=100,
    key="answer3"
)

if answer3:
    st.info(answer3)


# --------------------------------------------------
# 8. 네 번째 그래프 - 개봉일 스크린수와 총 관객 산점도
# --------------------------------------------------

st.divider()

st.header("4️⃣ 개봉일 스크린수와 총 관객의 관계")

scatter_df = df.dropna(
    subset=[
        "movieNm",
        "first_scrn",
        "total_audi",
        "genre"
    ]
).copy()

fig4 = px.scatter(
    scatter_df,
    x="first_scrn",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    title="개봉일 스크린수와 총 관객의 관계",
    labels={
        "first_scrn": "개봉일 스크린수",
        "total_audi": "총 관객",
        "genre": "장르"
    }
)

fig4.update_traces(
    marker=dict(
        size=10,
        opacity=0.75
    ),
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "개봉일 스크린수: %{x:,.0f}개<br>"
        "총 관객: %{y:,.0f}명"
        "<extra></extra>"
    )
)

fig4.update_layout(
    height=650,
    xaxis_title="개봉일 스크린수",
    yaxis_title="총 관객"
)

st.plotly_chart(
    fig4,
    use_container_width=True
)


# --------------------------------------------------
# 9. 네 번째 그래프에서 알 수 있는 것
# --------------------------------------------------

st.subheader("📌 이 그래프로 알 수 있는 것")

st.write(
    "이 산점도를 통해 개봉일에 확보한 스크린수가 많을수록 "
    "총 관객도 많은 경향이 있는지 확인할 수 있다. "
    "또한 장르별로 점의 색을 다르게 표시하여 "
    "장르에 따른 분포 차이도 살펴볼 수 있다."
)

answer4 = st.text_area(
    "이 그래프에 대해 추가로 알 수 있는 내용을 직접 작성하세요.",
    placeholder="예: 개봉일 스크린수가 많은 영화일수록 총 관객이 많은 경향이 보인다.",
    height=100,
    key="answer4"
)

if answer4:
    st.info(answer4)
    
