from fastapi import FastAPI, Request, HTTPException

from linebot import (
    WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, QuickReplyButton, MessageAction, FlexSendMessage
)

import User
import Messenger

from dotenv import load_dotenv
import os

load_dotenv()
CHANNEL_SECRET = str(os.environ["CHANNEL_SECRET"])

handler = WebhookHandler(CHANNEL_SECRET)

app = FastAPI()

@app.post("/callback")
async def callback(request: Request):
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = await request.body()

    # handle webhook body
    try:
        handler.handle(body.decode("utf-8"), signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        HTTPException(400)

    return 'OK'

# 年代リスト
age_list = []
for age in range(1, 8):
    tmp = str(age * 10) + "代"
    if age == 1:
        tmp += "以下"
    elif age == 7:
        tmp += "以上"

    age_list.append(tmp)

user_data = {}

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    user_input = event.message.text
    messenger = Messenger.Messenger(event)

    # データを格納していないユーザから"おすすめのお土産教えて"と言われたとき
    if user_id not in user_data and user_input == "おすすめのお土産教えて":

        # ユーザ情報作成、データ格納
        user = User.User(user_id)
        user_data[user_id] = user

        # 性別選択用メッセージ
        messenger.reply(
            [
                TextSendMessage(text = "わかりました！よりあなたが気に入りそうな新千歳空港のお土産をおすすめするために、あなたについて教えてください"),
                messenger.quick_reply(
                text = "まず、あなたの性別を教えてください",
                items = [
                    QuickReplyButton(action = MessageAction(label = "男性", text = "男性")),
                    QuickReplyButton(action = MessageAction(label = "女性", text = "女性")),
                    QuickReplyButton(action = MessageAction(label = "その他", text = "その他")),
                    ]
                )
            ]
        )

        user.update_step()

    # 格納済みユーザからのメッセージの時
    elif user_id in user_data:
        user = user_data[user_id]
        step = user.step

        # 性別を受け取ったとき
        if step == 1 and user_input in ["男性", "女性", "その他"]:
            user.set_gender(user_input)

            user.update_step()

            items =[
                QuickReplyButton(action = MessageAction(label = age, text = age))
                for age in age_list
                    ]

            # クイックリプライの選択肢付き年代選択メッセージ
            messenger.reply(
                messenger.quick_reply(
                    text = "ありがとうございます！\n次に、あなたの年代を教えてください",
                    items = items
                )
            )

        # 年代を受け取ったとき    
        elif step == 2 and user_input in age_list:
            user.set_age(user_input)

            # おすすめ結果を返信するメッセージ
            messenger.reply(
                [
                    TextSendMessage(text = f"ありがとうございます！\n{user.age}{user.gender}がよく検索している新千歳空港のお土産は以下になります"),
                    FlexSendMessage(alt_text = "おすすめのお土産3件", contents = {"type": "carousel", "contents": [messenger.flex_message(), messenger.flex_message(), messenger.flex_message()]}),
                    TextSendMessage(text = "またおすすめのお土産が知りたくなったら、「おすすめのお土産教えて」をタップしてみてくださいね！")
                ]
            )

            # 最後のステップを終えたのでユーザのデータは消す
            user_data.pop(user_id)

        # なんかおかしいとき
        else:
            messenger.reply(
                TextSendMessage(text = "入力内容がおかしいかもしれません。もう一度「おすすめのお土産教えて」をタップしてやり直してみてください")
            )

            user_data.pop(user_id)

    # 格納してないユーザから"おすすめのお土産教えて"以外のことを言われたとき
    else:
        messenger.reply(
            TextSendMessage(text = "「おすすめのお土産教えて」をタップしてみてください！")
        )