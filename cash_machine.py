# dependência circular - importar dentro da onde vai ser utilizado
# from file import MoneySlipsFileReader, MoneySlipsFileWriter


class BankAccount:

    def __init__(self, account_number, name, passwd, value, admin) -> None:
        self.account_number = account_number
        self.name = name
        self.passwd = passwd
        self.value = value
        self.admin = admin

    def check_account_number(self, account_number) -> bool:
        return account_number == self.account_number

    def check_passwd(self, passwd) -> bool:
        return passwd == self.passwd

    def balance_debit(self, value):
        self.value -= value

    def __str__(self, *args, **kwargs):
        return f"Account: {self.account_number}, Name: {self.name}, Saldo: {self.value}"


class CashMachineInsertMoneyBill:

    @staticmethod
    def insert_money_bill(money_bill, amount):
        cash_machine = CashMachineGetter.get()
        cash_machine.insert_money_bill(money_bill, amount)
        from file import MoneySlipsFileWriter
        MoneySlipsFileWriter().write_money_slips(cash_machine.money_slips)
        return cash_machine


class CashMachineWithDraw:
    @staticmethod
    def withdraw(account: BankAccount, value):
        cash_machine = CashMachineGetter.get()
        money_slips_user = cash_machine.withdraw(value)
        if money_slips_user:
            CashMachineWithDraw.__balance_debit(account, value)
            from file import MoneySlipsFileWriter
            MoneySlipsFileWriter().write_money_slips(cash_machine.money_slips)
        return cash_machine

    @staticmethod
    def __balance_debit(account, value):
        account.balance_debit(value)
        from file import BankAccountFileWriter
        BankAccountFileWriter().write_bank_account(account)


class CashMachine:

    def __init__(self, money_slips):
        self.money_slips = money_slips
        self.money_slips_user = {}
        self.value_remaining = 0

    def withdraw(self, value):
        self.value_remaining = value

        for money_bill in ['100', '50', '20']:
            self.__calculate_money_slips_user(money_bill)

        if self.value_remaining == 0:
            self.__decrease_money_slips()

        return False if self.value_remaining != 0 else self.money_slips

    def insert_money_bill(self, money_bill, amount):
        self.money_slips[money_bill] += amount

    def __calculate_money_slips_user(self, money_bill: str) -> None:
        actual_value = self.value_remaining // int(money_bill)
        if 0 < actual_value <= self.money_slips[money_bill]:
            self.money_slips_user[money_bill] = actual_value
            self.value_remaining -= actual_value * int(money_bill)

    def __decrease_money_slips(self):
        for key, value in self.money_slips_user.items():
            self.money_slips[key] -= value


class CashMachineGetter:

    @staticmethod
    def get():
        from file import MoneySlipsFileReader
        money_slips = MoneySlipsFileReader().get_money_slips()
        return CashMachine(money_slips)


accounts_list = [
    BankAccount('01-01', 'Fulano', '1', 1000, False),
    BankAccount('02-01', 'Beltrano', '1', 50, False),
    BankAccount('11-11', 'Admin', '1', 10000, True),
]