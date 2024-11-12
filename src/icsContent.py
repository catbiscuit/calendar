from getGovCalendar import govContent
from getBaiduCalendar import baiduContent

def getics(festival_lst, year):
    print("BEGIN:VCALENDAR")
    print("VERSION:2.0")
    print("X-WR-CALNAME:" + str(year) + "订阅法定节假日")
    print("X-APPLE-CALENDAR-COLOR:#FBD36A")
    print("X-WR-TIMEZONE:Asia/Shanghai")

    festival_lst = sorted(festival_lst, key=lambda x: x.dt)

    idx = 1
    for item in festival_lst:
        formatted_date = item.dt.strftime("%Y%m%d")
        print("BEGIN:VEVENT")
        print("UID:" + str(year) + "-" + f"{idx:04d}")
        print("DTSTART;VALUE=DATE:" + formatted_date)
        print("DTEND;VALUE=DATE:" + formatted_date)
        print("SUMMARY:" + item.festivalTips)
        print("SEQUENCE:0")
        print("BEGIN:VALARM")
        print("TRIGGER;VALUE=DATE-TIME:19760401T005545Z")
        print("ACTION:NONE")
        print("END:VALARM")
        print("END:VEVENT")

        idx += 1

    print("END:VCALENDAR")


def main():
    year = 2025
    # festival_lst1 = govContent(year)
    # getics(festival_lst1, year)

    festival_lst2 = baiduContent(year)
    getics(festival_lst2, year)


if __name__ == '__main__':
    main()
