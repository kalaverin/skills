---
---

# Security: Network

Talk only over encrypted transports: verify certificates, set timeouts, bind explicitly, avoid cleartext legacy protocols.

## Rule of thumb

1. Bind servers to a specific interface (`127.0.0.1` for local-only services); never hardcode `0.0.0.0`.
2. Set an explicit `timeout` on every `requests`/`httpx` call so stalled servers cannot hang the program.
3. Keep certificate and hostname verification on: rely on the default `verify=True` and build contexts with `ssl.create_default_context()`.
4. Allow-list URL schemes (`https://` only) before passing user-supplied URLs to `urlopen`.
5. Replace cleartext legacy protocols — Telnet, FTP, IPMI — with SSH, SFTP, and HTTPS management APIs.
6. Wrap sockets through a configured `SSLContext` pinned to TLS 1.2+; never call `ssl.wrap_socket` without a secure version.
7. Verify SSH host keys with `RejectPolicy` plus loaded system keys, and use SNMPv3 with both auth and privacy keys.

## Example: Monitoring agent

An internal agent polls upstream services and exposes a metrics socket, binding wide open and disabling TLS checks.

### Bad

```python
"""Poll upstreams and expose a metrics socket."""

import socket

import requests


def fetch_status(url: str) -> int:
    response = requests.get(url, verify=False)  # S113,S501
    return response.status_code


def serve_metrics(port: int) -> None:
    server = socket.socket()
    server.bind(("0.0.0.0", port))  # S104
    server.listen()
```

### Good

```python
"""Poll upstreams and expose a metrics socket."""

import socket

import requests

TIMEOUT = (3.05, 27)


def fetch_status(url: str) -> int:
    response = requests.get(url, timeout=TIMEOUT)
    return response.status_code


def serve_metrics(port: int) -> None:
    server = socket.socket()
    server.bind(("127.0.0.1", port))
    server.listen()
```

### Violations

1. **S104** — `server.bind(("0.0.0.0", port))`; binding to all interfaces exposes the service on untrusted networks.
2. **S113** — `requests.get(url, verify=False)`; the call has no `timeout` and may wait forever on a stalled server.
3. **S501** — `requests.get(url, verify=False)`; disabled certificate validation invites MITM attacks.

## Example: Config fetcher

A deployment tool downloads a config bundle with `urlopen`, taking any scheme and skipping certificate checks.

### Bad

```python
"""Download a config bundle."""

import ssl
from urllib.request import urlopen


def fetch_config(url: str) -> bytes:
    context = ssl._create_unverified_context()  # S323
    with urlopen(url, context=context) as response:  # S310
        return response.read()
```

### Good

```python
"""Download a config bundle."""

import ssl
from urllib.request import urlopen


def fetch_config(url: str) -> bytes:
    if not url.startswith("https://"):
        raise ValueError("only https URLs are allowed")
    context = ssl.create_default_context()
    with urlopen(url, context=context, timeout=30) as response:  # noqa: S310  # scheme restricted to https above
        return response.read()
```

### Violations

1. **S310** — `urlopen(url, context=context)`; unchecked input allows `file:` or custom schemes to read local resources.
2. **S323** — `ssl._create_unverified_context()`; the context skips certificate and hostname verification, enabling MITM.

## Example: Legacy device management

A datacenter script manages switches and BMCs over Telnet, FTP, and IPMI — all cleartext.

### Bad

```python
"""Manage legacy switches, file drops, and BMCs."""

import ftplib  # S402
import telnetlib  # S401

import pyghmi  # S415


def reboot_switch(host: str) -> None:
    session = telnetlib.Telnet(host)  # S312
    session.read_until(b"login: ")


def upload_firmware(host: str, path: str) -> None:
    ftp = ftplib.FTP(host)  # S321
    ftp.login()
    with open(path, "rb") as handle:
        ftp.storbinary(f"STOR {path}", handle)


def power_off(host: str) -> None:
    command = pyghmi.command.Command(bmc=host)
    command.set_power("off")
```

### Good

