# Streamlit 데이터 대시보드 웹앱
# 주요 기능: 데이터 업로드, 전처리, 시각화
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="데이터 대시보드", layout="wide")
st.title("데이터 분석 대시보드")

# 1. 데이터 업로드
data_file = st.file_uploader("CSV 데이터셋 업로드", type=["csv"])
if data_file is not None:
    df = pd.read_csv(data_file)
    st.subheader("원본 데이터 미리보기")
    st.dataframe(df.head())

    # 2. 전처리 옵션
    st.sidebar.header("전처리 옵션")
    if st.sidebar.checkbox("결측치(NaN) 제거"):
        df = df.dropna()
        st.write("결측치가 제거된 데이터:")
        st.dataframe(df.head())

    # 3. 기본 통계
    if st.checkbox("기본 통계 보기"):
        st.subheader("기본 통계")
        st.write(df.describe())

    # 4. 시각화
    st.sidebar.header("시각화 옵션")
    plot_type = st.sidebar.selectbox("시각화 종류", ["히스토그램", "상관관계 히트맵", "산점도"])
    if plot_type == "히스토그램":
        col = st.sidebar.selectbox("컬럼 선택", df.select_dtypes(include='number').columns)
        fig, ax = plt.subplots()
        sns.histplot(df[col], kde=True, ax=ax)
        st.pyplot(fig)
    elif plot_type == "상관관계 히트맵":
        fig, ax = plt.subplots(figsize=(8,6))
        sns.heatmap(df.corr(), annot=True, cmap='coolwarm', ax=ax)
        st.pyplot(fig)
    elif plot_type == "산점도":
        num_cols = df.select_dtypes(include='number').columns
        x_col = st.sidebar.selectbox("X축", num_cols)
        y_col = st.sidebar.selectbox("Y축", num_cols, index=1 if len(num_cols)>1 else 0)
        fig, ax = plt.subplots()
        sns.scatterplot(x=df[x_col], y=df[y_col], ax=ax)
        st.pyplot(fig)
else:
    st.info("좌측에서 CSV 파일을 업로드하세요.")
