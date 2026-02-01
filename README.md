# 画像16:9分割ツール - Streamlit Cloud デプロイガイド

## 📋 準備するもの
1. GitHubアカウント
2. Streamlit Cloudアカウント（GitHubアカウントで無料登録できます）

## 🚀 デプロイ手順

### ステップ1: GitHubリポジトリを作成
1. GitHub（https://github.com）にログイン
2. 新しいリポジトリを作成（例：image-splitter）
3. このフォルダの以下のファイルをアップロード：
   - `app.py`
   - `requirements.txt`

### ステップ2: Streamlit Cloudにデプロイ
1. Streamlit Cloud（https://streamlit.io/cloud）にアクセス
2. GitHubアカウントでログイン
3. 「New app」をクリック
4. リポジトリ、ブランチ、ファイルパスを選択：
   - Repository: `your-username/image-splitter`
   - Branch: `main`
   - Main file path: `app.py`
5. 「Deploy」をクリック

### ステップ3: 完成！
- デプロイ完了後、URLが表示されます
- そのURLを他の人と共有すればOK
- 誰でもブラウザで使えます

## 💡 使い方
1. 画像をアップロード
2. 自動で16:9にトリミング
3. 中央から4分割
4. 分割画像を個別またはZIPでダウンロード

## 🔧 ローカルで試す場合
```bash
# インストール
pip install streamlit pillow

# 実行
streamlit run app.py
```

ブラウザが自動で開き、ローカルホストで実行できます。

## 📝 ファイル説明
- `app.py`: メインのStreamlitアプリケーション
- `requirements.txt`: 必要なPythonパッケージ

---
問題が発生した場合はお知らせください！
