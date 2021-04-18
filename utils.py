import os


def header(width: int = 40) -> None:
    print("".center(width, "*"))
    print(" School of Net - Caixa Eletrônico ".center(width, "*"))
    print("".center(width, "*"))


def clear_screen() -> None:
    os.system("cls" if os.name == 'nt' else "clear")  # clear screen


def pause() -> None:
    input("Pressione <ENTER> para continuar...")  # pause
