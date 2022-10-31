import os
from dotenv import load_dotenv
import chardet
from datetime import datetime
import paramiko
import time
import re
from parser import parser, converter


def main():
    final = []
    OLT = input("Seleccione la OLT [15 | 2] : ")
    lst = parser(
        "CLIENTES DESACTIVADOS - Hoja 1.csv") if OLT == "15" else parser("DESACTIVADOS X2 - Hoja 1.csv")
    resultlst = parser("CLIENTES CON MAS  DE 2 MESES DESACTIVADOS - OLT X15 10-2022.csv") if OLT == "15" else parser(
        "CLIENTES CON MAS  DE 2 MESES DESACTIVADOS - OLT X2 10-2022.csv")
    for client in lst:
        for resultClient in resultlst:
            if (client["F"] == resultClient["F"] and client["S"] == resultClient["S"] and client["P"] == resultClient["P"] and client["ID"] == resultClient["ID"]):
                FRAME = client["F"]
                SLOT = client["S"]
                PORT = client["P"]
                ID = client["ID"]
                NAME = client["NAME"]
                TIME = resultClient["TIME"]
                SN = client["SERIAL"]
                final.append({"NAME": NAME, "F": FRAME, "S": SLOT,
                             "P": PORT, "ID": ID, "TIME": TIME, "SN": SN})
    converter(final, f"{OLT}")


if (__name__ == "__main__"):
    main()
