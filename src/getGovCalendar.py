from datetime import datetime, timedelta

from festivalInfo import FestivalModel


def getfestival(year, content):
    festival_lst = []
    for item in content.split('\n'):
        if not item:
            item = ''
        item = item.strip()
        if item == "":
            continue

        if "放假，" in item:
            idx1 = item.find('、')
            idx2 = item.find('：')
            idx3 = item.find('放假，')

            festival = item[idx1 + 1: idx2]
            date = item[idx2 + 1: idx3]

            if "、" in festival:
                festival_many = festival.split('、')
                festival = festival_many[1]

            appointed_date = convert_to_date(date, year)

            fest = FestivalModel(appointed_date, festival, '', 1)
            festival_lst.append(fest)

            # 处理与周末连休
            if "与周末连休" in item:
                weekday = appointed_date.weekday()
                if weekday == 0:
                    festival_sun = FestivalModel(appointed_date - timedelta(days=1), festival, '', 1)
                    festival_lst.append(festival_sun)
                    festival_sat = FestivalModel(appointed_date - timedelta(days=2), festival, '', 1)
                    festival_lst.append(festival_sat)
                elif weekday == 4:
                    festival_sat = FestivalModel(appointed_date + timedelta(days=1), festival, '', 1)
                    festival_lst.append(festival_sat)
                    festival_sun = FestivalModel(appointed_date + timedelta(days=2), festival, '', 1)
                    festival_lst.append(festival_sun)

        elif "放假调休，" in item:
            idx1 = item.find('、')
            idx2 = item.find('：')
            idx3 = item.find('放假调休，')

            festival = item[idx1 + 1: idx2]
            date_range = item[idx2 + 1: idx3]

            if "、" in festival:
                festival_many = festival.split('、')
                festival = festival_many[1]

            # 处理10月1日至7日这样的日期
            date_continuous = date_range.split('至')
            start = date_continuous[0]
            end = date_continuous[1]
            if "月" not in end:
                end = start[0:start.find('月') + 1] + end
            start_date = convert_to_date(start, year)
            end_date = convert_to_date(end, year)
            current_date = start_date
            while current_date <= end_date:
                fest = FestivalModel(current_date, festival, '', 1)
                festival_lst.append(fest)
                current_date += timedelta(days=1)

            # 处理补班
            many_sentence = item.split('。')
            for single_sentence in many_sentence:
                if "上班" in single_sentence:
                    many_work = single_sentence.split('、')
                    for single_work in many_work:
                        left_bracket = single_work.find('（')
                        date_work = single_work[0:left_bracket]

                        fest = FestivalModel(convert_to_date(date_work, year), festival, '', 2)
                        festival_lst.append(fest)

    for item in festival_lst:
        if item.status == 1:
            item.festivalTips = item.festival + '(休息)'
        else:
            item.festivalTips = item.festival + '(补班)'

    festival_lst = [item for item in festival_lst if item.dt >= datetime.strptime(str(year) + "-01-01", "%Y-%m-%d")]
    return festival_lst


def govContent(year):
    # https://www.gov.cn/zhengce/zhengceku/2022-12/08/content_5730844.htm?eqid=ebafcc500006405b00000006645a1112
    tips2023 = '''
        一、元旦：2022年12月31日至2023年1月2日放假调休，共3天。

    二、春节：1月21日至27日放假调休，共7天。1月28日（星期六）、1月29日（星期日）上班。

    三、清明节：4月5日放假，共1天。

    四、劳动节：4月29日至5月3日放假调休，共5天。4月23日（星期日）、5月6日（星期六）上班。

    五、端午节：6月22日至24日放假调休，共3天。6月25日（星期日）上班。

    六、中秋节、国庆节：9月29日至10月6日放假调休，共8天。10月7日（星期六）、10月8日（星期日）上班。
        '''

    # https://www.gov.cn/zhengce/content/202310/content_6911527.htm
    tips2024 = '''
        一、元旦：1月1日放假，与周末连休。

    二、春节：2月10日至17日放假调休，共8天。2月4日（星期日）、2月18日（星期日）上班。鼓励各单位结合带薪年休假等制度落实，安排职工在除夕（2月9日）休息。

    三、清明节：4月4日至6日放假调休，共3天。4月7日（星期日）上班。

    四、劳动节：5月1日至5日放假调休，共5天。4月28日（星期日）、5月11日（星期六）上班。

    五、端午节：6月10日放假，与周末连休。

    六、中秋节：9月15日至17日放假调休，共3天。9月14日（星期六）上班。

    七、国庆节：10月1日至7日放假调休，共7天。9月29日（星期日）、10月12日（星期六）上班。
        '''

    if year == 2023:
        return getfestival(year, tips2023)
    elif year == 2024:
        return getfestival(year, tips2024)
    else:
        return []


def main():
    print('main')


def convert_to_date(date, year):
    if "年" not in date:
        date = str(year) + '年' + date

    date_obj = datetime.strptime(date, "%Y年%m月%d日")
    return date_obj


if __name__ == '__main__':
    main()
