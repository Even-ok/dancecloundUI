import numpy as np
from math import acos
from dtw import dtw
from scipy.optimize import least_squares

from json_funcs import *

def get_angle_from_2_vector(x1, y1, x2, y2, deg_range=1):

    den = (np.sqrt(x1 ** 2 + y1 ** 2) * np.sqrt(x2 ** 2 + y2 ** 2))
    # 为避免出现分母为0
    if den == 0:
        return np.nan
    t = (x1 * x2 + y1 * y2) / den
    if t > 1:
        t = 1
    elif t <= -1:
        t = -1
    t_rad = acos(t)
    if x1 * y2 - x2 * y1 < 0:
        t_rad = 2 * np.pi - t_rad
    t_deg = t_rad * 180 / np.pi
    if deg_range == 2:
        if t_deg >= 180:
            t_deg -= 360
    return t_deg

def get_mykpdata(data, p): #data:list_json(横坐标，纵坐标，置信度) p:kp_set
    po = p[0]
    pa = p[1]
    pb = p[2]
    x1 = data[pa][0] - data[po][0]
    y1 = data[pa][1] - data[po][1]
    x2 = data[pb][0] - data[po][0]
    y2 = data[pb][1] - data[po][1]
    sideA = np.sqrt(x1 ** 2 + y1 ** 2)
    sideB = np.sqrt(x2 ** 2 + y2 ** 2)
    angle = get_angle_from_2_vector(x1, y1, x2, y2, deg_range=1)
    prob = data[po][2] ##################角度置信度使用中间点的置信度?
    mykpdata = np.array([sideA, sideB, angle, prob])
    return mykpdata

def get_mykpdata_video(list_json, kpset):
    frame_num = len(list_json)
    kp_num = len(kpset)
    mykpdata_list = np.zeros([frame_num, kp_num, 4])
    # 判断每一帧
    for i in range(0, frame_num):
        # 新建一帧的信息 len(kpset)*4
        mykpdata_frame = np.zeros([kp_num, 4])
        # 遍历每个关键点，共len(kpset)个
        for j in range(0, kp_num):
            mykpdata_frame[j, :] = get_mykpdata(list_json[i, ::], kpset[j, :])
        mykpdata_list[i, ::] = mykpdata_frame
    return mykpdata_list

def calc_angle_diff(a1, a2):
    diff = abs(a1 - a2)
    diff %= 360
    if diff > 180:
        diff = 360 - diff
    return diff

def score_bound(x, x_min, x_max):
    if x > x_max:
        return x_max
    if x < x_min:
        return x_min
    return x

def score_func(x):
    if x < 25:
        score = 1
    elif x < 45:
        score = (-2 * x + 150) / 100
    else:
        score = (-4 * x + 240) / 100
    score = score_bound(score, 0, 1)
    return score

def score_func2(x):
    """

    :param x: 角度。
    :return: 分数，范围在[0,1]。
    """

    if x < 5:
        score = 1
    elif x < 30:
        score = (-8 / 5 * x + 108) / 100
    elif x < 45:
        score = (-4 * x + 180) / 100
    else:
        score = 0
    score = score_bound(score, 0, 1)
    return score

def rhythm_score_func(x):#计算节奏分数
    """
    :param x: 角度。
    :return: 分数，范围在[0,1]。
    """

    if x < 20:
        score = 1
    elif x < 80:
        score = (-2 / 3 * x + 340/3) / 100
    elif x < 100:
        score = (-3 * x + 300) / 100
    else:
        score = 0
    score = score_bound(score, 0, 1)
    return score

def flip(arr):
    arr[arr>180] = 360 - arr[arr>180]
    return arr

def cal_score_by_dtw(kpd1,kpd2):
    m = len(kpd1)
    n = len(kpd1[0])

    angle_diff = np.zeros([m, n])#m帧，n个骨骼点
    kp_score = np.zeros([m, n])
    invalid_const = np.nan

    # 单个骨骼点的置信度阈值，不影响整个帧
    kp_prob_threshold = 0.6
    A = np.zeros([m, n])
    B = np.zeros([m, n])
    for i in range(0, m):
        for j in range(0, n):
            if kpd1[i, j, 3] < kp_prob_threshold:
                # print('low prob kp:', i, j)
                kp_score[i, j] = invalid_const
                angle_diff[i, j] = invalid_const
                A[i, j] = invalid_const
                B[i, j] = invalid_const
                
            else:
                if np.isnan(kpd1[i, j, 2]) or np.isnan(kpd2[i, j, 2]):
                    break
                angle_diff[i, j] = calc_angle_diff(kpd1[i, j, 2], kpd2[i, j, 2])
                kp_score[i, j] = score_func(angle_diff[i, j])

    return kp_score

