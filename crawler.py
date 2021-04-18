import csv

from bs4 import BeautifulSoup
import requests

home_page_request = requests.get("http://www.szrd.gov.cn/szrd_zjrd/szrd_zjrd_rddb/")
home_page_request.encoding = "utf-8"
home_page = home_page_request.text
soup = BeautifulSoup(home_page, "html.parser")
district_list = soup.find_all("ul", {"class": "ul-count"})
all_records = []
for district in district_list:
    district_name = district.find_previous_sibling("h3").get_text()[:-3]
    a_list = district.find_all("a")
    for a in a_list:
        url = "http://www.szrd.gov.cn/szrd_zjrd/szrd_zjrd_rddb/" + a["href"][2:]
        info_request = requests.get(url)
        info_request.encoding = "utf-8"
        info_soup = BeautifulSoup(info_request.text, "html.parser")
        info_box = info_soup.find_all("div", {"class": "act-r"})[0]
        info_list = [district_name]
        name = info_box.contents[1].h2.get_text()
        if "(女)" in name:
            name = name[:-3]
        info_list.append(name)
        info_list.append(info_box.contents[1].h4.get_text())
        info_list.append(info_box.contents[3].h2.get_text())
        info_list.append(info_box.contents[3].h4.get_text())
        info_list.append(info_box.contents[5].h2.get_text())
        info_list.append(info_box.contents[5].h4.get_text())
        info_list.append(info_box.contents[7].h2.get_text())
        info_list.append(info_box.contents[7].h4.get_text())
        info_list.append(info_box.contents[9].h2.get_text())
        info_list.append(info_box.contents[11].h2.get_text())
        all_records.append(info_list)
print(all_records)
with open("深圳市人大代表信息.csv", "w", newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["区", "姓名", "代表类别", "性别", "出生年月", "籍贯", "民族", "党派", "学历", "电子信箱", "工作单位及职务"])
    for info_list in all_records:
        csvwriter.writerow(info_list)
