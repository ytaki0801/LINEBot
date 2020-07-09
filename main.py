import os
from flask          import Flask, request
from linebot        import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage

HELP = '都道府県名（『茨城』や『東京都』）を送信すると，その都道府県に高専があるかどうかが返信されます．'
OK0 = [ '北海道', '東京', '東京都', '京都', '京都府', '大阪', '大阪府' ]
OK1 = [ '青森', '岩手', '宮城', '秋田', '山形', '福島' ]
OK2 = [ '茨城', '栃木', '群馬', '千葉' ]
OK3 = [ '新潟', '富山', '石川', '福井', '長野', '岐阜', '静岡', '愛知' ]
OK4 = [ '三重', '兵庫', '奈良', '和歌山' ]
OK5 = [ '鳥取', '島根', '岡山', '広島', '山口', '徳島', '香川', '愛媛', '高知' ]
OK6 = [ '福岡', '長崎', '熊本', '大分', '宮崎', '鹿児島', '沖縄' ]
OK = OK1 + OK2 + OK3 + OK4 + OK5 + OK6
OK += OK0 + list(map(lambda x: x+'県', OK))
NO = [ '神奈川', '埼玉', '山梨', '滋賀', '佐賀' ]
NO += list(map(lambda x: x+'県', NO))

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
        r = u + 'に高専はありま'
        if u in OK:
            r += 'す．'
        elif u in NO:
            r += 'せん．'
        else:
            r = '都道府県名を送信して下さい．'
    B.reply_message(e.reply_token, TextSendMessage(text=r))

if __name__ == "__main__":
    p = int(os.getenv("PORT"))
    A.run(host="0.0.0.0", port=p)
