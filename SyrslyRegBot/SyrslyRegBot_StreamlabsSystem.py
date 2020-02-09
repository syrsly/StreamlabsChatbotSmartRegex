#---------------------------
#   Import Libraries
#---------------------------
import os
import codecs
import ast
import sys
import json
import re
import random
# import requests
sys.path.append(os.path.join(os.path.dirname(__file__), "lib")) #point at lib folder for classes / references

import clr
clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")

#---------------------------
#   [Required] Script Information
#---------------------------
ScriptName = "SyrslyRegBot"
Website = "https://www.syrsly.com"
Description = "Use regex to manage commands and responses to commands"
Creator = "Syrsly"
Version = "1.0.0"

#---------------------------
#   Settings Handling
#---------------------------
class CpSettings:
	def __init__(self, settingsfile=None):
		try:
			with codecs.open(settingsfile, encoding="utf-8-sig", mode="r") as f:
				self.__dict__ = json.load(f, encoding="utf-8")
		except:
			self.Cooldown = 10
			self.Permission = "everyone"
			self.Info = ""

	def Reload(self, jsondata):
		self.__dict__ = json.loads(jsondata, encoding="utf-8")

	def Save(self, settingsfile):
		try:
			with codecs.open(settingsfile, encoding="utf-8-sig", mode="w+") as f:
				json.dump(self.__dict__, f, encoding="utf-8")
			with codecs.open(settingsfile.replace("json", "js"), encoding="utf-8-sig", mode="w+") as f:
				f.write("var settings = {0};".format(json.dumps(self.__dict__, encoding='utf-8')))
		except:
			Parent.Log(ScriptName, "Failed to save settings to file.")


#---------------------------
#   Define Global Variables
#---------------------------
global cpSettingsFile
cpSettingsFile = ""
global cpScriptSettings
cpScriptSettings = CpSettings()
global RegexArray
RegexArray = []
global message_pieces
message_pieces = []

global cpRegexPath
cpRegexPath = os.path.abspath(os.path.join(os.path.dirname(__file__), "regex.conf")).replace("\\", "/")
global cpJokePath
cpJokePath = os.path.abspath(os.path.join(os.path.dirname(__file__), "jokes.conf")).replace("\\", "/")

#---------------------------
#   [Required] Initialize Data (Only called on load)
#---------------------------
def Init():

    #   Create Settings Directory
    directory = os.path.join(os.path.dirname(__file__), "Settings")
    if not os.path.exists(directory):
        os.makedirs(directory)

    #   Load settings
    global cpSettingsFile
    cpSettingsFile = os.path.join(os.path.dirname(__file__), "Settings\settings.json")
    global cpScriptSettings
    cpScriptSettings = CpSettings(cpSettingsFile)

    updateUi()

    LoadConfigFile()

#---------------------------
#   [Required] Execute Data / Process messages
#---------------------------
def Execute(data):
    #   only handle messages from chat
    if data.IsChatMessage() and data.IsFromTwitch() and not data.IsWhisper():

        found = False
        regex = ''
        obj = {}
        #   Parse chat line for any given key word or phrase from the conf file
        for item in RegexArray:
			# item[0] is the regex pattern
			regex = item[0]
			# searchRegex = re.compile('(a|r$)').search
			message_pieces_temp = re.search(regex, data.Message)
			if message_pieces_temp:
				found = True
				message_pieces = message_pieces_temp.groups()
				Parent.Log(ScriptName,'message_pieces_temp: '+repr(message_pieces_temp))
				Parent.Log(ScriptName,'message_pieces_temp.groupdict(): '+repr(message_pieces_temp.groupdict()))
				Parent.Log(ScriptName,'message_pieces_temp.groups(): '+repr(message_pieces_temp.groups()))
				Parent.Log(ScriptName,'message_pieces: '+repr(message_pieces))
				obj = item[1]
				Parent.Log(ScriptName,'obj: '+repr(obj))
				break

        if found:
			#   Check if the command is not on cooldown and the user has permission to use the command
			# regex = re.search("^/.*/$", token).group(0).strip('/')
			# rename all commands to use dynamic username as well as command name
			Parent.Log(ScriptName,'obj command: '+repr(obj['command']))
			if not Parent.IsOnUserCooldown(ScriptName, ''.join(obj['command']), data.User) and not Parent.IsOnCooldown(ScriptName, ''.join(obj['command'])) and Parent.HasPermission(data.User, obj['permission'], obj['users']):
				Parent.Log(ScriptName,'message_pieces in if found: '+repr(message_pieces))
				response = Parse(obj['response'], data.User, data.Message, list(message_pieces))
				Parent.SendStreamMessage(response)    # Send your message to chat
				if (obj['cooldowntype'] == 'global'):
					Parent.AddCooldown(ScriptName, obj['command'], obj['cooldown'])  # Put the command on global cooldown
				else:
					Parent.AddUserCooldown(ScriptName,obj['command'],data.User,obj['cooldown'])  # Put the command on user-specific cooldown

