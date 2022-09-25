# Telegram bot for server tasks

create `settings.py` in root of the project containing like sample below

```python
from decouple import config

configurations = {
    "ec2": {
        "server1": {
            "id": "i-067b12910920192801850",
            "access_key": config("SERVER1_ACCESS_KEY"),
            "secret_key": config("SERVER1_SECRET_KEY"),
            "region": "eu-west-1",
        },
        "server2": {
            "id": "i-067b12910kjwe2801850",
            "access_key": config("SERVER2_ACCESS_KEY"),
            "secret_key": config("SERVER2_SECRET_KEY"),
            "region": "eu-west-1",
        },
    }
}
```

add `.env` for the servers credentials

```.env
# telegram
TELEGRAM_TOKEN=""
TELEGRAM_CHAT_ID=""

# servers
SERVER1_ACCESS_KEY=""
SERVER1_SECRET_KEY=""

SERVER2_ACCESS_KEY=""
SERVER2_SECRET_KEY=""
```

----
install requirements

```bash
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```

run the script

```bash
python index.py
```
