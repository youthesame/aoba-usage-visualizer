# AOBA 利用時間可視化アプリ

東北大学のスーパーコンピュータ AOBA の利用時間を可視化するための Streamlit アプリケーションです。

https://github.com/youthesame/aoba-usage-visualizer/assets/47704718/afe017b6-5e4e-430d-9517-e7dafe7a3b09

## アプリの概要

AOBA 利用時間可視化アプリは、AOBA-A, B の利用者ポータルからダウンロードしたプロジェクトジャーナル CSV（plist.csv）をアップロードすることで、プロジェクト全体の使用時間や料金、各ユーザーの使用状況を把握することができるツールです。

## 主な機能

- プロジェクト全体の使用時間と使用料金の表示
- 利用者ごとの使用時間の横棒グラフ表示
- 利用者別の詳細な使用状況の表示（使用時間、使用料金、ジョブの詳細）

## 使用方法

1. AOBA-A, B の[利用者ポータル](https://portal.ss.cc.tohoku.ac.jp/thkportal/riyosha_login/)にログインします。
2. プロジェクトジャーナル CSV（plist.csv）をダウンロードします。
3. [アプリ](https://aoba-usage-visualizer.streamlit.app)にアクセスします。
4. CSV ファイルをアップロードします。
5. アップロード後、自動的に使用状況が表示されます。

## デモ

このアプリケーションは Streamlit Cloud 上でホストされています。以下のリンクからアクセスできます。

[https://aoba-usage-visualizer.streamlit.app](https://aoba-usage-visualizer.streamlit.app)

## ローカルでの使用方法

ローカル環境で本アプリケーションを使用したい場合は、以下の手順に従ってください。

### 動作環境

- Python 3.7 以上
- Streamlit
- Pandas
- Plotly

### インストール方法

1. このリポジトリをクローンまたはダウンロードします。

```
git clone https://github.com/youthesame/aoba-usage-visualizer.git
```

2. 必要なライブラリをインストールします。

```
pip install -r requirements.txt
```

3. アプリケーションを起動します。

```
streamlit run app.py
```

4. ブラウザが自動的に開き、アプリケーションが表示されます。

## License

This project is licensed under the MIT License.
