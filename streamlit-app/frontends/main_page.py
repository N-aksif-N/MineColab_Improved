from jproperties import Properties
from backends.settings import Delete_server, LOG, Backup, Server_Properties, MAP, Install_server, SERVERSJAR, SET_SERVERCONFIG
from backends.settings import ONLINE, COLABCONFIG_LOAD, PROGRESS, starting, disable, ERROR, SERVERCONFIG, drive_path, path, USER
import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_ace import st_ace
from jproperties import Properties
from os.path import exists
from time import sleep
from os import listdir
from json import load, dump

user = load(open(USER)); uid = dict(st.context.headers)
del uid['Sec-Websocket-Key']
uid = str(uid); user_name = '';
for user_ in user['user']:
  if user_ != 'authtoken':
    if uid in user['user'][user_]['user_id']:
      user_name = user_
      break
if user_name == '': st.switch_page(st.Page('frontends/login.py'))
server_name = user['user'][user_name]['server_in_use']
if server_name == '': st.switch_page(st.Page('frontends/choose_server.py'))
permission = user['user'][user_name]['permission']
serverconfig = load(open(SERVERCONFIG))
colabconfig = COLABCONFIG_LOAD(server_name)
if permission['owner'] == True:
  permission = {'console': True, 'software': True, 'log viewing': True, 'world': True, 'server settings': True, 'owner': True}

@st.fragment
def SERVER_TYPE_2(server_type, server_version):
  with st.container(border=True):
    st.header(server_type)
    col1, col2 = st.columns([7, 4])
    with col1:
      version = st.selectbox('Version: ', tuple(server_version), index=None)
    with col2:
      tunnel_service = st.selectbox('Tunnel service ', ('default', 'ngrok', 'argo', 'zrok', 'playit', 'localtonet'), index=None)
    change = st.button('Change', use_container_width=True)
    if change is False and version is None and tunnel_service is None:
      st.stop()
    if tunnel_service == 'default': tunnel_service = colabconfig['tunnel_service']
    SET_SERVERCONFIG(tunnel_service, server_name)
    Delete_server(server_name)
    Install_server(server_name = server_name, server_type  = server_type , version = version, tunnel_service = tunnel_service, server_config=False)

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
  st.markdown('<p align="center"><a href="https://github.com/N-aksif-N/MineColab"><img src="https://raw.githubusercontent.com/N-aksif-N/MineColab/master/minecolab.png" alt="Logo" height="80"/></a></p>',unsafe_allow_html=True)
  if choice_1 == '':
    choice = option_menu("Minecolab", ["Server", 'Console', "Log", 'Settings', 'Software', 'Files', 'Worlds', 'Share acess',"---", 'Instructions'],  icons=['amd', 'caret-right-fill', 'newspaper', 'gear', 'cloud-arrow-up-fill','archive-fill', 'globe', 'bookmark-fill'], menu_icon=None)
  else:
    choice = option_menu("Minecolab", ["Server", 'Console', "Log", 'Settings', 'Software', choice_1 ,'Files', 'Worlds', 'Share acess', "---", 'Instructions'],  icons=['amd', 'caret-right-fill', 'newspaper', 'gear', 'cloud-arrow-up-fill', 'git', 'archive-fill', 'globe', 'bookmark-fill'], menu_icon=None)
  col1, col2 = st.columns(2, vertical_alignment='top')
  with col1:
    st.link_button("Github", "https://github.com/N-aksif-N/MineColab_Improved", use_container_width=True)
  with col2:
    st.link_button("Discord", "https://discord.gg/F9nPJTn7Nu", use_container_width=True)

