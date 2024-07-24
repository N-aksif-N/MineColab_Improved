
from jproperties import Properties
from backends.settings import Delete_server, LOG, Backup, Server_Properties, MAP, Install_server, SOFTWARE, SERVERSJAR, INSTRUCTIONS
from backends.settings import ONLINE, COLABCONFIG_LOAD, PROGRESS, starting, disable, ERROR, SERVERCONFIG, drive_path
import streamlit as st
from streamlit_option_menu import option_menu
from jproperties import Properties
from os.path import exists
from streamlit_ace import st_ace
from time import sleep
from os import listdir
from json import load, dump

server_name = st.session_state.server_in_use
colabconfig = COLABCONFIG_LOAD(server_name)
if st.session_state['permission']['owner'] == True:
  st.session_state['permission'] = {'console': True, 'software': True, 'log viewing': True, 'world': True, 'server settings': True, 'owner': True}
permission = st.session_state['permission']
starting = st.session_state['Starting']

def SERVER():
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
      st.button(str(ONLINE(player=True)) + ' / ' + str(max_player), disabled = True)
    with col3:
      if ONLINE(status=True) == 'Offline': st.error(ONLINE(status=True))
      else: st.success(ONLINE(status=True))
    with col2:
      button = st.button(st.session_state.start_button, use_container_width=True)
      if button: starting()
  col1, tmp, col4 = st.columns([2, 2, 4], vertical_alignment="top")
  with col4:
    tunnel = colabconfig['tunnel_service']
    with st.container(border= True):
      st.markdown(f'<center>IP:&nbsp;&nbsp;{st.session_state.ip}</center>', unsafe_allow_html= True)
      st.write('')
      if st.button('Log out', use_container_width=True):
        if st.session_state.Starting == True and st.session_state.start_button == '🛑 Stop':
          starting()
        sleep(5)
        st.switch_page(st.Page('frontends/choose_server.py'))
      if st.button('Delete', use_container_width= True):
        Delete_server(server_name)
        sleep(5)
        st.switch_page(st.Page('frontends/choose_server.py'))
  with col1:
    software = colabconfig['server_type']; version = colabconfig['server_version'];
    with st.container(border= True):
      st.markdown(f'''
        **Server type**&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{software}

        **Server version**&nbsp;:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{version}

        **Tunnel server**&nbsp;&nbsp;&nbsp;:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{tunnel}  ''', unsafe_allow_html= True)

