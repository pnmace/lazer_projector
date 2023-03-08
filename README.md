# lazer_projector
putting this back together in a video was just for fun, but this is pretty neat: https://headpat.xyz/uwu/c0d2b9.mp4
Firefox doesn't like this video for some reason, but mpv and chrome do.. odd..

atm this only has software for converting black/white input frames into an outline of the components of that frame.
Currently this is very unoptimized in order to have *something* since the focus of this project was to learn hardware things and this was quick an easy to make

personal notes:
resolution is 960x720

grab all frames from the input file at 30 fps: `ffmpeg -i bad_apple.webm -r 30 -f image2 video_frames/frame-%04d.png`

convert frames to black/white depending on a certain threshold:
```
Nyaa% for i in `ls | grep frame`
do
convert $i -threshold 55% 55/$i
done   
```
55 seems to look the best atm



maybe make an edge detection algo to figure out where to draw lines for things like frame 1836

we are tracing out all connected components in the frame, giving them an id, the number of px the perimeter is

when tracing out perimeters for each island, we will be using a 3x3 kernel
this could cause issues if we have two islands that are near touching each other
will have to specify to find only other pixels of the same color
i.e.
2o11
o2oo
o2oo
possibly don't even need to? could just consider them all the same color

we want to get a set of all the colored pixels on any given frame
the laser will have to trace out these pixels, and we want to minimize
the amount of blanking or additional distance traveled

if we do dfs, anytime we have a graph that does not have strongly connected components, we require blanking
if we do have a strongly connected component of this graph, we can possibly trace these coordinates
without requiring any blanking by doing the connected components last

determining where to start drawing a shape and which direction to start in could be important
https://en.wikipedia.org/wiki/Eulerian_path ?

turn individual png frames into a full video with audio!
```
ffmpeg -framerate 30 -pattern_type glob -i '*.png' -i bad_apple.opus -r 30 output.mp4
lossless:
ffmpeg -framerate 30 -pattern_type glob -i '*.png' -i bad_apple.opus -r 30 -c:v ayuv output.avi
```










lasers/hardware:
austin hackerspace: ttps://asmbly.org/
https://www.laserpointerpro.com/
https://en.wikipedia.org/wiki/Dichroic_filter
    https://www.edmundoptics.com/f/45-reflective-dichroic-color-filters/12836/

standard wavelength for various laser pointers:
red - 650nm
blu - 405-450nm
grn - 532nm
