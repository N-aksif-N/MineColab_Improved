from jproperties import Properties
from backends.settings import Delete_server, Backup, Server_Properties, MAP, Install_server, SERVERSJAR, SET_SERVERCONFIG, booleen, LOGS, GITHUB_GUIDE
from backends.settings import ONLINE, COLABCONFIG_LOAD, PROGRESS, starting, SERVERCONFIG, drive_path, path, USER, ERROR, LOG
import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_ace import st_ace
from jproperties import Properties
from os.path import exists
from time import sleep
from os import listdir
from json import load, dump
from datetime import datetime

user = load(open(USER)); uid = dict(st.context.headers)
del uid['Sec-Websocket-Key']
uid = str(uid); user_name = '';
for user_ in user['user']:
  if user_ != 'authtoken': # I use two layers of `if` because there may be someones won't login but will connect directly to main_page
    if uid in user['user'][user_]['user_id']: user_name = user_; break
if user_name == '': st.switch_page(st.Page('frontends/login.py'))
server_name = user['user'][user_name]['server_in_use']
if server_name == '': st.switch_page(st.Page('frontends/choose_server.py'))
permission = user['user'][user_name]['permission']
serverconfig = load(open(SERVERCONFIG))
colabconfig = COLABCONFIG_LOAD(server_name)
if permission['owner'] == True: permission = {'console': True, 'software': True, 'log viewing': True, 'players': False, 'plugins/mods': True, 'world': True, 'server settings': True, 'owner': True}

@st.fragment
def PLAYER_2(name):
  version = colabconfig['server_version']
  if name == 'Whitelist': name = 'whitelist.json'
  elif name == 'OPs': 
    if version <= '1.7.8': name = 'ops.txt'
    else: name = 'ops.json'
  elif name == 'Banned players': name = 'banned-players.json'
  else: name = 'banned-ips.json'
  if exists(f'{drive_path}/{server_name}/{name}'):
    st.header(name)
    col1, col2 = st.columns(2, vertical_alignment="bottom")
    with col1: player_name = st.text_input('User name: ', value='')
    with col2:
      if st.button('Create', use_container_width=True):
        if player_name != '':
          if name == 'ops.txt':
            with open(f'{drive_path}/{server_name}/{name}', 'w') as f:
              f.write(player_name)
          elif name == 'ops.json' or name == 'whitelist.json': 
            rJSON = GET(f'https://playerdb.co/api/player/minecraft/{player_name}').json()
            if rJSON['code'] == 'player.found':
              id = rJSON['data']['player']['id']
              try:
                content = load(f'{drive_path}/{server_name}/{name}')
                if name == 'ops.json': conent.append({"uuid": id, "name": player_name, "level": '4'})
                elif name == 'whitelist.json': content.append({"uuid": id, "name": player_name})
                else:
                  now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                  content.append({"uuid": id, "name": player_name, "created": f"{now} +0100", "source": "Console", "expires": "forever", "reason": "Set in the minecolab website"})
              except:
                if name == 'ops.json': content = [{"uuid": id, "name": player_name, "level": '4'}]
                elif name == 'whitelist.json': content = [{"uuid": id, "name": player_name}]
                else: 
                  now = datetime.now().strftime("%d-%m-%Y %H:%M:%S") # +0100 is the default 
                  content = [{"uuid": id, "name": player_name, "created": f"{now} +0100", "source": "Console", "expires": "forever", "reason": "Set in the minecolab website"}] 
              dump(content, opem(f'{drive_path}/{server_name}/{name}', 'w'))  
            else: ERROR('Player not found.')
    
    if name == 'ops.txt':
      LOG("We're in developing this. Wait for it")
    elif name == 'ops.json' or name == 'whitelist.json' or name == 'banned-players.json':
      try:
        content = load(f'{drive_path}/{server_name}/{name}')
        for player in content:
          with st.container(border=True):
            col1, col2 = st.columns([12, 1], vertical_alignments='top')
            with col1: st.write(player['name'])
            with col2:
              if st.button('🗑️', use_container_width=True, key = f'{player}_delete_btn'):
                LOG('Deleting player...'); content.remove(player)
                dump(content, open(f'{drive_path}/{server_name}/{name}', 'w'))
      except: pass
    else:      
      LOG("We're in developing this function.")
  else: ERROR("You didn't run the server .")