def cal_score_by_dtw_video(kpd1, kpd2, invalid_list):
    m1 = len(kpd1)
    m2 = len(kpd2)
    n = len(kpd1[0])

    if m1 < m2:
        m = m1
    else:
        m = m2
    angle_diff = np.zeros([m, n])#m帧，n个骨骼点
    kp_score = np.zeros([m, n])
    invalid_const = np.nan

    # 单个骨骼点的置信度阈值，不影响整个帧
    kp_prob_threshold = 0.6
    A = np.zeros([m, n])
    B = np.zeros([m, n])
    for i in range(0, m):
        # 如果是无效帧
        if i in invalid_list:
            kp_score[i, :] = invalid_const
            angle_diff[i, :] = invalid_const
            A[i, :] = invalid_const
            B[i, :] = invalid_const
        else:
            for j in range(0, n):
                if kpd1[i, j, 3] < kp_prob_threshold or kpd2[i, j, 3] < kp_prob_threshold:
                    # print('low prob kp:', i, j)
                    kp_score[i, j] = invalid_const
                    angle_diff[i, j] = invalid_const
                    A[i, j] = invalid_const
                    B[i, j] = invalid_const
                    
                else:
                    if np.isnan(kpd1[i, j, 2]) or np.isnan(kpd2[i, j, 2]):
                        break
                    angle_diff[i, j] = calc_angle_diff(kpd1[i, j, 2], kpd2[i, j, 2])
                    # todo 滤波？
                    kp_score[i, j] = score_func(angle_diff[i, j])
                    # print(i, j, kpd1[i, j, 2], kpd2[i, j, 2], kp_score[i, j])

                    A[i, j] = kpd1[i, j, 2] 
                    B[i, j] = kpd2[i, j, 2] #用于后面计算差分和最小二乘
    
    score_avg2 = np.zeros(n)
    rhythm_avg = np.zeros(n)

    def func(p,x):
        k,b=p
        return k*x+b
    def error(p,x,y):
        return func(p,x)-y

    for i in range(0,n):
        tmp_A = np.empty(shape=[0, 0])
        tmp_B = np.empty(shape= [0, 0])
        tmp_count = 0
        # print(i)
        for j in range(0, m):
            if(A[j, i] >= 0 and B[j, i] >= 0): # 也就是 np.isnan(kpd1[i, j, 2]) 不成立 ？
                tmp_count += 1
                tmp_A = np.append(tmp_A, A[j, i])
                tmp_B = np.append(tmp_B, B[j, i])
        if tmp_count <= 1:
            print("invalid!!!----",i)
            score_avg2[i] = np.nan
            continue

        tmp_A = flip(tmp_A)
        tmp_B = flip(tmp_B)
        
        dA = (tmp_A[1:]-tmp_A[:-1])
        dB = (tmp_B[1:]-tmp_B[:-1])
        alignment = dtw(dA, dB,keep_internals=True)

        rhythm_delta=np.abs(alignment.index2-alignment.index1)

        rhythm_avg[i] = rhythm_score_func(rhythm_delta.mean()) # 对角度的差分值根据DTW打分
        A_ = tmp_A[alignment.index1]
        B_ = tmp_B[alignment.index2]
        
        p0=[1,20]
        
        #把error函数中除了p0以外的参数打包到args中(使用要求)
        Para=least_squares(error,p0,args=(B_,A_))
        #最小二乘和差分操作是为了尽量减少拍摄视角带来的误差
        
        #读取结果
        k,b=Para.x
        kB_b = k*B_ + b

        least_squares_error=np.abs(A_- kB_b)
        raw_angle_error=np.abs(tmp_A- tmp_B)
        least_squares_error_mean=least_squares_error.mean()# 最小二乘的角度差分
        raw_angle_error_mean=raw_angle_error.mean()# 原角度的角度差分

        if np.abs(least_squares_error_mean - raw_angle_error_mean) < 20: # 最小二乘效果显著
            score_avg2[i] = score_func2(least_squares_error_mean)
        else:
            score_avg2[i] = score_func2(raw_angle_error_mean)
    
    return score_avg2, rhythm_avg
    #score_avg：未经过角度差分，通过score_func计算  score_avg2：经过角度差分最小二乘，通过score_func2计算  rhythm_avg：角度差分值根据dtw打分

def fill_nan(array):
    m, n, o = array.shape  # 帧，关节，关节信息（角度为2）
    new_array = array.copy()
    for i in range(n):
        # print(i)
        y = array[:, i, 2]  # 取某个关节的所有信息（帧，角）
        
        nans, x = np.isnan(y), lambda z: z.nonzero()[0]

        if(len(np.unique(nans)) != 1):#如果有缺失
            y[nans] = np.interp(x(nans), x(~nans), y[~nans])
        new_array[:, i, 2] = y
    return new_array

