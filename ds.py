import streamlit as st
import pandas as pd
import plotly.express as px
from io import StringIO

# -- Streamlit 페이지 기본 설정 --
st.set_page_config(
    page_title="2024년 월별 매출 대시보드",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -- 데이터 로드 --
# HTML 파일에서 추출한 CSV 데이터를 문자열로 정의합니다.
# 실제 환경에서는 st.file_uploader를 사용하는 것이 더 좋습니다.
DATA_STRING = """
월,매출액,전년동월,증감률
01월,12000000,10500000,14.3
02월,13500000,11200000,20.5
03월,11000000,12800000,-14.1
04월,18000000,15200000,18.4
05월,21000000,18500000,13.5
06월,24000000,20100000,19.4
07월,22500000,19000000,18.4
08월,23000000,20500000,12.2
09월,19500000,18000000,8.3
10월,25000000,21500000,16.3
11월,26500000,23000000,15.2
12월,28000000,25000000,12.0
"""
df = pd.read_csv(StringIO(DATA_STRING))

# -- 데이터 전처리 --
# 매출액 및 전년동월 데이터를 정수형으로 변환합니다.
df['매출액'] = df['매출액'].astype(int)
df['전년동월'] = df['전년동월'].astype(int)
# 통화 형식으로 포맷팅하는 헬퍼 함수
def format_currency(value):
    return f"₩{value:,.0f}"

# -- 대시보드 UI 구성 --
st.title("💰 2024년 월별 매출 대시보드")
st.markdown("---")

# -- 사이드바 위젯 --
# 사용자가 원하는 월을 선택할 수 있는 사이드바 셀렉트박스
st.sidebar.header("📊 데이터 필터링")
months = ['전체'] + list(df['월'].unique())
selected_month = st.sidebar.selectbox("월 선택", months, help="특정 월의 데이터만 보려면 선택하세요.")

# 선택된 월에 따라 데이터프레임을 필터링합니다.
if selected_month == '전체':
    filtered_df = df
else:
    filtered_df = df[df['월'] == selected_month]

# -- KPI 카드 섹션 --
st.header("📈 주요 지표 요약")
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_sales = filtered_df['매출액'].sum()
    st.metric(label="총 매출액", value=format_currency(total_sales))

with col2:
    average_sales = filtered_df['매출액'].mean()
    st.metric(label="월평균 매출액", value=format_currency(average_sales))

with col3:
    max_sales_row = filtered_df.loc[filtered_df['매출액'].idxmax()]
    st.metric(label="최고 매출 월", value=f"{max_sales_row['월']} ({format_currency(max_sales_row['매출액'])})")

with col4:
    min_sales_row = filtered_df.loc[filtered_df['매출액'].idxmin()]
    st.metric(label="최저 매출 월", value=f"{min_sales_row['월']} ({format_currency(min_sales_row['매출액'])})")

st.markdown("---")

# -- 그래프 섹션 --
st.header("📊 월별 매출 추이 및 증감률")

# 1. 월별 매출액 꺾은선 그래프 (Plotly Express)
fig_sales = px.line(
    filtered_df,
    x='월',
    y='매출액',
    title='월별 매출액 추이',
    markers=True,
    text='매출액',
    color_discrete_sequence=['#3498db']
)
fig_sales.update_traces(
    hovertemplate='<b>%{x}</b><br>매출액: %{y:,.0f}원'
)
fig_sales.update_layout(
    xaxis_title="월",
    yaxis_title="매출액 (원)",
    hovermode='x unified',
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)'
)
st.plotly_chart(fig_sales, use_container_width=True)

# 2. 전년 동월 대비 증감률 막대 그래프 (Plotly Express)
fig_growth = px.bar(
    filtered_df,
    x='월',
    y='증감률',
    title='전년 동월 대비 증감률',
    color='증감률',
    color_continuous_scale=['#e74c3c', '#2ecc71']
)
fig_growth.update_traces(
    hovertemplate='<b>%{x}</b><br>증감률: %{y:.1f}%'
)
fig_growth.update_layout(
    xaxis_title="월",
    yaxis_title="증감률 (%)",
    hovermode='x unified',
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)'
)
st.plotly_chart(fig_growth, use_container_width=True)

# -- 하단 정보 --
st.markdown("---")
st.markdown("데이터 출처: 내부 제공 데이터")



