#!/bin/bash

# Information:
# 	用crontab排程此程式(最高頻率每分鐘)，自動將webcam畫面截圖到photo資料夾
#	依日期建立資料夾，而圖片以「yyyymmddHHMM.jpg」的方式命名
       
# Foler name
DATE=$(date '+%Y%m%d');
FolderName=/home/pi/Desktop/shell-result/$DATE;

# 建立資料夾，帶-p表示資料夾存在的話忽略，不存在則建立
mkdir -p $FolderName


# 透過fswebcam截圖，先skip 60張圖讓webcam先自動對焦完成
# 將banner設定成透明，並加入時間戳記與調整字型
# fswebcam -r 1280x720 -S 60 --banner-colour '#FF000000' --line-colour '#FF000000' --timestamp '%Y-%m-%d %H:%M' --font 'sans:32' /home/pi/Timelapse/photo/$FolderName/$TIME.jpg
TIME=$(date '+%H_%M_%S_%3N');
fswebcam -r 4056x3040 -l 5 --no-banner $FolderName/$TIME.jpg

# return 0 to system
exit 0