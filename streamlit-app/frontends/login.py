import streamlit as st
from backends.settings import ERROR, path, USER
from random import choices
from string import ascii_letters
from json import load, dump
from time import sleep

user = load(open(USER)); uid = dict(st.context.headers)
del uid['Sec-Websocket-Key']
uid = str(uid)
if user != {"choose": True, "user": {"authtoken": ""}} != []:
  for user_ in user['user']:
    if user_ != 'authtoken':
      if uid in user['user'][user_]['user_id']: st.switch_page(st.Page('frontends/choose_server.py'));

container = st.container()
if user == {"choose": True, "user": {"authtoken": ""}}: text = 'Sign up'
else: text = 'Log in'
container.title(text)
container.text_input('Username: ', value='', key= 'user_name')
tmp, col2 = st.columns([9, 1], vertical_alignment='top')
with col2:
  st.button(text, use_container_width=True, key=f'{text}_btn')

if st.session_state[f'{text}_btn'] is True and st.session_state['user_name'] != '':
  if user == {"choose": True, "user": {"authtoken": ""}}:
    authtoken = ''.join(choices(ascii_letters, k=20))
    st.write(f'Your owner authtoken: {authtoken}')
    user['user']['authtoken'] = authtoken
    user['user'][st.session_state['user_name']] = {'permission': {'console': False, 'software': False, 'log viewing': False, 'players': False, 'plugins/mods': False, 'world': False, 'server settings': False, 'owner': True}, 'user_id': [uid], 'server_in_use': ''}
    dump(user, open(USER, 'w'))
    sleep(3)
    st.switch_page(st.Page('frontends/choose_server.py'))
  elif st.session_state['user_name'] in user['user'].keys():
    if user['user'][st.session_state['user_name']]['permission']['owner'] == True:
      container.text_input('Your authtoken: ', key = 'authtoken')
      if st.session_state['authtoken'] == user['user']['authtoken']:
        if uid not in user['user'][st.session_state['user_name']]['user_id']:
          user['user'][st.session_state['user_name']]['user_id'].append(uid)
        dump(user, open(USER, 'w'))
        sleep(1)
        st.switch_page(st.Page('frontends/choose_server.py'))
    else: ERROR('Invalid username or password')
  else: ERROR('Invalid username or password')
