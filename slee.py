#!/usr/bin/env python
# coding: UTF-8

#################################################################
# Copyright (C) 2017 Mono Wireless Inc. All Rights Reserved.    #
# Released under MW-SLA-*J,*E (MONO WIRELESS SOFTWARE LICENSE   #
# AGREEMENT).                                                   #
#################################################################

# ライブラリのインポート
import sys
import csv
#import os
#import copy
import threading
import time
import datetime
from optparse import *
import random
#from queue import Queue

import sys
import glob
import serial
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
from matplotlib import animation

# WONO WIRELESSのシリアル電文パーサなどのAPIのインポート
sys.path.append('./MNLib/')
from apppal import AppPAL



# ここより下はグローバル変数の宣言
# コマンドラインオプションで使用する変数
options = None
args = None

# 各種フラグ
bEnableLog = False
bEnableErrMsg = False

# プログラムバージョン
Ver = "1.1.0"


 
def serial_ports():
    """ Lists serial port names
 
        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')
 
    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

def ParseArgs():
		global options, args

		parser = OptionParser()
		parser.add_option('-t', '--target', type='string', help='target for connection', dest='target', default=None)
		parser.add_option('-b', '--baud', dest='baud', type='int', help='baud rate for serial connection.', metavar='BAUD', default=38400)
		parser.add_option('-s', '--serialmode', dest='format', type='string', help='serial data format type. (Ascii or Binary)',  default='Ascii')
		parser.add_option('-l', '--log', dest='log', action='store_true', help='output log.', default=False)
		parser.add_option('-e', '--errormessage', dest='err', action='store_true', help='output error message.', default=False)
		(options, args) = parser.parse_args()


def pal_script(open_port, nm):
    global flag
    global tagprintlist

    print("*** MONOWIRELESS App_PAL_Viewer " + Ver + " ***")


    ParseArgs()
    

    bEnableLog = options.log
    bEnableErrMsg = options.err
    try:
        PAL = AppPAL(port=open_port, baud=options.baud, tout=0.05, sformat=options.format, err=bEnableErrMsg)
    except:
        print("Cannot open \"AppPAL\" class...")
        exit(1)
    


    while flag:
        try:
            # データがあるかどうかの確認
            if PAL.ReadSensorData():
                # あったら辞書を取得する
                Data = PAL.GetDataDict()
                if Data['RouterSID'] == '80000000':
                    RSID = 'No Relay'
                else:
                    RSID = Data['RouterSID']
                #print(Data)
                #print(Data['ArriveTime'].strftime('%Y-%m-%d %H:%M:%S.%f')[:-3], end = ",")
                #print(Data['LogicalID'], end = ",")
                #print(Data['EndDeviceSID'], end = ",")
                #print(RSID, end = ",")
                #print(Data['SequenceNumber'], end = ",")
                #print(Data['LQI'], end = ",")
                #print(Data['Power'], end = "\n")
                datas_TAG = [str(Data['ArriveTime'].strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]),\
                Data['LogicalID'],Data['EndDeviceSID'],RSID,Data['SequenceNumber'],Data['LQI'],Data['Power']]
                tagprintlist.append(((Data['EndDeviceSID'])[-4:],Data['LQI'],str(nm)))

                #csvout=csv.writer(f)

                #csvout.writerow(datas_TAG)

                # なにか処理を記述する場合はこの下に書く
                #PAL.ShowSensorData()	# データを出力する
                # ここまでに処理を書く

                # ログを出力するオプションが有効だったらログを出力する。
                if bEnableLog == True:
                    PAL.OutputCSV()	# CSVでログをとる

        # Ctrl+C でこのスクリプトを抜ける
        except KeyboardInterrupt:
            break

    del PAL

    print("*** Exit App_PAL Viewer ***")


def _update(frame, i):
    # 現在のグラフを消去する
    global tagprintlist
    global flag
    #ax.cla()
    #tex1.cla()
    #tex2.cla()
    #ax.set_xlim(0, 6)
    #ax.set_ylim(0, 6)
    #tex2 = ax.text(6, 5, [], size=30, horizontalalignment="center", verticalalignment="top")
    N = 200 #曲線のなめらかさ
    pi_2 = 2.0 * math.pi
    t = np.linspace(0,pi_2,N)#媒介変数
    i = 0
    lefttext = 'NULL'
    righttext = 'NULL'
    try:
        print(i)
        #print(tagprintlist)
        leftlist = []
        rightlist = []        
        if len(tagprintlist) > 0:
            tag_df = pd.DataFrame(tagprintlist)
            maxlqlist = []
            for tag in tag_df.groupby(tag_df.columns[0]):
                #print(tag)
                #print(tag[1][tag[1].columns[1]].idxmax())
                #print(tag[1][tag[1].columns[1]].idxmax())
                maxlq = tag[1].loc[[tag[1][tag[1].columns[1]].idxmax()],:].reset_index(drop=True)
                if int(maxlq.iloc[0][2]) == 2:
                    leftlist.append(maxlq.iloc[0][0])
                else:
                    rightlist.append(maxlq.iloc[0][0])

                #if maxlq.loc[maxlq.columns[2]] == "2":
                 #   maxlq.loc[maxlq.columns[2]]
                print(maxlq)
                #maxlqlist.append(np.ravel((maxlq.values)).tolist())
            print("left")
            print(leftlist)
            print("right")
            print(rightlist)
            lefttext = jointext(leftlist)
            righttext = jointext(rightlist)
            tex1.set_text(lefttext)
            tex2.set_text(righttext)
            #print(maxlqlist)
            i += 1
            tagprintlist = []
    except(KeyboardInterrupt):
        flag = False



    # データを更新 (追加) する
    #cirx1 = 1 + 0.5 * np.cos(t) + random.random()
    #ciry1 = 1 + 0.5 * np.sin(t)
    # グラフを再描画する
    #ax.text(3,3,frame)
    #ax.plot(cirx1,ciry1,'-', color='blue')
    



def jointext(textlist):
    if len(textlist) == 0:
        return 'NULL'
    if len(textlist) == 1:
        return textlist[0]
    else:
        printtext = []
        isodd = True
        for text in textlist:
            if isodd:
                firsttext = text
                isodd = False
            else:
                addtext = firsttext + '  ' + text
                printtext.append(addtext)
                isodd = True
        if not isodd:
            printtext.append(firsttext + '      ')
        printtext_str = "\n".join(printtext)
        return printtext_str







flag = True

if(__name__ == "__main__"):
    portslist = serial_ports()
    i = 0
    tagprintlist = []
    threadlist = []
    nm = 1
    for port in portslist:
        try:
            t = threading.Thread(target=pal_script,args=(port,nm))
            threadlist.append(t)
            t.start()
            nm += 1
        except(KeyboardInterrupt):
            break
        except:
            pass
    time.sleep(1)
    #print(threadlist)
    fig = plt.figure(figsize=(10,10))
    ax = fig.add_subplot(111)
    #ax_base = fig.add_subplot(111)
    ax2 = fig.add_subplot(121)
    ax3 = fig.add_subplot(122)
    #ax2.tick_params(labelbottom=False, labelleft=False, labelright=False, labeltop=False)
    #ax3.tick_params(labelbottom=False, labelleft=False, labelright=False, labeltop=False)
    #ax2.tick_params(bottom=False, left=False, right=False, top=False)
    #ax3.tick_params(bottom=False, left=False, right=False, top=False)
    ax2.axis("off")
    ax3.axis("off")
    ax.set_xlim(0,8)
    ax.set_ylim(0,6)
    ax2.set_xlim(0,10)
    ax2.set_ylim(0,6)
    ax3.set_xlim(0,10)
    ax3.set_ylim(0,6)
    
    # bboxの作成
    boxdic = {
        "facecolor" : "lightgreen",
        "edgecolor" : "black",
        "boxstyle" : "Round",
        "linewidth" : 2
    }

    ax.text(2, 5.5, "Left", size=40, bbox=boxdic, horizontalalignment="center", verticalalignment="center")
    ax.text(6, 5.5, "Right", size=40, bbox=boxdic, horizontalalignment="center", verticalalignment="center")

    ax.plot([0.2, 3.8], [5.5, 5.5],color="black")
    ax.plot([0.2, 3.8], [0.2, 0.2],color="black")
    ax.plot([0.2, 0.2], [0.2, 5.5],color="black")
    ax.plot([3.8, 3.8], [0.2, 5.5],color="black")
    ax.plot([4.2, 7.8], [5.5, 5.5],color="black")
    ax.plot([4.2, 7.8], [0.2, 0.2],color="black")
    ax.plot([4.2, 4.2], [0.2, 5.5],color="black")
    ax.plot([7.8, 7.8], [0.2, 5.5],color="black")

    tex1 = ax.text(2, 5, "NULL", size=30, horizontalalignment="center", verticalalignment="top", fontfamily = 'monospace')
    tex2 = ax.text(6, 5, "NULL", size=30, horizontalalignment="center", verticalalignment="top", fontfamily = 'monospace')


    params = {
        'fig': fig,
        'func': _update,  # グラフを更新する関数
        'fargs': (i,),  # 関数の引数 (フレーム番号を除く)
        'interval': 1500,  # 更新間隔 (ミリ秒)
        'frames': np.arange(0, 10, 0.1),  # フレーム番号を生成するイテレータ
        'repeat': False,  # 繰り返さない
    }

    anime = animation.FuncAnimation(**params)
    plt.show()

    flag = False

    '''

  



    while(True):
        try:
            time.sleep(3)
            print(i)
            #print(tagprintlist)
            if len(tagprintlist) > 0:
                tag_df = pd.DataFrame(tagprintlist)
                maxlqlist = []
                for tag in tag_df.groupby(tag_df.columns[0]):
                    #print(tag)
                    #print(tag[1][tag[1].columns[1]].idxmax())
                    #print(tag[1][tag[1].columns[1]].idxmax())
                    maxlq = tag[1].loc[[tag[1][tag[1].columns[1]].idxmax()],:]
                    print(maxlq)
                    maxlqlist.append(np.ravel((maxlq.values)).tolist())
                print(maxlqlist)
                i += 1
                tagprintlist = []
        except(KeyboardInterrupt):
            flag = False
            break
            
    '''