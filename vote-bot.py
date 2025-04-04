import discord
from discord.ext import commands
import datetime
import pytz
import asyncio

# Botの設定
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# タイムゾーンの設定（日本時間）
JST = pytz.timezone('Asia/Tokyo')

# 投票用絵文字（追加の絵文字を含む）
EMOJI_NUMBERS = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟', '🇦', '🇧', '🇨', '🇩', '🇪']

@bot.event
async def on_ready():
    print(f'{bot.user} としてログインしました')

@bot.command(name='週間投票作成')
async def create_weekly_poll(ctx, 年: int, 月: int, 日: int):
    # コマンド実行開始を通知
    await ctx.send("投票を作成しています。しばらくお待ちください...")

@bot.command(name='期間投票作成')
async def create_period_poll(ctx, 開始年: int, 開始月: int, 開始日: int, 終了年: int, 終了月: int, 終了日: int):
    """
    指定した期間の9:00-21:00の2時間枠（重複あり）の投票を作成します
    使用例: !期間投票作成 2025 4 7 2025 4 15
    """
    # コマンド実行開始を通知
    await ctx.send("投票を作成しています。しばらくお待ちください...")
    
    # 開始日と終了日の設定
    try:
        start_date = datetime.datetime(開始年, 開始月, 開始日, tzinfo=JST)
        end_date = datetime.datetime(終了年, 終了月, 終了日, tzinfo=JST)
    except ValueError as e:
        await ctx.send(f"日付の指定が正しくありません: {str(e)}")
        return
    
    # 日数を計算
    delta = end_date - start_date
    days = delta.days + 1  # 終了日も含める
    
    if days <= 0:
        await ctx.send("終了日は開始日以降に設定してください。")
        return
    
    if days > 31:
        await ctx.send("期間が長すぎます。最大31日間までにしてください。")
        return
    
    # 投票メッセージを送信
    try:
        intro_msg = await ctx.send(f"**{開始年}年{開始月}月{開始日}日から{終了年}年{終了月}月{終了日}日までの予定投票**\n各日の参加可能な時間帯に投票してください（複数選択可）")
        await asyncio.sleep(1)  # 少し待機
    except Exception as e:
        await ctx.send(f"メッセージ送信中にエラーが発生しました: {str(e)}")
        return  # エラーがあれば中断
    
    # 曜日の日本語表記
    weekdays = ['月', '火', '水', '木', '金', '土', '日']
    
    # 指定された期間の投票を作成
    for day_offset in range(days):
        current_date = start_date + datetime.timedelta(days=day_offset)
        weekday = weekdays[current_date.weekday()]
        
        # 各日の投票メッセージ
        poll_message = f"**{current_date.month}月{current_date.day}日({weekday})の参加可能時間帯**"
        
        # 9:00から21:00まで、2時間枠（重複あり）の選択肢を作成
        options = []
        for hour in range(9, 20):
            # 利用可能な絵文字数を超えないようにする
            if len(options) < len(EMOJI_NUMBERS):
                options.append(f"{hour:02d}:00-{hour+2:02d}:00")
        
        # 投票メッセージに選択肢を追加
        for i, option in enumerate(options):
            poll_message += f"\n{EMOJI_NUMBERS[i]} {option}"
        
        # 投票メッセージを送信
        try:
            poll = await ctx.send(poll_message)
            
            # リアクションを1つずつ追加（レート制限対策）
            for i in range(len(options)):
                await poll.add_reaction(EMOJI_NUMBERS[i])
                await asyncio.sleep(1)  # 各リアクション間に1秒待機
        except Exception as e:
            await ctx.send(f"エラーが発生しました: {str(e)}")
            return
        
        # 各投票の間に少し待機（レート制限対策）
        await asyncio.sleep(3)
    """
    指定した日から一週間の9:00-21:00の2時間枠（重複あり）の投票を作成します
    使用例: !週間投票作成 2025 4 7
    """
    # 開始日の設定
    start_date = datetime.datetime(年, 月, 日, tzinfo=JST)
    
    # 曜日の日本語表記
    weekdays = ['月', '火', '水', '木', '金', '土', '日']
    
    # 投票メッセージを送信し、正常に送信できたか確認
    try:
        intro_msg = await ctx.send(f"**{年}年{月}月{日}日から一週間の予定投票**\n各日の参加可能な時間帯に投票してください（複数選択可）")
        await asyncio.sleep(1)  # 少し待機
    except Exception as e:
        await ctx.send(f"メッセージ送信中にエラーが発生しました: {str(e)}")
        return  # エラーがあれば中断
    
    # 7日間分の投票を作成
    for day_offset in range(7):
        current_date = start_date + datetime.timedelta(days=day_offset)
        weekday = weekdays[current_date.weekday()]
        
        # 各日の投票メッセージ
        poll_message = f"**{current_date.month}月{current_date.day}日({weekday})の参加可能時間帯**"
        
        # 9:00から21:00まで、2時間枠（重複あり）の選択肢を作成
        options = []
        for hour in range(9, 20):
            # 利用可能な絵文字数を超えないようにする
            if len(options) < len(EMOJI_NUMBERS):
                options.append(f"{hour:02d}:00-{hour+2:02d}:00")
        
        # 投票メッセージに選択肢を追加
        for i, option in enumerate(options):
            poll_message += f"\n{EMOJI_NUMBERS[i]} {option}"
        
        # 投票メッセージを送信
        poll = await ctx.send(poll_message)
        
        # リアクションを追加
        for i in range(len(options)):
            await poll.add_reaction(EMOJI_NUMBERS[i])
        
        # 各投票の間に少し待機（レート制限対策）
        await asyncio.sleep(3)
        
        # エラーがあれば報告
        try:
            for i in range(len(options)):
                await poll.add_reaction(EMOJI_NUMBERS[i])
                await asyncio.sleep(1)  # 各リアクション追加の間に待機
        except Exception as e:
            await ctx.send(f"エラーが発生しました: {str(e)}")

