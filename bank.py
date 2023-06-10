
from datetime import date

class Bank:
    __balance=0
    __loan=True
    __total_loan=0
    def __init__(self, name, amount) -> None:
        self.name=name
        self.add_balance(amount)
    
    @classmethod
    def balance(self):
        return self.__balance
    @classmethod
    def add_balance(self, amount):
        self.__balance+=amount

    @classmethod
    def deduct_balance(self, amount):
        self.__balance-=amount

    @classmethod
    def set_loan_flag(self, flag:bool):
        self.__loan=flag

    @classmethod
    def add_loan(self, amount):
        self.__total_loan+=amount
    
    @classmethod
    def see_loans(self):
        return self.__total_loan
    @classmethod
    def loan_status(self):
        return self.__loan


class userDatabase:
    # 'email':'pas'
    __user_credentials={}
    # 'email':user
    __user_list={}
    def __init__(self, name, initial_deposit) -> None:
        self.name=name
        self.__balance=initial_deposit
        Bank.add_balance(initial_deposit)
        self.state_ment=statement()
        
    @classmethod
    def userPassMatch(self, email, passs) -> bool:
       if email in self.__user_credentials:
           if self.__user_credentials[email] == passs:
               print("Access granted!")
               return True
           else:
               print("Access Denied!")
               return False
       else:
           print("User not found!")
           return False

    @classmethod
    def get_user(self, email):
            return self.__user_list[email]

    @classmethod
    def add_credintial(self, email, passs, user) -> bool:
        if email in self.__user_credentials:
            print('Email already exist')
            return False
        else:
            self.__user_credentials[email]=passs
            self.__user_list[email]=user
            return True
    
    def add_balance(self, amount):
        if amount>0:
            self.__balance+=amount
    
    def deduct_balance(self, amount):
        self.__balance-=amount
    
    def eligibility_for_wd(self, amount) -> bool:
        if amount <= Bank.balance() and amount <= self.__balance:
            return True
        else:
            return False

    @classmethod
    def transfer_to(self, email, amount) -> bool:
        if email in self.__user_list:
            # proceed trnasfer
            user=self.__user_list[email]
            user.db.add_balance(amount)
            user.db.state_ment.add_transaction(tx_date=date.today(), tx_type='FT', tx_amount=amount, tx_account='self')
            return True
        else:
            print("User not found.")
            return False
    
    @property
    def balance(self):
        return self.__balance

    @property
    def history(self):
        return self.state_ment.__repr__()

class adminDatabase:
    # 'adminEmail':'pass'
    __adminCredentials={}
    # 'adminEmail':'admin'
    __adminList={}

    def __init__(self, name) -> None:
        self.name=name
        
    @classmethod
    def adminPassMatch(self, email, passs) -> bool:
       if email in self.__adminCredentials:
           if self.__adminCredentials[email] == passs:
               print("Access granted!")
               return True
           else:
               print("Access Denied!")
               return False
       else:
           print("No such an Admin found!")
           return False

    @classmethod
    def get_admin(self, email):
            return self.__adminList[email]

    @classmethod
    def add_credintial(self, email, passs, admin) -> bool:
        if email in self.__adminCredentials:
            print('Email already exist')
            return False
        else:
            self.__adminCredentials[email]=passs
            self.__adminList[email]=admin
            return True
    

class statement:
    def __init__(self) -> None:
        # date ---- tansaction type ---- email ----- ammount
        self.txID=0
        # txID:field
        self.date={}
        self.transaction_type={}
        self.account_no={}
        self.amount={}

    def __repr__(self) -> str:
        statement_='Date\t-\tTransaction Type\t-\tAccount NO.\t-\tAmount\n'
        statement_+='----------------------------------------------------------------------------\n'
        for tx in range(1,self.txID+1):
            statement_+=f'{self.date[tx]}\t\t-\t{self.transaction_type[tx]}\t\t-\t{self.account_no[tx]}\t\t-\t{self.amount[tx]}\n'
        return statement_
    
    def add_transaction(self, **kwargs):
        self.txID+=1
        self.date[self.txID]=kwargs['tx_date']
        self.transaction_type[self.txID]=kwargs['tx_type']
        self.account_no[self.txID]=kwargs['tx_account']
        self.amount[self.txID]=kwargs['tx_amount']
    

