
# Sync_SL

**Centralized SSL/TLS certificate synchronization using Python, SSH, and SFTP.**

Sync_SL is a lightweight Python CLI tool designed to simplify SSL/TLS certificate deployment across multiple Linux servers.

It connects to remote servers through SSH, retrieves certificate files using SFTP, and deploys them to a configured reverse proxy directory. The goal is to centralize certificate management and reduce the need for manual certificate transfers between servers.

## Features

- **SSH Connectivity** — Connect to remote Linux servers using Paramiko.
- **SFTP File Transfer** — Retrieve SSL/TLS certificate files securely over SSH.
- **Multiple Server Support** — Configure multiple remote servers and domains.
- **INI Configuration** — Manage server connections and certificate paths through a centralized configuration file.
- **Certificate Deployment** — Copy retrieved certificates to configured local directories.
- **File Permissions** — Apply appropriate permissions to certificate and private key files.
- **Error Handling** — Report individual server or domain failures without necessarily stopping the entire synchronization process.

## How It Works

Sync_SL runs on a central server, such as an AWS EC2 instance hosting a reverse proxy.

It connects to remote Linux servers where SSL/TLS certificates are stored, retrieves the required files, and deploys them to the reverse proxy's certificate directory.

```text
             Remote Linux Servers
          ┌────────────────────────┐
          │  Server A              │
          │  SSL Certificates      │
          └───────────┬────────────┘
                      │
                      │ SSH / SFTP
                      ▼
┌─────────────────────────────────────────┐
│              Sync_SL                    │
│                                         │
│  1. Read configuration                  │
│  2. Connect to remote servers           │
│  3. Retrieve certificate files         │
│  4. Deploy files to proxy directory     │
│  5. Report synchronization results     │
└─────────────────────┬───────────────────┘
                      │
                      ▼
             ┌──────────────────┐
             │  Reverse Proxy   │
             │  Nginx / HAProxy │
             │  SSL Certificates│
             └──────────────────┘
```

## Requirements

- Linux-based host
- Python 3
- SSH access to remote servers
- SSH key authentication
- SFTP support on remote servers

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/Sync_SL.git
cd Sync_SL
```

Run the installer:

```bash
sudo ./install.sh
```

The installer sets up the application, creates its Python virtual environment, installs dependencies, and installs the configuration directory.

## Configuration

The configuration file is located at:

```text
/etc/sync-sl/config.ini
```

Configure your SSH settings, server types, certificate filenames, remote paths, and local deployment paths.

Example structure:

```ini
[SSH]
location = /root/.ssh/id_ed25519
known_host = /root/.ssh/known_hosts

[Forge]
crt = server.crt
fullchain = server.key

[Certbot]
crt = privkey.pem
fullchain = fullchain.pem

[example.com]
server = Certbot
user = deploy
ip = 192.168.1.100
port = 22
target_path = /etc/letsencrypt/live/example.com
proxy_path = /etc/nginx/ssl/example.com
```

**Note:** The filenames and server settings above are examples. Adjust them to match your actual remote certificate layout and deployment environment.

Keep SSH private keys and other credentials outside the repository. Restrict access to the configuration file because it may contain infrastructure information.

## Usage

Run Sync_SL:

```bash
sudo sync-sl
```

The application reads the configuration, connects to the configured servers, and processes their certificate files.

## Uninstallation

Run the uninstall script:

```bash
sudo ./uninstall.sh
```

The uninstall process removes the application and launcher while preserving the configuration directory.

## Project Structure

```text
Sync_SL/
├── app.py
├── ini_parser.py
├── requirements.txt
├── install.sh
├── uninstall.sh
├── config.ini
├── README.md
└── .gitignore
```

## Roadmap

- [x] INI configuration parsing
- [x] SSH connectivity
- [x] Remote certificate file retrieval
- [x] Basic certificate deployment
- [x] File permission handling
- [ ] Certificate and private key validation
- [ ] Certificate expiration checks
- [ ] File integrity verification
- [ ] Atomic certificate deployment
- [ ] Reverse proxy configuration testing
- [ ] Automatic Nginx/HAProxy reload
- [ ] Logging and detailed execution reports
- [ ] Certbot deploy-hook integration

## Technologies

- **Python** — Application logic
- **Paramiko** — SSH and SFTP connectivity
- **ConfigParser** — INI configuration management
- **Linux** — Deployment environment
- **Nginx / HAProxy** — Reverse proxy targets

## Disclaimer

Sync_SL is a personal development project and is still under active development.

It is not yet intended for unattended production use. Review the configuration, SSH permissions, certificate deployment behavior, and failure handling before using it in a production environment.

## License

Choose a license before distributing the project. If you want others to use, modify, and redistribute it, consider the MIT License.
