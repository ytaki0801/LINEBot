import os
from flask              import Flask, request, abort
from linebot            import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models     import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

bot = LineBotApi(os.environ["ACCESS_TOKEN"])
handler = WebhookHandler(os.environ["CHANNEL_SECRET"])

@app.route("/", methods=['POST'])
def callback():
    sign = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, sign)
    except InvalidSignatureError:
        abort(400)
    return('OK')

@handler.add(MessageEvent, message=TextMessage)
def handle_message(e):
    replyMes = e.message.text
    replyMes = '『help』以外の送信メッセージそのままオウム返しします．'
    bot.reply_message(e.reply_token, TextSendMessage(text=replyMes))

if __name__ == "__main__":
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
