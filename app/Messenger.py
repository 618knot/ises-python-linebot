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
                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_1_cafe.png",
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover",
                "action": {
                "type": "uri",
                "uri": "http://linecorp.com/"
                }
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "text",
                    "text": "ほげほげ",
                    "weight": "bold",
                    "size": "xl"
                },
                {
                    "type": "text",
                    "text": "￥999,999,999"
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
                    "uri": "https://example.com"
                    }
                }
                ],
                "flex": 0
            }
            }
        
        return flex_message_template


