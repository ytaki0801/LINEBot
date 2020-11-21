# -*- coding: utf-8 -*-
import os
from flask          import Flask, request
from linebot        import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage

HELP = 'Python eval will be executed for input string'

A = Flask(__name__)
B = LineBotApi(os.environ["ACCESS_TOKEN"])
H = WebhookHandler(os.environ["CHANNEL_SECRET"])

@A.route("/", methods=['POST'])
def callback():
    s = request.headers['X-Line-Signature']
    b = request.get_data(as_text=True)
    H.handle(b, s)
    return('OK')

@H.add(MessageEvent, message=TextMessage)
def handle_message(e):
    u = e.message.text
    if (u.lower() == 'help'):
        r = HELP
    else:
        r = eval("str("+u+")")
    B.reply_message(e.reply_token, TextSendMessage(text=r))

if __name__ == "__main__":
    p = int(os.getenv("PORT"))
    A.run(host="0.0.0.0", port=p)
