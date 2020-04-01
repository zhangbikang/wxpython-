import sys
import json
import re
import time
import paramiko
import requests
import wx
import threading
from pubsub import pub
import os
import math
import urllib
from http import cookiejar
import serial



class ToolsWindow(wx.Frame):

    def __init__(self, parent, title):
        self.get_union_id = ""
        self.url = ""
        wx.Frame.__init__(self, parent, title=title, size=(1000, 650),
                          style=wx.CAPTION | wx.CLOSE_BOX | wx.MINIMIZE_BOX)

        self.init_panel = wx.Panel(self, -1)
        self.SetBackgroundColour("#8F8FBC")
        self.init_panel.SetBackgroundColour("#8F8FBC")
        self.index_union_id = wx.StaticText(self.init_panel, -1, "设备Union ID", style=wx.ALIGN_CENTER)
        self.font_init = wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.LIGHT)
        self.index_union_id.SetFont(self.font_init)
        self.index_union_id.SetForegroundColour("Red")
        self.online_index = wx.StaticText(self.init_panel, -1, "设备在线状态", style=wx.ALIGN_CENTER)
        self.online_index.SetFont(self.font_init)
        self.online_index.SetForegroundColour("Red")
        self.online_status = wx.StaticText(self.init_panel, -1, "", style=wx.ALIGN_CENTER)
        self.online_status.SetFont(self.font_init)
        # self.font_init_panel.SetBackgroundColour("#00FFFF")
        # self.font_init_panel.SetForegroundColour("Red")
        self.index_dev_id = wx.StaticText(self.init_panel, -1, "设备ID", style=wx.ALIGN_CENTER)
        self.index_dev_id.SetFont(self.font_init)
        self.index_dev_id.SetForegroundColour("Red")
        self.dev_id = wx.TextCtrl(self.init_panel, -1, value="", style=0)
        self.dev_id.SetFont(self.font_init)
        self.dev_id.SetForegroundColour("Red")
        self.Union_id = wx.StaticText(self.init_panel, -1, "", style=wx.ALIGN_CENTER)
        self.Union_id.SetFont(self.font_init)
        self.Union_id.SetForegroundColour("Red")
        self.begin = wx.Button(self.init_panel, -1, "确定", style=wx.BU_BOTTOM)
        self.begin.SetFont(self.font_init)
        self.begin.SetForegroundColour("Blue")
        self.Bind(wx.EVT_BUTTON, self.begin_Click, self.begin)
        self.index_url = wx.StaticText(self.init_panel, -1, "设备环境", style=wx.ALIGN_CENTER)
        self.index_url.SetFont(self.font_init)
        self.index_url.SetForegroundColour("Red")
        self.dev_url = wx.Choice(self.init_panel, choices=["测试环境", "生产环境"])
        self.dev_url.SetFont(self.font_init)
        self.dev_url.SetForegroundColour("Red")
        self.Bind(wx.EVT_CHOICE, self.DEV_URL, self.dev_url)
        self.static_box = wx.StaticBox(self.init_panel, -1, "设备信息", size=(980, 0), style=wx.ALIGN_CENTER)
        self.static_box.SetForegroundColour("#EAADEA")
        self.init_box_v = wx.BoxSizer(wx.VERTICAL)
        self.union_id_box_h = wx.BoxSizer(wx.HORIZONTAL)
        self.union_id_statis_box = wx.StaticBox(self.init_panel, -1, "设备在线状态", size=(900, 0), style=wx.ALIGN_CENTER)
        self.union_id_statis_box_sizer = wx.StaticBoxSizer(self.union_id_statis_box, wx.HORIZONTAL)
        self.union_id_statis_box.SetForegroundColour("#EAADEA")
        self.union_id_box_h.Add(self.index_union_id, 1, wx.ALL | wx.EXPAND, 2)
        self.union_id_box_h.Add(self.Union_id, 1, wx.ALL | wx.EXPAND, 2)
        self.union_id_box_h.Add(self.online_index, 1, wx.ALL | wx.EXPAND, 2)
        self.union_id_box_h.Add(self.online_status, 1, wx.ALL | wx.EXPAND, 2)
        self.union_id_statis_box_sizer.Add(self.union_id_box_h, 1, wx.ALL | wx.EXPAND, 2)
        self.dev_config_sizer = wx.StaticBoxSizer(self.static_box, wx.HORIZONTAL)
        self.dev_info_H = wx.BoxSizer(wx.HORIZONTAL)
        self.dev_info_V = wx.BoxSizer(wx.VERTICAL)
        self.dev_info_H.Add(self.index_dev_id, 1, wx.ALL | wx.EXPAND, 2)
        self.dev_info_H.Add(self.dev_id, 1, wx.ALL | wx.EXPAND, 2)
        self.dev_info_H.Add(self.index_url, 1, wx.ALL | wx.EXPAND, 2)
        self.dev_info_H.Add(self.dev_url, 1, wx.ALL | wx.EXPAND, 2)
        self.dev_info_H.Add(self.begin, 1, wx.ALL | wx.EXPAND, 2)
        self.dev_config_sizer.Add(self.dev_info_H, 1, wx.ALL | wx.EXPAND, 2)
        self.init_box_v.Add(self.dev_config_sizer, 1, wx.ALL | wx.EXPAND, 2)
        self.init_box_v.Add(self.union_id_statis_box_sizer, 1, wx.ALL | wx.EXPAND, 2)
        self.init_panel.SetSizer(self.init_box_v)
        self.init_panel.Fit()
        self.operator_muen_size = self.init_panel.GetSize()
        self.operator_muen_panel = wx.Panel(self, -1, pos=(0, self.operator_muen_size[1] + 5), size=(985, 0))
        self.operator_muen_panel.SetBackgroundColour("#8F8FBC")
        self.door_lock = wx.Button(self.operator_muen_panel, -1, "门锁操作", style=wx.BU_BOTTOM)
        self.door_lock.SetFont(self.font_init)
        self.door_lock.SetForegroundColour("Blue")
        self.weigh = wx.Button(self.operator_muen_panel, -1, "秤盘操作", style=wx.BU_BOTTOM)
        self.weigh.SetFont(self.font_init)
        self.weigh.SetForegroundColour("Blue")
        self.vioce = wx.Button(self.operator_muen_panel, -1, "语音操作", style=wx.BU_BOTTOM)
        self.vioce.SetFont(self.font_init)
        self.vioce.SetForegroundColour("Blue")
        self.celluar = wx.Button(self.operator_muen_panel, -1, "信号操作", style=wx.BU_BOTTOM)
        self.celluar.SetFont(self.font_init)
        self.celluar.SetForegroundColour("Blue")
        self.com_ser=wx.Button(self.operator_muen_panel,-1,"直连称重",style=wx.BU_BOTTOM)
        self.com_ser.SetFont(self.font_init)
        self.com_ser.SetForegroundColour("Blue")
        self.Bind(wx.EVT_BUTTON, self.lock_operator, self.door_lock)
        self.Bind(wx.EVT_BUTTON, self.weigh_operator, self.weigh)
        self.Bind(wx.EVT_BUTTON, self.vioce_operator, self.vioce)
        self.Bind(wx.EVT_BUTTON, self.cellular_operator, self.celluar)
        self.Bind(wx.EVT_BUTTON,self.com_ser_operator,self.com_ser)
        self.door_lock.Disable()
        self.weigh.Disable()
        self.vioce.Disable()
        self.celluar.Disable()
        self.static_operation = wx.StaticBox(self.operator_muen_panel, -1, "操作菜单")
        self.static_operation.SetForegroundColour("#EAADEA")
        self.static_operation_sizer = wx.StaticBoxSizer(self.static_operation, wx.VERTICAL)
        self.operator_muen_panel_Box_H = wx.BoxSizer(wx.VERTICAL)
        self.operator_muen_panel_Box_H.Add(self.door_lock, 1, wx.ALL | wx.SHAPED | wx.ALIGN_CENTER_HORIZONTAL, 2)
        self.operator_muen_panel_Box_H.Add(self.weigh, 1, wx.ALL | wx.SHAPED | wx.ALIGN_CENTER_HORIZONTAL, 2)
        self.operator_muen_panel_Box_H.Add(self.vioce, 1, wx.ALL | wx.SHAPED | wx.ALIGN_CENTER_HORIZONTAL, 2)
        self.operator_muen_panel_Box_H.Add(self.celluar, 1, wx.ALL | wx.SHAPED | wx.ALIGN_CENTER_HORIZONTAL, 2)
        self.operator_muen_panel_Box_H.Add(self.com_ser, 1, wx.ALL | wx.SHAPED | wx.ALIGN_CENTER_HORIZONTAL, 2)
        self.static_operation_sizer.Add(self.operator_muen_panel_Box_H, 1,
                                        wx.ALL | wx.SHAPED | wx.ALIGN_CENTER_HORIZONTAL, 2)
        self.operator_muen_panel.SetSizer(self.static_operation_sizer)
        self.operator_muen_panel.Fit()
        self.system_dlg = wx.MessageDialog(self.init_panel, "", caption="操作提示", style=wx.OK)
        self.system_dlg.SetFont(self.font_init)
        self.system_dlg.SetForegroundColour("Red")
        self.user_name_dlg = wx.TextEntryDialog(self.init_panel, "请输入用户名", "登入设备用户名")
        self.user_name_dlg.SetFont(self.font_init)
        self.user_name_dlg.SetForegroundColour("Red")
        self.pw_dlg = wx.TextEntryDialog(self.init_panel, "请输入密码", "登入设备密码",
                                         style=wx.TE_PASSWORD | wx.OK | wx.CANCEL | wx.CENTER)
        self.pw_dlg.SetFont(self.font_init)
        self.pw_dlg.SetForegroundColour("Red")
        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def begin_Click(self, evt):
        self.Union_id.SetLabel("")
        self.online_status.SetLabel("")
        self.online_status.SetBackgroundColour("")
        self.door_lock.Disable()
        self.weigh.Disable()
        self.vioce.Disable()
        self.celluar.Disable()
        self.get_dev_id = self.dev_id.GetValue()
        self.get_union_id=""
        self.Refresh()

        if self.url != "" and self.get_dev_id != "":
            try:
                # login_url = "http://www.vegcloud.xyz:8500/login"
                cj = cookiejar.CookieJar()
                cookie_support = urllib.request.HTTPCookieProcessor(cj)
                opener = urllib.request.build_opener(cookie_support, urllib.request.HTTPHandler)
                urllib.request.install_opener(opener)
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
                    'Referer': self.web_Referer}
                postData = {"employee_id": "HZ03881", "employee_pass": "NetRing1"}
                postData = urllib.parse.urlencode(postData, encoding='gb2312').encode('gb2312')
                request_login = urllib.request.Request(self.web_login_url, postData, headers)
                response = urllib.request.urlopen(request_login)
                login_text_org = response.read().decode()
                login_text = json.loads(login_text_org)
                login_token = login_text["token"]
                if login_text["result"].lower() == "success":
                    time.sleep(1)
                    # query_dev_url = "http://www.vegcloud.xyz:8500/api/query_dev"
                    postQueryDev = {"access_token": login_token,
                                    "command": "query_commodity_info",
                                    "jwtauth_auth_ret_type": "json"}

                    postQueryDev = urllib.parse.urlencode(postQueryDev, encoding='gb2312').encode('gb2312')
                    request_QueryDev = urllib.request.Request(self.web_query_dev_url, postQueryDev, headers)
                    response_QueryDev = urllib.request.urlopen(request_QueryDev)
                    query_dev_org = response_QueryDev.read().decode()
                    query_dev_org_dict = json.loads(query_dev_org)
                    dev_info = query_dev_org_dict["output"]
                    if query_dev_org_dict["msg"].lower() == "success":
                        for key, value in dev_info.items():
                            value_dict = dev_info[key]
                            for subkey, subvalue in value_dict.items():
                                dev_id = value_dict["dev_id"]
                                online_status = value_dict["phy_state"]
                                if dev_id == int(self.dev_id.GetValue()):
                                    self.get_union_id = key
                                    self.Union_id.SetLabel(key)
                                    if online_status == 1:
                                        self.online_status.SetLabel("在线")
                                        self.online_status.SetBackgroundColour("Green")
                                    else:
                                        self.online_status.SetLabel("离线")
                                        self.online_status.SetBackgroundColour("Red")
                                        break
                                    self.door_lock.Enable()
                                    self.weigh.Enable()
                                    self.vioce.Enable()
                                    self.celluar.Enable()
                                    break
                        if  self.get_union_id =="":
                            self.Union_id.SetLabel("")
                            self.online_status.SetLabel("")
                            self.system_dlg.SetMessage("设备ID不存在！！！")
                            self.system_dlg.ShowModal()
                        return
                    else:
                        self.Union_id.SetLabel("")
                        self.online_status.SetLabel("")
                        self.system_dlg.SetMessage("获取Union ID 失败")
                        self.system_dlg.ShowModal()
                        return

                else:
                    self.Union_id.SetLabel("")
                    self.online_status.SetLabel("")
                    self.system_dlg.SetMessage("获取Union ID 失败")
                    self.system_dlg.ShowModal()
                    return
            except:
                self.Union_id.SetLabel("")
                self.online_status.SetLabel("")
                self.system_dlg.SetMessage("获取Union ID 失败")
                self.system_dlg.ShowModal()
                return

            # self.static_operation.SetBackgroundColour("#238E23")

        elif self.url == "":
            self.system_dlg.SetMessage("请选择设备所在环境 !!!")
            self.system_dlg.ShowModal()
        elif self.get_dev_id == "":
            self.system_dlg.SetMessage("请输入设备 ID !!!")
            self.system_dlg.ShowModal()
    #直连称重操作
    def com_ser_operator(self,evt):
        self.operator_muen_panel.Hide()
        self.init_panel.Hide()
        self.com_ser_panel = wx.ScrolledWindow(self, -1, pos=(0, 0), size=(960, 500))
        #self.weigh_operator_tip_panel = wx.Panel(self, -1, pos=(0, self.operator_muen_size[1] + 5), size=(980, 20))
        #self.weigh_operator_tip_panel.SetBackgroundColour("#000000")
        self.system_message = wx.StaticText(self.com_ser_panel, -1, "", style=wx.ALIGN_CENTER_HORIZONTAL|wx.ST_NO_AUTORESIZE)
        self.font_weigh_operator_tip = wx.Font(20, wx.DECORATIVE, wx.NORMAL, wx.LIGHT)
        self.system_message.SetFont(self.font_weigh_operator_tip)
        self.system_message.SetForegroundColour("Red")
        self.system_message.SetBackgroundColour("Black")
        self.system_message_box=wx.BoxSizer(wx.HORIZONTAL)
        self.system_message_box.Add(self.system_message,1,wx.ALL|wx.EXPAND,2)
        self.font_weight = wx.Font(15, wx.DECORATIVE, wx.NORMAL, wx.LIGHT)
        self.com_ser_panel.SetScrollbar(1,1,1000,2000)
        self.com_ser_panel.SetScrollRate(10,10)
        self.com_ser_panel.SetBackgroundColour("#D8BFD8")
        self.index_com=wx.StaticText(self.com_ser_panel,-1,"COM口")
        self.index_com.SetFont(self.font_weight)
        self.value_com=wx.TextCtrl(self.com_ser_panel,-1,"")
        self.index_speed=wx.StaticText(self.com_ser_panel,-1,"速率")
        self.index_speed.SetFont(self.font_weight)
        self.value_speed=wx.TextCtrl(self.com_ser_panel,-1,"9600")
        self.enter_button=wx.Button(self.com_ser_panel,-1,"开始")
        self.enter_button.SetFont(self.font_weight)
        self.Bind(wx.EVT_BUTTON,self.open_com,self.enter_button)
        self.stop_button=wx.Button(self.com_ser_panel,-1,"停止")
        self.stop_button.SetFont(self.font_weight)
        self.Bind(wx.EVT_BUTTON,self.stop_process,self.stop_button)
        self.clear=wx.Button(self.com_ser_panel,-1,"清零")
        self.Bind(wx.EVT_BUTTON,self.direct_clear_process,self.clear)
        self.display_value=wx.StaticText(self.com_ser_panel,-1,"0",style=wx.ALIGN_CENTER_HORIZONTAL|wx.ST_NO_AUTORESIZE)
        self.display_value.SetForegroundColour("red")
        self.display_value.SetFont(self.font_weight)
        self.config_static_box=wx.StaticBox(self.com_ser_panel,-1,"配置")
        self.config_static_box_sizer=wx.StaticBoxSizer(self.config_static_box,wx.VERTICAL)
        self.display_static_box=wx.StaticBox(self.com_ser_panel,-1,"重量")
        self.display_static_box_sizer=wx.StaticBoxSizer(self.display_static_box,wx.VERTICAL)
        self.control_static_box=wx.StaticBox(self.com_ser_panel,-1,"控制")
        self.control_static_box_sizer=wx.StaticBoxSizer(self.control_static_box,wx.VERTICAL)
        self.com_ser_back=wx.Button(self.com_ser_panel,-1,"返回")
        self.com_ser_back.SetFont(self.font_weight)
        self.Bind(wx.EVT_BUTTON,self.ser_com_back_int,self.com_ser_back)
        self.config_h_box=wx.BoxSizer(wx.HORIZONTAL)
        self.calc_V_box=wx.BoxSizer(wx.VERTICAL)
        self.control_h_box=wx.BoxSizer(wx.HORIZONTAL)
        self.config_h_box.Add(self.index_com,1,wx.ALL|wx.EXPAND,2)
        self.config_h_box.Add(self.value_com, 1, wx.ALL | wx.EXPAND, 2)
        self.config_h_box.Add(self.index_speed, 1, wx.ALL | wx.EXPAND, 2)
        self.config_h_box.Add(self.value_speed, 1, wx.ALL | wx.EXPAND, 2)
        self.config_static_box_sizer.Add(self.config_h_box,1,wx.ALL|wx.EXPAND,2)
        self.display_static_box_sizer.Add(self.display_value,1,wx.ALL|wx.EXPAND,2)
        #self.display_static_box_sizer.Add(self.display_static_box,1,wx.ALL|wx.EXPAND,2)
        self.control_h_box.Add(self.enter_button,1,wx.ALL|wx.EXPAND,2)
        self.control_h_box.Add(self.stop_button,1,wx.ALL|wx.EXPAND,2)
        self.control_h_box.Add(self.clear, 1, wx.ALL | wx.EXPAND, 2)
        self.control_static_box_sizer.Add(self.control_h_box,1,wx.ALL|wx.EXPAND,2)
        self.calc_V_box.Add(self.config_static_box_sizer,0,wx.ALL|wx.EXPAND,2)
        self.calc_V_box.Add(self.display_static_box_sizer,0,wx.ALL|wx.EXPAND,2)
        self.calc_V_box.Add(self.control_static_box_sizer,0,wx.ALL|wx.EXPAND,2)
        self.calc_V_box.Add(self.com_ser_back,0,wx.ALL|wx.EXPAND,2)
        self.com_ser_panel.SetSizer(self.calc_V_box)
        self.com_ser_panel.Layout()
        self.com_ser_panel.Fit()
        self.stop_button.Disable()
        self.clear.Disable()
        pub.subscribe(self.weight_update, "com_update")
    def weight_update(self,msg):
        self.display_value.SetLabel(str(msg))
    def open_com(self,evt):
        try:
            self.back_contor=True
            self.control_index=True
            self.direct_weight_base=0
            self.com_num=self.value_com.GetValue()
            self.com_speed=int(self.value_speed.GetValue())
            self.com_export_t=threading.Thread(target=self.com_process)
            self.com_export_t.start()
            self.com_ser_back.Disable()
            self.enter_button.Disable()
        except:
            self.system_dlg.SetMessage("串口打开失败")
            self.system_dlg.ShowModal()
            self.com_ser_back.Enable()
            self.enter_button.Enable()
            return

    def com_process(self):
        try:
            wx.CallAfter(pub.sendMessage, "com_update", msg="串口初始化中...")
            serial_com = serial.Serial(self.com_num, self.com_speed, timeout=2)
            serial_com.close()
            time.sleep(5)
            com_status = serial_com.open()
            time.sleep(5)
            # print (com_status)
            # print (serial_com.port)
            # print(serial_com.get_settings())
            while True:
                msg = serial_com.readline()
                self.stop_button.Enable()
                self.clear.Enable()
                if msg:
                    org = msg.decode()
                    weight_org = re.findall("(\d+)", org)
                    if weight_org:
                        self.direct_current_weight = int(weight_org[0])
                        change_weight=self.direct_current_weight-self.direct_weight_base
                        wx.CallAfter(pub.sendMessage, "com_update", msg=change_weight)
                if not self.control_index:
                    serial_com.close()
                    break
        except:
            self.system_dlg.SetMessage("串口打开失败")
            self.system_dlg.ShowModal()
            self.com_ser_back.Enable()
            self.enter_button.Enable()
            wx.CallAfter(pub.sendMessage, "com_update", msg="")
            return
    def stop_process(self,evt):
        self.control_index = False
        self.back_contor=False
        while True:
            if not self.com_export_t.isAlive():
                wx.CallAfter(pub.sendMessage, "com_update", msg="停止")
                break
        self.enter_button.Enable()
        self.com_ser_back.Enable()
    def direct_clear_process(self,evt):
        self.direct_weight_base=self.direct_current_weight
    def ser_com_back_int(self,evt):
            self.com_ser_panel.Destroy()
            self.init_panel.Show()
            self.operator_muen_panel.Show()
    # 秤盘操作
    def weigh_operator(self, evt):
        self.operator_muen_panel.Hide()
        self.init_panel.Hide()
        self.weigh_panel = wx.ScrolledWindow(self, -1, pos=(0, 0), size=(960, 500))
        #self.weigh_operator_tip_panel = wx.Panel(self, -1, pos=(0, self.operator_muen_size[1] + 5), size=(980, 20))
        #self.weigh_operator_tip_panel.SetBackgroundColour("#000000")
        self.system_message = wx.StaticText(self.weigh_panel, -1, "", style=wx.ALIGN_CENTER_HORIZONTAL|wx.ST_NO_AUTORESIZE)
        self.font_weigh_operator_tip = wx.Font(20, wx.DECORATIVE, wx.NORMAL, wx.LIGHT)
        self.system_message.SetFont(self.font_weigh_operator_tip)
        self.system_message.SetForegroundColour("Red")
        self.system_message.SetBackgroundColour("Black")
        self.system_message_box=wx.BoxSizer(wx.HORIZONTAL)
        self.system_message_box.Add(self.system_message,1,wx.ALL|wx.EXPAND,2)
        self.font_weigh = wx.Font(11, wx.DECORATIVE, wx.NORMAL, wx.LIGHT)
        self.weigh_panel.SetScrollbar(1,1,1000,2000)
        self.weigh_panel.SetScrollRate(10,10)
        self.weigh_panel.SetBackgroundColour("#D8BFD8")
        self.weigh_stability_box_h = wx.BoxSizer(wx.HORIZONTAL)
        self.goods_weight_box_h = wx.BoxSizer(wx.HORIZONTAL)
        self.get_weigh_weight_box_title_h = wx.BoxSizer(wx.HORIZONTAL)
        self.get_weigh_weight_box_actural_h_1 = wx.BoxSizer(wx.HORIZONTAL)
        self.get_weigh_weight_box_actural_h_2 = wx.BoxSizer(wx.HORIZONTAL)
        self.get_weigh_weight_box_actural_h_3 = wx.BoxSizer(wx.HORIZONTAL)
        self.get_weigh_weight_box_actural_h_4 = wx.BoxSizer(wx.HORIZONTAL)
        self.get_weigh_weight_box_actural_h_5 = wx.BoxSizer(wx.HORIZONTAL)
        self.weigh_box_v = wx.BoxSizer(wx.VERTICAL)
        self.weigh_floor = ["单第一层", "单第二层", "单第三层", "单第四层", "单第五层", "双左一层", "双右一层", "双左二层", "双右二层", "双左三层", "双右三层",
                            "双左四层", "双右四层", "双左五层", "双右五层"]
        self.weigh_floor_com = {"单第一层": 0, "单第二层": 2, "单第三层": 4, "单第四层": 6, "单第五层": 8, "双左一层": 0, "双右一层": 1, "双左二层": 2,
                                "双右二层": 3, "双左三层": 4, "双右三层": 5, "双左四层": 6, "双右四层": 7, "双左五层": 8, "双右五层": 9}
        self.floor_indx = {"单第一层": "010101", "单第二层": "010201", "单第三层": "010301", "单第四层": "010401", "单第五层": "010501",
                           "双左一层": "010101", "双右一层": "010102", "双左二层": "010201", "双右二层": "010202", "双左三层": "010301",
                           "双右三层": "010302", "双左四层": "010401", "双右四层": "010402", "双左五层": "010501", "双右五层": "010502"}
        self.weigh_stability_index = wx.ComboBox(self.weigh_panel, -1, "选择检测秤盘", choices=self.weigh_floor,style=wx.CB_DROPDOWN)
        self.weigh_stability_index.SetFont(self.font_weigh)
        self.weigh_stability_index.SetForegroundColour("Blue")
        self.weigh_stability_status_index = wx.StaticText(self.weigh_panel, -1, "状态")
        self.weigh_stability_status_index.SetFont(self.font_weigh)
        self.weigh_stability_status_index.SetForegroundColour("Blue")
        self.weigh_stability_status_value = wx.StaticText(self.weigh_panel, -1)
        self.weigh_stability_status_value.SetFont(self.font_weigh)
        self.weigh_stability_status_value.SetForegroundColour("Blue")
        self.weigh_stability_float_index = wx.StaticText(self.weigh_panel, -1, "浮动值")
        self.weigh_stability_float_index.SetFont(self.font_weigh)
        self.weigh_stability_float_index.SetForegroundColour("Blue")
        self.weigh_stability_float_value = wx.StaticText(self.weigh_panel, -1)
        self.weigh_stability_float_value.SetFont(self.font_weigh)
        self.weigh_stability_float_value.SetForegroundColour("Blue")
        self.weigh_stability_button = wx.Button(self.weigh_panel, -1, "检测")
        self.weigh_stability_button.SetFont(self.font_weigh)
        self.weigh_stability_button.SetForegroundColour("Blue")
        self.Bind(wx.EVT_BUTTON, self.weigh_stability, self.weigh_stability_button)
        self.weigh_stability_box = wx.StaticBox(self.weigh_panel, -1, "秤盘稳定性检测")
        self.weigh_stability_box_size = wx.StaticBoxSizer(self.weigh_stability_box, wx.VERTICAL)
        self.weigh_stability_box_h.Add(self.weigh_stability_index, 1, wx.ALL | wx.EXPAND, 2)
        self.weigh_stability_box_h.Add(self.weigh_stability_status_index, 1, wx.ALL | wx.EXPAND, 2)
        self.weigh_stability_box_h.Add(self.weigh_stability_status_value, 1, wx.ALL | wx.EXPAND, 2)
        self.weigh_stability_box_h.Add(self.weigh_stability_float_index, 1, wx.ALL | wx.EXPAND, 2)
        self.weigh_stability_box_h.Add(self.weigh_stability_float_value, 1, wx.ALL | wx.EXPAND, 2)
        self.weigh_stability_box_h.Add(self.weigh_stability_button, 1, wx.ALL | wx.EXPAND, 2)
        self.weigh_stability_box_size.Add(self.weigh_stability_box_h, 1, wx.ALL | wx.EXPAND, 2)
        self.goods_weight_index = wx.ComboBox(self.weigh_panel, -1, "选择商品放置的秤盘", choices=self.weigh_floor,style=wx.CB_DROPDOWN)
        self.goods_weight_index.SetFont(self.font_weigh)
        self.goods_weight_index.SetForegroundColour("Blue")
        self.actual_goods_weight_index = wx.StaticText(self.weigh_panel, -1, "秤盘读数")
        self.actual_goods_weight_index.SetFont(self.font_weigh)
        self.actual_goods_weight_index.SetForegroundColour("Blue")
        self.actual_goods_weight_value = wx.StaticText(self.weigh_panel, -1, "")
        self.actual_goods_weight_value.SetFont(self.font_weigh)
        self.actual_goods_weight_value.SetForegroundColour("Blue")
        self.goods_weight_button = wx.Button(self.weigh_panel, -1, "开始")
        self.Bind(wx.EVT_BUTTON, self.calc_goods_weight, self.goods_weight_button)
        self.goods_weight_button.SetFont(self.font_weigh)
        self.goods_weight_button.SetForegroundColour("Blue")
        self.clear_button=wx.Button(self.weigh_panel,-1,"归零")
        self.clear_button.SetFont(self.font_weigh)
        self.clear_button.SetForegroundColour("Blue")
        self.Bind(wx.EVT_BUTTON,self.clear_process,self.clear_button)
        self.stop_cal_weight=wx.Button(self.weigh_panel,-1,"停止")
        self.stop_cal_weight.SetFont(self.font_weigh)
        self.stop_cal_weight.SetForegroundColour("Blue")
        self.Bind(wx.EVT_BUTTON,self.stop_cal_weight_process,self.stop_cal_weight)
        self.goods_weight_box = wx.StaticBox(self.weigh_panel, -1, "商品称重")
        self.goods_weight_box_size = wx.StaticBoxSizer(self.goods_weight_box, wx.VERTICAL)
        self.goods_weight_box_h.Add(self.goods_weight_index, 1, wx.ALL | wx.EXPAND, 2)
        self.goods_weight_box_h.Add(self.actual_goods_weight_index, 1, wx.ALL | wx.EXPAND, 2)
        self.goods_weight_box_h.Add(self.actual_goods_weight_value, 1, wx.ALL | wx.EXPAND, 2)
        self.goods_weight_box_h.Add(self.goods_weight_button, 1, wx.ALL | wx.EXPAND, 2)
        self.goods_weight_box_h.Add(self.clear_button, 1, wx.ALL | wx.EXPAND, 2)
        self.goods_weight_box_h.Add(self.stop_cal_weight, 1, wx.ALL | wx.EXPAND, 2)
        self.goods_weight_box_size.Add(self.goods_weight_box_h, 1, wx.ALL | wx.EXPAND, 2)
        self.weight_attr_query_index=wx.StaticText(self.weigh_panel,-1,"属性查询")
        self.weight_attr_query_index.SetFont(self.font_weigh)
        self.weight_attr_query_index.SetForegroundColour("Blue")
        self.weight_attr_query_value=wx.StaticText(self.weigh_panel,-1,"")
        self.weight_attr_query_value.SetFont(self.font_weigh)
        self.weight_attr_query_value.SetForegroundColour("Blue")
        self.weight_attr_auery_button=wx.Button(self.weigh_panel,-1,"查询")
        self.weight_attr_auery_button.SetFont(self.font_weigh)
        self.weight_attr_auery_button.SetForegroundColour("Blue")
        self.Bind(wx.EVT_BUTTON,self.query_attr_weight,self.weight_attr_auery_button)
        self.weight_attr_set_index=wx.StaticText(self.weigh_panel,-1,"属性设置")
        self.weight_attr_set_index.SetFont(self.font_weigh)
        self.weight_attr_set_index.SetForegroundColour("Blue")
        self.weight_attr_set_value=wx.TextCtrl(self.weigh_panel,-1,"")
        self.weight_attr_set_value.SetFont(self.font_weigh)
        self.weight_attr_set_value.SetForegroundColour("Blue")
        self.weight_attr_set_button=wx.Button(self.weigh_panel,-1,"设置")
        self.weight_attr_set_button.SetFont(self.font_weigh)
        self.weight_attr_set_button.SetForegroundColour("Blue")
        self.Bind(wx.EVT_BUTTON,self.set_attr_weight,self.weight_attr_set_button)
        self.weight_attr_static_box=wx.StaticBox(self.weigh_panel,-1,"属性配置")
        self.weight_attr_static_box_sizer=wx.StaticBoxSizer(self.weight_attr_static_box,wx.VERTICAL)
        self.weight_attr_h_box_query=wx.BoxSizer(wx.HORIZONTAL)
        self.weight_attr_h_box_set=wx.BoxSizer(wx.HORIZONTAL)
        self.weight_attr_h_box_query.Add(self.weight_attr_query_index,1,wx.ALL|wx.EXPAND,2)
        self.weight_attr_h_box_query.Add(self.weight_attr_query_value, 1, wx.ALL | wx.EXPAND, 2)
        self.weight_attr_h_box_query.Add(self.weight_attr_auery_button, 1, wx.ALL | wx.EXPAND, 2)
        self.weight_attr_h_box_set.Add(self.weight_attr_set_index,1,wx.ALL|wx.EXPAND,2)
        self.weight_attr_h_box_set.Add(self.weight_attr_set_value, 1, wx.ALL | wx.EXPAND, 2)
        self.weight_attr_h_box_set.Add(self.weight_attr_set_button, 1, wx.ALL | wx.EXPAND, 2)
        self.weight_attr_static_box_sizer.Add(self.weight_attr_h_box_query,0,wx.ALL|wx.EXPAND,2)
        self.weight_attr_static_box_sizer.Add(self.weight_attr_h_box_set, 0, wx.ALL | wx.EXPAND, 2)
        self.devid_type_list = ["3112", "4100", "5100", "5200", "其他类型"]
        self.devide_type = wx.ComboBox(self.weigh_panel, -1, "选择设备类型", choices=self.devid_type_list,style=wx.CB_DROPDOWN)
        self.devide_type.SetFont(self.font_weigh)
        self.devide_type.SetForegroundColour("Blue")
        self.weigh_weight_button = wx.Button(self.weigh_panel, -1, "查询")
        self.Bind(wx.EVT_BUTTON, self.get_weigh_weight_send, self.weigh_weight_button)
        self.weigh_weight_button.SetFont(self.font_weigh)
        self.weigh_weight_button.SetForegroundColour("Blue")
        self.weigh_weight_index_1_l = wx.StaticText(self.weigh_panel, -1, "第一层左")
        self.weigh_weight_index_1_l.SetFont(self.font_weigh)
        self.weigh_weight_index_1_l.SetForegroundColour("Blue")
        self.weigh_weight_value_1_l = wx.StaticText(self.weigh_panel, -1, "0")
        self.weigh_weight_value_1_l.SetFont(self.font_weigh)
        self.weigh_weight_value_1_l.SetForegroundColour("Blue")
        self.weigh_weight_index_1_r = wx.StaticText(self.weigh_panel, -1, "第一层右")
        self.weigh_weight_index_1_r.SetFont(self.font_weigh)
        self.weigh_weight_index_1_r.SetForegroundColour("Blue")
        self.weigh_weight_value_1_r = wx.StaticText(self.weigh_panel, -1, "0")
        self.weigh_weight_value_1_r.SetFont(self.font_weigh)
        self.weigh_weight_value_1_r.SetForegroundColour("Blue")
        self.weigh_weight_index_2_l = wx.StaticText(self.weigh_panel, -1, "第二层左")
        self.weigh_weight_index_2_l.SetFont(self.font_weigh)
        self.weigh_weight_index_2_l.SetForegroundColour("Blue")
        self.weigh_weight_index_2_r = wx.StaticText(self.weigh_panel, -1, "第二层右")
        self.weigh_weight_index_2_r.SetFont(self.font_weigh)
        self.weigh_weight_index_2_r.SetForegroundColour("Blue")
        self.weigh_weight_value_2_l = wx.StaticText(self.weigh_panel, -1, "0")
        self.weigh_weight_value_2_l.SetFont(self.font_weigh)
        self.weigh_weight_value_2_l.SetForegroundColour("Blue")
        self.weigh_weight_value_2_r = wx.StaticText(self.weigh_panel, -1, "0")
        self.weigh_weight_value_2_r.SetFont(self.font_weigh)
        self.weigh_weight_value_2_r.SetForegroundColour("Blue")
        self.weigh_weight_index_3_l = wx.StaticText(self.weigh_panel, -1, "第三层左")
        self.weigh_weight_index_3_l.SetFont(self.font_weigh)
        self.weigh_weight_index_3_l.SetForegroundColour("Blue")
        self.weigh_weight_index_3_r = wx.StaticText(self.weigh_panel, -1, "第三层右")
        self.weigh_weight_index_3_r.SetFont(self.font_weigh)
        self.weigh_weight_index_3_r.SetForegroundColour("Blue")
        self.weigh_weight_value_3_l = wx.StaticText(self.weigh_panel, -1, "0")
        self.weigh_weight_value_3_l.SetFont(self.font_weigh)
        self.weigh_weight_value_3_l.SetForegroundColour("Blue")
        self.weigh_weight_value_3_r = wx.StaticText(self.weigh_panel, -1, "0")
        self.weigh_weight_value_3_r.SetFont(self.font_weigh)
        self.weigh_weight_value_3_r.SetForegroundColour("Blue")
        self.weigh_weight_index_4_l = wx.StaticText(self.weigh_panel, -1, "第四层左")
        self.weigh_weight_index_4_l.SetFont(self.font_weigh)
        self.weigh_weight_index_4_l.SetForegroundColour("Blue")
        self.weigh_weight_index_4_r = wx.StaticText(self.weigh_panel, -1, "第四层右")
        self.weigh_weight_index_4_r.SetFont(self.font_weigh)
        self.weigh_weight_index_4_r.SetForegroundColour("Blue")
        self.weigh_weight_value_4_l = wx.StaticText(self.weigh_panel, -1, "0")
        self.weigh_weight_value_4_l.SetFont(self.font_weigh)
        self.weigh_weight_value_4_l.SetForegroundColour("Blue")
        self.weigh_weight_value_4_r = wx.StaticText(self.weigh_panel, -1, "0")
        self.weigh_weight_value_4_r.SetFont(self.font_weigh)
        self.weigh_weight_value_4_r.SetForegroundColour("Blue")
        self.weigh_weight_index_5_l = wx.StaticText(self.weigh_panel, -1, "第五层左")
        self.weigh_weight_index_5_l.SetFont(self.font_weigh)
        self.weigh_weight_index_5_l.SetForegroundColour("Blue")
        self.weigh_weight_index_5_r = wx.StaticText(self.weigh_panel, -1, "第五层右")
        self.weigh_weight_index_5_r.SetFont(self.font_weigh)
        self.weigh_weight_index_5_r.SetForegroundColour("Blue")
        self.weigh_weight_value_5_l = wx.StaticText(self.weigh_panel, -1, "0")
        self.weigh_weight_value_5_l.SetFont(self.font_weigh)
        self.weigh_weight_value_5_l.SetForegroundColour("Blue")
        self.weigh_weight_value_5_r = wx.StaticText(self.weigh_panel, -1, "0")
        self.weigh_weight_value_5_r.SetFont(self.font_weigh)
        self.weigh_weight_value_5_r.SetForegroundColour("Blue")
        self.get_weigh_weight_box_actural_h_1.Add(self.weigh_weight_index_1_l, 1, wx.ALL | wx.EXPAND, 2)
        self.get_weigh_weight_box_actural_h_1.Add(self.weigh_weight_value_1_l, 1, wx.ALL | wx.EXPAND, 2)
        self.get_weigh_weight_box_actural_h_1.Add(self.weigh_weight_index_1_r, 1, wx.ALL | wx.EXPAND, 2)
        self.get_weigh_weight_box_actural_h_1.Add(self.weigh_weight_value_1_r, 1, wx.ALL | wx.EXPAND, 2)
        self.get_weigh_weight_box_actural_h_2.Add(self.weigh_weight_index_2_l, 1, wx.ALL | wx.EXPAND, 2)
        self.get_weigh_weight_box_actural_h_2.Add(self.weigh_weight_value_2_l, 1, wx.ALL | wx.EXPAND, 2)
        self.get_weigh_weight_box_actural_h_2.Add(self.weigh_weight_index_2_r, 1, wx.ALL | wx.EXPAND, 2)
        self.get_weigh_weight_box_actural_h_2.Add(self.weigh_weight_value_2_r, 1, wx.ALL | wx.EXPAND, 2)
        self.get_weigh_weight_box_actural_h_3.Add(self.weigh_weight_index_3_l, 1, wx.ALL | wx.EXPAND, 2)
        self.get_weigh_weight_box_actural_h_3.Add(self.weigh_weight_value_3_l, 1, wx.ALL | wx.EXPAND, 2)
        self.get_weigh_weight_box_actural_h_3.Add(self.weigh_weight_index_3_r, 1, wx.ALL | wx.EXPAND, 2)
        self.get_weigh_weight_box_actural_h_3.Add(self.weigh_weight_value_3_r, 1, wx.ALL | wx.EXPAND, 2)
        self.get_weigh_weight_box_actural_h_4.Add(self.weigh_weight_index_4_l, 1, wx.ALL | wx.EXPAND, 2)
        self.get_weigh_weight_box_actural_h_4.Add(self.weigh_weight_value_4_l, 1, wx.ALL | wx.EXPAND, 2)
        self.get_weigh_weight_box_actural_h_4.Add(self.weigh_weight_index_4_r, 1, wx.ALL | wx.EXPAND, 2)
        self.get_weigh_weight_box_actural_h_4.Add(self.weigh_weight_value_4_r, 1, wx.ALL | wx.EXPAND, 2)
        self.get_weigh_weight_box_actural_h_5.Add(self.weigh_weight_index_5_l, 1, wx.ALL | wx.EXPAND, 2)
        self.get_weigh_weight_box_actural_h_5.Add(self.weigh_weight_value_5_l, 1, wx.ALL | wx.EXPAND, 2)
        self.get_weigh_weight_box_actural_h_5.Add(self.weigh_weight_index_5_r, 1, wx.ALL | wx.EXPAND, 2)
        self.get_weigh_weight_box_actural_h_5.Add(self.weigh_weight_value_5_r, 1, wx.ALL | wx.EXPAND, 2)
        self.get_weigh_weight_box = wx.StaticBox(self.weigh_panel, -1, "查询秤盘当前重量")
        self.get_weigh_weight_box_size = wx.StaticBoxSizer(self.get_weigh_weight_box, wx.VERTICAL)
        self.get_weigh_weight_box_title_h.Add(self.devide_type, 1, wx.ALL | wx.EXPAND, 2)
        self.get_weigh_weight_box_title_h.Add(self.weigh_weight_button, 1, wx.ALL | wx.EXPAND, 2)
        self.get_weigh_weight_box_size.Add(self.get_weigh_weight_box_title_h, 1, wx.ALL | wx.EXPAND, 2)
        self.get_weigh_weight_box_size.Add(self.get_weigh_weight_box_actural_h_1, 1, wx.ALL | wx.EXPAND, 2)
        self.get_weigh_weight_box_size.Add(self.get_weigh_weight_box_actural_h_2, 1, wx.ALL | wx.EXPAND, 2)
        self.get_weigh_weight_box_size.Add(self.get_weigh_weight_box_actural_h_3, 1, wx.ALL | wx.EXPAND, 2)
        self.get_weigh_weight_box_size.Add(self.get_weigh_weight_box_actural_h_4, 1, wx.ALL | wx.EXPAND, 2)
        self.get_weigh_weight_box_size.Add(self.get_weigh_weight_box_actural_h_5, 1, wx.ALL | wx.EXPAND, 2)
        self.weigh_back = wx.Button(self.weigh_panel, -1, "返回主菜单")
        self.Bind(wx.EVT_BUTTON, self.weigh_back_int, self.weigh_back)
        self.weigh_back_box = wx.StaticBox(self.weigh_panel, -1, "")
        self.weigh_back_box_size = wx.StaticBoxSizer(self.weigh_back_box, wx.VERTICAL)
        self.weigh_back_box_size.Add(self.weigh_back, 1, wx.ALL | wx.EXPAND, 2)
        self.weigh_box_v.Add(self.system_message, 0, wx.ALL | wx.EXPAND, 2)
        self.weigh_box_v.Add(self.weigh_stability_box_size, 0, wx.ALL | wx.EXPAND, 2)
        self.weigh_box_v.Add(self.goods_weight_box_size, 0, wx.ALL | wx.EXPAND, 2)
        self.weigh_box_v.Add(self.weight_attr_static_box_sizer, 0, wx.ALL | wx.EXPAND, 2)
        self.weigh_box_v.Add(self.get_weigh_weight_box_size, 0, wx.ALL | wx.EXPAND, 2)
        self.weigh_box_v.Add(self.weigh_back_box_size, 0, wx.ALL | wx.EXPAND, 2)
        self.weigh_panel.SetSizer(self.weigh_box_v)
        self.weigh_panel.Layout()
        self.weigh_panel.Fit()
        # self.system_message.SetForegroundColour("Red")
        # self.weigh_operator_tip_panel.Layout()
        pub.subscribe(self.system_operator_tip, "update")
    #weigh属性查询
    def query_attr_weight(self,evt):
        self.count_time = 0
        self.count_time_alive = True
        self.weigh_stability_button.Disable()
        self.goods_weight_button.Disable()
        self.weigh_back.Disable()
        self.weigh_weight_button.Disable()
        self.weight_attr_set_button.Disable()
        self.weight_attr_auery_button.Disable()
        self.query_attr_weight_process_t = threading.Thread(target=self.query_attr_weight_process)
        self.query_attr_weight_process_t.start()
        self.operator_impact_t = threading.Thread(target=self.operator_impact)
        self.operator_impact_t.start()
    def query_attr_weight_process(self):
        try:
            payload = "{\"devname\": \"" + self.get_union_id + "\",\"req\": {\"A\": 119}}"
            headers = {'Content-Type': "application/json", 'cache-control': "no-cache",
                       'Postman-Token': "1f4c5013-b7de-4404-ad2e-74cfb28aacc7"}
            response = requests.request("POST", self.url, data=payload, headers=headers)
            query_weigh_algorithmattr_org = json.loads(response.text)
            if query_weigh_algorithmattr_org["msg"].lower() == "success":
                wx.CallAfter(pub.sendMessage, "update", msg="weigh_weight_stop")
                self.system_dlg.SetMessage("查询成功!!!")
                self.system_dlg.ShowModal()
                self.weight_attr_query_value.SetLabel(str(query_weigh_algorithmattr_org["output"]["attr"]))
            else:
                self.system_dlg.SetMessage(response.text)
                self.system_dlg.ShowModal()
        except:
            self.system_dlg.SetMessage(response.text)
            self.system_dlg.ShowModal()
    #设置weigh属性
    def set_attr_weight(self,evt):
        self.count_time = 0
        self.count_time_alive = True
        self.weigh_stability_button.Disable()
        self.goods_weight_button.Disable()
        self.weigh_back.Disable()
        self.weigh_weight_button.Disable()
        self.weight_attr_set_button.Disable()
        self.weight_attr_auery_button.Disable()
        self.set_attr_weight_process_t = threading.Thread(target=self.set_attr_weight_process)
        self.set_attr_weight_process_t.start()
        self.operator_impact_t = threading.Thread(target=self.operator_impact)
        self.operator_impact_t.start()
    def set_attr_weight_process(self):
        try:
            attr_value=int(self.weight_attr_set_value.GetValue())
            print (attr_value)
            if not str(attr_value).isdigit():
                self.system_dlg.SetMessage("请输入正确的值")
                self.system_dlg.ShowModal()
                wx.CallAfter(pub.sendMessage, "update", msg="weigh_weight_stop")
            payload = "{\"devname\": \"" + self.get_union_id + "\",\"req\": {\"A\": 118,\"P\":{\"algorithmattr\":{ \"attr\":" + str(attr_value) + "}}}}"
            headers = {'Content-Type': "application/json", 'cache-control': "no-cache",'Postman-Token': "1f4c5013-b7de-4404-ad2e-74cfb28aacc7"}
            response = requests.request("POST", self.url, data=payload, headers=headers)
            set_weigh_algorithmattr_org = json.loads(response.text)
            if set_weigh_algorithmattr_org["msg"].lower() == "success":
                wx.CallAfter(pub.sendMessage, "update", msg="weigh_weight_stop")
                self.system_dlg.SetMessage("设置成功")
                self.system_dlg.ShowModal()
            else:
                wx.CallAfter(pub.sendMessage, "update", msg="weigh_weight_stop")
                self.system_dlg.SetMessage(response.text)
                self.system_dlg.ShowModal()
        except:
            wx.CallAfter(pub.sendMessage, "update", msg="weigh_weight_stop")
            self.system_dlg.SetMessage("设置失败！！！")
            self.system_dlg.ShowModal()

    # 秤盘稳定性查询
    def weigh_stability(self, evt):
        self.user_name_dlg.ShowModal()
        if self.user_name_dlg.ShowModal() == wx.ID_OK:
            self.user_name_ssh = self.user_name_dlg.GetValue()
        else:
            return
        self.pw_dlg.ShowModal()
        if self.pw_dlg.ShowModal() == wx.ID_OK:
            self.pw_ssh = self.pw_dlg.GetValue()

        else:
            return
        self.count_time = 0
        self.count_time_alive = True
        select_floor = False
        for i in range(len(self.weigh_floor)):
            if self.weigh_stability_index.GetValue() == self.weigh_floor[i]:
                select_floor = True
        if not select_floor:
            self.system_dlg.SetMessage("请选择设备类型!!!")
            self.system_dlg.ShowModal()

            return
        self.weigh_stability_button.Disable()
        self.goods_weight_button.Disable()
        self.weigh_back.Disable()
        self.weigh_weight_button.Disable()
        self.weight_attr_set_button.Disable()
        self.weight_attr_auery_button.Disable()
        self.weigh_stability_process_t = threading.Thread(target=self.weigh_stability_process)
        self.weigh_stability_process_t.start()
        self.operator_impact_t = threading.Thread(target=self.operator_impact)
        self.operator_impact_t.start()

    # 秤盘稳定性查询发送
    def weigh_stability_process(self):
        try:
            weight_floor = self.weigh_floor_com[self.weigh_stability_index.GetValue()]
            hostid = "m.vegcloud.tech"
            if len(self.dev_id.GetValue())==5:
                portid=self.dev_id.GetValue()
            else:
                portid = "2" + self.dev_id.GetValue()

            sshid = int(portid)
            name = self.user_name_ssh
            pwd = self.pw_ssh
            myclient = paramiko.SSHClient()
            myclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            myclient.connect(hostid, port=sshid, username=name, password=pwd, allow_agent=False, look_for_keys=False)
            stdin, stdout, stderr = myclient.exec_command('sudo cat /dev/ttycom1 > weight1')
            myclient.close()
            init_time = int(math.floor(time.time()))
            weight_floor_value_list = []
            diff_value_list = []
            min_value = 0
            max_value = 0
            time.sleep(30)
            myclient.connect(hostid, port=sshid, username=name, password=pwd, allow_agent=False, look_for_keys=False)
            stdin, stdout, stderr = myclient.exec_command(r'sudo kill -9 $(pidof cat)')
            time.sleep(1)
            stdin, stdout, stderr = myclient.exec_command('sudo cat weight1')
            weight_org = stdout.read().decode()
            weight_floor_value = re.findall(r'CH' + str(weight_floor) + r'([-+])\s+(\d+)', weight_org, re.M)
            for i in range(len(weight_floor_value)):
                weight_floor_value_unit = weight_floor_value[i][1]
                weight_floor_symbol_unit = weight_floor_value[i][0]
                weight_floor_symbol_value_unit = weight_floor_symbol_unit + weight_floor_value_unit
                weight_floor_value_list.append(weight_floor_symbol_value_unit)
            for j in range(len(weight_floor_value_list) - 1):
                diff_value = abs(int(weight_floor_value_list[j + 1]) - int(weight_floor_value_list[j]))
                diff_value_list.append(diff_value)
            for n in range(len(diff_value_list)):
                if min_value > diff_value_list[n]:
                    min_value = diff_value_list[n]
                elif max_value < diff_value_list[n]:
                    max_value = diff_value_list[n]
            max_diff_value = int(max_value) - int(min_value)
            if max_diff_value >= 8:
                wx.CallAfter(pub.sendMessage, "update", msg="weigh_stability")
                self.system_dlg.SetMessage("检测完成!!!")
                self.system_dlg.ShowModal()

                self.weigh_stability_status_value.SetBackgroundColour("Rad")
                self.weigh_stability_status_value.SetLabel("不稳定")
                self.weigh_stability_float_value.SetBackgroundColour("Rad")
                self.weigh_stability_float_value.SetLabel(str(max_diff_value))
            else:
                wx.CallAfter(pub.sendMessage, "update", msg="weigh_stability")
                self.system_dlg.SetMessage("检测完成!!!")
                self.system_dlg.ShowModal()

                self.weigh_stability_status_value.SetBackgroundColour("Green")
                self.weigh_stability_status_value.SetLabel("稳定")
                self.weigh_stability_float_value.SetBackgroundColour("Green")
                self.weigh_stability_float_value.SetLabel(str(max_diff_value))

        except:
            wx.CallAfter(pub.sendMessage, "update", msg="weigh_stability")
            self.system_dlg.SetMessage("SSH 登入失败!!!")
            self.system_dlg.ShowModal()

    # 查询秤盘当前重量
    def get_weigh_weight_send(self, evt):
        select_type = False
        for i in range(len(self.devid_type_list)):
            if self.devide_type.GetValue() == self.devid_type_list[i]:
                select_type = True
        if not select_type:
            self.system_dlg.SetMessage("请选择设备类型!!!")
            self.system_dlg.ShowModal()

            return
        self.count_time = 0
        self.count_time_alive = True
        self.weigh_stability_button.Disable()
        self.goods_weight_button.Disable()
        self.weigh_back.Disable()
        self.weigh_weight_button.Disable()
        self.weight_attr_set_button.Disable()
        self.weight_attr_auery_button.Disable()
        self.get_weigh_weight_process_t = threading.Thread(target=self.get_weigh_weight_process)
        self.get_weigh_weight_process_t.start()
        self.operator_impact_t = threading.Thread(target=self.operator_impact)
        self.operator_impact_t.start()

    # 查询秤盘当前重量下发
    def get_weigh_weight_process(self):
        try:
            payload_weight = "{\r\n    \"devname\": \"" + self.get_union_id + "\",\r\n    \"req\": {\r\n        \"A\": 107,\r\n        \"P\":{\r\n        }\r\n    }\r\n}"
            headers_weight = {
                'Content-Type': "application/json",
                'Authorization': "Basic YWRtaW46Y2poeXkzMDA=",
                'cache-control': "no-cache",
                'Postman-Token': "81061e78-1abe-47f8-beed-c845639289db"
            }
            response_weight = requests.request("POST", self.url, data=payload_weight, headers=headers_weight)
            get_floor_weight_org = json.loads(response_weight.text)
            payload_online = "{\"req\":{\"A\":112},\"devname\": \"" + self.get_union_id + "\"}"
            headers_online = {
                'Content-Type': "application/json",
                'Authorization': "Basic YWRtaW46Y2poeXkzMDA=",
                'cache-control': "no-cache",
                'Postman-Token': "81061e78-1abe-47f8-beed-c845639289db"
            }
            response_online = requests.request("POST", self.url, data=payload_online, headers=headers_online)
            online_status_org = json.loads(response_online.text)
            self.weigh_weight_dict = {}
            self.weigh_weight_online={}
            if get_floor_weight_org["msg"].lower() == "success":
                get_floor_weight_value = get_floor_weight_org["output"]
                for i in range(0, len(get_floor_weight_value)):
                    weight_key = get_floor_weight_value[i]["weighid"]
                    weight_value = get_floor_weight_value[i]["weight"]
                    self.weigh_weight_dict[weight_key] = weight_value
            elif get_floor_weight_org["msg"] == "DEVICE_NAME_NOT_EXIST":
                wx.CallAfter(pub.sendMessage, "update", msg="weigh_weight_stop")
                self.system_dlg.SetMessage("请输入正确的Union ID!!!")
                self.system_dlg.ShowModal()

            elif get_floor_weight_org["msg"] == "RRPC_TIMEOUT":
                wx.CallAfter(pub.sendMessage, "update", msg="weigh_weight_stop")
                self.system_dlg.SetMessage("超时，请重新查询!!!")
                self.system_dlg.ShowModal()

            elif get_floor_weight_org["msg"] == "DEVICE_OFFLINE":
                wx.CallAfter(pub.sendMessage, "update", msg="weigh_weight_stop")
                self.system_dlg.SetMessage("设备离线!请检查设备!!!")
                self.system_dlg.ShowModal()

            else:
                wx.CallAfter(pub.sendMessage, "update", msg="weigh_weight_stop")
                self.system_dlg.SetMessage(get_floor_weight_org["msg"])
                self.system_dlg.ShowModal()
            if online_status_org["msg"].lower() == "success":
                weight_online_status=online_status_org["output"]
                for i in range(len(weight_online_status)):
                    weight_id=weight_online_status[i]["weighid"]
                    weight_status=weight_online_status[i]["online"]
                    self.weigh_weight_online[weight_id]=weight_status
                wx.CallAfter(pub.sendMessage, "update", msg="weigh_weight_stop")
                self.system_dlg.SetMessage("查询成功!!!")
                self.system_dlg.ShowModal()
            elif online_status_org["msg"] == "DEVICE_NAME_NOT_EXIST":
                wx.CallAfter(pub.sendMessage, "update", msg="weigh_weight_stop")
                self.system_dlg.SetMessage("请输入正确的Union ID!!!")
                self.system_dlg.ShowModal()

            elif online_status_org["msg"] == "RRPC_TIMEOUT":
                wx.CallAfter(pub.sendMessage, "update", msg="weigh_weight_stop")
                self.system_dlg.SetMessage("超时，请重新查询!!!")
                self.system_dlg.ShowModal()

            elif online_status_org["msg"] == "DEVICE_OFFLINE":
                wx.CallAfter(pub.sendMessage, "update", msg="weigh_weight_stop")
                self.system_dlg.SetMessage("设备离线!请检查设备!!!")
                self.system_dlg.ShowModal()

            else:
                wx.CallAfter(pub.sendMessage, "update", msg="weigh_weight_stop")
                self.system_dlg.SetMessage(online_status_org["msg"])
                self.system_dlg.ShowModal()

        except:
            wx.CallAfter(pub.sendMessage, "update", msg="weigh_weight_stop")
            self.system_dlg.SetMessage(response_weight.text)
            self.system_dlg.ShowModal()

    # 商品称重
    def calc_goods_weight(self, evt):
        self.count_time = 0
        self.count_time_alive = True
        self.weigh_stability_button.Disable()
        self.goods_weight_button.Disable()
        self.weigh_back.Disable()
        self.weigh_weight_button.Disable()
        self.weight_attr_set_button.Disable()
        self.weight_attr_auery_button.Disable()
        self.user_name_dlg.ShowModal()
        if self.user_name_dlg.ShowModal() == wx.ID_OK:
            self.user_name_ssh = self.user_name_dlg.GetValue()
            self.user_name_dlg.Close()
        else:
            return
        self.pw_dlg.ShowModal()
        if self.pw_dlg.ShowModal() == wx.ID_OK:
            self.pw_ssh = self.pw_dlg.GetValue()
            self.pw_dlg.Close()
        else:
            return
        self.calc_goods_weight_process_t = threading.Thread(target=self.calc_goods_weight_process)
        self.calc_goods_weight_process_t.start()
        #self.operator_impact_t = threading.Thread(target=self.operator_impact)
        #self.operator_impact_t.start()

    def calc_goods_weight_process(self):
        try:

            if len(self.dev_id.GetValue()) == 5:
                port_id = self.dev_id.GetValue()
            else:
                port_id = "2" + self.dev_id.GetValue()
            sshid = int(port_id)
            select_ch=self.weigh_floor_com[self.goods_weight_index.GetValue()]
            payload_frp = "{\"devname\": \"" + self.get_union_id + "\", \"req\": { \"A\": 152,\"P\": { \"appname\": \"frp-client-ssh\", \"action\": 4,\"port\":\"" + str(self.dev_id.GetValue()) + "\" }}}"
            headers_frp = {
                'Content-Type': "application/json",
                'cache-control': "no-cache",
                'Postman-Token': "0b5b07b3-c756-4359-88b9-da388c58324d"
            }
            response_frp_open = requests.request("POST", self.url, data=payload_frp, headers=headers_frp)
            frp_status = json.loads(response_frp_open.text)
            if frp_status["msg"].lower() == "success":
                pid = frp_status["output"]["pid"]
                for i in range(30):
                    try:
                        payload_pid = "{\n    \"devname\": \"" + self.get_union_id + "\",\n    \"req\": {\n        \"A\": 153,\n        \"P\": {\n          \"pid\":\"" + pid + "\"\n        }\n    }\n}\n"
                        headers_pid = {
                            'Content-Type': "application/json",
                            'cache-control': "no-cache",
                            'Postman-Token': "20e0e8d2-28c2-4f7b-be6b-89b6b2451d60"
                        }
                        response_pid = requests.request("POST", self.url, data=payload_pid, headers=headers_pid)
                        pid_status = json.loads(response_pid.text)
                        if pid_status["msg"].lower() == "success":
                            if pid_status["output"]["state"] == "completed":
                                break
                        else:
                            wx.CallAfter(pub.sendMessage, "update", msg="stop")
                            self.lock_dlg.SetMessage(pid_status["msg"])
                            self.lock_dlg.ShowModal()
                            break
                    except:
                        wx.CallAfter(pub.sendMessage, "update", msg="stop")
                        self.system_dlg.SetMessage("查询PID失败!!!")
                        self.system_dlg.ShowModal()
                        break
                        # Mymsg = wx.MessageBox("查询PID失败!!!", "Message box", style=wx.OK | wx.CANCEL)
                    time.sleep(1)
            else:
                wx.CallAfter(pub.sendMessage, "update", msg="calc_weight_stop")
                self.system_dlg.SetMessage(frp_status["msg"])
                self.system_dlg.ShowModal()
                return
        except:
            wx.CallAfter(pub.sendMessage, "update", msg="calc_weight_stop")
            self.system_dlg.SetMessage(response_frp_open.text)
            self.system_dlg.ShowModal()
            return
        try:
            self.system_message.SetLabel("初始化中。。。。")
            hostid = "m.vegcloud.tech"
            name = self.user_name_ssh
            pwd = self.pw_ssh
            myclient = paramiko.SSHClient()
            myclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            myclient.connect(hostid, port=sshid, username=name, password=pwd, allow_agent=False, look_for_keys=False)
            time.sleep(5)
            cmd = 'sudo cat /dev/ttycom1 |grep CH' + str(select_ch)
            stdin, stdout, stderr = myclient.exec_command(cmd,timeout=120)
            time.sleep(2)
            weight_org = stdout.readline()
            self.weight_base=0
            self.control_cal_weight=True
            change_tip_count=0
            while True:
                if weight_org:
                    actual_weight_org=re.findall("CH\d[-+]\s+(\d+)",weight_org)
                    if actual_weight_org:
                        self.actual_weight=actual_weight_org[0]
                        self.current_weight=int(self.actual_weight)-self.weight_base
                        wx.CallAfter(pub.sendMessage,"update", msg="current_weight_update")
                        if not change_tip_count>0:
                            self.system_message.SetLabel("读取秤盘数据成功")
                if not self.control_cal_weight:
                    stdin, stdout1, stderr = myclient.exec_command(r'sudo kill -9 $(pidof cat)')
                    time.sleep(2)
                    myclient.close()
                    wx.CallAfter(pub.sendMessage, "update", msg="calc_weight_stop")
                    break
                time.sleep(0.2)
                change_tip_count +=1
        except:
            wx.CallAfter(pub.sendMessage, "update", msg="weigh_weight_stop")
            self.system_dlg.SetMessage("SSH 登入失败!!!")
            self.system_dlg.ShowModal()
    def clear_process(self,evt):
        self.weight_base=int(self.actual_weight)
        self.system_message.SetLabel("清零成功")
        self.actual_goods_weight_index.SetLabel("商品重量")
    def stop_cal_weight_process(self,evt):
        self.control_cal_weight=False


    def weigh_back_int(self, evt):
        self.weigh_panel.Destroy()
        self.init_panel.Show()
        #self.weigh_operator_tip_panel.Destroy()
        self.operator_muen_panel.Show()

    # 信号操作
    def cellular_operator(self, evt):
        self.operator_muen_panel.Hide()
        self.init_panel.Hide()
        self.cellular_panel = wx.ScrolledWindow(self, -1, pos=(0, 0), size=(960, 500))
        self.cellular_panel.SetBackgroundColour("#D8BFD8")
        self.system_message = wx.StaticText(self.cellular_panel, -1, "", style=wx.ALIGN_CENTER_HORIZONTAL|wx.ST_NO_AUTORESIZE)
        self.font_cellular_operator_tip = wx.Font(20, wx.DECORATIVE, wx.NORMAL, wx.LIGHT)
        self.system_message.SetFont(self.font_cellular_operator_tip)
        self.system_message.SetForegroundColour("Red")
        self.system_message.SetBackgroundColour("Black")
        self.font_cellular = wx.Font(13, wx.DECORATIVE, wx.NORMAL, wx.LIGHT)
        self.cellular_csq_box_h = wx.BoxSizer(wx.HORIZONTAL)
        self.cellular_ccid_box_h = wx.BoxSizer(wx.HORIZONTAL)
        self.cellular_box_v = wx.BoxSizer(wx.VERTICAL)
        self.system_message_box=wx.BoxSizer(wx.HORIZONTAL)
        self.system_message_box.Add(self.system_message,1,wx.ALL|wx.EXPAND,2)
        self.cellular_panel.SetScrollbar(1,1,1000,2000)
        self.cellular_panel.SetScrollRate(10,10)
        self.query_cellular_csq = wx.StaticText(self.cellular_panel, -1, "当前信号强度")
        self.query_cellular_csq.SetFont(self.font_cellular)
        self.query_cellular_csq.SetForegroundColour("Blue")
        self.actual_cellular_csq = wx.StaticText(self.cellular_panel, -1, "")
        self.actual_cellular_csq.SetFont(self.font_cellular)
        self.actual_cellular_csq.SetForegroundColour("Blue")
        self.query_button_scq = wx.Button(self.cellular_panel, -1, "查询")
        self.query_button_scq.SetFont(self.font_cellular)
        self.query_button_scq.SetForegroundColour("Blue")
        self.Bind(wx.EVT_BUTTON, self.query_cellular_csq_send, self.query_button_scq)
        self.query_cellular_csq_box = wx.StaticBox(self.cellular_panel, -1, "查询信号强度")
        self.query_cellular_csq_box_size = wx.StaticBoxSizer(self.query_cellular_csq_box, wx.VERTICAL)
        self.cellular_csq_box_h.Add(self.query_cellular_csq, 1, wx.ALL | wx.EXPAND, 2)
        self.cellular_csq_box_h.Add(self.actual_cellular_csq, 1, wx.ALL | wx.EXPAND, 2)
        self.cellular_csq_box_h.Add(self.query_button_scq, 1, wx.ALL | wx.EXPAND, 2)
        self.query_cellular_csq_box_size.Add(self.cellular_csq_box_h, 1, wx.ALL | wx.EXPAND, 2)
        self.query_cellular_ccid = wx.StaticText(self.cellular_panel, -1, "CCID号码")
        self.query_cellular_ccid.SetFont(self.font_cellular)
        self.query_cellular_ccid.SetForegroundColour("Blue")
        self.actual_cellular_ccid = wx.StaticText(self.cellular_panel, -1, "")
        self.actual_cellular_ccid.SetFont(self.font_cellular)
        self.actual_cellular_ccid.SetForegroundColour("Blue")
        self.query_button_ccid = wx.Button(self.cellular_panel, -1, "查询")
        self.Bind(wx.EVT_BUTTON, self.query_cellular_ccid_send, self.query_button_ccid)
        self.query_button_ccid.SetFont(self.font_cellular)
        self.query_button_ccid.SetForegroundColour("Blue")
        self.query_cellular_ccid_box = wx.StaticBox(self.cellular_panel, -1, "查询CCID")
        self.query_cellular_ccid_box_size = wx.StaticBoxSizer(self.query_cellular_ccid_box, wx.VERTICAL)
        self.cellular_ccid_box_h.Add(self.query_cellular_ccid, 1, wx.ALL | wx.EXPAND, 2)
        self.cellular_ccid_box_h.Add(self.actual_cellular_ccid, 1, wx.ALL | wx.EXPAND, 2)
        self.cellular_ccid_box_h.Add(self.query_button_ccid, 1, wx.ALL | wx.EXPAND, 2)
        self.query_cellular_ccid_box_size.Add(self.cellular_ccid_box_h, 1, wx.ALL | wx.EXPAND, 2)
        self.cellular_back = wx.Button(self.cellular_panel, -1, "返回主菜单")
        self.cellular_back.SetFont(self.font_cellular)
        self.cellular_back.SetForegroundColour("Blue")
        self.Bind(wx.EVT_BUTTON, self.cellular_back_init, self.cellular_back)
        self.cellular_back_box = wx.StaticBox(self.cellular_panel, -1)
        self.cellular_back_box_size = wx.StaticBoxSizer(self.cellular_back_box, wx.VERTICAL)
        self.cellular_back_box_size.Add(self.cellular_back, 1, wx.ALL | wx.EXPAND, 2)
        self.cellular_box_v.Add(self.system_message_box, 0, wx.ALL | wx.EXPAND, 2)
        self.cellular_box_v.Add(self.query_cellular_csq_box_size, 0, wx.ALL | wx.EXPAND, 2)
        self.cellular_box_v.Add(self.query_cellular_ccid_box_size, 0, wx.ALL | wx.EXPAND, 2)
        self.cellular_box_v.Add(self.cellular_back_box_size, 0, wx.ALL | wx.EXPAND, 2)
        self.cellular_panel.SetSizer(self.cellular_box_v)
        self.cellular_panel.Layout()
        self.cellular_panel.Fit()
        pub.subscribe(self.system_operator_tip, "update")

    # 查询CCID
    def query_cellular_ccid_send(self, evt):
        self.count_time = 0
        self.count_time_alive = True
        self.query_button_scq.Disable()
        self.query_button_ccid.Disable()
        self.cellular_back.Disable()
        self.query_cellular_ccid_process_t = threading.Thread(target=self.query_cellular_ccid_process)
        self.query_cellular_ccid_process_t.start()
        self.operator_impact_t = threading.Thread(target=self.operator_impact)
        self.operator_impact_t.start()

    # 查询CCID下发
    def query_cellular_ccid_process(self):
        try:
            payload_ccid = "{\n    \"devname\": \"" + self.get_union_id + "\",\n    \"req\": {\n        \"A\": 353\n    }\n}"
            headers_ccid = {
                'Content-Type': "application/json",
                'cache-control': "no-cache",
                'Postman-Token': "b0431a14-ddb7-4974-8667-6ae53e96085f"
            }

            response_ccid = requests.request("POST", self.url, data=payload_ccid, headers=headers_ccid)
            cellular_ccid_org = json.loads(response_ccid.text)
            if cellular_ccid_org["msg"].lower() == "success":
                cellular_ccid_value_org = cellular_ccid_org["output"]["outputret"]
                cellular_ccid_value = re.findall(r'\+QCCID:\s+(\d+\S+)', cellular_ccid_value_org)
                self.actual_cellular_ccid.SetLabel(cellular_ccid_value[0])
                wx.CallAfter(pub.sendMessage, "update", msg="query_ccid_stop")
                self.system_dlg.SetMessage("查询成功!!!")
                self.system_dlg.ShowModal()

            elif cellular_ccid_org["msg"] == "DEVICE_NAME_NOT_EXIST":
                wx.CallAfter(pub.sendMessage, "update", msg="query_csq_stop")
                self.system_dlg.SetMessage("请输入正确的Union ID!!!")
                self.system_dlg.ShowModal()

            elif cellular_ccid_org["msg"] == "RRPC_TIMEOUT":
                wx.CallAfter(pub.sendMessage, "update", msg="query_csq_stop")
                self.system_dlg.SetMessage("超时，请重新查询!!!")
                self.system_dlg.ShowModal()

            elif cellular_ccid_org["msg"] == "DEVICE_OFFLINE":
                wx.CallAfter(pub.sendMessage, "update", msg="query_csq_stop")
                self.system_dlg.SetMessage("设备离线!请检查设备!!!")
                self.system_dlg.ShowModal()

            else:
                wx.CallAfter(pub.sendMessage, "update", msg="query_csq_stop")
                self.system_dlg.SetMessage(cellular_ccid_org["msg"])
                self.system_dlg.ShowModal()

        except:
            wx.CallAfter(pub.sendMessage, "update", msg="query_csq_stop")
            self.system_dlg.SetMessage(response_ccid.text)
            self.system_dlg.ShowModal()

    # 查询信号强度
    def query_cellular_csq_send(self, evt):
        self.count_time = 0
        self.count_time_alive = True
        self.query_button_scq.Disable()
        self.query_button_ccid.Disable()
        self.cellular_back.Disable()
        self.query_cellular_csq_process_t = threading.Thread(target=self.query_cellular_csq_process)
        self.query_cellular_csq_process_t.start()
        self.operator_impact_t = threading.Thread(target=self.operator_impact)
        self.operator_impact_t.start()

    # 查询信号强度下发
    def query_cellular_csq_process(self):
        try:
            payload_csq = "{\n    \"devname\": \"" + self.get_union_id + "\",\n    \"req\": {\n        \"A\": 351\n    }\n}\n"
            headers_csq = {
                'Content-Type': "application/json",
                'cache-control': "no-cache",
                'Postman-Token': "2e4eee13-0b59-48fa-b6c1-190a56d57463"
            }

            response_csq = requests.request("POST", self.url, data=payload_csq, headers=headers_csq)
            cellular_csq_org = json.loads(response_csq.text)
            if cellular_csq_org["msg"].lower() == "success":
                cellular_csq_value_org = cellular_csq_org["output"]["outputret"]
                cellular_csq_value = re.findall(r"\d+", cellular_csq_value_org)
                self.actual_cellular_csq.SetLabel(cellular_csq_value[0])
                wx.CallAfter(pub.sendMessage, "update", msg="query_csq_stop")
                self.system_dlg.SetMessage("查询成功!!!")
                self.system_dlg.ShowModal()

            elif cellular_csq_org["msg"] == "DEVICE_NAME_NOT_EXIST":
                wx.CallAfter(pub.sendMessage, "update", msg="query_csq_stop")
                self.system_dlg.SetMessage("请输入正确的Union ID!!!")
                self.system_dlg.ShowModal()

            elif cellular_csq_org["msg"] == "RRPC_TIMEOUT":
                wx.CallAfter(pub.sendMessage, "update", msg="query_csq_stop")
                self.system_dlg.SetMessage("超时，请重新查询!!!")
                self.system_dlg.ShowModal()

            elif cellular_csq_org["msg"] == "DEVICE_OFFLINE":
                wx.CallAfter(pub.sendMessage, "update", msg="query_csq_stop")
                self.system_dlg.SetMessage("设备离线!请检查设备!!!")
                self.system_dlg.ShowModal()

            else:
                wx.CallAfter(pub.sendMessage, "update", msg="query_csq_stop")
                self.system_dlg.SetMessage(cellular_csq_org["msg"])
                self.system_dlg.ShowModal()

        except:
            wx.CallAfter(pub.sendMessage, "update", msg="query_csq_stop")
            self.system_dlg.SetMessage(response_csq.text)
            self.system_dlg.ShowModal()

    # 信号强度返回主菜单
    def cellular_back_init(self, evt):
        self.cellular_panel.Destroy()
        self.init_panel.Show()
        #self.cellular_operator_tip_panel.Destroy()
        self.operator_muen_panel.Show()

    # 语音操作
    def vioce_operator(self, evt):
        self.operator_muen_panel.Hide()
        self.init_panel.Hide()
        self.vioce_panel = wx.ScrolledWindow(self, -1, pos=(0, 0), size=(960, 500))
        self.vioce_panel.SetBackgroundColour("#D8BFD8")
        self.system_message = wx.StaticText(self.vioce_panel, -1, "", style=wx.ALIGN_CENTER_HORIZONTAL|wx.ST_NO_AUTORESIZE)
        self.font_vioce_operator_tip = wx.Font(20, wx.DECORATIVE, wx.NORMAL, wx.LIGHT)
        self.system_message.SetFont(self.font_vioce_operator_tip)
        self.system_message.SetForegroundColour("Red")
        self.system_message.SetBackgroundColour("Black")
        self.font_vicoe = wx.Font(13, wx.DECORATIVE, wx.NORMAL, wx.LIGHT)
        self.vioce_query_box_H = wx.BoxSizer(wx.HORIZONTAL)
        self.vioce_set_box_H = wx.BoxSizer(wx.HORIZONTAL)
        self.vioce_back_box_H = wx.BoxSizer(wx.HORIZONTAL)
        self.vioce_box_V = wx.BoxSizer(wx.VERTICAL)
        self.system_message_box=wx.BoxSizer(wx.HORIZONTAL)
        self.system_message_box.Add(self.system_message,1,wx.ALL|wx.EXPAND,2)
        self.vioce_panel.SetScrollbar(1,1,1000,2000)
        self.vioce_panel.SetScrollRate(10,10)
        self.vioce_actual_index = wx.StaticText(self.vioce_panel, -1, "当前音量")
        self.vioce_actual_index.SetFont(self.font_vicoe)
        self.vioce_actual_index.SetForegroundColour("Blue")
        self.vioce_actual_value = wx.Slider(self.vioce_panel, -1, minValue=0, maxValue=100,
                                            style=wx.SL_HORIZONTAL | wx.SL_LABELS)
        self.vioce_actual_value.SetFont(self.font_vicoe)
        self.vioce_actual_value.SetForegroundColour("Blue")
        self.vioce_query_send = wx.Button(self.vioce_panel, -1, "查询")
        self.vioce_query_send.SetFont(self.font_vicoe)
        self.vioce_query_send.SetForegroundColour("Blue")
        self.Bind(wx.EVT_BUTTON, self.get_acutal_vioce, self.vioce_query_send)
        self.vioce_query_box = wx.StaticBox(self.vioce_panel, -1, "")
        self.vioce_query_box_size = wx.StaticBoxSizer(self.vioce_query_box, wx.VERTICAL)
        self.vioce_query_box_H.Add(self.vioce_actual_index, 1, wx.ALL | wx.EXPAND, 2)
        self.vioce_query_box_H.Add(self.vioce_actual_value, 1, wx.ALL | wx.EXPAND, 2)
        self.vioce_query_box_H.Add(self.vioce_query_send, 1, wx.ALL | wx.EXPAND, 2)
        self.vioce_query_box_size.Add(self.vioce_query_box_H, 1, wx.ALL | wx.EXPAND, 2)
        self.vioce_set_index = wx.StaticText(self.vioce_panel, -1, "设置音量")
        self.vioce_set_index.SetFont(self.font_vicoe)
        self.vioce_set_index.SetForegroundColour("Blue")
        self.vioce_set_value = wx.Slider(self.vioce_panel, -1, minValue=0, maxValue=100,
                                         style=wx.SL_HORIZONTAL | wx.SL_LABELS)
        self.vioce_set_value.SetFont(self.font_vicoe)
        self.vioce_set_value.SetForegroundColour("Blue")
        self.vioce_set_send = wx.Button(self.vioce_panel, -1, "设置")
        self.vioce_set_send.SetFont(self.font_vicoe)
        self.vioce_set_send.SetForegroundColour("Blue")
        self.Bind(wx.EVT_BUTTON, self.vioce_set, self.vioce_set_send)
        self.vioce_set_box = wx.StaticBox(self.vioce_panel, -1, "")
        self.vioce_set_box_size = wx.StaticBoxSizer(self.vioce_set_box, wx.VERTICAL)
        self.vioce_set_box_H.Add(self.vioce_set_index, 1, wx.ALL | wx.EXPAND, 2)
        self.vioce_set_box_H.Add(self.vioce_set_value, 1, wx.ALL | wx.EXPAND, 2)
        self.vioce_set_box_H.Add(self.vioce_set_send, 1, wx.ALL | wx.EXPAND, 2)
        self.vioce_set_box_size.Add(self.vioce_set_box_H, 1, wx.ALL | wx.EXPAND, 2)
        self.left_channel_button=wx.Button(self.vioce_panel,-1,"左声道")
        self.left_channel_button.SetFont(self.font_vicoe)
        self.left_channel_button.SetForegroundColour("Blue")
        self.Bind(wx.EVT_BUTTON,self.play_left_channel,self.left_channel_button)
        self.right_channel_button = wx.Button(self.vioce_panel, -1, "右声道")
        self.right_channel_button.SetFont(self.font_vicoe)
        self.right_channel_button.SetForegroundColour("Blue")
        self.Bind(wx.EVT_BUTTON, self.play_right_channel, self.right_channel_button)
        self.welcome_button = wx.Button(self.vioce_panel, -1, "开门提示")
        self.welcome_button.SetFont(self.font_vicoe)
        self.welcome_button.SetForegroundColour("Blue")
        self.Bind(wx.EVT_BUTTON, self.play_welcome, self.welcome_button)
        self.goodbye_button = wx.Button(self.vioce_panel, -1, "关门提示")
        self.goodbye_button.SetFont(self.font_vicoe)
        self.goodbye_button.SetForegroundColour("Blue")
        self.Bind(wx.EVT_BUTTON, self.play_goodbye, self.goodbye_button)
        self.vioce_test_box=wx.StaticBox(self.vioce_panel,-1,"喇叭检查")
        self.vioce_test_box_sizer=wx.StaticBoxSizer(self.vioce_test_box,wx.HORIZONTAL)
        self.vioce_test_box_sizer.Add(self.left_channel_button,1,wx.ALL|wx.EXPAND,2)
        self.vioce_test_box_sizer.Add(self.right_channel_button, 1, wx.ALL | wx.EXPAND, 2)
        self.vioce_test_box_sizer.Add(self.welcome_button, 1, wx.ALL | wx.EXPAND, 2)
        self.vioce_test_box_sizer.Add(self.goodbye_button, 1, wx.ALL | wx.EXPAND, 2)
        self.vioce_back = wx.Button(self.vioce_panel, -1, "返回主菜单")
        self.Bind(wx.EVT_BUTTON, self.vioce_back_init, self.vioce_back)
        self.vioce_back.SetFont(self.font_vicoe)
        self.vioce_back.SetForegroundColour("Blue")
        self.vioce_back_box = wx.StaticBox(self.vioce_panel, -1, "")
        self.vioce_back_box_size = wx.StaticBoxSizer(self.vioce_back_box, wx.VERTICAL)
        self.vioce_back_box_H.Add(self.vioce_back, 1, wx.ALL | wx.EXPAND, 2)
        self.vioce_back_box_size.Add(self.vioce_back_box_H, 1, wx.ALL | wx.EXPAND, 2)
        self.vioce_box_V.Add(self.system_message_box, 0, wx.ALL | wx.EXPAND, 2)
        self.vioce_box_V.Add(self.vioce_query_box_size, 0, wx.ALL | wx.EXPAND, 2)
        self.vioce_box_V.Add(self.vioce_set_box_size, 0, wx.ALL | wx.EXPAND, 2)
        self.vioce_box_V.Add(self.vioce_test_box_sizer, 0, wx.ALL | wx.EXPAND, 2)
        self.vioce_box_V.Add(self.vioce_back_box_size, 0, wx.ALL | wx.EXPAND, 2)
        self.vioce_panel.SetSizer(self.vioce_box_V)
        self.vioce_panel.Layout()
        self.vioce_panel.Fit()
        pub.subscribe(self.system_operator_tip, "update")

    # 返回主菜单
    def vioce_back_init(self, evt):
        self.vioce_panel.Destroy()
        self.init_panel.Show()
        #self.vioce_operator_tip_panel.Destroy()
        self.operator_muen_panel.Show()

    # 音量设置
    def vioce_set(self, evt):
        self.count_time = 0
        self.count_time_alive = True
        self.vioce_query_send.Disable()
        self.vioce_set_send.Disable()
        self.vioce_back.Disable()
        self.left_channel_button.Disable()
        self.right_channel_button.Disable()
        self.welcome_button.Disable()
        self.goodbye_button.Disable()
        self.vioce_set_process_t = threading.Thread(target=self.vioce_set_process)
        self.vioce_set_process_t.start()
        self.operator_impact_t = threading.Thread(target=self.operator_impact)
        self.operator_impact_t.start()

    def vioce_set_process(self):
        try:
            set_vioce_value = self.vioce_set_value.GetValue()
            payload_set_vioce = "{\r\n    \"devname\": \"" + self.get_union_id + "\",\r\n    \"req\": {\r\n        \"A\": 301,\r\n        \"P\":{\r\n         \"soundinfo\":{\r\n          \"volume\":\"" + str(
                set_vioce_value) + "\"\r\n          }\r\n         }\r\n    }\r\n}"
            headers = {
                'Content-Type': "application/json",
                'Authorization': "Basic YWRtaW46Y2poeXkzMDA=",
                'cache-control': "no-cache",
                'Postman-Token': "f9fa182f-691a-4254-93ad-a9bd31ee0b7e"
            }
            response_set = requests.request("POST", self.url, data=payload_set_vioce, headers=headers)
            vioce_set_status = json.loads(response_set.text)
            if vioce_set_status["msg"] == "DEVICE_NAME_NOT_EXIST":
                wx.CallAfter(pub.sendMessage, "update", msg="vioce_stop")
                self.system_dlg.SetMessage("请输入正确的Union ID !!!")
                self.system_dlg.ShowModal()

            elif vioce_set_status["msg"] == "RRPC_TIMEOUT":
                wx.CallAfter(pub.sendMessage, "update", msg="vioce_stop")
                self.system_dlg.SetMessage("超时，请重新查询 !!!")
                self.system_dlg.ShowModal()

            elif vioce_set_status["msg"] == "DEVICE_OFFLINE":
                wx.CallAfter(pub.sendMessage, "update", msg="vioce_stop")
                self.system_dlg.SetMessage("设备离线,请检查设备 !!!")
                self.system_dlg.ShowModal()

            elif vioce_set_status["msg"].lower() == "success":
                wx.CallAfter(pub.sendMessage, "update", msg="vioce_stop")
                self.system_dlg.SetMessage("设置成功 !!!")
                self.system_dlg.ShowModal()

            else:
                wx.CallAfter(pub.sendMessage, "update", msg="vioce_stop")
                self.system_dlg.SetMessage(vioce_set_status["msg"])
                self.system_dlg.ShowModal()

        except:
            wx.CallAfter(pub.sendMessage, "update", msg="vioce_stop")
            self.system_dlg.SetMessage(response_set.text)
            self.system_dlg.ShowModal()

    # 音量查询
    def get_acutal_vioce(self, evt):
        self.count_time = 0
        self.count_time_alive = True
        self.vioce_query_send.Disable()
        self.vioce_set_send.Disable()
        self.vioce_back.Disable()
        self.left_channel_button.Disable()
        self.right_channel_button.Disable()
        self.welcome_button.Disable()
        self.goodbye_button.Disable()
        self.get_actual_vioce_process_t = threading.Thread(target=self.get_actual_vioce_process)
        self.get_actual_vioce_process_t.start()
        self.operator_impact_t = threading.Thread(target=self.operator_impact)
        self.operator_impact_t.start()

    def get_actual_vioce_process(self):
        try:
            payload_actual_send = "{\n    \"devname\": \"" + self.get_union_id + "\",\n    \"req\": {\n        \"A\": 302\n    }\n}\n"
            headers = {
                'Content-Type': "application/json",
                'cache-control': "no-cache",
                'Postman-Token': "3d72c7e4-a9ea-448e-a572-b1be2f9ca931"
            }

            response = requests.request("POST", self.url, data=payload_actual_send, headers=headers)
            vicoe_actual_send_value = json.loads(response.text)
            if vicoe_actual_send_value["msg"] == "DEVICE_NAME_NOT_EXIST":
                wx.CallAfter(pub.sendMessage, "update", msg="vioce_stop")
                self.system_dlg.SetMessage("请输入正确的Union ID !!!")
                self.system_dlg.ShowModal()

            elif vicoe_actual_send_value["msg"] == "RRPC_TIMEOUT":
                wx.CallAfter(pub.sendMessage, "update", msg="vioce_stop")
                self.system_dlg.SetMessage("超时，请重新查询 !!!")
                self.system_dlg.ShowModal()

            elif vicoe_actual_send_value["msg"] == "DEVICE_OFFLINE":
                wx.CallAfter(pub.sendMessage, "update", msg="vioce_stop")
                self.system_dlg.SetMessage("设备离线,请检查设备 !!!")
                self.system_dlg.ShowModal()

            elif vicoe_actual_send_value["msg"].lower() == "success":
                wx.CallAfter(pub.sendMessage, "update", msg="vioce_stop")
                self.system_dlg.SetMessage("设置成功 !!!")
                self.system_dlg.ShowModal()

                actual_value = vicoe_actual_send_value["output"]["volume"]
                self.vioce_actual_value.SetValue(int(actual_value))

            else:
                wx.CallAfter(pub.sendMessage, "update", msg="vioce_stop")
                self.system_dlg.SetMessage(vicoe_actual_send_value["msg"])
                self.system_dlg.ShowModal()

        except:
            wx.CallAfter(pub.sendMessage, "update", msg="vioce_stop")
            self.system_dlg.SetMessage(response.text)
            self.system_dlg.ShowModal()
    #左声道
    def play_left_channel(self,evt):
        self.count_time = 0
        self.count_time_alive = True
        self.vioce_query_send.Disable()
        self.vioce_set_send.Disable()
        self.vioce_back.Disable()
        self.left_channel_button.Disable()
        self.right_channel_button.Disable()
        self.welcome_button.Disable()
        self.goodbye_button.Disable()
        self.play_left_channel_vioce_process_t = threading.Thread(target=self.play_left_channel_process)
        self.play_left_channel_vioce_process_t.start()
        self.operator_impact_t = threading.Thread(target=self.operator_impact)
        self.operator_impact_t.start()
    def play_left_channel_process(self):
        try:
            payload = "{\"devname\": \"" +  self.get_union_id + "\",\"req\": {\"A\": 303,\"P\": {\"event_type\":3,\"goods_id\":[\"left_channel\"]}}}"
            headers = {'Content-Type': "application/json", 'cache-control': "no-cache",
                       'Postman-Token': "1f4c5013-b7de-4404-ad2e-74cfb28aacc7"}
            response = requests.request("POST", self.url, data=payload, headers=headers)
            manual_paly_channel_org = json.loads(response.text)
            if manual_paly_channel_org["msg"].lower() == "success" or manual_paly_channel_org["msg"] == "IOT_CLIENT_RETURN_NO_CONTENT":
                time.sleep(5)
                wx.CallAfter(pub.sendMessage, "update", msg="vioce_stop")
                self.system_dlg.SetMessage("设置成功 !!!")
                self.system_dlg.ShowModal()
            elif manual_paly_channel_org["msg"] == "DEVICE_NAME_NOT_EXIST":
                wx.CallAfter(pub.sendMessage, "update", msg="vioce_stop")
                self.system_dlg.SetMessage("请输入正确的Union ID !!!")
                self.system_dlg.ShowModal()
            elif manual_paly_channel_org["msg"] == "RRPC_TIMEOUT":
                wx.CallAfter(pub.sendMessage, "update", msg="vioce_stop")
                self.system_dlg.SetMessage("超时，请重新查询 !!!")
                self.system_dlg.ShowModal()
            elif manual_paly_channel_org["msg"] == "DEVICE_OFFLINE":
                wx.CallAfter(pub.sendMessage, "update", msg="vioce_stop")
                self.system_dlg.SetMessage("设备离线,请检查设备 !!!")
                self.system_dlg.ShowModal()
            else:
                wx.CallAfter(pub.sendMessage, "update", msg="vioce_stop")
                self.system_dlg.SetMessage(vicoe_actual_send_value["msg"])
                self.system_dlg.ShowModal()
        except:
            wx.CallAfter(pub.sendMessage, "update", msg="vioce_stop")
            self.system_dlg.SetMessage(response.text)
            self.system_dlg.ShowModal()
    #右声道
    def play_right_channel(self,evt):
        self.count_time = 0
        self.count_time_alive = True
        self.vioce_query_send.Disable()
        self.vioce_set_send.Disable()
        self.vioce_back.Disable()
        self.left_channel_button.Disable()
        self.right_channel_button.Disable()
        self.welcome_button.Disable()
        self.goodbye_button.Disable()
        self.play_right_channel_vioce_process_t = threading.Thread(target=self.play_right_channel_process)
        self.play_right_channel_vioce_process_t.start()
        self.operator_impact_t = threading.Thread(target=self.operator_impact)
        self.operator_impact_t.start()
    def play_right_channel_process(self):
        try:
            payload = "{\"devname\": \"" +  self.get_union_id + "\",\"req\": {\"A\": 303,\"P\": {\"event_type\":3,\"goods_id\":[\"right_channel\"]}}}"
            headers = {'Content-Type': "application/json", 'cache-control': "no-cache",
                       'Postman-Token': "1f4c5013-b7de-4404-ad2e-74cfb28aacc7"}
            response = requests.request("POST", self.url, data=payload, headers=headers)
            manual_paly_channel_org = json.loads(response.text)
            if manual_paly_channel_org["msg"].lower() == "success" or manual_paly_channel_org["msg"] == "IOT_CLIENT_RETURN_NO_CONTENT":
                time.sleep(5)
                wx.CallAfter(pub.sendMessage, "update", msg="vioce_stop")
                self.system_dlg.SetMessage("设置成功 !!!")
                self.system_dlg.ShowModal()
            elif manual_paly_channel_org["msg"] == "DEVICE_NAME_NOT_EXIST":
                wx.CallAfter(pub.sendMessage, "update", msg="vioce_stop")
                self.system_dlg.SetMessage("请输入正确的Union ID !!!")
                self.system_dlg.ShowModal()
            elif manual_paly_channel_org["msg"] == "RRPC_TIMEOUT":
                wx.CallAfter(pub.sendMessage, "update", msg="vioce_stop")
                self.system_dlg.SetMessage("超时，请重新查询 !!!")
                self.system_dlg.ShowModal()
            elif manual_paly_channel_org["msg"] == "DEVICE_OFFLINE":
                wx.CallAfter(pub.sendMessage, "update", msg="vioce_stop")
                self.system_dlg.SetMessage("设备离线,请检查设备 !!!")
                self.system_dlg.ShowModal()
            else:
                wx.CallAfter(pub.sendMessage, "update", msg="vioce_stop")
                self.system_dlg.SetMessage(vicoe_actual_send_value["msg"])
                self.system_dlg.ShowModal()
        except:
            wx.CallAfter(pub.sendMessage, "update", msg="vioce_stop")
            self.system_dlg.SetMessage(response.text)
            self.system_dlg.ShowModal()
    #开门提示
    def play_welcome(self,evt):
        self.count_time = 0
        self.count_time_alive = True
        self.vioce_query_send.Disable()
        self.vioce_set_send.Disable()
        self.vioce_back.Disable()
        self.left_channel_button.Disable()
        self.right_channel_button.Disable()
        self.welcome_button.Disable()
        self.goodbye_button.Disable()
        self.play_welcome_vioce_process_t = threading.Thread(target=self.play_welcome_process)
        self.play_welcome_vioce_process_t.start()
        self.operator_impact_t = threading.Thread(target=self.operator_impact)
        self.operator_impact_t.start()
    def play_welcome_process(self):
        try:
            payload = "{\"devname\": \""+ self.get_union_id+ "\",\"req\": {\"A\": 303,\"P\": {\"event_type\":1}}}"
            headers = {'Content-Type': "application/json", 'cache-control': "no-cache",
                       'Postman-Token': "1f4c5013-b7de-4404-ad2e-74cfb28aacc7"}
            response = requests.request("POST", self.url, data=payload, headers=headers)
            manual_paly_channel_org = json.loads(response.text)
            if manual_paly_channel_org["msg"].lower() == "success" or manual_paly_channel_org["msg"] == "IOT_CLIENT_RETURN_NO_CONTENT":
                time.sleep(5)
                wx.CallAfter(pub.sendMessage, "update", msg="vioce_stop")
                self.system_dlg.SetMessage("设置成功 !!!")
                self.system_dlg.ShowModal()
            elif manual_paly_channel_org["msg"] == "DEVICE_NAME_NOT_EXIST":
                wx.CallAfter(pub.sendMessage, "update", msg="vioce_stop")
                self.system_dlg.SetMessage("请输入正确的Union ID !!!")
                self.system_dlg.ShowModal()
            elif manual_paly_channel_org["msg"] == "RRPC_TIMEOUT":
                wx.CallAfter(pub.sendMessage, "update", msg="vioce_stop")
                self.system_dlg.SetMessage("超时，请重新查询 !!!")
                self.system_dlg.ShowModal()
            elif manual_paly_channel_org["msg"] == "DEVICE_OFFLINE":
                wx.CallAfter(pub.sendMessage, "update", msg="vioce_stop")
                self.system_dlg.SetMessage("设备离线,请检查设备 !!!")
                self.system_dlg.ShowModal()
            else:
                wx.CallAfter(pub.sendMessage, "update", msg="vioce_stop")
                self.system_dlg.SetMessage(vicoe_actual_send_value["msg"])
                self.system_dlg.ShowModal()
        except:
            wx.CallAfter(pub.sendMessage, "update", msg="vioce_stop")
            self.system_dlg.SetMessage(response.text)
            self.system_dlg.ShowModal()
    #关门提示
    def play_goodbye(self,evt):
        self.count_time = 0
        self.count_time_alive = True
        self.vioce_query_send.Disable()
        self.vioce_set_send.Disable()
        self.vioce_back.Disable()
        self.left_channel_button.Disable()
        self.right_channel_button.Disable()
        self.welcome_button.Disable()
        self.goodbye_button.Disable()
        self.play_goodbye_vioce_process_t = threading.Thread(target=self.play_goodbye_process)
        self.play_goodbye_vioce_process_t.start()
        self.operator_impact_t = threading.Thread(target=self.operator_impact)
        self.operator_impact_t.start()
    def play_goodbye_process(self):
        try:
            payload = "{\"devname\": \""+ self.get_union_id+ "\",\"req\": {\"A\": 303,\"P\": {\"event_type\":2}}}"
            headers = {'Content-Type': "application/json", 'cache-control': "no-cache",
                       'Postman-Token': "1f4c5013-b7de-4404-ad2e-74cfb28aacc7"}
            response = requests.request("POST", self.url, data=payload, headers=headers)
            manual_paly_channel_org = json.loads(response.text)
            if manual_paly_channel_org["msg"].lower() == "success" or manual_paly_channel_org["msg"] == "IOT_CLIENT_RETURN_NO_CONTENT":
                time.sleep(5)
                wx.CallAfter(pub.sendMessage, "update", msg="vioce_stop")

                self.system_dlg.SetMessage("设置成功 !!!")
                self.system_dlg.ShowModal()
            elif manual_paly_channel_org["msg"] == "DEVICE_NAME_NOT_EXIST":
                wx.CallAfter(pub.sendMessage, "update", msg="vioce_stop")
                self.system_dlg.SetMessage("请输入正确的Union ID !!!")
                self.system_dlg.ShowModal()
            elif manual_paly_channel_org["msg"] == "RRPC_TIMEOUT":
                wx.CallAfter(pub.sendMessage, "update", msg="vioce_stop")
                self.system_dlg.SetMessage("超时，请重新查询 !!!")
                self.system_dlg.ShowModal()
            elif manual_paly_channel_org["msg"] == "DEVICE_OFFLINE":
                wx.CallAfter(pub.sendMessage, "update", msg="vioce_stop")
                self.system_dlg.SetMessage("设备离线,请检查设备 !!!")
                self.system_dlg.ShowModal()
            else:
                wx.CallAfter(pub.sendMessage, "update", msg="vioce_stop")
                self.system_dlg.SetMessage(vicoe_actual_send_value["msg"])
                self.system_dlg.ShowModal()
        except:
            wx.CallAfter(pub.sendMessage, "update", msg="vioce_stop")
            self.system_dlg.SetMessage(response.text)
            self.system_dlg.ShowModal()
    # 门锁操作
    def lock_operator(self, evt):
        self.lock_number = 1
        self.operator_muen_panel.Hide()
        self.init_panel.Hide()
        self.lock_panel = wx.ScrolledWindow(self, -1, pos=(0,0), size=(960, 500))
        self.lock_panel.SetBackgroundColour("#D8BFD8")
        self.system_message = wx.StaticText(self.lock_panel, -1, "", style=wx.ALIGN_CENTER_HORIZONTAL|wx.ST_NO_AUTORESIZE)
        self.font_lock_operator_tip = wx.Font(20, wx.DECORATIVE, wx.NORMAL, wx.LIGHT)
        self.system_message.SetFont(self.font_lock_operator_tip)
        self.system_message.SetForegroundColour("Red")
        self.system_message.SetBackgroundColour("Black")
        self.lock_box_stauts_h = wx.BoxSizer(wx.HORIZONTAL)
        self.lock_box_mode_h = wx.BoxSizer(wx.HORIZONTAL)
        self.lock_box_time_h = wx.BoxSizer(wx.HORIZONTAL)
        self.open_door_box_h = wx.BoxSizer(wx.HORIZONTAL)
        self.lock_times_h = wx.BoxSizer(wx.HORIZONTAL)
        self.lock_box_v = wx.BoxSizer(wx.VERTICAL)
        self.system_message_box=wx.BoxSizer(wx.HORIZONTAL)
        self.system_message_box.Add(self.system_message,1,wx.ALL|wx.EXPAND,2)
        self.lock_panel.SetScrollbar(1,1,1000,2000)
        self.lock_panel.SetScrollRate(10,10)
        self.font_lock = wx.Font(13, wx.DECORATIVE, wx.NORMAL, wx.LIGHT)
        self.lock_status_box = wx.StaticBox(self.lock_panel, -1, "")
        self.lock_status_box_size = wx.StaticBoxSizer(self.lock_status_box, wx.VERTICAL)
        self.lock_status_query = wx.StaticText(self.lock_panel, -1, "门锁状态")
        self.lock_status_query.SetFont(self.font_lock)
        self.lock_status_query.SetForegroundColour("Blue")
        self.door_status = wx.StaticText(self.lock_panel, -1, "门锁状态：")
        self.door_status.SetFont(self.font_lock)
        self.clock_status = wx.StaticText(self.lock_panel, -1, "门磁状态：")
        self.clock_status.SetFont(self.font_lock)
        self.lock_status_query_Bot = wx.Button(self.lock_panel, -1, "查询")
        self.lock_status_query_Bot.SetFont(self.font_lock)
        self.lock_status_query_Bot.SetForegroundColour("Blue")
        self.Bind(wx.EVT_BUTTON, self.send_lock_query, self.lock_status_query_Bot)
        self.lock_box_stauts_h.Add(self.lock_status_query, 1, wx.ALIGN_CENTER)
        self.lock_box_stauts_h.Add(self.door_status, 1, wx.ALIGN_CENTER)
        self.lock_box_stauts_h.Add(self.clock_status, 1, wx.ALIGN_CENTER)
        self.lock_box_stauts_h.Add(self.lock_status_query_Bot, 1, wx.ALIGN_CENTER)
        self.lock_status_box_size.Add(self.lock_box_stauts_h, 1, wx.ALL | wx.EXPAND, 2)
        self.lock_mode = wx.StaticText(self.lock_panel, -1, "门锁模式")
        self.lock_mode.SetFont(self.font_lock)
        self.lock_mode.SetForegroundColour("Blue")
        # self.lock_mode_chose=wx.RadioBox(self.lock_panel,label="",choices=["单门","双门"],majorDimension =1,style=wx.RA_SPECIFY_ROWS)
        # self.lock_mode_chose.SetFont(self.font_lock)
        # self.lock_mode_chose.SetForegroundColour("Blue")
        # self.lock_mode_chose.Bind(wx.EVT_RADIOBOX,self.select_mode)
        self.lock_mode_chose_a = wx.RadioButton(self.lock_panel, -1, label="单门", style=wx.RB_GROUP)
        self.lock_mode_chose_a.SetFont(self.font_lock)
        self.lock_mode_chose_a.SetForegroundColour("Blue")
        self.lock_mode_chose_b = wx.RadioButton(self.lock_panel, -1, label="双门")
        self.lock_mode_chose_b.SetFont(self.font_lock)
        self.lock_mode_chose_b.SetForegroundColour("Blue")
        self.Bind(wx.EVT_RADIOBUTTON, self.select_mode)
        self.lock_mode_send = wx.Button(self.lock_panel, -1, "设置")
        self.lock_mode_send.SetFont(self.font_lock)
        self.lock_mode_send.SetForegroundColour("Blue")
        self.Bind(wx.EVT_BUTTON, self.lock_mode_send_process, self.lock_mode_send)
        self.lock_time_index = wx.StaticText(self.lock_panel, -1, "落锁时间")
        self.lock_time_index.SetFont(self.font_lock)
        self.lock_time_index.SetForegroundColour("Blue")
        self.lock_times = wx.TextCtrl(self.lock_panel, -1)
        self.lock_times.SetFont(self.font_lock)
        self.lock_times.SetForegroundColour("Blue")
        self.lock_times_send = wx.Button(self.lock_panel, -1, "设置")
        self.lock_times_send.SetFont(self.font_lock)
        self.lock_times_send.SetForegroundColour("Blue")
        self.lock_time_actual = wx.StaticText(self.lock_panel, -1, "")
        self.lock_time_actual.SetFont(self.font_lock)
        self.lock_time_actual.SetForegroundColour("Blue")
        self.lock_times_box = wx.StaticBox(self.lock_panel, -1, "")
        self.lock_times_box_size = wx.StaticBoxSizer(self.lock_times_box, wx.VERTICAL)
        self.lock_times_h.Add(self.lock_time_index, 1, wx.ALL | wx.EXPAND, 2)
        self.lock_times_h.Add(self.lock_times, 1, wx.ALL | wx.EXPAND, 2)
        self.lock_times_h.Add(self.lock_time_actual, 1, wx.ALL | wx.EXPAND, 2)
        self.lock_times_h.Add(self.lock_times_send, 1, wx.ALL | wx.EXPAND, 2)
        self.lock_times_box_size.Add(self.lock_times_h, 1, wx.ALL | wx.EXPAND, 2)
        self.Bind(wx.EVT_BUTTON, self.set_lock_time, self.lock_times_send)
        self.lock_mode_box = wx.StaticBox(self.lock_panel, -1, "")
        self.lock_mode_box_size = wx.StaticBoxSizer(self.lock_mode_box, wx.VERTICAL)
        self.lock_box_mode_h.Add(self.lock_mode, 1, wx.ALL | wx.EXPAND, 2)
        self.lock_box_mode_h.Add(self.lock_mode_chose_a, 1, wx.ALL | wx.EXPAND, 2)
        self.lock_box_mode_h.Add(self.lock_mode_chose_b, 1, wx.ALL | wx.EXPAND, 2)
        self.lock_box_mode_h.Add(self.lock_mode_send, 1, wx.ALL | wx.EXPAND, 2)
        self.lock_mode_box_size.Add(self.lock_box_mode_h, 1, wx.ALL | wx.EXPAND, 2)
        self.open_door = wx.Button(self.lock_panel, -1, "管理员开锁")
        self.open_door.SetFont(self.font_lock)
        self.open_door.SetForegroundColour("Blue")
        self.Bind(wx.EVT_BUTTON, self.open_door_send, self.open_door)
        self.open_door_box = wx.StaticBox(self.lock_panel, -1)
        self.open_door_box_size = wx.StaticBoxSizer(self.open_door_box, wx.VERTICAL)
        self.open_door_box_h.Add(self.open_door, 1, wx.ALL | wx.EXPAND, 2)
        self.open_door_box_size.Add(self.open_door_box_h, 1, wx.ALL | wx.EXPAND, 2)
        self.lock_operator_back = wx.Button(self.lock_panel, -1, "返回主菜单")
        self.Bind(wx.EVT_BUTTON, self.lock_back, self.lock_operator_back)
        self.lock_operator_back.SetFont(self.font_lock)
        self.lock_operator_back.SetForegroundColour("Blue")
        self.lock_operator_back_box = wx.StaticBox(self.lock_panel, -1)
        self.lock_operator_back_box_size = wx.StaticBoxSizer(self.lock_operator_back_box, wx.VERTICAL)
        self.lock_operator_back_box_size.Add(self.lock_operator_back, 1, wx.ALL | wx.EXPAND, 2)
        self.lock_box_v.Add(self.system_message_box, 0, wx.ALL | wx.EXPAND, 1)
        self.lock_box_v.Add(self.lock_status_box_size, 0, wx.ALL | wx.EXPAND, 1)
        self.lock_box_v.Add(self.lock_mode_box_size, 0, wx.ALL | wx.EXPAND, 1)
        self.lock_box_v.Add(self.lock_times_box_size, 0, wx.ALL | wx.EXPAND, 1)
        self.lock_box_v.Add(self.open_door_box_size, 0, wx.ALL | wx.EXPAND, 1)
        self.lock_box_v.Add(self.lock_operator_back_box_size, 0, wx.ALL | wx.EXPAND, 1)
        self.lock_panel.SetSizer(self.lock_box_v)
        self.lock_panel.Layout()
        self.lock_panel.Fit()
        pub.subscribe(self.system_operator_tip, "update")

    # 开锁操作
    def open_door_send(self, evt):
        self.count_time = 0
        self.count_time_alive = True
        self.lock_status_query_Bot.Disable()
        self.lock_mode_send.Disable()
        self.lock_times_send.Disable()
        self.lock_operator_back.Disable()
        self.open_door.Disable()
        self.open_door_process_t = threading.Thread(target=self.open_door_process)
        self.open_door_process_t.start()
        self.operator_impact_t = threading.Thread(target=self.operator_impact)
        self.operator_impact_t.start()

    def open_door_process(self):
        try:
            payload_open_door = "{\n    \"devname\": \"" + self.get_union_id + "\",\n    \"req\": {\n        \"A\": 51,\n        \"P\": {\n            \"lockid\": \"1-1-1\",\n            \"transid\": \"1234567890\"\n        }\n    }\n}\n"
            headers_open_door = {
                'Content-Type': "application/json",
                'cache-control': "no-cache",
                'Postman-Token': "c4f9303e-0d6e-40c7-afdc-97e93a739475"
            }

            response_open_door = requests.request("POST", self.url, data=payload_open_door, headers=headers_open_door)
            open_door_status = json.loads(response_open_door.text)
            if open_door_status["msg"].lower() == "success":
                wx.CallAfter(pub.sendMessage, "update", msg="stop")
                self.system_dlg.SetMessage("开锁成功!!!")
                self.system_dlg.ShowModal()

            elif open_door_status["msg"] == "DEVICE_NAME_NOT_EXIST":
                wx.CallAfter(pub.sendMessage, "update", msg="stop")
                self.system_dlg.SetMessage("请输入正确的Union ID !!!")
                self.system_dlg.ShowModal()

                # Mymsg = wx.MessageBox("请输入正确的Union ID !!", "Message box", style=wx.OK | wx.CANCEL)
            elif open_door_status["msg"] == "RRPC_TIMEOUT":
                wx.CallAfter(pub.sendMessage, "update", msg="stop")
                self.system_dlg.SetMessage("超时，请重新查询 !!!")
                self.system_dlg.ShowModal()

                # Mymsg = wx.MessageBox("超时，请重新查询!!", "Message box", style=wx.OK | wx.CANCEL)
            elif open_door_status["msg"] == "DEVICE_OFFLINE":
                wx.CallAfter(pub.sendMessage, "update", msg="stop")
                self.system_dlg.SetMessage("设备离线！请检查设备!!!")
                self.system_dlg.ShowModal()

                # Mymsg = wx.MessageBox("设备离线！请检查设备！", "Message box", style=wx.OK | wx.CANCEL)
            elif open_door_status["msg"] == "The deviceName format is incorrect.":
                wx.CallAfter(pub.sendMessage, "update", msg="stop")
                self.system_dlg.SetMessage("Union ID格式错误!!!")
                self.system_dlg.ShowModal()

                # Mymsg = wx.MessageBox("Union ID格式错误！", "Message box", style=wx.OK | wx.CANCEL)
            else:
                wx.CallAfter(pub.sendMessage, "update", msg="stop")
                self.system_dlg.SetMessage(response_open_door.text)
                self.system_dlg.ShowModal()

                # Mymsg = wx.MessageBox(response_frp_open.text, "Message box", style=wx.OK | wx.CANCEL)
        except:
            wx.CallAfter(pub.sendMessage, "update", msg="stop")
            self.system_dlg.SetMessage("开锁失败!!!")
            self.system_dlg.ShowModal()

            # Mymsg = wx.MessageBox("FRP 启动失败!!!", "Message box", style=wx.OK | wx.CANCEL)



    # 返回主菜单
    def lock_back(self, evt):
        self.lock_panel.Destroy()
        self.init_panel.Show()
        #self.lock_operator_tip_panel.Destroy()
        self.operator_muen_panel.Show()

    # 设置开锁时间
    def set_lock_time(self, evt):
        self.count_time = 0
        self.count_time_alive = True
        self.lock_status_query_Bot.Disable()
        self.lock_mode_send.Disable()
        self.lock_times_send.Disable()
        self.lock_operator_back.Disable()
        self.open_door.Disable()
        self.set_lock_time_process_t = threading.Thread(target=self.set_lock_time_process)
        self.set_lock_time_process_t.start()

        self.operator_impact_t = threading.Thread(target=self.operator_impact)
        self.operator_impact_t.start()

    def set_lock_time_process(self):
        opentime = self.lock_times.GetValue()
        if opentime == "":
            wx.CallAfter(pub.sendMessage, "update", msg="stop")
            self.system_dlg.SetMessage("请输入时间!!!")
            self.system_dlg.ShowModal()

        elif not opentime.isdigit():
            wx.CallAfter(pub.sendMessage, "update", msg="stop")
            self.system_dlg.SetMessage("请输入数字格式!!!")
            self.system_dlg.ShowModal()

        else:
            try:
                payload_lock_time = "{\n    \"devname\": \"" + self.get_union_id + "\",\n    \"req\": {\n        \"A\": 53,\n        \"P\":{\n        \"lockid\": \"1-1-1\",\n        \"opentime\": " + opentime + "\n        }\n    }\n}"
                headers = {
                    'Content-Type': "application/json",
                    'cache-control': "no-cache",
                    'Postman-Token': "01763680-c613-401f-a758-3a1aea1fe2fc"
                }

                response_lock_time = requests.request("POST", self.url, data=payload_lock_time, headers=headers)
                door_opentime = json.loads(response_lock_time.text)
                if door_opentime["msg"].lower() == "success":
                    times_index = "当前落锁时间 " + opentime
                    self.lock_time_actual.SetLabel(times_index)
                    wx.CallAfter(pub.sendMessage, "update", msg="stop")
                    self.system_dlg.SetMessage("设置成功!!!")
                    self.system_dlg.ShowModal()

                elif door_opentime["msg"] == "DEVICE_NAME_NOT_EXIST":
                    wx.CallAfter(pub.sendMessage, "update", msg="stop")
                    self.system_dlg.SetMessage("请输入正确的Union ID!!!")
                    self.system_dlg.ShowModal()

                elif door_opentime["msg"] == "RRPC_TIMEOUT":
                    wx.CallAfter(pub.sendMessage, "update", msg="stop")
                    self.system_dlg.SetMessage("超时，请重新查询!!!")
                    self.system_dlg.ShowModal()

                elif door_opentime["msg"] == "DEVICE_OFFLINE":
                    wx.CallAfter(pub.sendMessage, "update", msg="stop")
                    self.system_dlg.SetMessage("设备离线!请检查设备!!!")
                    self.system_dlg.ShowModal()

                else:
                    wx.CallAfter(pub.sendMessage, "update", msg="stop")
                    self.system_dlg.SetMessage(door_opentime["msg"])
                    self.system_dlg.ShowModal()

            except:
                wx.CallAfter(pub.sendMessage, "update", msg="stop")
                self.system_dlg.SetMessage(response_lock_time.text)
                self.system_dlg.ShowModal()

    # 单双门锁模式选择
    def select_mode(self, evt):
        lock_mode = evt.GetEventObject()
        if lock_mode.GetLabel() == "单门":
            self.lock_number = 1
        elif lock_mode.GetLabel() == "双门":
            self.lock_number = 2
        # print (self.lock_mode_chose.GetSelection())

    # 门锁状态查询
    def send_lock_query(self, evt):
        self.count_time = 0
        self.count_time_alive = True
        self.lock_status_query_Bot.Disable()
        self.lock_mode_send.Disable()
        self.lock_times_send.Disable()
        self.lock_operator_back.Disable()
        self.open_door.Disable()
        self.query_lock_status_process_t = threading.Thread(target=self.query_lock_status_process)
        self.query_lock_status_process_t.start()

        self.operator_impact_t = threading.Thread(target=self.operator_impact)
        self.operator_impact_t.start()

    def query_lock_status_process(self):
        try:
            payload = "{\r\n    \"devname\": \"" + self.get_union_id + "\",\r\n    \"req\": {\r\n        \"A\": 52,\r\n        \"P\": {\r\n            \"lockid\": \"1-1-1\"\r\n        }\r\n    }\r\n}"
            headers = {
                'Content-Type': "application/json",
                'Authorization': "Basic YWRtaW46Y2poeXkzMDA=",
                'cache-control': "no-cache",
                'Postman-Token': "67a08d86-a31f-48ae-ac30-a135e900e86d"
            }
            response = requests.request("POST", self.url, data=payload, headers=headers)
            lock_door_status = json.loads(response.text)
            if lock_door_status["msg"] == "DEVICE_NAME_NOT_EXIST":
                wx.CallAfter(pub.sendMessage, "update", msg="stop")
                self.system_dlg.SetMessage("请输入正确的Union ID !!!")
                self.system_dlg.ShowModal()

            elif lock_door_status["msg"] == "RRPC_TIMEOUT":
                wx.CallAfter(pub.sendMessage, "update", msg="stop")
                self.system_dlg.SetMessage("超时，请重新查询 !!!")
                self.system_dlg.ShowModal()

            elif lock_door_status["msg"] == "DEVICE_OFFLINE":
                wx.CallAfter(pub.sendMessage, "update", msg="stop")
                self.system_dlg.SetMessage("设备离线！请检查设备!!!")
                self.system_dlg.ShowModal()

            elif lock_door_status["msg"].lower() == "success":
                wx.CallAfter(pub.sendMessage, "update", msg="stop")
                self.system_dlg.SetMessage("查询成功!!!")
                self.system_dlg.ShowModal()

                lock_status = lock_door_status["output"]["locked"]
                closed_status = lock_door_status["output"]["closed"]
                if lock_status == 1:
                    self.clock_status.SetLabel("门锁状态：关")
                    self.clock_status.SetBackgroundColour("Green")
                else:
                    self.clock_status.SetLabel("门锁状态：开")
                    self.clock_status.SetBackgroundColour("Red")
                if closed_status == 1:
                    self.door_status.SetLabel("门磁状态：关")
                    self.door_status.SetBackgroundColour("Green")
                else:
                    self.door_status.SetLabel("门磁状态：开")
                    self.door_status.SetBackgroundColour("Red")
            elif lock_door_status["msg"] == "The deviceName format is incorrect.":
                wx.CallAfter(pub.sendMessage, "update", msg="stop")
                self.system_dlg.SetMessage("Union ID格式错误!!!")
                self.system_dlg.ShowModal()

            else:
                wx.CallAfter(pub.sendMessage, "update", msg="stop")
                self.system_dlg.SetMessage(lock_door_status["msg"])
                self.system_dlg.ShowModal()

        except:
            wx.CallAfter(pub.sendMessage, "update", msg="stop")
            self.system_dlg.SetMessage(response.text)
            self.system_dlg.ShowModal()

    #  门锁模式设置
    def lock_mode_send_process(self, evt):
        self.user_name_dlg.ShowModal()
        if self.user_name_dlg.ShowModal() == wx.ID_OK:
            self.user_name_ssh = self.user_name_dlg.GetValue()
            self.user_name_dlg.Destroy()
        else:
            return
        self.pw_dlg.ShowModal()
        if self.pw_dlg.ShowModal() == wx.ID_OK:
            self.pw_ssh = self.pw_dlg.GetValue()
            self.pw_dlg.Destroy()
        else:
            return
        self.count_time = 0
        self.count_time_alive = True
        self.lock_status_query_Bot.Disable()
        self.lock_mode_send.Disable()
        self.lock_times_send.Disable()
        self.lock_operator_back.Disable()
        self.open_door.Disable()
        self.lock_mode_t = threading.Thread(target=self.look_mode_send_to_devid)
        self.lock_mode_t.start()
        self.operator_impact_t = threading.Thread(target=self.operator_impact)
        self.operator_impact_t.start()

    def look_mode_send_to_devid(self):
        try:
            if len(self.dev_id.GetValue()) == 5:
                port_id = self.dev_id.GetValue()
            else:
                port_id = "2" + self.dev_id.GetValue()
            sshid = int(port_id)
            payload_frp = "{\"devname\": \"" + self.get_union_id + "\", \"req\": { \"A\": 152,\"P\": { \"appname\": \"frp-client-ssh\", \"action\": 4,\"port\":\""+ str(self.dev_id.GetValue())+"\" }}}"
            headers_frp = {
                'Content-Type': "application/json",
                'cache-control': "no-cache",
                'Postman-Token': "0b5b07b3-c756-4359-88b9-da388c58324d"
            }
            response_frp_open = requests.request("POST", self.url, data=payload_frp, headers=headers_frp)
            frp_status = json.loads(response_frp_open.text)
            if frp_status["msg"].lower() == "success":
                pid = frp_status["output"]["pid"]
                while True:
                    loop_time = 0
                    try:
                        payload_pid = "{\n    \"devname\": \"" + self.get_union_id + "\",\n    \"req\": {\n        \"A\": 153,\n        \"P\": {\n          \"pid\":\"" + pid + "\"\n        }\n    }\n}\n"
                        headers_pid = {
                            'Content-Type': "application/json",
                            'cache-control': "no-cache",
                            'Postman-Token': "20e0e8d2-28c2-4f7b-be6b-89b6b2451d60"
                        }
                        response_pid = requests.request("POST", self.url, data=payload_pid, headers=headers_pid)
                        pid_status = json.loads(response_pid.text)
                        if pid_status["msg"].lower() == "success":
                            if pid_status["output"]["state"] == "completed":
                                try:
                                    hostid = "m.vegcloud.tech"
                                    name = self.user_name_ssh
                                    pwd = self.pw_ssh
                                    myclient = paramiko.SSHClient()
                                    myclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                    myclient.connect(hostid, port=sshid, username=name, password=pwd, allow_agent=False,
                                                     look_for_keys=False)
                                    time.sleep(5)
                                    stdin, stdout, stderr = myclient.exec_command('sudo systemctl stop door')
                                    time.sleep(2)
                                    stdin, stdout, stderr = myclient.exec_command('sudo systemctl status door')
                                    respons = stdout.read()
                                    if re.findall(r' Active: inactive', respons.decode()):
                                        time.sleep(1)
                                        stdin, stdout, stderr = myclient.exec_command('sudo rm /vbg/store_door.db')
                                        time.sleep(1)
                                        stdin, stdout, stderr = myclient.exec_command('sudo ls /vbg')
                                        respons_db = stdout.read()
                                        break
                                except:
                                    wx.CallAfter(pub.sendMessage, "update", msg="stop")
                                    self.system_dlg.SetMessage("SSH 登入失败!!!")
                                    self.system_dlg.ShowModal()

                                    # Mymsg = wx.MessageBox("SSH 登入失败!!!", "Message box", style=wx.OK | wx.CANCEL)
                                    break
                            elif pid_status["output"]["state"] == "running":
                                continue
                        elif loop_time > 30:
                            wx.CallAfter(pub.sendMessage, "update", msg="stop")
                            self.lock_dlg.SetMessage("FRP 启动超时!!!")
                            self.lock_dlg.ShowModal()

                            # Mymsg = wx.MessageBox("FRP 启动超时!!!", "Message box", style=wx.OK | wx.CANCEL)
                            break
                        else:
                            wx.CallAfter(pub.sendMessage, "update", msg="stop")
                            self.lock_dlg.SetMessage(pid_status["msg"])
                            self.lock_dlg.ShowModal()

                            # Mymsg = wx.MessageBox(pid_status["msg"], "Message box", style=wx.OK | wx.CANCEL)
                            break
                    except:
                        wx.CallAfter(pub.sendMessage, "update", msg="stop")
                        self.system_dlg.SetMessage("查询PID失败!!!")
                        self.system_dlg.ShowModal()

                        break
                        # Mymsg = wx.MessageBox("查询PID失败!!!", "Message box", style=wx.OK | wx.CANCEL)
                    time.sleep(1)
                    loop_time += 1
                if re.findall(r"store_door.db", respons_db.decode()):
                    wx.CallAfter(pub.sendMessage, "update", msg="stop")
                    self.system_dlg.SetMessage("删除DB失败!!!")
                    self.system_dlg.ShowModal()

                    # Mymsg = wx.MessageBox("删除DB失败!!!", "Message box", style=wx.OK | wx.CANCEL)
                else:
                    stdin, stdout, stderr = myclient.exec_command('sudo systemctl start door')
                    time.sleep(5)
                    stdin, stdout, stderr = myclient.exec_command('sudo systemctl status door')
                    respons_restart = stdout.read()
                    myclient.close()
                    if re.findall(r" Active: active", respons_restart.decode()):
                        try:
                            payload_set_mode = "{\n    \"devname\": \"" + self.get_union_id + "\",\n    \"req\": {\n        \"A\": 55,\n        \"P\": {\n            \"lockid\": \"1-1-1\",\n            \"locknumber\":" + str(
                                self.lock_number) + "\n        }\n    }\n}"
                            headers_set_mode = {
                                'Content-Type': "application/json",
                                'cache-control': "no-cache",
                                'Postman-Token': "467bea96-3f3a-485a-a562-acbf04871c52"
                            }
                            response_number = requests.request("POST", self.url, data=payload_set_mode,
                                                               headers=headers_set_mode)
                            lock_number_status = json.loads(response_number.text)
                            if lock_number_status["msg"].lower() == "success":
                                wx.CallAfter(pub.sendMessage, "update", msg="stop")
                                self.system_dlg.SetMessage("门锁模式设置成功!!!")
                                self.system_dlg.ShowModal()

                                # Mymsg = wx.MessageBox("门锁模式设置成功!!!", "Message box", style=wx.OK | wx.CANCEL)

                            else:
                                wx.CallAfter(pub.sendMessage, "update", msg="stop")
                                self.system_dlg.SetMessage("门锁模式设置失败!!!")
                                self.system_dlg.ShowModal()

                                # Mymsg = wx.MessageBox("门锁模式设置失败!!!", "Message box", style=wx.OK | wx.CANCEL)
                        except:
                            wx.CallAfter(pub.sendMessage, "update", msg="stop")
                            self.system_dlg.SetMessage(response_number.text)
                            self.system_dlg.ShowModal()

                            # Mymsg = wx.MessageBox(response_number.text, "Message box", style=wx.OK | wx.CANCEL)
            elif frp_status["msg"] == "DEVICE_NAME_NOT_EXIST":
                wx.CallAfter(pub.sendMessage, "update", msg="stop")
                self.system_dlg.SetMessage("请输入正确的Union ID !!!")
                self.system_dlg.ShowModal()

                # Mymsg = wx.MessageBox("请输入正确的Union ID !!", "Message box", style=wx.OK | wx.CANCEL)
            elif frp_status["msg"] == "RRPC_TIMEOUT":
                wx.CallAfter(pub.sendMessage, "update", msg="stop")
                self.system_dlg.SetMessage("超时，请重新查询 !!!")
                self.system_dlg.ShowModal()

                # Mymsg = wx.MessageBox("超时，请重新查询!!", "Message box", style=wx.OK | wx.CANCEL)
            elif frp_status["msg"] == "DEVICE_OFFLINE":
                wx.CallAfter(pub.sendMessage, "update", msg="stop")
                self.system_dlg.SetMessage("设备离线！请检查设备!!!")
                self.system_dlg.ShowModal()

                # Mymsg = wx.MessageBox("设备离线！请检查设备！", "Message box", style=wx.OK | wx.CANCEL)
            elif frp_status["msg"] == "The deviceName format is incorrect.":
                wx.CallAfter(pub.sendMessage, "update", msg="stop")
                self.system_dlg.SetMessage("Union ID格式错误!!!")
                self.system_dlg.ShowModal()

                # Mymsg = wx.MessageBox("Union ID格式错误！", "Message box", style=wx.OK | wx.CANCEL)
            else:
                wx.CallAfter(pub.sendMessage, "update", msg="stop")
                self.system_dlg.SetMessage(response_frp_open.text)
                self.system_dlg.ShowModal()


        except:
            wx.CallAfter(pub.sendMessage, "update", msg="stop")
            self.system_dlg.SetMessage("FRP 启动失败!!!")
            self.system_dlg.ShowModal()

            # Mymsg = wx.MessageBox("FRP 启动失败!!!", "Message box", style=wx.OK | wx.CANCEL)

    # 设置子进程
    def system_operator_tip(self, msg):
        if msg == "running":
            self.count_time += 1
            system_message_lable = "配置中请稍后!,运行 " + str(self.count_time) + " 秒"
            self.system_message.SetLabel(system_message_lable)
        elif msg == "stop":
            self.count_time_alive = False
            self.lock_status_query_Bot.Enable()
            self.lock_mode_send.Enable()
            self.lock_times_send.Enable()
            self.lock_operator_back.Enable()
            self.open_door.Enable()
            #self.weight_attr_set_button.Enable()
            #self.weight_attr_auery_button.Enable()
            self.system_message.SetLabel("")
        elif msg == "vioce_stop":
            self.count_time_alive = False
            self.vioce_query_send.Enable()
            self.vioce_set_send.Enable()
            self.vioce_back.Enable()
            self.left_channel_button.Enable()
            self.right_channel_button.Enable()
            self.welcome_button.Enable()
            self.goodbye_button.Enable()
            self.system_message.SetLabel("")
        elif msg == "query_csq_stop":
            self.count_time_alive = False
            self.query_button_scq.Enable()
            self.query_button_ccid.Enable()
            self.cellular_back.Enable()
            self.system_message.SetLabel("")
        elif msg == "query_ccid_stop":
            self.count_time_alive = False
            self.query_button_scq.Enable()
            self.query_button_ccid.Enable()
            self.cellular_back.Enable()
            self.system_message.SetLabel("")
        elif msg == "calc_weight_stop":
            self.count_time_alive = False
            self.weigh_stability_button.Enable()
            self.goods_weight_button.Enable()
            self.weigh_back.Enable()
            self.weigh_weight_button.Enable()
            self.system_message.SetLabel("")
        elif msg == "weigh_weight_stop":
            self.count_time_alive = False
            self.weigh_stability_button.Enable()
            self.goods_weight_button.Enable()
            self.weigh_back.Enable()
            self.weigh_weight_button.Enable()
            self.weight_attr_set_button.Enable()
            self.weight_attr_auery_button.Enable()
            self.system_message.SetLabel("")
            self.weigh_weight_index_1_l.SetLabel("")
            self.weigh_weight_value_1_l.SetLabel("")
            self.weigh_weight_value_1_l.SetBackgroundColour("")
            self.weigh_weight_index_1_r.SetLabel("")
            self.weigh_weight_value_1_r.SetLabel("")
            self.weigh_weight_value_1_r.SetBackgroundColour("")
            self.weigh_weight_index_2_l.SetLabel("")
            self.weigh_weight_value_2_l.SetLabel("")
            self.weigh_weight_value_2_l.SetBackgroundColour("")
            self.weigh_weight_index_2_r.SetLabel("")
            self.weigh_weight_value_2_r.SetLabel("")
            self.weigh_weight_value_2_r.SetBackgroundColour("")
            self.weigh_weight_index_3_l.SetLabel("")
            self.weigh_weight_value_3_l.SetLabel("")
            self.weigh_weight_value_3_l.SetBackgroundColour("")
            self.weigh_weight_index_3_r.SetLabel("")
            self.weigh_weight_value_3_r.SetLabel("")
            self.weigh_weight_value_3_r.SetBackgroundColour("")
            self.weigh_weight_index_4_l.SetLabel("")
            self.weigh_weight_value_4_l.SetLabel("")
            self.weigh_weight_value_4_l.SetBackgroundColour("")
            self.weigh_weight_index_4_r.SetLabel("")
            self.weigh_weight_value_4_r.SetLabel("")
            self.weigh_weight_value_4_r.SetBackgroundColour("")
            self.weigh_weight_index_5_l.SetLabel("")
            self.weigh_weight_value_5_l.SetLabel("")
            self.weigh_weight_value_5_l.SetBackgroundColour("")
            self.weigh_weight_index_5_r.SetLabel("")
            self.weigh_weight_value_5_r.SetLabel("")
            self.weigh_weight_value_5_r.SetBackgroundColour("")
            self.get_weigh_weight_box_actural_h_1.Clear()
            self.get_weigh_weight_box_actural_h_2.Clear()
            self.get_weigh_weight_box_actural_h_3.Clear()
            self.get_weigh_weight_box_actural_h_4.Clear()
            self.get_weigh_weight_box_actural_h_5.Clear()
            self.get_weigh_weight_box_size.Detach(self.get_weigh_weight_box_actural_h_1)
            self.get_weigh_weight_box_size.Detach(self.get_weigh_weight_box_actural_h_2)
            self.get_weigh_weight_box_size.Detach(self.get_weigh_weight_box_actural_h_3)
            self.get_weigh_weight_box_size.Detach(self.get_weigh_weight_box_actural_h_4)
            self.get_weigh_weight_box_size.Detach(self.get_weigh_weight_box_actural_h_5)
            self.weigh_panel.SetSizer(self.weigh_box_v)
            self.weigh_panel.Layout()
            self.weigh_panel.Fit()
            select_devid_type = self.devide_type.GetValue()
            if select_devid_type == "3112":
                self.weigh_weight_index_1_l.SetLabel("第一层")
                self.weigh_weight_value_1_l.SetLabel(str(self.weigh_weight_dict["010101"]))
                if self.weigh_weight_online["010101"]:
                    self.weigh_weight_value_1_l.SetBackgroundColour("Green")
                else:
                    self.weigh_weight_value_1_l.SetBackgroundColour("Red")
                self.weigh_weight_index_2_l.SetLabel("第二层")
                self.weigh_weight_value_2_l.SetLabel(str(self.weigh_weight_dict["010201"]))
                if self.weigh_weight_online["010201"]:
                    self.weigh_weight_value_2_l.SetBackgroundColour("Green")
                else:
                    self.weigh_weight_value_2_l.SetBackgroundColour("Red")
                #self.weigh_weight_value_2_l.SetBackgroundColour("Green")
                self.weigh_weight_index_3_l.SetLabel("第三层")
                self.weigh_weight_value_3_l.SetLabel(str(self.weigh_weight_dict["010301"]))
                if self.weigh_weight_online["010301"]:
                    self.weigh_weight_value_3_l.SetBackgroundColour("Green")
                else:
                    self.weigh_weight_value_3_l.SetBackgroundColour("Red")
                #self.weigh_weight_value_3_l.SetBackgroundColour("Green")
                self.weigh_weight_index_4_l.SetLabel("第四层左")
                self.weigh_weight_value_4_l.SetLabel(str(self.weigh_weight_dict["010401"]))
                if self.weigh_weight_online["010401"]:
                    self.weigh_weight_value_4_l.SetBackgroundColour("Green")
                else:
                    self.weigh_weight_value_4_l.SetBackgroundColour("Red")
                #self.weigh_weight_value_4_l.SetBackgroundColour("Green")
                self.weigh_weight_index_4_r.SetLabel("第四层右")
                self.weigh_weight_value_4_r.SetLabel(str(self.weigh_weight_dict["010402"]))
                if self.weigh_weight_online["010402"]:
                    self.weigh_weight_value_4_r.SetBackgroundColour("Green")
                else:
                    self.weigh_weight_value_4_r.SetBackgroundColour("Red")
                #self.weigh_weight_value_4_r.SetBackgroundColour("Green")
                self.get_weigh_weight_box_actural_h_1.Add(self.weigh_weight_index_1_l, 1, wx.ALL | wx.EXPAND, 2)
                self.get_weigh_weight_box_actural_h_1.Add(self.weigh_weight_value_1_l, 1, wx.ALL | wx.EXPAND, 2)
                self.get_weigh_weight_box_actural_h_2.Add(self.weigh_weight_index_2_l, 1, wx.ALL | wx.EXPAND, 2)
                self.get_weigh_weight_box_actural_h_2.Add(self.weigh_weight_value_2_l, 1, wx.ALL | wx.EXPAND, 2)
                self.get_weigh_weight_box_actural_h_3.Add(self.weigh_weight_index_3_l, 1, wx.ALL | wx.EXPAND, 2)
                self.get_weigh_weight_box_actural_h_3.Add(self.weigh_weight_value_3_l, 1, wx.ALL | wx.EXPAND, 2)
                self.get_weigh_weight_box_actural_h_4.Add(self.weigh_weight_index_4_l, 1, wx.ALL | wx.EXPAND, 2)
                self.get_weigh_weight_box_actural_h_4.Add(self.weigh_weight_value_4_l, 1, wx.ALL | wx.EXPAND, 2)
                self.get_weigh_weight_box_actural_h_5.Add(self.weigh_weight_index_4_r, 1, wx.ALL | wx.EXPAND, 2)
                self.get_weigh_weight_box_actural_h_5.Add(self.weigh_weight_value_4_r, 1, wx.ALL | wx.EXPAND, 2)
                self.get_weigh_weight_box_size.Add(self.get_weigh_weight_box_actural_h_1, 1, wx.ALL | wx.EXPAND, 2)
                self.get_weigh_weight_box_size.Add(self.get_weigh_weight_box_actural_h_2, 1, wx.ALL | wx.EXPAND, 2)
                self.get_weigh_weight_box_size.Add(self.get_weigh_weight_box_actural_h_3, 1, wx.ALL | wx.EXPAND, 2)
                self.get_weigh_weight_box_size.Add(self.get_weigh_weight_box_actural_h_4, 1, wx.ALL | wx.EXPAND, 2)
                self.get_weigh_weight_box_size.Add(self.get_weigh_weight_box_actural_h_5, 1, wx.ALL | wx.EXPAND, 2)
                self.weigh_panel.SetSizer(self.weigh_box_v)
                self.weigh_panel.Layout()
                self.weigh_panel.Fit()

            elif select_devid_type == "4100":
                self.weigh_weight_index_1_l.SetLabel("第一层")
                self.weigh_weight_value_1_l.SetLabel(str(self.weigh_weight_dict["010101"]))
                if self.weigh_weight_online["010101"]:
                    self.weigh_weight_value_1_l.SetBackgroundColour("Green")
                else:
                    self.weigh_weight_value_1_l.SetBackgroundColour("Red")
                self.weigh_weight_index_2_l.SetLabel("第二层")
                self.weigh_weight_value_2_l.SetLabel(str(self.weigh_weight_dict["010201"]))
                if self.weigh_weight_online["010201"]:
                    self.weigh_weight_value_2_l.SetBackgroundColour("Green")
                else:
                    self.weigh_weight_value_2_l.SetBackgroundColour("Red")
                self.weigh_weight_index_3_l.SetLabel("第三层")
                self.weigh_weight_value_3_l.SetLabel(str(self.weigh_weight_dict["010301"]))
                if self.weigh_weight_online["010301"]:
                    self.weigh_weight_value_3_l.SetBackgroundColour("Green")
                else:
                    self.weigh_weight_value_3_l.SetBackgroundColour("Red")
                self.weigh_weight_index_4_l.SetLabel("第四层")
                self.weigh_weight_value_4_l.SetLabel(str(self.weigh_weight_dict["010401"]))
                if self.weigh_weight_online["010401"]:
                    self.weigh_weight_value_4_l.SetBackgroundColour("Green")
                else:
                    self.weigh_weight_value_4_l.SetBackgroundColour("Red")
                self.get_weigh_weight_box_actural_h_1.Add(self.weigh_weight_index_1_l, 1, wx.ALL | wx.EXPAND, 2)
                self.get_weigh_weight_box_actural_h_1.Add(self.weigh_weight_value_1_l, 1, wx.ALL | wx.EXPAND, 2)
                self.get_weigh_weight_box_actural_h_2.Add(self.weigh_weight_index_2_l, 1, wx.ALL | wx.EXPAND, 2)
                self.get_weigh_weight_box_actural_h_2.Add(self.weigh_weight_value_2_l, 1, wx.ALL | wx.EXPAND, 2)
                self.get_weigh_weight_box_actural_h_3.Add(self.weigh_weight_index_3_l, 1, wx.ALL | wx.EXPAND, 2)
                self.get_weigh_weight_box_actural_h_3.Add(self.weigh_weight_value_3_l, 1, wx.ALL | wx.EXPAND, 2)
                self.get_weigh_weight_box_actural_h_4.Add(self.weigh_weight_index_4_l, 1, wx.ALL | wx.EXPAND, 2)
                self.get_weigh_weight_box_actural_h_4.Add(self.weigh_weight_value_4_l, 1, wx.ALL | wx.EXPAND, 2)
                self.get_weigh_weight_box_size.Add(self.get_weigh_weight_box_actural_h_1, 1, wx.ALL | wx.EXPAND, 2)
                self.get_weigh_weight_box_size.Add(self.get_weigh_weight_box_actural_h_2, 1, wx.ALL | wx.EXPAND, 2)
                self.get_weigh_weight_box_size.Add(self.get_weigh_weight_box_actural_h_3, 1, wx.ALL | wx.EXPAND, 2)
                self.get_weigh_weight_box_size.Add(self.get_weigh_weight_box_actural_h_4, 1, wx.ALL | wx.EXPAND, 2)
                self.weigh_panel.SetSizer(self.weigh_box_v)
                self.weigh_panel.Layout()
                self.weigh_panel.Fit()

            elif select_devid_type == "5100":
                self.weigh_weight_index_1_l.SetLabel("第一层")
                self.weigh_weight_value_1_l.SetLabel(str(self.weigh_weight_dict["010101"]))
                if self.weigh_weight_online["010101"]:
                    self.weigh_weight_value_1_l.SetBackgroundColour("Green")
                else:
                    self.weigh_weight_value_1_l.SetBackgroundColour("Red")
                self.weigh_weight_index_2_l.SetLabel("第二层")
                self.weigh_weight_value_2_l.SetLabel(str(self.weigh_weight_dict["010201"]))
                if self.weigh_weight_online["010201"]:
                    self.weigh_weight_value_2_l.SetBackgroundColour("Green")
                else:
                    self.weigh_weight_value_2_l.SetBackgroundColour("Red")
                self.weigh_weight_index_3_l.SetLabel("第三层")
                self.weigh_weight_value_3_l.SetLabel(str(self.weigh_weight_dict["010301"]))
                if self.weigh_weight_online["010301"]:
                    self.weigh_weight_value_3_l.SetBackgroundColour("Green")
                else:
                    self.weigh_weight_value_3_l.SetBackgroundColour("Red")
                self.weigh_weight_index_4_l.SetLabel("第四层")
                self.weigh_weight_value_4_l.SetLabel(str(self.weigh_weight_dict["010401"]))
                if self.weigh_weight_online["010401"]:
                    self.weigh_weight_value_4_l.SetBackgroundColour("Green")
                else:
                    self.weigh_weight_value_4_l.SetBackgroundColour("Red")
                self.weigh_weight_index_5_l.SetLabel("第五层")
                self.weigh_weight_value_5_l.SetLabel(str(self.weigh_weight_dict["010501"]))
                if self.weigh_weight_online["010501"]:
                    self.weigh_weight_value_5_l.SetBackgroundColour("Green")
                else:
                    self.weigh_weight_value_5_l.SetBackgroundColour("Red")
                self.get_weigh_weight_box_actural_h_1.Add(self.weigh_weight_index_1_l, 1, wx.ALL | wx.EXPAND, 2)
                self.get_weigh_weight_box_actural_h_1.Add(self.weigh_weight_value_1_l, 1, wx.ALL | wx.EXPAND, 2)
                self.get_weigh_weight_box_actural_h_2.Add(self.weigh_weight_index_2_l, 1, wx.ALL | wx.EXPAND, 2)
                self.get_weigh_weight_box_actural_h_2.Add(self.weigh_weight_value_2_l, 1, wx.ALL | wx.EXPAND, 2)
                self.get_weigh_weight_box_actural_h_3.Add(self.weigh_weight_index_3_l, 1, wx.ALL | wx.EXPAND, 2)
                self.get_weigh_weight_box_actural_h_3.Add(self.weigh_weight_value_3_l, 1, wx.ALL | wx.EXPAND, 2)
                self.get_weigh_weight_box_actural_h_4.Add(self.weigh_weight_index_4_l, 1, wx.ALL | wx.EXPAND, 2)
                self.get_weigh_weight_box_actural_h_4.Add(self.weigh_weight_value_4_l, 1, wx.ALL | wx.EXPAND, 2)
                self.get_weigh_weight_box_actural_h_5.Add(self.weigh_weight_index_5_l, 1, wx.ALL | wx.EXPAND, 2)
                self.get_weigh_weight_box_actural_h_5.Add(self.weigh_weight_value_5_l, 1, wx.ALL | wx.EXPAND, 2)
                self.get_weigh_weight_box_size.Add(self.get_weigh_weight_box_actural_h_1, 1, wx.ALL | wx.EXPAND, 2)
                self.get_weigh_weight_box_size.Add(self.get_weigh_weight_box_actural_h_2, 1, wx.ALL | wx.EXPAND, 2)
                self.get_weigh_weight_box_size.Add(self.get_weigh_weight_box_actural_h_3, 1, wx.ALL | wx.EXPAND, 2)
                self.get_weigh_weight_box_size.Add(self.get_weigh_weight_box_actural_h_4, 1, wx.ALL | wx.EXPAND, 2)
                self.get_weigh_weight_box_size.Add(self.get_weigh_weight_box_actural_h_5, 1, wx.ALL | wx.EXPAND, 2)
                self.weigh_panel.SetSizer(self.weigh_box_v)
                self.weigh_panel.Layout()
                self.weigh_panel.Fit()

            elif select_devid_type == "5200" or select_devid_type == "其他类型":
                self.weigh_weight_index_1_l.SetLabel("第一层左")
                self.weigh_weight_value_1_l.SetLabel(str(self.weigh_weight_dict["010101"]))
                if self.weigh_weight_online["010101"]:
                    self.weigh_weight_value_1_l.SetBackgroundColour("Green")
                else:
                    self.weigh_weight_value_1_l.SetBackgroundColour("Red")
                self.weigh_weight_index_1_r.SetLabel("第一左右")
                self.weigh_weight_value_1_r.SetLabel(str(self.weigh_weight_dict["010102"]))
                if self.weigh_weight_online["010102"]:
                    self.weigh_weight_value_1_r.SetBackgroundColour("Green")
                else:
                    self.weigh_weight_value_1_r.SetBackgroundColour("Red")
                self.weigh_weight_index_2_l.SetLabel("第二层左")
                self.weigh_weight_value_2_l.SetLabel(str(self.weigh_weight_dict["010201"]))
                if self.weigh_weight_online["010201"]:
                    self.weigh_weight_value_2_l.SetBackgroundColour("Green")
                else:
                    self.weigh_weight_value_2_l.SetBackgroundColour("Red")
                self.weigh_weight_index_2_r.SetLabel("第二层右")
                self.weigh_weight_value_2_r.SetLabel(str(self.weigh_weight_dict["010202"]))
                if self.weigh_weight_online["010202"]:
                    self.weigh_weight_value_2_r.SetBackgroundColour("Green")
                else:
                    self.weigh_weight_value_2_r.SetBackgroundColour("Red")
                self.weigh_weight_index_3_l.SetLabel("第三层左")
                self.weigh_weight_value_3_l.SetLabel(str(self.weigh_weight_dict["010301"]))
                if self.weigh_weight_online["010301"]:
                    self.weigh_weight_value_3_l.SetBackgroundColour("Green")
                else:
                    self.weigh_weight_value_3_l.SetBackgroundColour("Red")
                self.weigh_weight_index_3_r.SetLabel("第三层右")
                self.weigh_weight_value_3_r.SetLabel(str(self.weigh_weight_dict["010302"]))
                if self.weigh_weight_online["010302"]:
                    self.weigh_weight_value_3_r.SetBackgroundColour("Green")
                else:
                    self.weigh_weight_value_3_r.SetBackgroundColour("Red")
                self.weigh_weight_index_4_l.SetLabel("第四层左")
                self.weigh_weight_value_4_l.SetLabel(str(self.weigh_weight_dict["010401"]))
                if self.weigh_weight_online["010401"]:
                    self.weigh_weight_value_4_l.SetBackgroundColour("Green")
                else:
                    self.weigh_weight_value_4_l.SetBackgroundColour("Red")
                self.weigh_weight_index_4_r.SetLabel("第四层右")
                self.weigh_weight_value_4_r.SetLabel(str(self.weigh_weight_dict["010402"]))
                if self.weigh_weight_online["010402"]:
                    self.weigh_weight_value_4_r.SetBackgroundColour("Green")
                else:
                    self.weigh_weight_value_4_r.SetBackgroundColour("Red")
                self.weigh_weight_index_5_l.SetLabel("第五层左")
                self.weigh_weight_value_5_l.SetLabel(str(self.weigh_weight_dict["010501"]))
                if self.weigh_weight_online["010501"]:
                    self.weigh_weight_value_5_l.SetBackgroundColour("Green")
                else:
                    self.weigh_weight_value_5_l.SetBackgroundColour("Red")
                self.weigh_weight_index_5_r.SetLabel("第五层右")
                self.weigh_weight_value_5_r.SetLabel(str(self.weigh_weight_dict["010502"]))
                if self.weigh_weight_online["010502"]:
                    self.weigh_weight_value_5_r.SetBackgroundColour("Green")
                else:
                    self.weigh_weight_value_5_r.SetBackgroundColour("Red")
                self.get_weigh_weight_box_actural_h_1.Add(self.weigh_weight_index_1_l, 1, wx.ALL | wx.EXPAND, 2)
                self.get_weigh_weight_box_actural_h_1.Add(self.weigh_weight_value_1_l, 1, wx.ALL | wx.EXPAND, 2)
                self.get_weigh_weight_box_actural_h_1.Add(self.weigh_weight_index_1_r, 1, wx.ALL | wx.EXPAND, 2)
                self.get_weigh_weight_box_actural_h_1.Add(self.weigh_weight_value_1_r, 1, wx.ALL | wx.EXPAND, 2)
                self.get_weigh_weight_box_actural_h_2.Add(self.weigh_weight_index_2_l, 1, wx.ALL | wx.EXPAND, 2)
                self.get_weigh_weight_box_actural_h_2.Add(self.weigh_weight_value_2_l, 1, wx.ALL | wx.EXPAND, 2)
                self.get_weigh_weight_box_actural_h_2.Add(self.weigh_weight_index_2_r, 1, wx.ALL | wx.EXPAND, 2)
                self.get_weigh_weight_box_actural_h_2.Add(self.weigh_weight_value_2_r, 1, wx.ALL | wx.EXPAND, 2)
                self.get_weigh_weight_box_actural_h_3.Add(self.weigh_weight_index_3_l, 1, wx.ALL | wx.EXPAND, 2)
                self.get_weigh_weight_box_actural_h_3.Add(self.weigh_weight_value_3_l, 1, wx.ALL | wx.EXPAND, 2)
                self.get_weigh_weight_box_actural_h_3.Add(self.weigh_weight_index_3_r, 1, wx.ALL | wx.EXPAND, 2)
                self.get_weigh_weight_box_actural_h_3.Add(self.weigh_weight_value_3_r, 1, wx.ALL | wx.EXPAND, 2)
                self.get_weigh_weight_box_actural_h_4.Add(self.weigh_weight_index_4_l, 1, wx.ALL | wx.EXPAND, 2)
                self.get_weigh_weight_box_actural_h_4.Add(self.weigh_weight_value_4_l, 1, wx.ALL | wx.EXPAND, 2)
                self.get_weigh_weight_box_actural_h_4.Add(self.weigh_weight_index_4_r, 1, wx.ALL | wx.EXPAND, 2)
                self.get_weigh_weight_box_actural_h_4.Add(self.weigh_weight_value_4_r, 1, wx.ALL | wx.EXPAND, 2)
                self.get_weigh_weight_box_actural_h_5.Add(self.weigh_weight_index_5_l, 1, wx.ALL | wx.EXPAND, 2)
                self.get_weigh_weight_box_actural_h_5.Add(self.weigh_weight_value_5_l, 1, wx.ALL | wx.EXPAND, 2)
                self.get_weigh_weight_box_actural_h_5.Add(self.weigh_weight_index_5_r, 1, wx.ALL | wx.EXPAND, 2)
                self.get_weigh_weight_box_actural_h_5.Add(self.weigh_weight_value_5_r, 1, wx.ALL | wx.EXPAND, 2)
                self.get_weigh_weight_box_size.Add(self.get_weigh_weight_box_actural_h_1, 1, wx.ALL | wx.EXPAND, 2)
                self.get_weigh_weight_box_size.Add(self.get_weigh_weight_box_actural_h_2, 1, wx.ALL | wx.EXPAND, 2)
                self.get_weigh_weight_box_size.Add(self.get_weigh_weight_box_actural_h_3, 1, wx.ALL | wx.EXPAND, 2)
                self.get_weigh_weight_box_size.Add(self.get_weigh_weight_box_actural_h_4, 1, wx.ALL | wx.EXPAND, 2)
                self.get_weigh_weight_box_size.Add(self.get_weigh_weight_box_actural_h_5, 1, wx.ALL | wx.EXPAND, 2)
                self.weigh_panel.SetSizer(self.weigh_box_v)
                self.weigh_panel.Layout()
                self.weigh_panel.Fit()

        elif msg == "weigh_stability":
            self.count_time_alive = False
            self.weigh_stability_button.Enable()
            self.goods_weight_button.Enable()
            self.weigh_back.Enable()
            self.weigh_weight_button.Enable()
            self.system_message.SetLabel("")
        elif msg=="current_weight_update":
            self.actual_goods_weight_value.SetLabel(str(self.current_weight))

    def OnClose(self, evet):
        dlg = wx.MessageDialog(None, '确定关闭工具 ?', 'Confirmation', wx.YES_NO | wx.ICON_QUESTION)
        retCode = dlg.ShowModal()
        if (retCode == wx.ID_YES):
            self.Destroy()
            self.Show(False)
            wx.Exit()
        else:
            pass

    # 提示子进程
    def operator_impact(self):
        while True:
            if self.count_time_alive:
                Cart = "running"
                wx.CallAfter(pub.sendMessage, "update", msg=Cart)
            elif not self.count_time_alive:
                break
            time.sleep(1)

    # 设置URL选择
    def DEV_URL(self, evt):
        index = evt.GetEventObject().GetSelection()
        if (index == 0):
            self.url = "http://10.4.32.114:8085/rrpc"
            self.web_login_url = "http://218.108.7.116:8500/login"
            self.web_query_dev_url = "http://218.108.7.116:8500/api/query_dev"
            self.web_Referer="http://218.108.7.116:8500/main"
        elif (index == 1):
            self.url = "http://w.vegcloud.xyz:8085/rrpc"
            self.web_login_url = "http://www.vegcloud.xyz:8500/login"
            self.web_query_dev_url = "http://www.vegcloud.xyz:8500/api/query_dev"
            self.web_Referer="http://www.vegcloud.xyz:8500/"



class toolapp(wx.App):
    def OnInit(self):
        self.frame = ToolsWindow(None, '设备操作工具')
        self.frame.Show(True)
        return True


if __name__ == "__main__":
    app = toolapp(0)
    app.MainLoop()





