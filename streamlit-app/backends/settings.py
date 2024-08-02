from requests import get
from time import sleep
from json import load, dump, loads
from os import environ, listdir, makedirs, getcwd, chdir, walk, remove
from os import system as call
from os.path import exists, isdir, join, isfile
from jproperties import Properties
from pyngrok import conf, ngrok
from bs4 import BeautifulSoup
from shutil import rmtree, move
from zipfile import ZipFile
from ruamel.yaml import YAML
import streamlit as st
from streamlit_ace import st_ace
yaml = YAML()
#------------------------------------------------------------------------------------------------------------------------------------#

path = '/content/drive'
drive_path = join(path, 'MyDrive/minecraft_server')
SERVERCONFIG = join(drive_path, 'serverconfig.txt')
USER = join(path, 'MyDrive/streamlit-app/user.txt')
if getcwd() != drive_path: chdir(drive_path)
def COLABCONFIG(server_name):
  return f"{drive_path}/{server_name}/colabconfig.txt"
# The jar file name
JAR_LIST_RUN = {'generic': 'server.jar', 'vanilla':'server.jar','snapshot': 'server.jar',   # NORMAL
          'purpur' : 'server.jar', 'paper': 'server.jar', 'velocity' : 'server.jar',  # PLUGINS
          'fabric' : 'server.jar', # forge doesn't include in this category           # MODS
          'arclight' : 'server.jar', 'mohist': 'server.jar', 'banner': 'server.jar'}  # HYBRID

#------------------------------------------------------------------------------------------------------------------------------------#

def COLABCONFIG_LOAD(server_name) -> dict:
  if exists(COLABCONFIG(server_name)): return load(open(COLABCONFIG(server_name)))
  else:
    ERROR('Please checking whether you deleted your colabconfig file or not.')
    return {'server_type': False}
    
def starting(server_name):
  if st.session_state.Starting[server_name][1] == True:
    st.session_state.Starting[server_name] = ['Start', False]
  else:
    st.session_state.Starting[server_name] = ['Stop', True]
    
@st.cache_data
def booleen(str):
  if str == 'true':
    return True
  elif str == 'false':
    return False
    
def ONLINE(server_name, player = False, status= False):
  if player:
    return 0
  if status:
    if st.session_state['Starting'][server_name][1]:
      return 'Online'
    else:
      return 'Offline'

def LOG(*args, icon = ''):
  args_ = []
  for arg in args:
   if '\n' in arg: args_.extend(str(arg).split('\n'))
   elif args_ != []: args_[-1] = args_[-1] + ' ' + str(arg)
   else: args_.append(str(arg))
  args_[0] = '[ :green[LOG] ] ' + args_[0]
  for i in args_:
    if icon != '': st.toast(i, icon = icon)
    else: st.toast(i, icon = 'ℹ️')

def ERROR(*args, icon = '🚨'):
  args_ = []
  for arg in args:
   if '\n' in arg: args_.extend(str(arg).split('\n'))
   elif args_ != []: args_[-1] = args_[-1] + ' ' + str(arg)
   else: args_.append(str(arg))
  args_[0] = '[ :red[ERROR] ] ' + args_[0]
  for i in args_: st.toast(i, icon = icon)

def MKDIR(path: str):

  ''' Creating a directory with the given path
  
  packages: os        |    os.path
  method: makedirs    |    exists
  
  '''

  if exists(path): pass
  else:
    try:
      LOG(f'Creating {path}')
      makedirs(path, exist_ok = True)
    except: ERROR(f'Can not creating {path}')

@st.cache_data
def GET(url: str):
  ''' Getting data from given url
  
  packages: requests
  method: get 

  '''

  r = get(url)
  # Check gate
  if r.status_code == 200:
    return r
  else: ERROR('Error '+ str(r.status_code) + "! Most likely you entered an unsupported version. Try running the code again if you think that shouldn't have happened.")

def DOWNLOAD_FILE(content, url: str, path: str, file_name: str):
  ''' Downloading file
 
  packages: os.path     
  method: exists, GET, ERROR
  
  '''

  # Check gate
  if exists(path+ '/' + file_name): ERROR(f'File {file_name} already existed.')
  else:
    # Download file into file_name thourgh url
    if url != '':
      r = GET(url)
      r = r.content
    else: r = content
    with open(path + '/' + file_name, 'wb') as f:
      f.write(r)

def PROGRESS():
  # '''Fancy looking progress bar

  # packages: streamlit
  # method: progress
  
  # '''

  progress = st.progress(0, text=' Completing...')
  for percent_complete in range(100):
    if percent_complete == 50: time = 0.04
    elif percent_complete == 75: time = 0.02
    else: time = 0.05
    sleep(time)
    progress.progress(percent_complete + 1, text=' Completing...')
  sleep(1)
  progress.empty()
  LOG('Completed', icon= '✅')

