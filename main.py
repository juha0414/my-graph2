import streamlit as st
import pandas as pd
import plotly.express as px


# --------------------------------------------------
# 1. 기본 설정
# --------------------------------------------------

st.set_page_config(
    page_title="영화 데이터 그래프 도감 2",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 영화 데이터 그래프 도감 2")
st.write("분포와 관계를 그래프로 살펴봅니다.")


# --------------------------------------------------
# 2. 데이터 불러오기
# --------------------------------------------------

url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"

df = pd.read_csv(url)


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
numeric_columns = [
    "first_scrn",
    "first_show",
    "first_week_audi",
    "total_audi",
    "days_in_top10"
]

for col in numeric_columns:
    df[col] = pd.to_numeric(
        df[col],
        errors="coerce"
    )


# --------------------------------------------------
# 4. 장르별 영화 편수 - 도넛 그래프
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
# 5. 장르별 영화와 총 관객 - 트리맵
# --------------------------------------------------

st.divider()
st.header("2️⃣ 장르별 영화와 총 관객")

treemap_df = df.dropna(
    subset=[
        "genre",
        "movieNm",
        "total_audi"
    ]
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
# 6. 영화별 총 관객 분포 - 히스토그램
# --------------------------------------------------

st.divider()
st.header("3️⃣ 영화별 총 관객 분포")

hist_df = df.dropna(
    subset=[
        "movieNm",
        "total_audi"
    ]
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
    max_movie_audi = int(
        max_movie_row["total_audi"]
    )

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
    max_movie_audi = int(
        max_movie_row["total_audi"]
    )

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
# 7. 개봉일 스크린수와 총 관객의 관계 - 산점도
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


# --------------------------------------------------
# 8. 장르별 총 관객 분포 - 박스플롯
# --------------------------------------------------

st.divider()
st.header("5️⃣ 장르별 총 관객 분포")

genre_counts = df["genre"].value_counts()

valid_genres = genre_counts[
    genre_counts >= 10
].index

box_df = df[
    df["genre"].isin(valid_genres)
].dropna(
    subset=[
        "genre",
        "total_audi",
        "movieNm"
    ]
).copy()

fig5 = px.box(
    box_df,
    x="genre",
    y="total_audi",
    color="genre",
    points="outliers",
    hover_name="movieNm",
    title="영화가 10편 이상인 장르의 총 관객 분포",
    labels={
        "genre": "장르",
        "total_audi": "총 관객"
    }
)

fig5.update_traces(
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "총 관객: %{y:,.0f}명"
        "<extra></extra>"
    )
)

fig5.update_layout(
    height=650,
    showlegend=False,
    xaxis_title="장르",
    yaxis_title="총 관객"
)

st.plotly_chart(
    fig5,
    use_container_width=True
)

st.subheader("📌 이 그래프로 알 수 있는 것")

st.write(
    "영화가 10편 이상인 장르만 골라 장르별 총 관객의 "
    "중앙값과 분포 범위를 비교할 수 있다. "
    "상자 밖에 표시되는 점은 해당 장르의 일반적인 분포에서 "
    "상대적으로 벗어난 영화이다."
)

answer5 = st.text_area(
    "이 그래프에 대해 추가로 알 수 있는 내용을 직접 작성하세요.",
    placeholder="여기에 추가로 분석한 내용을 작성하세요.",
    height=100,
    key="answer5"
)

if answer5:
    st.info(answer5)


# --------------------------------------------------
# 9. 개봉일 스크린수·총 관객·첫 주 관객 - 버블 그래프
# --------------------------------------------------

st.divider()
st.header("6️⃣ 개봉일 스크린수와 총 관객의 관계 - 버블 그래프")

bubble_df = df.dropna(
    subset=[
        "movieNm",
        "first_scrn",
        "first_week_audi",
        "total_audi",
        "genre"
    ]
).copy()

bubble_df = bubble_df[
    bubble_df["first_week_audi"] > 0
].copy()

fig6 = px.scatter(
    bubble_df,
    x="first_scrn",
    y="total_audi",
    size="first_week_audi",
    color="genre",
    hover_name="movieNm",
    size_max=60,
    title="개봉일 스크린수·총 관객·첫 주 관객의 관계",
    labels={
        "first_scrn": "개봉일 스크린수",
        "total_audi": "총 관객",
        "first_week_audi": "개봉 첫 주 관객",
        "genre": "장르"
    }
)

fig6.update_traces(
    marker=dict(
        opacity=0.65
    ),
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "개봉일 스크린수: %{x:,.0f}개<br>"
        "총 관객: %{y:,.0f}명<br>"
        "개봉 첫 주 관객: %{marker.size:,.0f}명"
        "<extra></extra>"
    )
)

fig6.update_layout(
    height=700,
    xaxis_title="개봉일 스크린수",
    yaxis_title="총 관객"
)

st.plotly_chart(
    fig6,
    use_container_width=True
)

st.subheader("📌 이 그래프로 알 수 있는 것")

st.write(
    "이 버블 그래프는 4번 산점도에 개봉 첫 주 관객 수라는 "
    "정보를 추가한 것이다. "
    "가로축은 개봉일 스크린수, 세로축은 총 관객을 나타내며, "
    "버블의 크기가 클수록 개봉 첫 주 관객이 많다는 뜻이다. "
    "따라서 개봉 초반에 많은 관객을 확보한 영화가 "
    "총 관객에서 어떤 위치에 나타나는지 함께 확인할 수 있다."
)

answer6 = st.text_area(
    "이 그래프에 대해 추가로 알 수 있는 내용을 직접 작성하세요.",
    placeholder="예: 개봉 첫 주 관객이 많은 영화일수록 총 관객도 많은 경향이 나타난다.",
    height=100,
    key="answer6"
)

if answer6:
    st.info(answer6)


# --------------------------------------------------
# 10. 제작 국가와 장르별 영화 편수 - 선버스트
# --------------------------------------------------

st.divider()
st.header("7️⃣ 제작 국가와 장르별 영화 편수")

sunburst_df = df.dropna(
    subset=[
        "nation",
        "genre"
    ]
).copy()

sunburst_df["nation"] = (
    sunburst_df["nation"]
    .astype(str)
    .str.strip()
    .replace("", "미상")
)

sunburst_df["genre"] = (
    sunburst_df["genre"]
    .astype(str)
    .str.strip()
    .replace("", "미상")
)

sunburst_count = (
    sunburst_df
    .groupby(
        ["nation", "genre"]
    )
    .size()
    .reset_index(
        name="영화 편수"
    )
)

fig7 = px.sunburst(
    sunburst_count,
    path=["nation", "genre"],
    values="영화 편수",
    title="제작 국가 → 장르별 영화 편수"
)

fig7.update_traces(
    hovertemplate=(
        "<b>%{label}</b><br>"
        "영화 편수: %{value}편"
        "<extra></extra>"
    )
)

fig7.update_layout(
    height=750
)

st.plotly_chart(
    fig7,
    use_container_width=True
)

st.subheader("📌 이 그래프로 알 수 있는 것")

st.write(
    "선버스트 그래프의 안쪽은 제작 국가이고, "
    "바깥쪽은 해당 국가의 장르를 나타낸다. "
    "각 칸의 크기는 해당 국가와 장르에 속하는 영화 편수에 비례하므로, "
    "어떤 국가에서 어떤 장르의 영화가 많이 만들어졌는지 "
    "한눈에 확인할 수 있다."
)

answer7 = st.text_area(
    "이 그래프에 대해 추가로 알 수 있는 내용을 직접 작성하세요.",
    placeholder="예: 특정 제작 국가에서는 특정 장르의 영화가 많이 나타난다.",
    height=100,
    key="answer7"
)

if answer7:
    st.info(answer7)


# --------------------------------------------------
# 11. 개봉 첫 주 관객이 전체 관객에서 차지하는 비율
# --------------------------------------------------

st.divider()
st.header("8️⃣ 개봉 첫 주 관객이 전체 관객에서 차지하는 비율은 영화마다 얼마나 다른가")

question8 = "개봉 첫 주 관객이 전체 관객에서 차지하는 비율은 영화마다 얼마나 다른가"

ratio_df = df.dropna(
    subset=[
        "movieNm",
        "first_week_audi",
        "total_audi"
    ]
).copy()

# total_audi가 0인 영화 제외
ratio_df = ratio_df[
    ratio_df["total_audi"] > 0
].copy()

# 첫 주 관객 비율 계산
ratio_df["첫 주 관객 비율"] = (
    ratio_df["first_week_audi"]
    / ratio_df["total_audi"]
    * 100
)

# 비율이 높은 영화부터 정렬
ratio_df = ratio_df.sort_values(
    "첫 주 관객 비율",
    ascending=False
)

fig8 = px.bar(
    ratio_df,
    x="movieNm",
    y="첫 주 관객 비율",
    title=question8,
    labels={
        "movieNm": "영화명",
        "첫 주 관객 비율": "첫 주 관객 비율 (%)"
    }
)

fig8.update_traces(
    customdata=ratio_df[
        ["movieNm", "첫 주 관객 비율"]
    ],
    hovertemplate=(
        "<b>%{customdata[0]}</b><br>"
        "첫 주 관객 비율: %{customdata[1]:.2f}%"
        "<extra></extra>"
    )
)

fig8.update_layout(
    height=700,
    xaxis_title="영화명",
    yaxis_title="첫 주 관객 비율 (%)",
    xaxis_tickangle=-60
)

st.plotly_chart(
    fig8,
    use_container_width=True
)

st.subheader("📌 이 그래프로 알 수 있는 것")

st.write(
    "이 그래프는 각 영화의 개봉 첫 주 관객이 "
    "전체 관객에서 차지하는 비율을 보여준다. "
    "비율이 높을수록 전체 관객 중 많은 비중이 개봉 첫 주에 집중되었음을 의미하고, "
    "비율이 낮을수록 개봉 이후에도 관객이 지속적으로 유입되었음을 알 수 있다."
)

answer8 = st.text_area(
    "이 그래프에 대해 추가로 알 수 있는 내용을 직접 작성하세요.",
    placeholder="여기에 추가로 분석한 내용을 작성하세요.",
    height=100,
    key="answer8"
)

if answer8:
    st.info(answer8)
