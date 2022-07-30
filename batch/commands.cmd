@echo off
@echo. 
@echo [92mSystem [0m
@echo -------------------------------
@echo [1m^bounce [0m - reboot the computer
@echo [1m^poweroff [0m - shut down the computer
@echo [1m^commands [0m - show this help
@echo [1m^copyfile [0m - starts IU for mass copying files over a network with resumability to account for unreliable connections
@echo [1m^files [0m - start file manager
@echo [1m^sudo [0m [36m^<app name ^| command^> ^[options/switches^] [0m - run app/command as Administrator
@echo [1m^message [0m [36m^<title^> ^<text^> [0m - shows Windows pop-up message with supplied title and text
@echo [1m^win10colors [0m - shows the colors and codes for batch files like this one
@echo. 
@echo [92mApp Mangament [0m
@echo -------------------------------
@echo [1m^install [0m [36m^<app name ^| packages.config^> ^[app2...appN^] ^[options/switches^] [0m - use Chocolatey to install application(s)
@echo [1m^uninstall [0m [36m^<app name ^| all^> ^[app2...appN^] ^[options/switches^] [0m - use Chocolatey to remove application(s)
@echo [1m^upgrade [0m [36m^<app name ^| all^> ^[app2...appN^] ^[options/switches^] [0m - use Chocolatey to upgrade application(s)
@echo [1m^list-apps [0m - list apps installed with Chocolatey
@echo. 
@echo [92m^WSL [0m
@echo -------------------------------
@echo [1m^kill-linux [0m - stop any running Linux instances
@echo [1m^linux-status [0m - get the status of WSL Linux instances
@echo. 
@echo [92m^Utility [0m
@echo -------------------------------
@echo [1m^timezone [0m - launches time zone translation app
@echo [1m^tts [0m - launches simple UI for reading text using text-to-speech
@echo.
@echo on