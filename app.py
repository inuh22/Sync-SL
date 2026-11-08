import os
import subprocess
import paramiko
import shutil
from pathlib import Path
from configparser import ConfigParser
from ini_parser import config_ini

print("Effective UID:", os.geteuid())
config = ConfigParser()

config_path= "/etc/sync-sl/config.ini"
loaded_file = config.read(config_path)

if not os.access(config_path, os.R_OK):
    raise SystemExit(
        "[X] Permission denied: Cannot read configuration.\n"
        "[!] Try running: sudo sync-sl"
    )

if not loaded_file:
    raise SystemExit("Configuration file not found")

ssh_key = config["SSH"]["location"]
server_vars =  ['fullchain', 'crt']

domains = config_ini()

for domain in domains:

    client = paramiko.SSHClient()
    client.load_system_host_keys(filename=config["SSH"]['known_host'])
    client.set_missing_host_key_policy(paramiko.RejectPolicy())
    try: 
        client.connect(
            hostname = domains[domain]["ip"], 
            port = int(domains[domain]["port"]), 
            username = domains[domain]["user"], 
            key_filename= ssh_key 
        )
        sftp = client.open_sftp()
        print(f"-----------------------------\n[/] Connected to {domain}")
        server_type =  domains[domain]['server']

        if server_type not in ['Forge', 'Certbot']:

            print(f'[X] Invalid Server Type Skipping: {domain} > server: {domains[domain]['server']}')
            continue

        for file in server_vars:
            ssl_file = config[server_type][file]
            try:
                target_file = f"{domains[domain]['target_path']}/{ssl_file}"
                proxy_path = Path(domains[domain]["proxy_path"])
                proxy_path_file = f'{domains[domain]["proxy_path"]}/{ssl_file}'
                file_check =  sftp.stat(target_file)
                local_file = f"/tmp/{config[server_type][file]}"
                print(f'{domain} > File: {config[server_type][file]} exist')     
                try:         
                    print(f'Copying {ssl_file} to local /tmp')
                    sftp.get(
                        target_file, 
                        f"/tmp/{ssl_file}"
                    )

                    if file  == server_vars[1]:
                        result = subprocess.run(
                            ["openssl", "x509", "-in", ssl_file, "-noout", "-checkhost", domain],
                            cwd="/tmp",
                            capture_output=True,
                            text=True,
                        )
                        if result.returncode != 0:
                            print(f"[X] Certificate validation failed: {domain}")
                            continue
                        dom_check = result.stdout.strip()
                        if dom_check == f"Hostname {domain} does NOT match certificate":
                            print(f"[X] Skipping {dom_check}")
                            continue

                    print(f"Making Directory: {proxy_path}/")
                    proxy_path.mkdir(parents=True, exist_ok=True)
                    
                    if os.path.exists(local_file):
                        shutil.copy(local_file, proxy_path_file)
                        if file == server_vars[0]:
                            os.chmod(proxy_path_file, 0o644)
                        else:
                            os.chmod(proxy_path_file, 0o600)
                        print(f'Removing: {domain} > {local_file}')
                        os.remove(local_file)

                except (paramiko.SFTPError,OSError) as error:
                    print(f'[X] Skipping: {domain} > {error}')

            except (paramiko.SFTPError, OSError) as p_error:
                print(f"Skipping {domain} > {config[server_type][file]}: {p_error}")      

    except (paramiko.SSHException, OSError, ValueError) as error:
        print(f"Connection failed for {domain}: {error}")
    finally:
        client.close()
    
