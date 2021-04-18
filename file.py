import os.path
import ast
# dependência cirular
# from cash_machine import BankAccount
import cash_machine


class BankFile:

    BASE_PATH = os.path.dirname(os.path.abspath(__file__))

    def __init__(self):
        self._file = None

    @staticmethod
    def _open_file_bank(mode):  # convenção - protegido
        return open(MoneySlipsFileReader.BASE_PATH + '/_bank_file.dat', mode)

    def _read_lines(self):
        self._file = self._open_file_bank('r')
        lines = self._file.readlines()
        self._file.close()
        return lines

    def _write_lines(self, lines):
        self._file = self._open_file_bank('w')
        self._file.writelines(lines)
        self._file.close()


class BankAccountFileReader(BankFile):

    def get_line_index_of_bank_account(self, account_number):
        lines = self._read_lines()
        for index, line in enumerate(self.__skip_first_line(lines)):
            account = self.__create_bank_account_from_file_line(line)
            if account.check_account_number(account_number):
                return index + 1
        return -1

    def get_account(self, account_number):
        lines = self._read_lines()
        for line in self.__skip_first_line(lines):
            account = self.__create_bank_account_from_file_line(line)
            if account.check_account_number(account_number):
                return account
        return None

    @staticmethod
    def __create_bank_account_from_file_line(line):
        number, name, passwd, value, admin = line.split(';')[:-1]
        from cash_machine import BankAccount
        return BankAccount(number, name, passwd, float(value), ast.literal_eval(admin))

    @staticmethod
    def __skip_first_line(lines):
        return lines[1:len(lines)]


class BankAccountFileWriter(BankFile):

    def write_bank_account(self, account):
        line_index_to_update = BankAccountFileReader().get_line_index_of_bank_account(account.account_number)
        if line_index_to_update != -1:
            lines = self._read_lines()
            lines[line_index_to_update] = self.__format_line_to_write(account)
            self._write_lines(lines)

    @staticmethod
    def __format_line_to_write(account: cash_machine.BankAccount):
        return f"{account.account_number};{account.name};{account.passwd};{account.value};{str(account.admin)};\n"


class MoneySlipsFile(BankFile):
    MONEY_SLIPS_LINE = 0


class MoneySlipsFileReader(MoneySlipsFile):

    def __init__(self):
        super().__init__()
        self.__money_slips = {}

    def get_money_slips(self):
        self._file = self._open_file_bank('r')
        line_to_read = MoneySlipsFile.MONEY_SLIPS_LINE
        line = self._file.readlines(line_to_read)[0]
        for money_bill in line.split(';'):
            if money_bill != "\n":
                money_bill, amount = money_bill.split('=')
                self.__add_money_slips_from_file_line(money_bill, int(amount))
        return self.__money_slips

    def __add_money_slips_from_file_line(self, money_bill, amount):
        self.__money_slips[money_bill] = amount


class MoneySlipsFileWriter(MoneySlipsFile):

    def __init__(self):
        super().__init__()

    def write_money_slips(self, money_slips):
        lines = self._read_lines()
        line_to_write = MoneySlipsFile.MONEY_SLIPS_LINE
        lines[line_to_write] = self.__format_line_to_write(money_slips)
        self._write_lines(lines)

    @staticmethod
    def __format_line_to_write(money_slips):
        line = ""
        for key, value in money_slips.items():
            line += f"{key}={value};"
        return line + "\n"

