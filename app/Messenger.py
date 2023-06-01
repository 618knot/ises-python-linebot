from linebot import (
    LineBotApi
)

from linebot.models import (
    TextSendMessage, QuickReply
)

from dotenv import load_dotenv
import os

load_dotenv()
CHANNEL_ACCESS_TOKEN = str(os.environ["CHANNEL_ACCESS_TOKEN"])

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)

class Messenger:
    def __init__(self, event) -> None:
        self.event = event

    def reply(self, content):
        line_bot_api.reply_message(
            self.event.reply_token,
            content)
    
    def quick_reply(self, text: str, items: list):
            return TextSendMessage(
                text = text,
                quick_reply = QuickReply(
                    items = items
                )
            )

    def flex_message(self):
        flex_message_template = {
            "type": "bubble",
            "hero": {
                "type": "image",
                "url": "https://image.rakuten.co.jp/hokkaido-omiyage/cabinet/meika3/kankou_bs2021.jpg",
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover",
                "action": {
                "type": "uri",
                "uri": "https://www.new-chitose-airport.jp/ja/spend/shop/s20.html"
                }
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "text",
                    "text": "白いブラックサンダー",
                    "weight": "bold",
                    "size": "xl"
                },
                {
                    "type": "text",
                    "text": "￥999,999,999(税込)"
                },
                {
                    "type": "text",
                    "text": "なにか適当な説明とかあれば",
                    "style": "normal",
                    "color": "#666666"
                }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                    "type": "uri",
                    "label": "リンクはこちら",
                    "uri": "https://www.new-chitose-airport.jp/ja/spend/shop/s20.html"
                    }
                }
                ],
                "flex": 0
            }
            }
        
        return flex_message_template


