import re
import time
import wx
import threading
import serial
import serial.tools.list_ports
import sys
import os


class ToolsWindow(wx.Frame):
    def __init__(self, parent, title):
        try:
            port_list = serial.tools.list_ports.comports()
            com_list = []
            for i in range(len(port_list)):
                com_list_org = re.search("(COM\d+)", str(port_list[i]))
                if com_list_org:
                    com_list.append(com_list_org.group())
        except:
            com_list = []
        wx.Frame.__init__(self, parent, title=title, size=(800, 500),style=wx.CAPTION | wx.CLOSE_BOX | wx.MINIMIZE_BOX)
        self.init_panel = wx.Panel(self, -1)
        self.SetBackgroundColour("#00F5FF")
        #self.init_panel.SetBackgroundColour("#8F8FBC")
        #image_file="D:\python script\goGrid_back.jpg"
        self.init_panel.Bind(wx.EVT_ERASE_BACKGROUND,self.oneraseback)
        #to_bmp_image=wx.Image(image_file,wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        #self.back_image=wx.StaticBitmap(self.)
        self.font_init = wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.LIGHT)
        self.title_tool=wx.StaticText(self.init_panel,1,"goGrid 硬件测试工具",size=(400,50),style=wx.ALIGN_CENTER)
        self.title_font=wx.Font(20, wx.DECORATIVE, wx.NORMAL, wx.LIGHT)
        self.title_tool.SetForegroundColour("Red")
        self.title_tool.SetFont(self.title_font)
        #self.title_box=wx.StaticBox(self.init_panel,-1,"",size=(400,50),style=wx.ALIGN_CENTER)
        #self.title_sizer=wx.StaticBoxSizer(self.title_box,wx.HORIZONTAL)
        #self.title_sizer.Add(self.title_tool,0,wx.ALL|wx.ALIGN_CENTER_HORIZONTAL,2)
        self.index_com=wx.StaticText(self.init_panel,-1,"COM口")
        self.index_com.SetFont(self.font_init)
        self.value_com=wx.ComboBox(self.init_panel,-1,choices=com_list,size=(100,0))
        self.value_com.SetFont(self.font_init)
        self.index_speed=wx.StaticText(self.init_panel,-1,"速率")
        self.index_speed.SetFont(self.font_init)
        self.value_speed=wx.TextCtrl(self.init_panel,-1,"115200")
        self.value_speed.SetFont(self.font_init)
        self.conf_com = wx.StaticBox(self.init_panel, -1, '串口配置信息',size=(400,50),style=wx.ALIGN_CENTER)
        self.conf_com_sizer=wx.StaticBoxSizer(self.conf_com,wx.HORIZONTAL)
        self.conf_com_sizer.Add(self.index_com,0,wx.ALL|wx.ALIGN_CENTER_HORIZONTAL,2)
        self.conf_com_sizer.Add(self.value_com, 0, wx.ALL |wx.ALIGN_CENTER_HORIZONTAL, 2)
        self.conf_com_sizer.Add(self.index_speed, 0, wx.ALL |wx.ALIGN_CENTER_HORIZONTAL, 2)
        self.conf_com_sizer.Add(self.value_speed, 0, wx.ALL |wx.ALIGN_CENTER_HORIZONTAL, 2)
        self.row_index=wx.StaticText(self.init_panel,-1,"行数")
        self.row_index.SetFont(self.font_init)
        self.row_value=wx.TextCtrl(self.init_panel,-1,"")
        self.row_value.SetFont(self.font_init)
        self.col_index=wx.StaticText(self.init_panel,-1,"列数")
        self.col_index.SetFont(self.font_init)
        self.col_value=wx.TextCtrl(self.init_panel,-1,"")
        self.col_value.SetFont(self.font_init)
        self.conf_dev=wx.StaticBox(self.init_panel,-1,"设备规格",size=(400,50),style=wx.ALIGN_CENTER)
        self.conf_dev_sizer=wx.StaticBoxSizer(self.conf_dev,wx.HORIZONTAL)
        self.conf_dev_sizer.Add(self.row_index,0,wx.ALL|wx.ALIGN_CENTER_HORIZONTAL,2)
        self.conf_dev_sizer.Add(self.row_value, 0, wx.ALL |wx.ALIGN_CENTER_HORIZONTAL, 2)
        self.conf_dev_sizer.Add(self.col_index,0,wx.ALL|wx.ALIGN_CENTER_HORIZONTAL,2)
        self.conf_dev_sizer.Add(self.col_value, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 2)
        self.enter_button=wx.Button(self.init_panel,-1,"开始",size=(400,50))
        self.enter_button.SetFont(self.font_init)
        self.enter_button.SetBackgroundColour("Green")
        self.Bind(wx.EVT_BUTTON,self.start_test,self.enter_button)
        init_v_box=wx.BoxSizer(wx.VERTICAL)
        init_v_box.Add(self.title_tool,0,wx.ALL|wx.ALIGN_CENTER_VERTICAL |wx.ALIGN_CENTER_HORIZONTAL,1)
        init_v_box.Add(self.conf_com_sizer,0,wx.ALL|wx.ALIGN_CENTER_VERTICAL |wx.ALIGN_CENTER_HORIZONTAL,1)
        init_v_box.Add(self.conf_dev_sizer, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL |wx.ALIGN_CENTER_HORIZONTAL, 1)
        init_v_box.Add(self.enter_button, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL |wx.ALIGN_CENTER_HORIZONTAL, 1)
        self.init_panel.SetSizer(init_v_box)
        self.init_panel.Layout()
        self.init_panel.Fit()
        self.system_dlg = wx.MessageDialog(self.init_panel, "", caption="操作提示", style=wx.OK)
        self.system_dlg.SetFont(self.font_init)
        self.system_dlg.SetForegroundColour("Red")
    def oneraseback(self,evt):
        dc = evt.GetDC()
        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)
        dc.Clear()
        bmp = wx.Bitmap(self.resouce_path("C:\\Users\zhangbikang\AppData\Local\Programs\Python\Python37\Scripts\goGrid_back.jpg"))
        dc.DrawBitmap(bmp, 0, 0)
    def resouce_path(self,relateve_path):
        if hasattr(sys,"_MEIPASS"):
            self.base_path=sys._MEIPASS
        else:
            self.base_path=os.path.abspath(".")
        return os.path.join(self.base_path,relateve_path)

    #测试内容选项
    def start_test(self,evt):
        self.enter_button.Disable()
        self.dev_row=self.row_value.GetValue()
        self.dev_col=self.col_value.GetValue()
        self.com_number=self.value_com.GetValue()
        self.speed=self.value_speed.GetValue()
        com_type=re.findall("COM",self.com_number)
        self.enter_button.Disable()
        if self.com_number=="":
            self.system_dlg.SetMessage("请输入串口号")
            self.system_dlg.ShowModal()
            self.enter_button.Enable()
            return
        elif not com_type:
            self.system_dlg.SetMessage("串口格式不正确")
            self.system_dlg.ShowModal()
            self.enter_button.Enable()
            return
        if self.dev_col=="" or self.dev_row=="":
            self.system_dlg.SetMessage("请输入设备行列号")
            self.system_dlg.ShowModal()
            self.enter_button.Enable()
            return
        elif not self.dev_row.isdigit():
            self.system_dlg.SetMessage("行列号格式不正确")
            self.system_dlg.ShowModal()
            self.enter_button.Enable()
            return
        elif not self.dev_col.isdigit():
            self.system_dlg.SetMessage("行列号格式不正确")
            self.system_dlg.ShowModal()
            self.enter_button.Enable()
            return
        try:
            self.serial_com = serial.Serial(self.com_number, int(self.speed), timeout=2)
            self.serial_com.close()
            time.sleep(1)
            self.serial_com.open()
            time.sleep(1)
            self.enter_button.Enable()
        except Exception as e:
            self.system_dlg.SetMessage(str(e))
            self.system_dlg.ShowModal()
            self.enter_button.Enable()
            return
        self.init_panel.Hide()
        self.operation_panel=wx.Panel(self, -1, pos=(0, 0), size=(800, 500))
        font=wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.LIGHT)
        test_but=wx.Button(self.operation_panel,-1,"检测",pos=(300,175),size=(200,50))
        test_but.SetFont(font)
        test_but.SetBackgroundColour("#B3EE3A")
        weight_test_but=wx.Button(self.operation_panel,-1,"秤盘标定",pos=(300,225),size=(200,50))
        weight_test_but.SetFont(font)
        weight_test_but.SetBackgroundColour("#B3EE3A")
        back_int=wx.Button(self.operation_panel,-1,"返回",pos=(300,275),size=(200,50))
        back_int.SetFont(font)
        back_int.SetBackgroundColour("#B3EE3A")
        self.Bind(wx.EVT_BUTTON,self.test_process,test_but)
        self.Bind(wx.EVT_BUTTON,self.weight_test_process,weight_test_but)
        self.Bind(wx.EVT_BUTTON,self.back_to_int,back_int)
    # 门锁灯检测界面
    def test_process(self,evt):
        self.operation_panel.Hide()
        self.test_panel=wx.ScrolledWindow(self, -1, pos=(0, 0), size=(800, 500))
        self.test_panel.SetScrollbar(1,1,1000,2000)
        self.test_panel.SetScrollRate(10,10)
        self.test_panel.SetBackgroundColour("#00F5FF")
        full_cover_test=wx.Button(self.test_panel,-1,"一键检测")
        full_cover_test.SetFont(self.font_init)
        open_door=wx.Button(self.test_panel,-1,"一键开门")
        open_door.SetFont(self.font_init)
        close_door=wx.Button(self.test_panel,-1,"一键关门")
        close_door.SetFont(self.font_init)
        open_light=wx.Button(self.test_panel,-1,"一键开灯")
        open_light.SetFont(self.font_init)
        close_light=wx.Button(self.test_panel,-1,"一键关灯")
        close_light.SetFont(self.font_init)
        open_door.Bind(wx.EVT_BUTTON, self.open_close_door_light_all)
        close_door.Bind(wx.EVT_BUTTON, self.open_close_door_light_all)
        open_light.Bind(wx.EVT_BUTTON,self.open_close_door_light_all)
        close_light.Bind(wx.EVT_BUTTON,self.open_close_door_light_all)
        title_box=wx.StaticBox(self.test_panel,-1,"")
        title_box_sizer=wx.StaticBoxSizer(title_box,wx.HORIZONTAL)
        title_box_sizer.Add(full_cover_test,0,wx.ALIGN_CENTER_HORIZONTAL|wx.ALL)
        title_box_sizer.Add(open_door, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL)
        title_box_sizer.Add(close_door, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL)
        title_box_sizer.Add(open_light, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL)
        title_box_sizer.Add(close_light, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL)
        self.Bind(wx.EVT_BUTTON,self.full_cover_test_process,full_cover_test)
        gogrid_sizer=wx.GridSizer(int(self.dev_row)+1,int(self.dev_col),2,2)
        gride_index_names=globals()
        self.test_but_key={}
        for i in range(0,int(self.dev_row)+1):
            for j in range(1,int(self.dev_col)+1):
                lable_name="CH" + str(j) + str(i)
                ch_num = "CH" + str(j) + str(i)
                if i==0:
                    lable_name=lable_name+"only light"
                gride_index_names[ch_num]=wx.ToggleButton(self.test_panel,-1,lable_name,size=(150,50))
                gride_index_names[ch_num].SetBackgroundColour("Red")
                gride_index_names[ch_num].SetFont(self.font_init)
                self.test_but_key[gride_index_names[ch_num].GetId()]=ch_num
                gride_index_names[ch_num].Bind(wx.EVT_TOGGLEBUTTON,self.door_light_single_test)
                gogrid_sizer.Add(gride_index_names[ch_num],0)
        back_but=wx.Button(self.test_panel,-1,"返回")
        back_but.SetFont(self.font_init)
        self.Bind(wx.EVT_BUTTON,self.lock_back_select,back_but)
        v_box=wx.BoxSizer(wx.VERTICAL)
        v_box.Add(title_box_sizer,0,wx.ALL|wx.ALIGN_CENTER_HORIZONTAL)
        v_box.Add(gogrid_sizer, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL)
        v_box.Add(back_but, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL)
        self.test_panel.SetSizer(v_box)
        self.test_panel.Layout()
        self.test_panel.Fit()
    #秤盘检查界面
    def weight_test_process(self,evt):
        self.operation_panel.Hide()
        self.weight_panel = wx.ScrolledWindow(self, -1, pos=(0, 0), size=(800, 500))
        self.weight_panel.SetScrollbar(1, 1, 1000, 2000)
        self.weight_panel.SetScrollRate(10, 10)
        self.weight_panel.SetBackgroundColour("#00F5FF")
        full_clear=wx.Button(self.weight_panel,-1,"一键清零")
        full_clear.SetFont(self.font_init)
        full_query=wx.Button(self.weight_panel,-1,"一键查询重量")
        full_query.SetFont(self.font_init)
        open_door=wx.Button(self.weight_panel,-1,"一键开门")
        open_door.SetFont(self.font_init)
        close_door=wx.Button(self.weight_panel,-1,"一键关门")
        close_door.SetFont(self.font_init)
        title_box=wx.StaticBox(self.weight_panel,-1,"")
        self.Bind(wx.EVT_BUTTON,self.full_clear_weight,full_clear)
        self.Bind(wx.EVT_BUTTON, self.full_query_weight, full_query)
        open_door.Bind(wx.EVT_BUTTON,self.open_close_door_light_all)
        close_door.Bind(wx.EVT_BUTTON,self.open_close_door_light_all)
        title_box_sizer=wx.StaticBoxSizer(title_box,wx.HORIZONTAL)
        title_box_sizer.Add(full_clear,0,wx.ALIGN_CENTER_HORIZONTAL|wx.ALL)
        title_box_sizer.Add(full_query, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL)
        title_box_sizer.Add(open_door, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL)
        title_box_sizer.Add(close_door, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL)
        gogrid_sizer=wx.GridSizer(int(self.dev_row),int(self.dev_col),2,2)
        gride_index_names=globals()
        self.weight_but_key={}
        for i in range(1,int(self.dev_row)+1):
            for j in range(1,int(self.dev_col)+1):
                lable_name="第"+str(i)+"行 "+"第"+str(j)+"列"
                ch_num = "CH" + str(j) + str(i)
                gride_index_names[ch_num]=wx.ToggleButton(self.weight_panel,-1,ch_num,size=(150,50))
                gride_index_names[ch_num].SetBackgroundColour("Red")
                gride_index_names[ch_num].SetFont(self.font_init)
                self.weight_but_key[gride_index_names[ch_num].GetId()]=ch_num
                gride_index_names[ch_num].Bind(wx.EVT_TOGGLEBUTTON, self.calib_weight)
                gogrid_sizer.Add(gride_index_names[ch_num],0)
        back_but=wx.Button(self.weight_panel,-1,"返回")
        back_but.SetFont(self.font_init)
        self.Bind(wx.EVT_BUTTON,self.weight_back_select,back_but)
        v_box=wx.BoxSizer(wx.VERTICAL)
        v_box.Add(title_box_sizer,0,wx.ALL|wx.ALIGN_CENTER_HORIZONTAL)
        v_box.Add(gogrid_sizer, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL)
        v_box.Add(back_but, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL)
        self.weight_panel.SetSizer(v_box)
        self.weight_panel.Layout()
        self.weight_panel.Fit()
    #门锁灯检测
    def full_cover_test_process(self,evt):
        for i in range(0,int(self.dev_row)+1):
            for j in range(1,int(self.dev_col)+1):
                ch_num = "CH" + str(j) + str(i)
                globals()[ch_num].Disable()
        lock_test_t=threading.Thread(target=self.door_light_all_cover)
        lock_test_t.start()
    def door_light_all_cover(self):
        try:
            for i in range(0, int(self.dev_row) + 1):
                for j in range(1, int(self.dev_col) + 1):
                    ch_num = "CH" + str(j) + str(i)
                    if i!=0:
                        door_rel,door_status=self.door_run_process(ch_num)
                        time.sleep(0.5)
                    else:
                        door_rel="Pass"
                    light_rel,light_status=self.light_run_process(ch_num)
                    time.sleep(0.5)
                    if door_rel=="Pass" and light_rel=="Pass":
                        globals()[ch_num].SetLabel("Pass")
                        globals()[ch_num].SetBackgroundColour("Green")
                        globals()[ch_num].Enable()
                    elif door_rel =="Fail":
                        globals()[ch_num].SetLabel("Door Fail")
                        globals()[ch_num].SetBackgroundColour("Red")
                        globals()[ch_num].Enable()
                    elif light_rel=="Fail":
                        globals()[ch_num].SetLabel("Light Fail")
                        globals()[ch_num].SetBackgroundColour("Red")
                        globals()[ch_num].Enable()
        except Exception as e:
            for i in range(0, int(self.dev_row) + 1):
                for j in range(1, int(self.dev_col) + 1):
                    ch_num = "CH" + str(j) + str(i)
                    globals()[ch_num].Enable()
            self.system_dlg.SetMessage(str(e))
            self.system_dlg.ShowModal()
    #秤盘清零
    def full_clear_weight(self,evt):
        for i in range(1,int(self.dev_row)+1):
            for j in range(1,int(self.dev_col)+1):
                ch_num = "CH" + str(j) + str(i)
                globals()[ch_num].Disable()
        full_clear_t=threading.Thread(target=self.full_clear_process)
        full_clear_t.start()
    def full_clear_process(self):
        try:
            for i in range(1, int(self.dev_row) + 1):
                for j in range(1, int(self.dev_col) + 1):
                    ch_num = "CH" + str(j) + str(i)
                    clear_rel, clear_status = self.operater_serial(self.serial_com, ch_num, "clear", "set")
                    if clear_rel == "Pass":
                        query_rel, query_status = self.get_weight_process(ch_num)
                        if query_rel == "Pass":
                            globals()[ch_num].SetLabel(str(query_status))
                            globals()[ch_num].SetBackgroundColour("Green")
                            globals()[ch_num].Enable()
                        elif query_rel == "Fail":
                            globals()[ch_num].SetLabel(str(query_status))
                            globals()[ch_num].SetBackgroundColour("Red")
                            globals()[ch_num].Enable()
                    elif clear_rel == "Fail":
                        globals()[ch_num].SetLabel("Clear Fail")
                        globals()[ch_num].SetBackgroundColour("Red")
                        globals()[ch_num].Enable()
        except Exception as e:
            for i in range(1, int(self.dev_row) + 1):
                for j in range(1, int(self.dev_col) + 1):
                    ch_num = "CH" + str(j) + str(i)
                    globals()[ch_num].Enable()
            self.system_dlg.SetMessage(str(e))
            self.system_dlg.ShowModal()
    #秤盘读取重量
    def full_query_weight(self,evt):
        for i in range(1, int(self.dev_row) + 1):
            for j in range(1, int(self.dev_col) + 1):
                ch_num = "CH" + str(j) + str(i)
                globals()[ch_num].Disable()
        full_query_t = threading.Thread(target=self.full_weight_process)
        full_query_t.start()
    def full_weight_process(self):
        try:
            for i in range(1, int(self.dev_row) + 1):
                for j in range(1, int(self.dev_col) + 1):
                    ch_num = "CH" + str(j) + str(i)
                    query_rel, query_status = self.get_weight_process(ch_num)
                    if query_rel=="Pass":
                        globals()[ch_num].SetLabel(str(query_status))
                        globals()[ch_num].SetBackgroundColour("Green")
                        globals()[ch_num].Enable()
                    elif query_rel=="Fail":
                        globals()[ch_num].SetLabel(str(query_status))
                        globals()[ch_num].SetBackgroundColour("Red")
                        globals()[ch_num].Enable()
        except Exception as e:
            for i in range(1, int(self.dev_row) + 1):
                for j in range(1, int(self.dev_col) + 1):
                    ch_num = "CH" + str(j) + str(i)
                    globals()[ch_num].Enable()
            self.system_dlg.SetMessage(str(e))
            self.system_dlg.ShowModal()
    #灯门锁单个测试
    def door_light_single_test(self,evt):
        cur_ch_num = self.test_but_key[evt.GetEventObject().GetId()]
        for i in range(0,int(self.dev_row)+1):
            for j in range(1,int(self.dev_col)+1):
                ch_num = "CH" + str(j) + str(i)
                globals()[ch_num].Disable()
        sub_t=threading.Thread(target=self.door_light_single_test_process,args=(cur_ch_num,))
        sub_t.start()
        #print(evt.GetEventObject().GetValue())
        #print(evt.GetEventObject().GetLabel())
    def door_light_single_test_process(self,ch_num):
        try:
            only_light=False
            for i in range(1,int(self.col_value.GetValue())+1):
                light_ch_num="CH"+str(i)+"0"
                if light_ch_num==ch_num:
                    only_light=True
                    break
            if not only_light:
                door_rel, door_status = self.door_run_process(ch_num)
            else:
                door_rel="Pass"
            light_rel, light_status = self.light_run_process(ch_num)
            if door_rel == "Pass" and light_rel == "Pass":
                globals()[ch_num].SetLabel("Pass")
                globals()[ch_num].SetBackgroundColour("Green")
                globals()[ch_num].Enable()
            elif door_rel == "Fail":
                globals()[ch_num].SetLabel("Door fail")
                globals()[ch_num].SetBackgroundColour("Red")
                globals()[ch_num].Enable()
            elif light_rel == "Fail":
                globals()[ch_num].SetLabel("Light fail")
                globals()[ch_num].SetBackgroundColour("Red")
                globals()[ch_num].Enable()
            for i in range(0, int(self.dev_row) + 1):
                for j in range(1, int(self.dev_col) + 1):
                    ch_num = "CH" + str(j) + str(i)
                    globals()[ch_num].Enable()
        except Exception as e:
            globals()[ch_num].Enable()
            self.system_dlg.SetMessage(str(e))
            self.system_dlg.ShowModal()
            for i in range(0, int(self.dev_row) + 1):
                for j in range(1, int(self.dev_col) + 1):
                    ch_num = "CH" + str(j) + str(i)
                    globals()[ch_num].Enable()
    #标定
    def calib_weight(self,evt):
        for i in range(1,int(self.dev_row)+1):
            for j in range(1,int(self.dev_col)+1):
                ch_num = "CH" + str(j) + str(i)
                globals()[ch_num].Disable()
        ch_num = self.weight_but_key[evt.GetEventObject().GetId()]
        sub_t=threading.Thread(target=self.calib_weight_process,args=(ch_num,))
        sub_t.start()
    def calib_weight_process(self,ch_num):
        try:
            clear_rel,clear_status=self.operater_serial(self.serial_com,ch_num,"clear","set")
            if clear_rel=="Pass":
                self.system_dlg.SetMessage("清零成功，放入5KG 砝码后点击确定")
                self.system_dlg.ShowModal()
                calib_rel,calib_status=self.operater_serial(self.serial_com,ch_num,"calib","set")
                if calib_rel=="Pass":
                    query_rel,query_status=self.get_weight_process(ch_num)
                    if query_rel=="Pass":
                        globals()[ch_num].SetLabel(str(query_status))
                        globals()[ch_num].SetBackgroundColour("Green")
                        globals()[ch_num].Enable()
                    else:
                        globals()[ch_num].SetLabel("查询重量失败")
                        globals()[ch_num].SetBackgroundColour("Red")
                        globals()[ch_num].Enable()
                else:
                    globals()[ch_num].SetLabel("标定失败")
                    globals()[ch_num].SetBackgroundColour("Red")
                    globals()[ch_num].Enable()
            else:
                globals()[ch_num].SetLabel("清零失败")
                globals()[ch_num].SetBackgroundColour("Red")
                globals()[ch_num].Enable()
            for i in range(1, int(self.dev_row) + 1):
                for j in range(1, int(self.dev_col) + 1):
                    ch_num = "CH" + str(j) + str(i)
                    globals()[ch_num].Enable()
        except Exception as e:
            globals()[ch_num].Enable()
            self.system_dlg.SetMessage(str(e))
            self.system_dlg.ShowModal()
            for i in range(0, int(self.dev_row) + 1):
                for j in range(1, int(self.dev_col) + 1):
                    ch_num = "CH" + str(j) + str(i)
                    globals()[ch_num].Enable()


    def operater_serial(self,serial_com,ch_number,cmd,operation_type):
        org_date = "+" + ch_number + ":" + cmd + ":\n"
        date_byte = org_date.encode("utf-8")
        serial_com.write(date_byte)
        rel_org = serial_com.read(30).decode()
        rel=rel_org.strip()
        cmp_cmd = ch_number + ":" + cmd
        if operation_type=="set":
            if rel == cmp_cmd:
                return "Pass", rel
            else:
                return "Fail", rel
        elif operation_type=="get":
            result_filter=re.compile(cmp_cmd+"(.+)")
            respons_status=re.findall(result_filter,rel)
            if respons_status:
                return "Pass",respons_status[0]
            else:
                return "Fail","Get Fail"
    def door_run_process(self,ch_num):
        door_test_result=True
        operation_list = ["opendoor", "closedoor"]
        query_list = ["OPEN", "CLOSE"]
        for z in range(len(operation_list)):
            set_rel, set_status = self.operater_serial(self.serial_com, ch_num, operation_list[z], "set")
            if set_rel == "Pass":
                get_rel, get_status = self.operater_serial(self.serial_com, ch_num, "getlock", "get")
                if get_rel == "Pass":
                    query_parament = query_list[z]
                    status_org = re.search((query_parament) + "$", get_status)
                    if status_org:
                        status = status_org.group()
                        if status != query_list[z]:
                            return "Fail",status
                else:
                    return "Fail",get_status
            else:
                return "Fail",set_status
        return "Pass","lock is ok"
    def light_run_process(self,ch_num):
        operation_list = ["closeluminary", "openluminary"]
        for z in range(len(operation_list)):
            set_rel, set_status = self.operater_serial(self.serial_com, ch_num, operation_list[z], "set")
            if set_rel == "Fail":
                return "Fail",set_status
        return "Pass","light is ok"
    def lock_back_select(self,evt):
        self.test_panel.Hide()
        self.operation_panel.Show()
    def weight_back_select(self,evt):
        self.weight_panel.Hide()
        self.operation_panel.Show()
    def back_to_int(self,evt):
        self.operation_panel.Hide()
        self.init_panel.Show()
        self.serial_com.close()
    def get_weight_process(self,ch_num):
        try:
            query_rel, query_status = self.operater_serial(self.serial_com, ch_num, "getw", "get")
            if query_rel == "Pass":
                weight_value = re.findall(":([+|-]\s+.+)", query_status)
                return "Pass",weight_value[0]
            elif query_rel == "Fail":
                return "Fail",query_status
        except Exception as e:
            return "Fail",e
    #一键开门
    def open_close_door_light_all(self,evt):
        door_type=evt.GetEventObject().GetLabel()
        for i in range(1,int(self.dev_row)+1):
            for j in range(1,int(self.dev_col)+1):
                ch_num = "CH" + str(j) + str(i)
                globals()[ch_num].Disable()
        if door_type=="一键开门":
            open_door_t=threading.Thread(target=self.open_close_door_light_all_process,args=("opendoor",))
            open_door_t.start()
        elif door_type=="一键关门":
            close_door_t = threading.Thread(target=self.open_close_door_light_all_process, args=("closedoor",))
            close_door_t.start()
        elif door_type=="一键开灯":
            open_light_t = threading.Thread(target=self.open_close_door_light_all_process, args=("openluminary",))
            open_light_t.start()
        elif door_type=="一键关灯":
            close_light_t = threading.Thread(target=self.open_close_door_light_all_process, args=("closeluminary",))
            close_light_t.start()
    def open_close_door_light_all_process(self,cmd):
        if cmd=="openluminary" or cmd=="closeluminary":
            row_int=0
        else:
            row_int=1
        for i in range(row_int,int(self.dev_row)+1):
            for j in range(1,int(self.dev_col)+1):
                ch_num = "CH" + str(j) + str(i)
                set_rel, set_status = self.operater_serial(self.serial_com, ch_num, cmd, "set")
                if set_rel=="Pass":
                    globals()[ch_num].Enable()
                    globals()[ch_num].SetLabel(cmd)
                    globals()[ch_num].SetBackgroundColour("Green")
                else:
                    globals()[ch_num].Enable()
                    globals()[ch_num].SetLabel(cmd +"Fail")
                    globals()[ch_num].SetBackgroundColour("Red")










class toolapp(wx.App):
    def OnInit(self):
        self.frame = ToolsWindow(None, 'goGrid_tools')
        self.frame.Show(True)
        return True


if __name__ == "__main__":
    app = toolapp(0)
    app.MainLoop()