
# With start number
# ffmpeg -an -sn -start_number 100 -i "./session019/%08d.bmp" -framerate 1 -c:v libx264 -r 60 "session019.mp4"

# Limit the frames <frames wanted> * r (?)
# ffmpeg -an -sn -start_number 210 -i "./session019/%08d.bmp" -framerate 1 -frames:v 6000 -c:v libx264 -r 60 "session019.mp4"
# ffmpeg -an -sn -i "./session${1}/%08d.bmp" -framerate 1 -c:v libx264 -r 60 "session${1}.mp4"



# Slow down a video
# ffmpeg -i session${1}.mp4 -filter:v "setpts=4.0*PTS" data_matrix${1}.mp4

# For .Avi have a look at:
# https://askubuntu.com/questions/83161/use-ffmpeg-to-transform-mp4-to-same-high-quality-avi-file
ffmpeg -an -sn -i "./session${1}/%08d.bmp" -framerate 1 -vcodec mpeg4 -r 60 "session${1}.avi"