if choice == 'Instructions':

  st.markdown('''
    <p align="center"><a href="https://github.com/N-aksif-N/MineColab"><img src="https://raw.githubusercontent.com/N-aksif-N/MineColab/master/minecolab.png" alt="Logo" height="80"/></a></p>
    <h1 align="center">Mine Colab [Improved]</h1>
    <p align="center">Run Minecraft Server on Google Colab</p>
    <p align="right">
      <a target="_blank" href="https://discord.gg/F9nPJTn7Nu"><img src="https://discordapp.com/api/guilds/1214801871827501097/widget.png?style=shield" alt="Discord Minecolab Support"></a>
      <a target="_blank" href="https://github.com/N-aksif-N/Minecolab"><img src="https://img.shields.io/github/stars/N-aksif-N/Minecolab.svg?style=social&label=Star" alt="Star"></a>
      <a href="https://colab.research.google.com/github/N-aksif-N/MineColab_Improved/blob/free-config/MineColabImproved.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>
      <a href="https://github.com/N-aksif-N/MineColab_Improved/releases/download/0.1.3/MinecolabImproved.ipynb" target="_parent"><img src="https://cdn-icons-png.flaticon.com/128/10741/10741247.png" alt="Download" width="20" height="20"></a>
    </p>
  ''', unsafe_allow_html= True)
  st.write()
  st.divider()
  st.write()
  choice = st.selectbox('Frequent Question', ('What is Mine Colab [Improved]', 'Can Minecolab server online 24/7 ?', 'Instructions', 'How does it actually work ?', 'License', 'Found a bug?', 'Notes'))
  if choice == 'What is Mine Colab [Improved]':
    st.markdown('''
      # :hear_no_evil:  First of all, what is Mine Colab [Improved]?

      Mine Colab [Improved] is an alternative [Minecolab project](https://github.com/thecoder-001/MineColab) that helps to build a Minecraft server on your own Gdrive. It is easier to use and more flexible to edit. This project is suited for mainly [google colab](https://colab.research.google.com) (a free service based on [jupyter notebook](https://jupyter.org/) and [ubuntu](https://ubuntu.com) os), though this can be applied on other projects like [jupyter lab](https://jupyter.org/try-jupyter/lab/), [deepnote](https://deepnote.com/), etc. This project followed the [GNU License](https://github.com/N-aksif-N/Minecolab/blob/master/LICENSE). Before looking closer, please make sure to see [the original](https://github.com/thecoder-001/MineColab)
    ''')
  elif choice == 'Can Minecolab server online 24/7 ?':
    st.markdown('''
      # :moneybag:  Can Minecolab server online 24/7?

      Of course, it's possible but with a little hard work. Google Colab is a free service and it is not suited for 24/7 online so you can use [deepnote](https://deepnote.com/) instead. Or if you still want to use google collab you may need some tricks or friends to make the web online and accept the captcha manually.
    ''')
  elif choice == 'Instructions':
    st.markdown('''
      # :page_with_curl: Instructions
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
      ''')
  elif choice == 'How does it actually work ?':
    st.markdown('''
        # :zap:  So, how does it actually work?
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
            - Velocity: Set up a Velocity proxy server.
        ''')
  elif choice == 'License':
    st.markdown('''
      ## 🔮 **License:**
      [![License](https://camo.githubusercontent.com/966484ce4d3faab2d9803e7354431ff8e4fce6a424e97689f05b2f50f4ee424b/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f6c6963656e73652f497a7a656c416c697a2f4172636c696768743f7374796c653d666c61742d737175617265)](https://github.com/N-aksif-N)
    ''')
  elif choice == 'Found a bug?':
    st.markdown('''
    ## 🐛 Found a bug?

    - Report the bug by creating a new issue and use this helpful [issue template](https://github.com/N-aksif-N/MineColab/blob/main/.github/ISSUE_TEMPLATE/bug_report.md).
    Or join the Discord: [Minecolab Support](https://discord.gg/uCHcV3SAbs)
    - Suggest a new feature using this [template](https://github.com/N-aksif-N/MineColab/blob/main/.github/ISSUE_TEMPLATE/feature_request.md).
    - See all work that has been done, in processed, or what I want to do in the future from **[minecolab improve roadmap](https://github.com/users/N-aksif-N/projects/1)**
  ''')
  else:
    st.markdown('''
    ## 👍 Notes
    - Please use the FUNCTION in the notebook unless you want any ERRORS/BUGS.
    - If something does not work, try using a VPN like [windscribe](https://windscribe.com) before opening an issue.
    - Switch between the three tunnel providers and see which works best.
    - Make regular backups of your world.
    - Google Colab is not designed to create Minecraft servers, but it can be done. Google Colab promises to work for 12 hours straight, however, it is possible that if no person is reviewing the page or using the console, basically if the page detects inactivity the process will end. The performance is approximately 12 GB of RAM, together with a processor with a power of 2.2 GHz and 2 threads, this is better than many paid hostings, but it doesn't have support and doesn't promise to be open always
    - It is not advisable to fill it with as many as plugins, which is more limited to this server than its own processor, it is not very good, any hosting for 12 USD can offer a higher quality server, if you are thinking of creating something for many users, it's much better.

    [![ForTheBadge built-with-love](http://ForTheBadge.com/images/badges/built-with-love.svg)](https://github.com/N-aksif-N)
  ''')

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
      st.markdown(f'<center>IP:&nbsp;&nbsp;{st.session_state.ip}</center>', unsafe_allow_html= True)
      st.write('')
      if st.button('Log out', use_container_width=True):
        sleep(2)
        user['user'][user_name]['server_in_use'] = ''
        dump(user, open(USER, 'w'))
        st.switch_page(st.Page('frontends/choose_server.py'))
      if st.button('Delete', use_container_width= True):
        Delete_server(server_name)
        user['user'][user_name]['server_in_use'] = ''
        dump(user, open(USER, 'w'))
        sleep(2)
        st.switch_page(st.Page('frontends/choose_server.py'))
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

