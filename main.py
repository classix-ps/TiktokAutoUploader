from TiktokBot import TiktokBot
import os
import sys

if __name__ == "__main__":
    # Example Usage
    # pip install git+https://github.com/pytube/pytube
    os.chdir("/home/ubuntu/TiktokAutoUploader")
        
    # Use a video from your directory.
    # tiktok_bot.upload.uploadVideo("test1.mp4", "This is test", 1, 2, private=True)

    # Or use youtube url as video source. [Simpsons Meme 1:16 - 1:32 Example]

    # tiktok_bot.upload.uploadVideo("https://www.youtube.com/watch?v=4eegr0W_C5c", "", private=True, test=False)
    # tiktok_bot.upload.uploadVideo("test.mp4", "Hi", private=False, test=False)


    # You can also choose to upload a file directly with no editing or cropping of the video.
    #tiktok_bot.upload.directUpload("test.mp4", private=True, test=True)

    executions = 1
    maxExecutions = 10
    if str(sys.argv[1]) == "galaxy":
        tiktok_bot = TiktokBot("discovergalaxies", "galaxy.cookie", "VideosDirPath")

        fileIndex = -1
        with open("fileIndex") as f:
            fileIndex = int(f.readlines()[0])

        while not tiktok_bot.upload.directUpload("../videos/" + sorted(os.listdir("../videos"))[fileIndex], "galaxyHashtags.txt"):
            executions += 1
            if executions > maxExecutions:
                break
            pass
        
        if executions <= maxExecutions:
            with open("fileIndex", "w") as f:
                f.write(str(fileIndex+1))
    elif str(sys.argv[1]) == "podcast":
        tiktok_bot = TiktokBot("viralpodcastclips", "podcast.cookie", "VideosDirPath")

        while not tiktok_bot.upload.uploadVideo("https://www.youtube.com/watch?v=cqDb9AhblyQ", "", 0, 10, "podcastHashtags.txt"):
            executions += 1
            if executions > maxExecutions:
                break
            pass
    #tiktok_bot.upload.directUpload("test.mp4")
    #tiktok_bot.upload.directUpload("../videos/AM1316-241.mp4")
    #tiktok_bot.upload.directUpload("../videos/2MASXJ09133888-1019196.mp4")
    #tiktok_bot.upload.directUpload("../videos/25 years of stunning definition.mp4")

    print(f"Executions: {executions}")


    ####################################################################################################################
    # Scheduling does not work currently.

    # tiktok_bot.schedule.printSchedule()
    # playlist = https://www.youtube.com/playlist?list=PLiMQfyKvRdimHicuw1cAmwS7d_UiANXcj
    '''
        while True:
            url = input("Enter a url for uploading:: ")
            caption = input("Enter a caption for the video:: ")
            timeStart = input("Enter Start Time:: ")
            timeEnd = input("Enter End Time:: ")
            # Add this video into the csv so that you can upload yourself, by putting test parameter on and just showing you.
            tiktok_bot.schedule.scheduleVideo(url, caption, timeStart, timeEnd)
    '''
    # We can add task schedule from read from a csv: url, caption, startTime, endTime, time_to_release.
    # tiktok_bot.schedule.submit_all_schedule()
    # tiktok_bot.schedule.scheduleVideo("https://www.youtube.com/watch?v=yxErIigWRv4", "why do these never have my name!!", 115, 125)
    # Default params: Videos are separated by a day each "", time is constant: "20:10" ;