#---------------------------
#   [Required] Tick method (Gets called during every iteration even when there is no incoming data)
#---------------------------
def Tick():
    return

#---------------------------
#   [Optional] Parse method (Allows you to create your own custom $parameters)
#---------------------------
def Parse(parseString, username, message, message_pieces):
	temp_username = username.lower()
	Parent.Log(ScriptName,'Parse: message_pieces: '+repr(message_pieces))
	if len(message_pieces)>0:
		Parent.Log(ScriptName,'Parse: message_pieces[0] exists: '+message_pieces[0])
		parseString = parseString.replace('$insult', random.choice(['$resp1 is such a loser! Gawd!','If $resp1 was a chicken, it would pick up corn with its ass.','$resp1\'s mother is so fat, the recursive function computing her mass causes a stack overflow.','If the stream goes offline, it\'s $resp1\'s fault. Kappa','$resp1 could not pour water out of a boot if the instructions were written on the heel.','Somewhere, a tree is working really hard to replace the oxygen $resp1 used. They should say sorry.','$resp1 is bright as a black hole and twice as dense!','$resp1 has the subtly of a brick and the depth of a shot glass','$resp1 should try eating some makeup, at least they would be pretty on the inside.']))
		parseString = parseString.replace('$resp1', message_pieces[0])
	if len(message_pieces)>1:
		Parent.Log(ScriptName,'Parse: message_pieces[1] exists: '+message_pieces[1])
		parseString = parseString.replace('$resp2', message_pieces[1])
	if (parseString.find('$joke') != -1):
		# response = requests.get("https://icanhazdadjoke.com/nightbot")
		Parent.Log(ScriptName,'found joke')
		response = Parent.GetRequest("https://icanhazdadjoke.com/nightbot",{})
		Parent.Log(ScriptName,'response: '+repr(response))
		value = ast.literal_eval(response)
		parseString = parseString.replace('$joke', value['response'])
	parseString = parseString.replace('$message', message)
	parseString = parseString.replace('$random_comeback', random.choice(['Double stamped! No takebacksies! You can\'t triple stamp a double stamp!','DansGame','The whole world knows that! Where you been all this time?!','MaxLOL']))
	parseString = parseString.replace('$random_emote', random.choice(['CorgiDerp','DansGame','BrokeBack','CrreamAwk','MaxLOL']))
	return parseString

#---------------------------
#   [Optional] Reload Settings (Called when a user clicks the Save Settings button in the Chatbot UI)
#---------------------------
def ReloadSettings(jsonData):
    # Execute json reloading here
    cpScriptSettings.Reload(jsonData)
    cpScriptSettings.Save(cpSettingsFile)
    updateUi()
    LoadConfigFile()
    return

#---------------------------
#   [Optional] Unload (Called when a user reloads their scripts or closes the bot / cleanup stuff)
#---------------------------
def Unload():
    return

#---------------------------
#   [Optional] ScriptToggled (Notifies you when a user disables your script or enables it)
#---------------------------
def ScriptToggled(state):
    return

def EditConfigFile():
    os.startfile(cpRegexPath)
    return

