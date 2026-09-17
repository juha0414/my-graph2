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


# --------------------------------------------------
# 5. 그래프 해석 직접 입력
# --------------------------------------------------

st.subheader("📝 이 그래프로 알 수 있는 것")

genre_observation = st.text_input(
    "이 그래프를 보고 알 수 있는 점을 한 문장으로 적어 보세요.",
    placeholder="예: 액션 장르의 영화가 가장 많고, 다른 장르에 비해 비중이 높다."
)

if genre_observation:
    st.success(f"💡 {genre_observation}")
