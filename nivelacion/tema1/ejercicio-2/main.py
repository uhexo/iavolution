#!/usr/bin/env python3
import os
import subprocess
import sys
from ejercicio_2 import  *


def verify_bash_shell() -> None:
    """
        Valida que este script de python solo puede ser ejecutado bash shell.¡
    """
    try:
        ppid = os.getppid()
        # Query the parent process command name (works on macOS and Linux)
        result = subprocess.run(
            ["ps", "-p", str(ppid), "-o", "comm="],
            capture_output=True,
            text=True,
            check=True,
        )
        parent_comm = os.path.basename(result.stdout.strip())
        # Remove leading '-' in case it is a login shell (e.g., '-bash')
        if parent_comm.lstrip("-") != "bash":
            print(
                f"Error: This script must be run directly from bash "
                f"(detected parent process: '{parent_comm}').",
                file=sys.stderr,
            )
            sys.exit(1)

    except Exception as exc:
        print(f"Error verifying parent shell: {exc}", file=sys.stderr)
        sys.exit(1)


def clear_screen() -> None:
    """Clears the terminal screen using the standard POSIX clear command."""
    os.system("clear")


def reporte_none() -> None:
    print("\n--- Executing Report 1 ---")
    # Add your report 1 logic here


def menu() -> None:

    while True:
        clear_screen()
        print("==============================")
        print("        REPORTS MENU          ")
        print("==============================")
        print("1. fijar periodo del reporte")
        print("2. Reporte de volumen de pedidos por país del período")
        print("3. Reporte de pedidos del período")
        print("0. Exit")
        print("==============================")

        choice = input("Select an option [1-4]: ").strip()

        if choice == "1":
            periodo_inicio,periodo_final = ingrensar_periodo(periodo_inicio, periodo_final)
        elif choice == "2":
            reporte_pedidos_solicitados_por_pais(pedidos, periodo_inicio, periodo_final )
        elif choice == "3":
            reporte_pedido(pedidos, periodo_inicio, periodo_final )
        elif choice == "0":
            print("Exiting...")
            break
        else:
            print(f"\nOpción invalida '{choice}'. Elija una correcta.")

        input("\nPress Enter to return to the menu...")


def main() -> None:
    """
    Programa principal  
    """

    verify_bash_shell() 

    pedidos = recuperar_pedidos("pedidos.json")

    periodo_inicio = date(2026, 1, 1)
    periodo_final = date(2026, 1, 31)

    menu()

if __name__ == "__main__":
    file_path = Path(__file__).parent.resolve() / "pedidos.json"
    pedidos = leer_pedidos( file_path )
    reportar_invalidos(pedidos)

    #main()