def LoadConfigFile():
    try:
        with codecs.open(cpRegexPath, encoding="utf-8-sig", mode="r") as f:
            matches = []
            for line in f:
                line = line.strip()         # remove leading and trailing spaces
                if len(line) > 0:           # ignore empty lines
                    if line[0] != '#':      # ignore comment lines
						tokens = list(enumerate(line.split(" ")))
						regex = ''
						response = ''
						cooldown = -1
						permission = ''
						cooldowntype = ''
						users = ''
						command_name = str(tokens.pop(0)) # first element in list is the command name no matter what, so remove it before parsing further
						Parent.Log(ScriptName, "command_name: "+repr(command_name))
						Parent.Log(ScriptName, "everything else: "+repr(tokens))
						for i, token in tokens:
							Parent.Log(ScriptName, "next element in for loop: "+repr(token))
							try:
								if re.search("^/.*/$", token):
									regex = re.search("^/.*/$", token).group(0).strip('/')
									Parent.Log(ScriptName, "found regex: "+repr(regex))
								elif re.search("^-->/$", token):
									regex = re.search("^/-->/$", token).group(0).strip('/-->').strip('/')
									Parent.Log(ScriptName, "found regex: "+repr(regex))
								elif token[0] == '"' and not response:
									# if a response is already found this token is part of the response and already handled,
									words = []
									words.append(token)
									Parent.Log(ScriptName, "found remaining words list: "+repr(list(tokens[i:])))
									for word in list(tokens[i:]):
										Parent.Log(ScriptName, "found word: "+repr(word))
										words.append(word[1])
									text = " ".join(words)
									response = text[1:-1]   # remove first and last " rest are nested and part of response
									Parent.Log(ScriptName, "found response: "+repr(response))
									break   # since the response is the last element of the line, we are done here
								elif re.search("^\d+$", token) and cooldown < 0:
									cooldown = int(token) if int(token) >= 0 else 0
								elif token in ['everyone','moderator','subscriber','editor', 'user_specific'] and not permission:
									# if permission is already set, this token is part of the response
									permission = token
								elif token in ['global', 'user'] and not cooldowntype:
									cooldowntype = token
								elif re.search("^(\w+,?)+$", token) and permission == 'user_specific' and not users:
									# if the user list is already set, this token is part of the response
									users = token.replace(",", " ")
							except Exception as err:
								Parent.Log(ScriptName, "Error while parsing line: {0} - {1}".format(line, err))

						if not regex or not response:
							Parent.Log(ScriptName, "Error Parsing line - no regex or response found: {}".format(line))
							continue

						obj = {'response': response}
						obj['command'] = command_name
						obj['cooldown'] = cooldown if cooldown >= 0 else cpScriptSettings.Cooldown
						obj['permission'] = permission if permission else cpScriptSettings.Permission
						obj['cooldowntype'] = cooldowntype if cooldowntype else 'user'
						obj['users'] = users if users else cpScriptSettings.Info

						matches.append((regex, obj))

            global RegexArray
            RegexArray = matches

    except Exception as err:
        Parent.Log(ScriptName, "Could not load Regex file: {0}".format(err))

    try:
        with codecs.open(cpJokePath, encoding="utf-8-sig", mode="r") as jokefile:
			global numJokes
			numJokes = 0
			jokes = []
			for line in jokefile:
				line = line.strip()         # remove leading and trailing spaces
				if len(line) > 0:           # ignore empty lines
					if line[0] != '#':      # ignore comment lines
						numJokes+=1
						jokes.append(line)
			Parent.Log(ScriptName, "Number of jokes available: ".format(numJokes))
    except Exception as err:
        Parent.Log(ScriptName, "Could not load jokes file: {0}".format(err))


def updateUi():
    ui = {}
    UiFilePath = os.path.join(os.path.dirname(__file__), "UI_Config.json")
    try:
        with codecs.open(UiFilePath, encoding="utf-8-sig", mode="r") as f:
            ui = json.load(f, encoding="utf-8")
    except Exception as err:
        Parent.Log(ScriptName, "{0}".format(err))

    # update ui with loaded settings
    ui['Cooldown']['value'] = cpScriptSettings.Cooldown
    ui['Permission']['value'] = cpScriptSettings.Permission
    ui['Info']['value'] = cpScriptSettings.Info

    try:
        with codecs.open(UiFilePath, encoding="utf-8-sig", mode="w+") as f:
            json.dump(ui, f, encoding="utf-8", indent=4, sort_keys=True)
    except Exception as err:
        Parent.Log(ScriptName, "{0}".format(err))
