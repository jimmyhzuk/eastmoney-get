# coding=utf-8

import requests
import os
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

class Eastmoney():
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.money = self.get_percentage_1()

    @staticmethod
    def getabstrs(a, b, strs):# a|str|b
        if a == '':
            return strs[:strs.find(b)]
        elif b == '':
            return strs[strs.find(a) + len(a):]
        else:
            strs = strs[strs.find(a) + len(a):]
            return strs[:strs.find(b)]

    @staticmethod
    def gethtml(url, headers):
        return requests.get(url, headers=headers).content.decode()

    @staticmethod
    def headers(referer=None, cookie=None):
        # a reasonable UA
        ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
        headers = {'User-Agent': ua}
        if referer is not None:
            headers.update({'Referer': referer})
        if cookie is not None:
            headers.update({'Cookie': cookie})
        return headers

    def main_url(self):
        return 'http://fund.eastmoney.com/%s.html' % self.id
        
    def get_percentage_1(self):
        return self.getabstrs('ui-font-middle ui-color-red ui-num">', '%</span>', self.gethtml(self.main_url(), self.headers(referer='http://fund.eastmoney.com/')))

if __name__ == '__main__':
    def post_mail(my_sender, my_pass, to_users, my_message):
        ret = True
        try:
            msg=MIMEText(my_message, 'plain', 'utf-8')
            msg['From']=formataddr(["noreply", 'noreply@mail.com'])    # 括号里的对应发件人邮箱昵称、发件人邮箱账号
            msg['To']=formataddr(["someone", 'someone@mail.com'])        # 括号里的对应收件人邮箱昵称、收件人邮箱账号
            msg['Subject'] = "基金七日年化报告"                # 邮件的主题，也可以说是标题
            server=smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是465
            server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
            server.sendmail(my_sender, to_users, msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
            server.quit() # 关闭连接
        except Exception:
            ret = False
        return ret

    def eastmoneySort(data):
        eastmoney = [Eastmoney(id,name) for (id,name) in data]
        eastmoney.sort(key=lambda x:x.money,reverse=True)#由大到小,降序输出
        #for element in eastmoney:
        #    print(element.name,":",element.money)
        return eastmoney

    def need_change(first_id): # 优化为ini配置文件
        if os.access("eastmoney.ini", os.F_OK):
            with open('eastmoney.ini',"r", encoding="utf-8") as f:
                id_choice = f.read()
                if id_choice == first_id:
                    return 0
                else:
                    return 1
        else:
            f = open('eastmoney.ini', "w", encoding="utf-8")
            f.write('id')
            f.close()
            print('!!!Please enter the section "id":"name" in the document to start!!!')
            exit()

    data = [
        ('180008', '支付宝-银华货币A'),
        ('000638', '微信-富国富钱包货币'),
        ('000569', '京东-鹏华增值宝货币')
    ]
    data_list = eastmoneySort(data)
    if need_change(data_list[0].id):
        print('need change!!!')
        with open('eastmoney.ini', "w", encoding="utf-8") as f:
	        f.write(data_list[0].id)
        massage = '现在基金七日年化百分比排列出现变化！！！' \
            +'\n第一为:'+data_list[0].name+'\n七日年化百分比:'+data_list[0].money \
            +'\n第二为:'+data_list[1].name+'\n七日年化百分比:'+data_list[1].money \
            +'\n第三为:'+data_list[2].name+'\n七日年化百分比:'+data_list[2].money
        ret = post_mail('你的qq邮箱', '你的qq邮箱stmp密码', ['injahow@qq.com'], massage)
        if ret:
            print("邮件发送成功!!!")
        else:
            print("邮件发送失败???")
    else:
        print('all ok!!!')
