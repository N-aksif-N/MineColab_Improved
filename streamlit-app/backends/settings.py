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
    st.session_state.Starting[server_name] = ['▶ Start', False]
  else:
    st.session_state.Starting[server_name] = ['🛑 Stop', True]
    
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

def BUTTON(*args, key=None, **kwargs):  
    if key is None:
        raise ValueError("Must pass key")

    if key not in st.session_state:
        st.session_state[key] = False

    if "type" not in kwargs: kwargs["type"] = "primary" if st.session_state[key] else "secondary"
    if st.button(*args, **kwargs):
        st.session_state[key] = not st.session_state[key]
        st.rerun()
    return st.session_state[key]

def MKDIR(path: str):

  ''' Creating a directory with the given path
  
  packages: os        |    os.path
  method: makedirs    |    exists
  
  '''

  if exists(path): pass
  else:
    try: makedirs(path, exist_ok = True)
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

def Delete_server(server_name, software= False, reserve=[]):
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
    drive_dir = listdir(f'{drive_path}/{server_name}'); reserve.append('tunnels')
    for i in reserve:
      if exists(f'{drive_path}/{server_name}/{i}'): drive_dir.remove(i)
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

@st.fragment
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

@st.cache_data
def LOGS(server_name: str):
  with open(f'{drive_path}/{server_name}/logs/latest.log', 'r') as f:
    LOG('Try access to https://mclo.gs to see problems and the way to deal with.');
    content_ = f.read(); 
    return content_