```python
"""Manage switches, file drops, and BMCs over encrypted protocols."""

import paramiko
import requests

TIMEOUT = (3.05, 27)


def _connect(host: str, username: str, key_path: str) -> paramiko.SSHClient:
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.RejectPolicy)
    client.connect(host, username=username, key_filename=key_path)
    return client


def reboot_switch(host: str, username: str, key_path: str) -> None:
    client = _connect(host, username, key_path)
    _, stdout, _ = client.exec_command("reboot")
    stdout.read()


def upload_firmware(host: str, path: str, username: str, key_path: str) -> None:
    client = _connect(host, username, key_path)
    with client.open_sftp() as sftp:
        sftp.put(path, f"/firmware/{path}")


def power_off(host: str, token: str) -> None:
    requests.post(
        f"https://{host}/redfish/v1/Systems/1/Actions/ComputerSystem.Reset",
        headers={"X-Auth-Token": token},
        json={"ResetType": "ForceOff"},
        timeout=TIMEOUT,
    )
```

### Violations

1. **S312** — `telnetlib.Telnet(host)`; Telnet sends credentials and session data in cleartext.
2. **S321** — `ftplib.FTP(host)`; FTP transfers credentials and files without encryption.
3. **S401** — `import telnetlib`; importing `telnetlib` signals use of an insecure cleartext protocol.
4. **S402** — `import ftplib`; importing `ftplib` implies an unencrypted file-transfer path.
5. **S415** — `import pyghmi`; IPMI modules are typically unencrypted and expose baseboard management.

## Example: TLS socket helper

An edge proxy wraps raw sockets with `ssl.wrap_socket`, defaulting to obsolete protocol versions.

### Bad

```python
"""TLS helpers for the edge proxy."""

import socket
import ssl


def open_tls(raw_sock: socket.socket, version=ssl.PROTOCOL_TLSv1):  # S503
    return ssl.wrap_socket(raw_sock, ssl_version=version)


def connect_upstream(host: str, port: int):
    raw_sock = socket.create_connection((host, port))
    return ssl.wrap_socket(raw_sock)  # S504


def connect_legacy(host: str, port: int):
    raw_sock = socket.create_connection((host, port))
    return ssl.wrap_socket(raw_sock, ssl_version=ssl.PROTOCOL_TLSv1)  # S502
```

### Good

```python
"""TLS helpers for the edge proxy."""

import socket
import ssl

CONTEXT = ssl.create_default_context()


def open_tls(raw_sock: socket.socket, server_hostname: str, context: ssl.SSLContext = CONTEXT):
    return context.wrap_socket(raw_sock, server_hostname=server_hostname)


def connect_upstream(host: str, port: int):
    raw_sock = socket.create_connection((host, port), timeout=30)
    return open_tls(raw_sock, host)
```

### Violations

1. **S502** — `ssl.wrap_socket(raw_sock, ssl_version=ssl.PROTOCOL_TLSv1)`; TLS 1.0 has known exploitable weaknesses.
2. **S503** — `def open_tls(..., version=ssl.PROTOCOL_TLSv1)`; a weak default propagates insecure TLS to every caller.
3. **S504** — `ssl.wrap_socket(raw_sock)`; without `ssl_version` the call permits insecure protocol versions.

## Example: Device health collector

A health collector SSHes into devices with auto-trusted host keys and polls SNMPv1/v2c or unencrypted SNMPv3.

### Bad

```python
"""Collect device health over SSH and SNMP."""

from paramiko import client
from pysnmp.hlapi import CommunityData, UsmUserData


def run_check(host: str) -> None:
    ssh = client.SSHClient()
    ssh.set_missing_host_key_policy(client.AutoAddPolicy)  # S507
    ssh.connect(host, username="admin")
    _, stdout, _ = ssh.exec_command("uptime")
    print(stdout.read())


def snmp_auth(mode: str):
    if mode == "v2":
        return CommunityData("public", mpModel=0)  # S508
    return UsmUserData("monitor")  # S509
```

### Good

```python
"""Collect device health over SSH and SNMP."""

from paramiko import client
from pysnmp.hlapi import UsmUserData


def run_check(host: str) -> None:
    ssh = client.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(client.RejectPolicy)
    ssh.connect(host, username="admin")
    _, stdout, _ = ssh.exec_command("uptime")
    print(stdout.read())


def snmp_auth(auth_key: str, priv_key: str):
    return UsmUserData("monitor", auth_key, priv_key)
```

### Violations

1. **S507** — `ssh.set_missing_host_key_policy(client.AutoAddPolicy)`; auto-trusting unknown host keys allows connecting to an impersonator.
2. **S508** — `CommunityData("public", mpModel=0)`; SNMPv1/v2c community strings travel in cleartext.
3. **S509** — `UsmUserData("monitor")`; SNMPv3 without auth and privacy keys leaves traffic unencrypted.
