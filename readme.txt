该版本含选视频、录像、评分、显示各关节得分、显示节奏得分、显示并存储得分记录功能.

使用方法：
（1）已经有要模仿的视频
	1.将要模仿的视频放入origin_videos文件夹中
	2.打开origin.py，将main调用的参数namelist改成需要模仿的视频的名字列表（不带.mp4）
	3.注意origin.py main函数camera参数为False，否则文件夹下的原视频会丢失
	4.运行origin.py文件，会生成渲染后的视频与json文件
	5.可将原视频的示意图放入origin_pics文件夹中
	6.打开imitate.py运行（可能需要该路径）
	7.程序执行结束后再次执行程序只需点击输入图片名的框即可重新开始
（2）需要录制要模仿的视频
	1.打开origin.py，将main调用的参数namelist改为空列表（原视频会使用默认命名），或输入视	   频名称到namelist列表中，视频会依次按照给定的名称命名
	2.注意origin.py main函数camera参数为True
	3.运行origin.py文件，会生成渲染后的视频与json文件，进行视频录制，会生成渲染后的视频与	   json文件
	4.可将原视频的示意图放入origin_pics文件夹中
	5.打开imitate.py运行（可能需要该路径）
	6.程序执行结束后再次执行程序只需点击输入图片名的框即可重新开始

imitate.py文件中点击拍照对应函数photo_score中的参数camera用来控制本次打分是否需要重新录制视频，如果camera为True，则点击拍照时会开启摄像头进行录像，并进行姿态识别；如果camera为False，则点击拍照时会直接使用文件夹中的json文件进行打分。