elif choice == 'Worlds':

  if permission['world'] == True:
    if exists(f'{drive_path}/{server_name}/logs/latest.log') == False: ERROR('Running your minecraft server firsts')
    else:
      st.header('Worlds ')
      world_ = [i for i in listdir(f'{drive_path}/{server_name}') if 'world' in i]
      for world in world_:
        expander = st.expander(f'World: {world}')
        with expander:
          col1, col2, col3 = st.columns([6, 3.5, 2.5])
          with col2:
            if expander.button('Upload', use_container_width=True, key=f'expander_{world}'):
              seed = expander.text_input('Seed map: ', placeholder='Enter None to set upload file', key=f'expander_{world}_3', value='')
              uploaded_file = expander.file_uploader("Upload", label_visibility='collapsed', key=f'expender_{world}_4')
              if uploaded_file is not None:
                bytes_data = uploaded_file.getvalue()
                file_name = uploaded_file.name
                MAP(server_name= server_name, seed_map= seed, world_list=world_, world= world, content= bytes_data, file_name = file_name)
          with col3:
            if expander.button('Download', use_container_width=True, key=f'expander_{world}_2'):
              server_backup = expander.text_input('Server backup: ', placeholder='Enter None to set default backup', key=f'expander_{world}_5', value='')
              if server_backup != '': Backup(server_name= server_name, file_name=world, server_backup= server_backup)
  else:
    st.warning('You do not have permission to get access to this page.')

elif choice == 'Log':

  if permission['log viewing'] == True:
    if exists(f'{drive_path}/{server_name}/logs/latest.log'):
      st.header('Server Logs ')
      with open(f'{drive_path}/{server_name}/logs/latest.log', 'r') as f:
        content_ = f.read(); LOG('Try access to https://mclo.gs to see problems and the way to deal with.');
      content = st_ace(value=content_, readonly=True, language='plain_text', show_gutter=True)
    else: ERROR("Error: File didn't exists")
  else:
    st.warning('You do not have permission to get access to this page.')

