from youtube_transcript_api import YouTubeTranscriptApi as yta
import re
def Get_Transcript(video_id):

    data = yta.get_transcript(video_id,languages = ['en'])
    transcript = ''
    for value in data:
        for key,val in value.items():
            if key == "text":
                val = val+"\n"
                val = val.encode("ascii","ignore")
                transcript += val.decode() 
    return transcript


if __name__ == "__main__":
    with open("transcript.txt","w") as file:
        file.write(Get_Transcript(video_id = "y0oWA2yVB3s"))

