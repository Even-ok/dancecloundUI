import cv2
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# def video_capture(origin_name,save_path='C:/Users/dengl/Desktop/activity/imitation_video_ui/imitate_videos/',duration=5,WIDTH=1280,HEIGHT=720,FPS=24,preview=False):
#     imitate_name=origin_name+'.mp4'
#     FILENAME = save_path+origin_name+'/'+imitate_name

#     # 必须指定CAP_DSHOW(Direct Show)参数初始化摄像头,否则无法使用更高分辨率
#     cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
#     # 设置摄像头设备分辨率
#     cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
#     cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
#     # 设置摄像头设备帧率,如不指定,默认600
#     cap.set(cv2.CAP_PROP_FPS, 24)
#     # 建议使用XVID编码,图像质量和文件大小比较都兼顾的方案
#     fourcc = cv2.VideoWriter_fourcc(*'XVID')

#     out = cv2.VideoWriter(FILENAME, fourcc, FPS, (WIDTH, HEIGHT))

#     start_time = datetime.now()
#     while True:
#         ret, frame = cap.read()
#         if ret:
#             out.write(frame)
#             if preview: #显示预览窗口
#                 cv2.imshow('Preview_Window', frame)
#             if (datetime.now()-start_time).seconds == duration:
#                 cap.release()
#                 break
#             # 监测到ESC按键也停止
#             if cv2.waitKey(3) & 0xff == 27:
#                 cap.release()
#                 break
#     out.release()
#     if preview:
#         cv2.destroyAllWindows()
# video_capture('1')

dfcolumns=["编号","动作评分","节奏评分","右手", "左手", "右肩", "左肩", "头与躯干", "右肩与躯干", "左肩与躯干","躯干与右髋", "躯干与左髋", "右腿与髋", "左腿与髋", "右脚", "左脚", "右脚踝", "左脚踝"]
# df0=pd.DataFrame(columns=dfcolumns)
# a=np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]).reshape(1,-1)
# df0=pd.concat([df0,pd.DataFrame(a,columns=dfcolumns)],axis=0)
# df0.to_csv('C:/Users/dengl/Desktop/activity/score_video_ui/scores/'+'1.csv',encoding="utf_8_sig")

# scoredf=pd.read_csv('C:/Users/dengl/Desktop/activity/score_video_ui/scores/'+'1.csv',na_filter=np.nan)
# print(list(scoredf['编号'].values))
# if 1 not in list(scoredf['编号'].values):
#     a=np.array([1,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]).reshape(1,-1)
#     df0=pd.concat([df0,pd.DataFrame(a,columns=dfcolumns)],axis=0)
#     df0.to_csv('C:/Users/dengl/Desktop/activity/score_video_ui/scores/'+'1.csv',encoding="utf_8_sig")

row=[1]*18
scoredf=pd.DataFrame(columns=dfcolumns)
scoredf=pd.concat([scoredf,pd.DataFrame(np.array(row).reshape(1,-1),columns=dfcolumns)],axis=0)
scoredf.to_csv('C:/Users/dengl/Desktop/activity/score_video_ui/scores/'+'2.csv',encoding="utf_8_sig")

scoredf=pd.read_csv('C:/Users/dengl/Desktop/activity/score_video_ui/scores/'+'2.csv',index_col=0)
row=[2]*18
scoredf=pd.concat([scoredf,pd.DataFrame(np.array(row).reshape(1,-1),columns=dfcolumns)[dfcolumns]],axis=0)
scoredf.to_csv('C:/Users/dengl/Desktop/activity/score_video_ui/scores/'+'2.csv',encoding="utf_8_sig")

