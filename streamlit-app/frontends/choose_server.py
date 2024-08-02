import streamlit as st
from os import listdir
from os.path import exists, isdir
from json import load, dump
from time import sleep
from backends.settings import ERROR, COLABCONFIG_LOAD, PROGRESS, SERVERCONFIG, drive_path, path, USER
from time import sleep

pages = load(open(USER)); uid = dict(st.context.headers); user_name = ''
del uid['Sec-Websocket-Key']
uid = str(uid)
for user_ in pages['user']:
  if user_ != 'authtoken':
    if uid in pages['user'][user_]['user_id']:
      if pages['user'][user_]['server_in_use'] != '': st.switch_page(st.Page('frontends/main_page.py'))
      user_name = user_; break
if user_name == '': st.switch_page(st.Page('frontends/login.py'))
serverconfig = load(open(SERVERCONFIG))
drive_dir = listdir(drive_path); drive_dir.remove('serverconfig.txt');  drive_dir.remove('logs');
if drive_dir == []:
  ERROR('Create your server firsts')
  sleep(2)
  st.switch_page(st.Page('frontends/create_page_1.py'))

if pages['choose'] == True:

  st.header('Choose server', divider= 'rainbow')
  st.subheader('\nAivailable server: \n')
  server_list = []; server = ''
  container = st.container(border=True)
  for server in drive_dir:
    colabconfig = COLABCONFIG_LOAD(server)
    if colabconfig['server_type'] != False:
      button = container.button(f':blue[{server}] - {colabconfig["server_type"].capitalize()} - {colabconfig["server_version"]} ', use_container_width= True)
      server_list.append(button)
  st.subheader('\nExtra options: \n')
  col1, col2 = st.columns(2, vertical_alignment="bottom")
  with col1:
    if st.button('New Server', use_container_width= True): st.switch_page(st.Page('frontends/create_page_1.py'))
  with col2:
    if st.button('Use Default', use_container_width= True):
      if pages['user'][user_name]['server_in_use'] == '':
        pages['user'][user_name]['server_in_use'] = drive_dir[0]
        dump(pages, open(USER, 'w'))
        sleep(1)
      st.switch_page(st.Page('frontends/main_page.py'))
  if st.button("Change visibility", use_container_width= True):
    pages['choose'] = False
    ERROR(f' This is a warning after you choose this the visibility will change to ', str(pages['choose']).lower())
    dump(pages, open(USER, 'w'))
    sleep(2)

  for button in server_list:
    if button: server = drive_dir[server_list.index(button)]; break
    else: server = ''

  if server != '':
    if exists(f'{drive_path}/{server}') == False: ERROR('You choose the wrong server choose again')
    if server not in serverconfig['server_list']: serverconfig['server_list'].append(server)
    dump(serverconfig, open(SERVERCONFIG, 'w'))
    pages['user'][user_name]['server_in_use'] = server
    dump(pages, open(USER, 'w'))
    sleep(1)
    st.write('')
    PROGRESS()
    st.switch_page(st.Page('frontends/main_page.py'))
else:
  if pages['user'][user_name]['server_in_use'] == '':
    pages['user'][user_name]['server_in_use'] = drive_dir[0]
    dump(pages, open(USER, 'w'))
    sleep(1)
  st.switch_page(st.Page('frontends/main_page.py'))
