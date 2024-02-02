import os
from datetime import datetime, timedelta

import requests

"""
<사전 출석체크>
10월 31일 화요일, 저녁 운동 출석 체크하겠습니다. (19:00~22:00)
"""


def main():
    text_dic = {
        0: ["월요일", "오전", "09:30～12:00"],
        1: ["화요일", "저녁", "19:00～22:00"],
        2: ["수요일", "오전", "09:30～12:00"],
        3: ["목요일", "저녁", "19:00～22:00"],
        4: ["금요일", "오전", "09:30～12:00"],
        5: ["토요일", "주말", "14:00～17:00"],
        6: ["일요일", "주말", "14:00～17:00"],
    }

    tomorrow: datetime = datetime.now() + timedelta(1)

    text_monthday = tomorrow.strftime('%m월 %d일')
    text_weekday = text_dic[tomorrow.weekday()][0]
    text_timetype = text_dic[tomorrow.weekday()][1]
    text_timefromto = text_dic[tomorrow.weekday()][2]

    msg = f"""<사전 출석체크>
{text_monthday} {text_weekday}, {text_timetype} 운동 출석 체크하겠습니다. ({text_timefromto})
    """
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
