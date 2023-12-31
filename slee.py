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
#import time
import datetime
from optparse import *
import random
#from queue import Queue

import sys
import glob
import serial
 

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




import time

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
    #print(threadlist)
    while(True):
        try:

            print(i)
            print(tagprintlist)

            i += 1
            tagprintlist = []
            time.sleep(3)
        except(KeyboardInterrupt):
            flag = False
            break