import configparser
import os

config = configparser.ConfigParser()

config_path= "/etc/sync-sl/config.ini"

if not os.access(config_path, os.R_OK):
    raise SystemExit(
        "[X] Permission denied: Cannot read configuration.\n"
        "[!] Try running: sudo sync-sl"
    )
    
loaded_file = config.read(config_path)
if not loaded_file:
    raise SystemExit("Configuration file not found")

sections = config.sections() 
section_vars = ['server', 'user', 'ip', 'port', 'target_path', 'proxy_path']
allowed_servers = ('Forge', 'Certbot')

domains = {}

for section in sections :
    if section in ('Forge', 'Certbot', 'SSH'):
        continue
    server = config[section].get('server')
    domain_var = {}
    for var in section_vars:
        
        field = config[section].get(var)
        if field is None:
            # print(f"Missing Variable: {section}: {var}")
            field = "Missing"
        elif not field.strip() :
            if var == "password":
                field = ""
            else:
                field = "Empty"
       
        domain_var[var] = field

    domains[section] = domain_var

def config_ini():
    return domains

