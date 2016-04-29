import os

options = {"commands":
		{
		  "newsession":"qdbus org.kde.yakuake /yakuake/sessions org.kde.yakuake.addSession",
		  "session":"sess=`qdbus org.kde.yakuake /yakuake/sessions org.kde.yakuake.activeSessionId`",
		  "runcommand":"qdbus org.kde.yakuake /yakuake/sessions org.kde.yakuake.runCommand",
		  "tab":"qdbus org.kde.yakuake /yakuake/tabs org.kde.yakuake.setTabTitle $sess",
		  "sleep":"sleep 1"
		}
	  }


commandsPossible = {
		"rcis":'rcis /home/robocomp/robocomp/files/innermodel/hexapod.xml',
		"storm":"rcnode",
		"Joystick": ['cd /home/robocomp/robocomp/components/robocomp-robolab/components/joystickpublishComp', 'bin/joystickpublishcomp --Ice.Config=config'],
		"other": ['list','of','commands']
		}




os.system(options["commands"]["newsession"])
os.system(options["commands"]["session"])
os.system(options["commands"]["runcommand"]+" "+commandsPossible["storm"])
os.system(options["commands"]["tab"]+" "+"storm")
os.system(options["commands"]["sleep"])
