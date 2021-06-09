# T800 #

T800 is a tool that create and manage multiple android devices and run:
* An API that can be used to interact with thoses devices via Frida or not.
* A UI to debug and manage each device individually

### Setup and run ###

Setup docker
```bash
cd t800_avd
./setup.sh
```
Run an instance of Android 11 SDK 30 in an x86 arch
```bash
ARCH=x86 API_V=30 BUILD_V=30.0.2 docker-compose up -d
```
Run the manager
```bash
cd t800_manager
python3 -m venv .env
source .env/bin/activate
pip install --upgrade
pip install -r requirements.txt
cd api
python3 api.py
```
Now you can go to the manager [http://127.0.0.1:4000/](http://127.0.0.1:4000/)
### Contribution guidelines ###

* branch -> PR -> QA -> boom

### Who do I talk to? ###

* Faradj
* Théo
* Aymen