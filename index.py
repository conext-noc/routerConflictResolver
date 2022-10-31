import os
import re
from dotenv import load_dotenv
import paramiko
import time
from outputParser import decoder,outputParser
from parser import parser
load_dotenv()

condition = "Last down time          : "

username = os.environ["user"]
password = os.environ["pass"]
port = os.environ["port"]

# 7

condition = "---------------------------------------------------------------------------------------"

def main():
    delay = 1
    ROUTER = input("Seleccione El Router [AI | AV] : ")
    ip = "181.232.180.3" if (ROUTER == "AI") else ("181.232.180.4" if (ROUTER == "AV") else "NA")
    pool = "1" if ROUTER == "AI" else ("2" if (ROUTER == "AV") else "NA")
    lst = []
    conn = paramiko.SSHClient()
    conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    conn.connect(ip, port, username, password)
    comm = conn.invoke_shell()

    def enter():
        comm.send(" \n")
        comm.send(" \n")
        time.sleep(delay)

    def command(cmd):
        comm.send(cmd)
        time.sleep(delay)

    command("sys")
    enter()
    command(f"ip pool dhcp_server_residencial_{pool} server")
    enter()
    command("reset conflict-ip-address")
    enter()
    output = decoder(comm)
    command(f"display ip pool name dhcp_server_residencial_{pool} conflict decline | no-more")
    enter()
    (value, regex) = outputParser(comm,condition,"m")
    print(value,file=open("data.txt", "w"))
    (_,e) = regex[7]
    (s,_) = regex[8]
    data = re.sub(' +', ' ',value[e:s]).replace(" ", ",")
    print(data, file=open("data.txt", "w"))
    f = open("data.txt")
    lines = f.readlines()
    f.close()
    f = open("data.txt", 'w')
    for line in lines:
        f.write(line[1:])
    f.close()
    valueRES = open("data.txt", "r").read()
    os.remove("data.txt")
    header = """Index,IP,MAC,User-ID,Lease,Status1,Status2\n"""
    res = header + valueRES
    print(res, file=open("result.csv", "w"))
    resultado = parser("result.csv")
    os.remove("result.csv")
    for ipAdd in resultado:
        addss = ipAdd["IP"]
        command(f"reset conflict-ip-address {addss}")
        enter()
        print(f"Conflicto eliminado en la ip {addss}")



if (__name__ == "__main__"):
    main()
