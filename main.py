from console import CashMachineConsole
from console import AuthBankAccountConsole
from utils import clear_screen, header, pause


def main():
    clear_screen()
    header()
    if AuthBankAccountConsole.is_auth():
        clear_screen()
        header()
        CashMachineConsole.call_operation()
    else:
        print('Conta inválida')


if __name__ == "__main__":
    while True:
        main()
        pause()