@st.fragment
def SERVER_TYPE_2(server_type, server_version):
  with st.container(border=True):
    st.header(server_type)
    col1, col2 = st.columns([7, 4])
    with col1: version = st.selectbox('Version: ', tuple(server_version), index=None)
    with col2: tunnel_service = st.selectbox('Tunnel service ', ('default', 'ngrok', 'argo', 'zrok', 'playit', 'localtonet'), index=None)
    change = st.button('Change', use_container_width=True)
    if change is False or version is None or tunnel_service is None: st.stop()
    if tunnel_service == 'default': tunnel_service = colabconfig['tunnel_service']
    SET_SERVERCONFIG(tunnel_service, server_name)
    sleep(5); Delete_server(server_name, software= True)
    sleep(15); Install_server(server_name = server_name, server_type  = server_type , version = version, tunnel_service = tunnel_service)

def main()
  st.markdown(""" <style> section[data-testid="stSidebar"] {width: 275px !important; # Set the width to your desired value} </style> """, unsafe_allow_html=True)
  with st.sidebar:
    st.markdown('<p align="center"><a href="https://github.com/N-aksif-N/MineColab"><img src="https://raw.githubusercontent.com/N-aksif-N/MineColab/master/minecolab.png" alt="Logo" height="80"/></a></p>',unsafe_allow_html=True)
    if ONLINE(server_name, status=True) == 'Offline': st.error(ONLINE(server_name, status=True))
    else: st.success(ONLINE(server_name, status=True))
      
    if colabconfig['server_type'] == 'paper' or colabconfig['server_type'] == 'purpur': choice_1 = 'Plugins'
    elif colabconfig['server_type'] == 'forge' or colabconfig['server_type'] == 'fabric': choice_1 = 'Mods'
    elif colabconfig['server_type'] == 'arclight' or colabconfig['server_type'] == 'mohist' or colabconfig['server_type'] == 'banner': choice_1 = 'Plugins/Mods'
    else: choice_1 = ''
    if choice_1 == '': choice = option_menu("Minecolab", ["Server", 'Console', "Log", 'Settings', 'Software', 'Player', 'Worlds', 'Acess',"---", 'Instructions'],  icons=['amd', 'caret-right-fill', 'newspaper', 'gear', 'cloud-arrow-up-fill','person-fill', 'globe', 'person-add'], menu_icon=None)
    else: choice = option_menu("Minecolab", ["Server", 'Console', "Log", 'Settings', 'Software', choice_1 ,'Player', 'Worlds', 'Acess', "---", 'Instructions'],  icons=['amd', 'caret-right-fill', 'newspaper', 'gear', 'cloud-arrow-up-fill', 'git', 'person-fill', 'globe', 'person-add'], menu_icon=None)
    
    col1, col2 = st.columns(2, vertical_alignment='top')
    with col1: st.link_button("Github", "https://github.com/N-aksif-N/MineColab_Improved", use_container_width=True)
    with col2: st.link_button("Discord", "https://discord.gg/F9nPJTn7Nu", use_container_width=True)
  
  if choice == 'Instructions':
  
    st.markdown('''
      <p align="center"><a href="https://github.com/N-aksif-N/MineColab"><img src="https://raw.githubusercontent.com/N-aksif-N/MineColab/master/minecolab.png" alt="Logo" height="80"/></a></p>
      <h1 align="center">Mine Colab [Improved]</h1>
      <p align="center">Run Minecraft Server on Google Colab</p>
      <p align="right">
        <a href="https://colab.research.google.com/github/N-aksif-N/MineColab_Improved/blob/free-config/MineColabImproved.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>
        <a href="https://github.com/N-aksif-N/MineColab_Improved/releases/download/0.1.3/MinecolabImproved.ipynb" target="_parent"><img src="https://cdn-icons-png.flaticon.com/128/10741/10741247.png" alt="Download" width="20" height="20"></a>
      </p>''', unsafe_allow_html= True)
    st.write()
    st.divider()
    st.write()
    choice_ = st.selectbox('Frequent Question', ('What is Mine Colab [Improved]', 'Can Minecolab server online 24/7 ?', 'Instructions', 'How does it actually work ?', 'License', 'Found a bug?', 'Notes'))
    content = GITHUB_GUIDE(choice_)
    st.markdown(content)
  
  elif choice == 'Server':
  
    with st.container(border= True):
      st.markdown(f'<center>{server_name}</center>', unsafe_allow_html=True)
      col1, tmp, col2, tmp, col3 = st.columns([1,3,1,3,1], vertical_alignment="bottom")
      with col1:
        try:
          server_properties = Properties() # Download file
          with open(f"{drive_path}/{server_name}/server.properties", "rb") as f:
              server_properties.load(f);
          max_player = server_properties.get('max-players').data
        except: max_player = 20
        st.button(str(ONLINE(server_name, player=True)) + ' / ' + str(max_player), disabled = True)
      with col3:
        if ONLINE(server_name, status=True) == 'Offline': st.error(ONLINE(server_name, status=True))
        else: st.success(ONLINE(server_name, status=True))
      with col2:
        if st.button(st.session_state.Starting[server_name][0], use_container_width=True): starting(server_name)
    col1, tmp, col4 = st.columns([2, 2, 4], vertical_alignment="top")
    with col4:
      tunnel = colabconfig['tunnel_service']
      with st.container(border= True):
        ip = st.session_state.ip[server_name]
        st.markdown(f'<center>IP:&nbsp;&nbsp;{ip}</center>', unsafe_allow_html= True)
        if st.button('Log out', use_container_width=True):
          user['user'][user_name]['server_in_use'] = ''
          dump(user, open(USER, 'w'))
          sleep(2); st.switch_page(st.Page('frontends/choose_server.py'))
        if st.button('Delete', use_container_width= True):
          Delete_server(server_name)
          user['user'][user_name]['server_in_use'] = ''
          dump(user, open(USER, 'w'))
          sleep(2); st.switch_page(st.Page('frontends/choose_server.py'))
    with col1:
      software = colabconfig['server_type']; version = colabconfig['server_version'];
      with st.container(border= True):
        st.markdown(f'''
          **Server type**&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{software}
  
          **Server version**&nbsp;:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{version}
  
          **Tunnel server**&nbsp;&nbsp;&nbsp;:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{tunnel}  ''', unsafe_allow_html= True)
  
  elif choice =='Settings':
  
    if permission['server settings'] == True:
      if exists(f"{drive_path}/{server_name}/server.properties") == False: ERROR(' Running your minecraft server before editing properties')
      else:          
        st.divider()
        with st.container(border=True):
          col1, col2 = st.columns([0.75, 4], vertical_alignment="center")
          choice = ''; motd_ = ''
          with col2:
            server_properties = Properties() # Download file
            with open(f"{drive_path}/{server_name}/server.properties", "rb") as f:
                server_properties.load(f); motd = server_properties.get('motd').data
            with st.container(border=True):
              st.markdown(f'''<center>Server:&nbsp;&nbsp;{server_name}</center>''', unsafe_allow_html= True)
              motd_ = st.text_input('MOTD: ', value=str(motd))
            motd_button = st.button('Change MOTD', use_container_width= True)
            if motd_button:
              sleep(1)
              server_properties = Properties()
              with open(f"{drive_path}/{server_name}/server.properties", "rb") as f:
                  server_properties.load(f, "utf-8")
              server_properties["motd"] = motd
              with open(f"{drive_path}/{server_name}/server.properties", "wb") as f:
                  server_properties.store(f, encoding="utf-8")
              sleep(1); PROGRESS()
          with col1:
            if exists(f'{drive_path}/{server_name}/server-icon.png'): file_ = f'{drive_path}/{server_name}/server-icon.png'
            else: file_ = 'https://media.minecraftforum.net/attachments/300/619/636977108000120237.png'
            st.image(file_, width=128)
            uploaded_file = st.file_uploader("Change", label_visibility='collapsed') #####
            st.markdown(
                '''
                <style>
                    [data-testid='stFileUploader'] section > input + div {
                        display: none;
                        padding-top: 0;
                    }
                </style>
                ''', unsafe_allow_html=True)
            if uploaded_file is not None:
              # To read file as bytes:
              bytes_data = uploaded_file.getvalue()
              with open(f'{drive_path}/{server_name}/server-icon.png', 'rb') as f:
                f.write(bytes_data)
              sleep(5); PROGRESS()
              
        st.divider(); st.subheader('Server properties')
        server_properties = Properties() # Download file
        with open(f"{drive_path}/{server_name}/server.properties", "rb") as f:
            server_properties.load(f, 'utf-8')
        with st.container(border=True):
          col1, col2, col3 = st.columns(3, vertical_alignment="top")
          with col1:
            Slots = st.slider('Slots', min_value=0, max_value=100, value=int(server_properties.get("max-players").data), step=1)
            Whitelist = st.checkbox('Whitelist', value=booleen(server_properties.get('white-list').data))
            Cracked = st.checkbox('Cracked', value=booleen(server_properties.get("online-mode").data))
            Fly = st.toggle('Fly', value=booleen(server_properties.get('allow-flight').data))
            Monsters = st.toggle('Monsters', value=booleen(server_properties.get('spawn-monsters').data))
          with col2:
            Spawn_protection = st.slider('Spawn Protection', min_value=0, max_value=100, value=int(server_properties.get('spawn-protection').data), step=1)
            PVP = st.toggle('PVP', value=booleen(server_properties.get('pvp').data))
            Command_block = st.toggle('Commandblocks', value=booleen(server_properties.get('enable-command-block').data))
            Animals = st.checkbox('Animals', value=booleen(server_properties.get('spawn-animals').data))
            Resource_pack_required = st.checkbox('Resource pack required', value=booleen(server_properties.get('require-resource-pack').data))
          with col3:
            list_1 = ["peaceful", "easy", "normal", "hard"]; list_2 = ["survival", "creative", "adventure", "spectator"]
            Difficulty = st.selectbox('Difficulty', ("peaceful", "easy", "normal", "hard"), index=list_1.index(server_properties.get("difficulty").data))
            Gamemode = st.selectbox('Gamemode', ("survival", "creative", "adventure", "spectator") , index=list_2.index(server_properties.get("gamemode").data))
            Villagers = st.checkbox('Villagers', value=booleen(server_properties.get('spawn-npcs').data))
            Nether = st.checkbox('Nether', value=booleen(server_properties.get('allow-nether').data))
            Force_gamemode = st.toggle('Force Gamemode', value=booleen(server_properties.get('force-gamemode').data))
          col1, col2 = st.columns([10, 1], vertical_alignment="bottom")
          with col1:
            Resource_pack = st.text_input('Resource pack: ', value=server_properties.get('resource-pack').data)
            Resource_pack_prompt = st.text_input('Resource pack prompt: ', value=server_properties.get('resource-pack-prompt').data)
          with col2:
            if st.button('Save', use_container_width=True): Server_Properties(server_properties, server_name, Slots, Gamemode, Difficulty, Cracked, PVP, Command_block, Fly, Villagers, Animals, Monsters, Whitelist, Nether, Force_gamemode, Spawn_protection, Resource_pack_required, Resource_pack, Resource_pack_prompt)
    else: st.warning('You do not have permission to get access to this page.')
  
  elif choice == 'Worlds':
  
    if permission['world'] == True:
      if exists(f'{drive_path}/{server_name}/logs/latest.log') == False: ERROR('Running your minecraft server firsts')
      else:
        world_ = [i for i in listdir(f'{drive_path}/{server_name}') if 'world' in i]
        st.header('Worlds ')
        for world in world_:
          with st.expander(f'World: {world}'):
            col1, col2, col3 = st.columns([6, 3.5, 2.5])
            with col2:
              if expander.button('Upload', use_container_width=True, key=f'expander_{world}'):
                seed = expander.text_input('Seed map: ', placeholder='Enter None to set upload file', key=f'expander_{world}_3', value='')
                uploaded_file = expander.file_uploader("Upload", label_visibility='collapsed', key=f'expender_{world}_4')
                if uploaded_file is not None:
                  bytes_data = uploaded_file.getvalue(); file_name = uploaded_file.name
                  MAP(server_name= server_name, seed_map= seed, world_list=world_, world= world, content= bytes_data, file_name = file_name)
            with col3:
              if expander.button('Download', use_container_width=True, key=f'expander_{world}_2'):
                server_backup = expander.text_input('Server backup: ', placeholder='Enter None to set default backup', key=f'expander_{world}_5', value='')
                if server_backup != '': Backup(server_name= server_name, file_name=world, server_backup= server_backup)
    else: st.warning('You do not have permission to get access to this page.')
  
  elif choice == 'Log':
  
    if permission['log viewing'] == True:
      if exists(f'{drive_path}/{server_name}/logs/latest.log'):
        content_ = LOGS(server_name)
        st.header('Server Logs ')
        st_ace(value=content_, readonly=True, language='plain_text', show_gutter=True)
      else: ERROR("Error: File didn't exists")
    else: st.warning('You do not have permission to get access to this page.')
  
  elif choice == 'Software':
  
    if permission['software'] == True:
      SERVERJAR_ = ['vanilla', 'purpur', 'fabric', 'arclight', 'snapshot', 'paper', 'forge', 'mohist', 'velocity', 'banner']
      button_list = []; placeholder = st.empty()
      st.header('Software')
      with placeholder.container(border=True):
        col1, col2, col3 = st.columns(3, vertical_alignment='top')
        with col1:
          for i in (0, 1, 2, 3): server_type = SERVERJAR_[i]; button = st.button(f':green[{server_type}]', use_container_width= True); button_list.append(button)
        with col2:
          for i in (4, 5, 6, 7): server_type = SERVERJAR_[i]; button = st.button(f':green[{server_type}]', use_container_width= True); button_list.append(button)
        with col3:
          st.button('', use_container_width=True, disabled=True, key= 'ex_1'); 
          server_type = SERVERJAR_[8]; button = st.button(f':green[{server_type}]', use_container_width= True); button_list.append(button)
          st.button('', use_container_width=True, disabled=True, key= 'ex_2')
          server_type = SERVERJAR_[9]; button = st.button(f':green[{server_type}]', use_container_width= True); button_list.append(button)
      server_type = ''; server_version = []
      for button in button_list:
        if button:
          server_version = SERVERSJAR(server_type= SERVERJAR_[button_list.index(button)], version='', all = True)
          server_type = SERVERJAR_[button_list.index(button)]
          sleep(1); placeholder.empty(); sleep(1); SERVER_TYPE_2(server_type, server_version)
    else: st.warning('You do not have permission to get access to this page.')
  
  elif choice == 'Acess':
    if permission['owner'] == True:
      st.header('Share access')
      col1, col2 = st.columns(2, vertical_alignment="bottom")
      with col1:
        user_name = st.text_input('User name: ', value='')
      with col2:
        if st.button('Create', use_container_width=True):
          if user_name != '':
            if user_name in user['user']: ERROR('This username already exists')
            else:
              user['user'][user_name] = {'permission': {'console': False, 'software': False, 'log viewing': False, 'world': False, 'server settings': False, 'owner': True}, 'user_id': [''], 'server_in_use': ''}
              dump(user, open(f'{path}/content/drive/My Drive/streamlit-app/user.txt', 'w'))
      
      dict_ = user['user']
      for user_ in dict_:
        if user_ != 'authtoken':
          with st.expander(f'User: {user_}'):
            world = False; server_settings = False; log_viewing = False; software = False; owner = False; console = False; players = False; plugins_mods= False
            with st.container(border=True):
              col1, col2, col3 = st.columns(3, vertical_alignment="bottom")
              with col1:
                st.checkbox('Run/stop server', value=user['user'][user_]['permission']['console'], key=f'{user_}console')
                st.checkbox('Software', value=user['user'][user_]['permission']['software'], key=f'{user_}server_type')
                st.checkbox('Player Management', value=user['user'][user_]['permission']['players'], key=f'{user_}players')
              with col2:
                st.checkbox('Log viewing', value=user['user'][user_]['permission']['log viewing'], key=f'{user_}logs')
                st.checkbox('World', value=user['user'][user_]['permission']['world'], key=f'{user_}worlds')
                st.checkbox('Install plugins/mods', value=user['user'][user_]['permission']['plugins/mods'], key=f'{user_}plugins/mods')
              with col3:
                st.checkbox('Server settings', value=user['user'][user_]['permission']['server settings'], key=f'{user_}server_settings')
                st.checkbox('Administration', value=user['user'][user_]['permission']['owner'], key=f'{user_}administration')
              tmp, col1, col2 = st.columns([9, 1, 1], vertical_alignment="top")
              with col2:
                if st.button('Save', use_container_width=True, key= f'{user_}_save'):
                  if st.session_state[f'{user_}console']: console = True
                  if st.session_state[f'{user_}server_type']: software = True
                  if st.session_state[f'{user_}logs']: log_viewing = True
                  if st.session_state[f'{user_}players']: players = True
                  if st.session_state[f'{user_}plugins/mods']: plugins_mods = True
                  if st.session_state[f'{user_}worlds']: world = True
                  if st.session_state[f'{user_}server_settings']: server_settings = True
                  if st.session_state[f'{user_}administration']: owner = True
                  user['user'][user_]['permission'] = {'console': console, 'software': software, 'log viewing': log_viewing, 'players': players, 'plugins/mods': plugins_mods, 'world': world, 'server settings': server_settings, 'owner': owner}
                  dump(user, open(f'{path}/content/drive/My Drive/streamlit-app/user.txt', 'w'))
              with col1:
                if st.button('Remove', use_container_width=True, key= f'{user_}_remove'):
                  del user['user'][user_]
                  dump(user, open(f'{path}/content/drive/My Drive/streamlit-app/user.txt', 'w'))
    else: st.warning('You do not have permission to get access to this page.')
      
  elif choice == 'Player':
    
    if permission['players'‎]:
      
      button_list = ['White_list', 'OPs', 'Banned players', 'Banned IPs']
      col1, col2, col3, col4 = st.columns(4, vertical_alignments= 'bottom')
      with col1: st.button(button_list[0], use_container_width=True, key= button_list[0])
      with col2: st.button(button_list[1], use_container_width=True, key= button_list[1])
      with col3: st.button(button_list[2], use_container_width=True, key= button_list[2])
      with col4: st.button(button_list[3], use_container_width=True, key= button_list[3])
        
      for button in button_list:
        if st.session_state[button_list[button]]:
          PLAYER_2(name)
    else: st.warning('You do not have permission to get access to this page.')
        
  else: st.write('Are comming')
    
if __name__ == "__main__":
  main()
