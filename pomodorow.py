from multiprocessing import Process
import threading
import random
import time
import re
import os

from ffpyplayer.player import MediaPlayer
import playsound
import requests
import plyer
from youtube_dl import YoutubeDL

global streams
global ambience
streams = ['https://www.youtube.com/watch?v=grBFMP3HDZA', 'https://www.youtube.com/watch?v=RDbvC5I9wtw', 'https://www.youtube.com/watch?v=sca4VG9b0NY', 
           'https://www.youtube.com/watch?v=GTZROPwG3Pk', 'https://www.youtube.com/watch?v=o5Gv4_FdcYs', 'https://www.youtube.com/watch?v=_ITiwPMUzho',
           'https://www.youtube.com/watch?v=8TlQMC-Njrs', 'https://www.youtube.com/watch?v=O3UenuM-SYY', 'https://www.youtube.com/watch?v=Vdxp5H2vOdU',
           'https://www.youtube.com/watch?v=X9EY84-Hzls', 'https://www.youtube.com/watch?v=q55qNEKQLG0', 'https://www.youtube.com/watch?v=KTRRp9N7BTc',
           'https://www.youtube.com/watch?v=rY0mSSOnkL0', 'https://www.youtube.com/watch?v=eGy-E8-cTjQ', 'https://www.youtube.com/watch?v=t_i_Dq2GjAI']
ambience =['https://www.youtube.com/watch?v=9oc8Fa7tb8c', 'https://www.youtube.com/watch?v=q76bMs-NwRk', 'https://www.youtube.com/watch?v=LlKyGAGHc4c']
bells =   ['bell_sound1.mp3', 'bell_sound2.mp3', 'bell_sound3.mp3', 'bell_sound4.mp3', 'bell_sound5.mp3']

global state
global timer_state
global music_state
music_state = 'playing'

global player

yt_config = YoutubeDL({'quiet': True,
                       'format': 'bestaudio'})

def get_url(url):
    video_info = yt_config.extract_info(url, download=False) 
    url = [video['url'] for video in video_info['formats'] if video['asr'] is not None][3]
    return url

def play(url, ambience = None, volume = 1.0):
    if ambience is not None:    global player
    ff_opts = {'paused': True, 'volume': volume}
    player = MediaPlayer(get_url(url), ff_opts = ff_opts)

    time.sleep(6)
    player.toggle_pause()
    last_pts = 10
    updated_pts = 0

    print('::: playing stream')

    last_buffered_pts = 0
    buffer_repeat_count = 0
    duration = int(str(player.get_metadata()['duration']).split('.')[0])
    while True:
        updated_pts = int(str(player.get_pts()).split('.')[0])
        while player.get_pause():
            time.sleep(0.4)

        if updated_pts == last_pts != 0:
            if last_pts == 0 and updated_pts == 0:   pass
            player.toggle_pause()
            print("buffered out, pausing")
            time.sleep(2)
            player.toggle_pause()
            last_buffered_pts = last_pts
            if last_buffered_pts == updated_pts:    buffer_repeat_count += 1
            print('::: buffer count', buffer_repeat_count)
        
        if updated_pts != last_buffered_pts:
            last_buffered_pts = 0
            buffer_repeat_count = 0

        if buffer_repeat_count > 3:
            print('::: reviving stream')
            player.close_player()
            time.sleep(1)
            print('::: closed stream')
            player = MediaPlayer(get_url(url), ff_opts = ff_opts)
            time.sleep(2)
            player.toggle_pause()
            player.seek(updated_pts + 1) 
            player.toggle_pause()
            buffer_repeat_count = 0

        current_pts = int(str(player.get_pts()).split('.')[0])
        if current_pts + 8 == duration:
            print(':::entered closing')
            buffer_repeat_count = 0
            while player.get_volume() >= 0.0156255:
                player.set_volume(player.get_volume() - 0.0009765625)
                time.sleep(0.0625)
            print(":::closing stream")
            player.toggle_pause()
            time.sleep(2)
            break
        last_pts = updated_pts
        time.sleep(1)

    print('broke...')

def send_notif(message, title):
	plyer.notification.notify(
			title = title,
			message = message,
			app_icon = 'feo.ico',
			app_name = 'M E E T',
			timeout = 10,
			toast = False
		)

def timer_thread(work_time, break_time):
    '''
    function to handle timing and set make changes to appropriate variables which affect the state of the player thread
    also handles notifications
    '''
    while True:
        time.sleep(60 * work_time)
        while player.get_volume() >= 0.0156255:
            player.set_volume(player.get_volume() - 0.0009765625)
            time.sleep(0.0625)
        player.toggle_pause()
        playsound.playsound(bells[random.randint(0, 3)])
        print(':::breakTime')
        time.sleep(60 * break_time)
        print(':::breakOver')
        playsound.playsound(bells[random.randint(0, 3)])
        player.toggle_pause()
        player.set_volume(0.125)
        while player.get_volume() < 0.95:
            player.set_volume(player.get_volume() + 0.03125)
            time.sleep(0.100)

def player_thread(shuffle, sleep):
    time.sleep(sleep)
    print('started palyer thread')
    while True:
        if shuffle: random.shuffle(streams)
        for stream in streams:
            play(stream)

def ambience_handler(shuffle, volume):
    print('started ambience thread')
    while True:
        if shuffle: random.shuffle(ambience)
        for sound in ambience:
            play(sound, ambience = True, volume = volume)


if __name__ == '__main__':
    threading._start_new_thread(os.system, ('python play_ambience.py 0.05', ))
    #, {'func': ambience_handler, 'args': (True, 'med', )}
    le_threads = [{'func': timer_thread, 'args': (25, 5, )}, {'func': player_thread, 'args': (True, 0)}]
    threads = [threading.Thread(target = thread['func'], args = thread['args']) for thread in le_threads]
    [thread.start() for thread in threads]
    [thread.join() for thread in threads]
