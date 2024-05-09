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

        # 利用者ごとの使用時間と料金を計算
        user_usage = filtered_df.groupby("利用者番号")["ノード時間（使用量）"].sum() / 3600
        user_usage = user_usage.sort_index(ascending=False)
        user_cost = user_usage * 22
        user_data = pd.DataFrame({"使用時間（時間）": user_usage, "使用料金（円）": user_cost})

        # タブを使用して使用時間と料金を切り替え表示
        tab1, tab2, tab3 = st.tabs(["使用時間", "使用料金", "グループ全体の使用状況"])
        with tab1:
            fig1 = px.bar(
                user_data,
                x=user_data["使用時間（時間）"],
                y=user_data.index,
                orientation="h",
                labels={"x": "使用時間（時間）", "y": "利用者番号"},
                title="利用者ごとの使用時間",
                template="plotly_white",
            )
            fig1.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                xaxis={"showgrid": True, "gridcolor": "darkgray", "gridwidth": 1},
                yaxis={"showgrid": True, "gridcolor": "darkgray", "gridwidth": 1},
            )
            fig1.update_traces(marker_color=px.colors.qualitative.Plotly[0])
            st.plotly_chart(fig1, use_container_width=True)

        with tab2:
            fig2 = px.bar(
                user_data,
                x=user_data["使用料金（円）"],
                y=user_data.index,
                orientation="h",
                labels={"x": "使用料金（円）", "y": "利用者番号"},
                title="利用者ごとの使用料金",
                template="plotly_white",
            )
            fig2.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                xaxis={"showgrid": True, "gridcolor": "darkgray", "gridwidth": 1},
                yaxis={"showgrid": True, "gridcolor": "darkgray", "gridwidth": 1},
            )
            fig2.update_traces(marker_color=px.colors.qualitative.Plotly[1])
            st.plotly_chart(fig2, use_container_width=True)

        with tab3:
            # 2020年以降のデータのみを使用
            group_df = filtered_df[
                pd.to_datetime(filtered_df["終了日時"], format="%Y%m%d%H%M%S") >= pd.to_datetime("2020-01-01")
            ]

            # グループ全体の日付に対する使用時間と使用料金を計算
            group_usage = (
                group_df.groupby(pd.to_datetime(group_df["終了日時"], format="%Y%m%d%H%M%S"))[
                    "ノード時間（使用量）"
                ].sum()
                / 3600
            )
            group_cost = group_usage * 22
            group_data = pd.DataFrame({"使用時間（時間）": group_usage, "使用料金（円）": group_cost})

            # 累積の使用時間と使用料金を計算
            group_data["累積使用時間（時間）"] = group_data["使用時間（時間）"].cumsum()
            group_data["累積使用料金（円）"] = group_data["使用料金（円）"].cumsum()

            fig3 = px.line(
                group_data,
                x=group_data.index,
                y=["累積使用時間（時間）", "累積使用料金（円）"],
                labels={"x": "日付", "value": "累積使用量"},
                title="グループ全体の累積使用時間と料金の推移",
                template="plotly_white",
            )

            fig3.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                xaxis={"showgrid": True, "gridcolor": "darkgray", "gridwidth": 1},
                yaxis={"showgrid": True, "gridcolor": "darkgray", "gridwidth": 1},
                legend={"title": ""},
            )

            fig3.update_traces(
                mode="lines",
                line={"width": 2},
                fill="tozeroy",
                fillcolor="rgba(0, 0, 255, 0.1)",
                selector={"name": "累積使用時間（時間）"},
            )

            fig3.update_traces(
                mode="lines",
                line={"width": 2},
                fill="tozeroy",
                fillcolor="rgba(255, 0, 0, 0.1)",
                selector={"name": "累積使用料金（円）"},
            )
            st.plotly_chart(fig3, use_container_width=True)

        # 利用者番号ごとの使用時間、料金、ジョブ詳細を表示
        st.subheader("利用者別の使用状況")
        user_ids = sorted(filtered_df["利用者番号"].unique())

        for user_id in user_ids:
            user_df = filtered_df[filtered_df["利用者番号"] == user_id].copy()
            user_node_time = user_df["ノード時間（使用量）"].sum()
            user_node_hours = user_node_time / 3600
            user_node_cost = user_node_hours * 22

            # 投入日時、開始日時、終了日時を時間形式に変換
            user_df.loc[:, "投入日時"] = pd.to_datetime(user_df["投入日時"], format="%Y%m%d%H%M%S", errors="coerce")
            user_df.loc[:, "開始日時"] = pd.to_datetime(user_df["開始日時"], format="%Y%m%d%H%M%S", errors="coerce")
            user_df.loc[:, "終了日時"] = pd.to_datetime(user_df["終了日時"], format="%Y%m%d%H%M%S", errors="coerce")

            with st.expander(f"利用者番号: {user_id}"):
                col1, col2 = st.columns(2)
                col1.metric("使用時間", f"{user_node_hours:.2f} 時間", delta_color="off")
                col2.metric("使用料金", f"¥{user_node_cost:.2f}", delta_color="off")

                st.write("---")
                user_df.loc[:, "料金（円）"] = user_df["ノード時間（使用量）"] / 3600 * 22
                st.dataframe(
                    user_df[
                        [
                            "キュー名",
                            "投入日時",
                            "開始日時",
                            "終了日時",
                            "経過時間",
                            "ノード時間（使用量）",
                            "料金（円）",
                        ]
                    ],
                )


if __name__ == "__main__":
    main()
