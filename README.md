## Introduction
#### This repo is for game web app, now it only contains the connect four game, but feel free to add more games
apps - web app, 
blueprints - flask bp & response logic
configs - config files
game - enviroment for different games
model_data - file to store game data
services - main services
strategy - strategy file for games
tests - test tools
tools - tool functions
utils - util tool, (utilize tools)
manager.py main process

MVC - model, view, controller

## Start
1. need a server, GPU is perfered

2. build a new conda eniroment(optional)
```
conda create --name game_engine python==3.9
```

3. change the env path to local conda env in util __init__.py
```
ENV_PATH = ''
```

4. install requirements
```
pip setup.py develop
```

5. config files
```
connect_four_web_config.py 
```

6. start/ stop/ restart web server
```
manager connect_four start
manager connect_four stop
manager connect_four restart
```

view：
crontab -l
screen -ls


