from cash_machine import BankAccount
from cash_machine import accounts_list
from file import BankAccountFileReader


class AuthBankAccount:

    __bank_account_authenticated = None

    @staticmethod
    def authenticate(account_number, passwd):
        bank_account_fr = BankAccountFileReader()
        account = bank_account_fr.get_account(account_number)
        if account and AuthBankAccount.__has_bank_account_valid(account, account_number, passwd):
            AuthBankAccount.__bank_account_authenticated = account
            return account
        return False

    @staticmethod
    def __has_bank_account_valid(account: BankAccount, account_number: str, passwd: str):
        return account.check_account_number(account_number) and \
            account.check_passwd(passwd)

    @staticmethod
    def get_authenticate_account() -> BankAccount:
        return AuthBankAccount.__bank_account_authenticated
