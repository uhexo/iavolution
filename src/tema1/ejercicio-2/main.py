
from datetime import date

from proceso import (
    recuperar_pedidos,
    reporte_pedido,
    subtitulo_periodo,
    reporte_pedidos_solicitados_por_pais,
)
from utilitarios import clear_screen, ingrensar_periodo, linea, verify_bash_shell




def menu() -> None:
    pedidos = recuperar_pedidos()
    periodo_inicio = date(2026, 1, 1)
    periodo_final = date(2026, 1, 31) 


    while True:
        clear_screen()
        periodo =  subtitulo_periodo( periodo_inicio, periodo_final )
        linea("=")
        print("        REPORTS MENU          ")
        linea("=")
        print("1. fijar periodo del reporte ")
        print("2. Reporte de volumen de pedidos por país del período")
        print("3. Reporte de pedidos del período")
        print("0. Exit")
        linea()
        print(f"Periodo Seleccionado: {periodo} ")
        linea("=")

        choice = input("Select an option [1-4]: ").strip()

        clear_screen()
        if choice == "1":
            periodo_inicio, periodo_final = ingrensar_periodo(periodo_inicio, periodo_final)
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
    menu()

if __name__ == "__main__":
    main()
