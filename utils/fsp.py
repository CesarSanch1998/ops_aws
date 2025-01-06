def calcular(fsp: str):
    value_initial_port = 4194304000
    multipler_slot = 8192
    multiplier_puerto = 256

    f,s,p = fsp.split("/")

    snmp_port_cod = value_initial_port +(int(s) * multipler_slot ) + (int(p) * multiplier_puerto)
    return snmp_port_cod