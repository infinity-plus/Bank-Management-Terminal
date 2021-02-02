import Employee_end as Ee

while(True):
    a = input('''Main Menu\n
        1 - New User
        2 - User Details
        3 - Transaction
        4 - Transaction History
        5 - Close Account
        Else press any key to exit\n''')
    if a not in ['1', '2', '3', '4', '5']:
        break
    a = int(a)
    if(a == 1):
        while(True):
            b = input("\nEnter Name\n")
            c = input("\nEnter Phone number\n")
            d = input("\nEnter Email Id\n")
            if not(c.isdigit() or len(c) != 10):
                print("\nKindly enter digits only and/or enter 10 digits only\n")
                e = input(
                    '\nPress Y to try once more, else press any key to main menu\n').lower()
                if(e != 'y'):
                    break
                continue
            e = input(
                f'\nPress Y to create account with details Name = {b}, Phone = {c},Email = {d}, Else press any key to main menu\n').lower()
            if(e != 'y'):
                break
            f = Ee.new_user(b, c, d)
            print(f[1])
            e = input(
                '\nPress y to do again else press any key to main menu\n').lower()
            if(e != 'y'):
                break

    if(a == 2):
        z = 0
        while(z == 0):
            b = '%'+input("\nEnter name of account Holder\n")+'%'
            c = Ee.select_account(b)
            if(c[0]):
                print("\nAccount_Number   Name    Email     Balance\n")
                print(Ee.account_details(c[1]))
                e = input(
                    '\nPress y to do again else press any key to main menu\n').lower()
                if(e != 'y'):
                    z = 1
            else:
                print(c[1])
                e = input(
                    '\nPress y to do again else press any key to main menu\n').lower()
                if(e != 'y'):
                    z = 1

    if(a == 3):
        z = 0
        while(z == 0):
            b = input(
                "\nEnter \n1. For Bank to Bank Transaction \n2. For Cash Withdrawal \n3. For Cash Deposit\nElse any key to Main Menu\n")            
            if not(b.isdigit()):
                break
            if(int(b) not in range(1, 4)):
                break
            if(int(b) == 1):
                c = input("\nEnter Amount in Rupees to transfer\n")
                if not(c.isdigit()):
                    print("\nPlease Enter amount in digits only\n")
                    e = input(
                        '\nPress Y to do again else press any key to main menu\n').lower()
                    if(e != 'y'):
                        z = 1
                        continue
                if(len(c) >= 10):
                    print("\nKindly Enter a small amount\n")
                    e = input(
                        '\nPress Y to do again else press any key to main menu\n').lower()
                    if(e != 'y'):
                        z = 1
                        continue
                else:
                    c = int(c)
                d = '%'+input("\nEnter name of Sender's\n")+'%'
                m = Ee.select_account(d)
                if(m[0]):
                    e = '%'+input("\nEnter name of Beneficiar's\n")+'%'
                    n = Ee.select_account(e)
                    if(n[0]):
                        f = Ee.trans(c, 1, m[1], n[1])
                        print(f)
                        e = input(
                            '\nPress y to do again else press any key to Main Menu\n').lower()
                        if(e != 'y'):
                            z = 1
                            continue
                    else:
                        print(n[1])
                        e = input(
                            '\nPress y to do again else press any key to Main Menu\n').lower()
                        if(e != 'y'):
                            z = 1
                            continue
                else:
                    print(m[1])
                    e = input(
                        '\nPress y to do again else press any key to Main Menu\n').lower()
                    if(e != 'y'):
                        z = 1
                        continue
            elif(int(b) == 2):
                c = input("\nEnter Amount in Rupees to transfer\n")
                if not(c.isdigit()):
                    print("\nPlease Enter amount in digits only\n")
                    e = input(
                        '\nPress y to do again else press any key to Main Menu\n').lower()
                    if(e != 'y'):
                        z = 1
                        continue
                c = int(c)
                d = '%'+input("\nEnter name of Beneficiar\n")+'%'
                e = Ee.select_account(d)
                if(e[0]):
                    f = Ee.trans(c, 2, e[1])
                    print(f)
                    e = input(
                        '\nPress y to do again else press any key to Main Menu\n').lower()
                    if(e != 'y'):
                        z = 1
                        continue
                else:
                    print(e[1])
                    e = input(
                        '\nPress y to do again else press any key to Main Menu\n').lower()
                    if(e != 'y'):
                        z = 1
                        continue
            elif(int(b) == 3):
                c = input("\nEnter Amount in Rupees to transfer\n")
                if not(c.isdigit()):
                    print("\nPlease Enter amount in digits only\n")
                    e = input(
                        '\nPress y to do again else press any key to Main Menu\n').lower()
                    if(e != 'y'):
                        z = 1
                        continue
                else:
                    c = int(c)
                d = '%'+input("\nEnter name of Beneficiar\n")+'%'
                e = Ee.select_account(d)
                if(e[0]):
                    f = Ee.trans(c, 3, e[1])
                    print(f)
                    e = input(
                        '\nPress y to do again else press any key to Main Menu\n').lower()
                    if(e != 'y'):
                        z = 1
                        continue
                else:
                    print(e[1])
                    e = input(
                        '\nPress y to do again else press any key to Main Menu\n').lower()
                    if(e != 'y'):
                        z = 1
                        break

    if(a == 4):
        z = 0
        while(z == 0):
            b = '%'+input("\nEnter name of Account Holder\n")+'%'
            c = Ee.select_account(b)
            if(c[0]):
                d = Ee.trans_history(c[1])
                if(d[0]):
                    k, x, y = 0, 0, 0
                    for i in d[1]:
                        for j in i:
                            if(k == 0 or x == 0):
                                print(
                                    '\ntransid, sender, beneficiary, date, amount\n')
                            print(j, end='')
                            if(y == 0):
                                k += 1
                            else:
                                x += 1
                        print('\n')
                        y += 1
                    if(k == 0 and x == 0):
                        print("\nNo History Founded\n")
                        e = input(
                            '\nPress y to do again else press any key to Main Menu\n').lower()
                        if(e != 'y'):
                            z = 1
                            break
                    else:
                        e = input(
                            '\nPress y to do again else press any key to Main Menu\n').lower()
                        if(e != 'y'):
                            z = 1
                            break
                else:
                    print(d[1])
                    e = input(
                        '\nPress y to do again else press any key to Main Menu\n').lower()
                    if(e != 'y'):
                        z = 1
                        break
            else:
                print(c[1])
                e = input(
                    '\nPress y to do again else press any key to Main Menu\n').lower()
                if(e != 'y'):
                    z = 1
                    break
    elif(a == 5):
        while(True):
            b = '%'+input('\nEnter Name of Customer\n')+'%'
            c = Ee.select_account(b)
            if(c[0]):
                print(Ee.close_account(c[1]))
                e = input(
                    '\nPress y to do again else press any key to Main Menu\n').lower()
                if(e != 'y'):
                    break
            else:
                print(c[1])
                e = input(
                    '\nPress y to do again else press any key to Main Menu\n').lower()
                if(e != 'y'):
                    break