def SERVER_SETTINHS():
  if permission['server settings'] == True:
    if exists(f"{drive_path}/{server_name}/server.properties") == False: ERROR(' Running your minecraft server before editing properties')
    else:
      def booleen(str):
        if str == 'true':
          return True
        elif str == 'false':
          return False
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
            sleep(1)
            PROGRESS()
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
              ''',
              unsafe_allow_html=True
          )
          if uploaded_file is not None:
            # To read file as bytes:
            bytes_data = uploaded_file.getvalue()
            with open(f'{drive_path}/{server_name}/server-icon.png', 'rb') as f:
              f.write(bytes_data)
            sleep(5)
            PROGRESS()
      st.divider()
      st.subheader('Server properties')
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
          list_ = ["peaceful", "easy", "normal", "hard"]
          Difficulty = st.selectbox('Difficulty', ("peaceful", "easy", "normal", "hard"), index=list_.index(server_properties.get("difficulty").data))
          list_ = ["survival", "creative", "adventure", "spectator"]
          Gamemode = st.selectbox('Gamemode', ("survival", "creative", "adventure", "spectator") , index=list_.index(server_properties.get("gamemode").data))
          Villagers = st.checkbox('Villagers', value=booleen(server_properties.get('spawn-npcs').data))
          Nether = st.checkbox('Nether', value=booleen(server_properties.get('allow-nether').data))
          Force_gamemode = st.toggle('Force Gamemode', value=booleen(server_properties.get('force-gamemode').data))
        col1, col2 = st.columns([10, 1], vertical_alignment="bottom")
        with col1:
          Resource_pack = st.text_input('Resource pack: ', value=server_properties.get('resource-pack').data)
          Resource_pack_prompt = st.text_input('Resource pack prompt: ', value=server_properties.get('resource-pack-prompt').data)
        with col2:
          if st.button('Save', use_container_width=True): Server_Properties(server_properties, server_name, Slots, Gamemode, Difficulty, Cracked, PVP, Command_block, Fly, Villagers, Animals, Monsters, Whitelist, Nether, Force_gamemode, Spawn_protection, Resource_pack_required, Resource_pack, Resource_pack_prompt)
  else:
    st.warning('You do not have permission to get access to this page.')

def WORLDS():
  if permission['world'] == True:
    if exists(f'/content/drive/My Drive/minecraft/{server_name}/logs/latest.log') == False: ERROR('Running your minecraft server firsts')
    else:
      st.header('Worlds ')
      world_ = [i for i in listdir(f'{drive_path}/{server_name}') if 'world' in i]
      block = []
      for world in world_:
        expander = st.expander(f'World: {world}')
        with expander:
          col1, col2, col3 = st.columns([6, 3.5, 2.5])
          with col2:
            if expander.button('Upload', use_container_width=True, key=f'expander_{world}'):
              seed = expander.text_input('Seed map: ', placeholder='Enter None to set upload file', key=f'expander_{world}_3', value='')
              uploaded_file = expander.file_uploader("Upload", label_visibility='collapsed', key=f'expender_{world}_4')
              bytes_data = uploaded_file.getvalue()
              file_name = uploaded_file.name
              MAP(server_name= server_name, seed_map= seed, world_list=world_, world= world, content= bytes_data, file_name = file_name)
          with col3:
            if expander.button('Download', use_container_width=True, key=f'expander_{world}_2'):
              server_backup = expander.text_input('Server backup: ', placeholder='Enter None to set default backup', key=f'expander_{world}_5', value='')
              if server_backup != '': Backup(server_name= server_name, file_name=world, server_backup= server_backup)
  else:
    st.warning('You do not have permission to get access to this page.')

def SERVER_TYPE():
  if permission['software'] == True:
    SERVERJAR_ = ['vanilla', 'snapshot', 'purpur', 'paper', 'velocity', 'fabric', 'forge', 'arclight', 'mohist', 'banner']
    button_list = []
    st.header('Software')
    placeholder = st.empty()
    with placeholder.container(border=True):
      for server_type in SERVERJAR_:
        button = container.button(f':green[{server_type}]', use_container_width= True)
        button_list.append(button)
    server_type = ''; server_version = []
    for button in button_list:
      if button:
        server_version = SERVERSJAR(server_type= SERVERJAR_[button_list.index(button)], version='', all = True)
        server_type = SERVERJAR_[button_list.index(button)]
        break
    sleep(2)
    placeholder.empty()
    sleep(2)
    with placeholder.container(border=True):
      st.header(server_type);
      button_list = []
      col1, col2 = st.columns([7, 4])
      with col1:
        version = st.selectbox('Version: ', tuple(server_version), index=None)
      with col2:
        tunnel_service = st.selectbox('Tunnel service ', ('default', 'ngrok', 'argo', 'zrok', 'playit', 'localtonet'), index=None)
      if choice != None and tunnel_service != None:
        serverconfig = load(open(SERVERCONFIG))
        serverconfig['server_list'] += [server_name]
        serverconfig['server_in_use'] = server_name
        if tunnel_service == 'default': tunnel_service = colabconfig['tunnel_service']
        if serverconfig['ngrok_proxy'] == {"authtoken": "", "region": ""} and tunnel_service == 'ngrok':
          LOG('Get your authtoken from https://dashboard.ngrok.com/get-started/your-authtoken')
          serverconfig['ngrok_proxy']['authtoken'] = st.text_input('Your authtoken: ')
          LOG('Available Regions:', ' ap - Asia/Pacific (Singapore)', ' au - Australia (Sydney)', ' eu - Europa (Frankfurt - Germany)', ' in - India (Mumbai)', ' jp - Japan (Tokyo)', ' sa - America (São Paulo - Brazil)', ' us - United States (Ohio)')
          serverconfig['ngrok_proxy']['region'] = st.text_input('Region: ')
        elif tunnel_service == 'zrok' and serverconfig['zrok_proxy'] == {'authtoken': ''}:
          serverconfig['zrok_proxy']['authtoken'] = st.text_input('Your zrok token: ')
        elif tunnel_service == 'localtonet' and serverconfig['localtonet_proxy'] == {'authtoken': ''}:
          LOG('Get your authtoken from https://localtonet.com/usertoken')
          serverconfig['localtonet_proxy']['authtoken'] = st.text_input('Your localtonet token: ')
        SOFTWARE(server_name = server_name, server_type  = server_type , version = version, tunnel_service = tunnel_service)
  else:
    st.warning('You do not have permission to get access to this page.')

def SERVER_LOG():
  if permission['log viewing'] == True:
    st.header('Server Logs ')
    if exists(f'/content/drive/My Drive/minecraft/{server_name}/logs/latest.log'):
      with open(f'/content/drive/My Drive/minecraft/{server_name}/logs/latest.log', 'r') as f:
        content_ = f.read(); LOG('Try access to https://mclo.gs to see problems and the way to deal with.');
      content = st_ace(value=content_, readonly=True, language='plain_text', show_gutter=True)
    else: ERROR("Error: File didn't exists")
  else:
    st.warning('You do not have permission to get access to this page.')

def SHARE_ACCESS():
  if permission['owner'] == True:
    st.header('Share access')
    col1, col2 = st.columns(2, vertical_alignment="bottom")
    with col1:
      user_name = st.text_input('User name: ', value='')
    with col2:
      create =  st.button('Create', use_container_width=True, on_click=disable)
    world = False; server_settings = False; log_viewing = False; software = False; owner = False; console = False
    if st.session_state.disable:
      with st.container(border=True):
        col1, col2, col3 = st.columns(3, vertical_alignment="top")
        with col1:
          if st.checkbox('Run/stop server', value=False):
            console = True
          if st.checkbox('Software', value=False):
            software = True
        with col2:
          if st.checkbox('Log viewing', value=False):
            log_viewing = True
          if st.checkbox('World', value=False):
            world = True
        with col3:
          if st.checkbox('Server settings', value=False):
            server_settings = True
          if st.checkbox('Administration', value=False):
            owner = True
        tmp, col2 = st.columns([9, 1], vertical_alignment="top")
        with col2:
          if st.button('Save', use_container_width=True):
            if user_name != '':
              sleep(5)
              user = load(open('/content/drive/MyDrive/streamlit-app/user.txt'))
              user['user'][user_name] = ['', {'console': console, 'software': software, 'log viewing': log_viewing, 'world': world, 'server settings': server_settings, 'owner': owner}]
              dump(user, open('/content/drive/MyDrive/streamlit-app/user.txt', 'w'))
  else:
    st.warning('You do not have permission to get access to this page.')

if colabconfig['server_type'] == 'paper' or colabconfig['server_type'] == 'purpur': choice_1 = 'Plugins'
elif colabconfig['server_type'] == 'forge' or colabconfig['server_type'] == 'fabric': choice_1 = 'Mods'
elif colabconfig['server_type'] == 'arclight' or colabconfig['server_type'] == 'mohist' or colabconfig['server_type'] == 'banner': choice_1 = 'Plugins/Mods'
else: choice_1 = ''

st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 275px !important; # Set the width to your desired value
        }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
  tmp, col2, tmp = st.columns(3)
  with col2
    st.image('https://raw.githubusercontent.com/N-aksif-N/MineColab/master/minecolab.png', width=90)
  if choice_1 == '':
    choice = option_menu("Minecolab", ["Server", 'Console', "Log", 'Settings', 'Software', 'Files', 'Worlds', 'Share acess',"---", 'Instructions'],  icons=['amd', 'caret-right-fill', 'newspaper', 'gear', 'cloud-arrow-up-fill','archive-fill', 'globe', 'bookmark-fill'], menu_icon=None)
  else:
    choice = option_menu("Minecolab", ["Server", 'Console', "Log", 'Settings', 'Software', choice_1 ,'Files', 'Worlds', 'Share acess', "---", 'Instructions'],  icons=['amd', 'caret-right-fill', 'newspaper', 'gear', 'cloud-arrow-up-fill', 'git', 'archive-fill', 'globe', 'bookmark-fill'], menu_icon=None)
  col1, col2 = st.columns(2, vertical_alignment='top')
  with col1:
    st.link_button("Github", "https://github.com/N-aksif-N/MineColab_Improved", use_container_width=True)
  with col2:
    st.link_button("Discord", "https://discord.gg/F9nPJTn7Nu", use_container_width=True)
if choice == 'Instructions': INSTRUCTIONS()
elif choice == 'Server': SERVER()
elif choice =='Settings': SERVER_SETTINHS()
elif choice == 'Worlds': WORLDS()
elif choice == 'Log': SERVER_LOG()
elif choice == 'Software': SERVER_TYPE()
elif choice == 'Share acess': SHARE_ACCESS()
else:
  st.write('Are comming')
