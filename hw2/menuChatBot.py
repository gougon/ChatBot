from flask import abort
from chatBotConfig import channel_secret, channel_access_token
from linebot import WebhookHandler, LineBotApi
from linebot.exceptions import InvalidSignatureError
from linebot.models import FollowEvent, TextSendMessage, MessageEvent, TextMessage, PostbackEvent

handler = WebhookHandler(channel_secret)
line_bot_api = LineBotApi(channel_access_token)

welcomeMessage = TextSendMessage(text='歡迎修習AlertBot課程')
menuMessage = TextSendMessage(text='請開啟選單點選所需功能')
createUserMessage = TextSendMessage(text='收到，我將為您辦理註冊手續')
deleteUserMessage = TextSendMessage(text='收到，我將為您辦理退出手續')
userListMessage = TextSendMessage(text='收到，我將為您呈現人員列表')
updateUserMessage = TextSendMessage(text='收到，我將為您辦理資料修改手續')
errorMessage = TextSendMessage(text='哦，這超出我的能力範圍......')

# Webhook
def lineWebhook(request):
    # get X-Line-Signature header value
    signature = request.headers.get('X-Line-Signature')

    # get request body as text
    body = request.get_data(as_text=True)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return '200 OK'

# Follow Event
@handler.add(FollowEvent)
def handle_follow(event):
    replyMessages = [welcomeMessage, menuMessage]
    line_bot_api.reply_message(event.reply_token, replyMessages)

# Message Event
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    command = event.message.text

    if command in ['1', '註冊', '報名']:
        replyMessages = createUserMessage
    elif command in ['2', '退出', '退選']:
        replyMessages = deleteUserMessage
    elif command in ['3', '列表', '清單']:
        replyMessages = userListMessage
    elif command in ['4', '修改', '變更']:
        replyMessages = updateUserMessage
    else:
        replyMessages = [errorMessage, menuMessage]

    line_bot_api.reply_message(event.reply_token, replyMessages)

# Postback Event
@handler.add(PostbackEvent)
def handle_postback(event):
    command = event.postback.data

    if command == 'createUser':
        replyMessages = createUserMessage
    elif command == 'deleteUser':
        replyMessages = deleteUserMessage
    elif command == 'userList':
        replyMessages = userListMessage
    elif command == 'updateUser':
        replyMessages = updateUserMessage

    line_bot_api.reply_message(event.reply_token, replyMessages)