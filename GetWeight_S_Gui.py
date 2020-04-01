#-*- coding: UTF-8 -*-
import sys
import json
import re
import openpyxl
import xlwt
import time
import xlrd
import xlutils
from xlutils.copy import copy
import requests
import wx
import thread
import threading


class MainWindow(wx.Frame):
    """We simply derive a new class of Frame."""
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title = title, size = (800, 600))
        panel = wx.Panel(self, -1)
        self.conf=wx.StaticBox(panel, -1, '配置信息')
        self.confSizer = wx.StaticBoxSizer(self.conf, wx.VERTICAL)
        nmbox = wx.BoxSizer(wx.HORIZONTAL)
        hmbox= wx.BoxSizer(wx.VERTICAL)
        self.actl = wx.StaticBox(panel, -1, '运行数据')
        self.actlSizer = wx.StaticBoxSizer(self.actl, wx.VERTICAL)
        self.cnt=wx.StaticBox(panel, -1, '控制')
        self.cntSizer = wx.StaticBoxSizer(self.cnt, wx.VERTICAL)
        self.label_patch = wx.StaticText(panel,wx.ID_ANY,"文件目录和名字")
        self.label_patch.SetForegroundColour("Red")
        self.label_patch.SetBackgroundColour("Black")
        font=wx.Font(14,wx.DECORATIVE,wx.ITALIC,wx.NORMAL)
        self.label_patch.SetFont(font)
        self.label_sampling  = wx.StaticText(panel,wx.ID_ANY,"采样间隔")
        self.label_sampling .SetForegroundColour("Red")
        self.label_sampling .SetBackgroundColour("Black")
        self.label_sampling .SetFont(font)
        self.label_union  = wx.StaticText(panel,wx.ID_ANY,"Union ID")
        self.label_union .SetForegroundColour("Red")
        self.label_union .SetBackgroundColour("Black")
        self.label_union .SetFont(font)
        self.label_crl  = wx.StaticText(panel,wx.ID_ANY,"设备所在环境")
        self.label_crl .SetForegroundColour("Red")
        self.label_crl .SetBackgroundColour("Black")
        self.label_crl .SetFont(font)
        self.label_sampling_times  = wx.StaticText(panel,wx.ID_ANY,"采样次数")
        self.label_sampling_times .SetForegroundColour("Red")
        self.label_sampling_times .SetBackgroundColour("Black")
        self.label_sampling_times .SetFont(font)
        self.acturl_sampling_times  = wx.StaticText(panel,wx.ID_ANY,"当前采样次数",(400, 240))
        self.acturl_sampling_times .SetForegroundColour("Red")
        self.acturl_sampling_times .SetBackgroundColour("Black")
        self.acturl_sampling_times .SetFont(font)
        self.label_drif  = wx.StaticText(panel,wx.ID_ANY,"抖动阀值标记")
        self.label_drif .SetForegroundColour("Red")
        self.label_drif .SetBackgroundColour("Black")
        self.label_drif .SetFont(font)
        self.patch = wx.TextCtrl(panel,value="d:\Weight_Get.xls", style=wx.TE_LEFT)
        self.sampling = wx.TextCtrl(panel, value="5", style=wx.TE_LEFT)
        self.union = wx.TextCtrl(panel,value="02c000813e71eab9", style=wx.TE_LEFT)
        self.dev_url=wx.Choice(panel,size = (100, 30),choices =["测试环境","生产环境"])
        self.sampling_times = wx.TextCtrl(panel,value="10000", style=wx.TE_LEFT)
        self.drif = wx.TextCtrl(panel,value="5", style=wx.TE_LEFT)
        self.acturl_sampling = wx.TextCtrl(panel, style=wx.TE_LEFT)
        self.running = wx.Button(panel,-1, "开始")
        self.stop = wx.Button(panel, -1, "结束")
        # self.Bind(wx.EVT_TEXT, self.Patch_OnEnter, self.patch)
        # self.Bind(wx.EVT_TEXT, self.Sampling_OnEnter, self.sampling)
        # self.Bind(wx.EVT_TEXT, self.Union_OnEnter, self.union)
        # self.Bind(wx.EVT_TEXT, self.Sampling_Times_OnEnter, self.sampling_times)
        # self.Bind(wx.EVT_TEXT, self.Drif_OnEnter, self.drif)
        self.Bind(wx.EVT_CHOICE,self.DEV_URL, self.dev_url)
        self.Bind(wx.EVT_BUTTON,self.RunButton,self.running)
        self.Bind(wx.EVT_BUTTON, self.StopButton, self.stop)
        self.int_date=["0","0","0","0","0"]
        self.acturl_data=wx.ComboBox(panel, -1, value="当前数据",size=(100,100), choices=self.int_date, style=wx.CB_SIMPLE)
        self.acturl_data .SetForegroundColour("Red")
        self.acturl_data .SetBackgroundColour("White")
        self.acturl_data .SetFont(font)

        self.weigth_stop=0
        self.Show(True)
    #def Patch_OnEnter(self,evt):
        #self.file_path= self.patch.GetValue()
    #def Sampling_OnEnter(self,evt):
        #self.Times=self.sampling.GetValue()
    #def Union_OnEnter(self, evt):
        #self.Union_ID = self.union.GetValue()
    #def Sampling_Times_OnEnter(self, evt):
        #self.SamplingTimes = self.sampling_times.GetValue()
    #def Drif_OnEnter(self, evt):
        #self.Drif = self.drif.GetValue()
    def DEV_URL(self,evt):
        index = evt.GetEventObject().GetSelection()
        if (index == 0):
            self.url="http://10.4.32.114:8085/rrpc"
        elif (index == 1):
            self.url ="http://w.vegcloud.xyz:8085/rrpc"

    def wirt_cell_value(self,file_patch, cow, col, value=[]):
        tmy = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        tmd = time.strftime('%H-%M-%S', time.localtime(time.time()))
        try:
            rb1 = xlrd.open_workbook(file_patch, formatting_info=True)
            wb1 = copy(rb1)
            ws1 = wb1.get_sheet(0)
            ws1.write(cow, 0, tmy)
            ws1.write(cow, 1, tmd)
            for i in range(len(value)):
                ws1.write(cow, col + i, value[i])
            wb1.save(file_patch)
        except:
            Mymsg = wx.MessageBox("文件打开失败\n 文件被打开或者不存在", "Message box", style=wx.OK | wx.CANCEL)
            return True


    def read_cell_value(self,file_patch, cow, col):
        try:
            rb1 = xlrd.open_workbook(file_patch, formatting_info=True)
            sheet = rb1.sheet_by_index(0)
            self.cell_value = sheet.row(cow)[col].value
            return self.cell_value
        except:
            Mymsg = wx.MessageBox("文件打开失败\n文件被打开或者不存在", "Message box", style=wx.OK | wx.CANCEL)
            return True

    def styel(self,colourtype):
        self.colour_style = xlwt.XFStyle()
        pattern_clour = xlwt.Pattern()  # 创建pattern_red
        pattern_clour.pattern = xlwt.Pattern.SOLID_PATTERN  # 设置填充模式为全部填充
        pattern_clour.pattern_fore_colour = int(colourtype)  # 设置填充颜色为
        self.colour_style.pattern = pattern_clour
        return self.colour_style

    def wirt_cell_value_styel(self,file_patch, cow, col, styel, value=[]):
        try:
            tmy = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            tmd = time.strftime('%H-%M-%S', time.localtime(time.time()))
            rb1 = xlrd.open_workbook(file_patch, formatting_info=True)
            wb1 = copy(rb1)
            ws1 = wb1.get_sheet(0)
            ws1.write(cow, 0, tmy, styel)
            ws1.write(cow, 1, tmd, styel)
            for i in range(len(value)):
                ws1.write(cow, col + i, value[i], styel)
            wb1.save(file_patch)
        except:
            Mymsg = wx.MessageBox("文件打开失败\n 文件被打开或者不存在", "Message box", style=wx.OK | wx.CANCEL)
            return True

    def list_cmp(self,list1,list2):
        for i in range (0,5):
            try:
                acturl_drif = abs(int(list1[i]) - int(list2[i]))
                if (acturl_drif>int(self.Drif)):
                    return True
            except:
                return True
    def RunButton(self,evt):
        self.weigth_stop = 0
        self.loop_times = 0
        self.file_path = self.patch.GetValue()
        self.Times = self.sampling.GetValue()
        self.Union_ID = self.union.GetValue()
        self.Drif = self.drif.GetValue()
        self.SamplingTimes = self.sampling_times.GetValue()
        Get_data=threading.Thread(target=self.Save_date)
        Get_data.setDaemon(True)
        Get_data.start()
    def StopButton(self,evt):
        self.weigth_stop=1
        self.loop_times=0
    def Save_date(self):
        payload1 = "{\r\n    \"devname\":" + "\"" + self.Union_ID + "\"" + ",\r\n    \"req\": {\r\n        \"A\": 107,\r\n        \"P\":{\r\n        }\r\n    }\r\n}"
        headers1 = {
            'content-type': "application/json",
            'authorization': "Basic YWRtaW46Y2poeXkzMDA=",
            'cache-control': "no-cache",
            'postman-token': "822de31b-855e-3d9a-a6e0-c1d734e80df5"
        }
        book = xlwt.Workbook(encoding='utf-8', style_compression=0)
        sheet1 = book.add_sheet('GetWeight', cell_overwrite_ok=True)
        for x in range(5):
            sheet1.write(0, x + 2, "第" + str(x + 1) + "层")
        book.save(self.file_path)
        loop_times = 1
        while True:
            try:
                response1 = requests.request("POST", self.url, data=payload1, headers=headers1)
                js_to_py_1 = json.loads(response1.text)
                all_weight = js_to_py_1["output"]
                weight_dict = {}
                weight_list = range(0, 5)
                old_weight_list = range(0, 5)
                for i in range(0, len(all_weight)):
                    weight_key = all_weight[i]["weighid"]
                    weight_value = all_weight[i]["weight"]
                    weight_dict[weight_key] = weight_value
                for j in range(0, 5):
                    weigh_id = "010" + str(j + 1) + "01"
                    weight_list[j] = int(weight_dict[weigh_id])
                    self.acturl_data.SetString(j, str(weight_list[j]))
            except:
                Mymsg=wx.MessageBox("设备失连请检查网络","Message box",style=wx.OK | wx.CANCEL)
                for j in range(0, 5):
                    weight_list = [0, 0, 0, 0, 0]
                    self.acturl_data.SetString(j, str(weight_list[j]))
            if (loop_times > 2):
                for z in range(0, 5):
                    try:
                        cell_value = self.read_cell_value(self.file_path, loop_times - 1, z + 2)
                        old_weight_list[z] = int(cell_value)
                    except:
                        old_weight_list=[0,0,0,0,0]
                if(self.list_cmp(weight_list,old_weight_list)):
                    styel1 = self.styel(2)
                    self.wirt_cell_value_styel(self.file_path, loop_times , 2, styel1, weight_list)
                else:
                    self.wirt_cell_value(self.file_path, loop_times , 2, weight_list)
            else:
                self.wirt_cell_value(self.file_path, loop_times , 2, weight_list)
            loop_times += 1
            self.acturl_sampling.SetValue(str(loop_times))
            if (loop_times == int(self.SamplingTimes) or self.weigth_stop == 1):
                break
            time.sleep(int(self.Times))


if __name__=="__main__":
    app = wx.App(True)
    frame = MainWindow(None, '温飘抖动测试工具')
    app.MainLoop()