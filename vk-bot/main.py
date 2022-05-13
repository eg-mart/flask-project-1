from session import get_session
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from reply import send_answer, get_user
import random
import json
import os
import re
import requests
from datetime import datetime as dt
from datetime import time, date
from image_generator import generate_image


def validate_time(start, end, occupied_time):
    if end <= start:
        return False
    valid = True
    for time in occupied_time:
        if time[0] < start < time[1] or time[0] < end < time[1]:
            valid = False
            break
    return valid


def main():
    longpoll = VkBotLongPoll(get_session(), os.environ.get("GROUP_ID"))
    step = 0
    api_session = None

    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            user = event.obj.message['from_id']
            text = event.obj.message['text']

            if text.lower() == 'отменить бронирование':
                step = 0

            if step == 0:
                send_answer(user, step)
                step += 1
            
            elif step == 1:
                if text.lower() == 'забронировать':
                    send_answer(user, step)
                    step += 1
                else:
                    send_answer(user)
            
            elif step == 2:
                if text[0] == '8':
                    text = text.replace('8', '+7', 1)
                text = text.replace('(', '')
                text = text.replace(')', '')
                text = text.replace('-', '')
                text = text.replace(' ', '')
                phone_match = re.search('^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{5}$', text)
                if not phone_match:
                    send_answer(user)
                    continue
                phone = phone_match.string
                send_answer(user, step)
                step += 1
            
            elif step == 3:
                user_data = get_user(user)
                if ' ' in text:
                    send_answer(user)
                    continue
                data = {
                    "phone": phone,
                    "password": text,
                }
                r = requests.post('http://10.0.0.100:5000/api/v1/login', json=data)

                if r.status_code == 200:
                    api_session = requests.Session()
                    token = r.json()["access_token"]
                    api_session.headers["Authorization"] = f"Bearer {token}"
                    send_answer(user, step)
                    step += 1
                    continue

                data = {
                    "phone": phone,
                    "password": text,
                    "name": user_data[0]["first_name"],
                    "surname": user_data[0]["last_name"],
                    "is_admin": False
                }
                r = requests.post('http://10.0.0.100:5000/api/v1/users', json=data)

                if r.status_code == 200:
                    r = requests.post('http://10.0.0.100:5000/api/v1/login', json=data)
                    api_session = requests.Session()
                    token = r.json()["access_token"]
                    api_session.headers["Authorization"] = f"Bearer {token}"
                    send_answer(user, step)
                    step += 1
                    continue
                
                send_answer(user)
            
            elif step == 4:
                tables_match = re.match("^([1-6],\s?){1,}[1-6]$|^[1-6]$", text)
                if not tables_match:
                    send_answer(user)
                    continue
                booking = {
                    "user_phone": phone,
                    "tables": text
                }
                send_answer(user, step)
                step += 1
            
            elif step == 5:
                try:
                    d, m, y = map(int, text.split('.'))
                    book_date = date(y, m, d)
                except Exception as e:
                    send_answer(user)
                    continue
                date_str = book_date.strftime('%Y-%m-%d')
                r = api_session.post('http://10.0.0.100:5000/api/v1/occupied-time', json={"date": date_str})
                occupied_time = r.json()['occupied_time']
                generate_image(occupied_time)
                send_answer(user, step)
                step += 1
            
            elif step == 6:
                time_match = re.match("^([0-9]|(1[0-9])|(2[0-4]))-([0-9]|(1[0-9])|(2[0-4]))$", text)
                if not time_match:
                    send_answer(user)
                    continue
                start_hour, end_hour = map(int, text.split('-'))
                if not validate_time(start_hour, end_hour, occupied_time):
                    send_answer(user)
                    continue
                start = time(start_hour, 0, 0)
                booking["datetime"] = dt.combine(book_date, start).strftime("%Y-%m-%d %H:%M:%S")
                booking["duration"] = (end_hour - start_hour) * 60
                send_answer(user, step)
                step += 1
            
            elif step == 7:
                if text.lower() == 'да':
                    r = api_session.post('http://10.0.0.100:5000/api/v1/bookings', json=booking)
                    if r.status_code == 200:
                        send_answer(user, step)
                    else:
                        send_answer(user)
                step = 0


if __name__ == '__main__':
    main()