elif choice == 'Software':

  if permission['software'] == True:
    SERVERJAR_ = ['vanilla', 'snapshot', 'purpur', 'paper', 'velocity', 'fabric', 'forge', 'arclight', 'mohist', 'banner']
    button_list = []
    st.header('Software')
    placeholder = st.empty()
    with placeholder.container(border=True):
      col1, col2, col3 = st.columns(3, vertical_alignment='top')
      with col1:
        for i in (0, 2, 5, 7):
          server_type = SERVERJAR_[i]
          button = st.button(f':green[{server_type}]', use_container_width= True)
          button_list.append(button)
      with col2:
        for i in (1, 3, 6, 8):
          server_type = SERVERJAR_[i]
          button = st.button(f':green[{server_type}]', use_container_width= True)
          button_list.append(button)
      with col3:
        st.button('', use_container_width=True, disabled=True, key= 'ex_1')
        server_type = SERVERJAR_[4]
        button = st.button(f':green[{server_type}]', use_container_width= True)
        button_list.append(button)
        st.button('', use_container_width=True, disabled=True, key= 'ex_2')
        server_type = SERVERJAR_[9]
        button = st.button(f':green[{server_type}]', use_container_width= True)
        button_list.append(button)
    server_type = ''; server_version = []
    for button in button_list:
      if button:
        server_version = SERVERSJAR(server_type= SERVERJAR_[button_list.index(button)], version='', all = True)
        server_type = SERVERJAR_[button_list.index(button)]
        sleep(1)
        placeholder.empty()
        sleep(1)
        SERVER_TYPE_2(server_type, server_version)
  else:
    st.warning('You do not have permission to get access to this page.')

elif choice == 'Share acess':

  if permission['owner'] == True:
    st.header('Share access')
    user = load(open(f'{path}/content/drive/My Drive/streamlit-app/user.txt'))
    dict_ = user['user']
    for user_ in dict_:
      if user_ != 'authtoken':
        with st.expander(f'User: {user_}'):
          world = False; server_settings = False; log_viewing = False; software = False; owner = False; console = False
          with st.container(border=True):
            col1, col2, col3 = st.columns(3, vertical_alignment="top")
            with col1:
              st.checkbox('Run/stop server', value=user['user'][user_]['permission']['console'], key=f'{user_}console')
              st.checkbox('Software', value=user['user'][user_]['permission']['software'], key=f'{user_}server_type')
            with col2:
              st.checkbox('Log viewing', value=user['user'][user_]['permission']['log viewing'], key=f'{user_}logs')
              st.checkbox('World', value=user['user'][user_]['permission']['world'], key=f'{user_}worlds')
            with col3:
              st.checkbox('Server settings', value=user['user'][user_]['permission']['server settings'], key=f'{user_}server_settings')
              st.checkbox('Administration', value=user['user'][user_]['permission']['owner'], key=f'{user_}administration')
            tmp, col2 = st.columns([9, 1], vertical_alignment="top")
            with col2:
              if st.button('Save', use_container_width=True, key= f'{user_}_save'):
                if st.session_state[f'{user_}console']: console = True
                if st.session_state[f'{user_}server_type']: software = True
                if st.session_state[f'{user_}logs']: log_viewing = True
                if st.session_state[f'{user_}worlds']: world = True
                if st.session_state[f'{user_}server_settings']: server_settings = True
                if st.session_state[f'{user_}administration']: owner = True
                user['user'][user_]['permission'] = {'console': console, 'software': software, 'log viewing': log_viewing, 'world': world, 'server settings': server_settings, 'owner': owner}
                dump(user, open(f'{path}/content/drive/My Drive/streamlit-app/user.txt', 'w'))
    col1, col2 = st.columns(2, vertical_alignment="bottom")
    with col1:
      user_name = st.text_input('User name: ', value='')
    with col2:
      if st.button('Create', use_container_width=True):
        if user_name != '':
          if user_name in user['user']:
            ERROR('This username already exists')
          else:
            user['user'][user_name] = {'permission': {'console': False, 'software': False, 'log viewing': False, 'world': False, 'server settings': False, 'owner': True}, 'user_id': [''], 'server_in_use': ''}
            dump(user, open(f'{path}/content/drive/My Drive/streamlit-app/user.txt', 'w'))
  else:
    st.warning('You do not have permission to get access to this page.')

else:
  st.write('Are comming')