@st.cache_data
def GITHUB_GUIDE(choice):
  text = ''
  if choice == 'What is Mine Colab [Improved]':
    text = ''' 
    # :hear_no_evil:  First of all, what is Mine Colab [Improved]?

    Mine Colab [Improved] is an alternative [Minecolab project](https://github.com/thecoder-001/MineColab) that helps to build a Minecraft server on your own Gdrive. It is easier to use and more flexible to edit. This project is suited for mainly [google colab](https://colab.research.google.com) (a free service based on [jupyter notebook](https://jupyter.org/) and [ubuntu](https://ubuntu.com) os), though this can be applied on other projects like [jupyter lab](https://jupyter.org/try-jupyter/lab/), [deepnote](https://deepnote.com/), etc. This project followed the [GNU License](https://github.com/N-aksif-N/Minecolab/blob/master/LICENSE). Before looking closer, please make sure to see [the original](https://github.com/thecoder-001/MineColab)'''
  elif choice == 'Can Minecolab server online 24/7 ?':
    text = ''' 
    # :moneybag:  Can Minecolab server online 24/7?

    Of course, it's possible but with a little hard work. Google Colab is a free service and it is not suited for 24/7 online so you can use [deepnote](https://deepnote.com/) instead. Or if you still want to use google collab you may need some tricks or friends to make the web online and accept the captcha manually.'''
  elif choice == 'Instructions':
    text = ''' # :page_with_curl: Instructions
      - Open the notebook in Google Colab.
      - RUN THE SET-UP CELL (important)
      - Read through the notebook, most of the code is self-explanatory. Run the cells that are useful for your use case.

      **Create Minecraft server**
      1. Run the cell that creates the Minecraft server.
      2. After that, you have five options. You can either use Ngrok, PlayIt, or Cloudflare's Argo. Ngrok, Localtonet is easy to set up and doesn't require anything to be installed by the clients but it can often be quite unreliable. Argo doesn't have such limitations but requires a bit more work. Playit, Zrok may get bugged at this point but it is more reliable and does not require any hard work.

      - **[Ngrok](https://ngrok.com)**
        + Follow the prompts.
        + The IP will change whenever you restart the server.
      - **[Cloudflare's argo](https://www.cloudflare.com/)** :
          - If the 'Your free tunnel has started!' notification appears => Done.
          - Access to your server:
          1. Download [Cloudflared client](https://github.com/cloudflare/cloudflared/releases/).
          2. Launch the binary with `<your Cloudflare file name> access tcp --hostname <tunnel_address> --url 127.0.0.1:25565` (note: tunnel_address is your address which has been set on your Cloudflare).
          4. Finally, connect to `127.0.0.1:25565` from the minecraft client which is located in that machine.

      - **[Localtonet](https://localtonet.com/)**:

        1. Navigate to [TCP-UDG](https://localtonet.com/tunnel/tcpudp) page. Select TCP in Protocol Types.
        2. Get your authtoken from [Authtoken](https://localtonet.com/usertoken).
        3. Pick the server you'd like your tunnel to operate on.
        4. Input the IP and Port values the tunnel will listen to, in this case, for Minecraft, it's typically IP: 127.0.0.1 and Port: 25565.
        5. Finally, create and start your tunnel by pressing the Start button.

        - Read more on [how-to-use-localtonet-with-minecraft](https://localtonet.com/documents/using-localtonet-with-minecraft)

      - **[Zrok](https://zrok.io/)**:
        1. Download the zrok app through [link](https://docs.zrok.io/docs/getting-started/)
        2. Open the shell. Type `zrok invite` to sign up and get the authtoken
        3. Follow the prompts

      - **[PlayIt](https://playit.gg/)**: follow the prompts.
      
      ### If you wanna to read more then join our discord: [Minecolab Support](https://discord.gg/uCHcV3SAbs)'''
  elif choice == 'How does it actually work ?':
    text = ''' # :zap:  So, how does it actually work?
        MInecolab [Improved] is an alternative Minecolab project. Therefore, it has all the main features, which the Minecolab project does:

        1. Update the system's apt-cache.
        2. Install Openjdk-8 (For Minecraft versions below 1.17) or Openjdk-17 (For Minecraft versions over or in 1.17) through apt-get.
        3. Mount Google Drive to access the Minecraft folder (Drive is used here to provide persistent storage).
        4. Setup Argo/ngrok/playit Tunnel (Opening a tunnel at port 25565) depending on the `tunnel_service` variable.
        5. Change the directory to the Minecraft server folder on Google Drive ("Minecraft-server" is the default, located in the root directory of your Google Drive.)
        6. List/Print the file list on the screen to indicate successful directory change.
        7. Startup the Minecraft server (with optimized JVM parameters from [Aikar's guide)](https://aikar.co/2018/07/02/tuning-the-jvm-g1gc-garbage-collector-flags-for-minecraft/) and from GC logging

        Additionally, Minecolab [Improved] has more new features:

        1. Bug Fixes: Mine Colab [Improved] addresses issues like Java errors, connection disruptions, and missing files, ensuring a smoother experience.
        2. Performance Improvements: The project has been optimized for better performance, making it more efficient.
        3. Mod and Plugin Support: You can now easily integrate mods, plugins, and mod packs from two primary sources: Modrinth and CurseForge.
        4. Server Configuration:
            - Server Properties: Customize server properties such as game rules, difficulty, and world settings.
            - Server MOTD (Message of the Day): Describe the server, promote features, create announcements, attract attention.
        5. Server Icon Configuration: Choose an icon to represent your server visually.
        6. Logs Viewing: Access and review server logs to troubleshoot issues or monitor server activity.
        7. Server Backup: Create backups of your server data in zip files, ensuring data safety.
        8. Expanded Software Support:
            - Forge: Use the popular Forge modding platform.
            - Fabric: Opt for the lightweight Fabric mod loader.
            - Vanilla: Run a vanilla Minecraft server.
            - Snapshot: Experiment with the latest Minecraft snapshots.
            - Paper: Utilize the Paper server software.
            - Purpur: Explore the Purpur server implementation.
            - Arclight: Try out the Arclight server software.
            - Mohist: Use Mohist, which combines Forge and Fabric.
            - Banner: Deploy a Banner server.
            - Velocity: Set up a Velocity proxy server.'''
  elif choice == 'License':
    LICENSE = get('https://raw.githubusercontent.com/N-aksif-N/MineColab_Improved/master/LICENSE')
    text = f'''## 🔮 **License:**
      
      {LICENSE.text}'''
  elif choice == 'Found a bug?':
    text = ''' ## 🐛 Found a bug?

    - Report the bug by creating a new issue and use this helpful [issue template](https://github.com/N-aksif-N/MineColab/blob/main/.github/ISSUE_TEMPLATE/bug_report.md).
    Or join the Discord: [Minecolab Support](https://discord.gg/uCHcV3SAbs)
    - Suggest a new feature using this [template](https://github.com/N-aksif-N/MineColab/blob/main/.github/ISSUE_TEMPLATE/feature_request.md).
    - See all work that has been done, in processed, or what I want to do in the future from **[minecolab improve roadmap](https://github.com/users/N-aksif-N/projects/1)**'''
  elif choice == 'Notes':
    text = ''' ## 👍 Notes
    - Please use the FUNCTION in the notebook unless you want any ERRORS/BUGS.
    - If something does not work, try using a VPN like [windscribe](https://windscribe.com) before opening an issue.
    - Switch between the three tunnel providers and see which works best.
    - Make regular backups of your world.
    - Google Colab is not designed to create Minecraft servers, but it can be done. Google Colab promises to work for 12 hours straight, however, it is possible that if no person is reviewing the page or using the console, basically if the page detects inactivity the process will end. The performance is approximately 12 GB of RAM, together with a processor with a power of 2.2 GHz and 2 threads, this is better than many paid hostings, but it doesn't have support and doesn't promise to be open always
    - It is not advisable to fill it with as many as plugins, which is more limited to this server than its own processor, it is not very good, any hosting for 12 USD can offer a higher quality server, if you are thinking of creating something for many users, it's much better.

    [![ForTheBadge built-with-love](http://ForTheBadge.com/images/badges/built-with-love.svg)](https://github.com/N-aksif-N)'''
  return text