@st.fragment
def SET_SERVERCONFIG(tunnel_service, server_name):
  # Settings serverconfig

  # packages: streamlit     | json
  # methods: text_input     | load, dump
  
  LOG('Configuring serverconfig.txt and colabconfig.txt')
  serverconfig = load(open(SERVERCONFIG))
  serverconfig['server_list'] += [server_name]
  if serverconfig['ngrok_proxy'] == {"authtoken": "", "region": ""} and tunnel_service == 'ngrok':
    st.info('Get your authtoken from https://dashboard.ngrok.com/get-started/your-authtoken')
    st.text_input('Your authtoken: ', key= 'authtoken')
    st.selectbox('Region: ', ('ap', 'au', 'eu', 'in', 'jp', 'sa', 'us'), index=None, key = 'region')
    if st.session_state['authtoken'] != '' and st.session_state['region'] != None:
      serverconfig['ngrok_proxy']['authtoken'] = st.session_state['authtoken']
      serverconfig['ngrok_proxy']['region'] = st.session_state['region']
  elif tunnel_service == 'zrok' and serverconfig['zrok_proxy'] == {'authtoken': ''}:
    st.text_input('Your zrok token: ', key='authtoken')
    if st.session_state['authtoken'] != '':
      serverconfig['zrok_proxy']['authtoken'] = st.session_state['authtoken']
  elif tunnel_service == 'localtonet' and serverconfig['localtonet_proxy'] == {'authtoken': ''}:
    LOG('Get your authtoken from https://localtonet.com/usertoken')
    st.text_input('Your localtonet token: ', value= '', key='authtoken')
    if st.session_state['authtoken'] != '':
      serverconfig['localtonet_proxy']['authtoken'] = st.session_state['authtoken']
  dump(serverconfig, open(SERVERCONFIG, 'w'))

def SERVERSJAR(server_type, version, all = False, jar = False):
  '''Get the download URL (jar) AND return the detailed versions for each software (all)

  packages: requests  | BeautifulSoup
  method: GET         | html.parser
  
  '''
  
  if all:
    Server_Jars_All = {
      'paper': 'https://api.papermc.io/v2/projects/paper', 'velocity': 'https://api.papermc.io/v2/projects/velocity',
      'purpur': 'https://api.purpurmc.org/v2/purpur',
      'mohist': 'https://mohistmc.com/api/v2/projects/mohist', 'banner': 'https://mohistmc.com/api/v2/projects/banner'
    }
    if server_type == 'vanilla' or server_type=='snapshot':
      rJSON = GET('https://launchermeta.mojang.com/mc/game/version_manifest.json').json()
      if server_type == 'vanilla': server_type = 'release'
      if version != 'vanilla - latest_version': server_version = [hit["id"] for hit in rJSON["versions"] if hit["type"] == server_type]
      else: return rJSON['latest']['release']
    elif server_type == 'paper' or  server_type == 'velocity' or server_type == 'purpur' or server_type == 'mohist' or server_type == 'banner':
      rJSON = GET(Server_Jars_All[server_type]).json()
      server_version = [hit for hit in rJSON["versions"]]
    elif server_type == 'fabric':
      rJSON = GET('https://meta.fabricmc.net/v2/versions/game').json()
      server_version = [hit['version'] for hit in rJSON if hit['stable'] == True]
    elif server_type == 'forge':
      rJSON = GET('https://files.minecraftforge.net/net/minecraftforge/forge/index.html')
      soup = BeautifulSoup(rJSON.content, "html.parser")
      server_version = [tag.text for tag in soup.find_all('a') if '.' in tag.text and '\n' not in tag.text]
    else:
      LOG('Before going deeper, please check out https://github.com/IzzelAliz/Arclight')
      rJSON = GET('https://files.hypoglycemia.icu/v1/files/arclight/minecraft').json()['files']
      server_version  = [hit['name'] for hit in rJSON]
    return server_version
    
  elif jar == True and version != None:
    # RETURN DOWNLOAD URL
    if server_type == 'vanilla' or server_type=='snapshot':
      rJSON = GET('https://launchermeta.mojang.com/mc/game/version_manifest.json').json()
      if server_type == 'vanilla': server_type = 'release'
      for hit in rJSON["versions"]:
        if hit["type"] == server_type and hit['id'] == version: return GET(hit['url']).json()["downloads"]['server']['url']
    elif server_type == 'paper' or  server_type == 'velocity':
       build = GET(f'https://api.papermc.io/v2/projects/{server_type}/versions/{version}').json()["builds"][-1]
       jar_name = GET(f'https://api.papermc.io/v2/projects/{server_type}/versions/{version}/builds/{build}').json()["downloads"]["application"]["name"]
       return f'https://api.papermc.io/v2/projects/{server_type}/versions/{version}/builds/{build}/downloads/{jar_name}'
    elif server_type == 'purpur':
       build = GET(f'https://api.purpurmc.org/v2/purpur/{version}').json()["builds"]["latest"]
       return f'https://api.purpurmc.org/v2/purpur/{version}/{build}/download'
    elif server_type == 'mohist' or server_type == 'banner':
       return GET(f'https://mohistmc.com/api/v2/projects/{server_type}/{version}/builds').json()["builds"][-1]["url"]
    elif server_type == 'fabric':
       installerVersion = GET('https://meta.fabricmc.net/v2/versions/installer').json()[0]["version"]
       fabricVersion = GET(f'https://meta.fabricmc.net/v2/versions/loader/{version}').json()[0]["loader"]["version"]
       return "https://meta.fabricmc.net/v2/versions/loader/" + version + "/" + fabricVersion + "/" + installerVersion + "/server/jar"
    elif server_type == 'forge':
       rJSON = GET(f'https://files.minecraftforge.net/net/minecraftforge/forge/index_{version}.html')
       soup = BeautifulSoup(rJSON.content, "html.parser")
       tag =  soup.find('a', title="Installer"); tag = str(tag); tag = tag[tag.find('"') + 1 :]
       link = tag[:tag.find('"')]; link = link[link.find('=') + 1:]; link = link[link.find('=') + 1:]
       return link
    else:
      rJSON = GET(f'https://files.hypoglycemia.icu/v1/files/arclight/minecraft/{version}/loaders').json()
      list_build = [hit['name'] for hit in rJSON['files']]
      st.selectbox(' Type? ', tuple(list_build), key='build', index=None)
      st.selectbox('Stable(st) or Snapshot(sn)? ', ('stable', 'snapshot'), key='choice', index=None)
      if st.session_state['build'] != None and st.session_state['choice']:
        build = st.session_state['build']
        if 'sn' in str(st.session_state['choice']).lower(): choice = 'latest-snapshot';
        else: choice = "latest-stable";
        f'https://files.hypoglycemia.icu/v1/files/arclight/minecraft/{version}/loaders/{build}/{choice}'
  else: ERROR('Wrong given arguments')

