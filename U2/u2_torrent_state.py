# -*- coding: utf-8 -*-

# by kysdm
# 瞎几把写的，语法乱七八糟，写的好看费时间
# last_page 为种子页面最后一页，这个计算是从0开始的
# 会一直重试下载元素，除非手动暂停，不然它是不会停的 (
# 没有用多线程，估计会很慢 (
# 综上，网络差的话，凉凉
#
# 如如要走代理，请删除', proxies=proxies'

import os
import re
import time
import requests
import xlsxwriter
from bs4 import BeautifulSoup


# **************用户变量********************

cookie = '__cfduid=xxxx; nexusphp_u2=xxxx; __dtsu=xxxx'
last_page = 1
# 代理
proxies = {'http': '127.0.0.1:1000',
           'https': '127.0.0.1:1000'
           }

# **************用户变量********************


def openhtml(page):
    headers = {
        'Referer': f'https://u2.dmhy.org/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0',
        'cookie': cookie
    }
    i = 0
    main_list = []
    while i <= page:
        while True:
            _page = i + 1
            print(f'正在下载第{_page}页的元素...')
            try:
                html = requests.get(
                    f'https://u2.dmhy.org/torrents.php?inclbookmarked=0&incldead=0&spstate=0&page={i}', headers=headers, proxies=proxies, timeout=5)
                soup = BeautifulSoup(html.text, 'lxml')
                html = soup.find_all('tr')
                i += 1
                print('下载完成，开始处理元素...\n')
                break
            except requests.exceptions.RequestException as e:
                print(f'第{_page}下载失败，错误代码：{e}\n\n等待15秒后重试')
                time.sleep(15)

        # 提取包含种子信息的html
        html_list = []
        for v in html:
            v = str(v)
            re1 = re.search(
                r'<td\s?class="rowfollow\s?nowrap"\s?valign="middle">', v, re.S)
            re2 = re.search(
                r'<td\s?class="embedded\s?overflow-control">', v, re.S)
            re3 = re.search(r'<\/b><\/a><\/td><\/tr>$', v, re.S)
            if re1 and re2 and re3:
                html_list.append(v)

        for v in html_list:
            # re1 = re.search(r'title="置顶"', v, re.S)
            # if re1:
            re1 = re.compile(r'<a\s?href="\?cat=\d+?">(.+?)<\/a>', re.S)  # 分类
            re2 = re.compile(
                r'<tr><td\s?class="embedded\s?overflow-control">.*?<a\s?class="tooltip"\s?href="details\.php\?id=\d+?&amp;hit=1">(.+?)<\/a><\/td>', re.S)  # 标题
            re3 = re.compile(
                r'<a\s?href="viewsnatches\.php\?id=(\d+)">', re.S)  # ID
            re4 = re.search(r'#startcomments">(\d+?)<\/a>', v, re.S)  # 评论数量
            re5 = re.compile(
                r'<time>(\d{4}-\d{2}-\d{2})<br\s?\/>(\d{2}:\d{2}:\d{2})<\/time>', re.S)  # 时间
            re6 = re.compile(
                r'<td\sclass="rowfollow">(\d+?\.\d+?)<br\s?\/>(\w+?)<\/td>', re.S)  # 大小
            # re7 = re.compile(r'#seeders">(\d+?)<\/a>', re.S)
            re7 = re.search(r'#seeders">(\d+?)<\/a>', v, re.S)  # 上传人数
            re8 = re.search(r'#leechers">(\d+?)<\/a>', v, re.S)  # 下载人数
            re9 = re.search(
                r'<a\shref="viewsnatches\.php\?id=\d+?"><b>(\d+?)<\/b><\/a>', v, re.S)  # 完成人数

            _classification = (re.findall(re1, v))[0].replace('<br/>', ' ')

            _Title = (re.findall(re2, v))[0]

            _id = (re.findall(re3, v))[0]

            if re4:
                re4 = re.compile(r'#startcomments">(\d+?)<\/a>', re.S)  # 评论数量
                _Comment_quantity = (re.findall(re4, v))[0]
            else:
                _Comment_quantity = '0'

            _time = f'{(re.findall(re5, v))[0][0]} {(re.findall(re5, v))[0][1]}'

            _Size = (re.findall(re6, v))[0]
            _Size = f'{(re.findall(re6, v))[0][0]} {(re.findall(re6, v))[0][1]}'

            if re7:
                re7 = re.compile(r'#seeders">(\d+?)<\/a>', re.S)  # 上传人数
                _Upload_number = (re.findall(re7, v))[0]
            else:
                _Upload_number = '0'
            if re8:
                re8 = re.compile(r'#leechers">(\d+?)<\/a>', re.S)  # 下载人数
                _Download_number = (re.findall(re8, v))[0]
            else:
                _Download_number = '0'
            if re9:
                re9 = re.compile(
                    r'<a\shref="viewsnatches\.php\?id=\d+?"><b>(\d+?)<\/b><\/a>', re.S)  # 完成人数
                _Completion_number = (re.findall(re9, v))[0]
            else:
                _Completion_number = '0'
            if 'rowfollow snatchhlc_finish' in v:
                _download_progress = '完成'
                if 'rowfollow seedhlc_current'in v:
                    _download_progress = '当前做种中'
            else:
                _download_progress = '未下载过'

        # ----------------------------------------------------------------------------------
        #               1                |           2         |         3            |
        #                                |    未完成下载        |                      |    1
        # 当前未做种，历史做种时间<1天     |                     |       完成           |    2
        # 当前未做种，历史做种时间<1天     |                     |       做种/辅种过    |    3
        # 当前未做种，历史做种时间>1天     |                     |       完成           |    4
        # 当前未做种，历史做种时间>1天     |                     |       做种/辅种过     |    5
        # 当前做种中                      |                     |       做种/辅种过     |    6
        # 当前做种中                      |                     |        完成          |    7
        #                                |                     |        完成           |    8
        #                               |   当前下载中          |                      |    9
        #                               |                       |                      |    10
        # -------------------------------------------------------------------------------------
            if '未完成下载' in v:
                _download_progress = 1
            elif '做种时间&lt;1天' in v and '完成' in v:
                _download_progress = 2
            elif '做种时间&lt;1天' in v and '辅种过' in v:
                _download_progress = 3
            elif '做种时间&gt;1天' in v and '完成' in v:
                _download_progress = 4
            elif '做种时间&gt;1天' in v and '辅种过' in v:
                _download_progress = 5
            elif '当前做种中' in v and '辅种过' in v:
                _download_progress = 6
            elif '当前做种中' in v and '完成' in v:
                _download_progress = 7
            elif '当前下载中' in v:
                _download_progress = 9
            elif '完成' in v:
                _download_progress = 8
            else:
                _download_progress = 10
            main_list.append((_classification, _id, _Title,  _time, _Size, _download_progress,
                              _Upload_number, _Download_number, _Completion_number, _Comment_quantity))
    return main_list


