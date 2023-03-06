import asyncio
import sys
import threading
import os

async def callScript(frame):
    os.system('python data_conversion.py %s' % (frame))

for i in range(0, 6573, 20):
    threads = []
    for j in range(0, 20):
        frame_num = (i+j)
        if frame_num > 6572:
            exit()
        frame = "frame-%s.png" % (str(frame_num).zfill(4))
        print(frame)

        # here we are calling the python script
        t = threading.Thread(target=asyncio.run, args=(callScript(frame),))
        threads.append(t)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

