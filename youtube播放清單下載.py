# from pytube import Playlist

# url= 'https://www.youtube.com/watch?v=IFWPOnq_Q7k&list=PLXArRTWDgwVFwV2r0JzjKog7WYq6Fa78A' 
# playlist = Playlist(url)
# print('此清單中有: %s' % len(playlist.video_urls) + '部影片')

# playlist.download_all()
# print('download is complete')

import requests
import re
from pytube import YouTube
import os

#觀察後發現所有播放清單網址的差別都在/watch後面，所以須將完整網址拆成兩部分
url = 'https://www.youtube.com'
playlist_url = input('請輸入您要下載的播放清單(youtube.com之後的網址，例如：/watch?v=IFWPOnq_Q7k&list=PLXArRTWDgwVFwV2r0JzjKog7WYq6Fa78A)') 
html = requests.get(url + playlist_url) #取得網頁原始碼

#設一個空串列來接要的網址
video_list = [] 

#用正規表達式找到播放清單中的連結
res_list = re.findall(r'/watch[-A-Za-z0-9+&@#%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]',html.text) 

#以os指定影片下載到哪個資料夾，若不存在此資料夾則建立新資料夾
pathdir = "E:\\temp"
if not os.path.isdir(pathdir):
    os.mkdir(pathdir)

#在 pytube 的 YouTube 這個 class 當中，存在著 “on_progress_callback” 可以自行編寫進度條
def progress(stream, chunk, file_handle, bytes_remaining):
    contentSize = yt.streams.filter(subtype='mp4',res='360p',progressive=True).first().filesize
    size = contentSize - bytes_remaining

    print('\r' + '[Download progress]:[%s%s]%.2f%%;' % (
    '█' * int(size*20/contentSize), ' '*(20-int(size*20/contentSize)), float(size/contentSize*100)), end='')

#將抓取到的youtube網址做迴圈分別取得
for res in res_list:
     #將含有list= & index=的網址篩選出來
    if "list=" and "index=" in res:

        #判斷影片是否存在串列中，避免重複
        if res not in video_list: 

        #將沒有重複的網址加入串列
            video_list.append(res) 
n = 1         
for video in video_list:
    yt = YouTube(url + video,on_progress_callback=progress)
    print(str(n) +'.'+ yt.title) 

    #用filter篩選影片格式及解析度等，再下載第一個符合條件的影片，並下載到指定資料夾
    yt.streams.filter(subtype='mp4',res='360p',progressive=True).first().download(pathdir)
    
    n = n+1

#所有影片下載完成後，告訴使用者影片下載完成
print('影片下載完成~')    

