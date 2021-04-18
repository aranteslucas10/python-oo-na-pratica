import getpass

from auth import AuthBankAccount
from cash_machine import CashMachineWithDraw, CashMachineInsertMoneyBill


class AuthBankAccountConsole:

    @staticmethod
    def is_auth():
        account_number_typed = input('Digite sua conta: ')
        passwd_typed = getpass.getpass('Digite sua senha: ')
        return AuthBankAccount.authenticate(account_number_typed, passwd_typed)


class CashMachineConsole:

    @staticmethod
    def call_operation() -> None:
        option_typed = CashMachineConsole.__get_menu_options_typed()
        CashMachineOperation.do_operation(option_typed)

    @staticmethod
    def __get_menu_options_typed() -> int:
        print(f"{CashMachineOperation.OPERATION_SHOW_BALANCE} - Saldo")
        print(f"{CashMachineOperation.OPERATION_WITHDRAW} - Saque")
        account = AuthBankAccount.get_authenticate_account()
        if account.admin:
            print(f"{CashMachineOperation.OPERATION_INSERT_MONEY_BILL} - Iserir cédulas")
        return int(input('Escolha uma das opções acima: '))


class CashMachineOperation:

    OPERATION_SHOW_BALANCE = 1
    OPERATION_WITHDRAW = 2
    OPERATION_INSERT_MONEY_BILL = 10

    @staticmethod
    def do_operation(option):
        account = AuthBankAccount.get_authenticate_account()
        if option == CashMachineOperation.OPERATION_SHOW_BALANCE:
            ShowBalanceOperation.do_operation()
        elif option == CashMachineOperation.OPERATION_WITHDRAW:
            WithDrawOperation.do_operation()
        elif option == CashMachineOperation.OPERATION_INSERT_MONEY_BILL and account.admin:
            InsertMoneyBillOperation.do_operation()


class ShowBalanceOperation:

    @staticmethod
    def do_operation():
        account = AuthBankAccount.get_authenticate_account()
        print(f'Seu saldo é: {account.value}')


class WithDrawOperation:

    @staticmethod
    def do_operation():
        value_typed = int(input("Digite o valor a ser sacado: "))
        account = AuthBankAccount.get_authenticate_account()
        cash_machine = CashMachineWithDraw.withdraw(account, value_typed)
        if cash_machine.value_remaining != 0:
            print('O caixa não tem cédulas disponíveis para este valor.')
        else:
            print('Pegue as notas')
            print(cash_machine.money_slips_user)
            print(account)


class InsertMoneyBillOperation:
    @staticmethod
    def do_operation():
        amount_typed = int(input("Digite a quantidade de cédulas: "))
        money_bill_typed = input("Digite a cédula a ser incluída: ")
        cash_machine = CashMachineInsertMoneyBill.insert_money_bill(money_bill_typed, amount_typed)
        print(cash_machine.money_slips)