#--------------------------------------------------------------------------------------------------------------------------------#

def Install_server(server_name, server_type, version, tunnel_service):
  # Create folder
  LOG(f'Creating {drive_path}/{server_name}')
  MKDIR(f'{drive_path}/{server_name}')
  sleep(10)

  # For developer: PLEASE USE SET_SERVERCONFIG() to set the serverconfig before using THIS function!
  
  # Get version
  if version == 'vanilla - latest_version': version = SERVERSJAR(server_type, version, all = True)
  else: version = version
  # Set up colabconfig
  colabconfig = {"server_type": server_type, "server_version": version, "tunnel_service" : tunnel_service}
  dump(colabconfig, open(COLABCONFIG(server_name),'w'))
  # Download jar file
  LOG('Found URL. Downloading server.jar ...')
  if server_type == 'forge': jarname = 'forge-installer.jar' # The jar file name (forge need a special process)
  else: jarname = JAR_LIST_RUN[server_type]
  DOWNLOAD_FILE(content='', url= SERVERSJAR(server_type, version, jar = True), path = f"{drive_path}/{server_name}", file_name= jarname)
  sleep(10)

def Delete_server(server_name, software= False):
  LOG(f'Found server {server_name}')
  sleep(10)
  # Remove the folder name in server config txt files
  LOG('Configuring serverconfig.txt')
  serverconfig = load(open(SERVERCONFIG));
  serverconfig['server_list'].remove(server_name)
  dump(serverconfig, open(SERVERCONFIG, 'w'))
  sleep(10)
  # Delete folder without noticable
  if software:
    drive_dir = listdir(f'{drive_path}/{server_name}')
    if exists(f'{drive_path}/{server_name}/tunnels'): drive_dir.remove('tunnels')
    for i in drive_dir:
      if isdir(f'{drive_path}/{server_name}/{i}'):
        rmtree(f'{drive_path}/{server_name}/{i}')
        sleep(5)
      elif isfile(f'{drive_path}/{server_name}/{i}'):
        remove(f'{drive_path}/{server_name}/{i}')
        sleep(10)
  else:
    rmtree(f'{drive_path}/{server_name}')
    sleep(10)
  LOG(f'Deleting {server_name}...')
  sleep(10)

