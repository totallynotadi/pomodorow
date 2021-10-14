import random
import sys

from pomodorow import play

print(sys.argv)
volume = float(sys.argv [1])
print(volume)

ambience = ['https://www.youtube.com/watch?v=9oc8Fa7tb8c',
            'https://www.youtube.com/watch?v=q76bMs-NwRk',
            'https://www.youtube.com/watch?v=LlKyGAGHc4c',
            'https://www.youtube.com/watch?v=m5Mz9Tqs9CE',]

SHUFFLE = True
while True:
    print('started ambinece')
    if SHUFFLE:
        random.shuffle(ambience)
    for sound in ambience:
        play(sound, volume=volume)