def main_2(ns,origin_json_path,imitate_json_path):
    # 角度关键点集合
    keypoint_set = np.array([
        [3, 2, 4],  # 右手
        [6, 7, 5],  # 左手
        [2, 1, 3],  # 右肩
        [5, 6, 1],  # 左肩
        [1, 0, 8],  # 头与躯干
        [1, 2, 8],  # 右肩与躯干
        [1, 5, 8],  # 左肩与躯干
        [8, 9, 1],  # 躯干与右髋
        [8, 12, 1],  # 躯干与左髋
        [9, 8, 10],  # 右腿与髋
        [12, 8, 13],  # 左腿与髋
        [10, 9, 11],  # 右脚
        [13, 12, 14],  # 左脚
        [11, 10, 22],  # 右脚踝
        [14, 13, 19],  # 左脚踝
    ], dtype=int)

    #关键点集合，[ 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 19 22]
    key_point_list = np.unique(keypoint_set)

    # 无效帧列表
    invalid_frame1 = {'no_people_frame': [],
                      'low_prob_frame': [],
                      'reverse_frame': [],
                      }

    invalid_frame2 = {'no_people_frame': [],
                      'low_prob_frame': [],
                      'reverse_frame': [],
                      }

    # 读取json文件  lj:三维数组，帧数*关键点数*3(横坐标、纵坐标、置信度)   lr:一维数组，每一帧的flag(1正面 2反面 0无效)
    lj2,lr2 = read_json_imitate_video(imitate_json_path,key_point_list,invalid_frame2)
    lj1,lr1 = read_json_origin_video(origin_json_path,key_point_list,invalid_frame1)
    # 转换数据编排方式，改为三维数组，帧数*关键点数*4(A边长度，B边长度，角度，置信度)，将原关键点信息的像素信息转化为角度及长度
    mykpdata1 = get_mykpdata_video(lj1, keypoint_set)
    mykpdata2 = get_mykpdata_video(lj2, keypoint_set)

    # 取无效帧列表
    # 无效帧序号并非json文件号，而是从start开始计算
    #以音乐对齐为前提，标准视频与测试视频的无效帧都要同时删除，并互相删除对方的无效帧，以保证后续动作对齐
    no_people_frame_list1 = invalid_frame1['no_people_frame']
    low_prob_frame_list1 = invalid_frame1['low_prob_frame']
    no_people_frame_list2 = invalid_frame2['no_people_frame']
    low_prob_frame_list2 = invalid_frame2['low_prob_frame']
    invalid_frame_list = list(set(
        no_people_frame_list1 + low_prob_frame_list1 + no_people_frame_list2 + low_prob_frame_list2))
    invalid_frame_list.sort()

    lr_len = min(len(lr1), len(lr2))
    lr_list = []
    for i in range(lr_len):
        # 判断左右反转
        if i not in invalid_frame_list and lr1[i] * lr2[i] == 2:
            lr_list.append(i)

    #将左右翻转的帧也当作无效帧
    invalid_frame_list = invalid_frame_list + lr_list
    invalid_frame_list.sort()

    # 插值
    fill_nan(mykpdata1)
    fill_nan(mykpdata2)

    # 算分
    scores,rhythm_score = cal_score_by_dtw_video(mykpdata1, mykpdata2, invalid_frame_list)

    return scores,rhythm_score

def score_print(ns,origin_json_path,imitate_json_path):
    kpscores,rhythm_score=main_2(ns,origin_json_path,imitate_json_path)
    kpscores=kpscores.reshape(1,-1)

    #5
    kpnames=np.array(["右手", "左手", "右肩", "左肩", "头与躯干", "右肩与躯干", "左肩与躯干","躯干与右髋", "躯干与左髋", "右腿与髋", "左腿与髋", "右脚", "左脚", "右脚踝", "左脚踝"])
    scoresum=0
    kpscores=kpscores.T
    nankp=~np.isnan(kpscores).any(axis=1)
    print(nankp)
    kpscores=kpscores[nankp]
    namestp=kpnames[nankp]
    kpscores=kpscores.T
    scores=np.zeros(kpscores.shape[1])
    name_score=[]
    for i in range(kpscores.shape[1]):
        tp=kpscores[:,i]
        print(tp)
        tp=np.mean(tp[tp>=0])
        if not tp>=0:
            tp=0
        print('mean ',tp)
        scores[i]=tp
        name_score.append([namestp[i],tp*100])

    scores=np.sort(scores)
    scoresum=scores[:2].mean()*30+scores[2:-3].mean()*50+scores[-3:].mean()*20
    print(name_score)
    print(scoresum)
    return scoresum,name_score,rhythm_score
