import os
from datetime import datetime, timedelta

import requests
import boto3

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get("WUXIJIA_TB")

table = dynamodb.Table(table_name)

"""
<사전 출석체크>
10월 31일 화요일, 저녁 운동 출석 체크하겠습니다. (19:00~22:00)

"""


def main():
    # {'dayInKorean': '월요일', 'comment': '', 'ampm': '오전', 'day': 'Monday', 'time': '09:30～12:00'}
    # {'dayInKorean': '화요일', 'comment': '예약 코트 수 : 2개', 'ampm': '저녁', 'day': 'Tuesday', 'time': '19:00~21:00'}
    # {'dayInKorean': '수요일', 'comment': '', 'ampm': '오전', 'day': 'Wednesday', 'time': '09:30～12:00'}
    # {'dayInKorean': '목요일', 'comment': '예약 코트 수 : 2개', 'ampm': '저녁', 'day': 'Thursday', 'time': '19:00~21:00'}
    # {'dayInKorean': '금요일', 'comment': '', 'ampm': '오전', 'day': 'Friday', 'time': '09:30～12:00'}
    # {'dayInKorean': '토요일', 'comment': '예약 코트 수 : 4개 \n\n주말운동 게스트는 오전 11시 이후 신청 가능합니다. (28명 이상시 신청 불가)', 'ampm': '주말', 'day': 'Saturday', 'time': '14:00~17:00'}
    # {'dayInKorean': '일요일', 'comment': '예약 코트 수 : \n14:00~15:00 코트 2개\n15:00~17:00 코트 3개 \n\n주말운동 게스트는 오전 11시 이후 신청 가능합니다. (21명 이상시 신청 불가)', 'ampm': '주말', 'day': 'Sunday', 'time': '14:00~17:00'}

    tomorrow: datetime = datetime.now() + timedelta(1)
    day = tomorrow.strftime("%A")  # Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday

    key = {
        'day': day
    }
    # 항목 가져오기
    response = table.get_item(Key=key)

    # 항목 출력
    if 'Item' in response:
        text_dic = response['Item']
        # print(text_dic)
    else:
        print('항목을 찾을 수 없습니다.')

    text_monthday = tomorrow.strftime('%m월 %d일')

    text_weekday = text_dic['dayInKorean']
    text_timetype = text_dic['ampm']
    text_timefromto = text_dic['time']
    text_comment = text_dic['comment']

    msg = f"""<사전 출석체크>
{text_monthday} {text_weekday}, {text_timetype} 운동 출석 체크하겠습니다. ({text_timefromto})
"""
    if text_comment:
        msg += "----------------------------\n"
        msg += text_comment
    print(msg)
    send_message(msg)


def send_message(msg):
    url = os.environ.get("WEBHOOK_URL")
    header = {
    }
    data = {
        "content": msg
    }
    response = requests.post(url, header, data)
    print(response.status_code)
    print(response.text)


if __name__ == '__main__':
    main()
