
**New Features:**

Bug fixed (java error)

Get mod/plugin (modrinth), modpack (curseforge - intested)

Server properties, server MOTD, and server icon configuration.

Logs View.

File Backup.

Expanded software (forge, fabric, vanilla, snapshot, paper, purpur)

[Discord Support](https://discord.gg/uCHcV3SAbs)


**Note:** 

This project followed the MIT. Before looking closer, please make sure to see [the original file](https://github.com/thecoder-001/MineColab/blob/master/MineColab.ipynb)


<p align="center"><a href="https://github.com/thecoder-001/MineColab"><img src="https://github.com/thecoder-001/MineColab/blob/master/Logo.png" alt="Logo" height="80"/></a></p>
<h1 align="center">MineColab</h1>
<p align="center">Run Minecraft Server on Google Colab</p>
<a href="https://colab.research.google.com/drive/1XaKGzktNHVr3o2rf4SuwlkuwDmQapYal?usp=sharing" target="_parent"><img align="right" src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>

## :hear_no_evil:  First of all, what is Mine Colab [Improved]?

Mine Colab [Improved] is an alternative [Minecolab project](https://github.com/thecoder-001/MineColab) which helps to build minecraft server on your own Gdrive. It is easier to use and more flexible edited. This project is suited for mainly [google colab](https://colab.research.google.com) (a free service based on [jupyter notebook](https://jupyter.org/) and [ubuntu](https://ubuntu.com) os), though this can be appied on other project like [jupyter lab](https://jupyter.org/try-jupyter/lab/), [deepnote](https://deepnote.com/), etc. 

## :moneybag:  Can Minecolab server online 24/7?

Of course, it's able to do it but with a little hard works. Google colab is a free service but it is not suited for 24/7 so you can use deepnote instead. Or if you wanna use google colab you may need some tricks or friends to make the web online and accept the capcha manually.

## :page_with_curl: Instructions
1. Open the notebook in google colab.
3. Read through the notebook, most of the code is self explanatory. Run the cells which are useful for your use-case.

1. Run the first cell which runs the Minecraft server.
2. Now you have three options. You can either use ngrok, playit.gg or cloudflare's argo. Ngrok is easy to setup and doesn't requires anything to be installed by the clients but it can often be quite unreliable. Argo doesn't have such limitations but requires a bit more work. Playit.gg's implementation is unpolished at the moment (debug log spam) but offers convenient static subdomains.
  * Ngrok:
    Change `tunnel_service` variable and follow the prompts.
  * Cloudflare argo:
    - If 'Your free tunnel has started!' notification appears => Done.
    - Access to your server: 
    1. Download [Cloudflared client](https://github.com/cloudflare/cloudflared/releases/).
    2. Launch the binary with `<your cloudflared file name> access tcp --hostname <tunnel_address> --url 127.0.0.1:25565` (note: tunnel_address is your address which has been set on your cloudflare)
    4. Finally, connect to `127.0.0.1:25565` from the minecraft client located in that machine.
  * Playit.gg:
    Change `tunnel_service` variable, ignore the debug output _(todo:fix)_ and follow the prompts.

## :zap:  So, how does it actually work?
As Google Colab is a VM running Ubuntu server as base OS, it can be easily used as a Minecraft server. Here are the steps which the notebook performs to setup the server:
1. Update the system's apt cache.
2. Install Openjdk-16 (Java) through apt-get.
3. Mount Google Drive to access the minecraft folder (Drive is used here to provide persistent storage).
4. Setup Argo/ngrok/playit Tunnel (Opening a tunnel at port 25565) depending on the `tunnel_service` variable.
5. Change directory to the minecraft-server folder on google drive ("Minecraft-server" is the default, located in the root directory of my Google Drive.)
6. List/Print the file list on the screen to indicate succesful directory change.
7. Startup the Minecraft server (with optimized JVM parameters from [Aikar's guide)](https://aikar.co/2018/07/02/tuning-the-jvm-g1gc-garbage-collector-flags-for-minecraft/)

## 🐛 Found a bug?
Report report the bug by creating a new issue and use this helpful [issue template](https://github.com/thecoder-001/MineColab/issues/new?assignees=&labels=bug&template=bug_report.md&title=%5BBUG%5D).

Or suggest a new feature using this [template](https://github.com/thecoder-001/MineColab/issues/new?assignees=&labels=enhancement&template=feature_request.md&title=%5BFeature+Request%5D).

## 👍 Tips
- If something does not work, try using a VPN like [windscribe](https://windscribe.com) before opening an issue.
- Switch between the three different tunnel providers and see which works best for you.
- Make regular backups of your world.

[![ForTheBadge built-with-love](http://ForTheBadge.com/images/badges/built-with-love.svg)](https://github.com/thecoder-001)

