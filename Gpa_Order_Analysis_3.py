import sys
import os
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
from urllib.request import urlretrieve




class ToolsWindow(wx.Frame):

    def __init__(self, parent, title):
        self.get_dev_id = ""
        self.select_url=False
        wx.Frame.__init__(self, parent, title=title, size=(1000, 700),style=wx.CAPTION | wx.CLOSE_BOX | wx.MINIMIZE_BOX|wx.RESIZE_BORDER)
        self.init_panel = wx.Panel(self, -1)
        #self.init_panel=scrolled.ScrolledPanel(self,-1)
        self.SetBackgroundColour("#8F8FBC")
        self.init_panel.SetBackgroundColour("#8F8FBC")
        self.index_login_name = wx.StaticText(self.init_panel, -1, "ERP用户名", style=wx.TE_LEFT)
        self.font_init = wx.Font(11, wx.DECORATIVE, wx.NORMAL, wx.LIGHT)
        self.index_login_name.SetFont(self.font_init)
        self.index_login_name.SetForegroundColour("Red")
        self.index_login_pw = wx.StaticText(self.init_panel, -1, "ERP密码", style=wx.TE_LEFT)
        self.index_login_pw.SetFont(self.font_init)
        self.index_login_pw.SetForegroundColour("Red")
        self.value_login_pw = wx.TextCtrl(self.init_panel, -1, "76831213", style=wx.TE_CENTER|wx.TE_PASSWORD)
        self.value_login_pw.SetFont(self.font_init)
        self.value_login_pw.SetForegroundColour("Red")
        self.index_dev_id = wx.StaticText(self.init_panel, -1, "设备ID", style=wx.TE_LEFT)
        self.index_dev_id.SetFont(self.font_init)
        self.index_dev_id.SetForegroundColour("Red")
        self.dev_id = wx.TextCtrl(self.init_panel, -1, value="", style=wx.TE_CENTER)
        self.dev_id.SetFont(self.font_init)
        self.dev_id.SetForegroundColour("Red")
        self.value_longin_name = wx.TextCtrl(self.init_panel, -1, "HZ05791", style=wx.TE_CENTER)
        self.value_longin_name.SetFont(self.font_init)
        self.value_longin_name.SetForegroundColour("Red")
        self.begin = wx.Button(self.init_panel, -1, "确定", style=wx.BU_BOTTOM)
        self.begin.SetFont(self.font_init)
        self.begin.SetForegroundColour("Blue")
        self.Bind(wx.EVT_BUTTON, self.begin_Click, self.begin)
        self.index_url = wx.StaticText(self.init_panel, -1, "设备环境", style=wx.TE_LEFT)
        self.index_url.SetFont(self.font_init)
        self.index_url.SetForegroundColour("Red")
        self.dev_url = wx.Choice(self.init_panel, choices=["测试环境", "生产环境"])
        self.dev_url.SetFont(self.font_init)
        self.dev_url.SetForegroundColour("Red")
        self.Bind(wx.EVT_CHOICE, self.DEV_URL, self.dev_url)
        self.static_box = wx.StaticBox(self.init_panel, -1, "初始配置信息", size=(980, 0), style=wx.TE_CENTER)
        self.static_box.SetForegroundColour("#EAADEA")
        self.init_box_v = wx.BoxSizer(wx.VERTICAL)
        self.dev_id_box_h = wx.BoxSizer(wx.HORIZONTAL)
        self.erp_longin_h=wx.BoxSizer(wx.HORIZONTAL)
        self.enter_h=wx.BoxSizer(wx.HORIZONTAL)
        self.dev_config_sizer = wx.StaticBoxSizer(self.static_box, wx.VERTICAL)
        self.dev_id_box_h.Add(self.index_dev_id, 1, wx.ALL | wx.EXPAND, 2)
        self.dev_id_box_h.Add(self.dev_id, 1, wx.ALL | wx.EXPAND, 2)
        self.dev_id_box_h.Add(self.index_url, 1, wx.ALL | wx.EXPAND, 2)
        self.dev_id_box_h.Add(self.dev_url, 1, wx.ALL | wx.EXPAND, 2)
        self.erp_longin_h.Add(self.index_login_name,1,wx.ALL|wx.EXPAND,2)
        self.erp_longin_h.Add(self.value_longin_name, 1, wx.ALL | wx.EXPAND, 2)
        self.erp_longin_h.Add(self.index_login_pw, 1, wx.ALL | wx.EXPAND, 2)
        self.erp_longin_h.Add(self.value_login_pw, 1, wx.ALL | wx.EXPAND, 2)
        self.enter_h.Add(self.begin, 1, wx.ALL | wx.EXPAND, 2)
        self.dev_config_sizer.Add(self.dev_id_box_h, 1, wx.ALL | wx.EXPAND, 2)
        self.dev_config_sizer.Add(self.erp_longin_h, 1, wx.ALL | wx.EXPAND, 2)
        self.dev_config_sizer.Add(self.enter_h, 1, wx.ALL | wx.EXPAND, 2)
        self.init_panel.SetSizer(self.dev_config_sizer)
        self.init_panel.Fit()
        self.operator_muen_size = self.init_panel.GetSize()
        self.operator_muen_panel = wx.Panel(self, -1, pos=(0, self.operator_muen_size[1] + 5), size=(985, 0))
        #self.operator_muen_panel=scrolled.ScrolledPanel(self, -1, pos=(0, self.operator_muen_size[1] + 5), size=(985, 650-self.operator_muen_size[1]))
        self.operator_muen_panel.SetBackgroundColour("#8F8FBC")
        self.index_trans_id = wx.StaticText(self.operator_muen_panel, -1, "交易ID", style=wx.TE_LEFT)
        self.index_trans_id.SetFont(self.font_init)
        self.index_trans_id.SetForegroundColour("Red")
        self.value_trans_id = wx.TextCtrl(self.operator_muen_panel, -1, value="", style=wx.TE_LEFT)
        self.value_trans_id.SetFont(self.font_init)
        self.value_trans_id.SetForegroundColour("Red")
        self.analysis_trans = wx.Button(self.operator_muen_panel, -1, "分析", style=wx.BU_BOTTOM)
        self.analysis_trans.SetFont(self.font_init)
        self.analysis_trans.SetForegroundColour("Red")
        self.index_devid_type = wx.ComboBox(self.operator_muen_panel, -1, value="设备类型",choices=["CM","AS"],style=wx.CB_DROPDOWN)
        self.index_devid_type.SetFont(self.font_init)
        self.index_devid_type.SetForegroundColour("Red")
        self.pic_detail_infomation=wx.Button(self.operator_muen_panel,-1,"详细信息",style=wx.BU_BOTTOM)
        self.pic_detail_infomation.SetFont(self.font_init)
        self.pic_detail_infomation.SetForegroundColour("Red")
        self.Bind(wx.EVT_BUTTON,self.goods_detail_infomation,self.pic_detail_infomation)
        self.Bind(wx.EVT_BUTTON, self.analysis_trans_operator, self.analysis_trans)
        self.static_operation = wx.StaticBox(self.operator_muen_panel, -1, "操作菜单")
        self.static_operation.SetForegroundColour("#EAADEA")
        self.static_operation_sizer = wx.StaticBoxSizer(self.static_operation, wx.VERTICAL)
        self.operator_muen_panel_Box_H = wx.BoxSizer(wx.HORIZONTAL)
        self.index_down_file=wx.StaticText(self.operator_muen_panel,-1,"下载日志保存路径",style=wx.TE_LEFT)
        self.index_down_file.SetFont(self.font_init)
        self.index_down_file.SetForegroundColour("Red")
        self.value_down_file=wx.TextCtrl(self.operator_muen_panel,-1,"D:\log",style=wx.TE_LEFT)
        self.value_down_file.SetFont(self.font_init)
        self.value_down_file.SetForegroundColour("Red")
        self.button_down_file=wx.Button(self.operator_muen_panel,-1,"下载",style=wx.BU_BOTTOM)
        self.button_down_file.SetFont(self.font_init)
        self.button_down_file.SetForegroundColour("Red")
        self.Bind(wx.EVT_BUTTON,self.down_file_process,self.button_down_file)
        self.down_file_box=wx.StaticBox(self.operator_muen_panel,-1,"下载配置")
        self.down_file_box.SetForegroundColour("#EAADEA")
        self.down_file_box_sizer=wx.StaticBoxSizer(self.down_file_box,wx.VERTICAL)
        self.down_file_box_h=wx.BoxSizer(wx.HORIZONTAL)
        self.operator_muen_panel_Box_H.Add(self.index_devid_type, 1, wx.ALL | wx.EXPAND, 2)
        self.operator_muen_panel_Box_H.Add(self.button_down_file, 1, wx.ALL | wx.EXPAND , 2)
        self.operator_muen_panel_Box_H.Add(self.analysis_trans, 1, wx.ALL | wx.EXPAND , 2)
        self.operator_muen_panel_Box_H.Add(self.pic_detail_infomation, 1, wx.ALL | wx.EXPAND, 2)
        self.static_operation_sizer.Add(self.operator_muen_panel_Box_H, 1,wx.ALL | wx.EXPAND, 2)

        self.down_file_box_h.Add(self.index_down_file,0,wx.ALL|wx.EXPAND,2)
        self.down_file_box_h.Add(self.value_down_file, 1, wx.ALL | wx.EXPAND, 2)
        self.down_file_box_h.Add(self.index_trans_id, 0, wx.ALL | wx.EXPAND, 2)
        self.down_file_box_h.Add(self.value_trans_id, 1, wx.ALL | wx.EXPAND, 2)
        self.down_file_box_sizer.Add(self.down_file_box_h,1,wx.ALL|wx.EXPAND,2)
        self.system_dlg = wx.MessageDialog(self.init_panel, "", caption="操作提示", style=wx.OK)
        self.system_dlg.SetFont(self.font_init)
        self.system_dlg.SetForegroundColour("Red")
        self.user_name_dlg = wx.TextEntryDialog(self.init_panel, "请输入用户名", "登入设备用户名")
        self.user_name_dlg.SetFont(self.font_init)
        self.user_name_dlg.SetForegroundColour("Red")
        self.pw_dlg = wx.TextEntryDialog(self.init_panel, "请输入密码", "登入设备密码",style=wx.TE_PASSWORD | wx.OK | wx.CANCEL | wx.CENTER)
        self.pw_dlg.SetFont(self.font_init)
        self.pw_dlg.SetForegroundColour("Red")
        self.font_result = wx.Font(11, wx.DECORATIVE, wx.NORMAL, wx.LIGHT)
        self.static_result_box=wx.StaticBox(self.operator_muen_panel,-1,"图像结果")
        self.static_result_box.SetForegroundColour("#EAADEA")
        self.static_result_box_sizer=wx.StaticBoxSizer(self.static_result_box,wx.VERTICAL)
        self.value_change_goods_layer_1=wx.ComboBox(self.operator_muen_panel,-1,value="第一层商品变化",choices=["","","","","","","","","","","","","","","","","","","","",""],style=wx.CB_SIMPLE)
        self.value_change_goods_layer_2 = wx.ComboBox(self.operator_muen_panel, -1, value="第二层商品变化",choices=["","","","","","","","","","","","","","","","","","","","",""],style=wx.CB_SIMPLE)
        self.value_change_goods_layer_3 = wx.ComboBox(self.operator_muen_panel, -1, value="第三层商品变化",choices=["","","","","","","","","","","","","","","","","","","","",""], style=wx.CB_SIMPLE)
        self.value_change_goods_layer_4 = wx.ComboBox(self.operator_muen_panel, -1, value="第四层商品变化",choices=["","","","","","","","","","","","","","","","","","","","",""],style=wx.CB_SIMPLE)
        self.value_change_goods_layer_1.SetForegroundColour("Red")
        self.value_change_goods_layer_2.SetForegroundColour("Red")
        self.value_change_goods_layer_3.SetForegroundColour("Red")
        self.value_change_goods_layer_4.SetForegroundColour("Red")
        self.pic_change_weight_layer_1=wx.TextCtrl(self.operator_muen_panel, -1, "", style=wx.TE_CENTER|wx.TE_READONLY)
        self.pic_change_weight_layer_1.SetFont(self.font_result)
        self.pic_change_weight_layer_1.SetForegroundColour("Red")
        self.pic_change_weight_layer_2=wx.TextCtrl(self.operator_muen_panel, -1, "", style=wx.TE_CENTER|wx.TE_READONLY)
        self.pic_change_weight_layer_2.SetFont(self.font_result)
        self.pic_change_weight_layer_2.SetForegroundColour("Red")
        self.pic_change_weight_layer_3=wx.TextCtrl(self.operator_muen_panel, -1, "", style=wx.TE_CENTER|wx.TE_READONLY)
        self.pic_change_weight_layer_3.SetFont(self.font_result)
        self.pic_change_weight_layer_3.SetForegroundColour("Red")
        self.pic_change_weight_layer_4=wx.TextCtrl(self.operator_muen_panel, -1, "", style=wx.TE_CENTER|wx.TE_READONLY)
        self.pic_change_weight_layer_4.SetFont(self.font_result)
        self.pic_change_weight_layer_4.SetForegroundColour("Red")
        self.index_change_goods_H=wx.BoxSizer(wx.HORIZONTAL)
        self.value_change_goods_H=wx.BoxSizer(wx.HORIZONTAL)
        self.pic_change_weight_H = wx.BoxSizer(wx.HORIZONTAL)
        self.value_change_goods_H.Add(self.value_change_goods_layer_1, 1, wx.ALL | wx.EXPAND, 2)
        self.value_change_goods_H.Add(self.value_change_goods_layer_2, 1, wx.ALL | wx.EXPAND, 2)
        self.value_change_goods_H.Add(self.value_change_goods_layer_3, 1, wx.ALL | wx.EXPAND, 2)
        self.value_change_goods_H.Add(self.value_change_goods_layer_4, 1, wx.ALL | wx.EXPAND, 2)
        self.pic_change_weight_H.Add(self.pic_change_weight_layer_1, 1, wx.ALL | wx.EXPAND, 2)
        self.pic_change_weight_H.Add(self.pic_change_weight_layer_2, 1, wx.ALL | wx.EXPAND, 2)
        self.pic_change_weight_H.Add(self.pic_change_weight_layer_3, 1, wx.ALL | wx.EXPAND, 2)
        self.pic_change_weight_H.Add(self.pic_change_weight_layer_4, 1, wx.ALL | wx.EXPAND, 2)
        #self.static_result_box_sizer.Add(self.index_change_goods_H, 0, wx.ALL | wx.EXPAND, 2)
        self.static_result_box_sizer.Add(self.value_change_goods_H, 1, wx.ALL | wx.EXPAND, 2)
        self.static_result_box_sizer.Add(self.pic_change_weight_H, 0, wx.ALL | wx.EXPAND, 2)
        #self.operator_muen_panel.SetSizer(self.static_result_box_sizer)
        self.static_weight_result_box=wx.StaticBox(self.operator_muen_panel,-1,"重力结果")
        self.static_weight_result_box.SetForegroundColour("#EAADEA")
        self.static_weight_result_box_sizer=wx.StaticBoxSizer(self.static_weight_result_box,wx.VERTICAL)
        self.index_change_weight_layer_1=wx.StaticText(self.operator_muen_panel,-1,"第一层重力变化",style=wx.TE_CENTER)
        self.index_change_weight_layer_1.SetFont(self.font_result)
        self.index_change_weight_layer_1.SetForegroundColour("Red")
        self.index_change_weight_layer_2 = wx.StaticText(self.operator_muen_panel, -1, "第二层重力变化", style=wx.TE_CENTER)
        self.index_change_weight_layer_2.SetFont(self.font_result)
        self.index_change_weight_layer_2.SetForegroundColour("Red")
        self.index_change_weight_layer_3 = wx.StaticText(self.operator_muen_panel, -1, "第三层重力变化", style=wx.TE_CENTER)
        self.index_change_weight_layer_3.SetFont(self.font_result)
        self.index_change_weight_layer_3.SetForegroundColour("Red")
        self.index_change_weight_layer_4 = wx.StaticText(self.operator_muen_panel, -1, "第四层重力变化", style=wx.TE_CENTER)
        self.index_change_weight_layer_4.SetFont(self.font_result)
        self.index_change_weight_layer_4.SetForegroundColour("Red")
        self.value_change_weight_layer_1=wx.TextCtrl(self.operator_muen_panel,-1,"",style=wx.TE_CENTER |wx.TE_READONLY)
        self.value_change_weight_layer_1.SetFont(self.font_result)
        self.value_change_weight_layer_1.SetForegroundColour("Red")
        self.value_change_weight_layer_2=wx.TextCtrl(self.operator_muen_panel,-1,"",style=wx.TE_CENTER|wx.TE_READONLY)
        self.value_change_weight_layer_2.SetFont(self.font_result)
        self.value_change_weight_layer_2.SetForegroundColour("Red")
        self.value_change_weight_layer_3=wx.TextCtrl(self.operator_muen_panel,-1,"",style=wx.TE_CENTER|wx.TE_READONLY)
        self.value_change_weight_layer_3.SetFont(self.font_result)
        self.value_change_weight_layer_3.SetForegroundColour("Red")
        self.value_change_weight_layer_4=wx.TextCtrl(self.operator_muen_panel,-1,"",style=wx.TE_CENTER|wx.TE_READONLY)
        self.value_change_weight_layer_4.SetFont(self.font_result)
        self.value_change_weight_layer_4.SetForegroundColour("Red")
        self.index_weight_change_h=wx.BoxSizer(wx.HORIZONTAL)
        self.value_weight_change_h = wx.BoxSizer(wx.HORIZONTAL)
        self.index_weight_change_h.Add(self.index_change_weight_layer_1,1,wx.ALL|wx.EXPAND,2)
        self.index_weight_change_h.Add(self.index_change_weight_layer_2, 1, wx.ALL | wx.EXPAND, 2)
        self.index_weight_change_h.Add(self.index_change_weight_layer_3, 1, wx.ALL | wx.EXPAND, 2)
        self.index_weight_change_h.Add(self.index_change_weight_layer_4, 1, wx.ALL | wx.EXPAND, 2)
        self.value_weight_change_h.Add(self.value_change_weight_layer_1,1,wx.ALL|wx.EXPAND,2)
        self.value_weight_change_h.Add(self.value_change_weight_layer_2,1,wx.ALL|wx.EXPAND,2)
        self.value_weight_change_h.Add(self.value_change_weight_layer_3,1,wx.ALL|wx.EXPAND,2)
        self.value_weight_change_h.Add(self.value_change_weight_layer_4,1,wx.ALL|wx.EXPAND,2)
        self.static_weight_result_box_sizer.Add(self.index_weight_change_h,1,wx.ALL|wx.EXPAND,2)
        self.static_weight_result_box_sizer.Add(self.value_weight_change_h, 1, wx.ALL | wx.EXPAND, 2)
        self.operator_box_V=wx.BoxSizer(wx.VERTICAL)
        self.operator_box_V.Add(self.down_file_box_sizer, 0, wx.ALL | wx.EXPAND, 2)
        self.operator_box_V.Add(self.static_operation_sizer,0,wx.ALL|wx.EXPAND,2)
        self.operator_box_V.Add(self.static_result_box_sizer, 1, wx.ALL | wx.EXPAND, 2)
        self.operator_box_V.Add(self.static_weight_result_box_sizer, 0, wx.ALL | wx.EXPAND, 2)
        self.operator_muen_panel.SetSizer(self.operator_box_V)
        self.operator_muen_panel.Fit()
        #self.operator_muen_panel.SetAutoLayout(1)
        #self.operator_muen_panel.SetupScrolling()
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.analysis_trans.Disable()
        self.pic_detail_infomation.Disable()
        self.button_down_file.Disable()
    # 开关门商品显示
    def goods_detail_infomation(self,evt):
        if self.index_devid_type.GetValue() == "CM":
            self.save_pic_path = self.value_down_file.GetValue().strip()
            self.save_pic_path = self.save_pic_path.rstrip("\\") + "\\" + "CM_picture"
            picture_dir_is_exist = os.path.exists(self.save_pic_path)
            try:
                if not picture_dir_is_exist:
                    os.makedirs(self.save_pic_path)
            except:
                self.system_dlg.SetMessage("创建保存图片文件夹失败！！！！")
                self.system_dlg.ShowModal()
                return
            self.open_pic_layer_1_name = self.value_trans_id.GetValue().strip() + "_open_1.jpg"
            self.open_pic_layer_2_name = self.value_trans_id.GetValue().strip() + "_open_2.jpg"
            self.open_pic_layer_3_name = self.value_trans_id.GetValue().strip() + "_open_3.jpg"
            self.open_pic_layer_4_name = self.value_trans_id.GetValue().strip() + "_open_4.jpg"
            if self.close_link_layer_1:
                self.close_pic_layer_1_name = self.value_trans_id.GetValue().strip() + "_close_1.jpg"
            else:
                self.close_pic_layer_1_name = self.value_trans_id.GetValue().strip() + "_open_1.jpg"
            if self.close_link_layer_2:
                self.close_pic_layer_2_name = self.value_trans_id.GetValue().strip() + "_close_2.jpg"
            else:
                self.close_pic_layer_2_name = self.value_trans_id.GetValue().strip() + "_open_2.jpg"
            if self.close_link_layer_3:
                self.close_pic_layer_3_name = self.value_trans_id.GetValue().strip() + "_close_3.jpg"
            else:
                self.close_pic_layer_3_name = self.value_trans_id.GetValue().strip() + "_open_3.jpg"
            if self.close_link_layer_4:
                self.close_pic_layer_4_name = self.value_trans_id.GetValue().strip() + "_close_4.jpg"
            else:
                self.close_pic_layer_4_name = self.value_trans_id.GetValue().strip() + "_open_4.jpg"
        elif self.index_devid_type.GetValue() == "AS":
            self.save_pic_path = self.value_down_file.GetValue().strip()
            self.save_pic_path = self.save_pic_path.rstrip("\\") + "\\" + "AS_picture"
            picture_dir_is_exist = os.path.exists(self.save_pic_path)
            try:
                if not picture_dir_is_exist:
                    os.makedirs(self.save_pic_path)
            except:
                self.system_dlg.SetMessage("创建保存图片文件夹失败！！！！")
                self.system_dlg.ShowModal()
                return
            self.close_pic_layer_1_name = self.value_trans_id.GetValue().strip() + "-close_010101_0.jpg"
            self.close_pic_layer_2_name = self.value_trans_id.GetValue().strip() + "-close_010201_0.jpg"
            self.close_pic_layer_3_name = self.value_trans_id.GetValue().strip() + "-close_010301_0.jpg"
            self.close_pic_layer_4_name = self.value_trans_id.GetValue().strip() + "-close_010401_0.jpg"
            self.open_pic_layer_1_name = self.value_trans_id.GetValue().strip() + "-close_010101_0.jpg"
            self.open_pic_layer_2_name = self.value_trans_id.GetValue().strip() + "-close_010201_0.jpg"
            self.open_pic_layer_3_name = self.value_trans_id.GetValue().strip() + "-close_010301_0.jpg"
            self.open_pic_layer_4_name = self.value_trans_id.GetValue().strip() + "-close_010401_0.jpg"
        self.operator_muen_panel.Hide()
        self.init_panel.Hide()
        self.pic_detail_panel = wx.ScrolledWindow(self, -1, pos=(0, 0), size=(960, 600))
        self.pic_detail_panel.SetScrollbar(1, 1, 900, 600)
        self.pic_detail_panel.SetScrollRate(10, 10)
        self.pic_detail_panel.SetBackgroundColour("#8F8FBC")
        self.font_detail = wx.Font(11, wx.DECORATIVE, wx.NORMAL, wx.LIGHT)
        open_detail_goods_layer_1 = ["" for i in range(20)]
        open_detail_goods_layer_2 = ["" for i in range(20)]
        open_detail_goods_layer_3 = ["" for i in range(20)]
        open_detail_goods_layer_4 = ["" for i in range(20)]
        close_detail_goods_layer_1 = ["" for i in range(20)]
        close_detail_goods_layer_2 = ["" for i in range(20)]
        close_detail_goods_layer_3 = ["" for i in range(20)]
        close_detail_goods_layer_4 = ["" for i in range(20)]
        WeighGoodsNumCache_Open_detail_layer_1 = ["" for i in range(20)]
        WeighGoodsNumCache_Open_detail_layer_2 = ["" for i in range(20)]
        WeighGoodsNumCache_Open_detail_layer_3 = ["" for i in range(20)]
        WeighGoodsNumCache_Open_detail_layer_4 = ["" for i in range(20)]
        WeighGoodsNumCache_Close_detail_layer_1 = ["" for i in range(20)]
        WeighGoodsNumCache_Close_detail_layer_2 = ["" for i in range(20)]
        WeighGoodsNumCache_Close_detail_layer_3 = ["" for i in range(20)]
        WeighGoodsNumCache_Close_detail_layer_4 = ["" for i in range(20)]
        if self.index_devid_type.GetValue() == "CM":
            if len(self.display_trans(self.org_open_goods_name_layer_1)):
                for i in range(len(self.display_trans(self.org_open_goods_name_layer_1))):
                    open_detail_goods_layer_1[i] = self.display_trans(self.org_open_goods_name_layer_1)[i]
            if len(self.display_trans(self.org_open_goods_name_layer_2)):
                for i in range(len(self.display_trans(self.org_open_goods_name_layer_2))):
                    open_detail_goods_layer_2[i] = self.display_trans(self.org_open_goods_name_layer_2)[i]
            if len(self.display_trans(self.org_open_goods_name_layer_3)):
                for i in range(len(self.display_trans(self.org_open_goods_name_layer_3))):
                    open_detail_goods_layer_3[i] = self.display_trans(self.org_open_goods_name_layer_3)[i]
            if len(self.display_trans(self.org_open_goods_name_layer_4)):
                for i in range(len(self.display_trans(self.org_open_goods_name_layer_4))):
                    open_detail_goods_layer_4[i] = self.display_trans(self.org_open_goods_name_layer_4)[i]
            if len(self.display_trans(self.org_close_goods_name_layer_1)):
                for i in range(len(self.display_trans(self.org_close_goods_name_layer_1))):
                    close_detail_goods_layer_1[i] = self.display_trans(self.org_close_goods_name_layer_1)[i]
            if len(self.display_trans(self.org_close_goods_name_layer_2)):
                for i in range(len(self.display_trans(self.org_close_goods_name_layer_2))):
                    close_detail_goods_layer_2[i] = self.display_trans(self.org_close_goods_name_layer_2)[i]
            if len(self.display_trans(self.org_close_goods_name_layer_3)):
                for i in range(len(self.display_trans(self.org_close_goods_name_layer_3))):
                    close_detail_goods_layer_3[i] = self.display_trans(self.org_close_goods_name_layer_3)[i]
            if len(self.display_trans(self.org_close_goods_name_layer_4)):
                for i in range(len(self.display_trans(self.org_close_goods_name_layer_4))):
                    close_detail_goods_layer_4[i] = self.display_trans(self.org_close_goods_name_layer_4)[i]
        elif self.index_devid_type.GetValue() == "AS":
            if len(self.org_open_goods_name_layer_1):
                for i in range(len(self.org_open_goods_name_layer_1)):
                    open_detail_goods_layer_1[i] = self.org_open_goods_name_layer_1[i]["goodsname"] + ":" + \
                                                   str(self.org_open_goods_name_layer_1[i]["goodsnum"])
            if len(self.org_open_goods_name_layer_2):
                for i in range(len(self.org_open_goods_name_layer_2)):
                    open_detail_goods_layer_2[i] = self.org_open_goods_name_layer_2[i]["goodsname"] + ":" + \
                                                   str(self.org_open_goods_name_layer_2[i]["goodsnum"])
            if len(self.org_open_goods_name_layer_3):
                for i in range(len(self.org_open_goods_name_layer_3)):
                    open_detail_goods_layer_3[i] = self.org_open_goods_name_layer_3[i]["goodsname"] + ":" + \
                                                   str(self.org_open_goods_name_layer_3[i]["goodsnum"])
            if len(self.org_open_goods_name_layer_4):
                for i in range(len(self.org_open_goods_name_layer_4)):
                    open_detail_goods_layer_4[i] = self.org_open_goods_name_layer_4[i]["goodsname"] + ":" + \
                                                   str(self.org_open_goods_name_layer_4[i]["goodsnum"])
            if len(self.org_close_goods_name_layer_1):
                for i in range(len(self.org_close_goods_name_layer_1)):
                    close_detail_goods_layer_1[i] = self.org_close_goods_name_layer_1[i]["goodsname"] + ":" + \
                                                    str(self.org_close_goods_name_layer_1[i]["goodsnum"])
            if len(self.org_close_goods_name_layer_2):
                for i in range(len(self.org_close_goods_name_layer_2)):
                    close_detail_goods_layer_2[i] = self.org_close_goods_name_layer_2[i]["goodsname"] + ":" + \
                                                    str(self.org_close_goods_name_layer_2[i]["goodsnum"])
            if len(self.org_close_goods_name_layer_3):
                for i in range(len(self.org_close_goods_name_layer_3)):
                    close_detail_goods_layer_3[i] = self.org_close_goods_name_layer_3[i]["goodsname"] + ":" + \
                                                    str(self.org_close_goods_name_layer_3[i]["goodsnum"])
            if len(self.org_close_goods_name_layer_4):
                for i in range(len(self.org_close_goods_name_layer_4)):
                    close_detail_goods_layer_4[i] = self.org_close_goods_name_layer_4[i]["goodsname"] + ":" + \
                                                    str(self.org_close_goods_name_layer_4[i]["goodsnum"])
        if len(self.WeighGoodsNumCache_Open_layer_1):
            for i in range(len(self.WeighGoodsNumCache_Open_layer_1)):
                WeighGoodsNumCache_Open_detail_layer_1[i] = self.WeighGoodsNumCache_Open_layer_1[i]["name"] + ":" + str(
                    self.WeighGoodsNumCache_Open_layer_1[i]["num"])
        if len(self.WeighGoodsNumCache_Open_layer_2):
            for i in range(len(self.WeighGoodsNumCache_Open_layer_2)):
                WeighGoodsNumCache_Open_detail_layer_2[i] = self.WeighGoodsNumCache_Open_layer_2[i]["name"] + ":" + str(
                    self.WeighGoodsNumCache_Open_layer_2[i]["num"])
        if len(self.WeighGoodsNumCache_Open_layer_3):
            for i in range(len(self.WeighGoodsNumCache_Open_layer_3)):
                WeighGoodsNumCache_Open_detail_layer_3[i] = self.WeighGoodsNumCache_Open_layer_3[i]["name"] + ":" + str(
                    self.WeighGoodsNumCache_Open_layer_3[i]["num"])
        if len(self.WeighGoodsNumCache_Open_layer_4):
            for i in range(len(self.WeighGoodsNumCache_Open_layer_4)):
                WeighGoodsNumCache_Open_detail_layer_4[i] = self.WeighGoodsNumCache_Open_layer_4[i]["name"] + ":" + str(
                    self.WeighGoodsNumCache_Open_layer_4[i]["num"])
        if len(self.WeighGoodsNumCache_Close_layer_1):
            for i in range(len(self.WeighGoodsNumCache_Close_layer_1)):
                WeighGoodsNumCache_Close_detail_layer_1[i] = self.WeighGoodsNumCache_Close_layer_1[i][
                                                                 "name"] + ":" + str(
                    self.WeighGoodsNumCache_Close_layer_1[i]["num"])
        if len(self.WeighGoodsNumCache_Close_layer_2):
            for i in range(len(self.WeighGoodsNumCache_Close_layer_2)):
                WeighGoodsNumCache_Close_detail_layer_2[i] = self.WeighGoodsNumCache_Close_layer_2[i][
                                                                 "name"] + ":" + str(
                    self.WeighGoodsNumCache_Close_layer_2[i]["num"])
        if len(self.WeighGoodsNumCache_Close_layer_3):
            for i in range(len(self.WeighGoodsNumCache_Close_layer_3)):
                WeighGoodsNumCache_Close_detail_layer_3[i] = self.WeighGoodsNumCache_Close_layer_3[i][
                                                                 "name"] + ":" + str(
                    self.WeighGoodsNumCache_Close_layer_3[i]["num"])
        if len(self.WeighGoodsNumCache_Close_layer_4):
            for i in range(len(self.WeighGoodsNumCache_Close_layer_4)):
                WeighGoodsNumCache_Close_detail_layer_4[i] = self.WeighGoodsNumCache_Close_layer_4[i][
                                                                 "name"] + ":" + str(
                    self.WeighGoodsNumCache_Close_layer_4[i]["num"])
        self.vaule_goods_cache_open_layer_1 = wx.ComboBox(self.pic_detail_panel, -1, value="第一层开门Cache",choices=WeighGoodsNumCache_Open_detail_layer_1,style=wx.CB_SIMPLE)
        self.vaule_goods_cache_open_layer_1.SetFont(self.font_detail)
        self.vaule_goods_cache_open_layer_1.SetForegroundColour("Red")
        self.vaule_goods_cache_open_layer_2 = wx.ComboBox(self.pic_detail_panel, -1, value="第二层开门Cache",choices=WeighGoodsNumCache_Open_detail_layer_2,style=wx.CB_SIMPLE)
        self.vaule_goods_cache_open_layer_2.SetFont(self.font_detail)
        self.vaule_goods_cache_open_layer_2.SetForegroundColour("Red")
        self.vaule_goods_cache_open_layer_3 = wx.ComboBox(self.pic_detail_panel, -1, value="第三层开门Cache",choices=WeighGoodsNumCache_Open_detail_layer_3,style=wx.CB_SIMPLE)
        self.vaule_goods_cache_open_layer_3.SetFont(self.font_detail)
        self.vaule_goods_cache_open_layer_3.SetForegroundColour("Red")
        self.vaule_goods_cache_open_layer_4 = wx.ComboBox(self.pic_detail_panel, -1, value="第四层开门Cache",choices=WeighGoodsNumCache_Open_detail_layer_4,style=wx.CB_SIMPLE)
        self.vaule_goods_cache_open_layer_4.SetFont(self.font_detail)
        self.vaule_goods_cache_open_layer_4.SetForegroundColour("Red")
        self.vaule_goods_cache_close_layer_1 = wx.ComboBox(self.pic_detail_panel, -1, value="第一层关门Cache",choices=WeighGoodsNumCache_Close_detail_layer_1,style=wx.CB_SIMPLE)
        self.vaule_goods_cache_close_layer_1.SetFont(self.font_detail)
        self.vaule_goods_cache_close_layer_1.SetForegroundColour("Red")
        self.vaule_goods_cache_close_layer_2 = wx.ComboBox(self.pic_detail_panel, -1, value="第二层关门Cache",choices=WeighGoodsNumCache_Close_detail_layer_2,style=wx.CB_SIMPLE)
        self.vaule_goods_cache_close_layer_2.SetFont(self.font_detail)
        self.vaule_goods_cache_close_layer_2.SetForegroundColour("Red")
        self.vaule_goods_cache_close_layer_3 = wx.ComboBox(self.pic_detail_panel, -1, value="第三层关门Cache",choices=WeighGoodsNumCache_Close_detail_layer_3,style=wx.CB_SIMPLE)
        self.vaule_goods_cache_close_layer_3.SetFont(self.font_detail)
        self.vaule_goods_cache_close_layer_3.SetForegroundColour("Red")
        self.vaule_goods_cache_close_layer_4 = wx.ComboBox(self.pic_detail_panel, -1, value="第四层关门Cache",choices=WeighGoodsNumCache_Close_detail_layer_4,style=wx.CB_SIMPLE)
        self.vaule_goods_cache_close_layer_4.SetFont(self.font_detail)
        self.vaule_goods_cache_close_layer_4.SetForegroundColour("Red")
        self.value_open_goods_layer_1 = wx.ComboBox(self.pic_detail_panel, -1, value="第一层开门",choices=open_detail_goods_layer_1, style=wx.CB_SIMPLE)
        self.value_open_goods_layer_1.SetFont(self.font_detail)
        self.value_open_goods_layer_1.SetForegroundColour("Red")
        self.value_open_goods_layer_2 = wx.ComboBox(self.pic_detail_panel, -1, value="第二层开门",choices=open_detail_goods_layer_2,style=wx.CB_SIMPLE)
        self.value_open_goods_layer_2.SetFont(self.font_detail)
        self.value_open_goods_layer_2.SetForegroundColour("Red")
        self.value_open_goods_layer_3 = wx.ComboBox(self.pic_detail_panel, -1, value="第三层开门",choices=open_detail_goods_layer_3, style=wx.CB_SIMPLE)
        self.value_open_goods_layer_3.SetFont(self.font_detail)
        self.value_open_goods_layer_3.SetForegroundColour("Red")
        self.value_open_goods_layer_4 = wx.ComboBox(self.pic_detail_panel, -1, value="第四层开门",choices=open_detail_goods_layer_4, style=wx.CB_SIMPLE)
        self.value_open_goods_layer_4.SetFont(self.font_detail)
        self.value_open_goods_layer_4.SetForegroundColour("Red")
        self.value_close_goods_layer_1 = wx.ComboBox(self.pic_detail_panel, -1, value="第一层关门",choices=close_detail_goods_layer_1, style=wx.CB_SIMPLE)
        self.value_close_goods_layer_1.SetFont(self.font_detail)
        self.value_close_goods_layer_1.SetForegroundColour("Red")
        self.value_close_goods_layer_2 = wx.ComboBox(self.pic_detail_panel, -1, value="第二层关门",choices=close_detail_goods_layer_2, style=wx.CB_SIMPLE)
        self.value_close_goods_layer_2.SetFont(self.font_detail)
        self.value_close_goods_layer_2.SetForegroundColour("Red")
        self.value_close_goods_layer_3 = wx.ComboBox(self.pic_detail_panel, -1, value="第三层关门",choices=close_detail_goods_layer_3, style=wx.CB_SIMPLE)
        self.value_close_goods_layer_3.SetFont(self.font_detail)
        self.value_close_goods_layer_3.SetForegroundColour("Red")
        self.value_close_goods_layer_4 = wx.ComboBox(self.pic_detail_panel, -1, value="第四层关门",choices=close_detail_goods_layer_4, style=wx.CB_SIMPLE)
        self.value_close_goods_layer_4.SetFont(self.font_detail)
        self.value_close_goods_layer_4.SetForegroundColour("Red")
        # 开门识别显示
        self.open_static_box = wx.StaticBox(self.pic_detail_panel, -1, "开门识别")
        self.open_static_box.SetForegroundColour("#EAADEA")
        self.open_static_box_sizer = wx.StaticBoxSizer(self.open_static_box, wx.VERTICAL)
        self.value_open_box = wx.BoxSizer(wx.HORIZONTAL)
        self.value_open_box.Add(self.value_open_goods_layer_1, 1, wx.ALL | wx.EXPAND, 2)
        self.value_open_box.Add(self.value_open_goods_layer_2, 1, wx.ALL | wx.EXPAND, 2)
        self.value_open_box.Add(self.value_open_goods_layer_3, 1, wx.ALL | wx.EXPAND, 2)
        self.value_open_box.Add(self.value_open_goods_layer_4, 1, wx.ALL | wx.EXPAND, 2)
        self.open_static_box_sizer.Add(self.value_open_box, 1, wx.ALL | wx.EXPAND, 2)
        # 关门识别显示
        self.close_static_box = wx.StaticBox(self.pic_detail_panel, -1, "关门识别")
        self.close_static_box.SetForegroundColour("#EAADEA")
        self.close_static_box_sizer = wx.StaticBoxSizer(self.close_static_box, wx.VERTICAL)
        self.value_close_box = wx.BoxSizer(wx.HORIZONTAL)
        self.value_close_box.Add(self.value_close_goods_layer_1, 1, wx.ALL | wx.EXPAND, 2)
        self.value_close_box.Add(self.value_close_goods_layer_2, 1, wx.ALL | wx.EXPAND, 2)
        self.value_close_box.Add(self.value_close_goods_layer_3, 1, wx.ALL | wx.EXPAND, 2)
        self.value_close_box.Add(self.value_close_goods_layer_4, 1, wx.ALL | wx.EXPAND, 2)
        self.close_static_box_sizer.Add(self.value_close_box, 1, wx.ALL | wx.EXPAND, 2)
        # 开门cache
        self.value_cache_open_box = wx.StaticBox(self.pic_detail_panel, -1, "开门cache")
        self.value_cache_open_box_sizer = wx.StaticBoxSizer(self.value_cache_open_box, wx.VERTICAL)
        self.display_cache_open_box = wx.BoxSizer(wx.HORIZONTAL)
        self.display_cache_open_box.Add(self.vaule_goods_cache_open_layer_1, 1, wx.ALL | wx.EXPAND, 2)
        self.display_cache_open_box.Add(self.vaule_goods_cache_open_layer_2, 1, wx.ALL | wx.EXPAND, 2)
        self.display_cache_open_box.Add(self.vaule_goods_cache_open_layer_3, 1, wx.ALL | wx.EXPAND, 2)
        self.display_cache_open_box.Add(self.vaule_goods_cache_open_layer_4, 1, wx.ALL | wx.EXPAND, 2)
        self.value_cache_open_box_sizer.Add(self.display_cache_open_box, 1, wx.ALL |wx.EXPAND, 2)
        # 关门cache
        self.value_cache_close_box = wx.StaticBox(self.pic_detail_panel, -1, "关门cache")
        self.value_cache_close_box_sizer = wx.StaticBoxSizer(self.value_cache_close_box, wx.VERTICAL)
        self.display_cache_close_box = wx.BoxSizer(wx.HORIZONTAL)
        self.display_cache_close_box.Add(self.vaule_goods_cache_close_layer_1, 1, wx.ALL | wx.EXPAND, 2)
        self.display_cache_close_box.Add(self.vaule_goods_cache_close_layer_2, 1, wx.ALL | wx.EXPAND, 2)
        self.display_cache_close_box.Add(self.vaule_goods_cache_close_layer_3, 1, wx.ALL | wx.EXPAND, 2)
        self.display_cache_close_box.Add(self.vaule_goods_cache_close_layer_4, 1, wx.ALL | wx.EXPAND, 2)
        self.value_cache_close_box_sizer.Add(self.display_cache_close_box, 1, wx.ALL | wx.EXPAND, 2)
        # 图片显示
        self.down_pic_button = wx.Button(self.pic_detail_panel, -1, "下载图片")
        self.Bind(wx.EVT_BUTTON, self.pic_download, self.down_pic_button)
        self.pic_display_button = wx.Button(self.pic_detail_panel, -1, "显示图片")
        self.Bind(wx.EVT_BUTTON, self.display_pic, self.pic_display_button)
        self.pic_url_box = wx.StaticBox(self.pic_detail_panel, -1, "图片操作")
        self.pic_url_box_sizer = wx.StaticBoxSizer(self.pic_url_box, wx.VERTICAL)
        self.pic_url_box_H = wx.BoxSizer(wx.HORIZONTAL)
        self.pic_url_box_H.Add(self.down_pic_button, 1, wx.ALL | wx.EXPAND, 2)
        self.pic_url_box_H.Add(self.pic_display_button, 1, wx.ALL | wx.EXPAND, 2)
        self.pic_url_box_sizer.Add(self.pic_url_box_H, 1, wx.ALL | wx.EXPAND, 2)
        # 返回主页
        self.back_static_box = wx.StaticBox(self.pic_detail_panel, -1, "返回主页")
        self.back_static_box_sizer = wx.StaticBoxSizer(self.back_static_box, wx.VERTICAL)
        self.back_operater = wx.Button(self.pic_detail_panel, -1, "返回主页", style=wx.BU_BOTTOM)
        self.Bind(wx.EVT_BUTTON, self.back, self.back_operater)
        self.back_static_box_H = wx.BoxSizer(wx.HORIZONTAL)
        self.back_static_box_H.Add(self.back_operater, 1, wx.ALL | wx.EXPAND, 2)
        self.back_static_box_sizer.Add(self.back_static_box_H, 1, wx.ALL | wx.EXPAND, 2)
        self.detail_box_v = wx.BoxSizer(wx.VERTICAL)
        self.detail_box_v.Add(self.open_static_box_sizer, 1, wx.ALL | wx.EXPAND, 2)
        self.detail_box_v.Add(self.close_static_box_sizer, 1, wx.ALL | wx.EXPAND, 2)
        self.detail_box_v.Add(self.value_cache_open_box_sizer, 1, wx.ALL | wx.EXPAND, 2)
        self.detail_box_v.Add(self.value_cache_close_box_sizer, 1, wx.ALL | wx.EXPAND, 2)
        self.detail_box_v.Add(self.pic_url_box_sizer, 0, wx.ALL | wx.EXPAND, 2)
        self.detail_box_v.Add(self.back_static_box_sizer, 0, wx.ALL | wx.EXPAND, 2)
        self.pic_detail_panel.SetSizer(self.detail_box_v)
        self.pic_detail_panel.Layout()
        self.pic_detail_panel.Fit()
    # CM云端图片下载
    def pic_download(self,evt):
        if self.index_devid_type.GetValue()=="CM":
            self.down_load_pic_T = threading.Thread(target=self.pic_download_process)
            self.down_load_pic_T.start()
            self.pic_display_button.Disable()
            self.down_pic_button.Disable()
        elif self.index_devid_type.GetValue()=="AS":
            self.pic_display_button.Disable()
            self.down_load_pic_T = threading.Thread(target=self.down_load_as_pic)
            self.down_load_pic_T.start()
            self.down_pic_button.Disable()
    # AS设备本地图片下载
    def down_load_as_pic(self):
        dev_id = self.dev_id.GetValue()
        if len(dev_id) == 5:
            port_id = int(dev_id)
        else:
            port_id = "2" + self.dev_id.GetValue()
        hostid = "m.vegcloud.tech"
        sshid = int(port_id)
        name = "linaro"
        pwd = "Ustaff201"
        for i in range(1,5):
            ssh_repeat = 0
            while True:
                try:
                    myclient = paramiko.Transport((hostid, sshid))
                    # myclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    myclient.connect(username=name, password=pwd)
                    sftp = paramiko.SFTPClient.from_transport(myclient)
                    self.AS_picture_remote_layer = '/vbg/root/weighcv-as/image/' + self.value_trans_id.GetValue().strip() + "-close_010" + str(i) + "01_0.jpg"
                    self.AS_picture_local = self.save_pic_path.replace("\\", "/") + "/" + self.value_trans_id.GetValue().strip() + "-close_010" + str(i) + "01_0.jpg"
                    sftp.get(self.AS_picture_remote_layer, self.AS_picture_local)
                except:
                    ssh_repeat += 1
                    if ssh_repeat > 5:
                        self.system_dlg.SetMessage("下载第"+str(i)+"层图片失败！！")
                        self.system_dlg.ShowModal()
                        myclient.close()
                        self.down_pic_button.Enable()
                        return
                    time.sleep(10)
                else:
                    myclient.close()
                    break
        self.pic_display_button.Enable()
        self.down_pic_button.Enable()
        self.system_dlg.SetMessage("下载图片完成！！")
        self.system_dlg.ShowModal()
    # CM云端图片下载子进程
    def pic_download_process(self):
        if self.index_devid_type.GetValue()=="CM":
            if self.open_link_layer_1:
                try:
                    urlretrieve(self.open_link_layer_1, self.save_pic_path + "\\"+ self.open_pic_layer_1_name)
                except:
                    self.system_dlg.SetMessage("下载第一层开门图片失败！！")
                    self.system_dlg.ShowModal()
                    self.down_pic_button.Enable()
                    return
            if self.open_link_layer_2:
                try:
                    urlretrieve(self.open_link_layer_2, self.save_pic_path + "\\"+ self.open_pic_layer_2_name)
                except:
                    self.system_dlg.SetMessage("下载第二层开门图片失败！！")
                    self.system_dlg.ShowModal()
                    self.down_pic_button.Enable()
                    return
            if self.open_link_layer_3:
                try:
                    urlretrieve(self.open_link_layer_3, self.save_pic_path + "\\"+ self.open_pic_layer_3_name)
                except:
                    self.system_dlg.SetMessage("下载第三层开门图片失败！！")
                    self.system_dlg.ShowModal()
                    self.down_pic_button.Enable()
                    return
            if self.open_link_layer_4:
                try:
                    urlretrieve(self.open_link_layer_4, self.save_pic_path + "\\"+ self.open_pic_layer_4_name)
                except:
                    self.system_dlg.SetMessage("下载第四层开门图片失败！！")
                    self.system_dlg.ShowModal()
                    self.down_pic_button.Enable()
                    return
            if self.close_link_layer_1:
                try:
                    urlretrieve(self.close_link_layer_1, self.save_pic_path + "\\"+ self.close_pic_layer_1_name)
                except:
                    self.system_dlg.SetMessage("下载第一层关门图片失败！！")
                    self.system_dlg.ShowModal()
                    self.down_pic_button.Enable()
                    return
            if self.close_link_layer_2:
                try:
                    urlretrieve(self.close_link_layer_2, self.save_pic_path + "\\"+ self.close_pic_layer_2_name)
                except:
                    self.system_dlg.SetMessage("下载第二层关门图片失败！！")
                    self.system_dlg.ShowModal()
                    self.down_pic_button.Enable()
                    return
            if self.close_link_layer_3:
                try:
                    urlretrieve(self.close_link_layer_3, self.save_pic_path + "\\"+ self.close_pic_layer_3_name)
                except:
                    self.system_dlg.SetMessage("下载第三层关门图片失败！！")
                    self.system_dlg.ShowModal()
                    self.down_pic_button.Enable()
                    return
            if self.close_link_layer_4:
                try:
                    urlretrieve(self.close_link_layer_4, self.save_pic_path + "\\"+ self.close_pic_layer_4_name)
                except:
                    self.system_dlg.SetMessage("下载第四层关门图片失败！！")
                    self.system_dlg.ShowModal()
                    self.down_pic_button.Enable()
                    return
            self.pic_display_button.Enable()
            self.down_pic_button.Enable()
            self.system_dlg.SetMessage("下载完成！！")
            self.system_dlg.ShowModal()
    # 图片显示
    def display_pic(self,evt):
        self.layer_1_pic_open=self.save_pic_path + "\\" + self.open_pic_layer_1_name
        self.layer_2_pic_open = self.save_pic_path + "\\" + self.open_pic_layer_2_name
        self.layer_3_pic_open = self.save_pic_path + "\\" + self.open_pic_layer_3_name
        self.layer_4_pic_open = self.save_pic_path + "\\" + self.open_pic_layer_4_name
        layer_1_pic_is_exist=os.path.exists(self.layer_1_pic_open)
        layer_2_pic_is_exist = os.path.exists(self.layer_2_pic_open)
        layer_3_pic_is_exist = os.path.exists(self.layer_3_pic_open)
        layer_4_pic_is_exist = os.path.exists(self.layer_4_pic_open)
        if layer_1_pic_is_exist and layer_2_pic_is_exist and layer_3_pic_is_exist and layer_4_pic_is_exist:
            try:
                self.pic_detail_panel.Hide()
                self.init_panel.Hide()
                self.operator_muen_panel.Hide()
                self.display_pic_detail_panel = wx.ScrolledWindow(self, -1, pos=(0, 0), size=(960, 600))
                self.display_pic_detail_panel.SetScrollbar(1, 1, 1000, 2000)
                self.display_pic_detail_panel.SetScrollRate(10, 10)
                open_image_layer_1 = wx.Image(self.save_pic_path + "\\" + self.open_pic_layer_1_name,
                                              wx.BITMAP_TYPE_ANY)
                open_image_layer_1.Rescale(500, 458)
                adjust_open_image_layer_1 = open_image_layer_1.ConvertToBitmap()
                staticBmp_open_layer_1 = wx.StaticBitmap(self.display_pic_detail_panel, -1, adjust_open_image_layer_1)
                open_image_layer_2 = wx.Image(self.save_pic_path + "\\" + self.open_pic_layer_2_name,
                                              wx.BITMAP_TYPE_ANY)
                open_image_layer_2.Rescale(500, 458)
                adjust_open_image_layer_2 = open_image_layer_2.ConvertToBitmap()
                staticBmp_open_layer_2 = wx.StaticBitmap(self.display_pic_detail_panel, -1, adjust_open_image_layer_2)
                open_image_layer_3 = wx.Image(self.save_pic_path + "\\" + self.open_pic_layer_3_name,
                                              wx.BITMAP_TYPE_ANY)
                open_image_layer_3.Rescale(500, 458)
                adjust_open_image_layer_3 = open_image_layer_3.ConvertToBitmap()
                staticBmp_open_layer_3 = wx.StaticBitmap(self.display_pic_detail_panel, -1, adjust_open_image_layer_3)
                open_image_layer_4 = wx.Image(self.save_pic_path + "\\" + self.open_pic_layer_4_name,
                                              wx.BITMAP_TYPE_ANY)
                open_image_layer_4.Rescale(500, 458)
                adjust_open_image_layer_4 = open_image_layer_4.ConvertToBitmap()
                staticBmp_open_layer_4 = wx.StaticBitmap(self.display_pic_detail_panel, -1, adjust_open_image_layer_4)
                close_image_layer_1 = wx.Image(self.save_pic_path + "\\" + self.close_pic_layer_1_name,
                                               wx.BITMAP_TYPE_ANY)
                close_image_layer_1.Rescale(500, 458)
                adjust_close_image_layer_1 = close_image_layer_1.ConvertToBitmap()
                staticBmp_close_layer_1 = wx.StaticBitmap(self.display_pic_detail_panel, -1, adjust_close_image_layer_1)
                close_image_layer_2 = wx.Image(self.save_pic_path + "\\" + self.close_pic_layer_2_name,
                                               wx.BITMAP_TYPE_ANY)
                close_image_layer_2.Rescale(500, 458)
                adjust_close_image_layer_2 = close_image_layer_2.ConvertToBitmap()
                staticBmp_close_layer_2 = wx.StaticBitmap(self.display_pic_detail_panel, -1, adjust_close_image_layer_2)
                close_image_layer_3 = wx.Image(self.save_pic_path + "\\" + self.close_pic_layer_3_name,
                                               wx.BITMAP_TYPE_ANY)
                close_image_layer_3.Rescale(500, 458)
                adjust_close_image_layer_3 = close_image_layer_3.ConvertToBitmap()
                staticBmp_close_layer_3 = wx.StaticBitmap(self.display_pic_detail_panel, -1, adjust_close_image_layer_3)
                close_image_layer_4 = wx.Image(self.save_pic_path + "\\" + self.close_pic_layer_4_name,
                                               wx.BITMAP_TYPE_ANY)
                close_image_layer_4.Rescale(500, 458)
                adjust_close_image_layer_4 = close_image_layer_4.ConvertToBitmap()
                staticBmp_close_layer_4 = wx.StaticBitmap(self.display_pic_detail_panel, -1, adjust_close_image_layer_4)
                self.back_to_pic_detail = wx.Button(self.display_pic_detail_panel, -1, "返回")
                self.Bind(wx.EVT_BUTTON, self.back_to_pic_detail_process, self.back_to_pic_detail)
                self.back_to_pic_detail_box = wx.StaticBox(self.display_pic_detail_panel, -1, "")
                self.back_to_pic_detail_box_sizer = wx.StaticBoxSizer(self.back_to_pic_detail_box, wx.VERTICAL)
                self.back_h_box = wx.BoxSizer(wx.HORIZONTAL)
                self.back_h_box.Add(self.back_to_pic_detail, 1, wx.ALL | wx.EXPAND, 2)
                self.back_to_pic_detail_box_sizer.Add(self.back_h_box, 1, wx.ALL | wx.EXPAND, 2)
                self.open_v_box = wx.BoxSizer(wx.VERTICAL)
                self.close_v_box = wx.BoxSizer(wx.VERTICAL)
                self.pic_h_box = wx.BoxSizer(wx.HORIZONTAL)
                self.pic_v_box = wx.BoxSizer(wx.VERTICAL)
                self.open_pic_display_box = wx.StaticBox(self.display_pic_detail_panel, -1, "开门图片")
                self.open_pic_display_box_sizer = wx.StaticBoxSizer(self.open_pic_display_box, wx.VERTICAL)
                self.close_pic_display_box = wx.StaticBox(self.display_pic_detail_panel, -1, "关门图片")
                self.close_pic_display_box_sizer = wx.StaticBoxSizer(self.close_pic_display_box, wx.VERTICAL)
                self.pic_display_box_h = wx.StaticBox(self.display_pic_detail_panel, -1, "")
                self.pic_display_box_h_sizer = wx.StaticBoxSizer(self.pic_display_box_h, wx.HORIZONTAL)
                self.open_v_box.Add(staticBmp_open_layer_1, 1, wx.ALL | wx.EXPAND, 2)
                self.open_v_box.Add(staticBmp_open_layer_2, 1, wx.ALL | wx.EXPAND, 2)
                self.open_v_box.Add(staticBmp_open_layer_3, 1, wx.ALL | wx.EXPAND, 2)
                self.open_v_box.Add(staticBmp_open_layer_4, 1, wx.ALL | wx.EXPAND, 2)
                self.open_pic_display_box_sizer.Add(self.open_v_box, 1, wx.ALL | wx.EXPAND, 2)
                self.close_v_box.Add(staticBmp_close_layer_1, 1, wx.ALL | wx.EXPAND, 2)
                self.close_v_box.Add(staticBmp_close_layer_2, 1, wx.ALL | wx.EXPAND, 2)
                self.close_v_box.Add(staticBmp_close_layer_3, 1, wx.ALL | wx.EXPAND, 2)
                self.close_v_box.Add(staticBmp_close_layer_4, 1, wx.ALL | wx.EXPAND, 2)
                self.close_pic_display_box_sizer.Add(self.close_v_box, 1, wx.ALL | wx.EXPAND, 2)
                self.pic_h_box.Add(self.open_pic_display_box_sizer, 1, wx.ALL | wx.EXPAND, 2)
                self.pic_h_box.Add(self.close_pic_display_box_sizer, 1, wx.ALL | wx.EXPAND, 2)
                self.pic_display_box_h_sizer.Add(self.pic_h_box, 1, wx.ALL | wx.EXPAND, 2)
                self.pic_v_box.Add(self.pic_display_box_h_sizer, 1, wx.ALL | wx.EXPAND, 2)
                self.pic_v_box.Add(self.back_to_pic_detail_box_sizer, 0, wx.ALL | wx.EXPAND, 2)
                self.display_pic_detail_panel.SetSizer(self.pic_v_box)
                self.display_pic_detail_panel.Layout()
                self.display_pic_detail_panel.Fit()
            except:
                return
        else:
            self.system_dlg.SetMessage("图片不存在，先点击下载按钮！！")
            self.system_dlg.ShowModal()
            return

    #返回首页
    def back_to_pic_detail_process(self,evt):
        self.display_pic_detail_panel.Hide()
        self.init_panel.Show()
        self.operator_muen_panel.Show()
    #日志下载
    def down_file_process(self,evt):
        if self.value_down_file.GetValue() =="" or self.value_trans_id.GetValue().strip()=="":
            self.system_dlg.SetMessage("请填写正确的保存路径或者交易ID")
            self.system_dlg.ShowModal()
            return
        elif self.index_devid_type.GetValue()== "设备类型":
            self.system_dlg.SetMessage("请选择设备类型！")
            self.system_dlg.ShowModal()
            return
        try:
            file_path = self.value_down_file.GetValue().strip()
            file_path = file_path.strip("\\")
            is_exists = os.path.exists(file_path)
            if not is_exists:
                os.makedirs(file_path)
        except:
            self.system_dlg.SetMessage("创建目录失败！！！")
            self.system_dlg.ShowModal()
            return
        self.analysis_trans.Disable()
        self.pic_detail_infomation.Disable()
        self.button_down_file.Disable()
        self.down_load_type=1
        self.down_file_process_t = threading.Thread(target=self.down_load_file_T)
        self.down_file_process_t.start()
    #日志下载子进程
    def down_load_file_T(self):
        try:
            ssh_repeat = 0
            dev_id = self.dev_id.GetValue()
            if len(dev_id) == 5:
                port_id = int(dev_id)
            else:
                port_id = "2" + dev_id
            hostid = "m.vegcloud.tech"
            sshid = int(port_id)
            name = "linaro"
            pwd = "Ustaff201"
            while True:
                try:
                    trans_id = self.value_trans_id.GetValue().strip()
                    myclient = paramiko.Transport((hostid, sshid))
                    # myclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    myclient.connect(username=name, password=pwd)
                    sftp = paramiko.SFTPClient.from_transport(myclient)
                    if self.index_devid_type.GetValue() == "CM":
                        remote_file = '/vbg/root/weighcv-cm/log/' + str(trans_id) + ".txt"
                        local_file = self.value_down_file.GetValue().replace("\\","/") + '/' + str(trans_id) + ".txt"
                        sftp.get(remote_file, local_file)
                    if self.index_devid_type.GetValue() == "AS":
                        remote_file = '/vbg/root/weighcv-as/log/' + str(trans_id) + ".txt"
                        local_file = self.value_down_file.GetValue().replace("\\","/") + '/' + str(trans_id) + ".txt"
                        sftp.get(remote_file, local_file)
                except:
                    ssh_repeat += 1
                    if ssh_repeat > 5:
                        self.system_dlg.SetMessage("获取日志失败！！")
                        self.system_dlg.ShowModal()
                        myclient.close()
                        self.button_down_file.Enable()
                        break
                    time.sleep(10)
                else:
                    self.analysis_trans.Enable()
                    self.button_down_file.Enable()
                    myclient.close()
                    self.system_dlg.SetMessage("日志下载成功！！")
                    self.system_dlg.ShowModal()
                    break
        except:
            self.button_down_file.Enable()
            self.system_dlg.SetMessage("日志下载失败！！")
            self.system_dlg.ShowModal()

    #开启FRP端口映射和获取ERP上商品信息
    def begin_Click(self, evt):
        #self.analysis_trans.Disable()
        self.button_down_file.Disable()
        self.analysis_trans.Disable()
        self.begin.Disable()
        self.pic_detail_infomation.Disable()
        self.get_dev_id = self.dev_id.GetValue()
        self.login_user=self.value_longin_name.GetValue()
        self.login_pw=self.value_login_pw.GetValue()
        self.get_union_id=""
        if self.get_dev_id != "" and self.select_url:
            try:
                login_url = "http://www.vegcloud.xyz:8500/login"
                cj = cookiejar.CookieJar()
                cookie_support = urllib.request.HTTPCookieProcessor(cj)
                opener = urllib.request.build_opener(cookie_support, urllib.request.HTTPHandler)
                urllib.request.install_opener(opener)
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
                    'Referer': self.web_Referer}
                postData = {"employee_id": "HZ03881", "employee_pass": "NetRing1"}
                postData = urllib.parse.urlencode(postData, encoding='gb2312').encode('gb2312')
                request_login = urllib.request.Request(self.web_login_dev_url, postData, headers)
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
                                    if online_status != 1:
                                        self.system_dlg.SetMessage("设备不在线！！！")
                                        self.system_dlg.ShowModal()
                                        self.begin.Enable()
                                        return
                        if  self.get_union_id =="":
                            self.system_dlg.SetMessage("设备ID不存在！！！")
                            self.system_dlg.ShowModal()
                            self.begin.Enable()
                            return
                    else:
                        self.system_dlg.SetMessage("获取Union ID 失败")
                        self.system_dlg.ShowModal()
                        self.begin.Enable()
                        return

                else:
                    self.system_dlg.SetMessage("获取Union ID 失败")
                    self.system_dlg.ShowModal()
                    self.begin.Enable()
                    return
            except:
                self.system_dlg.SetMessage("获取Union ID 失败")
                self.system_dlg.ShowModal()
                self.begin.Enable()
                return
            try:
                port_id = self.dev_id.GetValue()
                payload_frp = "{\"devname\": \"" + self.get_union_id + "\", \"req\": { \"A\": 152,\"P\": { \"appname\": \"frp-client-ssh\", \"action\": 4,\"port\":\"" + str(
                    port_id) + "\" }}}"
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
                            self.lock_dlg.SetMessage(pid_status["msg"])
                            self.lock_dlg.ShowModal()
                            self.begin.Enable()
                            return
                    except:
                        self.system_dlg.SetMessage("查询PID失败!!!")
                        self.system_dlg.ShowModal()
                        self.begin.Enable()
                        return
                        # Mymsg = wx.MessageBox("查询PID失败!!!", "Message box", style=wx.OK | wx.CANCEL)
                    time.sleep(1)
                else:
                    self.system_dlg.SetMessage(frp_status["msg"])
                    self.system_dlg.ShowModal()
                    self.begin.Enable()
                    return
            except:
                self.system_dlg.SetMessage(response_frp_open.text)
                self.system_dlg.ShowModal()
                self.begin.Enable()
                return
            try:
                cj = cookiejar.CookieJar()
                cookie_support = urllib.request.HTTPCookieProcessor(cj)
                opener = urllib.request.build_opener(cookie_support, urllib.request.HTTPHandler)
                urllib.request.install_opener(opener)

                login_url = self.web_login_url
                headers_login = {'Referer': self.web_login_Referer,
                                 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
                postData_login = {'employee_id':self.login_user , 'employee_pass': self.login_pw}
                postData_login = urllib.parse.urlencode(postData_login, encoding='gb2312').encode('gb2312')
                request_login = urllib.request.Request(login_url, postData_login, headers_login)
                response_login = urllib.request.urlopen(request_login)
                login_text_org = response_login.read().decode()
                login_text = json.loads(login_text_org)
                login_token = login_text["token"]
                query_goods_url = self.web_query_goods_url
                headers_query_goods = {'Referer': self.web_query_goods_Referer,
                                       'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
                postData_headers_query = {"access_token": login_token, "jwtauth_auth_ret_type": "json",
                                          "command": "query_sku"}

                postData_headers_query = urllib.parse.urlencode(postData_headers_query, encoding='gb2312').encode(
                    'gb2312')
                request_query_goods = urllib.request.Request(query_goods_url, postData_headers_query,
                                                             headers_query_goods)
                response_query_goods = urllib.request.urlopen(request_query_goods)
                query_goods_text_org = response_query_goods.read().decode()
                query_goods_text = json.loads(query_goods_text_org)
                self.goods_info_date = query_goods_text["output"]
                if query_goods_text["msg"].lower() == "success":
                    self.button_down_file.Enable()
                    self.analysis_trans.Enable()
                    self.system_dlg.SetMessage("获取商品信息成功！！")
                    self.system_dlg.ShowModal()
                    self.begin.Enable()

                else:
                    self.system_dlg.SetMessage("获取商品信息失败")
                    self.system_dlg.ShowModal()
                    self.begin.Enable()
            except:
                self.system_dlg.SetMessage("登入ERP 失败")
                self.system_dlg.ShowModal()
                self.begin.Enable()

        elif not self.select_url:
            self.system_dlg.SetMessage("请选择设备所在环境 !!!")
            self.system_dlg.ShowModal()
            self.begin.Enable()
        elif self.get_dev_id == "":
            self.system_dlg.SetMessage("请输入设备 ID !!!")
            self.system_dlg.ShowModal()
            self.begin.Enable()
    #日志过滤显示重量变化和开关门图片识别
    def analysis_trans_operator(self,evt):
        try:
            trans_id = self.value_trans_id.GetValue().strip()
            print(trans_id)
            file_dir = self.value_down_file.GetValue() +"\\"+ str(trans_id) + ".txt"
            f = open(file_dir, "r",encoding='UTF-8')
        except:
            self.system_dlg.SetMessage("打开日志失败")
            self.system_dlg.ShowModal()
            return
        self.close_link_layer_1=""
        self.close_link_layer_2 = ""
        self.close_link_layer_3 = ""
        self.close_link_layer_4 = ""
        self.open_link_layer_1 = ""
        self.open_link_layer_2 = ""
        self.open_link_layer_3 = ""
        self.open_link_layer_4 = ""
        open_goods_code_layer_1_date = []
        open_goods_code_layer_2_date = []
        open_goods_code_layer_3_date = []
        open_goods_code_layer_4_date = []
        close_goods_code_layer_1_date = []
        close_goods_code_layer_2_date = []
        close_goods_code_layer_3_date = []
        close_goods_code_layer_4_date = []
        self.open_link_layer_1=""
        self.open_link_layer_2 = ""
        self.open_link_layer_3 = ""
        self.open_link_layer_4 = ""
        self.close_link_layer_1 = ""
        self.close_link_layer_2 = ""
        self.close_link_layer_3 = ""
        self.close_link_layer_4 = ""
        self.WeighGoodsNumCache_Open_layer_1=[]
        self.WeighGoodsNumCache_Open_layer_2=[]
        self.WeighGoodsNumCache_Open_layer_3=[]
        self.WeighGoodsNumCache_Open_layer_4=[]
        self.WeighGoodsNumCache_Close_layer_1=[]
        self.WeighGoodsNumCache_Close_layer_2=[]
        self.WeighGoodsNumCache_Close_layer_3=[]
        self.WeighGoodsNumCache_Close_layer_4=[]
        WeighGoodsNumCache_Open_layer_1_org = []
        WeighGoodsNumCache_Open_layer_2_org = []
        WeighGoodsNumCache_Open_layer_3_org = []
        WeighGoodsNumCache_Open_layer_4_org = []
        WeighGoodsNumCache_Close_layer_1_org = []
        WeighGoodsNumCache_Close_layer_2_org = []
        WeighGoodsNumCache_Close_layer_3_org = []
        WeighGoodsNumCache_Close_layer_4_org = []
        layer_1_diff=0
        layer_2_diff=0
        layer_3_diff=0
        layer_4_diff=0
        close_goods_change_layer_1 = ""
        close_goods_change_layer_2 = ""
        close_goods_change_layer_3 = ""
        close_goods_change_layer_4 = ""
        close_door = False
        for i in range(20):
            self.value_change_goods_layer_1.SetString(i,"")
            self.value_change_goods_layer_2.SetString(i, "")
            self.value_change_goods_layer_3.SetString(i, "")
            self.value_change_goods_layer_4.SetString(i, "")

        if self.index_devid_type.GetValue()=="CM":
            cache_open=True
            try:
                while True:
                    line = f.readline()
                    if line:
                        open_goods_info_org = re.findall("CVOpenDoorDo OpenObjDetectInfo detectinfo=\s+(.+)", line)
                        close_goods_info_org = re.findall("CVCloseDoorDo CloseObjDetectInfo detectinfo=\s+(.+)", line)
                        layer_1_diff_org = re.findall("DealLockEvent  isclose= true ;weighid= 010101.+opendiff=\s+(\S+)", line)
                        layer_2_diff_org = re.findall("DealLockEvent  isclose= true ;weighid= 010201.+opendiff=\s+(\S+)", line)
                        layer_3_diff_org = re.findall("DealLockEvent  isclose= true ;weighid= 010301.+opendiff=\s+(\S+)", line)
                        layer_4_diff_org = re.findall("DealLockEvent  isclose= true ;weighid= 010401.+opendiff=\s+(\S+)", line)
                        WeighGoodsNumCache_org = re.findall("WeighGoodsNumCache=\s+(.+)", line)
                        if open_goods_info_org:
                            open_goods_info = open_goods_info_org[0]
                            open_goods_info_list = json.loads(open_goods_info)
                            for j in range(len(open_goods_info_list)):
                                if open_goods_info_list[j]["weighid"] == "010101":
                                    open_goods_info_layer_1_org = open_goods_info_list[j]["goodsinfo"]
                                    self.open_link_layer_1=open_goods_info_list[j]["imageurl"]
                                    for j in range(len(open_goods_info_layer_1_org)):
                                        open_goods_info_layer_1_sub = ()
                                        open_goods_info_layer_1_sub = (open_goods_info_layer_1_org[j]["goodsid"],open_goods_info_layer_1_org[j]["goodsnum"])
                                        open_goods_code_layer_1_date.append(open_goods_info_layer_1_sub)
                                elif open_goods_info_list[j]["weighid"] == "010201":
                                    open_goods_info_layer_2_org = open_goods_info_list[j]["goodsinfo"]
                                    self.open_link_layer_2= open_goods_info_list[j]["imageurl"]
                                    for j in range(len(open_goods_info_layer_2_org)):
                                        open_goods_info_layer_2_sub = ()
                                        open_goods_info_layer_2_sub = (open_goods_info_layer_2_org[j]["goodsid"],open_goods_info_layer_2_org[j]["goodsnum"])
                                        open_goods_code_layer_2_date.append(open_goods_info_layer_2_sub)
                                elif open_goods_info_list[j]["weighid"] == "010301":
                                    open_goods_info_layer_3_org = open_goods_info_list[j]["goodsinfo"]
                                    self.open_link_layer_3 = open_goods_info_list[j]["imageurl"]
                                    for j in range(len(open_goods_info_layer_3_org)):
                                        open_goods_info_layer_3_sub = ()
                                        open_goods_info_layer_3_sub = (open_goods_info_layer_3_org[j]["goodsid"],open_goods_info_layer_3_org[j]["goodsnum"])
                                        open_goods_code_layer_3_date.append(open_goods_info_layer_3_sub)
                                elif open_goods_info_list[j]["weighid"] == "010401":
                                    open_goods_info_layer_4_org = open_goods_info_list[j]["goodsinfo"]
                                    self.open_link_layer_4 = open_goods_info_list[j]["imageurl"]
                                    for j in range(len(open_goods_info_layer_4_org)):
                                        open_goods_info_layer_4_sub = ()
                                        open_goods_info_layer_4_sub = (open_goods_info_layer_4_org[j]["goodsid"],open_goods_info_layer_4_org[j]["goodsnum"])
                                        open_goods_code_layer_4_date.append(open_goods_info_layer_4_sub)
                        if close_goods_info_org:
                            close_goods_info = close_goods_info_org[0]
                            close_goods_info_list = json.loads(close_goods_info)
                            for j in range(len(close_goods_info_list)):
                                if close_goods_info_list[j]["weighid"] == "010101":
                                    close_goods_info_layer_1_org = close_goods_info_list[j]["goodsinfo"]
                                    self.close_link_layer_1 = close_goods_info_list[j]["imageurl"]
                                    for j in range(len(close_goods_info_layer_1_org)):
                                        close_goods_info_layer_1_sub = ()
                                        close_goods_info_layer_1_sub = (close_goods_info_layer_1_org[j]["goodsid"],close_goods_info_layer_1_org[j]["goodsnum"])
                                        close_goods_code_layer_1_date.append(close_goods_info_layer_1_sub)
                                elif close_goods_info_list[j]["weighid"] == "010201":
                                    close_goods_info_layer_2_org = close_goods_info_list[j]["goodsinfo"]
                                    self.close_link_layer_2 = close_goods_info_list[j]["imageurl"]
                                    for j in range(len(close_goods_info_layer_2_org)):
                                        close_goods_info_layer_2_sub = ()
                                        close_goods_info_layer_2_sub = (close_goods_info_layer_2_org[j]["goodsid"],close_goods_info_layer_2_org[j]["goodsnum"])
                                        close_goods_code_layer_2_date.append(close_goods_info_layer_2_sub)
                                elif close_goods_info_list[j]["weighid"] == "010301":
                                    close_goods_info_layer_3_org = close_goods_info_list[j]["goodsinfo"]
                                    self.close_link_layer_3 = close_goods_info_list[j]["imageurl"]
                                    for j in range(len(close_goods_info_layer_3_org)):
                                        close_goods_info_layer_3_sub = ()
                                        close_goods_info_layer_3_sub = (close_goods_info_layer_3_org[j]["goodsid"],close_goods_info_layer_3_org[j]["goodsnum"])
                                        close_goods_code_layer_3_date.append(close_goods_info_layer_3_sub)
                                elif close_goods_info_list[j]["weighid"] == "010401":
                                    close_goods_info_layer_4_org = close_goods_info_list[j]["goodsinfo"]
                                    self.close_link_layer_4 = close_goods_info_list[j]["imageurl"]
                                    for j in range(len(close_goods_info_layer_4_org)):
                                        close_goods_info_layer_4_sub = ()
                                        close_goods_info_layer_4_sub = (close_goods_info_layer_4_org[j]["goodsid"], close_goods_info_layer_4_org[j]["goodsnum"])
                                        close_goods_code_layer_4_date.append(close_goods_info_layer_4_sub)
                        if WeighGoodsNumCache_org and cache_open:
                            cache_open=False
                            WeighGoodsNumCache_Open_info = WeighGoodsNumCache_org[0]
                            WeighGoodsNumCache_Open_list = json.loads(WeighGoodsNumCache_Open_info)
                            for i in range(len(WeighGoodsNumCache_Open_list)):
                                if WeighGoodsNumCache_Open_list[i]["weighid"] == "010101":
                                    WeighGoodsNumCache_Open_layer_1_org = WeighGoodsNumCache_Open_list[i]["cur_weigh"]
                                elif WeighGoodsNumCache_Open_list[i]["weighid"] == "010201":
                                    WeighGoodsNumCache_Open_layer_2_org = WeighGoodsNumCache_Open_list[i]["cur_weigh"]
                                elif WeighGoodsNumCache_Open_list[i]["weighid"] == "010301":
                                    WeighGoodsNumCache_Open_layer_3_org = WeighGoodsNumCache_Open_list[i]["cur_weigh"]
                                elif WeighGoodsNumCache_Open_list[i]["weighid"] == "010401":
                                    WeighGoodsNumCache_Open_layer_4_org = WeighGoodsNumCache_Open_list[i]["cur_weigh"]
                        elif WeighGoodsNumCache_org and not cache_open:
                            cache_open=True
                            WeighGoodsNumCache_Close_info = WeighGoodsNumCache_org[0]
                            WeighGoodsNumCache_Close_list = json.loads(WeighGoodsNumCache_Close_info)
                            for i in range(len(WeighGoodsNumCache_Close_list)):
                                if WeighGoodsNumCache_Close_list[i]["weighid"] == "010101":
                                    WeighGoodsNumCache_Close_layer_1_org = WeighGoodsNumCache_Close_list[i]["cur_weigh"]
                                elif WeighGoodsNumCache_Close_list[i]["weighid"] == "010201":
                                    WeighGoodsNumCache_Close_layer_2_org = WeighGoodsNumCache_Close_list[i]["cur_weigh"]
                                elif WeighGoodsNumCache_Close_list[i]["weighid"] == "010301":
                                    WeighGoodsNumCache_Close_layer_3_org = WeighGoodsNumCache_Close_list[i]["cur_weigh"]
                                elif WeighGoodsNumCache_Close_list[i]["weighid"] == "010401":
                                    WeighGoodsNumCache_Close_layer_4_org = WeighGoodsNumCache_Close_list[i]["cur_weigh"]

                        elif layer_1_diff_org:
                            layer_1_diff = layer_1_diff_org[0]
                        elif layer_2_diff_org:
                            layer_2_diff = layer_2_diff_org[0]
                        elif layer_3_diff_org:
                            layer_3_diff = layer_3_diff_org[0]
                        elif layer_4_diff_org:
                            layer_4_diff = layer_4_diff_org[0]
                    else:
                        break
            except:
                self.system_dlg.SetMessage("获取原始数据失败！！")
                self.system_dlg.ShowModal()
                return
            if self.close_link_layer_1:
                change_layer_1 = self.calc_goods(open_goods_code_layer_1_date, close_goods_code_layer_1_date)
            else:
                change_layer_1 = {}
            if self.close_link_layer_2:
                change_layer_2 = self.calc_goods(open_goods_code_layer_2_date, close_goods_code_layer_2_date)
            else:
                change_layer_2 = {}
            if self.close_link_layer_3:
                change_layer_3 = self.calc_goods(open_goods_code_layer_3_date, close_goods_code_layer_3_date)
            else:
                change_layer_3 = {}
            if self.close_link_layer_4:
                change_layer_4 = self.calc_goods(open_goods_code_layer_4_date, close_goods_code_layer_4_date)
            else:
                change_layer_4 = {}
            change_goods_name_1 = self.goods_name_lock(change_layer_1, self.goods_info_date)
            change_weight_1 = self.change_weight(change_layer_1, self.goods_info_date)
            change_goods_name_2 = self.goods_name_lock(change_layer_2, self.goods_info_date)
            change_weight_2 = self.change_weight(change_layer_2, self.goods_info_date)
            change_goods_name_3 = self.goods_name_lock(change_layer_3, self.goods_info_date)
            change_weight_3 = self.change_weight(change_layer_3, self.goods_info_date)
            change_goods_name_4 = self.goods_name_lock(change_layer_4, self.goods_info_date)
            change_weight_4 = self.change_weight(change_layer_4, self.goods_info_date)
            change_goods_name_list_1=self.display_trans(change_goods_name_1)
            if len(change_goods_name_list_1):
                for i in range(len(change_goods_name_list_1)):
                    self.value_change_goods_layer_1.SetString(i,change_goods_name_list_1[i])
            else:
                self.value_change_goods_layer_1.SetString(0, "")
            change_goods_name_list_2 =self.display_trans(change_goods_name_2)
            if len(change_goods_name_list_2):
                for i in range(len(change_goods_name_list_2)):
                    self.value_change_goods_layer_2.SetString(i,change_goods_name_list_2[i])
            else:
                self.value_change_goods_layer_2.SetString(0, "")
            change_goods_name_list_3 =self.display_trans(change_goods_name_3)
            if len(change_goods_name_list_3):
                for i in range(len(change_goods_name_list_3)):
                    self.value_change_goods_layer_3.SetString(i,change_goods_name_list_3[i])
            else:
                self.value_change_goods_layer_3.SetString(0, "")
            change_goods_name_list_4 =self.display_trans(change_goods_name_4)
            if len(change_goods_name_list_4):
                for i in range(len(change_goods_name_list_4)):
                    self.value_change_goods_layer_4.SetString(i,change_goods_name_list_4[i])
            else:
                self.value_change_goods_layer_4.SetString(0, "")
            #self.value_change_goods_layer_1.SetValue(str(change_goods_name_1))
            #self.value_change_goods_layer_2.SetValue(str(change_goods_name_2))
            #self.value_change_goods_layer_3.SetValue(str(change_goods_name_3))
            #self.value_change_goods_layer_4.SetValue(str(change_goods_name_4))
            self.pic_change_weight_layer_1.SetValue(str(change_weight_1))
            self.pic_change_weight_layer_2.SetValue(str(change_weight_2))
            self.pic_change_weight_layer_3.SetValue(str(change_weight_3))
            self.pic_change_weight_layer_4.SetValue(str(change_weight_4))
            self.value_change_weight_layer_1.SetValue(str(layer_1_diff))
            self.value_change_weight_layer_2.SetValue(str(layer_2_diff))
            self.value_change_weight_layer_3.SetValue(str(layer_3_diff))
            self.value_change_weight_layer_4.SetValue(str(layer_4_diff))
            open_goods_code_layer_1_dict = self.list_to_dic(open_goods_code_layer_1_date)
            open_goods_code_layer_2_dict = self.list_to_dic(open_goods_code_layer_2_date)
            open_goods_code_layer_3_dict = self.list_to_dic(open_goods_code_layer_3_date)
            open_goods_code_layer_4_dict = self.list_to_dic(open_goods_code_layer_4_date)
            close_goods_code_layer_1_dict = self.list_to_dic(close_goods_code_layer_1_date)
            close_goods_code_layer_2_dict = self.list_to_dic(close_goods_code_layer_2_date)
            close_goods_code_layer_3_dict = self.list_to_dic(close_goods_code_layer_3_date)
            close_goods_code_layer_4_dict = self.list_to_dic(close_goods_code_layer_4_date)
            self.org_open_goods_name_layer_1 = self.goods_name_lock(open_goods_code_layer_1_dict, self.goods_info_date)
            self.org_open_goods_name_layer_2 = self.goods_name_lock(open_goods_code_layer_2_dict, self.goods_info_date)
            self.org_open_goods_name_layer_3 = self.goods_name_lock(open_goods_code_layer_3_dict, self.goods_info_date)
            self.org_open_goods_name_layer_4 = self.goods_name_lock(open_goods_code_layer_4_dict, self.goods_info_date)
            self.org_close_goods_name_layer_1 = self.goods_name_lock(close_goods_code_layer_1_dict,self.goods_info_date)
            self.org_close_goods_name_layer_2 = self.goods_name_lock(close_goods_code_layer_2_dict,self.goods_info_date)
            self.org_close_goods_name_layer_3 = self.goods_name_lock(close_goods_code_layer_3_dict,self.goods_info_date)
            self.org_close_goods_name_layer_4 = self.goods_name_lock(close_goods_code_layer_4_dict,self.goods_info_date)
            if int(change_weight_1[0]) <= int(layer_1_diff) and int(layer_1_diff) <= int(change_weight_1[1]):
                self.pic_change_weight_layer_1.SetBackgroundColour("Green")
                self.value_change_weight_layer_1.SetBackgroundColour("Green")
                self.pic_change_weight_layer_1.SetForegroundColour("Red")
                self.value_change_weight_layer_1.SetForegroundColour("Red")
            elif int(change_weight_1[0])==int(change_weight_1[1])==0:
                if -8<=int(layer_1_diff) and int(layer_1_diff) <= 8:
                    self.pic_change_weight_layer_1.SetBackgroundColour("Green")
                    self.value_change_weight_layer_1.SetBackgroundColour("Green")
                    self.pic_change_weight_layer_1.SetForegroundColour("Red")
                    self.value_change_weight_layer_1.SetForegroundColour("Red")
                else:
                    self.pic_change_weight_layer_1.SetBackgroundColour("Red")
                    self.value_change_weight_layer_1.SetBackgroundColour("Red")
                    self.pic_change_weight_layer_1.SetForegroundColour("Black")
                    self.value_change_weight_layer_1.SetForegroundColour("Black")
            else:
                self.pic_change_weight_layer_1.SetBackgroundColour("Red")
                self.value_change_weight_layer_1.SetBackgroundColour("Red")
                self.pic_change_weight_layer_1.SetForegroundColour("Black")
                self.value_change_weight_layer_1.SetForegroundColour("Black")
            if int(change_weight_2[0]) <= int(layer_2_diff) and int(layer_2_diff) <= int(change_weight_2[1]):
                self.pic_change_weight_layer_2.SetBackgroundColour("Green")
                self.value_change_weight_layer_2.SetBackgroundColour("Green")
                self.pic_change_weight_layer_2.SetForegroundColour("Red")
                self.value_change_weight_layer_2.SetForegroundColour("Red")
            elif int(change_weight_2[0])==int(change_weight_2[1])==0:
                if -8<=int(layer_2_diff) and int(layer_2_diff) <= 8:
                    self.pic_change_weight_layer_2.SetBackgroundColour("Green")
                    self.value_change_weight_layer_2.SetBackgroundColour("Green")
                    self.pic_change_weight_layer_2.SetForegroundColour("Red")
                    self.value_change_weight_layer_2.SetForegroundColour("Red")
                else:
                    self.pic_change_weight_layer_2.SetBackgroundColour("Red")
                    self.value_change_weight_layer_2.SetBackgroundColour("Red")
                    self.pic_change_weight_layer_2.SetForegroundColour("Black")
                    self.value_change_weight_layer_2.SetForegroundColour("Black")
            else:
                self.pic_change_weight_layer_2.SetBackgroundColour("Red")
                self.value_change_weight_layer_2.SetBackgroundColour("Red")
                self.pic_change_weight_layer_2.SetForegroundColour("Black")
                self.value_change_weight_layer_2.SetForegroundColour("Black")
            if int(change_weight_3[0]) <= int(layer_3_diff) and int(layer_3_diff) <= int(change_weight_3[1]):
                self.pic_change_weight_layer_3.SetBackgroundColour("Green")
                self.value_change_weight_layer_3.SetBackgroundColour("Green")
                self.pic_change_weight_layer_3.SetForegroundColour("Red")
                self.value_change_weight_layer_3.SetForegroundColour("Red")
            elif int(change_weight_3[0])==int(change_weight_3[1])==0:
                if -8<=int(layer_3_diff) and int(layer_3_diff) <= 8:
                    self.pic_change_weight_layer_3.SetBackgroundColour("Green")
                    self.value_change_weight_layer_3.SetBackgroundColour("Green")
                    self.pic_change_weight_layer_3.SetForegroundColour("Red")
                    self.value_change_weight_layer_3.SetForegroundColour("Red")
                else:
                    self.pic_change_weight_layer_3.SetBackgroundColour("Red")
                    self.value_change_weight_layer_3.SetBackgroundColour("Red")
                    self.pic_change_weight_layer_3.SetForegroundColour("Black")
                    self.value_change_weight_layer_3.SetForegroundColour("Black")
            else:
                self.pic_change_weight_layer_3.SetBackgroundColour("Red")
                self.value_change_weight_layer_3.SetBackgroundColour("Red")
                self.pic_change_weight_layer_3.SetForegroundColour("Black")
                self.value_change_weight_layer_3.SetForegroundColour("Black")
            if int(change_weight_4[0]) <= int(layer_4_diff) and int(layer_4_diff) <= int(change_weight_4[1]):
                self.pic_change_weight_layer_4.SetBackgroundColour("Green")
                self.value_change_weight_layer_4.SetBackgroundColour("Green")
                self.pic_change_weight_layer_4.SetForegroundColour("Red")
                self.value_change_weight_layer_4.SetForegroundColour("Red")
            elif int(change_weight_4[0])==int(change_weight_4[1])==0:
                if -8<=int(layer_4_diff) and int(layer_4_diff) <= 8:
                    self.pic_change_weight_layer_4.SetBackgroundColour("Green")
                    self.value_change_weight_layer_4.SetBackgroundColour("Green")
                    self.pic_change_weight_layer_4.SetForegroundColour("Red")
                    self.value_change_weight_layer_4.SetForegroundColour("Red")
                else:
                    self.pic_change_weight_layer_4.SetBackgroundColour("Red")
                    self.value_change_weight_layer_4.SetBackgroundColour("Red")
                    self.pic_change_weight_layer_4.SetForegroundColour("Black")
                    self.value_change_weight_layer_4.SetForegroundColour("Black")
            else:
                self.pic_change_weight_layer_4.SetBackgroundColour("Red")
                self.value_change_weight_layer_4.SetBackgroundColour("Red")
                self.pic_change_weight_layer_4.SetForegroundColour("Black")
                self.value_change_weight_layer_4.SetForegroundColour("Black")
            self.pic_detail_infomation.Enable()
        elif self.index_devid_type.GetValue() == "AS":
            layer_1_close_detect=False
            layer_2_close_detect = False
            layer_3_close_detect = False
            layer_4_close_detect = False
            while True:
                line = f.readline()
                if line:
                    if not close_door:
                        detect_close_door = re.findall("ASGetLockChgDetectGoods:", line)
                        open_detect_goods_layer_1 = re.findall(
                            "DoObjDetect OpenObjDetectInfo weId: 010101 detectinfo=\s+(.+)", line)
                        open_detect_goods_layer_2 = re.findall(
                            "DoObjDetect OpenObjDetectInfo weId: 010201 detectinfo=\s+(.+)", line)
                        open_detect_goods_layer_3 = re.findall(
                            "DoObjDetect OpenObjDetectInfo weId: 010301 detectinfo=\s+(.+)", line)
                        open_detect_goods_layer_4 = re.findall(
                            "DoObjDetect OpenObjDetectInfo weId: 010401 detectinfo=\s+(.+)", line)
                        close_detect_goods_layer_1 = re.findall(
                            "DoObjDetect CloseObjDetectInfo weId: 010101 detectinfo=\s+(.+)", line)
                        close_detect_goods_layer_2 = re.findall(
                            "DoObjDetect CloseObjDetectInfo weId: 010201 detectinfo=\s+(.+)", line)
                        close_detect_goods_layer_3 = re.findall(
                            "DoObjDetect CloseObjDetectInfo weId: 010301 detectinfo=\s(.+)", line)
                        close_detect_goods_layer_4 = re.findall(
                            "DoObjDetect CloseObjDetectInfo weId: 010401 detectinfo=\s(.+)", line)
                        WeighGoodsNumCache_Open_org = re.findall("WeighGoodsNumCache=\s+(.+)", line)
                        if detect_close_door:
                            close_door = True
                        if open_detect_goods_layer_1:
                            open_goods_code_layer_1_date_org = json.loads(open_detect_goods_layer_1[0])
                            open_goods_code_layer_1_date_list = open_goods_code_layer_1_date_org["goodsinfo"]
                            for i in range(len(open_goods_code_layer_1_date_list)):
                                open_goods_code_layer_1_date_sub = {}
                                open_goods_code_layer_1_date_sub["goodsname"] = open_goods_code_layer_1_date_list[i][
                                    "goodsname"]
                                open_goods_code_layer_1_date_sub["goodsnum"] = open_goods_code_layer_1_date_list[i][
                                    "goodsnum"]
                                open_goods_code_layer_1_date.append(open_goods_code_layer_1_date_sub)
                        elif open_detect_goods_layer_2:
                            open_goods_code_layer_2_date_org = json.loads(open_detect_goods_layer_2[0])
                            open_goods_code_layer_2_date_list = open_goods_code_layer_2_date_org["goodsinfo"]
                            for i in range(len(open_goods_code_layer_2_date_list)):
                                open_goods_code_layer_2_date_sub = {}
                                open_goods_code_layer_2_date_sub["goodsname"] = open_goods_code_layer_2_date_list[i][
                                    "goodsname"]
                                open_goods_code_layer_2_date_sub["goodsnum"] = open_goods_code_layer_2_date_list[i][
                                    "goodsnum"]
                                open_goods_code_layer_2_date.append(open_goods_code_layer_2_date_sub)
                        elif open_detect_goods_layer_3:
                            open_goods_code_layer_3_date_org = json.loads(open_detect_goods_layer_3[0])
                            open_goods_code_layer_3_date_list = open_goods_code_layer_3_date_org["goodsinfo"]
                            for i in range(len(open_goods_code_layer_3_date_list)):
                                open_goods_code_layer_3_date_sub = {}
                                open_goods_code_layer_3_date_sub["goodsname"] = open_goods_code_layer_3_date_list[i][
                                    "goodsname"]
                                open_goods_code_layer_3_date_sub["goodsnum"] = open_goods_code_layer_3_date_list[i][
                                    "goodsnum"]
                                open_goods_code_layer_3_date.append(open_goods_code_layer_3_date_sub)
                        elif open_detect_goods_layer_4:
                            open_goods_code_layer_4_date_org = json.loads(open_detect_goods_layer_4[0])
                            open_goods_code_layer_4_date_list = open_goods_code_layer_4_date_org["goodsinfo"]
                            for i in range(len(open_goods_code_layer_4_date_list)):
                                open_goods_code_layer_4_date_sub = {}
                                open_goods_code_layer_4_date_sub["goodsname"] = open_goods_code_layer_4_date_list[i][
                                    "goodsname"]
                                open_goods_code_layer_4_date_sub["goodsnum"] = open_goods_code_layer_4_date_list[i][
                                    "goodsnum"]
                                open_goods_code_layer_4_date.append(open_goods_code_layer_4_date_sub)
                        if close_detect_goods_layer_1:
                            close_goods_code_layer_1_date_org = json.loads(close_detect_goods_layer_1[0])
                            close_goods_code_layer_1_date_list = close_goods_code_layer_1_date_org["goodsinfo"]
                            for i in range(len(close_goods_code_layer_1_date_list)):
                                close_goods_code_layer_1_date_sub = {}
                                close_goods_code_layer_1_date_sub["goodsname"] = close_goods_code_layer_1_date_list[i][
                                    "goodsname"]
                                close_goods_code_layer_1_date_sub["goodsnum"] = close_goods_code_layer_1_date_list[i][
                                    "goodsnum"]
                                close_goods_code_layer_1_date.append(close_goods_code_layer_1_date_sub)
                        elif close_detect_goods_layer_2:
                            close_goods_code_layer_2_date_org = json.loads(close_detect_goods_layer_2[0])
                            close_goods_code_layer_2_date_list = close_goods_code_layer_2_date_org["goodsinfo"]
                            for i in range(len(close_goods_code_layer_2_date_list)):
                                close_goods_code_layer_2_date_sub = {}
                                close_goods_code_layer_2_date_sub["goodsname"] = close_goods_code_layer_2_date_list[i][
                                    "goodsname"]
                                close_goods_code_layer_2_date_sub["goodsnum"] = close_goods_code_layer_2_date_list[i][
                                    "goodsnum"]
                                close_goods_code_layer_2_date.append(close_goods_code_layer_2_date_sub)
                        elif close_detect_goods_layer_3:
                            close_goods_code_layer_3_date_org = json.loads(close_detect_goods_layer_3[0])
                            close_goods_code_layer_3_date_list = close_goods_code_layer_3_date_org["goodsinfo"]
                            for i in range(len(close_goods_code_layer_3_date_list)):
                                close_goods_code_layer_3_date_sub = {}
                                close_goods_code_layer_3_date_sub["goodsname"] = close_goods_code_layer_3_date_list[i][
                                    "goodsname"]
                                close_goods_code_layer_3_date_sub["goodsnum"] = close_goods_code_layer_3_date_list[i][
                                    "goodsnum"]
                                close_goods_code_layer_3_date.append(close_goods_code_layer_3_date_sub)
                        elif close_detect_goods_layer_4:
                            close_goods_code_layer_4_date_org = json.loads(close_detect_goods_layer_4[0])
                            close_goods_code_layer_4_date_list = close_goods_code_layer_4_date_org["goodsinfo"]
                            for i in range(len(close_goods_code_layer_4_date_list)):
                                close_goods_code_layer_4_date_sub = {}
                                close_goods_code_layer_4_date_sub["goodsname"] = close_goods_code_layer_4_date_list[i][
                                    "goodsname"]
                                close_goods_code_layer_4_date_sub["goodsnum"] = close_goods_code_layer_4_date_list[i][
                                    "goodsnum"]
                                close_goods_code_layer_4_date.append(close_goods_code_layer_4_date_sub)
                        if WeighGoodsNumCache_Open_org:
                            WeighGoodsNumCache_Open_info = WeighGoodsNumCache_Open_org[0]
                            WeighGoodsNumCache_Open_list = json.loads(WeighGoodsNumCache_Open_info)
                            for i in range(len(WeighGoodsNumCache_Open_list)):
                                if WeighGoodsNumCache_Open_list[i]["weighid"] == "010101":
                                    WeighGoodsNumCache_Open_layer_1_org = WeighGoodsNumCache_Open_list[i]["cur_weigh"]
                                elif WeighGoodsNumCache_Open_list[i]["weighid"] == "010201":
                                    WeighGoodsNumCache_Open_layer_2_org = WeighGoodsNumCache_Open_list[i]["cur_weigh"]
                                elif WeighGoodsNumCache_Open_list[i]["weighid"] == "010301":
                                    WeighGoodsNumCache_Open_layer_3_org = WeighGoodsNumCache_Open_list[i]["cur_weigh"]
                                elif WeighGoodsNumCache_Open_list[i]["weighid"] == "010401":
                                    WeighGoodsNumCache_Open_layer_4_org = WeighGoodsNumCache_Open_list[i]["cur_weigh"]
                    elif close_door:
                        if not layer_1_close_detect:
                            close_goods_change_layer_1_org = re.findall(
                                "ChgObjDetect\\[ \d+ \\]=  {\d+ 010101 0 \\[(.*?)\\]", line)
                        if not layer_2_close_detect:
                            close_goods_change_layer_2_org = re.findall(
                                "ChgObjDetect\\[ \d+ \\]=  {\d+ 010201 0 \\[(.*?)\\]", line)
                        if not layer_3_close_detect:
                            close_goods_change_layer_3_org = re.findall(
                                "ChgObjDetect\\[ \d+ \\]=  {\d+ 010301 0 \\[(.*?)\\]", line)
                        if not layer_4_close_detect:
                            close_goods_change_layer_4_org = re.findall(
                                "ChgObjDetect\\[ \d+ \\]=  {\d+ 010401 0 \\[(.*?)\\]", line)
                        layer_1_diff_org = re.findall(
                            "DealLockEvent  isclose= true ;weighid= 010101.+opendiff=\s+(\S+)", line)
                        layer_2_diff_org = re.findall(
                            "DealLockEvent  isclose= true ;weighid= 010201.+opendiff=\s+(\S+)", line)
                        layer_3_diff_org = re.findall(
                            "DealLockEvent  isclose= true ;weighid= 010301.+opendiff=\s+(\S+)", line)
                        layer_4_diff_org = re.findall(
                            "DealLockEvent  isclose= true ;weighid= 010401.+opendiff=\s+(\S+)", line)
                        WeighGoodsNumCache_Close_org = re.findall("WeighGoodsNumCache=\s+(.+)", line)
                        if WeighGoodsNumCache_Close_org:
                            WeighGoodsNumCache_Close_info = WeighGoodsNumCache_Close_org[0]
                            WeighGoodsNumCache_Close_list = json.loads(WeighGoodsNumCache_Close_info)
                            for i in range(len(WeighGoodsNumCache_Close_list)):
                                if WeighGoodsNumCache_Close_list[i]["weighid"] == "010101":
                                    WeighGoodsNumCache_Close_layer_1_org = WeighGoodsNumCache_Close_list[i]["cur_weigh"]
                                elif WeighGoodsNumCache_Close_list[i]["weighid"] == "010201":
                                    WeighGoodsNumCache_Close_layer_2_org = WeighGoodsNumCache_Close_list[i]["cur_weigh"]
                                elif WeighGoodsNumCache_Close_list[i]["weighid"] == "010301":
                                    WeighGoodsNumCache_Close_layer_3_org = WeighGoodsNumCache_Close_list[i]["cur_weigh"]
                                elif WeighGoodsNumCache_Close_list[i]["weighid"] == "010401":
                                    WeighGoodsNumCache_Close_layer_4_org = WeighGoodsNumCache_Close_list[i]["cur_weigh"]
                        if close_goods_change_layer_1_org:
                            close_goods_change_layer_1 = close_goods_change_layer_1_org[0]
                            layer_1_close_detect = True
                        if close_goods_change_layer_2_org:
                            close_goods_change_layer_2 = close_goods_change_layer_2_org[0]
                            layer_2_close_detect = True
                        if close_goods_change_layer_3_org:
                            close_goods_change_layer_3 = close_goods_change_layer_3_org[0]
                            layer_3_close_detect = True
                        if close_goods_change_layer_4_org:
                            close_goods_change_layer_4 = close_goods_change_layer_4_org[0]
                            layer_4_close_detect = True
                        if layer_1_diff_org:
                            layer_1_diff = layer_1_diff_org[0]
                        if layer_2_diff_org:
                            layer_2_diff = layer_2_diff_org[0]
                        if layer_3_diff_org:
                            layer_3_diff = layer_3_diff_org[0]
                        if layer_4_diff_org:
                            layer_4_diff = layer_4_diff_org[0]
                else:
                    break
                transfer_list_goods = re.compile("\{\d+\s+\d+\s+(\S+)\s+(\d+)\s+(\d+)?\}?")
                transfer_list_weight = re.compile("\{\d+\s+(\d+)\s+(\S+)\s+(\d+)\s+(\d+)?\}?")
                if close_goods_change_layer_1 == "":
                    close_goods_change_layer_1_list_goods = []
                    close_goods_change_layer_1_list_weight = []
                else:
                    close_goods_change_layer_1_list_goods = transfer_list_goods.findall(close_goods_change_layer_1)
                    close_goods_change_layer_1_list_weight = transfer_list_weight.findall(close_goods_change_layer_1)
                if close_goods_change_layer_2 == "":
                    close_goods_change_layer_2_list_goods = []
                    close_goods_change_layer_2_list_weight = []
                else:
                    close_goods_change_layer_2_list_goods = transfer_list_goods.findall(close_goods_change_layer_2)
                    close_goods_change_layer_2_list_weight = transfer_list_weight.findall(close_goods_change_layer_2)
                if close_goods_change_layer_3 == "":
                    close_goods_change_layer_3_list_goods = []
                    close_goods_change_layer_3_list_weight = []
                else:
                    close_goods_change_layer_3_list_goods = transfer_list_goods.findall(close_goods_change_layer_3)
                    close_goods_change_layer_3_list_weight = transfer_list_weight.findall(close_goods_change_layer_3)
                if close_goods_change_layer_4 == "":
                    close_goods_change_layer_4_list_goods = []
                    close_goods_change_layer_4_list_weight = []
                else:
                    close_goods_change_layer_4_list_goods = transfer_list_goods.findall(close_goods_change_layer_4)
                    close_goods_change_layer_4_list_weight = transfer_list_weight.findall(close_goods_change_layer_4)
            close_change_weight_1=self.change_weigh_as(close_goods_change_layer_1_list_weight,self.goods_info_date)
            close_change_weight_2 = self.change_weigh_as(close_goods_change_layer_2_list_weight, self.goods_info_date)
            close_change_weight_3 = self.change_weigh_as(close_goods_change_layer_3_list_weight, self.goods_info_date)
            close_change_weight_4 = self.change_weigh_as(close_goods_change_layer_4_list_weight, self.goods_info_date)
            if len(close_goods_change_layer_1_list_goods):
                for i in range(len(close_goods_change_layer_1_list_goods)):
                    self.value_change_goods_layer_1.SetString(i,str(close_goods_change_layer_1_list_goods[i]))
            if len(close_goods_change_layer_2_list_goods):
                for i in range(len(close_goods_change_layer_2_list_goods)):
                    self.value_change_goods_layer_2.SetString(i,str(close_goods_change_layer_2_list_goods[i]))
            if len(close_goods_change_layer_3_list_goods):
                for i in range(len(close_goods_change_layer_3_list_goods)):
                    self.value_change_goods_layer_3.SetString(i,str(close_goods_change_layer_3_list_goods[i]))
            if len(close_goods_change_layer_4_list_goods):
                for i in range(len(close_goods_change_layer_4_list_goods)):
                    self.value_change_goods_layer_4.SetString(i,str(close_goods_change_layer_4_list_goods[i]))
            self.pic_change_weight_layer_1.SetValue(str(close_change_weight_1))
            self.pic_change_weight_layer_2.SetValue(str(close_change_weight_2))
            self.pic_change_weight_layer_3.SetValue(str(close_change_weight_3))
            self.pic_change_weight_layer_4.SetValue(str(close_change_weight_4))
            self.value_change_weight_layer_1.SetValue(str(layer_1_diff))
            self.value_change_weight_layer_2.SetValue(str(layer_2_diff))
            self.value_change_weight_layer_3.SetValue(str(layer_3_diff))
            self.value_change_weight_layer_4.SetValue(str(layer_4_diff))
            if int(close_change_weight_1[0]) <= int(layer_1_diff) and int(layer_1_diff) <= int(close_change_weight_1[1]):
                self.pic_change_weight_layer_1.SetBackgroundColour("Green")
                self.value_change_weight_layer_1.SetBackgroundColour("Green")
                self.pic_change_weight_layer_1.SetForegroundColour("Red")
                self.value_change_weight_layer_1.SetForegroundColour("Red")
            elif int(close_change_weight_1[0])==0 and int(close_change_weight_1[1])==0:
                if int(close_change_weight_1[0])-8 <= int(layer_1_diff) and int(layer_1_diff) <= int(close_change_weight_1[1])+8:
                    self.pic_change_weight_layer_1.SetBackgroundColour("Green")
                    self.value_change_weight_layer_1.SetBackgroundColour("Green")
                    self.pic_change_weight_layer_1.SetForegroundColour("Red")
                    self.value_change_weight_layer_1.SetForegroundColour("Red")
                else:
                    self.pic_change_weight_layer_1.SetBackgroundColour("Red")
                    self.value_change_weight_layer_1.SetBackgroundColour("Red")
                    self.pic_change_weight_layer_1.SetForegroundColour("Black")
                    self.value_change_weight_layer_1.SetForegroundColour("Black")
            else:
                self.pic_change_weight_layer_1.SetBackgroundColour("Red")
                self.value_change_weight_layer_1.SetBackgroundColour("Red")
                self.pic_change_weight_layer_1.SetForegroundColour("Black")
                self.value_change_weight_layer_1.SetForegroundColour("Black")
            if int(close_change_weight_2[0]) <= int(layer_2_diff) and int(layer_2_diff) <= int(close_change_weight_2[1]):
                self.pic_change_weight_layer_2.SetBackgroundColour("Green")
                self.value_change_weight_layer_2.SetBackgroundColour("Green")
                self.pic_change_weight_layer_2.SetForegroundColour("Red")
                self.value_change_weight_layer_2.SetForegroundColour("Red")
            elif int(close_change_weight_2[0])==0 and int(close_change_weight_2[1])==0:
                if int(close_change_weight_2[0])-8 <= int(layer_2_diff) and int(layer_2_diff) <= int(close_change_weight_2[1])+8:
                    self.pic_change_weight_layer_2.SetBackgroundColour("Green")
                    self.value_change_weight_layer_2.SetBackgroundColour("Green")
                    self.pic_change_weight_layer_2.SetForegroundColour("Red")
                    self.value_change_weight_layer_2.SetForegroundColour("Red")
                else:
                    self.pic_change_weight_layer_2.SetBackgroundColour("Red")
                    self.value_change_weight_layer_2.SetBackgroundColour("Red")
                    self.pic_change_weight_layer_2.SetForegroundColour("Black")
                    self.value_change_weight_layer_2.SetForegroundColour("Black")
            else:
                self.pic_change_weight_layer_2.SetBackgroundColour("Red")
                self.value_change_weight_layer_2.SetBackgroundColour("Red")
                self.pic_change_weight_layer_2.SetForegroundColour("Black")
                self.value_change_weight_layer_2.SetForegroundColour("Black")
            if int(close_change_weight_3[0]) <= int(layer_3_diff) and int(layer_3_diff) <= int(close_change_weight_3[1]):
                self.pic_change_weight_layer_3.SetBackgroundColour("Green")
                self.value_change_weight_layer_3.SetBackgroundColour("Green")
                self.pic_change_weight_layer_3.SetForegroundColour("Red")
                self.value_change_weight_layer_3.SetForegroundColour("Red")
            elif int(close_change_weight_3[0])==0 and int(close_change_weight_3[1])==0:
                if  int(close_change_weight_3[0])-8 <= int(layer_3_diff) and int(layer_3_diff) <= int(close_change_weight_3[1])+8:
                    self.pic_change_weight_layer_3.SetBackgroundColour("Green")
                    self.value_change_weight_layer_3.SetBackgroundColour("Green")
                    self.pic_change_weight_layer_3.SetForegroundColour("Red")
                    self.value_change_weight_layer_3.SetForegroundColour("Red")
                else:
                    self.pic_change_weight_layer_3.SetBackgroundColour("Red")
                    self.value_change_weight_layer_3.SetBackgroundColour("Red")
                    self.pic_change_weight_layer_3.SetForegroundColour("Black")
                    self.value_change_weight_layer_3.SetForegroundColour("Black")
            else:
                self.pic_change_weight_layer_3.SetBackgroundColour("Red")
                self.value_change_weight_layer_3.SetBackgroundColour("Red")
                self.pic_change_weight_layer_3.SetForegroundColour("Black")
                self.value_change_weight_layer_3.SetForegroundColour("Black")
            if int(close_change_weight_4[0]) <= int(layer_4_diff) and int(layer_4_diff) <= int(close_change_weight_4[1]):
                self.pic_change_weight_layer_4.SetBackgroundColour("Green")
                self.value_change_weight_layer_4.SetBackgroundColour("Green")
                self.pic_change_weight_layer_4.SetForegroundColour("Red")
                self.value_change_weight_layer_4.SetForegroundColour("Red")
            elif int(close_change_weight_4[0])==0 and int(close_change_weight_4[1])==0:
                if int(close_change_weight_4[0])-8 <= int(layer_4_diff) and int(layer_4_diff) <= int(close_change_weight_4[0])+8:
                    self.pic_change_weight_layer_4.SetBackgroundColour("Green")
                    self.value_change_weight_layer_4.SetBackgroundColour("Green")
                    self.pic_change_weight_layer_4.SetForegroundColour("Red")
                    self.value_change_weight_layer_4.SetForegroundColour("Red")
                else:
                    self.pic_change_weight_layer_4.SetBackgroundColour("Red")
                    self.value_change_weight_layer_4.SetBackgroundColour("Red")
                    self.pic_change_weight_layer_4.SetForegroundColour("Black")
                    self.value_change_weight_layer_4.SetForegroundColour("Black")
            else:
                self.pic_change_weight_layer_4.SetBackgroundColour("Red")
                self.value_change_weight_layer_4.SetBackgroundColour("Red")
                self.pic_change_weight_layer_4.SetForegroundColour("Black")
                self.value_change_weight_layer_4.SetForegroundColour("Black")
            self.org_close_goods_name_layer_1 = close_goods_code_layer_1_date
            self.org_close_goods_name_layer_2 = close_goods_code_layer_2_date
            self.org_close_goods_name_layer_3 = close_goods_code_layer_3_date
            self.org_close_goods_name_layer_4 = close_goods_code_layer_4_date
            self.org_open_goods_name_layer_1 = open_goods_code_layer_1_date
            self.org_open_goods_name_layer_2 = open_goods_code_layer_2_date
            self.org_open_goods_name_layer_3 = open_goods_code_layer_3_date
            self.org_open_goods_name_layer_4 = open_goods_code_layer_4_date
            self.pic_detail_infomation.Enable()
        if WeighGoodsNumCache_Open_layer_1_org:
            for i in range(len(WeighGoodsNumCache_Open_layer_1_org)):
                goods_cache = {}
                goods_cache["barcode"] = WeighGoodsNumCache_Open_layer_1_org[i]["goodsid"]
                goods_cache["num"] = [WeighGoodsNumCache_Open_layer_1_org[i]["goodsnum"],
                                      WeighGoodsNumCache_Open_layer_1_org[i]["isabngds"]]
                self.WeighGoodsNumCache_Open_layer_1.append(goods_cache)
        if WeighGoodsNumCache_Open_layer_2_org:
            for i in range(len(WeighGoodsNumCache_Open_layer_2_org)):
                goods_cache = {}
                goods_cache["barcode"] = WeighGoodsNumCache_Open_layer_2_org[i]["goodsid"]
                goods_cache["num"] = [WeighGoodsNumCache_Open_layer_2_org[i]["goodsnum"],
                                      WeighGoodsNumCache_Open_layer_2_org[i]["isabngds"]]
                self.WeighGoodsNumCache_Open_layer_2.append(goods_cache)
        if WeighGoodsNumCache_Open_layer_3_org:
            for i in range(len(WeighGoodsNumCache_Open_layer_3_org)):
                goods_cache = {}
                goods_cache["barcode"] = WeighGoodsNumCache_Open_layer_3_org[i]["goodsid"]
                goods_cache["num"] = [WeighGoodsNumCache_Open_layer_3_org[i]["goodsnum"],
                                      WeighGoodsNumCache_Open_layer_3_org[i]["isabngds"]]
                self.WeighGoodsNumCache_Open_layer_3.append(goods_cache)
        if WeighGoodsNumCache_Open_layer_4_org:
            for i in range(len(WeighGoodsNumCache_Open_layer_4_org)):
                goods_cache = {}
                goods_cache["barcode"] = WeighGoodsNumCache_Open_layer_4_org[i]["goodsid"]
                goods_cache["num"] = [WeighGoodsNumCache_Open_layer_4_org[i]["goodsnum"],
                                      WeighGoodsNumCache_Open_layer_4_org[i]["isabngds"]]
                self.WeighGoodsNumCache_Open_layer_4.append(goods_cache)
        if WeighGoodsNumCache_Close_layer_1_org:
            for i in range(len(WeighGoodsNumCache_Close_layer_1_org)):
                goods_cache = {}
                goods_cache["barcode"] = WeighGoodsNumCache_Close_layer_1_org[i]["goodsid"]
                goods_cache["num"] = [WeighGoodsNumCache_Close_layer_1_org[i]["goodsnum"],
                                      WeighGoodsNumCache_Close_layer_1_org[i]["isabngds"]]
                self.WeighGoodsNumCache_Close_layer_1.append(goods_cache)
        if WeighGoodsNumCache_Close_layer_2_org:
            for i in range(len(WeighGoodsNumCache_Close_layer_2_org)):
                goods_cache = {}
                goods_cache["barcode"] = WeighGoodsNumCache_Close_layer_2_org[i]["goodsid"]
                goods_cache["num"] = [WeighGoodsNumCache_Close_layer_2_org[i]["goodsnum"],
                                      WeighGoodsNumCache_Close_layer_2_org[i]["isabngds"]]
                self.WeighGoodsNumCache_Close_layer_2.append(goods_cache)
        if WeighGoodsNumCache_Close_layer_3_org:
            for i in range(len(WeighGoodsNumCache_Close_layer_3_org)):
                goods_cache = {}
                goods_cache["barcode"] = WeighGoodsNumCache_Close_layer_3_org[i]["goodsid"]
                goods_cache["num"] = [WeighGoodsNumCache_Close_layer_3_org[i]["goodsnum"],
                                      WeighGoodsNumCache_Close_layer_3_org[i]["isabngds"]]
                self.WeighGoodsNumCache_Close_layer_3.append(goods_cache)
        if WeighGoodsNumCache_Close_layer_4_org:
            for i in range(len(WeighGoodsNumCache_Close_layer_4_org)):
                goods_cache = {}
                goods_cache["barcode"] = WeighGoodsNumCache_Close_layer_4_org[i]["goodsid"]
                goods_cache["num"] = [WeighGoodsNumCache_Close_layer_4_org[i]["goodsnum"],
                                      WeighGoodsNumCache_Close_layer_4_org[i]["isabngds"]]
                self.WeighGoodsNumCache_Close_layer_4.append(goods_cache)
        if self.WeighGoodsNumCache_Open_layer_1:
            self.WeighGoodsNumCache_Open_layer_1 = self.barcode_change_goods_name(
                self.WeighGoodsNumCache_Open_layer_1, self.goods_info_date)
        if self.WeighGoodsNumCache_Open_layer_2:
            self.WeighGoodsNumCache_Open_layer_2 = self.barcode_change_goods_name(
                self.WeighGoodsNumCache_Open_layer_2, self.goods_info_date)
        if self.WeighGoodsNumCache_Open_layer_3:
            self.WeighGoodsNumCache_Open_layer_3 = self.barcode_change_goods_name(
                self.WeighGoodsNumCache_Open_layer_3, self.goods_info_date)
        if self.WeighGoodsNumCache_Open_layer_4:
            self.WeighGoodsNumCache_Open_layer_4 = self.barcode_change_goods_name(
                self.WeighGoodsNumCache_Open_layer_4, self.goods_info_date)
        if self.WeighGoodsNumCache_Close_layer_1:
            self.WeighGoodsNumCache_Close_layer_1 = self.barcode_change_goods_name(
                self.WeighGoodsNumCache_Close_layer_1, self.goods_info_date)
        if self.WeighGoodsNumCache_Close_layer_2:
            self.WeighGoodsNumCache_Close_layer_2 = self.barcode_change_goods_name(
                self.WeighGoodsNumCache_Close_layer_2, self.goods_info_date)
        if self.WeighGoodsNumCache_Close_layer_3:
            self.WeighGoodsNumCache_Close_layer_3 = self.barcode_change_goods_name(
                self.WeighGoodsNumCache_Close_layer_3, self.goods_info_date)
        if self.WeighGoodsNumCache_Close_layer_4:
            self.WeighGoodsNumCache_Close_layer_4 = self.barcode_change_goods_name(
                self.WeighGoodsNumCache_Close_layer_4, self.goods_info_date)

    #格式转换
    def display_trans(self,org_change_goods):
        org_change_goods_list=[]
        if org_change_goods:
            try:
                for value, key in org_change_goods.items():
                    change_result = value + ":" + str(key)
                    org_change_goods_list.append(change_result)
                    #self.value_change_goods_layer_1.SetString(change_row, change_result)
                    # globals()["value_change_goods_layer_"+str(layer)].SetString(change_row, change_result)
                    # self.operator_muen_panel.Refresh()
            except:
                pass
            return org_change_goods_list
        else:
            return org_change_goods_list
    #列表转字典
    def list_to_dic(self,org_list):
        try:
            change_to_dict = {}
            for i in range(len(org_list)):
                change_to_dict[org_list[i][0]] = org_list[i][1]
            return change_to_dict
        except:
            return "Null"
    #图片检查商品重量变化
    def calc_goods(self,open_goods_org, close_goods_org):
        try :
            open_goods=open_goods_org.copy()
            close_goods=close_goods_org.copy()
            change_goods_dict = {}
            for i in range(len(open_goods)):
                del_all = True
                for j in range(len(close_goods)):
                    if open_goods[i][0] == close_goods[j][0]:
                        del_all = False
                        goods_change_num = (int(close_goods[j][1]) - int(open_goods[i][1]))
                        if goods_change_num == 0:
                            del close_goods[j]
                            break
                        else:
                            change_goods_dict[open_goods[i][0]] = int(goods_change_num)
                            del close_goods[j]
                            break
                if del_all:
                    change_goods_dict[open_goods[i][0]] = -int(open_goods[i][1])
            for z in range(len(close_goods)):
                change_goods_dict[close_goods[z][0]] = int(close_goods[z][1])
            return change_goods_dict
        except:
            return "null"
    #Goods_Num_cache barcode转换名字
    def barcode_change_goods_name(self,org_barcode_list,org_date):
        barcode_change_name=[]
        for i in range(len(org_barcode_list)):
            barcode_change_name_sub = {}
            for j in range(len(org_date)):
                if org_barcode_list[i]["barcode"]==org_date[j]["barcode"]:
                    barcode_change_name_sub["name"]=org_date[j]["name"]
                    barcode_change_name_sub["num"]=org_barcode_list[i]["num"]
                    break
                else:
                    barcode_change_name_sub["name"]=org_barcode_list[i]["barcode"]
                    barcode_change_name_sub["num"]=org_barcode_list[i]["num"]
            barcode_change_name.append(barcode_change_name_sub)
        return barcode_change_name
    #根据barcode查找商品名字
    def goods_name_lock(self,org_dict, org_date):
        try:
            change_goods_name = {}
            for key, value in org_dict.items():
                for i in range(len(org_date)):
                    if org_date[i]["barcode"] == key:
                        change_goods_name[org_date[i]["name"]] = value
                        break
            return change_goods_name
        except:
            return "null"
    #AS 重量变化计算
    def change_weigh_as(self,org_list,org_date):
        try:
            change_weight_min = change_weight_max = 0
            for i in range(len(org_list)):
                key=org_list[i][0]
                change_status=org_list[i][3]
                change_num=org_list[i][2]
                for j in range(len(org_date)):
                    if org_date[j]["barcode"] == key:
                        goods_weight = int(org_date[j]["weight"])
                        goods_weight_drift = int(org_date[j]["weight_drift"]) + 5
                        if change_status=="2":
                            goods_weight_min=int(change_num) * (goods_weight - goods_weight_drift)
                            goods_weight_max=int(change_num)* (goods_weight + goods_weight_drift)
                        elif change_status=="4":
                            goods_weight_min = -int(change_num) * (goods_weight + goods_weight_drift)
                            goods_weight_max = -int(change_num) * (goods_weight - goods_weight_drift)
                        change_weight_min = change_weight_min + goods_weight_min
                        change_weight_max = change_weight_max + goods_weight_max
                        break
            return change_weight_min, change_weight_max
        except:
            return "null"
    # CM 重量变化计算
    def change_weight(self,org_dict, org_date):
        try:
            change_weight_min = change_weight_max = 0
            for key, value in org_dict.items():
                for i in range(len(org_date)):
                    if org_date[i]["barcode"] == key:
                        goods_weight = int(org_date[i]["weight"])
                        goods_weight_drift = int(org_date[i]["weight_drift"]) + 5
                        if value > 0:
                            goods_weight_min = -value * (goods_weight + goods_weight_drift)
                            goods_weight_max = -value * (goods_weight - goods_weight_drift)
                        if value < 0:
                            goods_weight_min = -value * (goods_weight - goods_weight_drift)
                            goods_weight_max = -value * (goods_weight + goods_weight_drift)
                        change_weight_min = change_weight_min + goods_weight_min
                        change_weight_max = change_weight_max + goods_weight_max
                        break
            return change_weight_min, change_weight_max
        except:
            return "null"
    #返回首页
    def back(self,evt):
        self.pic_detail_panel.Hide()
        self.operator_muen_panel.Show()
        self.init_panel.Show()
    # 退出提示
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
    #测试和生产环境url
    def DEV_URL(self, evt):
        index = evt.GetEventObject().GetSelection()
        if (index == 0):
            self.select_url=True
            self.url = "http://10.4.32.114:8085/rrpc"
            self.web_login_url = "http://218.108.7.116:8080/login"
            self.web_query_goods_url = "http://218.108.7.116:8080/post_common_admin/"
            self.web_login_Referer = "http://218.108.7.116:8080/g/utstarcom"
            self.web_query_goods_Referer = "http://218.108.7.116:8080/main"
            self.web_query_dev_url = "http://218.108.7.116:8500/api/query_dev"
            self.web_Referer="http://218.108.7.116:8500/main"
            self.web_login_dev_url = "http://218.108.7.116:8500/login"
        elif (index == 1):
            self.select_url=True
            self.url = "http://w.vegcloud.xyz:8085/rrpc"
            self.web_login_url = "https://gosmart.ustar-ai.com/login"
            self.web_query_goods_url = "https://gosmart.ustar-ai.com/post_common_admin/"
            self.web_query_goods_Referer = "https://gosmart.ustar-ai.com"
            self.web_login_Referer = "https://gosmart.ustar-ai.com/g/utstarcom"
            self.web_query_dev_url = "http://gosmart.ustar-ai.com:8500/api/query_dev"
            self.web_Referer="http://gosmart.ustar-ai.com:8500/main/"
            self.web_login_dev_url = "http://gosmart.ustar-ai.com:8500/login"

class toolapp(wx.App):
    def OnInit(self):
        self.frame = ToolsWindow(None, '图像log过滤')
        self.frame.Show(True)
        return True

if __name__ == "__main__":
    app = toolapp(0)
    app.MainLoop()

