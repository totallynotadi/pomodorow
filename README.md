# pomodorow
---

A python script to accompany your pomodorow sessions with a timer an lofi music combined with soothing ambience. Fetches music form lofi playlists on youtube links to which are sspecified in the configurations file.
There also exist bell sounds to notify the user about the start and beginning of the work/break times with some sweet bell sounds, notifications can be enabled optionally

features can be toggled and configured from the configuration files which allows the user to configure some music profiles to play and change the break/work session durations

## installaion

clone this repository form the ul https://github.com/addyett/pomodorow 
or download the zip file for the repo and unzip it

run the setup.py file to install all the dependancies

## usage

just run the pomodorow.py file and you're in for good time

default configs will be applied unless specified by the user

## configuration

music profiles - a user can choose what music to play during their pomodorow sessions, the links to all the videos need to be specified with a name to that profile in a similar way as the defalut profile is configured. then the user can choose the profile to play mmusic to play from. (the default profile consists of lofi music)

ambience - a boolean value to specify wether or not to play the ambient sounds.

work duration - an integer value to specify the duration for a work session
break duration - an integer value to specify the break duration after every work session.

notification - a boolean value to specify wether or not to send system notifications to notify the user about work/break times

bell sounds - a boolean value to wether play bell sounds afterr every work/break session in order to notify the user.

## runtime commands

users can also control the playback of the music in cases when one needs to go out for urgent chores.
some commmands that exist are:

pusse - sets the state to pusesd to pause all the music 
play - unpauses the state of the player to start the player after pausin
rewind - rewinds the currently playing song in the player queue
skip - skip the current track and start playing the next track
