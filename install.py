import os
import sys
from os import environ

userHomeDir = os.path.expanduser("~")
activeUserName = os.path.split(userHomeDir)[-1]

def askYesNo(question: str) -> bool:
    YesNoAnswer = ""
    while not YesNoAnswer.startswith(("Y", "N")):
        YesNoAnswer = input(f"{question}: ").upper()
    if YesNoAnswer.startswith("Y"):
        return True
    return False


def updateTextFile(fileName, originalText, newText):

    with open(fileName,'r') as f:
        filedata = f.read()

    newdata = filedata.replace(originalText, newText)

    with open(fileName, 'w') as f:
        f.write(newdata)


def installVstats(vstatsToken) -> None:
    # Check if it exists already
    if os.path.isdir(f"{userHomeDir}/harmony_node_stats"):
        question = askYesNo("* You already have vstats installed, would you like to update & reinstall vstats? (YES/NO)")
        if question is False:
            raise SystemExit(0)
        else:
            # Start install by stopping and wipe for re-install if yes
            os.system("sudo service harmony_node_stats stop")
            os.system(f"sudo rm -r {userHomeDir}/harmony_node_stats")
        
    # Install it bud, pull git repo
    os.chdir(f"{userHomeDir}")
    os.system("git clone https://github.com/FortuneV13/harmony_node_stats")
    os.chdir(f"{userHomeDir}/harmony_node_stats")
    # setup python stuff
    os.system("sudo apt install python3-pip -y")
    os.system("pip3 install -r requirements.txt")
    # customize config file
    os.system("cp config.example.py config.py")
    updateTextFile(f"{userHomeDir}/harmony_node_stats/config.py", 'VSTATS_TOKEN=""', f'VSTATS_TOKEN="{vstatsToken}"')
    if os.path.isdir(f"{userHomeDir}/harmony"):
        updateTextFile(f"{userHomeDir}/harmony_node_stats/config.py", '"harmony_folder":"/home/serviceharmony/harmony"', f'"harmony_folder":"{userHomeDir}/harmony"')
    else:
        if os.path.isfile(f"{userHomeDir}/harmony"):
            updateTextFile(f"{userHomeDir}/harmony_node_stats/config.py", '"harmony_folder":"/home/serviceharmony/harmony"', f'"harmony_folder":"{userHomeDir}"')
    # Do service stuff here
    if activeUserName == 'root':
        os.system(
        f"sudo cp {userHomeDir}/harmony_node_stats/util/harmony_node_stats.service . && sed -i 's/home\/serviceharmony/{activeUserName}/g' 'harmony_node_stats.service' && sed -i 's/serviceharmony/{activeUserName}/g' 'harmony_node_stats.service' && sudo mv harmony_node_stats.service /etc/systemd/system/harmony_node_stats.service && sudo chmod a-x /etc/systemd/system/harmony_node_stats.service && sudo systemctl enable harmony_node_stats.service && sudo service harmony_node_stats start"
    )
    else:
        os.system(
        f"sudo cp {userHomeDir}/harmony_node_stats/util/harmony_node_stats.service . && sed -i 's/serviceharmony/{activeUserName}/g' 'harmony_node_stats.service' && sudo mv harmony_node_stats.service /etc/systemd/system/harmony_node_stats.service && sudo chmod a-x /etc/systemd/system/harmony_node_stats.service && sudo systemctl enable harmony_node_stats.service && sudo service harmony_node_stats start"
    )
    return
    

def getToken():
    if len(sys.argv) > 1:
        vstatsToken = sys.argv[1]
    else:
        question = askYesNo(
            f"* No token found, please run /token on vStats Bot to obtain your token. Would you like to enter one now? (YES/NO)"
        )
        if question:
            vstatsToken = input(
                f"* Please input your vStats token here: "
            )
        else:
            raise SystemExit(0)
    return vstatsToken


if __name__ == '__main__':
    os.system("clear")
    # Check for argument token or ask for one!
    vstatsToken = getToken()
    
    # install once we have the info to customize
    installVstats(vstatsToken)

    # Goodbye!
    print("****")
    print("\n*\n* Installer has finished, you should have a ping waiting on vStats if everything was input correctly\n* You can also run `sudo service harmony_node_stats status` to verify your service is online and running!\n*")
    print("****")
