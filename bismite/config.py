from dataclasses import dataclass
from os.path     import expanduser
from re          import compile as re_compile
from typing      import Dict, List, Optional, Pattern, Tuple

import yaml

@dataclass
class Config(object):
    server:   Tuple[str, int, bool]
    nickname: str
    username: str
    realname: str
    password: str
    channel:  str
    database: str

    sasl: Tuple[str, str]
    oper: Tuple[str, str, Optional[str]]

    bancmd:    str
    cliconnre: Pattern
    cliexitre: Pattern
    clinickre: Pattern
    antiidle:  bool

def load(filepath: str):
    with open(filepath) as file:
        config_yaml = yaml.safe_load(file.read())

    nickname = config_yaml["nickname"]

    server   = config_yaml["server"]
    hostname, port_s = server.split(":", 1)
    tls      = False

    if port_s.startswith("+"):
        tls    = True
        port_s = port_s.lstrip("+")
    port = int(port_s)

    oper_name = config_yaml["oper"]["name"]
    oper_pass = config_yaml["oper"]["pass"]
    oper_file: Optional[str] = None
    if "file" in config_yaml["oper"]:
        oper_file = expanduser(config_yaml["oper"]["file"])

    cliconnre = re_compile(config_yaml["cliconnre"])
    cliexitre = re_compile(config_yaml["cliexitre"])
    clinickre = re_compile(config_yaml["clinickre"])

    return Config(
        (hostname, port, tls),
        nickname,
        config_yaml.get("username", nickname),
        config_yaml.get("realname", nickname),
        config_yaml["password"],
        config_yaml["channel"],
        expanduser(config_yaml["database"]),
        (config_yaml["sasl"]["username"], config_yaml["sasl"]["password"]),
        (oper_name, oper_pass, oper_file),
        config_yaml["bancmd"],
        cliconnre,
        cliexitre,
        clinickre,
        config_yaml["antiidle"],
    )
