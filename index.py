from outputParser import checkIter, decoder
from parser import dataToDict
from ssh import ssh
                          

condition = "---------------------------------------------------------------------------------------"
confHeader = "NA,ID,start,end,total,used,idle,conflict,disable,reserved,staticBind"
sectionHeader = "ip,mac,userId,lease,status,index,na"
sectionMapper = {
    "1":{"start":4,"end":5},
    "2":{"start":7,"end":8},
}

def main():
    ROUTER = input("Seleccione El Router [AI | AV] : ").upper()
    ip = "181.232.180.3" if (ROUTER == "AI") else ("181.232.180.4" if (ROUTER == "AV") else "NA")
    pool = "1" if ROUTER == "AI" else ("2" if (ROUTER == "AV") else "NA")
    (comm,command) = ssh(ip)
    sections = []
    ranges = []
    ipAddressess = []
    command("sys")
    command(f"ip pool dhcp_server_residencial_{pool} server")
    command(f"display ip pool name dhcp_server_residencial_{pool} conflict decline | no-more")
    value = decoder(comm)
    regex = checkIter(value,condition)
    (_,start) = regex[1]
    (end,_) = regex[2]
    summary = dataToDict(confHeader, value[start:end])
    for idx, section in enumerate(summary):
        if int(section["conflict"]) > 0:
            sections.append(sectionMapper[str(idx + 1)])
    for section in sections:
        (_,start) = regex[section["start"]]
        (end,_) = regex[section["end"]]
        data = dataToDict(sectionHeader, value[start:end])
        ranges.append(data)
    for rg in ranges:
        for ipAddStatus in rg:
            ipAddressess.append(ipAddStatus["ip"])
            
    for ip in ipAddressess:
        command(f"reset conflict-ip-address {ip}")
        print(f"Conflicto eliminado en la ip {ip}")



if (__name__ == "__main__"):
    main()
