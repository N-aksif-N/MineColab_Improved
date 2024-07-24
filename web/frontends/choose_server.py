import streamlit as st
from os import listdir
from os.path import exists, isdir
from json import load, dump
from time import sleep
from backends.settings import ERROR, COLABCONFIG_LOAD, PROGRESS, SERVERCONFIG, drive_path
from time import sleep

pages = load(open('/content/drive/MyDrive/streamlit-app/user.txt'))
if pages['choose'] == True:
  st.header('Choose server', divider= 'rainbow')
  serverconfig = load(open(SERVERCONFIG))
  if listdir(drive_path) == []:
    ERROR('Create your server firsts')
    sleep(2)
    st.switch_page(st.Page('frontends/create_page_1.py'))
  else:
    st.subheader('\nAivailable server:\n')
    server_list = []; drive_dir = listdir(drive_path); server = ''; drive_dir.remove('logs'); drive_dir.remove('server_list.txt')
    container = st.container(border=True)
    for server in drive_dir:
      colabconfig = COLABCONFIG_LOAD(server);
      if colabconfig['server_type'] != False:
        button = container.button(f':blue[{server}] - {colabconfig["server_type"].capitalize()} - {colabconfig["server_version"]} ', use_container_width= True)
        server_list.append(button)
    col1, col2 = st.columns(2, vertical_alignment="bottom")
    with col1:
      if st.button('New Server', use_container_width= True): st.switch_page(st.Page('frontends/create_page_1.py'))
    with col2:
      if st.button('Use Default', use_container_width= True): st.switch_page(st.Page('frontends/main_page.py'))
    default = st.button("Change visibility", use_container_width= True)
    if default:
      pages['choose'] = False
      ERROR(f' This is a warning after you choose this the visibility will change to ', str(pages['choose']).lower())
      dump(pages, open('/content/drive/MyDrive/streamlit-app/pages.txt', 'w'))
      sleep(5)
    for button in server_list:
      if button: server = drive_dir[server_list.index(button)]; break
      else: server = ''
    if server != '':
      if exists(f'{drive_path}/{server}') == False: ERROR('You choose the wrong server choose again')
      if server in serverconfig['server_list']: serverconfig['server_in_use'] = server
      else: serverconfig['server_list'].append(server); serverconfig['server_in_use'] = server
      dump(serverconfig, open(SERVERCONFIG, 'w'))
      sleep(1)
      if 'server_in_use' not in st.session_state:
        st.session_state['server_in_use'] = server
      st.session_state['server_in_use'] = server
      st.write('')
      PROGRESS()
      st.switch_page(st.Page('frontends/main_page.py'))
else: st.switch_page(st.Page('frontends/main_page.py'))
