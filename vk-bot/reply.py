import random
from session import get_session
import vk_api
import json


def generate_answer(user_id, step=-1):
    replies = json.load(open('vk-bot/replies.json', 'r', encoding='utf-8'))
    order = replies['order']

    if step >= 0:
        reply_name = order[step]
    else:
        reply_name = 'error'

    reply = replies[reply_name]

    if len(reply['attachments']) > 0:
        uploaded = []
        for photo_name in reply['attachments']:
            photo_path = replies['attachments_dir'] + '/' + photo_name
            upload  = vk_api.VkUpload(get_session())
            photo = upload.photo_messages(photo_path, user_id)
            uploaded.append(f"photo{photo[0]['owner_id']}_{photo[0]['id']}")
        reply['attachments'] = ','.join(uploaded)
    
    return reply


def send_answer(user_id, step=-1):
    answer = generate_answer(user_id, step)
    vk = get_session().get_api()
    vk.messages.send(user_id=user_id,
                     message=answer['message'],
                     keyboard=json.dumps(answer['keyboard']),
                     attachment=answer['attachments'],
                     random_id=random.randint(0, 2 ** 64))


def get_user(user_id):
    vk = get_session().get_api()
    return vk.users.get(user_id=user_id)
