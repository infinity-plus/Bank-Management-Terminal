# This File contains all the sql functions requireed in the project including a) Create Account b) Transaction option with Bank -> Bank, Bank-> Customer, Customer -> Bank, c) Transaction History, d) Delete Account
import mysql.connector
from datetime import date, datetime
from date_verifier import date_input

Date = date.today().strftime('%Y/%m/%d')
mydb = mysql.connector.connect(host='localhost',
                               user='root',
                               passwd='admin')
mycursor = mydb.cursor(buffered=False)
mycursor1 = mydb.cursor(buffered=False)
mycursor.execute('Create database if not exists bank_Management')
mycursor.execute('Use Bank_Management')
mycursor.execute('create table if not exists user(account char(17) Primary Key, name Varchar(20) Not Null, Phone char(11) Not Null,email varchar(35) Unique Not Null, Balance int(10) check(Balance >-1) Not Null, transid varchar(25) not null, TOA varchar(10) Not Null, DOC date Not Null)')
mycursor.execute('create table if not exists trans(Sender char(17) references user(account), Beneficiary char(17) references user(account), transid varchar(25) not null, date date not null, amount int(10))')
mycursor.execute(
    'create table if not exists amount(transid varchar(25) not null Primary Key,Sender_amount char(17), Beneficiary_amount char(17) )')

def check_details(email):
    mycursor.execute('Select email from user')
    if(mycursor):
        for j in mycursor:
            if(email in j):
                return (False, 'Email Already Exists in database')
    return (True,)

def new_user(name, phone, email):
    if not(phone.isdigit() and len(phone) == len(phone)):
        return (False, "Please Enter Digits in Mobile number and/or Enter mobile number without country code\n")
    if not(check_details(email)[0]):
        return check_details(email)
    if(len(name) <= 20):
        if(len(email) <= 35):
            pass
        else:
            return(False, "Kindly Enter Email within 35 characters\n")
    else:
        return(False, "Kindly Enter Name within 20 Characters\n")

    account = datetime.today().strftime('%Y%m%d%H%M%S%f')[:16]
    mycursor.execute("Insert into user values(%s,%s,%s,%s,%s,%s,%s,%s)",
                     (account, name, phone, email, 1000, account+'1', "savings", Date))
    mycursor.execute("Insert into trans values('Self', %s, %s, %s, %s)",
                     (account, account+'1', Date, 1000))
    mycursor.execute("Insert into amount values(%s,%s,%s)",
                     (account+'1', "Null", 1000))
    mydb.commit()
    return (True, "Successfully new Account Created with account number - "+account+"\nFirst Transaction id is " + account+'1')

def account_details(reciever):
    mycursor.execute(
        "Select account, name, email, Balance from user where account = %s", (reciever,))
    f = mycursor.fetchall()
    return f

def check_balance(account):
    mycursor.execute("select balance from user where account = %s", (account,))
    a = mycursor.fetchall()
    return a[0][0]

def account_number(Name):
    mycursor.execute(
        'select account, name from user where name like %s', ('%'+Name+'%',))
    return mycursor.fetchall()

def transid(account):
    mycursor.execute("select transid from user where account = %s", (account,))
    for i in mycursor:
        print(account + str(int(i[0][16:])+1))
        return (account + str(int(i[0][16:])+1))

def trans(amount, mode, account, reciever='Self'):
    if(mode == 1):
        if(int(check_balance(str(account))) >= 1000+int(amount)):
            if(amount < 1):
                return "Please Enter Valid Amount"
            mycursor.execute(
                "Select account, name, email from user where account = %s", (reciever,))
            for i in mycursor:
                print(i, end='')
            print()
            a = input(
                'Press Y if the above details about the reciever are correct\n').lower()
            if(a == 'y'):
                tid = str(int(transid(account))+1)
                mycursor.execute("insert into trans values(%s,%s,%s,%s,%s)", (
                    account, reciever, tid, date.today().strftime('%Y/%m/%d'), amount))
                mycursor.execute("insert into amount values(%s,%s,%s)", (tid, check_balance(
                    str(account)) - amount, check_balance(str(account)) + amount))
                mycursor1.execute(
                    "Update user set balance = balance - %s where account = %s", (amount, account))
                mycursor1.execute(
                    "Update user set balance = balance + %s and transid = %s where account = %s", (amount, tid, reciever))
                mydb.commit()
                return f"{amount} Rs has been transferred from {account} to {reciever}"
            return "Transaction is Aborted"
        return "Insufficient Balance"

    if(mode == 2):
        tid = str(int(transid(account))+1)
        if(check_balance(str(account)) >= amount+1000):
            mycursor.execute("insert into trans values(%s,'self',%s,%s,%s)",
                             (account, tid, date.today().strftime('%Y/%m/%d'), amount))
            mycursor.execute("insert into amount values(%s,%s,%s)",
                             (tid, check_balance(amount)-amount, "Null"))
            mycursor.execute(
                "update user set balance = balance -%s where account = %s", (amount, account))
            mycursor.execute(
                "update user set balance = balance +%s and transid = %s where account = %s", (amount, tid, reciever))
            mydb.commit()
            return str(amount) + " Rs has been withdrawn from " + account
        return "Insufficient Balance"

    if(mode == 3):
        tid = str(int(transid(account))+1)
        mycursor.execute("insert into trans values('self', %s, %s, %s,%s)",
                         (account, tid, date.today().strftime('%Y/%m/%d'), amount))
        mycursor.execute("insert into amount values(%s,%s,%s)",
                         (tid, "Null", check_balance(str(account))+int(amount)))
        mycursor.execute(
            "update user set balance = balance + %s where account = %s", (amount, account))
        mycursor.execute(
            "update user set transid = %s where account = %s", (tid, account))
        mydb.commit()
        return f'{amount} rs has been credited to {account}'

    if(mode == 4):
        tid = str(int(transid(account))+1)
        mycursor.execute("insert into trans values(%s,'self',%s,%s,%s)", (account,
                                                                          tid, date.today().strftime('%Y/%m/%d'), check_balance(str(account))))
        mycursor.execute(
            "insert into amount values(%s,%s,%s)", (tid, 0, "Null"))
        mycursor.execute("delete from user where account = %s", (account,))
        mycursor.execute(
            "update user set balance = balance +%s and transid = %s where account = %s", (amount, tid, reciever))
        mydb.commit()
        return str(amount) + " Rs has been withdrawn from " + account + " with transid "+tid+" and Account Has been Closed"

