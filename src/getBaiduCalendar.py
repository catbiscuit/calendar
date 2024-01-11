import json
import time
from datetime import datetime

import requests

from festivalInfo import FestivalModel


def baiduContent(year):
    festival_lst = []
    # 因该接口传入的时间，查询了前一个月，当前月和后一个月的数据，所以只需要2、5、8、11即可全部获取到。比如查询5月份，则会查询4,5,6月分的数据
    months = ["2", "5", "8", "11"]

    for month in months:
        ts = int(time.time() * 1000)
        domain = "https://sp1.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?tn=wisetpl&format=json&resource_id=39043&query="
        url = domain + str(year) + "年" + month + "月&t=" + str(ts)

        response = requests.get(url)
        content = response.text

        root = json.loads(content)
        almanac = root["data"][0]["almanac"]
        for item in almanac:
            if ('status' in item and item["status"] == '1'):
                current_date = convert_to_date(item["year"] + "年" + item["month"] + "月" + item["day"] + "日", year)
                festival = ''
                if ('term' in item):
                    festival = item["term"]
                fest = FestivalModel(current_date, festival, '', 1)
                festival_lst.append(fest)
            elif ('status' in item and item["status"] == '2'):
                current_date = convert_to_date(item["year"] + "年" + item["month"] + "月" + item["day"] + "日", year)
                festival = ''
                if ('term' in item):
                    festival = item["term"]
                fest = FestivalModel(current_date, festival, '', 2)
                festival_lst.append(fest)

    for item in festival_lst:
        if item.status == 1:
            item.festivalTips = item.festival + '(休息)'
        else:
            item.festivalTips = item.festival + '(补班)'

    festival_lst = [item for item in festival_lst if item.dt >= datetime.strptime(str(year) + "-01-01", "%Y-%m-%d")]
    return festival_lst


def convert_to_date(date, year):
    if "年" not in date:
        date = str(year) + '年' + date

    date_obj = datetime.strptime(date, "%Y年%m月%d日")
    return date_obj


def main():
    print('main')


if __name__ == '__main__':
    main()
