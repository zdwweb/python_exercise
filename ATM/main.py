import sys
import os
import pymysql


conn = pymysql.connect(user="root", host='localhost', passwd="zdw15175529059")
cur = conn.cursor()
conn.select_db("work")


class Customer:
    money = None
    name = None

    def __init__(self, cardID, password):
        self.cardID = cardID
        self.password = password


class ATM:
    time = 0

    def welcome(self, cstm):
        if self.check_pswd(cstm):
            self.menu(cstm)
        else:
            self.lock()

    def check_pswd(self, cstm):
        cur.execute("select * from cstm_information")
        conn.commit()
        re = cur.fetchall()
        for r in re:
            if r[0] == cstm.cardID and r[2] == cstm.password:
                cstm.name, cstm.money = r[1], r[3]
                return True
        else:
            return False

    def change_pswd(self, cstm):

        self.time = 0
        while self.time < 3:
            old_pswd = input("请输入旧密码：")
            if old_pswd == cstm.password:
                break
            self.time += 1
        else:
            self.lock()
        while True:
            new_pswd = input("请输入新密码：")
            if new_pswd != old_pswd:
                new_pswd1 = input("确认输入新密码:")
                if new_pswd1 == new_pswd and len(new_pswd1) == 6:
                    cstm.password = new_pswd
                    update_pswd = 'update cstm_information set password=%s where card_id=%s'
                    cur.execute(update_pswd, (new_pswd1, cstm.cardID))
                    conn.commit()
                    print("修改密码成功")
                    break
                else:
                    print("你输入的两次密码不一样，请重新输入!")
            else:
                print("密码不能与旧密码相同且为6位数")

    def fetch_money(self, cstm):
        while True:
            mn = float(input("请输入提取金额"))
            if mn > cstm.money:
                print("余额不足")
            if mn < cstm.money:
                cstm.money -= mn
                update_money = "update cstm_information set money=money-%s where card_id=%s"
                cur.execute(update_money, (mn, cstm.cardID))
                conn.commit()
                print("取款成功")
            operater = input("是否继续取款 Y/N ")
            if operater == 'N' or operater == 'n':
                print("取款操作结束")
                break

    def reserve_money(self, cstm):
        while True:
            mn = float(input("请输入存入金额"))
            if mn > 10000:
                print("请一次性存入小于10000元")
            else:
                cstm.money += mn
                update_money = "update cstm_information set money=money+%s where card_id=%s"
                cur.execute(update_money, (mn, cstm.cardID))
                conn.commit()
                print("存款成功")
            operater = input("是否继续存款 Y/N ")
            if operater == 'N' or  operater == 'n':
                print("存款操作结束")
                break

    def transfer_accounts(self, cstm):
        while True:
            flag = 0
            confirm = 1 #  默认可以输入金额
            while True:
                other_id = input("请输入转账卡号:")
                cur.execute("select * from cstm_information")
                conn.commit()
                re = cur.fetchall()
                for r in re:
                    if r[0] == other_id:
                        confirm = r
                        flag = 1
                        break
                else:
                    print("不存在该账号")
                    operater = input("是否重新转账 Y/N ")
                    if operater == 'N' or operater == 'n':
                        confirm = 0
                        print("转账操作结束")
                        break
                if flag == 1:
                    break
            if confirm ==0:
                break
            mn = float(input("请输入转账金额:"))
            if mn > cstm.money:
                print("余额不足")
            else:
                print('确认信息')
                print(f'id:{confirm[0]},name:{confirm[1]},transfer:{mn}')
                temp = input()
                cstm.money -= mn
                host_money = "update cstm_information set money=money-%s where card_id=%s"
                cur.execute(host_money, (mn, cstm.cardID))
                conn.commit()
                other_money = "update cstm_information set money=money+%s where card_id=%s"
                cur.execute(other_money, (mn, other_id))
                conn.commit()
                print('转账成功')
            operater = input("是否继续转账 Y/N ")
            if operater == 'N' or operater == 'n':
                print("转账操作结束")
                break

    def information(self, cstm):
        print("用户姓名:{0}\n卡号:{1}\n余额:{2}\n".format(cstm.name, cstm.cardID, cstm.money))

    def lock(self):
        cur.close()
        conn.close()
        print("感谢你对本银行的支持，欢迎下次光临！")
        print("请取卡")
        sys.exit(0)

    def exit(self):
        print("退出系统")
        cur.close()
        conn.close()
        sys.exit(0)

    def menu(self, cstm):
        menu_ifms = '\n 1)余额查询\n2）修改密码\n3）取款\n4）存款\n5)转账\n6) 退出系统\n'
        while True:
            print(menu_ifms)
            num = int(input("请输入操作序号："))
            if num == 1:
                self.information(cstm)
            elif num == 2:
                self.change_pswd(cstm)
            elif num == 3:
                self.fetch_money(cstm)
            elif num == 4:
                self.reserve_money(cstm)
            elif num == 5:
                self.transfer_accounts(cstm)
            elif num == 6:
                self.exit()
            operater = input("是否返回菜单栏 Y/N ")
            if operater == 'N' or operater == 'n':
                self.exit()


def main():
    print('---------------欢迎使用---------------')
    card_id = input("please input card_id:")
    password = input("please input password:")
    cstm = Customer(card_id, password)
    ATM().welcome(cstm)


main()