def excel(_list):
    workbook = xlsxwriter.Workbook(f'{abs_path}/U2.xlsx')  # 新建文件
    worksheet = workbook.add_worksheet()  # 新建sheet

    headings = ['分类', 'ID', '标题', '添加时间', '大小', '下载状态',
                '上传', '下载', '完成', '评论']  # 设置表头
    # 我可去你妈的吧
    # Unfortunately, there is no way to specify “AutoFit” for a column in the Excel file format. This feature is only available at runtime from within Excel. It is possible to simulate “AutoFit” in your application by tracking the maximum width of the data in the column as your write it and then adjusting the column width at the end.
    # 指定列宽
    worksheet.set_column(0, 0, 18)
    worksheet.set_column(1, 1, 10)
    worksheet.set_column(2, 2, 125)
    worksheet.set_column(3, 3, 28)
    worksheet.set_column(4, 4, 16)
    worksheet.set_column(5, 5, 34)
    worksheet.set_column(6, 6, 10)
    worksheet.set_column(7, 7, 10)
    worksheet.set_column(8, 8, 10)
    worksheet.set_column(9, 9, 10)

    # 表格属性
    workbook.set_properties({'title': 'U2 种子列表'})

    # 标题样式
    cell_format1 = workbook.add_format()
    cell_format1.set_font_name('微软雅黑')
    cell_format1.set_font_size(18)
    cell_format1.set_font_color('#5F497A')
    cell_format1.set_align('center')
    cell_format1.set_bold()
    cell_format1.set_align('vcenter')
    cell_format1.set_bg_color('#CCC0DA')  # 图案的背景色

    # 通用样式
    cell_format2 = workbook.add_format()
    cell_format2.set_font_name('微软雅黑')
    cell_format2.set_font_size(12)
    cell_format2.set_font_color('#5F497A')
    cell_format2.set_align('center')
    cell_format2.set_align('vcenter')
    cell_format2.set_border(1)  # 边框
    cell_format2.set_bg_color('#DCE6F1')  # 背景色
    cell_format2.set_border_color('#F5F5F5')  # 边框颜色
    # 标题样式
    cell_format3 = workbook.add_format()
    cell_format3.set_font_name('微软雅黑')
    cell_format3.set_font_size(12)
    cell_format3.set_font_color('#5F497A')
    cell_format3.set_align('left')
    cell_format3.set_align('vcenter')
    cell_format3.set_border(1)  # 边框
    cell_format3.set_bg_color('#DCE6F1')  # 背景色
    cell_format3.set_border_color('#F5F5F5')  # 边框颜色
    # b0c4de
    b0c4de = workbook.add_format()
    b0c4de.set_font_name('微软雅黑')
    b0c4de.set_font_size(12)
    b0c4de.set_font_color('#5F497A')
    b0c4de.set_align('center')
    b0c4de.set_align('vcenter')
    b0c4de.set_border(1)  # 边框
    b0c4de.set_bg_color('#B0C4DE')  # 背景色
    b0c4de.set_border_color('#F5F5F5')  # 边框颜色
    # cd853f
    cd853f = workbook.add_format()
    cd853f.set_font_name('微软雅黑')
    cd853f.set_font_size(12)
    cd853f.set_font_color('#5F497A')
    cd853f.set_align('center')
    cd853f.set_align('vcenter')
    cd853f.set_border(1)  # 边框
    cd853f.set_bg_color('#cd853f')  # 背景色
    cd853f.set_border_color('#F5F5F5')  # 边框颜色
    # 20b2aa
    _20b2aa = workbook.add_format()
    _20b2aa.set_font_name('微软雅黑')
    _20b2aa.set_font_size(12)
    _20b2aa.set_font_color('#5F497A')
    _20b2aa.set_align('center')
    _20b2aa.set_align('vcenter')
    _20b2aa.set_border(1)  # 边框
    _20b2aa.set_bg_color('#20b2aa')  # 背景色
    _20b2aa.set_border_color('#F5F5F5')  # 边框颜色
    # add8e6
    _add8e6 = workbook.add_format()
    _add8e6.set_font_name('微软雅黑')
    _add8e6.set_font_size(12)
    _add8e6.set_font_color('#5F497A')
    _add8e6.set_align('center')
    _add8e6.set_align('vcenter')
    _add8e6.set_border(1)  # 边框
    _add8e6.set_bg_color('#add8e6')  # 背景色
    _add8e6.set_border_color('#F5F5F5')  # 边框颜色
    # 87cefa
    _87cefa = workbook.add_format()
    _87cefa.set_font_name('微软雅黑')
    _87cefa.set_font_size(12)
    _87cefa.set_font_color('#5F497A')
    _87cefa.set_align('center')
    _87cefa.set_align('vcenter')
    _87cefa.set_border(1)  # 边框
    _87cefa.set_bg_color('#87cefa')  # 背景色
    _87cefa.set_border_color('#F5F5F5')  # 边框颜色
    # 32cd32
    _32cd32 = workbook.add_format()
    _32cd32.set_font_name('微软雅黑')
    _32cd32.set_font_size(12)
    _32cd32.set_font_color('#5F497A')
    _32cd32.set_align('center')
    _32cd32.set_align('vcenter')
    _32cd32.set_border(1)  # 边框
    _32cd32.set_bg_color('#32cd32')  # 背景色
    _32cd32.set_border_color('#F5F5F5')  # 边框颜色
    # 6495ed
    _6495ed = workbook.add_format()
    _6495ed.set_font_name('微软雅黑')
    _6495ed.set_font_size(12)
    _6495ed.set_font_color('#5F497A')
    _6495ed.set_align('center')
    _6495ed.set_align('vcenter')
    _6495ed.set_border(1)  # 边框
    _6495ed.set_bg_color('#6495ed')  # 背景色
    _6495ed.set_border_color('#F5F5F5')  # 边框颜色

    # 插入数据
    worksheet.write_row('A1', headings, cell_format1)
    i = 1
    for v in _list:
        if v[5] == 1:
            status = '未完成下载'
            Upload = cell_format2
            Download = b0c4de
            Completion = cell_format2
        elif v[5] == 2:
            status = '未做种/做种<1天/完成'
            Upload = cd853f
            Download = cell_format2
            Completion = _20b2aa
        elif v[5] == 3:
            status = '未做种/做种<1天/做种/辅种过'
            Upload = cd853f
            Download = cell_format2
            Completion = _add8e6
        elif v[5] == 4:
            status = '做种>1天/完成'
            Upload = _87cefa
            Download = cell_format2
            Completion = _20b2aa
        elif v[5] == 5:
            status = '未做种/做种>1天/做种/辅种过'
            Upload = _87cefa
            Download = cell_format2
            Completion = _add8e6
        elif v[5] == 6:
            status = '做种中/做种/辅种过'
            Upload = _32cd32
            Download = cell_format2
            Completion = _add8e6
        elif v[5] == 7:
            status = '做种中/完成'
            Upload = _32cd32
            Download = cell_format2
            Completion = _20b2aa
        elif v[5] == 8:
            status = '完成'
            Upload = cell_format2
            Download = cell_format2
            Completion = _20b2aa
        elif v[5] == 9:
            status = '下载中'
            Upload = cell_format2
            Download = _6495ed
            Completion = cell_format2
        elif v[5] == 10:
            status = '未下载'
            Upload = cell_format2
            Download = cell_format2
            Completion = cell_format2

        worksheet.write(i, 0, v[0], cell_format2)
        worksheet.write(i, 1, v[1], cell_format2)
        worksheet.write(i, 2, v[2], cell_format3)
        worksheet.write(i, 3, v[3], cell_format2)
        worksheet.write(i, 4, v[4], cell_format2)
        worksheet.write(i, 5, status, cell_format2)
        worksheet.write(i, 6, v[6], Upload)
        worksheet.write(i, 7, v[7], Download)
        worksheet.write(i, 8, v[8], Completion)
        worksheet.write(i, 9, v[9], cell_format2)
        i += 1
    workbook.close()  # 保存并关闭
    i -= 1  # 一个是0开始计算 一个是1开始计算
    print(f'共插入{i}条种子信息')


if __name__ == '__main__':
    abs_path = os.path.split(os.path.realpath(__file__))[0]
    f = openhtml(last_page)
    print(f'共查找到{len(f)}种子信息')
    excel(f)