def istransid(account, transid):
    mycursor.execute(
        "Select transid from trans where sender = %s or beneficiary = %s", (account, account))
    for i in mycursor.fetchall():
        if i[0] == transid:
            return True
    return False

def trans_history(account):
    while(True):
        a = input("Enter \n1. For only Transid Searched Transaction \n2. For Transaction between Specific Date Range \n3. For Transaction Made on a day\n")
        if(a.isdigit()):
            a = int(a)
            if(a in range(1, 4)):
                if(a == 1):
                    transid = input("Enter transid\n")
                    if(istransid(account, transid)):
                        i = []
                        mycursor.execute(
                            "select transid, sender, beneficiary, date, sender_amount from trans natural join amount where trans.transid = %s and sender = %s", (transid, account))
                        i.append(mycursor.fetchone())
                        mycursor1.execute(
                            "select transid, sender, beneficiary, date, Beneficiary_amount from trans natural join amount where trans.transid = %s and beneficiary = %s", (transid, account))
                        i.append(mycursor1.fetchone())
                        return(True, i)
                    return(False, "Incorrect transid Provided")
                if(a == 2):
                    b = date_input()
                    if(b[0] is True):
                        print('Enter Second Date')
                        c = date_input()
                        if(c[0]):
                            mycursor.execute(
                                "select transid, sender, beneficiary, date, sender_amount from trans natural join amount where sender = %s and Date between %s and %s", (str(account), b[1], c[1]))
                            e = mycursor.fetchall()
                            mycursor1.execute(
                                "select transid, sender, beneficiary, date, beneficiary_amount from trans natural join amount where Date between %s and %s and beneficiary = %s", (b[1], c[1], account))
                            f = mycursor1.fetchall()
                            i = [e, f]
                            return (True, i)
                        return (False, c[1])
                    return (False, b[1])
                b = date_input()
                if(b[0] is True):
                    i = []
                    mycursor.execute(
                        "select transid, sender, beneficiary, date, sender_amount from trans natural join amount where Date = %s and sender = %s", (b[1], account))
                    i.append(mycursor.fetchall())
                    mycursor1.execute(
                        "select transid, sender, beneficiary, date, Beneficiary_amount from trans natural join amount where Date = %s and beneficiary = %s", (b[1], account))
                    i.append(mycursor1.fetchall())
                    return (True, i)
                return (False, b[1])

def close_account(account):
    if(check_balance(str(account)) == '0'):
        k = input(
            "Are you Sure to delete Account, Press Y to continue, Else press any key to exit").lower()
        if(k != 'y'):
            return "Operation Cancelled"
        mycursor.execute("delete from user where account = %s", (account,))
        mydb.commit()
        return "Account deleted Successfully"
    balance = check_balance(str(account))
    trans(check_balance(account), 4, account)
    mycursor.execute("delete from user where account = %s", (account,))
    mydb.commit()
    return f"Account deleted succesfully and Rs {balance} will be returned to you as cash"

def select_account(name):
    k, j = 0, []
    l = "Srno. Name Account_Number".split()
    mycursor.execute(
        'select name, account from user where name like %s', (name,))
    for i in mycursor.fetchall():
        if(k == 0):
            for m in l:
                print(m, end='')
            print()
        j.append(i)
        print(str(k+1)+'>', i[0], i[1], '\n')
        k += 1
    if(k == 0):
        return (False, "Account Does't Exsist\n")
    while(True):
        a = input("\nEnter Serial number\n")
        if(a.isdigit()):
            a = int(a)
            if(a > 0 and a < int(k+1)):
                return (True, j[int(a)-1][1])
            print("Please Select from given\n")
        else:
            print("Please enter digits only\n")