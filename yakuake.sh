#!/bin/bash

# The documentation is in qdbusviewer. To install: sudo apt-get install qt5-default qttools5-dev-tools

flag=0

# keyvalue: key is a tab name and value is a program name
# TODO: read json or xml key value
# ["mosca"]="/home/smartpolitech/ACHO/mosca/mosca.sh" 
declare -A dictOfComponents=( ["telegram"]="/home/smartpolitech/ACHO/telegram/achobot.py" ["tv"]="/home/smartpolitech/ACHO/tv/tv.py" ["lights"]="/home/smartpolitech/ACHO/luces/light_bulbs.py" ["ASR"]="/home/smartpolitech/ACHO/asr/achoASR.py" ["persiana"]="/home/smartpolitech/ACHO/persiana/persiana.py" ["tts"]="/home/smartpolitech/ACHO/tts/tts.py" ["nlp"]="/home/smartpolitech/ACHO/nlp/nlp.py" ["avatar"]="/home/smartpolitech/ACHO/avatar/avatar.py")

for component in "${!dictOfComponents[@]}"
do
        #This is for split the sessionIDList string of the tabs in a list (yeah!)
        sessionList=$(echo `qdbus org.kde.yakuake /yakuake/sessions org.kde.yakuake.sessionIdList` | tr "," "\n")
        for sessionID in $sessionList
        do
                sessionName=`qdbus org.kde.yakuake /yakuake/tabs org.kde.yakuake.tabTitle $sessionID`
                if [ "$sessionName" = "$component" ]; then
                        flag=1
                        session=`expr $sessionID + 1`
                        processID=`qdbus org.kde.yakuake /Sessions/$session org.kde.konsole.Session.processId`
                        fourGroundProcessID=`qdbus org.kde.yakuake /Sessions/$session org.kde.konsole.Session.foregroundProcessId`
                        # If the ids are the same, the user process is death
                        if [ "$processID" = "$fourGroundProcessID" ]; then
                                qdbus org.kde.yakuake /yakuake/sessions org.kde.yakuake.runCommand ${dictOfComponents["$component"]}
                        fi
                #ELSE TODO: LAUNCH EXCEPTION!!
                fi
        done
        if [ $flag == 0 ]; then
                qdbus org.kde.yakuake /yakuake/sessions org.kde.yakuake.addSession
		sess=`qdbus org.kde.yakuake /yakuake/sessions org.kde.yakuake.activeSessionId`
		qdbus org.kde.yakuake /yakuake/tabs org.kde.yakuake.setTabTitle $sess $component
		qdbus org.kde.yakuake /yakuake/sessions org.kde.yakuake.runCommand "python ${dictOfComponents["$component"]}"
                sleep 1
        fi
done
