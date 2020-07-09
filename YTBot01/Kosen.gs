// LINE Messaging API Access Token
var ACCESS_TOKEN = '(dummy)';
// URL for reply
var REPLY_URL = 'https://api.line.me/v2/bot/message/reply';

function doPost(e) {
  var replyToken = JSON.parse(e.postData.contents).events[0].replyToken;
  var userMessage = JSON.parse(e.postData.contents).events[0].message.text;
  var headers = { 
    'Content-Type': 'application/json; charset=UTF-8',
    'Authorization': 'Bearer ' + ACCESS_TOKEN 
  };
  
  if (userMessage.toLowerCase() == 'help') {
    replyMessage = '関東の県名（『茨城』や『東京都』）を送信すると，その県に高専があるかどうかが返信されます．';
  } else {
    var KosenListOK = [ '茨城', '茨城県', '栃木', '栃木県', '群馬', '群馬県', '東京', '東京都', '千葉', '千葉県'];
    var KosenListNO = [ '神奈川', '神奈川県', '埼玉', '埼玉県' ];
    var replyMessage = userMessage + 'に高専はありま';
    if (KosenListOK.includes(userMessage)) replyMessage += 'す．';
    else
    if (KosenListNO.includes(userMessage)) replyMessage += 'せん．';
    else
      replyMessage = '関東の県名を送信して下さい．';
  }

  var payload = JSON.stringify({
    'replyToken' : replyToken,
    'messages': [{
      'type' : 'text',
      'text' : replyMessage
    }]
  })
  
  var options = {
    'headers' : headers,
    'method' : 'post',
    'payload' : payload
  };

  UrlFetchApp.fetch(REPLY_URL, options);
}

