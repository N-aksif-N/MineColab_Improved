from shutil import rmtree
from os.path import exists, join
from os import makedirs
from time import sleep
from json import dump
from requests import get

path = 'content/drive'
drive_path = join(path, 'MyDrive/minecraft_server')

r = get('https://raw.githubusercontent.com/N-aksif-N/MineColab_Improved/app/streamlit-app/update.txt')
if 'update=True' in r.text or exists(join(path, 'MyDrive/streamlit-app')) == False:
  if exists(join(path, 'MyDrive/streamlit-app')):
    rmtree(join(path, 'MyDrive/streamlit-app'))
    sleep(5)
  dict = {'app.py':                    'https://raw.githubusercontent.com/N-aksif-N/MineColab_Improved/app/streamlit-app/app.py',
         'backends/settings.py':       'https://raw.githubusercontent.com/N-aksif-N/MineColab_Improved/app/streamlit-app/backends/settings.py',
         'frontends/choose_server.py': 'https://raw.githubusercontent.com/N-aksif-N/MineColab_Improved/app/streamlit-app/frontends/choose_server.py',
         'frontends/create_page_1.py': 'https://raw.githubusercontent.com/N-aksif-N/MineColab_Improved/app/streamlit-app/frontends/create_page_1.py',
         'frontends/login.py':         'https://raw.githubusercontent.com/N-aksif-N/MineColab_Improved/app/streamlit-app/frontends/login.py',
         'frontends/main_page.py':     'https://raw.githubusercontent.com/N-aksif-N/MineColab_Improved/app/streamlit-app/frontends/main_page.py'}
  makedirs(join(path, 'MyDrive/streamlit-app'))
  makedirs(join(path, 'MyDrive/streamlit-app/backends'))
  makedirs(join(path, 'MyDrive/streamlit-app/frontends'))
  sleep(10)
  for key in dict:
    with open(f'{path}/MyDrive/streamlit-app/{key}', 'w') as f:
      r = get(dict[key])
      f.write(r.text)
  dump({'choose': True, 'user': {'authtoken': ''}}, open(path + '/MyDrive/streamlit-app/user.txt', 'w'))
  # Creating minecraft_server folder
  sleep(10)
  if exists(drive_path) == False:
    makedirs(drive_path)
    makedirs(f'{drive_path}/logs')
  if exists(join(path, drive_path, 'serverconfig.txt')) == False:
    dump({"server_list": [], "ngrok_proxy" : {"authtoken" : '', "region" : ''}, "zrok_proxy": {"authtoken": ''}, "localtonet_proxy": {"authtoken": ''}}, open(drive_path + '/serverconfig.txt', 'w'))
sleep(20)
