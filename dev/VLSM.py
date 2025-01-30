from typing import overload


class IP:

    @overload
    def __init__(self, ip:list[int], mask: int) -> None:
        ...
    def __init__(self, ip:str, mask:int=32) -> None:
        if isinstance(ip, str):
            self.ip = [int(i) for i in ip.split('.')]
        else:
            self.ip = ip
        self.mask = mask

    def __str__(self) -> str : return '.'.join(map(str, self.ip)) + "/" + str(self.mask)

    def __add__(self, other: int) -> 'IP':

        temp = self.ip.copy()
        if temp[-1] + other <= 255:
            temp[-1] += other
        elif temp[-2] + other <= 255:
            temp[-2] += other
            temp[-1] = 0
        elif temp[-3] + other <= 255:
            temp[-3] += other
            temp[-2] = 0
            temp[-1] = 0
        elif temp[0] + other <= 255 :
            temp = [temp[0] + other, 0, 0, 0]
        else:
            raise ValueError("Invalid IP address")
        return IP(temp, self.mask)


table_adressage:dict[str:int] = {"KL": 28, "Perth": 60, "Sydney": 12, "Singapore": 12, "WAN1": 2, "WAN2": 2, "WAN3": 2}

def allouer_plages_ip(ip:IP, table_adressage:dict[str:int]) -> dict[str:list[IP]]:

    """

    A chaque itération : on cherche les valeurs les plus grandes pour allouer 2^x adresses

    """

    plan_addressage:list[str: str, str:IP, str:IP, str:list[IP]] = [{
        "network": "",
        "@net": 0,
        "@broadcast": 0,
        "@plage": 0
    } for _ in range(len(table_adressage))]

    counter:int = 0

    while table_adressage:
        max = list(table_adressage.keys())[0]
        for key, value in table_adressage.items():
            if value > table_adressage[max]:
                max = key
        
        i:int = len(str(bin(table_adressage[max])[2:]))
        ip.mask = 32 - i
        
        plan_addressage[counter] = {
            "network": max,
            "@net": str(ip),
            "@broadcast": str(ip + (2**i - 1)),
            "@plage": [str(ip), str(ip + (2**i - 2))]
        }
        ip += 2 ** i
        del table_adressage[max]
        counter += 1
    return plan_addressage

print(allouer_plages_ip(IP("1.2.3.4", 24), table_adressage))