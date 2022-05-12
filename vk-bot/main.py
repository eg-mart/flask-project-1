from session import get_session
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from reply import send_answer
import random
import json
import os


def main():
    longpoll = VkBotLongPoll(get_session(), os.environ.get("GROUP_ID"))
    step = 0

    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            if step == 0:
                if event.obj.message['text'] == 'Начать':
                    send_answer(event.obj.message['from_id'], step)
                else:
                    send_answer(event.obj.message['from_id'])


if __name__ == '__main__':
    main()
