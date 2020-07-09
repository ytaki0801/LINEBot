import os
from flask          import Flask, request
from linebot        import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage

App = Flask(__name__)

Bot = LineBotApi(os.environ["ACCESS_TOKEN"])
Handler = WebhookHandler(os.environ["CHANNEL_SECRET"])

@App.route("/", methods=['POST'])
def callback():
    body = request.get_data(as_text=True)
    sign = request.headers['X-Line-Signature']
    Handler.handle(body, sign)

@Handler.add(MessageEvent, message=TextMessage)
def handle_message(e):
    replyMes = e.message.text
    if replyMes.lower() == 'help':
        replyMes = '『help』以外の送信メッセージそのままオウム返しします．'
    Bot.reply_message(
        e.reply_token,
        TextSendMessage(text=replyMes)
    )

if __name__ == "__main__":
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