def Server_Properties(server_properties, server_name, Slots, Gamemode, Difficulty, Cracked, PVP, Command_block, Fly, Villagers, Animals, Monsters, Whitelist, Nether, Force_gamemode, Spawn_protection, Resource_pack_required, Resource_pack, Resource_pack_prompt):
  LOG('Changing server.properties')
  if 'https' not in Resource_pack or 'http' not in Resource_pack: ERROR('Please give the right http link for resource_pack')
  else: server_properties['resource-pack'] = Resource_pack
  server_properties['resource-pack-prompt'] = Resource_pack_prompt
  # Configuring
  server_properties["max-players"] = str(Slots)
  server_properties['spawn-protection'] = str(Spawn_protection)
  server_properties["gamemode"] = Gamemode
  server_properties["difficulty"] = Difficulty
  dict_ = {'pvp': PVP, 'enable-command-block': Command_block, 'allow-flight': Fly, 'spawn-animals': Animals, 'spawn-monsters': Monsters, 'white-list': Whitelist,
          'spawn-npcs': Villagers, 'allow-nether': Nether, 'force-gamemode': Force_gamemode, "online-mode" : Cracked, 'require-resource-pack': Resource_pack_required}
  for keys, value in dict_.items(): server_properties[keys] = str(value).lower()
  # Saving
  with open(f"{drive_path}/{server_name}/server.properties", "wb") as f:
    server_properties.store(f, encoding="utf-8")
  PROGRESS()

def MAP(server_name, seed_map, world_list, world, content, file_name):
  if seed_map != '':
    sleep(5)
    LOG('Configuring server.properties')
    server_properties = Properties()
    with open(f"{drive_path}/{server_name}/server.properties", "wb") as f:
      server_properties.load(f, 'utf-8')
    server_properties['level-seed'] = seed_map
    with open(f"{drive_path}/{server_name}/server.properties", "wb") as f:
      server_properties.store(f, encoding="utf-8")
    sleep(5)
    LOG('Deleting world folders...')
    for i in world_list:
      rmtree(f"{drive_path}/{server_name}/{i}")
      sleep(5)
    PROGRESS()
  else:
    LOG('Downloading')
    DOWNLOAD_FILE(content = content, url = '', path = f'{drive_path}/{server_name}', file_name = file_name)
    sleep(5)
    with ZipFile(f"{drive_path}/{server_name}/{file_name}") as zip:
      zip.extractall(drive_path)
      inside_file = [i.split('/') for i in zip.namelist() if '/' in i]
      key = inside_file[0][0]
      inside_file = [i.split('/') for i in zip.namelist() if key in i]
      for i in inside_file:
        i.remove(key)
    MKDIR(f"{drive_path}/{server_name}/{world}")
    LOG('Moving files to world folder')
    move(f"{drive_path}/{server_name}/{key}", f"{drive_path}/{server_name}/{world}")
    sleep(5)
    server_properties = Properties()
    with open(f"{drive_path}/{server_name}/server.properties", "wb") as f:
      server_properties.load(f, 'utf-8')
    server_properties['level-name'] = key
    with open(f"{drive_path}/{server_name}/server.properties", "wb") as f:
      server_properties.store(f, encoding="utf-8")
    sleep(5)
    PROGRESS()

def Backup(server_name ='', file_name ='', server_backup ='', file_backup =''):
  # file_name = input('File name'); file_backup = input('File back up name: ')
  def zip_directory(folder_path, zip_file):
    for folder_name, subfolders, filenames in walk(folder_path):
        for filename in filenames:
            # Create complete filepath of file in directory
            file_path = join(folder_name, filename)
            # Add file to zip
            zip_file.write(file_path)

  # Settings path
  if file_name != '':
    path1 = f'{server_name}/' + file_name
    if server_backup != '':
      if exists(f'{drive_path}/{server_backup}') == False:
        MKDIR(f'{drive_path}/{server_backup}')
        sleep(40)
    if file_backup != '' and server_backup != '': path2 = f'{server_backup}/' + file_backup
    elif file_backup != '' and server_backup == '': path2 = f'{server_name}/' + file_backup
    elif file_backup == '' and server_backup != '':  path2 = f'{server_backup}/' + '-back-up-file'
    else: path2 = server_name + '-back-up-file'
  else:
    path1 = server_name
    if server_backup != '': path2 = server_backup
    else: path2 = server_name + '-back-up-world'
  # Checking and zipping
  #if exists(path1) == False: ERROR(' Creating your minecraft server before backing up files')
  if exists(path2) == True: ERROR(' Back up path exists')
  # Zipping
  LOG('Zipping files')
  zip_file = ZipFile(f'{path2}.zip', 'w')
  zip_directory(path1, zip_file)
  # Download
  container = st.empty()
  with container.container():
    with open(f'{path2}.zip', "rb") as fp:
      if st.download_button( label="Download ZIP", data=fp, file_name=f'{path2}.zip', mime="application/zip"):
        sleep(10)
        container.empty()
