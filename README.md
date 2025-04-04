# Discord 投票Bot

Discordサーバーで時間枠の投票を簡単に作成するためのBotです。9:00から21:00までの2時間枠（重複あり）で、一週間分の投票を自動生成することができます。

## 機能

- 指定した日から一週間分の時間枠投票を自動作成
- 各日の9:00から21:00までの2時間枠（重複あり）を選択肢として表示
- カスタム投票の作成
- 絵文字リアクションによる簡単な投票システム

## インストール方法

1. リポジトリをクローン
   ```
   git clone https://github.com/your-username/discord-poll-bot.git
   cd discord-poll-bot
   ```

2. 必要なライブラリをインストール
   ```
   pip install discord.py pytz
   ```

3. 設定ファイルのセットアップ
   ```
   cp config.json.example config.json
   ```
   `config.json`を編集し、あなたのBotトークンを設定してください。

## Discord Bot作成手順

1. [Discord Developer Portal](https://discord.com/developers/applications)にアクセス
2. 「New Application」ボタンをクリックして新しいアプリケーションを作成
3. 左側のメニューから「Bot」をクリック
4. 「Add Bot」ボタンをクリック
5. 「Reset Token」ボタンをクリックしてトークンを取得し、`config.json`に設定
6. 「MESSAGE CONTENT INTENT」をオンにする
7. 左側のメニューから「OAuth2」→「URL Generator」をクリック
8. 「bot」スコープを選択し、以下の権限を付与:
   - Read Messages/View Channels
   - Send Messages
   - Manage Messages
   - Add Reactions
9. 生成されたURLを使用してBotをサーバーに招待

## 使用方法

Botを起動:
```
python vote-bot.py
```

### コマンド

- `!週間投票作成 [年] [月] [日]`: 指定した日から一週間分の投票を作成
  例: `!週間投票作成 2025 4 7`

- `!投票作成 [タイトル] [選択肢1] [選択肢2] ...`: カスタム投票を作成
  例: `!投票作成 "好きな食べ物は？" "ラーメン" "寿司" "カレー"`

- `!ヘルプ`: コマンド一覧と使い方を表示

## 注意事項

- トークンは絶対に公開しないでください
- Discordのレート制限により、短時間に多くの操作を行うとエラーが発生する場合があります
- サーバーにBotを招待する際は適切な権限を付与してください

## ライセンス

MIT

## 作者

Tatsuaki NEMOTO