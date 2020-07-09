import os
from flask          import Flask, request
from linebot        import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage

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
    r = e.message.text
    if (r.lower() == 'help'):
        r = '『help』以外の送信メッセージはそのままオウム返しします．'
    else:

        OK = [ '茨城', '茨城県', '栃木', '栃木県', '群馬', '群馬県', '東京', '東京都', '千葉', '千葉県']
        NO = [ '神奈川', '神奈川県', '埼玉', '埼玉県' ]
        r += 'に高専はありま'
        if r in OK:
            r += 'す．'
        elif r in NO:
            r += 'せん．'
        else:
            r = '関東の県名を送信して下さい．'

    B.reply_message(e.reply_token, TextSendMessage(text=r))

if __name__ == "__main__":
    p = int(os.getenv("PORT"))
    A.run(host="0.0.0.0", port=p)