class user:
    def __init__(self) -> None:
        self.status=False
        self.db=None

    def create_account(self, name, deposit, email, password) -> None:
        self.db=userDatabase(name, deposit)
        if self.db.add_credintial(email, password,self):
            print(f'Thank you {name}! Balance: {deposit}')
            self.status=True

    def login(self, email, pas):
        if userDatabase.userPassMatch(email,pas):
            self.status=True
            return userDatabase.get_user(email)
        return self
        
    def get_balance(self):
        if self.isActive:
            return self.db.balance
    
    def deposit(self, amount):
        if self.isActive:
            self.db.add_balance(amount)
            Bank.add_balance(amount)
            # tx_date=date.today().strftime(%d %m %Y)
            # print(tx_date)
            self.db.state_ment.add_transaction(tx_date=date.today(), tx_type='Deposit', tx_amount=amount, tx_account='self')

    def withdraw(self, amount):
        if self.isActive:
            if(self.db.eligibility_for_wd(amount)):
                self.db.deduct_balance(amount)
                Bank.deduct_balance(amount)
                self.db.state_ment.add_transaction(tx_date=date.today(), tx_type='W.Draw', tx_amount=(-amount), tx_account='self')
            elif self.db.balance < amount:
                print("Sorry, insufficient balance")
            else:
                print('The bank is bankrupt')

    def fund_transfer(self, email, amount):
        if self.isActive:
            if self.get_balance() >= amount:
                if self.db.transfer_to(email, amount):
                    self.db.deduct_balance(amount)
                    print('Fund transfer is successful. New balance:', self.get_balance(), 'BDT')
                    self.db.state_ment.add_transaction(tx_date=date.today(), tx_type='FT', tx_amount=(-amount), tx_account='Other')
            else:
                print('Insufficient balance')

    def transaction_history(self):
        if self.isActive:
            print(self.db.history)

    def take_loan(self, amount):
        if self.isActive:
            if Bank.loan_status():
                if amount<=2*self.get_balance() and amount<=Bank.balance():
                    self.db.add_balance(amount)
                    Bank.deduct_balance(amount)
                    Bank.add_loan(amount)
                    print(f'Loan request of amount: {amount} BDT, has been accepted. Your new balance: {self.get_balance()}')
                    self.db.state_ment.add_transaction(tx_date=date.today(), tx_type='Loan', tx_amount=amount, tx_account='self')
                else:
                    print('The amount is too large')
            else:
                print('Loan is not available')
    
    # as the object may be empty or not having database, isActive method is used to handle that case:
    @property
    def isActive(self) -> bool:
        if self.status==True:
            return True
        else:
            return False

class admin:
    def __init__(self) -> None:
        self.status=False
        self.db=None

    def create_account(self, name, email, password) -> None:
        self.db=adminDatabase(name)
        if self.db.add_credintial(email, password,self):
            print(f'Welcome Mr. {name}!')
            self.status=True

    def login(self, email, pas):
        if adminDatabase.adminPassMatch(email,pas):
            self.status=True
            return adminDatabase.get_admin(email)
        return self

    def see_total_loan(self):
        return Bank.see_loans()
    
    def see_total_bal(self):
        return Bank.balance()
    
    def set_loan(self, activation:bool):
        Bank.set_loan_flag(activation)

    
# -----------------------------------
# code runs from here:

def user_logged_in(user):
    i=input('1. Check Balance\t 2. Deposit \t 3. Withdraw \t 4. Transfer \t 5. History \t 6. Loan\n')
    match i:
        case '1':
            print('Your balance: ', user.get_balance())
        case '2':
            amount=int(input('Input amount: '))
            user.deposit(amount)
            print('Successfully diposited tk', amount, '- Balance: ',user.get_balance())
        case '3':
            amount=int(input('Enter amount:\t'))
            if amount>0:
                user.withdraw(amount)
                print('Withdraw amount:',amount,'successfully. Balance:',user.get_balance(),'BDT')
            else:
                print('Zero amount not accepted')
        case '4':
            amount=int(input('Enter amount:\t'))
            if amount<=0:
                print('Amount can\'t be zero.')
                return
            email=input('Enter user email:\t')
            user.fund_transfer(email, amount)

        case '5':
            user.transaction_history()
        case '6':
            amount=int(input('Enter loan amount:\t'))
            if amount>0:
                user.take_loan(amount)
            else:
                print('Amount can\'t be zero.')
        case _:
            print('Invalid')

def userFunctions():
    print('1. log in\t\t2. Sign Up')
    i=input()
    if i=='1':
        # login credentials:
        email=input('Email:\t')
        pas=input('Password:\t')
        usr=user()
        usr=usr.login(email, pas)
        if usr.status:
            user_logged_in(usr)
    elif i == '2':
        # signing up
        email=input("Enter email:\t\t")
        pas=input("Enter password:\t\t")
        name=input('Enter your name:\t\t')
        amount=int(input('Enter diposited amount:\t\t'))
        usr=user().create_account(email=email, name=name, deposit=amount,password=pas)

def admin_logged_in(ad):
    i=input('1. Check Bank Balance\t 2. Check Loan Amount\t 3. Set Loan Feature on/off\n')
    match i:
        case '1':
            print(f'Balance: {ad.see_total_bal()}')
        case '2':
            print(f'Loan: {ad.see_total_loan()}')
        case '3':
            states='Deactivate'
            print('Current loan setting: ', end='')
            if Bank.loan_status()==True:
                print('Active')
            else:
                print('Deactive')
                states='Activate'
            print('Choose an operation:')
            i=input(f'1. {states}\t 2. Cancel\n')
            if i=='1':
                if states== 'Activate':
                    ad.set_loan(True)
                else:
                    ad.set_loan(False)
        case _:
            print('Invalid')


def adminFunctions():
    print('1. log in\t\t2. Sign Up')
    i=input()
    if i=='1':
        # login credentials:
        email=input('Email:\t')
        pas=input('Password:\t')
        ad=admin()
        ad=ad.login(email,pas)
        if ad.status:
            admin_logged_in(ad)
    elif i == '2':
        # signing up
        email=input("Enter email:\t\t")
        pas=input("Enter password:\t\t")
        name=input('Enter your name:\t\t')
        ad=admin().create_account(email=email, name=name,password=pas)

b=Bank('Any bank', 100)
while(True):
    print('Welcome to our Bank, are you an User or Admin?')
    print('1. User\t\t2. Admin')
    i =input()
    if i == '1':
        # user functions:
        userFunctions()
    elif i == '2':
        # admin funtions:
        adminFunctions()
    else:
        print('invalid')
        break