@bot.command(name='投票作成')
async def create_poll(ctx, タイトル, *選択肢):
    """
    カスタム投票を作成します
    使用例: !投票作成 "好きな食べ物は？" "ラーメン" "寿司" "カレー"
    """
    if len(選択肢) > 10:
        await ctx.send("選択肢は最大10個までです。")
        return
    
    # 投票メッセージを作成
    poll_message = f"**{タイトル}**"
    for i, option in enumerate(選択肢):
        poll_message += f"\n{EMOJI_NUMBERS[i]} {option}"
    
    # 投票メッセージを送信
    poll = await ctx.send(poll_message)
    
    # リアクションを追加
    for i in range(len(選択肢)):
        await poll.add_reaction(EMOJI_NUMBERS[i])

@bot.command(name='ヘルプ')
async def help_command(ctx):
    """ボットのコマンド一覧と使い方を表示します"""
    help_message = """
**投票ボットの使い方**

**`!週間投票作成 [年] [月] [日]`**
指定した日から一週間の9:00-21:00の2時間枠（重複あり）の投票を作成します
例: `!週間投票作成 2025 4 7`

**`!期間投票作成 [開始年] [開始月] [開始日] [終了年] [終了月] [終了日]`**
指定した期間の9:00-21:00の2時間枠（重複あり）の投票を作成します（最大31日間）
例: `!期間投票作成 2025 4 7 2025 4 15`

**`!投票作成 [タイトル] [選択肢1] [選択肢2] ...`**
カスタム投票を作成します（最大10個の選択肢）
例: `!投票作成 "今週末の活動は？" "オンライン会議" "Discord通話" "スキップ"`

**`!ヘルプ`**
このヘルプメッセージを表示します
"""
    await ctx.send(help_message)

# 設定ファイルからトークンを読み込む
import os
import json

# config.jsonファイルからトークンを読み込む
def load_config():
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("エラー: config.jsonファイルが見つかりません。")
        print("config.json.exampleをconfig.jsonにリネームし、Botトークンを設定してください。")
        exit(1)
    except json.JSONDecodeError:
        print("エラー: config.jsonの形式が正しくありません。")
        exit(1)

# 設定を読み込み
config = load_config()

# Botを実行
bot.run(config['token'])