import pandas as pd
import plotly.express as px
import streamlit as st

# Streamlitのカスタマイズ
st.set_page_config(page_title="スパコン利用時間可視化アプリ", layout="wide")
st.markdown(
    """
    <style>
    body {
        background-color: #1e1e1e;
        color: #e1e1e1;
    }

    .stMetricLabel {
        color: #e1e1e1;
    }

    .stMetricValue {
        color: #e1e1e1;
    }

    .css-1qrvfrg {
        color: #e1e1e1;
    }

    .github-link {
        font-size: 12px;
        color: #999999;
        position: absolute;
        top: 5px;
        left: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def main():
    st.title("AOBA 利用時間可視化アプリ")
    st.write("このアプリは、東北大学のスーパーコンピュータ AOBA の使用時間を可視化するためのツールです。")
    st.write(
        "AOBA-A, B の[利用者ポータル](https://portal.ss.cc.tohoku.ac.jp/thkportal/riyosha_login/)からダウンロードした プロジェクトジャーナルCSV（plist.csv） をアップロードすることで、プロジェクト全体の使用時間や料金、各ユーザーの使用状況を把握することができます。"
    )

    # csvファイルのアップロード
    uploaded_file = st.file_uploader("CSVファイルを選択してください", type="csv")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file, encoding="shift_jis")

        # ホストIDが'LX'かつクラスIDが'LX'のデータを取得
        filtered_df = df[(df["ホストID"] == "LX") & (df["クラスID"] == "LX")]

        # ノード時間（使用量）の合計を計算し、時間に変換
        total_node_time = filtered_df["ノード時間（使用量）"].sum()
        total_node_hours = total_node_time / 3600

        # 合計使用時間とノード時間単価をかけた金額を表示
        st.subheader("グループ全体の使用状況")
        col1, col2 = st.columns(2)
        col1.metric("合計使用時間", f"{total_node_hours:.2f} 時間", delta_color="off")
        col2.metric("合計使用料金", f"¥{total_node_hours * 22:.2f}", delta_color="off")

        # 利用者ごとの使用時間を計算
        user_usage = filtered_df.groupby("利用者番号")["ノード時間（使用量）"].sum() / 3600
        user_usage = user_usage.sort_index(ascending=False)

        # 利用者ごとの使用時間を横棒グラフで表示
        fig = px.bar(
            user_usage,
            x=user_usage.values,
            y=user_usage.index,
            orientation="h",
            labels={"x": "使用時間（時間）", "y": "利用者番号"},
            title="利用者ごとの使用時間",
            template="plotly_white",
        )
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis={"showgrid": True, "gridcolor": "lightgray", "gridwidth": 1},
            yaxis={"showgrid": True, "gridcolor": "lightgray", "gridwidth": 1},
        )
        st.plotly_chart(fig, use_container_width=True)

        # 利用者番号ごとの使用時間と金額を表示
        st.subheader("利用者別の使用状況")
        user_ids = sorted(filtered_df["利用者番号"].unique())

        for user_id in user_ids:
            user_df = filtered_df[filtered_df["利用者番号"] == user_id]
            user_node_time = user_df["ノード時間（使用量）"].sum()
            user_node_hours = user_node_time / 3600

            # 投入日時、開始日時、終了日時を時間形式に変換
            user_df["投入日時"] = pd.to_datetime(user_df["投入日時"], format="%Y%m%d%H%M%S")
            user_df["開始日時"] = pd.to_datetime(user_df["開始日時"], format="%Y%m%d%H%M%S")
            user_df["終了日時"] = pd.to_datetime(user_df["終了日時"], format="%Y%m%d%H%M%S")

            with st.expander(f"利用者番号: {user_id}"):
                col1, col2 = st.columns(2)
                col1.metric("使用時間", f"{user_node_hours:.2f} 時間", delta_color="off")
                col2.metric("使用料金", f"¥{user_node_hours * 22:.2f}", delta_color="off")

                st.write("---")
                st.dataframe(
                    user_df[["キュー名", "投入日時", "開始日時", "終了日時", "経過時間", "ノード時間（使用量）"]],
                    width=800,
                )

    st.markdown(
        '<div class="github-link"><a href="https://github.com/youthesame/aoba-usage-visualizer.git" target="_blank">GitHub</a></div>',
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
