from moviepy.editor import VideoFileClip, concatenate_videoclips


video_1 = VideoFileClip("V:\Torrent\AriaData\Complete\HRV051A\HRV051A.mp4")
video_2 = VideoFileClip("V:\Torrent\AriaData\Complete\HRV051A\HRV051B.mp4")

final_video= concatenate_videoclips([video_1, video_2])
final_video.write_videofile("V:\Torrent\AriaData\Complete\HRV051A\HRV051.mp4",threads=4)