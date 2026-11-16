#!/usr/bin/env python3
import sys
from utilitarios import  *







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

    pedidos = recuperar_pedidos()
    periodo_inicio = date(2026, 1, 1)
    periodo_final = date(2026, 1, 31)

    menu()

if __name__ == "__main__":
    main()
