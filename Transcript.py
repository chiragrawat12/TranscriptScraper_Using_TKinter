from tkinter import Tk,PhotoImage,Label,Frame,Button,BooleanVar,Canvas,DISABLED,NORMAL,OptionMenu,messagebox
from tkinter import IntVar,StringVar,Entry,Radiobutton,Scrollbar,filedialog,END,Text,Checkbutton
from PIL import ImageTk,Image
import tkinter.scrolledtext as scrolledtext
from os import path,environ
from threading import Thread
from api import *
from io import BytesIO
from urllib.request import urlopen
import requests
from tk_html_widgets import HTMLLabel
from get_trans import Get_Transcript
import datetime
import logging
import time
import traceback



#GUI class starts from here 
class GUI(Tk):
    def __init__(self):
        super().__init__()
        self.ws = self.winfo_screenwidth()
        self.hs = self.winfo_screenheight()
        self.height = 650
        self.width = 750
        self.x = int((self.ws/2) - (self.width/2))
        self.y = int((self.hs/2) - (self.height/2))
        self.geometry("{}x{}+{}+{}".format(self.width,self.height,self.x,self.y))
        self.update()
        self.title("Transcript Scraper")
        self.resizable(width = False,height = False)
        self.iconbitmap("Images/scraper.ico") 
        self.Choose_Text_File = ""
        self.In_Use = int()
        self.videos = []
        self.max =0
        self.key =""
        self.manual_videos_cha = []
        self.manual_videos =[]
        self.videos_url =[]
        self.Schedule_var = StringVar()
        self.Schedule_var.set("None")
        self.Use_CheckBtns_var_show_s = []
        self.Use_CheckBtns_var_show_c = []
        self.Use_CheckBtns_var = []
        self.Use_CheckBtns_var_cha = []
        self.Use_CheckBtns_var_url =[]
        self.Sort_By_var = StringVar()
        self.Sort_By_var.set("searchSortUnspecified")
        self.Video_Duration_var = StringVar()
        self.Video_Duration_var.set("videoDurationUnspecified")
        self.stp = 0
        self.rerun_videos = []
        self.cap_vi = 0
        self.skip_vi = 0
        dirname = os.path.dirname(__file__)
        Log_Format = "%(levelname)s | %(asctime)s  -  %(message)s"
        logging.basicConfig(filename=path.join(dirname,'Mains/Log_File.log'),
                    level = logging.INFO,format=Log_Format)
        self.logger = logging.getLogger()
        Create_Database()

#function to show list of videos searched by keyword/'s by clicking on manual checkbox
    def Keywords_show_manual(self):
        self.Working_on_Frame_5()   
        self.Use_CheckBtns_var = []
        self.Use_CheckBtns = []
        self.Use_f = []
        self.Use_Photo_f = []
        self.Use_Title_f = []
        self.Use_Check_f = []
        self.photo_lst = []
        if self.Choose_Text_File =="":
            keys = self.Keyword_Var.get().split(",")
        else:
            with open(self.Choose_Text_File,"r") as file:
                keys = file.read().split(',')
        k = 0
        self.manual_videos = []
        self.split_keys = []
        for j in range(len(keys)):
            self.videos = []
            try:
                self.videos = Extract_Detail_by_keyword(keys[j],self.Max_Result.get(),self.Sort_By_var.get(),self.Video_Duration_var.get())
            except:
                self.Max_Result_error_Label.config(text = "Api Quota Exceeded",fg ="red")
            for i in range(len(self.videos)):
                self.manual_videos.append(self.videos[i])
                self.split_keys.append(keys[j])
                self.f = Frame(self.second_frame,borderwidth = 4,relief = "sunken",width = 500,height = 100)
                self.Use_f.append(self.f)
                self.photo_f = Frame(self.f,borderwidth = 4,relief = "sunken",width = 150)
                self.Use_Photo_f.append(self.photo_f)
                self.title_f = Frame(self.f,borderwidth = 4,relief = "sunken",width = 270)
                self.Use_Title_f.append(self.title_f)
                self.check_f = Frame(self.f,borderwidth = 4,relief = "sunken",width = 80)
                self.Use_Check_f.append(self.check_f)

                self.Check_btn_var = IntVar()
                self.Check_btn_var.set(1)
                self.Use_CheckBtns_var.append(self.Check_btn_var)
                self.Check_btn = Checkbutton(self.check_f,variable = self.Use_CheckBtns_var[k])
                self.Check_btn.pack(side = "left")
                self.Use_CheckBtns.append(self.Check_btn)
        
                self.Use_Photo_f[k].pack(expand = 0,fill = "y",side = "left")
                self.Use_Photo_f[k].pack_propagate(0)
                self.Use_Title_f[k].pack(expand = 0,fill = "y",side = "left")
                self.Use_Title_f[k].pack_propagate(0)
                self.Use_Check_f[k].pack(expand = 0,fill = "y",side = "left")
                self.Use_Check_f[k].pack_propagate(0)
                self.Use_f[k].pack(expand = 0,fill = "both")
                self.Use_f[k].pack_propagate(0)

                self.imgurl = "{}".format(self.videos[i][2])
                self.image_data = requests.get(self.imgurl).content
                self.photo_lst.append(ImageTk.PhotoImage(Image.open(BytesIO(self.image_data)).resize((150, 100), Image.ANTIALIAS)))
                
                Label(self.Use_Photo_f[k],image = self.photo_lst[k]).pack()
        
                Label(self.Use_Title_f[k],text = "Title:{}...".format(self.videos[i][0][:35]) ,
                                                    font = ("helvetica",9,"bold"),justify = "left").pack(anchor = "nw")
                Label(self.Use_Title_f[k],text = "Description:{}...".format(self.videos[i][1][:30]),
                                                        font = ("helvetica",9),justify = "left").pack(anchor = "nw")
                Label(self.Use_Title_f[k],text = "Published on:{}".format(self.videos[i][5],justify = "left"),
                                                            font = ("helvetica",8)).pack(anchor = "nw") 
                self.html = HTMLLabel(self.Use_Title_f[k],html = "<a style = \"font-size:8px\" href ={}>Click! to Open Video</a><br>".format("https://www.youtube.com/watch?v="+str(self.videos[i][3]))).pack( anchor = "nw")
                k+=1

    #function to show channel's videos when searched by channel and manually select is onn 
    def channel_show_manual(self):
        self.Working_on_Frame_5()
        self.Use_CheckBtns_var_cha = []
        self.Use_CheckBtns_cha = []
        self.Use_f_cha = []
        self.Use_Photo_f_cha = []
        self.Use_Title_f_cha = []
        self.Use_Check_f_cha = []
        self.photo_lst_cha = []
        
        if self.Choose_Text_File =="":
            keys = self.Channel_Var.get().split(",")
        else:
            with open(self.Choose_Text_File,"r") as file:
                keys = file.read().split(',')
        k = 0
        self.manual_videos_cha = []
        self.split_keys_cha = []
        for j in range(len(keys)):
            self.videos_cha = []
            try:
                self.videos_cha = Extract_Detail_by_channel(keys[j].strip(),1,self.Sort_By_var.get(),self.Video_Duration_var.get())
                self.search_channel_videos = Extract_Details_of_Channel_videos(self.videos_cha[0][0])
            except:
                self.Max_Result_error_Label.config(text = "Api Quota Exceeded",fg ="red")
            for i in range(len(self.search_channel_videos[:self.Max_Result.get()])):
                self.manual_videos_cha.append(self.search_channel_videos[i])
                self.split_keys_cha.append(keys[j])
                self.f_cha = Frame(self.second_frame,borderwidth = 4,relief = "sunken",width = 500,height = 100)
                self.Use_f_cha.append(self.f_cha)
                self.photo_f_cha = Frame(self.f_cha,borderwidth = 4,relief = "sunken",width = 150)
                self.Use_Photo_f_cha.append(self.photo_f_cha)
                self.title_f_cha = Frame(self.f_cha,borderwidth = 4,relief = "sunken",width = 270)
                self.Use_Title_f_cha.append(self.title_f_cha)
                self.check_f_cha = Frame(self.f_cha,borderwidth = 4,relief = "sunken",width = 80)
                self.Use_Check_f_cha.append(self.check_f_cha)

                self.Check_btn_var_cha = IntVar()
                self.Check_btn_var_cha.set(1)
                self.Use_CheckBtns_var_cha.append(self.Check_btn_var_cha)
                self.Check_btn_cha = Checkbutton(self.check_f_cha,variable = self.Use_CheckBtns_var_cha[k])
                self.Check_btn_cha.pack(side = "left")
                self.Use_CheckBtns_cha.append(self.Check_btn_cha)
        
                self.Use_Photo_f_cha[k].pack(expand = 0,fill = "y",side = "left")
                self.Use_Photo_f_cha[k].pack_propagate(0)
                self.Use_Title_f_cha[k].pack(expand = 0,fill = "y",side = "left")
                self.Use_Title_f_cha[k].pack_propagate(0)
                self.Use_Check_f_cha[k].pack(expand = 0,fill = "y",side = "left")
                self.Use_Check_f_cha[k].pack_propagate(0)
                self.Use_f_cha[k].pack(expand = 0,fill = "both")
                self.Use_f_cha[k].pack_propagate(0)

                self.imgurl_cha = "{}".format(self.search_channel_videos[i][2])
                self.image_data_cha = requests.get(self.imgurl_cha).content
                self.photo_lst_cha.append(ImageTk.PhotoImage(Image.open(BytesIO(self.image_data_cha)).resize((150, 100), Image.ANTIALIAS)))
                
                Label(self.Use_Photo_f_cha[k],image = self.photo_lst_cha[k]).pack()
                Label(self.Use_Title_f_cha[k],text = "Title:{}...".format(self.search_channel_videos[i][0][:35]) ,
                                                    font = ("helvetica",9,"bold"),justify = "left").pack(anchor = "nw")
                Label(self.Use_Title_f_cha[k],text = "Description:{}...".format(self.search_channel_videos[i][1][:30]),
                                                        font = ("helvetica",9),justify = "left").pack(anchor = "nw")
                Label(self.Use_Title_f_cha[k],text = "Published on:{}".format(self.search_channel_videos[i][5],justify = "left"),
                                                            font = ("helvetica",8)).pack(anchor = "nw") 
                self.html_cha = HTMLLabel(self.Use_Title_f_cha[k],html = "<a style = \"font-size:8px\" href ={}>Click! to Open Video</a><br>".format("https://www.youtube.com/watch?v="+str(self.search_channel_videos[i][3]))).pack( anchor = "nw")
                k+=1
            

    #function to show URL's videos when searched by URL and manually select is onn 
    def url_show_manual(self):
        self.Working_on_Frame_5()   
        self.Use_CheckBtns_var_url = []
        self.Use_CheckBtns_url = []
        self.Use_f_url = []
        self.Use_Photo_f_url = []
        self.Use_Title_f_url = []
        self.Use_Check_f_url = []
        self.photo_lst_url = []
    
        if self.Choose_Text_File =="":
            keys = self.URL_Var.get().split(",")
        else:
            with open(self.Choose_Text_File,"r") as file:
                keys = file.read().split(',')
        for n in range(len(keys)):
            keys[n] = keys[n].split("=")[-1]
        self.videos_url = []
        try:
            self.videos_url = Extract_Detail_of_URL_video(keys)
        except:
            self.Max_Result_error_Label.config(text = "Api Quota Exceeded",fg ="red")
        for i in range(len(self.videos_url)):
            self.f_url = Frame(self.second_frame,borderwidth = 4,relief = "sunken",width = 500,height = 100)
            self.Use_f_url.append(self.f_url)
            self.photo_f_url = Frame(self.f_url,borderwidth = 4,relief = "sunken",width = 150)
            self.Use_Photo_f_url.append(self.photo_f_url)
            self.title_f_url = Frame(self.f_url,borderwidth = 4,relief = "sunken",width = 270)
            self.Use_Title_f_url.append(self.title_f_url)
            self.check_f_url = Frame(self.f_url,borderwidth = 4,relief = "sunken",width = 80)
            self.Use_Check_f_url.append(self.check_f_url)

            self.Check_btn_var_url = IntVar()
            self.Check_btn_var_url.set(1)
            self.Use_CheckBtns_var_url.append(self.Check_btn_var_url)
            self.Check_btn_url = Checkbutton(self.check_f_url,variable = self.Use_CheckBtns_var_url[i])
            self.Check_btn_url.pack(side = "left")
            self.Use_CheckBtns_url.append(self.Check_btn_url)
                
            self.Use_Photo_f_url[i].pack(expand = 0,fill = "y",side = "left")
            self.Use_Photo_f_url[i].pack_propagate(0)
            self.Use_Title_f_url[i].pack(expand = 0,fill = "y",side = "left")
            self.Use_Title_f_url[i].pack_propagate(0)
            self.Use_Check_f_url[i].pack(expand = 0,fill = "y",side = "left")
            self.Use_Check_f_url[i].pack_propagate(0)
            self.Use_f_url[i].pack(expand = 0,fill = "both")
            self.Use_f_url[i].pack_propagate(0)

            self.imgurl_url = "{}".format(self.videos_url[i][2])
            self.image_data_url = requests.get(self.imgurl_url).content
            self.photo_lst_url.append(ImageTk.PhotoImage(Image.open(BytesIO(self.image_data_url)).resize((150, 100), Image.ANTIALIAS)))
                
            Label(self.Use_Photo_f_url[i],image = self.photo_lst_url[i]).pack()
            Label(self.Use_Title_f_url[i],text = "Title:{}...".format(self.videos_url[i][0][:35]) ,
                                                    font = ("helvetica",9,"bold"),justify = "left").pack(anchor = "nw")
            Label(self.Use_Title_f_url[i],text = "Description:{}...".format(self.videos_url[i][1][:30]),
                                                        font = ("helvetica",9),justify = "left").pack(anchor = "nw")
            Label(self.Use_Title_f_url[i],text = "Published on:{}".format(self.videos_url[i][5],justify = "left"),
                                                            font = ("helvetica",8)).pack(anchor = "nw") 
            self.html = HTMLLabel(self.Use_Title_f_url[i],html = "<a style = \"font-size:8px\" href ={}>Click! to Open Video</a><br>".format("https://www.youtube.com/watch?v="+str(self.videos_url[i][3]))).pack( anchor = "nw")    

    #function to show skipped videos and manually select is onn 
    def Show_Skipped_Func(self):
        self.Working_on_Frame_5()
        with DatabaseConnection("DataBase.db") as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM show_skipped")
            show_videos_captured = cursor.fetchall()
            connection.commit()
        self.Use_CheckBtns_show_s = []
        self.Use_f_show_s = []
        self.Use_Photo_f_show_s = []
        self.Use_Title_f_show_s = []
        self.Use_Check_f_show_s = []
        self.photo_lst_show_s = []
        for i in range(len(show_videos_captured)):
            self.f_show_s = Frame(self.second_frame,borderwidth = 4,relief = "sunken",width = 500,height = 100)
            self.Use_f_show_s.append(self.f_show_s)
            self.photo_f_show_s = Frame(self.f_show_s,borderwidth = 4,relief = "sunken",width = 150)
            self.Use_Photo_f_show_s.append(self.photo_f_show_s)
            self.title_f_show_s = Frame(self.f_show_s,borderwidth = 4,relief = "sunken",width = 270)
            self.Use_Title_f_show_s.append(self.title_f_show_s)
            self.check_f_show_s = Frame(self.f_show_s,borderwidth = 4,relief = "sunken",width = 80)
            self.Use_Check_f_show_s.append(self.check_f_show_s)

            self.Check_btn_var_show_s = IntVar()
            self.Use_CheckBtns_var_show_s.append(self.Check_btn_var_show_s)
            self.Check_btn_show_s = Checkbutton(self.check_f_show_s,variable = self.Use_CheckBtns_var_show_s[i])
            self.Check_btn_show_s.pack(side = "left")
            self.Use_CheckBtns_show_s.append(self.Check_btn_show_s)
                
            self.Use_Photo_f_show_s[i].pack(expand = 0,fill = "y",side = "left")
            self.Use_Photo_f_show_s[i].pack_propagate(0)
            self.Use_Title_f_show_s[i].pack(expand = 0,fill = "y",side = "left")
            self.Use_Title_f_show_s[i].pack_propagate(0)
            self.Use_Check_f_show_s[i].pack(expand = 0,fill = "y",side = "left")
            self.Use_Check_f_show_s[i].pack_propagate(0)
            self.Use_f_show_s[i].pack(expand = 0,fill = "both")
            self.Use_f_show_s[i].pack_propagate(0)

            self.imgurl_show_s = "{}".format(show_videos_captured[i][2])
            self.image_data_show_s = requests.get(self.imgurl_show_s).content
            self.photo_lst_show_s.append(ImageTk.PhotoImage(Image.open(BytesIO(self.image_data_show_s)).resize((150, 100), Image.ANTIALIAS)))
                
            Label(self.Use_Photo_f_show_s[i],image = self.photo_lst_show_s[i]).pack()
            Label(self.Use_Title_f_show_s[i],text = "Title:{}...".format(show_videos_captured[i][0][:35]) ,
                                                    font = ("helvetica",9,"bold"),justify = "left").pack(anchor = "nw")
            Label(self.Use_Title_f_show_s[i],text = "Description:{}...".format(show_videos_captured[i][1][:30]),
                                                        font = ("helvetica",9),justify = "left").pack(anchor = "nw")
            Label(self.Use_Title_f_show_s[i],text = "Published on:{}".format(show_videos_captured[i][5],justify = "left"),
                                                            font = ("helvetica",8)).pack(anchor = "nw") 
            self.html = HTMLLabel(self.Use_Title_f_show_s[i],html = "<a style = \"font-size:8px\" href ={}>Click! to Open Video</a><br>".format("https://www.youtube.com/watch?v="+str(show_videos_captured[i][3]))).pack( anchor = "nw")    

    #function to show captured videos  manually select is onn 
    def Show_Captured_Func(self):
            self.Working_on_Frame_5()
            with DatabaseConnection("DataBase.db") as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM show_captured")
                show_videos_skipped = cursor.fetchall()
                connection.commit()
            self.Use_CheckBtns_show_c = []
            self.Use_f_show_c = []
            self.Use_Photo_f_show_c = []
            self.Use_Title_f_show_c = []
            self.Use_Check_f_show_c = []
            self.photo_lst_show_c = []
            for i in range(len(show_videos_skipped)):
                self.f_show_c = Frame(self.second_frame,borderwidth = 4,relief = "sunken",width = 500,height = 100)
                self.Use_f_show_c.append(self.f_show_c)
                self.photo_f_show_c = Frame(self.f_show_c,borderwidth = 4,relief = "sunken",width = 150)
                self.Use_Photo_f_show_c.append(self.photo_f_show_c)
                self.title_f_show_c = Frame(self.f_show_c,borderwidth = 4,relief = "sunken",width = 270)
                self.Use_Title_f_show_c.append(self.title_f_show_c)
                self.check_f_show_c = Frame(self.f_show_c,borderwidth = 4,relief = "sunken",width = 80)
                self.Use_Check_f_show_c.append(self.check_f_show_c)

                self.Check_btn_var_show_c = IntVar()
                self.Use_CheckBtns_var_show_c.append(self.Check_btn_var_show_c)
                self.Check_btn_show_c = Checkbutton(self.check_f_show_c,variable = self.Use_CheckBtns_var_show_c[i])
                self.Check_btn_show_c.pack(side = "left")
                self.Use_CheckBtns_show_c.append(self.Check_btn_show_c)
                    
                self.Use_Photo_f_show_c[i].pack(expand = 0,fill = "y",side = "left")
                self.Use_Photo_f_show_c[i].pack_propagate(0)
                self.Use_Title_f_show_c[i].pack(expand = 0,fill = "y",side = "left")
                self.Use_Title_f_show_c[i].pack_propagate(0)
                self.Use_Check_f_show_c[i].pack(expand = 0,fill = "y",side = "left")
                self.Use_Check_f_show_c[i].pack_propagate(0)
                self.Use_f_show_c[i].pack(expand = 0,fill = "both")
                self.Use_f_show_c[i].pack_propagate(0)

                self.imgurl_show_c = "{}".format(show_videos_skipped[i][2])
                self.image_data_show_c = requests.get(self.imgurl_show_c).content
                self.photo_lst_show_c.append(ImageTk.PhotoImage(Image.open(BytesIO(self.image_data_show_c)).resize((150, 100), Image.ANTIALIAS)))     
                Label(self.Use_Photo_f_show_c[i],image = self.photo_lst_show_c[i]).pack()
            
                Label(self.Use_Title_f_show_c[i],text = "Title:{}...".format(show_videos_skipped[i][0][:35]) ,
                                                        font = ("helvetica",9,"bold"),justify = "left").pack(anchor = "nw")
                Label(self.Use_Title_f_show_c[i],text = "Description:{}...".format(show_videos_skipped[i][1][:30]),
                                                            font = ("helvetica",9),justify = "left").pack(anchor = "nw")
                Label(self.Use_Title_f_show_c[i],text = "Published on:{}".format(show_videos_skipped[i][5],justify = "left"),
                                                                font = ("helvetica",8)).pack(anchor = "nw") 
                self.html = HTMLLabel(self.Use_Title_f_show_c[i],html = "<a style = \"font-size:8px\" href ={}>Click! to Open Video</a><br>".format("https://www.youtube.com/watch?v="+str(show_videos_skipped[i][3]))).pack( anchor = "nw")    

    #function to start scraping skipped videos again only get the data of manualy chaeckbox checked videos 
    def Show_Skipped_Start_Func(self):
        if self.Use_CheckBtns_var_show_s != []:
            with DatabaseConnection("DataBase.db") as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM show_skipped")
                videos_captured = cursor.fetchall()
                connection.commit()
            self.log.insert(END,"->Capturing selected videos from show_skipped database\n\n")
            self.log.yview(END)
            self.logger.info("Capturing selected videos from show_skipped database")
            i=0
            for video_capture in videos_captured:
                if self.stp:
                    break
                if self.Use_CheckBtns_var_show_s[i].get():
                    if video_capture[7]=="keyword":
                        try:
                            updated_video = Extract_Detail_of_URL_video(video_capture[3])
                            self.log.insert(END,"->Got video {} from youtube Api\n\n".format("https://www.youtube.com/watch?v="+video_capture[3]))
                            self.log.yview(END)
                            self.logger.info("Got videos {} from youtube Api".format(video_capture[3]))
                        except:
                            self.log.insert(END,"->Youtube api key quota is exceeded\n\n")
                            self.log.yview(END)
                            self.logger.info("Youtube api key quota is exceeded")
                            self.Max_Result_error_Label.config(text = "Api Quota Exceeded",fg ="red")
                        try:
                            os.mkdir("Files/Searched_By_Keyword")
                            self.log.insert(END,"->Searched_By_Keyword Directory has been created\n\n")
                            self.log.yview(END)
                            self.logger.info("Searched_By_Keyword Directory has been created")
                        except:
                            self.log.insert(END,"->Searched_By_Keyword Directory is already available\n\n")
                            self.log.yview(END)
                            self.logger.info("Searched_By_Keyword Directory is already available")
                        try:
                            os.mkdir("Files/Searched_By_Keyword/{}".format(video_capture[6]))
                            self.log.insert(END,"->Searched_By_Keyword/{} Directory has been created\n\n".format(video_capture[6]))
                            self.log.yview(END)
                            self.logger.info("Searched_By_Keyword/{} Directory has been created".format(video_capture[6]))
                        except:
                            self.log.insert(END,"->Searched_By_Keyword/{} Directory already available\n\n".format(video_capture[6]))
                            self.log.yview(END)
                            self.logger.info("Searched_By_Keyword/{} Directory already available".format(video_capture[6]))
                        try:
                            self.transcript = Get_Transcript(updated_video[0][3])
                            self.log.insert(END,"->Got Transcript : {}\n\n".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                            self.log.yview(END)
                            self.logger.info("Got Transcript : {}".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                            f = self.file_name(updated_video[0][0])
                            try:
                                os.mkdir("Files/Searched_By_Keyword/{}/{}".format(video_capture[6],f))
                                self.log.insert(END,"->Searched_By_Keyword/{}/{} Directory has been created\n\n".format(video_capture[6],f))
                                self.log.yview(END)
                                self.logger.info("Searched_By_Keyword/{}/{} Directory has been created".format(video_capture[6],f))
                            except:
                                self.log.insert(END,"->Searched_By_Keyword/{}/{} Directory is already available\n\n".format(video_capture[6],f))
                                self.log.yview(END)
                                self.logger.info("Searched_By_Keyword/{}/{} Directory is already available".format(video_capture[6],f))
                                
                            with open("Files/Searched_By_Keyword/{}/{}/{}.txt".format(video_capture[6],f,f),"w",encoding="utf-8") as file:
                                try:
                                    r = requests.get(updated_video[0][2])
                                    b = BytesIO(r.content)
                                    img = Image.open(b)
                                    img.save("Files/Searched_By_Keyword/{}/{}/{}.jpeg".format(video_capture[6],f,f))
                                    file.write("-------------------------------------------------Video Details-------------------------------------------------")
                                    file.write("\n")
                                    file.write("\nTitle: "+updated_video[0][0])
                                    file.write("\nDescription: "+updated_video[0][1])
                                    file.write("\nThumbnail Link: "+updated_video[0][2])
                                    file.write("\nVideo Link: "+updated_video[0][3])
                                    file.write("\nChannel Name: "+updated_video[0][4])
                                    file.write("\nPublish Time: "+updated_video[0][5])
                                    file.write("\n\n")
                                    file.write("\n------------------------------------------Transcript Starts from here...----------------------------------------")
                                    file.write("\n")
                                    file.write(self.transcript)
                                    with DatabaseConnection("DataBase.db") as connection:
                                        cursor = connection.cursor()
                                        cursor.execute("""INSERT INTO SHOW_CAPTURED VALUES(?,?,?,?,?,?,?,?)
                                        """,(updated_video[0][0],updated_video[0][1],updated_video[0][2],updated_video[0][3],updated_video[0][4],updated_video[0][5],video_capture[6],"keyword"))
                                        connection.commit()

                                        cursor.execute("""DELETE FROM SHOW_CAPTURED WHERE video_link = ?""",(video_capture[3]))
                                        connection.commit()
                                        self.log.insert(END,"->Captured Succesfully: {}\n\n".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                                        self.log.yview(END)
                                        self.logger.info("Captured Succesfully: {}".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                                except Exception:
                                    self.log.insert(END,"->Skipped it because it is Already Captured : {}\n\n".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                                    self.log.yview(END)
                                    self.logger.info("Skipped it because it is Already Captured : {}".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                        except:
                            try:
                                with DatabaseConnection("DataBase.db") as connection:
                                        cursor = connection.cursor()
                                        cursor.execute("""UPDATE SHOW_SKIPPED SET title = ?,
                                                                            description = ?,
                                                                            thumbnail_link = ?,
                                                                            video_link = ?,
                                                                            channel_name = ?,
                                                                            publish_time = ?,
                                                                            searched = ?,
                                                                            searched_by = ?
                                        WHERE video_link=?""",(updated_video[0][0],updated_video[0][1],updated_video[0][2],updated_video[0][3],updated_video[0][4],updated_video[0][5],video_capture[6],"keyword",video_capture[3]))
                                        connection.commit()
                                        self.log.insert(END,"->Transcript Not Found! - Skipped : {}\n\n".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                                        self.log.yview(END)
                                        self.logger.info("Transcript Not Found! - Skipped : {}".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                            except: 
                                self.log.insert(END,"->Already in Skipped : {}\n\n".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                                self.log.yview(END)
                                self.logger.info("Already in Skipped : {}".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                                
                    elif video_capture[7] =="channel":
                        try:
                            updated_video = Extract_Detail_of_URL_video(video_capture[3])
                            self.log.insert(END,"->Got video {} from youtube Api\n\n".format("https://www.youtube.com/watch?v="+video_capture[3]))
                            self.log.yview(END)
                            self.logger.info("Got videos {} from youtube Api".format("https://www.youtube.com/watch?v="+video_capture[3]))
                        except:
                            self.log.insert(END,"->Youtube api key quota is exceeded\n\n")
                            self.log.yview(END)
                            self.logger.info("Youtube api key quota is exceeded")
                            self.Max_Result_error_Label.config(text = "Api Quota Exceeded",fg ="red")
                            
                        try:
                            os.mkdir("Files/Searched_By_Channel")
                            self.log.insert(END,"->Searched_By_Channel Directory has been created\n\n")
                            self.log.yview(END)
                            self.logger.info("Searched_By_Channel Directory has been created")
                        except:
                            self.log.insert(END,"->Searched_By_Channel Directory is already available\n\n")
                            self.log.yview(END)
                            self.logger.info("Searched_By_Channel Directory is already available")
                            
                        try:
                            os.mkdir("Files/Searched_By_Channel/{}".format(video_capture[6]))
                            self.log.insert(END,"->Searched_By_Channel/{} Directory has been created\n\n".format(video_capture[6]))
                            self.log.yview(END)
                            self.logger.info("Searched_By_Channel/{} Directory has been created".format(video_capture[6]))
                        except:
                            self.log.insert(END,"->Searched_By_Channel/{} Directory already available\n\n".format(video_capture[6]))
                            self.logger.info("Searched_By_Channel/{} Directory already available".format(video_capture[6]))
                            
                        try:
                            self.transcript = Get_Transcript(updated_video[0][3])
                            self.log.insert(END,"->Got Transcript : {}\n\n".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                            self.log.yview(END)
                            self.logger.info("Got Transcript : {}".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                            f = self.file_name(updated_video[0][0])
                            try:
                                os.mkdir("Files/Searched_By_Channel/{}/{}".format(video_capture[6],f))
                                self.log.insert(END,"->Searched_By_Channel/{}/{} Directory has been created\n\n".format(video_capture[6],f))
                                self.log.yview(END)
                                self.logger.info("Searched_By_Channel/{}/{} Directory has been created".format(video_capture[6],f))
                            except:
                                self.log.insert(END,"->Searched_By_Channel/{}/{} Directory is already available\n\n".format(video_capture[6],f))
                                self.log.yview(END)
                                self.logger.info("Searched_By_Channel/{}/{} Directory is already available".format(video_capture[6],f))
                                
                            with open("Files/Searched_By_Channel/{}/{}/{}.txt".format(video_capture[6],f,f),"w",encoding="utf-8") as file:
                                try:
                                    r = requests.get(updated_video[0][2])
                                    b = BytesIO(r.content)
                                    img = Image.open(b)
                                    img.save("Files/Searched_By_Channel/{}/{}/{}.jpeg".format(video_capture[6],f,f))
                                    file.write("-------------------------------------------------Video Details-------------------------------------------------")
                                    file.write("\n")
                                    file.write("\nTitle: "+updated_video[0][0])
                                    file.write("\nDescription: "+updated_video[0][1])
                                    file.write("\nThumbnail Link: "+updated_video[0][2])
                                    file.write("\nVideo Link: "+updated_video[0][3])
                                    file.write("\nChannel Name: "+updated_video[0][4])
                                    file.write("\nPublish Time: "+updated_video[0][5])
                                    file.write("\n\n")
                                    file.write("\n------------------------------------------Transcript Starts from here...----------------------------------------")
                                    file.write("\n")
                                    file.write(self.transcript)
                                    with DatabaseConnection("DataBase.db") as connection:
                                        cursor = connection.cursor()
                                        cursor.execute("""UPDATE SHOW_CAPTURED SET title = ?,
                                                                            description = ?,
                                                                            thumbnail_link = ?,
                                                                            video_link = ?,
                                                                            channel_name = ?,
                                                                            publish_time = ?,
                                                                            searched = ?,
                                                                            searched_by = ?
                                    WHERE video_link=?""",(updated_video[0][0],updated_video[0][1],updated_video[0][2],updated_video[0][3],updated_video[0][4],updated_video[0][5],video_capture[6],"keyword",video_capture[3]))
                                    connection.commit()
                                    self.log.insert(END,"->Captured Succesfully: {}\n\n".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                                    self.log.yview(END)
                                    self.logger.info("Captured Succesfully: {}".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                                except Exception:
                                    self.log.insert(END,"->Skipped it because it is Already Captured : {}\n\n".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                                    self.log.yview(END)
                                    self.logger.info("Skipped it because it is Already Captured : {}".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                                    
                        except:
                            try:
                                with DatabaseConnection("DataBase.db") as connection:
                                    cursor = connection.cursor()
                                    cursor.execute("""INSERT INTO SHOW_SKIPPED VALUES(?,?,?,?,?,?,?,?) 
                                            """,(updated_video[0][0],updated_video[0][1],updated_video[0][2],updated_video[0][3],updated_video[0][4],updated_video[0][5],video_capture[6],"keyword"))
                                    connection.commit()
                                    cursor.execute("""DELETE FROM SHOW_CAPTURED WHERE video_link = ?""",(video_capture[3]))
                                    connection.commit()
                                    self.log.insert(END,"->Transcript Not Found! - Skipped : {}\n\n".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                                    self.log.yview(END)
                                    self.logger.info("Transcript Not Found! - Skipped : {}".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                            except: 
                                self.log.insert(END,"->Already in Skipped : {}\n\n".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                                self.log.yview(END)
                                self.logger.info("Already in Skipped : {}".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                    elif video_capture[7] == "url":
                        try:
                            updated_video = Extract_Detail_of_URL_video(video_capture[3])
                            self.log.insert(END,"->Got video {} from youtube Api\n\n".format("https://www.youtube.com/watch?v="+video_capture[3]))
                            self.log.yview(END)
                            self.logger.info("Got videos {} from youtube Api".format("https://www.youtube.com/watch?v="+video_capture[3]))
                        except:
                            self.log.insert(END,"->Youtube api key quota is exceeded\n\n")
                            self.log.yview(END)
                            self.logger.info("Youtube api key quota is exceeded")
                            self.Max_Result_error_Label.config(text = "Api Quota Exceeded",fg ="red")
                        try:
                            os.mkdir("Files/Searched_By_URL")
                            self.log.insert(END,"->Searched_By_URL Directory has been created\n\n")
                            self.log.yview(END)
                            self.logger.info("Searched_By_URL Directory has been created")
                        except:
                            self.log.insert(END,"->Searched_By_URL Directory is already available\n\n")
                            self.log.yview(END)
                            self.logger.info("Searched_By_URL Directory is already available")
                        try:
                            os.mkdir("Files/Searched_By_URL/{}".format(video_capture[6]))
                            self.log.insert(END,"->Searched_By_URL/{} Directory has been created\n\n".format(video_capture[6]))
                            self.log.yview(END)
                            self.logger.info("Searched_By_URL/{} Directory has been created".format(video_capture[6]))
                        except:
                            self.log.insert(END,"->Searched_By_URL/{} Directory is already available\n\n".format(video_capture[6]))
                            self.log.yview(END)
                            self.logger.info("Searched_By_URL/{} Directory is already available".format(video_capture[6]))
                        try:
                            self.transcript = Get_Transcript(updated_video[0][3])
                            self.log.insert(END,"->Got Transcript : {}\n\n".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                            self.log.yview(END)
                            self.logger.info("Got Transcript : {}".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                            f = self.file_name(updated_video[0][0])
                            try:
                                os.mkdir("Files/Searched_By_URL/{}/{}".format(video_capture[6],f))
                                self.log.insert(END,"->Searched_By_URL/{}/{} Directory has been created\n\n".format(video_capture[6],f))
                                self.log.yview(END)
                                self.logger.info("Searched_By_URL/{}/{} Directory has been created".format(video_capture[6],f))
                            except:
                                self.log.insert(END,"->Searched_By_URL/{}/{} Directory is already available\n\n".format(video_capture[6],f))
                                self.log.yview(END)
                                self.logger.info("Searched_By_URL/{}/{} Directory is already available".format(video_capture[6],f))
                            with open("Files/Searched_By_URL/{}/{}/{}.txt".format(video_capture[6],f,f),"w",encoding="utf-8") as file:
                                try:
                                    r = requests.get(updated_video[0][2])
                                    b = BytesIO(r.content)
                                    img = Image.open(b)
                                    img.save("Files/Searched_By_URL/{}/{}/{}.jpeg".format(video_capture[6],f,f))
                                    file.write("-------------------------------------------------Video Details-------------------------------------------------")
                                    file.write("\n")
                                    file.write("\nTitle: "+updated_video[0][0])
                                    file.write("\nDescription: "+updated_video[0][1])
                                    file.write("\nThumbnail Link: "+updated_video[0][2])
                                    file.write("\nVideo Link: "+updated_video[0][3])
                                    file.write("\nChannel Name: "+updated_video[0][4])
                                    file.write("\nPublish Time: "+updated_video[0][5])
                                    file.write("\n\n")
                                    file.write("\n------------------------------------------Transcript Starts from here...----------------------------------------")
                                    file.write("\n")
                                    file.write(self.transcript)
                                    with DatabaseConnection("DataBase.db") as connection:
                                        cursor = connection.cursor()
                                        cursor.execute("""UPDATE SHOW_CAPTURED SET title = ?,
                                                                            description = ?,
                                                                            thumbnail_link = ?,
                                                                            video_link = ?,
                                                                            channel_name = ?,
                                                                            publish_time = ?,
                                                                            searched = ?,
                                                                            searched_by = ?
                                    WHERE video_link=?""",(updated_video[0][0],updated_video[0][1],updated_video[0][2],updated_video[0][3],updated_video[0][4],updated_video[0][5],video_capture[6],"keyword",video_capture[3]))
                                    connection.commit()
                                    self.log.insert(END,"->Captured Succesfully: {}\n\n".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                                    self.log.yview(END)
                                    self.logger.info("Captured Succesfully: {}".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                                except Exception:
                                    self.log.insert(END,"->Skipped it because it is Already Captured : {}\n\n".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                                    self.log.yview(END)
                                    self.logger.info("Skipped it because it is Already Captured : {}".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                                    
                        except:
                            try:
                                with DatabaseConnection("DataBase.db") as connection:
                                    cursor = connection.cursor()
                                    cursor.execute("""INSERT INTO SHOW_SKIPPED VALUES(?,?,?,?,?,?,?,?) 
                                            """,(updated_video[0][0],updated_video[0][1],updated_video[0][2],updated_video[0][3],updated_video[0][4],updated_video[0][5],video_capture[6],"keyword"))
                                    connection.commit()
                                    cursor.execute("""DELETE FROM SHOW_CAPTURED WHERE video_link = ?""",(video_capture[3]))
                                    connection.commit()
                                    self.log.insert(END,"->Transcript Not Found! - Skipped : {}\n\n".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                                    self.log.yview(END)
                                    self.logger.info("Transcript Not Found! - Skipped : {}".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                            except: 
                                self.log.insert(END,"->Already in Skipped : {}\n\n".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                                self.log.yview(END)
                                self.logger.info("Already in Skipped : {}".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                                
                i+=1
        
    #function to get data of videos again of captured videos when searched by channel and manually select is onn
    def Show_Captured_Start_Func(self):
        if self.Use_CheckBtns_var_show_c != []:
            with DatabaseConnection("DataBase.db") as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM show_captured")
                videos_captured = cursor.fetchall()
                connection.commit()
            self.log.insert(END,"->Capturing selected videos from show_captured database\n\n")
            self.log.yview(END)
            self.logger.info("Capturing selected videos from show_captured database")
            i=0
            if self.Use_CheckBtns_var_show_c != []:
                for video_capture in videos_captured:
                    if self.stp:
                        break
                    if self.Use_CheckBtns_var_show_c[i].get():
                        if video_capture[7]=="keyword":
                            try:
                                updated_video = Extract_Detail_of_URL_video(video_capture[3])
                                self.log.insert(END,"->Got video {} from youtube Api\n\n".format("https://www.youtube.com/watch?v="+video_capture[3]))
                                self.log.yview(END)
                                self.logger.info("Got videos {} from youtube Api".format("https://www.youtube.com/watch?v="+video_capture[3]))
                            except:
                                self.log.insert(END,"->Youtube api key quota is exceeded\n\n")
                                self.logger.info("Youtube api key quota is exceeded")
                                self.log.yview(END)
                                self.Max_Result_error_Label.config(text = "Api Quota Exceeded",fg ="red")
                                
                            try:
                                os.mkdir("Files/Searched_By_Keyword")
                                self.log.insert(END,"->Searched_By_Keyword Directory has been created\n\n")
                                self.log.yview(END)
                                self.logger.info("Searched_By_Keyword Directory has been created")
                            except:
                                self.log.insert(END,"->Searched_By_Keyword Directory is already available\n\n")
                                self.log.yview(END)
                                self.logger.info("Searched_By_Keyword Directory is already available")
                                
                            try:
                                os.mkdir("Files/Searched_By_Keyword/{}".format(video_capture[6]))
                                self.log.insert(END,"->Searched_By_Keyword/{} Directory has been created\n\n".format(video_capture[6]))
                                self.log.yview(END)
                                self.logger.info("Searched_By_Keyword/{} Directory has been created".format(video_capture[6]))
                            except:
                                self.log.insert(END,"->Searched_By_Keyword/{} Directory already available\n\n".format(video_capture[6]))
                                self.log.yview(END)
                                self.logger.info("Searched_By_Keyword/{} Directory already available".format(video_capture[6]))
                                
                            try:
                                self.transcript = Get_Transcript(updated_video[0][3])
                                self.log.insert(END,"->Got Transcript : {}\n\n".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                                self.log.yview(END)
                                self.logger.info("Got Transcript : {}".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                                f = self.file_name(updated_video[0][0])
                                try:
                                    os.mkdir("Files/Searched_By_Keyword/{}/{}".format(video_capture[6],f))
                                    self.log.insert(END,"->Searched_By_Keyword/{}/{} Directory has been created\n\n".format(video_capture[6],f))
                                    self.log.yview(END)
                                    self.logger.info("Searched_By_Keyword/{}/{} Directory has been created".format(video_capture[6],f))
                                except:
                                    self.log.insert(END,"->Searched_By_Keyword/{}/{} Directory is already available\n\n".format(video_capture[6],f))
                                    self.log.yview(END)
                                    self.logger.info("Searched_By_Keyword/{}/{} Directory is already available".format(video_capture[6],f))
                                    
                                with open("Files/Searched_By_Keyword/{}/{}/{}.txt".format(video_capture[6],f,f),"w",encoding="utf-8") as file:
                                    try:
                                        r = requests.get(updated_video[0][2])
                                        b = BytesIO(r.content)
                                        img = Image.open(b)
                                        img.save("Files/Searched_By_Keyword/{}/{}/{}.jpeg".format(video_capture[6],f,f))
                                        file.write("-------------------------------------------------Video Details-------------------------------------------------")
                                        file.write("\n")
                                        file.write("\nTitle: "+updated_video[0][0])
                                        file.write("\nDescription: "+updated_video[0][1])
                                        file.write("\nThumbnail Link: "+updated_video[0][2])
                                        file.write("\nVideo Link: "+updated_video[0][3])
                                        file.write("\nChannel Name: "+updated_video[0][4])
                                        file.write("\nPublish Time: "+updated_video[0][5])
                                        file.write("\n\n")
                                        file.write("\n------------------------------------------Transcript Starts from here...----------------------------------------")
                                        file.write("\n")
                                        file.write(self.transcript)
                                        with DatabaseConnection("DataBase.db") as connection:
                                            cursor = connection.cursor()
                                            cursor.execute("""UPDATE SHOW_CAPTURED SET title = ?,
                                                                                description = ?,
                                                                                thumbnail_link = ?,
                                                                                video_link = ?,
                                                                                channel_name = ?,
                                                                                publish_time = ?,
                                                                                searched = ?,
                                                                                searched_by = ?
                                        WHERE video_link=?""",(updated_video[0][0],updated_video[0][1],updated_video[0][2],updated_video[0][3],updated_video[0][4],updated_video[0][5],video_capture[6],"keyword",video_capture[3]))
                                        connection.commit()
                                        self.log.insert(END,"->Captured Succesfully: {}\n\n".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                                        self.log.yview(END)
                                        self.logger.info("Captured Succesfully: {}".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                                    except Exception:
                                        self.log.insert(END,"->Skipped it because it is Already Captured : {}\n\n".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                                        self.log.yview(END)
                                        self.logger.info("Skipped it because it is Already Captured : {}".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                                        
                            except:
                                try:
                                    with DatabaseConnection("DataBase.db") as connection:
                                        cursor = connection.cursor()
                                        cursor.execute("""INSERT INTO SHOW_SKIPPED VALUES(?,?,?,?,?,?,?,?)
                                        """,(updated_video[0][0],updated_video[0][1],updated_video[0][2],updated_video[0][3],updated_video[0][4],updated_video[0][5],video_capture[6],"keyword"))
                                        connection.commit()

                                        cursor.execute("""DELETE FROM SHOW_CAPTURED WHERE video_link = ?""",(video_capture[3]))
                                        connection.commit()
                                        self.log.insert(END,"->Transcript Not Found! - Skipped : {}\n\n".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                                        self.log.yview(END)
                                        self.logger.info("Transcript Not Found! - Skipped : {}".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                                except: 
                                    self.log.insert(END,"->Already in Skipped : {}\n\n".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                                    self.log.yview(END)
                                    self.logger.info("Already in Skipped : {}".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                                
                        elif video_capture[7] =="channel":
                            try:
                                updated_video = Extract_Detail_of_URL_video(video_capture[3])
                                self.log.insert(END,"->Got video {} from youtube Api\n\n".format("https://www.youtube.com/watch?v="+video_capture[3]))
                                self.log.yview(END)
                                self.logger.info("Got videos {} from youtube Api".format("https://www.youtube.com/watch?v="+video_capture[3]))
                            except:
                                self.log.insert(END,"->Youtube api key quota is exceeded\n\n")
                                self.logger.info("Youtube api key quota is exceeded")
                                self.log.yview(END)
                                self.Max_Result_error_Label.config(text = "Api Quota Exceeded",fg ="red")
                                
                            try:
                                os.mkdir("Files/Searched_By_Channel")
                                self.log.insert(END,"->Searched_By_Channel Directory has been created\n\n")
                                self.log.yview(END)
                                self.logger.info("Searched_By_Channel Directory has been created")
                            except:
                                self.log.insert(END,"->Searched_By_Channel Directory is already available\n\n")
                                self.log.yview(END)
                                self.logger.info("Searched_By_Channel Directory is already available")
                         
                            try:
                                os.mkdir("Files/Searched_By_Channel/{}".format(video_capture[6]))
                                self.log.insert(END,"->Searched_By_Channel/{} Directory has been created\n\n".format(video_capture[6]))
                                self.log.yview(END)
                                self.logger.info("Searched_By_Channel/{} Directory has been created".format(video_capture[6]))
                            except:
                                self.log.insert(END,"->Searched_By_Channel/{} Directory already available\n\n".format(video_capture[6]))
                                self.log.yview(END)
                                self.logger.info("Searched_By_Channel/{} Directory already available".format(video_capture[6]))
                               
                            try:
                                self.transcript = Get_Transcript(updated_video[0][3])
                                self.log.insert(END,"->Got Transcript : {}\n\n".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                                self.log.yview(END)
                                self.logger.info("Got Transcript : {}".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                                f = self.file_name(updated_video[0][0])
                                try:
                                    os.mkdir("Files/Searched_By_Channel/{}/{}".format(video_capture[6],f))
                                    self.log.insert(END,"->Searched_By_Channel/{}/{} Directory has been created\n\n".format(video_capture[6],f))
                                    self.log.yview(END)
                                    self.logger.info("Searched_By_Channel/{}/{} Directory has been created".format(video_capture[6],f))
                                except:
                                    self.log.insert(END,"->Searched_By_Channel/{}/{} Directory is already available\n\n".format(video_capture[6],f))
                                    self.log.yview(END)
                                    self.logger.info("Searched_By_Channel/{}/{} Directory is already available".format(video_capture[6],f))
                                    
                                with open("Files/Searched_By_Channel/{}/{}/{}.txt".format(video_capture[6],f,f),"w",encoding="utf-8") as file:
                                    try:
                                        r = requests.get(updated_video[0][2])
                                        b = BytesIO(r.content)
                                        img = Image.open(b)
                                        img.save("Files/Searched_By_Channel/{}/{}/{}.jpeg".format(video_capture[6],f,f))
                                        file.write("-------------------------------------------------Video Details-------------------------------------------------")
                                        file.write("\n")
                                        file.write("\nTitle: "+updated_video[0][0])
                                        file.write("\nDescription: "+updated_video[0][1])
                                        file.write("\nThumbnail Link: "+updated_video[0][2])
                                        file.write("\nVideo Link: "+updated_video[0][3])
                                        file.write("\nChannel Name: "+updated_video[0][4])
                                        file.write("\nPublish Time: "+updated_video[0][5])
                                        file.write("\n\n")
                                        file.write("\n------------------------------------------Transcript Starts from here...----------------------------------------")
                                        file.write("\n")
                                        file.write(self.transcript)
                                        with DatabaseConnection("DataBase.db") as connection:
                                            cursor = connection.cursor()
                                            cursor.execute("""UPDATE SHOW_CAPTURED SET title = ?,
                                                                                description = ?,
                                                                                thumbnail_link = ?,
                                                                                video_link = ?,
                                                                                channel_name = ?,
                                                                                publish_time = ?,
                                                                                searched = ?,
                                                                                searched_by = ?
                                        WHERE video_link=?""",(updated_video[0][0],updated_video[0][1],updated_video[0][2],updated_video[0][3],updated_video[0][4],updated_video[0][5],video_capture[6],"keyword",video_capture[3]))
                                        connection.commit()
                                        self.log.insert(END,"->Captured Succesfully: {}\n\n".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                                        self.log.yview(END)
                                        self.logger.info("Captured Succesfully: {}".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                                    except Exception:
                                        self.log.insert(END,"->Skipped it because it is Already Captured : {}\n\n".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                                        self.log.yview(END)
                                        self.logger.info("Skipped it because it is Already Captured : {}".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                                        
                            except:
                                try:
                                    with DatabaseConnection("DataBase.db") as connection:
                                        cursor = connection.cursor()
                                        cursor.execute("""INSERT INTO SHOW_SKIPPED VALUES(?,?,?,?,?,?,?,?) 
                                                """,(updated_video[0][0],updated_video[0][1],updated_video[0][2],updated_video[0][3],updated_video[0][4],updated_video[0][5],video_capture[6],"keyword"))
                                        connection.commit()
                                        cursor.execute("""DELETE FROM SHOW_CAPTURED WHERE video_link = ?""",(video_capture[3]))
                                        connection.commit()
                                        self.log.insert(END,"->Transcript Not Found! - Skipped : {}\n\n".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                                        self.log.yview(END)
                                        self.logger.info("Transcript Not Found! - Skipped : {}".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                                except: 
                                    self.log.insert(END,"->Already in Skipped : {}\n\n".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                                    self.log.yview(END)
                                    self.logger.info("Already in Skipped : {}".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                                    
                        elif video_capture[7] == "url":
                            try:
                                updated_video = Extract_Detail_of_URL_video(video_capture[3])
                                self.log.insert(END,"->Got video {} from youtube Api\n\n".format("https://www.youtube.com/watch?v="+video_capture[3]))
                                self.log.yview(END)
                                self.logger.info("Got videos {} from youtube Api".format("https://www.youtube.com/watch?v="+video_capture[3]))
                            except:
                                self.log.insert(END,"->Youtube api key quota is exceeded\n\n")
                                self.log.yview(END)
                                self.logger.info("Youtube api key quota is exceeded")
                                self.Max_Result_error_Label.config(text = "Api Quota Exceeded",fg ="red")
                        
                            try:
                                os.mkdir("Files/Searched_By_URL")
                                self.log.insert(END,"->Searched_By_URL Directory has been created\n\n")
                                self.log.yview(END)
                                self.logger.info("Searched_By_URL Directory has been created")
                            except:
                                self.log.insert(END,"->Searched_By_URL Directory is already available\n\n")
                                self.log.yview(END)
                                self.logger.info("Searched_By_URL Directory is already available")
                                
                            try:
                                os.mkdir("Files/Searched_By_URL/{}".format(video_capture[6]))
                                self.log.insert(END,"->Searched_By_URL/{} Directory has been created\n\n".format(video_capture[6]))
                                self.log.yview(END)
                                self.logger.info("Searched_By_URL/{} Directory has been created".format(video_capture[6]))
                            except:
                                self.log.insert(END,"->Searched_By_URL/{} Directory is already available\n\n".format(video_capture[6]))
                                self.log.yview(END)
                                self.logger.info("Searched_By_URL/{} Directory is already available".format(video_capture[6]))
                                
                            try:
                                self.transcript = Get_Transcript(updated_video[0][3])
                                self.log.insert(END,"->Got Transcript : {}\n\n".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                                self.log.yview(END)
                                self.logger.info("Got Transcript : {}".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                                f = self.file_name(updated_video[0][0])
                                try:
                                    os.mkdir("Files/Searched_By_URL/{}/{}".format(video_capture[6],f))
                                    self.log.insert(END,"->Searched_By_URL/{}/{} Directory has been created\n\n".format(video_capture[6],f))
                                    self.log.yview(END)
                                    self.logger.info("Searched_By_URL/{}/{} Directory has been created".format(video_capture[6],f))
                                except:
                                    self.log.insert(END,"->Searched_By_URL/{}/{} Directory is already available\n\n".format(video_capture[6],f))
                                    self.log.yview(END)
                                    self.logger.info("Searched_By_URL/{}/{} Directory is already available".format(video_capture[6],f))
                                    
                                with open("Files/Searched_By_URL/{}/{}/{}.txt".format(video_capture[6],f,f),"w",encoding="utf-8") as file:
                                    try:
                                        r = requests.get(updated_video[0][2])
                                        b = BytesIO(r.content)
                                        img = Image.open(b)
                                        img.save("Files/Searched_By_URL/{}/{}/{}.jpeg".format(video_capture[6],f,f))
                                        file.write("-------------------------------------------------Video Details-------------------------------------------------")
                                        file.write("\n")
                                        file.write("\nTitle: "+updated_video[0][0])
                                        file.write("\nDescription: "+updated_video[0][1])
                                        file.write("\nThumbnail Link: "+updated_video[0][2])
                                        file.write("\nVideo Link: "+updated_video[0][3])
                                        file.write("\nChannel Name: "+updated_video[0][4])
                                        file.write("\nPublish Time: "+updated_video[0][5])
                                        file.write("\n\n")
                                        file.write("\n------------------------------------------Transcript Starts from here...----------------------------------------")
                                        file.write("\n")
                                        file.write(self.transcript)
                                        with DatabaseConnection("DataBase.db") as connection:
                                            cursor = connection.cursor()
                                            cursor.execute("""UPDATE SHOW_CAPTURED SET title = ?,
                                                                                description = ?,
                                                                                thumbnail_link = ?,
                                                                                video_link = ?,
                                                                                channel_name = ?,
                                                                                publish_time = ?,
                                                                                searched = ?,
                                                                                searched_by = ?
                                        WHERE video_link=?""",(updated_video[0][0],updated_video[0][1],updated_video[0][2],updated_video[0][3],updated_video[0][4],updated_video[0][5],video_capture[6],"keyword",video_capture[3]))
                                        connection.commit()
                                        self.log.insert(END,"->Captured Succesfully: {}\n\n".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                                        self.log.yview(END)
                                        self.logger.info("Captured Succesfully: {}".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                                    except Exception:
                                        self.log.insert(END,"->Skipped it because it is Already Captured : {}\n\n".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                                        self.log.yview(END)
                                        self.logger.info("Skipped it because it is Already Captured : {}".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                                        
                            except:
                                try:
                                    with DatabaseConnection("DataBase.db") as connection:
                                        cursor = connection.cursor()
                                        cursor.execute("""INSERT INTO SHOW_SKIPPED VALUES(?,?,?,?,?,?,?,?) 
                                                """,(updated_video[0][0],updated_video[0][1],updated_video[0][2],updated_video[0][3],updated_video[0][4],updated_video[0][5],video_capture[6],"keyword"))
                                        connection.commit()
                                        cursor.execute("""DELETE FROM SHOW_CAPTURED WHERE video_link = ?""",(video_capture[3]))
                                        connection.commit()
                                        self.log.insert(END,"->Transcript Not Found! - Skipped : {}\n\n".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                                        self.log.yview(END)
                                        self.logger.info("Transcript Not Found! - Skipped : {}".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                                except: 
                                    self.log.insert(END,"->Already in Skipped : {}\n\n".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                                    self.log.yview(END)
                                    self.logger.info("Already in Skipped : {}".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                                    
                    i+=1
       
    #function to update by schedule        
    def Start_Updating(self):
        self.stp = 0
        self.skip_vi = 0
        self.cap_vi = 0
        self.Start_Button.config(state = DISABLED)
        self.Stop_Button.config(state = NORMAL)
        self.show_skipped.config(state  = DISABLED)
        self.show_captured.config(state = DISABLED)
        self.Sort_By.config(state = DISABLED)
        self.Video_Duration.config(state = DISABLED)
        with DatabaseConnection("DataBase.db") as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM show_captured")
            videos_captured = cursor.fetchall()
            connection.commit()
        self.log.insert(END,"->Updating Schedule Videos...........\n\n")
        self.log.yview(END)
        self.logger.info("Updating schedule Videos...........")
        self.Max_Result_label.config(text = "Max Result: {}".format(len(videos_captured)))
        for video_capture in videos_captured:
            if self.stp:
                break
            if video_capture[7]=="keyword":
                try:
                    updated_video = Extract_Detail_of_URL_video(video_capture[3])
                    self.log.insert(END,"->Got video {} from youtube Api\n\n".format("https://www.youtube.com/watch?v="+video_capture[3]))
                    self.log.yview(END)
                    self.logger.info("Got videos {} from youtube Api".format("https://www.youtube.com/watch?v="+video_capture[3]))
                except:
                    self.log.insert(END,"->Youtube api key quota is exceeded\n\n")
                    self.logger.info("Youtube api key quota is exceeded")
                    self.log.yview(END)
                    self.Max_Result_error_Label.config(text = "Api Quota Exceeded",fg ="red")
                    
                try:
                    os.mkdir("Files/Searched_By_Keyword")
                    self.log.insert(END,"->Searched_By_Keyword Directory has been created\n\n")
                    self.log.yview(END)
                    self.logger.info("Searched_By_Keyword Directory has been created")
                except:
                    self.log.insert(END,"->Searched_By_Keyword Directory is already available\n\n")
                    self.log.yview(END)
                    self.logger.info("Searched_By_Keyword Directory is already available")
                    
                try:
                    os.mkdir("Files/Searched_By_Keyword/{}".format(video_capture[6]))
                    self.log.insert(END,"->Searched_By_Keyword/{} Directory has been created\n\n".format(video_capture[6]))
                    self.log.yview(END)
                    self.logger.info("Searched_By_Keyword/{} Directory has been created".format(video_capture[6]))
                except:
                    self.log.insert(END,"->Searched_By_Keyword/{} Directory already available\n\n".format(video_capture[6]))
                    self.log.yview(END)
                    self.logger.info("Searched_By_Keyword/{} Directory already available".format(video_capture[6]))
                    
                try:
                    self.transcript = Get_Transcript(updated_video[0][3])
                    self.log.insert(END,"->Got Transcript : {}\n\n".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                    self.log.yview(END)
                    self.logger.info("Got Transcript : {}".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                    f = self.file_name(updated_video[0][0])
                    try:
                        os.mkdir("Files/Searched_By_Keyword/{}/{}".format(video_capture[6],f))
                        self.log.insert(END,"->Searched_By_Keyword/{}/{} Directory has been created\n\n".format(video_capture[6],f))
                        self.log.yview(END)
                        self.logger.info("Searched_By_Keyword/{}/{} Directory has been created".format(video_capture[6],f))
                    except:
                        self.log.insert(END,"->Searched_By_Keyword/{}/{} Directory is already available\n\n".format(video_capture[6],f))
                        self.log.yview(END)
                        self.logger.info("Searched_By_Keyword/{}/{} Directory is already available".format(video_capture[6],f))
                        
                    with open("Files/Searched_By_Keyword/{}/{}/{}.txt".format(video_capture[6],f,f),"w",encoding="utf-8") as file:
                        try:
                            r = requests.get(updated_video[0][2])
                            b = BytesIO(r.content)
                            img = Image.open(b)
                            img.save("Files/Searched_By_Keyword/{}/{}/{}.jpeg".format(video_capture[6],f,f))
                            file.write("-------------------------------------------------Video Details-------------------------------------------------")
                            file.write("\n")
                            file.write("\nTitle: "+updated_video[0][0])
                            file.write("\nDescription: "+updated_video[0][1])
                            file.write("\nThumbnail Link: "+updated_video[0][2])
                            file.write("\nVideo Link: "+updated_video[0][3])
                            file.write("\nChannel Name: "+updated_video[0][4])
                            file.write("\nPublish Time: "+updated_video[0][5])
                            file.write("\n\n")
                            file.write("\n------------------------------------------Transcript Starts from here...----------------------------------------")
                            file.write("\n")
                            file.write(self.transcript)
                            with DatabaseConnection("DataBase.db") as connection:
                                cursor = connection.cursor()
                                cursor.execute("""UPDATE SHOW_CAPTURED SET title = ?,
                                                                    description = ?,
                                                                    thumbnail_link = ?,
                                                                    video_link = ?,
                                                                    channel_name = ?,
                                                                    publish_time = ?,
                                                                    searched = ?,
                                                                    searched_by = ?
                            WHERE video_link=?""",(updated_video[0][0],updated_video[0][1],updated_video[0][2],updated_video[0][3],updated_video[0][4],updated_video[0][5],video_capture[6],"keyword",video_capture[3]))
                            connection.commit()
                            self.log.insert(END,"->Captured Succesfully: {}\n\n".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                            self.log.yview(END)
                            self.logger.info("Captured Succesfully: {}".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                            self.cap_vi+=1
                            self.Captured_label.config(text = "Captured: {}".format(self.cap_vi))
                        except:
                            self.log.insert(END,"->Skipped it because it is Already Captured : {}\n\n".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                            self.log.yview(END)
                            self.logger.info("Skipped it because it is Already Captured : {}".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                            self.cap_vi+=1
                            self.Captured_label.config(text = "Captured: {}".format(self.cap_vi))
                            
                except:
                    self.log.insert(END,"->Transcript NOT FOUND! : {}\n\n".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                    self.log.yview(END)
                    self.logger.info("Transcript NOT FOUND! : {}".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                    self.skip_vi+=1
                    self.Skipped_label.config(text = "Skipped: {}".format(self.skip_vi))
                    
            elif video_capture[7] =="channel":
                try:
                    updated_video = Extract_Detail_of_URL_video(video_capture[3])
                    self.log.insert(END,"->Got video {} from youtube Api\n\n".format("https://www.youtube.com/watch?v="+video_capture[3]))
                    self.log.yview(END)
                    self.logger.info("Got videos {} from youtube Api".format("https://www.youtube.com/watch?v="+video_capture[3]))
                except:
                    self.log.insert(END,"->Youtube api key quota is exceeded\n\n")
                    self.log.yview(END)
                    self.logger.info("Youtube api key quota is exceeded")
                    self.Max_Result_error_Label.config(text = "Api Quota Exceeded",fg ="red")
                try:
                    os.mkdir("Files/Searched_By_Channel")
                    self.log.insert(END,"->Searched_By_Channel Directory has been created\n\n")
                    self.log.yview(END)
                    self.logger.info("Searched_By_Channel Directory has been created")
                except:
                    self.log.insert(END,"->Searched_By_Channel Directory is already available\n\n")
                    self.log.yview(END)
                    self.logger.info("Searched_By_Channel Directory is already available")
                    
                try:
                    os.mkdir("Files/Searched_By_Channel/{}".format(video_capture[6]))
                    self.log.insert(END,"->Searched_By_Channel/{} Directory has been created\n\n".format(video_capture[6]))
                    self.log.yview(END)
                    self.logger.info("Searched_By_Channel/{} Directory has been created".format(video_capture[6]))
                except:
                    self.log.insert(END,"->Searched_By_Channel/{} Directory already available\n\n".format(video_capture[6]))
                    self.log.yview(END)
                    self.logger.info("Searched_By_Channel/{} Directory already available".format(video_capture[6]))
                    
                try:
                    self.transcript = Get_Transcript(updated_video[0][3])
                    self.log.insert(END,"->Got Transcript : {}\n\n".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                    self.log.yview(END)
                    self.logger.info("Got Transcript : {}".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                    f = self.file_name(updated_video[0][0])
                    try:
                        os.mkdir("Files/Searched_By_Channel/{}/{}".format(video_capture[6],f))
                        self.log.insert(END,"->Searched_By_Channel/{}/{} Directory has been created\n\n".format(video_capture[6],f))
                        self.log.yview(END)
                        self.logger.info("Searched_By_Channel/{}/{} Directory has been created".format(video_capture[6],f))
                    except:
                        self.log.insert(END,"->Searched_By_Channel/{}/{} Directory is already available\n\n".format(video_capture[6],f))
                        self.log.yview(END)
                        self.logger.info("Searched_By_Channel/{}/{} Directory is already available".format(video_capture[6],f))
                        
                    with open("Files/Searched_By_Channel/{}/{}/{}.txt".format(video_capture[6],f,f),"w",encoding="utf-8") as file:
                        try:
                            r = requests.get(updated_video[0][2])
                            b = BytesIO(r.content)
                            img = Image.open(b)
                            img.save("Files/Searched_By_Channel/{}/{}/{}.jpeg".format(video_capture[6],f,f))
                            file.write("-------------------------------------------------Video Details-------------------------------------------------")
                            file.write("\n")
                            file.write("\nTitle: "+updated_video[0][0])
                            file.write("\nDescription: "+updated_video[0][1])
                            file.write("\nThumbnail Link: "+updated_video[0][2])
                            file.write("\nVideo Link: "+updated_video[0][3])
                            file.write("\nChannel Name: "+updated_video[0][4])
                            file.write("\nPublish Time: "+updated_video[0][5])
                            file.write("\n\n")
                            file.write("\n------------------------------------------Transcript Starts from here...----------------------------------------")
                            file.write("\n")
                            file.write(self.transcript)
                            with DatabaseConnection("DataBase.db") as connection:
                                cursor = connection.cursor()
                                cursor.execute("""UPDATE SHOW_CAPTURED SET title = ?,
                                                                    description = ?,
                                                                    thumbnail_link = ?,
                                                                    video_link = ?,
                                                                    channel_name = ?,
                                                                    publish_time = ?,
                                                                    searched = ?,
                                                                    searched_by = ?
                            WHERE video_link=?""",(updated_video[0][0],updated_video[0][1],updated_video[0][2],updated_video[0][3],updated_video[0][4],updated_video[0][5],video_capture[6],"keyword",video_capture[3]))
                            connection.commit()
                            self.log.insert(END,"->Captured Succesfully: {}\n\n".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                            self.log.yview(END)
                            self.logger.info("Captured Succesfully: {}".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                            self.cap_vi+=1
                            self.Captured_label.config(text = "Captured: {}".format(self.cap_vi))
                        except Exception:
                            self.log.insert(END,"->Skipped it because it is Already Captured : {}\n\n".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                            self.log.yview(END)
                            self.logger.info("Skipped it because it is Already Captured : {}".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                            self.cap_vi+=1
                            self.Captured_label.config(text = "Captured: {}".format(self.cap_vi))
                except:
                    self.log.insert(END,"->Transcript NOT FOUND! : {}\n\n".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                    self.log.yview(END)
                    self.logger.info("Transcript NOT FOUND! : {}".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                    self.skip_vi+=1
                    self.Skipped_label.config(text = "Skipped: {}".format(self.skip_vi))
                    
            elif video_capture[7] == "url":
                try:
                    updated_video = Extract_Detail_of_URL_video(video_capture[3])
                    self.log.insert(END,"->Got video {} from youtube Api\n\n".format("https://www.youtube.com/watch?v="+video_capture[3]))
                    self.log.yview(END)
                    self.logger.info("Got videos {} from youtube Api".format("https://www.youtube.com/watch?v="+video_capture[3]))
                except:
                    self.log.insert(END,"->Youtube api key quota is exceeded\n\n")
                    self.log.yview(END)
                    self.logger.info("Youtube api key quota is exceeded")
                    self.Max_Result_error_Label.config(text = "Api Quota Exceeded",fg ="red")
                    
                try:
                    os.mkdir("Files/Searched_By_URL")
                    self.log.insert(END,"->Searched_By_URL Directory has been created\n\n")
                    self.log.yview(END)
                    self.logger.info("Searched_By_URL Directory has been created")
                except:
                    self.log.insert(END,"->Searched_By_URL Directory is already available\n\n")
                    self.log.yview(END)
                    self.logger.info("Searched_By_URL Directory is already available")
                    
                try:
                    os.mkdir("Files/Searched_By_URL/{}".format(video_capture[6]))
                    self.log.insert(END,"->Searched_By_URL/{} Directory has been created\n\n".format(video_capture[6]))
                    self.log.yview(END)
                    self.logger.info("Searched_By_URL/{} Directory has been created".format(video_capture[6]))
                except:
                    self.log.insert(END,"->Searched_By_URL/{} Directory is already available\n\n".format(video_capture[6]))
                    self.log.yview(END)
                    self.logger.info("Searched_By_URL/{} Directory is already available".format(video_capture[6]))
                    
                try:
                    self.transcript = Get_Transcript(updated_video[0][3])
                    self.log.insert(END,"->Got Transcript : {}\n\n".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                    self.log.yview(END)
                    self.logger.info("Got Transcript : {}".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                    f = self.file_name(updated_video[0][0])
                    try:
                        os.mkdir("Files/Searched_By_URL/{}/{}".format(video_capture[6],f))
                        self.log.insert(END,"->Searched_By_URL/{}/{} Directory has been created\n\n".format(video_capture[6],f))
                        self.log.yview(END)
                        self.logger.info("Searched_By_URL/{}/{} Directory has been created".format(video_capture[6],f))
                    except:
                        self.log.insert(END,"->Searched_By_URL/{}/{} Directory is already available\n\n".format(video_capture[6],f))
                        self.log.yview(END)
                        self.logger.info("Searched_By_URL/{}/{} Directory is already available".format(video_capture[6],f))
                        
                    with open("Files/Searched_By_URL/{}/{}/{}.txt".format(video_capture[6],f,f),"w",encoding="utf-8") as file:
                        try:
                            r = requests.get(updated_video[0][2])
                            b = BytesIO(r.content)
                            img = Image.open(b)
                            img.save("Files/Searched_By_URL/{}/{}/{}.jpeg".format(video_capture[6],f,f))
                            file.write("-------------------------------------------------Video Details-------------------------------------------------")
                            file.write("\n")
                            file.write("\nTitle: "+updated_video[0][0])
                            file.write("\nDescription: "+updated_video[0][1])
                            file.write("\nThumbnail Link: "+updated_video[0][2])
                            file.write("\nVideo Link: "+updated_video[0][3])
                            file.write("\nChannel Name: "+updated_video[0][4])
                            file.write("\nPublish Time: "+updated_video[0][5])
                            file.write("\n\n")
                            file.write("\n------------------------------------------Transcript Starts from here...----------------------------------------")
                            file.write("\n")
                            file.write(self.transcript)
                            with DatabaseConnection("DataBase.db") as connection:
                                cursor = connection.cursor()
                                cursor.execute("""UPDATE SHOW_CAPTURED SET title = ?,
                                                                    description = ?,
                                                                    thumbnail_link = ?,
                                                                    video_link = ?,
                                                                    channel_name = ?,
                                                                    publish_time = ?,
                                                                    searched = ?,
                                                                    searched_by = ?
                            WHERE video_link=?""",(updated_video[0][0],updated_video[0][1],updated_video[0][2],updated_video[0][3],updated_video[0][4],updated_video[0][5],video_capture[6],"keyword",video_capture[3]))
                            connection.commit()
                            self.log.insert(END,"->Captured Succesfully: {}\n\n".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                            self.log.yview(END)
                            self.logger.info("Captured Succesfully: {}".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                            self.cap_vi+=1
                            self.Captured_label.config(text = "Captured: {}".format(self.cap_vi))
                        except :
                            self.log.insert(END,"->Skipped it because it is Already Captured : {}\n\n".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                            self.log.yview(END)
                            self.logger.info("Skipped it because it is Already Captured : {}".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                            self.cap_vi+=1
                            self.Captured_label.config(text = "Captured: {}".format(self.cap_vi))
                except:
                    self.log.insert(END,"->Transcript NOT FOUND! : {}\n\n".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                    self.log.yview(END)
                    self.logger.info("Transcript NOT FOUND! : {}".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                    self.skip_vi+=1
                    self.Skipped_label.config(text = "Skipped: {}".format(self.skip_vi))
        self.Start_Button.config(state =NORMAL )
        self.Stop_Button.config(state = DISABLED)
        self.show_skipped.config(state  = NORMAL)
        self.show_captured.config(state = NORMAL)
        self.Sort_By.config(state = NORMAL)
        self.Video_Duration.config(state = NORMAL)

    #function to check the date of schedule and starts updating data on schedule time
    def Schedule(self):
        with DatabaseConnection("DataBase.db") as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM LOG")
            log_data_sch = cursor.fetchall()
            connection.commit()
        today = datetime.date.today()
        sch = []
        for data in log_data_sch:
            if data[3]!="None":
                delta = today-data[4]
                if delta.days >= int(data[3]):
                    sch.append(data)
        if len(sch) > 0:
            value = messagebox.askyesno(title = "Scheduled Update",message = "Do you want to run the updating Process?")
            if value:
                for s in sch:
                    if s[6] == "keyword":
                        self.Clear_Frame_5()
                        self.show_log()
                        self.Use_CheckBtn.set(1)
                        self.Keyword_Var.set(s[2])
                        self.Max_Result.set(s[5])
                        self.Thread_Start()
                    if s[6] == "channel":
                        self.Clear_Frame_5()
                        self.show_log()
                        self.Use_CheckBtn.set(2)
                        self.Channel_Var.set(s[2])
                        self.Max_Result.set(s[5])
                        self.Thread_Start()
                    if s[6] == "url":
                        self.Clear_Frame_5()
                        self.show_log()
                        self.Use_CheckBtn.set(3)
                        self.URL_Var.set(s[2])
                        self.Max_Result.set(s[5])
                        self.Thread_Start()


    #function of option menu for filter of youtube videos 
    def Filter_func(self):
        self.Sort_By_label = Label(self.Frame_7,text = "Sort by:")
        self.Sort_By  =OptionMenu(self.Frame_7,self.Sort_By_var,"searchSortUnspecified","date","rating","relevance",
                                    "title","viewCount")
        self.Video_Duration_label = Label(self.Frame_7,text = "Video Duration:")
        self.Video_Duration = OptionMenu(self.Frame_7,self.Video_Duration_var,"videoDurationUnspecified","any","long","medium","short")
        self.Video_Duration.pack(fill = "x",side = "bottom")
        self.Video_Duration_label.pack(side = "bottom",anchor = "w")
        self.Sort_By.pack(fill = "x",side = "bottom")
        self.Sort_By_label.pack(side = "bottom",anchor = "w")

    #function to disable when clicked on start
    def Start_Disable_1(self):
        self.log_button.config(state = DISABLED)
        self.log_options_search.config(state = DISABLED)
        self.log_options_time.config(state = DISABLED)
        self.Max_Result_label.config(text = "Max Result: {}".format(0))
        self.Skipped_label.config(text = "Skipped: {}".format(0))
        self.Skipped_label.update()
        self.Captured_label.config(text = "Captured: {}".format(0))
        self.Captured_label.update()
        self.Stop_Button.config(state = NORMAL)
        self.Start_Button.config(state = DISABLED)
        self.show_captured.config(state = DISABLED)
        self.show_skipped.config(state = DISABLED)

        if (self.In_Use == 1):
            self.Max_Result_Entry.config(state = DISABLED)

            self.Use_Channels.config(state = DISABLED)
            self.Use_URLs.config(state = DISABLED)
                    
            self.Keyword_Entry.config(state = DISABLED)
            self.Choose_Keywords_Button.config(state = DISABLED)

        elif(self.In_Use == 2):
            self.Max_Result_Entry.config(state = DISABLED)

            self.Use_Keywords.config(state = DISABLED)
            self.Use_URLs.config(state = DISABLED)

            self.Choose_Channels_Button.config(state = DISABLED)
            self.Channel_Entry.config(state = DISABLED)

        elif(self.In_Use == 3):
            self.Max_Result_Entry.config(state = DISABLED)

            self.Use_Keywords.config(state = DISABLED)
            self.Use_Channels.config(state = DISABLED)

            self.Choose_URLs_Button.config(state = DISABLED)
            self.URL_Entry.config(state = DISABLED)

    #function to enable disable objects when start comes to end 
    def Start_Disable_2(self):
        self.Convert_to_Start()
        self.log_button.config(state = NORMAL)
        self.log_options_search.config(state = NORMAL)
        self.log_options_time.config(state = NORMAL)
        self.Start_Button.config(state = NORMAL)
        self.show_captured.config(state = NORMAL)
        self.show_skipped.config(state = NORMAL)

        if (self.In_Use == 1):
            self.Max_Result_Entry.config(state = NORMAL)

            self.Use_Channels.config(state = NORMAL)
            self.Use_URLs.config(state = NORMAL)
        
            self.Choose_Keywords_Button.config(state = NORMAL)
            self.Keyword_Entry.config(state = NORMAL)

        if(self.In_Use == 2):
            self.Max_Result_Entry.config(state = NORMAL)

            self.Use_Keywords.config(state = NORMAL)
            self.Use_URLs.config(state = NORMAL)

            self.Choose_Channels_Button.config(state = NORMAL)
            self.Channel_Entry.config(state = NORMAL)

        if(self.In_Use == 3):
            self.Use_Keywords.config(state = NORMAL)
            self.Use_Channels.config(state = NORMAL)

            self.Choose_URLs_Button.config(state = NORMAL)
            self.URL_Entry.config(state = NORMAL)
        self.Stop_Button.config(state = DISABLED)

    def run(self):
        with DatabaseConnection("DataBase.db") as connection:
            cursor = connection.cursor()
            cursor.execute("""DELETE from rerun""")
            connection.commit()
        if self.Use_CheckBtn.get() == 1:
            if self.manual_videos != []:
                for video in self.manual_videos:
                    with DatabaseConnection("DataBase.db") as connection:
                        cursor = connection.cursor()
                        cursor.execute("""INSERT INTO RERUN VALUES(?,?,?,?,?,?,?,?)
                        """,(video[0],video[1],video[2],video[3],video[4],video[5],video[4],"keyword"))
                        connection.commit()
            elif self.rerun_videos != []:
                for video in self.rerun_videos:
                    with DatabaseConnection("DataBase.db") as connection:
                        cursor = connection.cursor()
                        cursor.execute("""INSERT INTO RERUN VALUES(?,?,?,?,?,?,?,?)
                        """,(video[0],video[1],video[2],video[3],video[4],video[5],video[4],"keyword"))
                        connection.commit()
        if self.Use_CheckBtn.get() == 2:
            if self.manual_videos_cha != []:
                for video in self.manual_videos_cha:
                    
                    with DatabaseConnection("DataBase.db") as connection:
                        cursor = connection.cursor()
                        cursor.execute("""INSERT INTO RERUN VALUES(?,?,?,?,?,?,?,?)
                        """,(video[0],video[1],video[2],video[3],video[4],video[5],video[4],"keyword"))
                        connection.commit()
            elif self.rerun_videos != []:
                for video in self.rerun_videos:
                    with DatabaseConnection("DataBase.db") as connection:
                        cursor = connection.cursor()
                        cursor.execute("""INSERT INTO RERUN VALUES(?,?,?,?,?,?,?,?)
                        """,(video[0],video[1],video[2],video[3],video[4],video[5],video[4],"keyword"))
                        connection.commit()
        if self.Use_CheckBtn.get() == 3:
            if self.videos_url != []:
                for video in self.videos_url:
                    with DatabaseConnection("DataBase.db") as connection:
                        cursor = connection.cursor()
                        cursor.execute("""INSERT INTO RERUN VALUES(?,?,?,?,?,?,?,?)
                        """,(video[0],video[1],video[2],video[3],video[4],video[5],video[4],"keyword"))
                        connection.commit()
            elif self.rerun_videos != []:
                for video in self.rerun_videos:
                    with DatabaseConnection("DataBase.db") as connection:
                        cursor = connection.cursor()
                        cursor.execute("""INSERT INTO RERUN VALUES(?,?,?,?,?,?,?,?)
                        """,(video[0],video[1],video[2],video[3],video[4],video[5],video[4],"keyword"))
                        connection.commit()
        
    def rerun_func(self):
        self.rerun_videos = []
        self.skip_vi = 0
        self.cap_vi = 0
        self.stp =0
        self.Rerun_Button.config(state = DISABLED)
        self.Start_Button.config(state = DISABLED)
        self.Stop_Button.config(state = NORMAL)
        self.show_captured.config(state = DISABLED)
        self.show_skipped.config(state = DISABLED)
        with DatabaseConnection("DataBase.db") as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM rerun")
            videos_captured = cursor.fetchall()
            connection.commit()
        self.log.insert(END,"->Rerunning Capturing process from rerun database\n\n")
        self.log.yview(END)
        self.logger.info("Rerunning Capturing process from rerun database")
        self.Max_Result_label.config(text = "Max Result: {}".format(len(videos_captured)))
        for video_capture in videos_captured:
            if self.stp:
                self.Rerun_Button.pack_forget()
                break
            if video_capture[7]=="keyword":
                try:
                    updated_video = Extract_Detail_of_URL_video(video_capture[3])
                    self.log.insert(END,"->Got video {} from youtube Api\n\n".format("https://www.youtube.com/watch?v="+video_capture[3]))
                    self.log.yview(END)
                    self.logger.info("Got videos {} from youtube Api".format("https://www.youtube.com/watch?v="+video_capture[3]))
                except:
                    self.log.insert(END,"->Youtube api key quota is exceeded\n\n")
                    self.log.yview(END)
                    self.logger.info("Youtube api key quota is exceeded")
                    self.Max_Result_error_Label.config(text = "Api Quota Exceeded",fg ="red")
                
                try:
                    os.mkdir("Files/Searched_By_Keyword")
                    self.log.insert(END,"->Searched_By_Keyword Directory has been created\n\n")
                    self.log.yview(END)
                    self.logger.info("Searched_By_Keyword Directory has been created")
                except:
                    self.log.insert(END,"->Searched_By_Keyword Directory is already available\n\n")
                    self.log.yview(END)
                    self.logger.info("Searched_By_Keyword Directory is already available")
                    
                try:
                    os.mkdir("Files/Searched_By_Keyword/{}".format(video_capture[6]))
                    self.log.insert(END,"->Searched_By_Keyword/{} Directory has been created\n\n".format(video_capture[6]))
                    self.log.yview(END)
                    self.logger.info("Searched_By_Keyword/{} Directory has been created".format(video_capture[6]))
                except:
                    self.log.insert(END,"->Searched_By_Keyword/{} Directory already available\n\n".format(video_capture[6]))
                    self.log.yview(END)
                    self.logger.info("Searched_By_Keyword/{} Directory already available".format(video_capture[6]))
                    
                try:
                    self.transcript = Get_Transcript(updated_video[0][3])
                    self.log.insert(END,"->Got Transcript : {}\n\n".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                    self.log.yview(END)
                    self.logger.info("Got Transcript : {}".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                    f = self.file_name(updated_video[0][0])
                    try:
                        os.mkdir("Files/Searched_By_Keyword/{}/{}".format(video_capture[6],f))
                        self.log.insert(END,"->Searched_By_Keyword/{}/{} Directory has been created\n\n".format(video_capture[6],f))
                        self.log.yview(END)
                        self.logger.info("Searched_By_Keyword/{}/{} Directory has been created".format(video_capture[6],f))
                    except:
                        self.log.insert(END,"->Searched_By_Keyword/{}/{} Directory is already available\n\n".format(video_capture[6],f))
                        self.log.yview(END)
                        self.logger.info("Searched_By_Keyword/{}/{} Directory is already available".format(video_capture[6],f))
                        
                    with open("Files/Searched_By_Keyword/{}/{}/{}.txt".format(video_capture[6],f,f),"w",encoding="utf-8") as file:
                        try:
                            r = requests.get(updated_video[0][2])
                            b = BytesIO(r.content)
                            img = Image.open(b)
                            img.save("Files/Searched_By_Keyword/{}/{}/{}.jpeg".format(video_capture[6],f,f))
                            file.write("-------------------------------------------------Video Details-------------------------------------------------")
                            file.write("\n")
                            file.write("\nTitle: "+updated_video[0][0])
                            file.write("\nDescription: "+updated_video[0][1])
                            file.write("\nThumbnail Link: "+updated_video[0][2])
                            file.write("\nVideo Link: "+updated_video[0][3])
                            file.write("\nChannel Name: "+updated_video[0][4])
                            file.write("\nPublish Time: "+updated_video[0][5])
                            file.write("\n\n")
                            file.write("\n------------------------------------------Transcript Starts from here...----------------------------------------")
                            file.write("\n")
                            file.write(self.transcript)
                            with DatabaseConnection("DataBase.db") as connection:
                                cursor = connection.cursor()
                                cursor.execute("""INSERT INTO SHOW_CAPTURED VALUES(?,?,?,?,?,?,?,?)
                                """,(updated_video[0][0],updated_video[0][1],updated_video[0][2],updated_video[0][3],updated_video[0][4],updated_video[0][5],video_capture[6],"keyword"))
                                connection.commit()
                                self.cap_vi+=1
                                self.Captured_label.config(text = "Captured: {}".format(self.cap_vi))
                                self.Captured_label.update()
                                self.log.insert(END,"->Captured Succesfully: {}\n\n".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                                self.log.yview(END)
                                self.logger.info("Captured Succesfully: {}".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                        except:
                            self.cap_vi+=1
                            self.Captured_label.config(text = "Captured: {}".format(self.cap_vi))
                            self.Captured_label.update()
                            self.log.insert(END,"->Skipped it because it is Already Captured : {}\n\n".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                            self.log.yview(END)
                            self.logger.info("Skipped it because it is Already Captured : {}".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                            
                except:
                    try:
                        with DatabaseConnection("DataBase.db") as connection:
                            cursor = connection.cursor()
                            cursor.execute("""INSERT INTO SHOW_SKIPPED VALUES(?,?,?,?,?,?,?,?)
                            """,(updated_video[0][0],updated_video[0][1],updated_video[0][2],updated_video[0][3],updated_video[0][4],updated_video[0][5],video_capture[6],"keyword"))
                            connection.commit()

                            cursor.execute("""DELETE FROM SHOW_CAPTURED WHERE video_link = ?""",(video_capture[3]))
                            connection.commit()
                            self.skip_vi+=1
                            self.Skipped_label.config(text = "Skipped: {}".format(self.skip_vi))
                            self.Skipped_label.update()
                            self.log.insert(END,"->Transcript Not Found! - Skipped : {}\n\n".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                            self.log.yview(END)
                            self.logger.info("Transcript Not Found! - Skipped : {}".format("https://www.youtube.com/watch?v="+updated_video[0][3]))

                    except:
                        self.skip_vi+=1
                        self.Skipped_label.config(text = "Skipped: {}".format(self.skip_vi))
                        self.Skipped_label.update()
                        self.log.insert(END,"->Already in Skipped : {}\n\n".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                        self.log.yview(END)
                        self.logger.info("Already in Skipped : {}".format("https://www.youtube.com/watch?v="+updated_video[0][3])) 
                        
            elif video_capture[7] =="channel":
                try:
                    updated_video = Extract_Detail_of_URL_video(video_capture[3])
                    self.log.insert(END,"->Got video {} from youtube Api\n\n".format("https://www.youtube.com/watch?v="+video_capture[3]))
                    self.log.yview(END)
                    self.logger.info("Got videos {} from youtube Api".format("https://www.youtube.com/watch?v="+video_capture[3]))
                except:
                    self.log.insert(END,"->Youtube api key quota is exceeded\n\n")
                    self.log.yview(END)
                    self.logger.info("Youtube api key quota is exceeded")
                    self.Max_Result_error_Label.config(text = "Api Quota Exceeded",fg ="red")
                    
                try:
                    os.mkdir("Files/Searched_By_Channel")
                    self.log.insert(END,"->Searched_By_Channel Directory has been created\n\n")
                    self.log.yview(END)
                    self.logger.info("Searched_By_Channel Directory has been created")
                except:
                    self.log.insert(END,"->Searched_By_Channel Directory is already available\n\n")
                    self.log.yview(END)
                    self.logger.info("Searched_By_Channel Directory is already available")
                    
                try:
                    os.mkdir("Files/Searched_By_Channel/{}".format(video_capture[6]))
                    self.log.insert(END,"->Searched_By_Channel/{} Directory has been created\n\n".format(video_capture[6]))
                    self.log.yview(END)
                    self.logger.info("Searched_By_Channel/{} Directory has been created".format(video_capture[6]))
                except:
                    self.log.insert(END,"->Searched_By_Channel/{} Directory already available\n\n".format(video_capture[6]))
                    self.log.yview(END)
                    self.logger.info("Searched_By_Channel/{} Directory already available".format(video_capture[6]))
                   
                try:
                    self.transcript = Get_Transcript(updated_video[0][3])
                    self.log.insert(END,"->Got Transcript : {}\n\n".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                    self.log.yview(END)
                    self.logger.info("Got Transcript : {}".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                    f = self.file_name(updated_video[0][0])
                    try:
                        os.mkdir("Files/Searched_By_Channel/{}/{}".format(video_capture[6],f))
                        self.log.insert(END,"->Searched_By_Channel/{}/{} Directory has been created\n\n".format(video_capture[6],f))
                        self.log.yview(END)
                        self.logger.info("Searched_By_Channel/{}/{} Directory has been created".format(video_capture[6],f))
                    except:
                        self.log.insert(END,"->Searched_By_Channel/{}/{} Directory is already available\n\n".format(video_capture[6],f))
                        self.log.yview(END)
                        self.logger.info("Searched_By_Channel/{}/{} Directory is already available".format(video_capture[6],f))
                        
                    with open("Files/Searched_By_Channel/{}/{}/{}.txt".format(video_capture[6],f,f),"w",encoding="utf-8") as file:
                        try:
                            r = requests.get(updated_video[0][2])
                            b = BytesIO(r.content)
                            img = Image.open(b)
                            img.save("Files/Searched_By_Channel/{}/{}/{}.jpeg".format(video_capture[6],f,f))
                            file.write("-------------------------------------------------Video Details-------------------------------------------------")
                            file.write("\n")
                            file.write("\nTitle: "+updated_video[0][0])
                            file.write("\nDescription: "+updated_video[0][1])
                            file.write("\nThumbnail Link: "+updated_video[0][2])
                            file.write("\nVideo Link: "+updated_video[0][3])
                            file.write("\nChannel Name: "+updated_video[0][4])
                            file.write("\nPublish Time: "+updated_video[0][5])
                            file.write("\n\n")
                            file.write("\n------------------------------------------Transcript Starts from here...----------------------------------------")
                            file.write("\n")
                            file.write(self.transcript)
                            with DatabaseConnection("DataBase.db") as connection:
                                cursor = connection.cursor()
                                cursor.execute("""INSERT INTO SHOW_CAPTURED VALUES(?,?,?,?,?,?,?,?)
                                """,(updated_video[0][0],updated_video[0][1],updated_video[0][2],updated_video[0][3],updated_video[0][4],updated_video[0][5],video_capture[6],"keyword"))
                                connection.commit()
                                self.cap_vi+=1
                                self.Captured_label.config(text = "Captured: {}".format(self.cap_vi))
                                self.Captured_label.update()
                                self.log.insert(END,"->Captured Succesfully: {}\n\n".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                                self.log.yview(END)
                                self.logger.info("Captured Succesfully: {}".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                        except:
                            self.cap_vi+=1
                            self.Captured_label.config(text = "Captured: {}".format(self.cap_vi))
                            self.Captured_label.update()
                            self.log.insert(END,"->Skipped it because it is Already Captured : {}\n\n".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                            self.log.yview(END)
                            self.logger.info("Skipped it because it is Already Captured : {}".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                            
                except:
                    try:
                        with DatabaseConnection("DataBase.db") as connection:
                            cursor = connection.cursor()
                            cursor.execute("""INSERT INTO SHOW_SKIPPED VALUES(?,?,?,?,?,?,?,?) 
                                    """,(updated_video[0][0],updated_video[0][1],updated_video[0][2],updated_video[0][3],updated_video[0][4],updated_video[0][5],video_capture[6],"keyword"))
                            connection.commit()
                            cursor.execute("""DELETE FROM SHOW_CAPTURED WHERE video_link = ?""",(video_capture[3]))
                            connection.commit()
                            self.skip_vi+=1
                            self.Skipped_label.config(text = "Skipped: {}".format(self.skip_vi))
                            self.Skipped_label.update()
                            self.log.insert(END,"->Transcript Not Found! - Skipped : {}\n\n".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                            self.log.yview(END)
                            self.logger.info("Transcript Not Found! - Skipped : {}".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                    except: 
                        self.skip_vi+=1
                        self.Skipped_label.config(text = "Skipped: {}".format(self.skip_vi))
                        self.Skipped_label.update()
                        self.log.insert(END,"->Already in Skipped : {}\n\n".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                        self.log.yview(END)
                        self.logger.info("Already in Skipped : {}".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                        
            elif video_capture[7] == "url":
                try:
                    updated_video = Extract_Detail_of_URL_video(video_capture[3])
                    self.log.insert(END,"->Got video {} from youtube Api\n\n".format("https://www.youtube.com/watch?v="+video_capture[3]))
                    self.log.yview(END)
                    self.logger.info("Got videos {} from youtube Api".format("https://www.youtube.com/watch?v="+video_capture[3]))
                except:
                    self.log.insert(END,"->Youtube api key quota is exceeded\n\n")
                    self.log.yview(END)
                    self.logger.info("Youtube api key quota is exceeded")
                    self.Max_Result_error_Label.config(text = "Api Quota Exceeded",fg ="red")
                    
                try:
                    os.mkdir("Files/Searched_By_URL")
                    self.log.insert(END,"->Searched_By_URL Directory has been created\n\n")
                    self.log.yview(END)
                    self.logger.info("Searched_By_URL Directory has been created")
                except:
                    self.log.insert(END,"->Searched_By_URL Directory is already available\n\n")
                    self.log.yview(END)
                    self.logger.info("Searched_By_URL Directory is already available")
                    
                try:
                    os.mkdir("Files/Searched_By_URL/{}".format(video_capture[6]))
                    self.log.insert(END,"->Searched_By_URL/{} Directory has been created\n\n".format(video_capture[6]))
                    self.log.yview(END)
                    self.logger.info("Searched_By_URL/{} Directory has been created".format(video_capture[6]))
                except:
                    self.log.insert(END,"->Searched_By_URL/{} Directory is already available\n\n".format(video_capture[6]))
                    self.log.yview(END)
                    self.logger.info("Searched_By_URL/{} Directory is already available".format(video_capture[6]))
                    
                try:
                    self.transcript = Get_Transcript(updated_video[0][3])
                    self.log.insert(END,"->Got Transcript : {}\n\n".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                    self.log.yview(END)
                    self.logger.info("Got Transcript : {}".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                    f = self.file_name(updated_video[0][0])
                    try:
                        os.mkdir("Files/Searched_By_URL/{}/{}".format(video_capture[6],f))
                        self.log.insert(END,"->Searched_By_URL/{}/{} Directory has been created\n\n".format(video_capture[6],f))
                        self.log.yview(END)
                        self.logger.info("Searched_By_URL/{}/{} Directory has been created".format(video_capture[6],f))
                    except:
                        self.log.insert(END,"->Searched_By_URL/{}/{} Directory is already available\n\n".format(video_capture[6],f))
                        self.log.yview(END)
                        self.logger.info("Searched_By_URL/{}/{} Directory is already available".format(video_capture[6],f))
                        
                    with open("Files/Searched_By_URL/{}/{}/{}.txt".format(video_capture[6],f,f),"w",encoding="utf-8") as file:
                        try:
                            r = requests.get(updated_video[0][2])
                            b = BytesIO(r.content)
                            img = Image.open(b)
                            img.save("Files/Searched_By_URL/{}/{}/{}.jpeg".format(video_capture[6],f,f))
                            file.write("-------------------------------------------------Video Details-------------------------------------------------")
                            file.write("\n")
                            file.write("\nTitle: "+updated_video[0][0])
                            file.write("\nDescription: "+updated_video[0][1])
                            file.write("\nThumbnail Link: "+updated_video[0][2])
                            file.write("\nVideo Link: "+updated_video[0][3])
                            file.write("\nChannel Name: "+updated_video[0][4])
                            file.write("\nPublish Time: "+updated_video[0][5])
                            file.write("\n\n")
                            file.write("\n------------------------------------------Transcript Starts from here...----------------------------------------")
                            file.write("\n")
                            file.write(self.transcript)
                            with DatabaseConnection("DataBase.db") as connection:
                                cursor = connection.cursor()
                                cursor.execute("""INSERT INTO SHOW_CAPTURED VALUES(?,?,?,?,?,?,?,?)
                                """,(updated_video[0][0],updated_video[0][1],updated_video[0][2],updated_video[0][3],updated_video[0][4],updated_video[0][5],video_capture[6],"keyword"))
                                connection.commit()
                                self.cap_vi+=1
                                self.Captured_label.config(text = "Captured: {}".format(self.cap_vi))
                                self.Captured_label.update()
                                self.log.insert(END,"->Captured Succesfully: {}\n\n".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                                self.log.yview(END)
                                self.logger.info("Captured Succesfully: {}".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                        except:
                            self.cap_vi+=1
                            self.Captured_label.config(text = "Captured: {}".format(self.cap_vi))
                            self.Captured_label.update()
                            self.log.insert(END,"->Skipped it because it is Already Captured : {}\n\n".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                            self.log.yview(END)
                            self.logger.info("Skipped it because it is Already Captured : {}".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                            
                except:
                    try:
                        with DatabaseConnection("DataBase.db") as connection:
                            cursor = connection.cursor()
                            cursor.execute("""INSERT INTO SHOW_SKIPPED VALUES(?,?,?,?,?,?,?,?) 
                                    """,(updated_video[0][0],updated_video[0][1],updated_video[0][2],updated_video[0][3],updated_video[0][4],updated_video[0][5],video_capture[6],"keyword"))
                            connection.commit()
                            cursor.execute("""DELETE FROM SHOW_CAPTURED WHERE video_link = ?""",(video_capture[3]))
                            connection.commit()
                            self.skip_vi+=1
                            self.Skipped_label.config(text = "Skipped: {}".format(self.skip_vi))
                            self.Skipped_label.update()
                            self.log.insert(END,"->Transcript Not Found! - Skipped : {}\n\n".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                            self.log.yview(END)
                            self.logger.info("Transcript Not Found! - Skipped : {}".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                    except: 
                        self.skip_vi+=1
                        self.Skipped_label.config(text = "Skipped: {}".format(self.skip_vi))
                        self.Skipped_label.update()
                        self.log.insert(END,"->Already in Skipped : {}\n\n".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                        self.log.yview(END)
                        self.logger.info("Already in Skipped : {}".format("https://www.youtube.com/watch?v="+updated_video[0][3]))
                        
        self.Show_Captured_Start_Func()
        self.Show_Skipped_Start_Func()
        self.Max_Result_error_Label.config(text = "Error Box.",fg ="black")
        self.show_captured.config(state = NORMAL)
        self.show_skipped.config(state = NORMAL)
        self.Start_Button.config(state = NORMAL)
        self.Stop_Button.config(state  = DISABLED)
        self.Rerun_Button.pack_forget()
        self.rerun_videos = []
        self.stp =0
    


    def Thread_Rerun(self):
        self.thread_rerun = Thread(target = self.rerun_func)
        self.thread_rerun.start()
    # rerun button function 
    def rerun(self):
        self.Rerun_Button = Button(self.Frame_4, text = "Rerun", 
                                        relief = "raised",bg = "#0060de",bd = 3,fg = 'white',
                                        font =("helvetica",9,"bold"),
                                        activeforeground = "#0a5ac4", activebackground = "#89b5f0",command = self.Thread_Rerun)
        self.Rerun_Button.pack(side = "bottom",anchor = "w", padx = 10, pady = 10,fill = "x")
    
    #function to get the data when searched by url
    def Multiple_URLs(self):
        self.add_to_log()
        self.rerun_videos = []
        self.skip_vi = 0
        self.cap_vi = 0
        if self.Manually_var.get() == 0 :
            if self.Choose_Text_File =="":
                keys = self.URL_Var.get()
                keys = keys.split(',')
            else:
                with open(self.Choose_Text_File,"r") as file:
                    keys = file.read().split(',')
            for n in range(len(keys)):
                keys[n] = keys[n].split("?v=")[-1]
            self.Max_Result_label.config(text = "Max Result: {}".format(len(keys)))
            self.Max_Result_label.update()
            self.process_URL(keys)
        if self.Manually_var.get() == 1:
            self.Max_Result_label.config(text = "Max Result: {}".format(len(self.videos_url)))
            self.Max_Result_label.update()
            for i in range(len(self.videos_url)):
                if self.stp:
                    break
                if self.Use_CheckBtns_var_url[i].get() == 1:
                    try:
                        os.mkdir("Files/Searched_By_URL")
                        self.log.insert(END,"->Searched_By_URL Directory has been created\n\n")
                        self.log.yview(END)
                        self.logger.info("Searched_By_URL Directory has been created")
                    except:
                        self.log.insert(END,"->Searched_By_URL is already available\n\n")
                        self.log.yview(END)
                        self.logger.info("Searched_By_URL is already available")
                        
                    try:
                        os.mkdir("Files/Searched_By_URL/{}".format(self.videos_url[i][4]))
                        self.log.insert(END,"->Searched_By_URL/{} Directory has been created\n\n".format(self.videos_url[i][4]))
                        self.log.yview(END)
                        self.logger.info("Searched_By_URL/{} Directory has been created".format(self.videos_url[i][4]))
                    except:
                        self.log.insert(END,"->Searched_By_URL/{} Directory is already available\n\n".format(self.videos_url[i][4]))
                        self.log.yview(END)
                        self.logger.info("Searched_By_URL/{} Directory is already available".format(self.videos_url[i][4]))
                        
                    try:
                        self.transcript = Get_Transcript(self.videos_url[i][3])
                        self.log.insert(END,"->Got the Transcript for {}\n\n".format(self.videos_url[i][3]))
                        self.log.yview(END)
                        self.logger.info("Got the Transcript for {}".format(self.videos_url[i][3]))
                        f = self.file_name(self.videos_url[i][0])
                        try:
                            os.mkdir("Files/Searched_By_URL/{}/{}".format(self.videos_url[i][4],f))
                            self.log.insert(END,"->Searched_By_URL/{}/{} Directory has been created\n\n".format(self.videos_url[i][4],f))
                            self.log.yview(END)
                            self.logger.info("Searched_By_URL/{}/{} Directory has been created".format(self.videos_url[i][4],f))
                        except:
                            self.log.insert(END,"->Searched_By_URL/{}/{} Directory is already available\n\n".format(self.videos_url[i][4],f))
                            self.log.yview(END)
                            self.logger.info("Searched_By_URL/{}/{} Directory is already available".format(self.videos_url[i][4],f))
                            
                        with open("Files/Searched_By_URL/{}/{}/{}.txt".format(self.videos_url[i][4],f,f),"w",encoding="utf-8") as file:
                            try:
                                r = requests.get(self.videos_url[i][2])
                                b = BytesIO(r.content)
                                img = Image.open(b)
                                img.save("Files/Searched_By_URL/{}/{}/{}.jpeg".format(self.videos_url[i][4],f,f))
                                file.write("-------------------------------------------------Video Details-------------------------------------------------")
                                file.write("\n")
                                file.write("\nTitle: "+self.videos_url[i][0])
                                file.write("\nDescription: "+self.videos_url[i][1])
                                file.write("\nThumbnail Link: "+self.videos_url[i][2])
                                file.write("\nVideo Link: "+self.videos_url[i][3])
                                file.write("\nChannel Name: "+self.videos_url[i][4])
                                file.write("\nPublish Time: "+self.videos_url[i][5])
                                file.write("\n\n")
                                file.write("\n------------------------------------------Transcript Starts from here...----------------------------------------")
                                file.write("\n")
                                file.write(self.transcript)
                                with DatabaseConnection("DataBase.db") as connection:
                                    cursor = connection.cursor()
                                    cursor.execute("""INSERT INTO SHOW_CAPTURED VALUES(?,?,?,?,?,?,?,?)
                                    """,(self.videos_url[i][0],self.videos_url[i][1],self.videos_url[i][2],self.videos_url[i][3],self.videos_url[i][4],self.videos_url[i][5],self.videos_url[i][4],"url"))
                                    connection.commit()
                                    self.cap_vi += 1
                                    self.Captured_label.config(text = "Captured: {}".format(self.cap_vi))
                                    self.Captured_label.update()
                                    self.log.insert(END,"->Captured Succesfully: \n{}\n\n".format("https://www.youtube.com/watch?v="+self.videos_url[i][3]))
                                    self.log.yview(END)
                                    self.logger.info("Captured Succesfully: {}".format("https://www.youtube.com/watch?v="+self.videos_url[i][3]))
                                    
                            except:
                                self.cap_vi += 1
                                self.Captured_label.config(text = "Captured: {}".format(self.cap_vi))
                                self.Captured_label.update()
                                self.log.insert(END,"->Skipped it because it is Already Captured : \n{}\n\n".format("https://www.youtube.com/watch?v="+self.videos_url[i][3]))
                                self.log.yview(END)
                                self.logger.info("Skipped it because it is Already Captured : {}".format("https://www.youtube.com/watch?v="+self.videos_url[i][3]))
                                
                    except:
                        try:
                            with DatabaseConnection("DataBase.db") as connection:
                                cursor = connection.cursor()
                                cursor.execute("""INSERT INTO SHOW_SKIPPED VALUES(?,?,?,?,?,?,?,?)
                                """,(self.videos_url[i][0],self.videos_url[i][1],self.videos_url[i][2],self.videos_url[i][3],self.videos_url[i][4],self.videos_url[i][5],self.videos_url[i][4],"url"))
                                connection.commit()
                                self.skip_vi +=1
                                self.Skipped_label.config(text = "Skipped: {}".format(self.skip_vi))
                                self.Skipped_label.update()
                                self.log.insert(END,"->Transcript Not Found! - Skipped : \n{}".format("https://www.youtube.com/watch?v="+self.videos_url[i][3]))
                                self.log.yview(END)
                                self.logger.info("Transcript Not Found! - Skipped : {}".format("https://www.youtube.com/watch?v="+self.videos_url[i][3]))
                        except:
                            self.skip_vi +=1
                            self.Skipped_label.config(text = "Skipped: {}".format(self.skip_vi))
                            self.Skipped_label.update() 
                            self.log.insert(END,"->Already in Skipped : \n{}\n\n".format("https://www.youtube.com/watch?v="+self.videos_url[i][3]))
                            self.log.yview(END)
                            self.logger.info("Already in Skipped : {}".format("https://www.youtube.com/watch?v="+self.videos_url[i][3]))
                        
                if self.Use_CheckBtns_var_url[i].get() == 0:
                    try:
                        with DatabaseConnection("DataBase.db") as connection:
                            cursor = connection.cursor()
                            cursor.execute("""INSERT INTO SHOW_SKIPPED VALUES(?,?,?,?,?,?,?,?)
                            """,(self.videos_url[i][0],self.videos_url[i][1],self.videos_url[i][2],self.videos_url[i][3],self.videos_url[i][4],self.videos_url[i][5],self.videos_url[i][4],"url"))
                            connection.commit()
                            self.skip_vi +=1
                            self.Skipped_label.config(text = "Skipped: {}".format(self.skip_vi))
                            self.Skipped_label.update()
                            self.log.insert(END,"->Skipped it because you have deselected it : \n{}".format("https://www.youtube.com/watch?v="+self.videos_url[i][3]))
                            self.log.yview(END)
                            self.logger.info("Skipped it because you have deselected it : {}".format("https://www.youtube.com/watch?v="+self.videos_url[i][3]))
                    except:
                        self.skip_vi +=1
                        self.Skipped_label.config(text = "Skipped: {}".format(self.skip_vi))
                        self.Skipped_label.update()
                        self.log.insert(END,"->Deselected video already present in Skipped : \n{}\n\n".format("https://www.youtube.com/watch?v="+self.videos_url[i][3]))
                        self.log.yview(END)
                        self.logger.info("Deselected video already present in Skipped : {}".format("https://www.youtube.com/watch?v="+self.videos_url[i][3]))
                        

    #this function is used to get the data when searched by channel
    def Multiple_Channels(self):
        self.add_to_log()
        self.stp = 0
        self.skip_vi = 0
        self.cap_vi = 0
        self.rerun_videos = []
        if self.Manually_var.get() == 0 :
            if self.Choose_Text_File =="":
                self.keys_lst = self.Channel_Var.get()
                self.keys_lst = self.keys_lst.split(',')
            else:
                with open(self.Choose_Text_File,"r") as file:
                    self.keys_lst = file.read().split(',')
            self.Max_Result_label.config(text = "Max Result: {}".format(self.Max_Result.get()*len(self.keys_lst)))
            self.Max_Result_label.update()
            for i in self.keys_lst:
                if self.stp==1:
                    break
                self.process_channel(i.strip())
        if self.Manually_var.get() == 1:
            self.Max_Result_label.config(text = "Max Result: {}".format(len(self.manual_videos_cha)))
            self.Max_Result_label.update()
            for i in range(len(self.manual_videos_cha)):
                if self.stp==1:
                    break
                if self.Use_CheckBtns_var_cha[i].get() == 1:
                    try:
                        os.mkdir("Files/Searched_By_Channel")
                        self.log.insert(END,"->Searched_By_Channel Directory has been created\n\n")
                        self.log.yview(END)
                        self.logger.info("Searched_By_Channel Directory has been created")
                    except:
                        self.log.insert(END,"->Searched_By_Channel is already available\n\n")
                        self.log.yview(END)
                        self.logger.info("Searched_By_Channel is already available")
                        
                    try:
                        os.mkdir("Files/Searched_By_Channel/{}".format(self.split_keys_cha[i].strip()))
                        self.log.insert(END,"->Searched_By_Channel/{} Directory has been created\n\n".format(self.split_keys_cha[i].strip()))
                        self.log.yview(END)
                        self.logger.info("Searched_By__Channel/{} Directory has been created".format(self.split_keys_cha[i].strip()))
                    except:
                        self.log.insert(END,"->Searched_By_Channel/{} Directory is already available\n\n".format(self.split_keys_cha[i].strip()))
                        self.log.yview(END)
                        self.logger.info("Searched_By_Channel/{} Directory is already available".format(self.split_keys_cha[i].strip()))
                    
                    try:
                        self.transcript = Get_Transcript(self.manual_videos_cha[i][3])
                        self.log.insert(END,"->Got the Transcript for {}\n\n".format(self.manual_videos_cha[i][3]))
                        self.log.yview(END)
                        self.logger.info("Got the Transcript for {}".format(self.manual_videos_cha[i][3]))
                        f = self.file_name(self.manual_videos_cha[i][0])
                        try:
                            os.mkdir("Files/Searched_By_Channel/{}/{}".format(self.split_keys_cha[i].strip(),f))
                            self.log.insert(END,"->Searched_By_Channel/{}/{} Directory has been created\n\n".format(self.split_keys_cha[i].strip(),f))
                            self.log.yview(END)
                            self.logger.info("Searched_By_Channel/{}/{} Directory has been created".format(self.split_keys_cha[i].strip(),f))
                        except:
                            self.log.insert(END,"->Searched_By_Channel/{}/{} Directory is already available\n\n".format(self.split_keys_cha[i].strip(),f))
                            self.log.yview(END)
                            self.logger.info("Searched_By_Channel/{}/{} Directory is already available".format(self.split_keys_cha[i].strip(),f))
        
                        with open("Files/Searched_By_Channel/{}/{}/{}.txt".format(self.split_keys_cha[i].strip(),f,f),"w",encoding="utf-8") as file:
                            try:
                                r = requests.get(self.manual_videos_cha[i][2])
                                b = BytesIO(r.content)
                                img = Image.open(b)
                                img.save("Files/Searched_By_Channel/{}/{}/{}.jpeg".format(self.split_keys_cha[i].strip(),f,f))
                                file.write("-------------------------------------------------Video Details-------------------------------------------------")
                                file.write("\n")
                                file.write("\nTitle: "+self.manual_videos_cha[i][0])
                                file.write("\nDescription: "+self.manual_videos_cha[i][1])
                                file.write("\nThumbnail Link: "+self.manual_videos_cha[i][2])
                                file.write("\nVideo Link: "+self.manual_videos_cha[i][3])
                                file.write("\nChannel Name: "+self.manual_videos_cha[i][4])
                                file.write("\nPublish Time: "+self.manual_videos_cha[i][5])
                                file.write("\n\n")
                                file.write("\n------------------------------------------Transcript Starts from here...----------------------------------------")
                                file.write("\n")
                                file.write(self.transcript)
                                with DatabaseConnection("DataBase.db") as connection:
                                    cursor = connection.cursor()
                                    cursor.execute("""INSERT INTO SHOW_CAPTURED VALUES(?,?,?,?,?,?,?,?)
                                    """,(self.manual_videos_cha[i][0],self.manual_videos_cha[i][1],self.manual_videos_cha[i][2],self.manual_videos_cha[i][3],self.manual_videos_cha[i][4],self.manual_videos_cha[i][5],self.split_keys_cha[i],"channel"))
                                    connection.commit()
                                    self.cap_vi+=1
                                    self.Captured_label.config(text = "Captured: {}".format(self.cap_vi))
                                    self.Captured_label.update()
                                    self.log.insert(END,"->Captured Succesfully: \n{}\n\n".format("https://www.youtube.com/watch?v="+self.manual_videos_cha[i][3]))
                                    self.log.yview(END)
                                    self.logger.info("Captured Succesfully: {}".format("https://www.youtube.com/watch?v="+self.manual_videos_cha[i][3]))
                            except:
                                self.cap_vi+=1
                                self.Captured_label.config(text = "Captured: {}".format(self.cap_vi))
                                self.Captured_label.update()
                                self.log.insert(END,"->Skipped it because it is Already Captured : \n{}\n\n".format("https://www.youtube.com/watch?v="+self.manual_videos_cha[i][3]))
                                self.log.yview(END)
                                self.logger.info("Skipped it because it is Already Captured : {}".format("https://www.youtube.com/watch?v="+self.manual_videos_cha[i][3]))
                            
                    except:
                        try:
                            with DatabaseConnection("DataBase.db") as connection:
                                cursor = connection.cursor()
                                cursor.execute("""INSERT INTO SHOW_SKIPPED VALUES(?,?,?,?,?,?,?,?)
                                """,(self.manual_videos_cha[i][0],self.manual_videos_cha[i][1],self.manual_videos_cha[i][2],self.manual_videos_cha[i][3],self.manual_videos_cha[i][4],self.manual_videos_cha[i][5],self.split_keys_cha[i],"channel"))
                                connection.commit()
                                self.skip_vi+=1
                                self.Skipped_label.config(text = "Skipped: {}".format(self.skip_vi))
                                self.Skipped_label.update()
                                self.log.insert(END,"->Transcript Not Found! - Skipped : \n{}".format("https://www.youtube.com/watch?v="+self.manual_videos_cha[i][3]))
                                self.log.yview(END)
                                self.logger.info("Transcript Not Found! - Skipped : {}".format("https://www.youtube.com/watch?v="+self.manual_videos_cha[i][3]))
                        except:
                            self.skip_vi+=1
                            self.Skipped_label.config(text = "Skipped: {}".format(self.skip_vi))
                            self.Skipped_label.update() 
                            self.log.insert(END,"->Already in Skipped : \n{}\n\n".format("https://www.youtube.com/watch?v="+self.manual_videos_cha[i][3]))
                            self.log.yview(END)
                            self.logger.info("Already in Skipped : {}".format("https://www.youtube.com/watch?v="+self.manual_videos_cha[i][3]))
                            
                if self.Use_CheckBtns_var_cha[i].get() == 0:
                    try:
                        with DatabaseConnection("DataBase.db") as connection:
                            cursor = connection.cursor()
                            cursor.execute("""INSERT INTO SHOW_SKIPPED VALUES(?,?,?,?,?,?,?,?)
                            """,(self.manual_videos_cha[i][0],self.manual_videos_cha[i][1],self.manual_videos_cha[i][2],self.manual_videos_cha[i][3],self.manual_videos_cha[i][4],self.manual_videos_cha[i][5],self.split_keys_cha[i],"channel"))
                            connection.commit()
                            self.skip_vi+=1
                            self.Skipped_label.config(text = "Skipped: {}".format(self.skip_vi))
                            self.Skipped_label.update()
                            self.log.insert(END,"->Skipped it because you have deselected it : \n{}".format("https://www.youtube.com/watch?v="+self.manual_videos_cha[i][3]))
                            self.log.yview(END)
                            self.logger.info("Skipped it because you have deselected it : {}".format("https://www.youtube.com/watch?v="+self.manual_videos_cha[i][3]))
                    except:
                        self.skip_vi+=1
                        self.Skipped_label.config(text = "Skipped: {}".format(self.skip_vi))
                        self.Skipped_label.update()
                        self.log.insert(END,"->Deselected video already present in Skipped : \n{}\n\n".format("https://www.youtube.com/watch?v="+self.manual_videos_cha[i][3]))
                        self.log.yview(END)
                        self.logger.info("Deselected video already present in Skipped : {}".format("https://www.youtube.com/watch?v="+self.manual_videos_cha[i][3]))
                        

    #this function used by the start function to get the data searched by the keywords
    def Multiple_Keywords(self):
        self.add_to_log()
        self.skip_vi = 0
        self.cap_vi = 0
        self.rerun_videos = []
        if self.Manually_var.get() == 0:
            if self.Choose_Text_File =="":
                self.keys_lst = self.Keyword_Var.get()
                self.keys_lst = self.keys_lst.split(',')
            else:
                with open(self.Choose_Text_File,"r") as file:
                    self.keys_lst = file.read().split(',')
            self.Max_Result_label.config(text = "Max Result: {}".format(self.Max_Result.get()*len(self.keys_lst)))
            self.Max_Result_label.update()
            for i in self.keys_lst:
                if self.stp:
                    break
                self.process_keyword(i.strip())
        if self.Manually_var.get() == 1:
            self.Max_Result_label.config(text = "Max Result: {}".format(len(self.manual_videos)))
            self.Max_Result_label.update()
            for i in range(len(self.manual_videos)):
                if self.stp:
                    break
                if self.Use_CheckBtns_var[i].get() == 1:
                    try:
                        os.mkdir("Files/Searched_By_Keyword")
                        self.log.insert(END,"->Searched_By_Keyword Directory has been created\n\n")
                        self.log.yview(END)
                        self.logger.info("Searched_By_Keyword Directory has been created")
                    except:
                        self.log.insert(END,"->Searched_By_Keyword is already available\n\n")
                        self.log.yview(END)
                        self.logger.info("Searched_By_Keyword is already available")
                    
                    try:
                        os.mkdir("Files/Searched_By_Keyword/{}".format(self.split_keys[i].strip()))
                        self.log.insert(END,"->Searched_By_Keyword/{} Directory has been created\n\n".format(self.split_keys[i].strip()))
                        self.log.yview(END)
                        self.logger.info("Searched_By_Keyword/{} Directory has been created".format(self.split_keys[i].strip()))
                    except:
                        self.log.insert(END,"->Searched_By_Keyword/{} Directory is already available\n\n".format(self.split_keys[i].strip()))
                        self.log.yview(END)
                        self.logger.info("Searched_By_Keyword/{} Directory is already available".format(self.split_keys[i].strip()))
                        
                    try:
                        self.transcript = Get_Transcript(self.manual_videos[i][3])
                        self.log.insert(END,"->Got the Transcript for {}\n\n".format(self.manual_videos[i][3]))
                        self.log.yview(END)
                        self.logger.info("Got the Transcript for {}".format(self.manual_videos[i][3]))
                        f = self.file_name(self.manual_videos[i][0])
                        try:
                            os.mkdir("Files/Searched_By_Keyword/{}/{}".format(self.split_keys[i].strip(),f))
                            self.log.insert(END,"->Searched_By_Keyword/{}/{} Directory has been created\n\n".format(self.split_keys[i].strip(),f))
                            self.log.yview(END)
                            self.logger.info("Searched_By_Keyword/{}/{} Directory has been created".format(self.split_keys[i].strip(),f))
                        except:
                            self.log.insert(END,"->Searched_By_Keyword/{}/{} Directory is already available\n\n".format(self.split_keys[i].strip(),f))
                            self.log.yview(END)
                            self.logger.info("Searched_By_Keyword/{}/{} Directory is already available".format(self.split_keys[i].strip(),f))
                            
                        with open("Files/Searched_By_Keyword/{}/{}/{}.txt".format(self.split_keys[i].strip(),f,f),"w",encoding="utf-8") as file:
                            try:
                                r = requests.get(self.manual_videos[i][2])
                                b = BytesIO(r.content)
                                img = Image.open(b)
                                img.save("Files/Searched_By_Keyword/{}/{}/{}.jpeg".format(self.split_keys[i].strip(),f,f))
                                file.write("-------------------------------------------------Video Details-------------------------------------------------")
                                file.write("\n")
                                file.write("Title: "+self.manual_videos[i][0])
                                file.write("Description: "+self.manual_videos[i][1])
                                file.write("Thumbnail Link: "+self.manual_videos[i][2])
                                file.write("Video Link: "+self.manual_videos[i][3])
                                file.write("Channel Name: "+self.manual_videos[i][4])
                                file.write("Publish Time: "+self.manual_videos[i][5])
                                file.write("\n\n")
                                file.write("------------------------------------------Transcript Starts from here...----------------------------------------")
                                file.write("\n")
                                file.write(self.transcript)
                                with DatabaseConnection("DataBase.db") as connection:
                                    cursor = connection.cursor()
                                    cursor.execute("""INSERT INTO SHOW_CAPTURED VALUES(?,?,?,?,?,?,?,?)
                                    """,(self.manual_videos[i][0],self.manual_videos[i][1],self.manual_videos[i][2],self.manual_videos[i][3],self.manual_videos[i][4],self.manual_videos[i][5],self.split_keys_cha[i],"keyword"))
                                    connection.commit()
                                    self.cap_vi+=1
                                    self.Captured_label.config(text = "Captured: {}".format(self.cap_vi))
                                    self.Captured_label.update()
                                    self.log.insert(END,"->Captured Succesfully: \n{}\n\n".format("https://www.youtube.com/watch?v="+self.manual_videos[i][3]))
                                    self.log.yview(END)
                                    self.logger.info("Captured Succesfully: {}".format("https://www.youtube.com/watch?v="+self.manual_videos[i][3]))
                            except:
                                self.cap_vi+=1
                                self.Captured_label.config(text = "Captured: {}".format(self.cap_vi))
                                self.Captured_label.update()
                                self.log.insert(END,"->Skipped it because it is Already Captured : \n{}\n\n".format("https://www.youtube.com/watch?v="+self.manual_videos[i][3]))
                                self.log.yview(END)
                                self.logger.info("Skipped it because it is Already Captured : {}".format("https://www.youtube.com/watch?v="+self.manual_videos[i][3]))
                                
                    except:
                        try:
                            with DatabaseConnection("DataBase.db") as connection:
                                cursor = connection.cursor()
                                cursor.execute("""INSERT INTO SHOW_SKIPPED VALUES(?,?,?,?,?,?,?,?)
                                """,(self.manual_videos[i][0],self.manual_videos[i][1],self.manual_videos[i][2],self.manual_videos[i][3],self.manual_videos[i][4],self.manual_videos[i][5],self.split_keys_cha[i],"keyword"))
                                connection.commit()
                                self.skip_vi += 1
                                self.Skipped_label.config(text = "Skipped: {}".format(self.skip_vi))
                                self.Skipped_label.update()
                                self.log.insert(END,"->Transcript Not Found! - Skipped : \n{}".format("https://www.youtube.com/watch?v="+self.manual_videos[i][3]))
                                self.log.yview(END)
                                self.logger.info("Transcript Not Found! - Skipped : {}".format("https://www.youtube.com/watch?v="+self.manual_videos[i][3]))
                        except: 
                            self.skip_vi += 1
                            self.Skipped_label.config(text = "Skipped: {}".format(self.skip_vi))
                            self.Skipped_label.update()
                            self.log.insert(END,"->Already in Skipped : \n{}\n\n".format("https://www.youtube.com/watch?v="+self.manual_videos[i][3]))
                            self.log.yview(END)
                            self.logger.info("Already in Skipped : {}".format("https://www.youtube.com/watch?v="+self.manual_videos[i][3]))
                            
                if self.Use_CheckBtns_var[i].get() == 0:
                    try:
                        with DatabaseConnection("DataBase.db") as connection:
                            cursor = connection.cursor()
                            cursor.execute("""INSERT INTO SHOW_SKIPPED VALUES(?,?,?,?,?,?,?,?)
                            """,(self.manual_videos[i][0],self.manual_videos[i][1],self.manual_videos[i][2],self.manual_videos[i][3],self.manual_videos[i][4],self.manual_videos[i][5],self.split_keys_cha[i],"keyword"))
                            connection.commit()
                            self.skip_vi =+1
                            self.Skipped_label.config(text = "Skipped: {}".format(self.skip_vi))
                            self.Skipped_label.update()
                            self.log.insert(END,"->Skipped it because you have deselected it : \n{}".format("https://www.youtube.com/watch?v="+self.manual_videos[i][3]))
                            self.log.yview(END)
                            self.logger.info("Skipped it because you have deselected it : {}".format("https://www.youtube.com/watch?v="+self.manual_videos[i][3]))
                    except:
                        self.skip_vi =+1
                        self.Skipped_label.config(text = "Skipped: {}".format(self.skip_vi))
                        self.Skipped_label.update()
                        self.log.insert(END,"->Deselected video already present in Skipped : \n{}\n\n".format("https://www.youtube.com/watch?v="+self.manual_videos[i][3]))
                        self.log.yview(END)
                        self.logger.info("Deselected video already present in Skipped : {}".format("https://www.youtube.com/watch?v="+self.manual_videos[i][3]))
                        

    #this function is used to change the title to file name - it removes special characters from the same 
    def file_name(self,file):
        name = ""
        for i in file:
            if i.isalpha():
                name+=i
            elif i.isnumeric():
                name +=i
            else:
                name+="_"
        return name

    #this function is used by multiple_keywords() function when manually select is deselect() 
    def process_keyword(self,keyword):
        try:
            self.videos = Extract_Detail_by_keyword(keyword,self.Max_Result.get(),self.Sort_By_var.get(),self.Video_Duration_var.get())
            self.log.insert(END,"->Got list of videos from youtube Api\n\n")
            self.log.yview(END)
            self.logger.info("Got list of videos from youtube Api")
        except:
            self.log.insert(END,"->Youtube api key quota is exceeded\n\n")
            self.log.yview(END)
            self.logger.info("Youtube api key quota is exceeded")
            self.Max_Result_error_Label.config(text = "Api Quota Exceeded",fg ="red")
            
        [self.rerun_videos.append(video) for video in self.videos]
        try:
            os.mkdir("Files/Searched_By_Keyword")
            self.log.insert(END,"->Searched_By_Keyword Directory has been created\n\n")
            self.log.yview(END)
            self.logger.info("Searched_By_Keyword Directory has been created")
        except:
            self.log.insert(END,"->Searched_By_Keyword Directory is already available\n\n")
            self.log.yview(END)
            self.logger.info("Searched_By_Keyword Directory is already available")
            
        try:
            os.mkdir("Files/Searched_By_Keyword/{}".format(keyword))
            self.log.insert(END,"->Searched_By_Keyword/{} Directory has been created\n\n".format(keyword))
            self.log.yview(END)
            self.logger.info("Searched_By_Keyword/{} Directory has been created".format(keyword))
        except:
            self.log.insert(END,"->Searched_By_Keyword/{} Directory already available\n\n".format(keyword))
            self.log.yview(END)
            self.logger.info("Searched_By_Keyword/{} Directory already available".format(keyword))
            
        for i in range(len(self.videos)):
            if self.stp:
                break
            try:
                self.transcript = Get_Transcript(self.videos[i][3])
                self.log.insert(END,"->Got Transcript : {}\n\n".format("https://www.youtube.com/watch?v="+self.videos[i][3]))
                self.log.yview(END)
                self.logger.info("Got Transcript : {}".format("https://www.youtube.com/watch?v="+self.videos[i][3]))
                f = self.file_name(self.videos[i][0])
                try:
                    os.mkdir("Files/Searched_By_Keyword/{}/{}".format(keyword,f))
                    self.log.insert(END,"->Searched_By_Keyword/{}/{} Directory has been created\n\n".format(keyword,f))
                    self.log.yview(END)
                    self.logger.info("Searched_By_Keyword/{}/{} Directory has been created".format(keyword,f))
                except:
                    self.log.insert(END,"->Searched_By_Keyword/{}/{} Directory is already available\n\n".format(keyword,f))
                    self.log.yview(END)
                    self.logger.info("Searched_By_Keyword/{}/{} Directory is already available".format(keyword,f))
                    
                with open("Files/Searched_By_Keyword/{}/{}/{}.txt".format(keyword,f,f),"w",encoding="utf-8") as file:
                    try:
                        r = requests.get(self.videos[i][2])
                        b = BytesIO(r.content)
                        img = Image.open(b)
                        img.save("Files/Searched_By_Keyword/{}/{}/{}.jpeg".format(keyword,f,f))
                        file.write("-------------------------------------------------Video Details-------------------------------------------------")
                        file.write("\n")
                        file.write("\nTitle: "+self.videos[i][0])
                        file.write("\nDescription: "+self.videos[i][1])
                        file.write("\nThumbnail Link: "+self.videos[i][2])
                        file.write("\nVideo Link: "+self.videos[i][3])
                        file.write("\nChannel Name: "+self.videos[i][4])
                        file.write("\nPublish Time: "+self.videos[i][5])
                        file.write("\n\n")
                        file.write("\n------------------------------------------Transcript Starts from here...----------------------------------------")
                        file.write("\n")
                        file.write(self.transcript)
                        with DatabaseConnection("DataBase.db") as connection:
                            cursor = connection.cursor()
                            cursor.execute("""INSERT INTO SHOW_CAPTURED VALUES(?,?,?,?,?,?,?,?)
                            """,(self.videos[i][0],self.videos[i][1],self.videos[i][2],self.videos[i][3],self.videos[i][4],self.videos[i][5],keyword,"keyword"))
                            connection.commit()
                            self.cap_vi+=1
                            self.Captured_label.config(text = "Captured: {}".format(self.cap_vi))
                            self.Captured_label.update()
                            self.log.insert(END,"->Captured Succesfully: {}\n\n".format("https://www.youtube.com/watch?v="+self.videos[i][3]))
                            self.log.yview(END)
                            self.logger.info("Captured Succesfully: {}".format("https://www.youtube.com/watch?v="+self.videos[i][3]))
                    except:
                        self.cap_vi+=1
                        self.Captured_label.config(text = "Captured: {}".format(self.cap_vi))
                        self.Captured_label.update()
                        self.log.insert(END,"->Skipped it because it is Already Captured : {}\n\n".format("https://www.youtube.com/watch?v="+self.videos[i][3]))
                        self.log.yview(END)
                        self.logger.info("Skipped it because it is Already Captured : {}".format("https://www.youtube.com/watch?v="+self.videos[i][3]))
                        
            except:
                try:
                    with DatabaseConnection("DataBase.db") as connection:
                        cursor = connection.cursor()
                        cursor.execute("""INSERT INTO SHOW_SKIPPED VALUES(?,?,?,?,?,?,?,?)
                        """,(self.videos[i][0],self.videos[i][1],self.videos[i][2],self.videos[i][3],self.videos[i][4],self.videos[i][5],keyword,"keyword"))
                        connection.commit()
                        self.skip_vi+=1
                        self.Skipped_label.config(text = "Skipped: {}".format(self.skip_vi))
                        self.Skipped_label.update()
                        self.log.insert(END,"->Transcript Not Found! - Skipped : {}\n\n".format("https://www.youtube.com/watch?v="+self.videos[i][3]))
                        self.log.yview(END)
                        self.logger.info("Transcript Not Found! - Skipped : {}".format("https://www.youtube.com/watch?v="+self.videos[i][3]))

                except: 
                    self.skip_vi+=1
                    self.Skipped_label.config(text = "Skipped: {}".format(self.skip_vi))
                    self.Skipped_label.update()
                    self.log.insert(END,"->Already in Skipped : {}\n\n".format("https://www.youtube.com/watch?v="+self.videos[i][3]))
                    self.log.yview(END)
                    self.logger.info("Already in Skipped : {}".format("https://www.youtube.com/watch?v="+self.videos[i][3]))
                        
        
    #this function is used by the multiple_channel() function when manually select is diable (deselect)
    def process_channel(self,channel):
        try:
            self.videos_cha = Extract_Detail_by_channel(channel,1,self.Sort_By_var.get(),self.Video_Duration_var.get())
            self.search_channel_videos = Extract_Details_of_Channel_videos(self.videos_cha[0][0])
            self.log.insert(END,"->Got list of videos from youtube Api\n\n")
            self.log.yview(END)
            self.logger.info("Got list of videos from youtube Api")
        except:
            self.log.insert(END,"->Youtube api key quota is exceeded\n\n")
            self.log.yview(END)
            self.logger.info("Youtube api key quota is exceeded")
            self.Max_Result_error_Label.config(text = "Api Quota Exceeded",fg ="red")
            
        [self.rerun_videos.append(video) for video in self.search_channel_videos[:self.Max_Result.get()]]
        try:
            os.mkdir("Files/Searched_By_Channel")
            self.log.insert(END,"->Searched_By_Channel Directory has been created\n\n")
            self.log.yview(END)
            self.logger.info("Searched_By_Channel Directory has been created")
        except:
            self.log.insert(END,"->Searched_By_Channel Directory is already available\n\n")
            self.logger.info("Searched_By_Channel Directory is already available")
            
        try:
            os.mkdir("Files/Searched_By_Channel/{}".format(channel))
            self.log.insert(END,"->Searched_By_Channel/{} Directory has been created\n\n".format(channel))
            self.log.yview(END)
            self.logger.info("Searched_By_Channel/{} Directory has been created".format(channel))
        except:
            self.log.insert(END,"->Searched_By_Channel/{} Directory already available\n\n".format(channel))
            self.log.yview(END)
            self.logger.info("Searched_By_Channel/{} Directory already available".format(channel))
            
        for i in range(len(self.search_channel_videos[:self.Max_Result.get()])):
            if self.stp==1:
                break
            try:
                self.transcript = Get_Transcript(self.search_channel_videos[i][3])
                self.log.insert(END,"->Got Transcript : {}\n\n".format("https://www.youtube.com/watch?v="+self.search_channel_videos[i][3]))
                self.log.yview(END)
                self.logger.info("Got Transcript : {}".format("https://www.youtube.com/watch?v="+self.search_channel_videos[i][3]))
                f = self.file_name(self.search_channel_videos[i][0])
                try:
                    os.mkdir("Files/Searched_By_Channel/{}/{}".format(channel,f))
                    self.log.insert(END,"->Searched_By_Channel/{}/{} Directory has been created\n\n".format(channel,f))
                    self.log.yview(END)
                    self.logger.info("Searched_By_Channel/{}/{} Directory has been created".format(channel,f))
                except:
                    self.log.insert(END,"->Searched_By_Channel/{}/{} Directory is already available\n\n".format(channel,f))
                    self.log.yview(END)
                    self.logger.info("Searched_By_Channel/{}/{} Directory is already available".format(channel,f))
                    
                with open("Files/Searched_By_Channel/{}/{}/{}.txt".format(channel,f,f),"w",encoding="utf-8") as file:
                    try:
                        r = requests.get(self.search_channel_videos[i][2])
                        b = BytesIO(r.content)
                        img = Image.open(b)
                        img.save("Files/Searched_By_Channel/{}/{}/{}.jpeg".format(channel,f,f))
                        file.write("-------------------------------------------------Video Details-------------------------------------------------")
                        file.write("\n")
                        file.write("\nTitle: "+self.search_channel_videos[i][0])
                        file.write("\nDescription: "+self.search_channel_videos[i][1])
                        file.write("\nThumbnail Link: "+self.search_channel_videos[i][2])
                        file.write("\nVideo Link: "+self.search_channel_videos[i][3])
                        file.write("\nChannel Name: "+self.search_channel_videos[i][4])
                        file.write("\nPublish Time: "+self.search_channel_videos[i][5])
                        file.write("\n\n")
                        file.write("\n------------------------------------------Transcript Starts from here...----------------------------------------")
                        file.write("\n")
                        file.write(self.transcript)
                        with DatabaseConnection("DataBase.db") as connection:
                            cursor = connection.cursor()
                            cursor.execute("""INSERT INTO SHOW_CAPTURED VALUES(?,?,?,?,?,?,?,?)
                            """,(self.search_channel_videos[i][0],self.search_channel_videos[i][1],self.search_channel_videos[i][2],self.search_channel_videos[i][3],self.search_channel_videos[i][4],self.search_channel_videos[i][5],channel,"channel"))
                            connection.commit()
                            self.cap_vi+=1
                            self.Captured_label.config(text = "Captured: {}".format(self.cap_vi))
                            self.Captured_label.update()
                            self.log.insert(END,"->Captured Succesfully: {}\n\n".format("https://www.youtube.com/watch?v="+self.search_channel_videos[i][3]))
                            self.log.yview(END)
                            self.logger.info("Captured Succesfully: {}".format("https://www.youtube.com/watch?v="+self.search_channel_videos[i][3]))
                    except Exception:
                        self.cap_vi+=1
                        self.Captured_label.config(text = "Captured: {}".format(self.cap_vi))
                        self.Captured_label.update()
                        self.log.insert(END,"->Skipped it because it is Already Captured : {}\n\n".format("https://www.youtube.com/watch?v="+self.search_channel_videos[i][3]))
                        self.log.yview(END)
                        self.logger.info("Skipped it because it is Already Captured : {}".format("https://www.youtube.com/watch?v="+self.search_channel_videos[i][3]))
                        
            except:
                try:
                    with DatabaseConnection("DataBase.db") as connection:
                        cursor = connection.cursor()
                        cursor.execute("""INSERT INTO SHOW_SKIPPED VALUES(?,?,?,?,?,?,?,?)
                        """,(self.search_channel_videos[i][0],self.search_channel_videos[i][1],self.search_channel_videos[i][2],self.search_channel_videos[i][3],self.search_channel_videos[i][4],self.search_channel_videos[i][5],channel,"channel"))
                        connection.commit()
                        self.skip_vi+=1
                        self.Skipped_label.config(text = "Skipped: {}".format(self.skip_vi))
                        self.Skipped_label.update()
                        self.log.insert(END,"->Transcript Not Found! - Skipped : {}\n\n".format("https://www.youtube.com/watch?v="+self.search_channel_videos[i][3]))
                        self.log.yview(END)
                        self.logger.info("Transcript Not Found! - Skipped : {}".format("https://www.youtube.com/watch?v="+self.search_channel_videos[i][3]))
                except:
                    self.skip_vi+=1
                    self.Skipped_label.config(text = "Skipped: {}".format(self.skip_vi))
                    self.Skipped_label.update() 
                    self.log.insert(END,"->Already in Skipped : {}\n\n".format("https://www.youtube.com/watch?v="+self.search_channel_videos[i][3]))
                    self.log.yview(END)
                    self.logger.info("Already in Skipped : {}".format("https://www.youtube.com/watch?v="+self.search_channel_videos[i][3]))
                    

    #this function is used by the multiple_url() function to get the data of videos when maunual select is deselct()
    def process_URL(self,URL):
        try:
            self.videos_url = Extract_Detail_of_URL_video(URL)
            self.log.insert(END,"->Got list of videos from youtube Api\n\n")
            self.log.yview(END)
            self.logger.info("Got list of videos from youtube Api")
        except:
            self.log.insert(END,"->Youtube api key quota is exceeded\n\n")
            self.log.yview(END)
            self.logger.info("Youtube api key quota is exceeded")
            self.Max_Result_error_Label.config(text = "Api Quota Exceeded",fg ="red")
            
        self.rerun_videos = self.videos_url
        for i in range(len(self.videos_url)):
            if self.stp:
                break
            try:
                os.mkdir("Files/Searched_By_URL")
                self.log.insert(END,"->Searched_By_URL Directory has been created\n\n")
                self.log.yview(END)
                self.logger.info("Searched_By_URL Directory has been created")
            except:
                self.log.insert(END,"->Searched_By_URL Directory is already available\n\n")
                self.log.yview(END)
                self.logger.info("Searched_By_URL Directory is already available")
                
            try:
                os.mkdir("Files/Searched_By_URL/{}".format(self.videos_url[i][4]))
                self.log.insert(END,"->Searched_By_URL/{} Directory has been created\n\n".format(self.videos_url[i][4]))
                self.log.yview(END)
                self.logger.info("Searched_By_URL/{} Directory has been created".format(self.videos_url[i][4]))
            except:
                self.log.insert(END,"->Searched_By_URL/{} Directory already available\n\n".format(self.videos_url[i][4]))
                self.log.yview(END)
                self.logger.info("Searched_By_URL/{} Directory already available".format(self.videos_url[i][4]))
                
            try:
                self.transcript = Get_Transcript(self.videos_url[i][3])
                self.log.insert(END,"->Got Transcript : {}\n\n".format("https://www.youtube.com/watch?v="+self.videos_url[i][3]))
                self.log.yview(END)
                self.logger.info("Got Transcript : {}".format("https://www.youtube.com/watch?v="+self.videos_url[i][3]))
                f = self.file_name(self.videos_url[i][0])
                try:
                    os.mkdir("Files/Searched_By_URL/{}/{}".format(self.videos_url[i][4],f))
                    self.log.insert(END,"->Searched_By_URL/{}/{} Directory has been created\n\n".format(self.videos_url[i][4],f))
                    self.log.yview(END)
                    self.logger.info("Searched_By_URL/{}/{} Directory has been created".format(self.videos_url[i][4],f))
                except:
                    self.log.insert(END,"->Searched_By_URL/{}/{} Directory is already available\n\n".format(self.videos_url[i][4],f))
                    self.log.yview(END)
                    self.logger.info("Searched_By_URL/{}/{} Directory is already available".format(self.videos_url[i][4],f))
                
                with open("Files/Searched_By_URL/{}/{}/{}.txt".format(self.videos_url[i][4],f,f),"w",encoding="utf-8") as file:
                    try:
                        r = requests.get(self.videos_url[i][2])
                        b = BytesIO(r.content)
                        img = Image.open(b)
                        img.save("Files/Searched_By_URL/{}/{}/{}.jpeg".format(self.videos_url[i][4],f,f))
                        file.write("-------------------------------------------------Video Details-------------------------------------------------")
                        file.write("\n")
                        file.write("\nTitle: "+self.videos_url[i][0])
                        file.write("\nDescription: "+self.videos_url[i][1])
                        file.write("\nThumbnail Link: "+self.videos_url[i][2])
                        file.write("\nVideo Link: "+self.videos_url[i][3])
                        file.write("\nChannel Name: "+self.videos_url[i][4])
                        file.write("\nPublish Time: "+self.videos_url[i][5])
                        file.write("\n\n")
                        file.write("\n------------------------------------------Transcript Starts from here...----------------------------------------")
                        file.write("\n")
                        file.write(self.transcript)
                        with DatabaseConnection("DataBase.db") as connection:
                            cursor = connection.cursor()
                            cursor.execute("""INSERT INTO SHOW_CAPTURED VALUES(?,?,?,?,?,?,?,?)
                            """,(self.videos_url[i][0],self.videos_url[i][1],self.videos_url[i][2],self.videos_url[i][3],self.videos_url[i][4],self.videos_url[i][5],self.videos_url[i][4],"url"))
                            connection.commit()
                            self.cap_vi+=1
                            self.Captured_label.config(text = "Captured: {}".format(self.cap_vi))
                            self.Captured_label.update()
                            self.log.insert(END,"->Captured Succesfully: {}\n\n".format("https://www.youtube.com/watch?v="+self.videos_url[i][3]))
                            self.log.yview(END)
                            self.logger.info("Captured Succesfully: {}".format("https://www.youtube.com/watch?v="+self.videos_url[i][3]))
                    except:
                        self.cap_vi+=1
                        self.Captured_label.config(text = "Captured: {}".format(self.cap_vi))
                        self.Captured_label.update()
                        self.log.insert(END,"->Skipped it because it is Already Captured : {}\n\n".format("https://www.youtube.com/watch?v="+self.videos_url[i][3]))
                        self.log.yview(END)
                        self.logger.info("Skipped it because it is Already Captured : {}".format("https://www.youtube.com/watch?v="+self.videos_url[i][3]))
                        
            except:
                try:
                    with DatabaseConnection("DataBase.db") as connection:
                        cursor = connection.cursor()
                        cursor.execute("""INSERT INTO SHOW_SKIPPED VALUES(?,?,?,?,?,?,?,?)
                        """,(self.videos_url[i][0],self.videos_url[i][1],self.videos_url[i][2],self.videos_url[i][3],self.videos_url[i][4],self.videos_url[i][5],self.videos_url[i][4],"url"))
                        connection.commit()
                        self.skip_vi+=1
                        self.Skipped_label.config(text = "Skipped: {}".format(self.skip_vi))
                        self.Skipped_label.update()
                        self.log.insert(END,"->Transcript Not Found! - Skipped : {}\n\n".format("https://www.youtube.com/watch?v="+self.videos_url[i][3]))
                        self.log.yview(END)
                        self.logger.info("Transcript Not Found! - Skipped : {}".format("https://www.youtube.com/watch?v="+self.videos_url[i][3]))


                except: 
                    self.skip_vi+=1
                    self.Skipped_label.config(text = "Skipped: {}".format(self.skip_vi))
                    self.Skipped_label.update()
                    self.log.insert(END,"->Already in Skipped : {}\n\n".format("https://www.youtube.com/watch?v="+self.videos_url[i][3]))
                    self.log.yview(END)
                    self.logger.info("Already in Skipped : {}".format("https://www.youtube.com/watch?v="+self.videos_url[i][3]))
                        

    def Clear_Frame_5(self):
        for widget in self.Frame_5.winfo_children():
            widget.destroy()

    #this function is used when start is clicked
    def start(self):
        try:
            self.Rerun_Button.pack_forget()
        except:
            pass
        try:
            if(self.Max_Result.get() and self.Use_CheckBtn.get() != 0):
                self.Max_Result_error_Label.config(text ="Error Box.",fg = "black")
                try:
                    if(self.Use_CheckBtn.get() == 1):
                        if (self.Choose_Text_File == "" and self.Keyword_Var.get() != ""):
                            self.Start_Disable_1()
                            self.Clear_Frame_5()
                            self.show_log()
                            self.Multiple_Keywords()
            
                            self.Show_Captured_Start_Func()
                            self.Show_Skipped_Start_Func()
                            self.Use_CheckBtns_var_show_s = []
                            self.Use_CheckBtns_var_show_c = []
                            
                            self.Start_Disable_2()
                        elif(self.Choose_Text_File != ""):
                            self.Start_Disable_1()
                            self.Clear_Frame_5()
            
                            self.show_log()
                            self.Multiple_Keywords()
                        
                            self.Show_Captured_Start_Func()
                            self.Show_Skipped_Start_Func()
                            self.Use_CheckBtns_var_show_s = []
                            self.Use_CheckBtns_var_show_c = []
                           
                            self.Start_Disable_2()
                        elif(self.Choose_Text_File == "" and self.Keyword_Var.get() == ""):
                            raise Exception("Enter some keyword")
                except :
                    self.Max_Result_error_Label.config(text = "You didn\'t Enter any Keyword!",fg = "red",
                                                justify = "left",
                                                font =("helvetica",9))
                try:
                    if(self.Use_CheckBtn.get() == 2):
                        if (self.Choose_Text_File == "" and self.Channel_Var.get() != ""):
                            self.Start_Disable_1()
                            self.Clear_Frame_5()
                            self.show_log()
                            self.Multiple_Channels()
                         
                            self.Show_Captured_Start_Func()
                            self.Show_Skipped_Start_Func()
                            self.Use_CheckBtns_var_show_s = []
                            self.Use_CheckBtns_var_show_c = []
                            
                            self.Start_Disable_2()
                        elif(self.Choose_Text_File != ""):
                            self.Start_Disable_1()
                            self.Clear_Frame_5()
                            self.show_log()
                            self.Multiple_Channels()
                        
                            self.Show_Captured_Start_Func()
                            self.Show_Skipped_Start_Func()
                            self.Use_CheckBtns_var_show_s = []
                            self.Use_CheckBtns_var_show_c = []
                            
                            self.Start_Disable_2()
                        elif(self.Choose_Text_File == "" and self.Channel_Var.get() == ""):
                            raise Exception("Enter some Channel")
                except :
                    self.Max_Result_error_Label.config(text = "You didn\'t Enter any Channel\nName!",fg = "red",
                                                justify = "left",
                                                font =("helvetica",9))
                try:
                    if(self.Use_CheckBtn.get() == 3):
                        if (self.Choose_Text_File == "" and self.URL_Var.get() != ""):
                            self.Start_Disable_1()
                            self.Clear_Frame_5()
                            self.show_log()
                            self.Multiple_URLs()
                            self.Show_Captured_Start_Func()
                            self.Show_Skipped_Start_Func()
                            self.Use_CheckBtns_var_show_s = []
                            self.Use_CheckBtns_var_show_c = []
                            
                            self.Start_Disable_2()
                        elif(self.Choose_Text_File != ""):
                            self.Start_Disable_1()
                            self.Clear_Frame_5()
                            self.show_log()
                            self.Multiple_URLs()
                        
                            self.Show_Captured_Start_Func()
                            self.Show_Skipped_Start_Func()
                            self.Use_CheckBtns_var_show_s = []
                            self.Use_CheckBtns_var_show_c = []
                            
                            self.Start_Disable_2()
                        elif(self.Choose_Text_File == "" and self.URL_Var.get() == ""):
                            raise Exception("Enter some URL")
                except :
                    self.Max_Result_error_Label.config(text = "You didn\'t Enter any URL!",fg = "red",
                                                justify = "left",
                                                font =("helvetica",9))
            else:
                raise Exception()
        except:
            self.Max_Result_error_Label.config(text = "You didn\'t select any options,\nor didn\'t enter the max result\nor both.",fg = "red",
                                                justify = "left",
                                                font =("helvetica",9))
    

    def add_to_log(self):
        if self.Schedule_var.get()=="None":
            next_run = datetime.date.today()
        else:
            next_run = datetime.date.today() + datetime.timedelta(days = int(self.Schedule_var.get()))

        if self.Use_CheckBtn.get() == 1:
            if self.Keyword_Var.get() != "" and self.Choose_Text_File == "":
                keys = self.Keyword_Var.get()
            elif self.Keyword_Var.get() == "" and self.Choose_Text_File != "":
                with open(self.Choose_Text_File ,"r") as file :
                    keys = file.read().strip()
            with DatabaseConnection("DataBase.db") as connection:
                cursor = connection.cursor()
                cursor.execute("""select * from log where searched_phrase = ?;""",(keys,))
                got = cursor.fetchone()
                connection.commit()
            if got==None:
                with DatabaseConnection("DataBase.db") as connection:
                    cursor = connection.cursor()
                    cursor.execute("""
                    INSERT INTO log(last_run,searched_phrase,schedule,next_run,max_result,searched_by)
                    values(?,?,?,?,?,?);
                    """,(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),keys,self.Schedule_var.get(),next_run,self.Max_Result.get(),"keyword"))
                    connection.commit()
            elif got != None:
                with DatabaseConnection("DataBase.db") as connection:
                    cursor = connection.cursor()
                    cursor.execute("""UPDATE LOG SET last_run=?,
                                        searched_phrase=?,
                                        schedule =?,
                                        next_run=?,
                                        max_result = ?,
                                        searched_by=?
                                where searched_phrase = ?;""",(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),keys,self.Schedule_var.get(),next_run,self.Max_Result.get(),"keyword",keys))
                    connection.commit()
        elif self.Use_CheckBtn.get() == 2:
            if self.Channel_Var.get() != "" and self.Choose_Text_File == "":
                keys = self.Channel_Var.get()
            elif self.Channel_Var.get() == "" and self.Choose_Text_File != "":
                with open(self.Choose_Text_File ,"r") as file :
                    keys = file.read().strip()
            with DatabaseConnection("DataBase.db") as connection:
                cursor = connection.cursor()
                cursor.execute("""select * from log where searched_phrase = ?;""",(keys,))
                got = cursor.fetchone()
                connection.commit()
            if got == None:
                with DatabaseConnection("DataBase.db") as connection:
                    cursor = connection.cursor()
                    cursor.execute("""
                    INSERT INTO log(last_run,searched_phrase,schedule,next_run,max_result,searched_by)
                    values(?,?,?,?,?,?);
                    """,(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),keys,self.Schedule_var.get(),next_run,self.Max_Result.get(),"channel"))
                    connection.commit()
            if got != None:
                with DatabaseConnection("DataBase.db") as connection:
                    cursor = connection.cursor()
                    cursor.execute("""UPDATE LOG SET last_run=?,
                                        searched_phrase=?,
                                        schedule =?,
                                        next_run =?,
                                        max_result = ?,
                                        searched_by=?
                                where searched_phrase = ?;""",(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),keys,self.Schedule_var.get(),next_run,self.Max_Result.get(),"channel",keys))
                    connection.commit()

        elif self.Use_CheckBtn.get() == 3:
            if self.URL_Var.get() != "" and self.Choose_Text_File == "":
                keys = self.URL_Var.get()
            elif self.URL_Var.get() == "" and self.Choose_Text_File != "":
                with open(self.Choose_Text_File ,"r") as file :
                    keys = file.read().strip()
            with DatabaseConnection("DataBase.db") as connection:
                cursor = connection.cursor()
                cursor.execute("""select * from log where searched_phrase = ?;""",(keys,))
                got = cursor.fetchone()
                connection.commit()
            if got == None:
                with DatabaseConnection("DataBase.db") as connection:
                    cursor = connection.cursor()
                    cursor.execute("""
                    INSERT INTO log(last_run,searched_phrase,schedule,next_run,max_result,searched_by)
                    values(?,?,?,?,?,?);
                    """,(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),keys,self.Schedule_var.get(),next_run ,self.Max_Result.get(),"url"))
                    connection.commit()
            elif got !=None:
                with DatabaseConnection("DataBase.db") as connection:
                    cursor = connection.cursor()
                    cursor.execute("""UPDATE LOG SET last_run=?,
                                        searched_phrase=?,
                                        schedule =?,
                                        next_run = ?,
                                        max_result = ?,
                                        searched_by=?
                                where searched_phrase = ?;""",(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),keys,self.Schedule_var.get(),next_run,self.Max_Result.get(),"url",keys))
                    connection.commit()
        

    def get_run_data(self,button_id):
        col=""
        time=""
        if self.radio.get() == 1 :
            col = "last_run"
        elif self.radio.get() == 2:
            col = "next_run"
        if self.log_options_time_var.get() == "Newest First":
            time = "DESC"
        elif self.log_options_search_var.get() == "Oldest First":
            time = "ASC"
        if self.log_options_search_var.get() == "All":
            with DatabaseConnection("DataBase.db") as connection:
                cursor = connection.cursor()
                cursor.execute("""SELECT * from log ORDER BY {} {};""".format(col,time))
                log_data = cursor.fetchall()
                connection.commit()
            return log_data[button_id]
        elif self.log_options_search_var.get() == "Keywords":
            with DatabaseConnection("DataBase.db") as connection:
                cursor = connection.cursor()
                cursor.execute("""SELECT * from log WHERE SEARCHED_BY=? ORDER BY {} {};""".format(col,time),("keyword",))
                log_data = cursor.fetchall()
                connection.commit()
            return log_data[button_id]
        elif self.log_options_search_var.get() == "Channels":
            with DatabaseConnection("DataBase.db") as connection:
                cursor = connection.cursor()
                cursor.execute("""SELECT * from log WHERE SEARCHED_BY=? ORDER BY {} {};""".format(col,time),("channel",))
                log_data = cursor.fetchall()
                connection.commit()
            return log_data[button_id]
        elif self.log_options_search_var.get() == "Urls":
            with DatabaseConnection("DataBase.db") as connection:
                cursor = connection.cursor()
                cursor.execute("""SELECT * from log WHERE SEARCHED_BY=? ORDER BY {} {};""".format(col,time),("url",))
                log_data = cursor.fetchall()
                connection.commit()
            return log_data[button_id]


    def run_from_log(self,button_id):
        get_log = self.get_run_data(button_id)
        if get_log[6] == "keyword":
            self.Clear_Frame_5()
            self.show_log()
            self.Use_CheckBtn.set(1)
            self.Keyword_Var.set(get_log[2])
            self.Max_Result.set(get_log[5])
            self.Thread_Start()
        if get_log[6] == "channel":
            self.Clear_Frame_5()
            self.show_log()
            self.Use_CheckBtn.set(2)
            self.Channel_Var.set(get_log[2])
            self.Max_Result.set(get_log[5])
            self.Thread_Start()
        if get_log[6] == "url":
            self.Clear_Frame_5()
            self.show_log()
            self.Use_CheckBtn.set(3)
            self.URL_Var.set(get_log[2])
            self.Max_Result.set(get_log[5])
            self.Thread_Start()

    def save_edit(self,button_id):
        get_log = self.get_run_data(button_id)
        with DatabaseConnection('DataBase.db') as connection:
            cursor = connection.cursor()
            cursor.execute("""UPDATE LOG SET last_run=?,
                                            searched_phrase=?,
                                            schedule = ?,
                                            next_run=?,
                                            max_result = ?
            where id = ?;""",(self.table_entry[button_id][0].get(),self.table_entry[button_id][1].get(),self.table_entry[button_id][2].get(),self.table_entry[button_id][3].get(),self.table_entry[button_id][4].get(),get_log[0]))
            connection.commit()
        self.show_log_func()

    def get_data(self):
        col=""
        time=""
        if self.radio.get() == 1 :
            col = "last_run"
        elif self.radio.get() == 2:
            col = "next_run"
        if self.log_options_time_var.get() == "Newest First":
            time = "DESC"
        elif self.log_options_search_var.get() == "Oldest First":
            time = "ASC"
        if self.log_options_search_var.get() == "All":
            with DatabaseConnection("DataBase.db") as connection:
                cursor = connection.cursor()
                cursor.execute("""SELECT * from log ORDER BY {} {};""".format(col,time))
                log_data = cursor.fetchall()
                connection.commit()
            return log_data
        elif self.log_options_search_var.get() == "Keywords":
            with DatabaseConnection("DataBase.db") as connection:
                cursor = connection.cursor()
                cursor.execute("""SELECT * from log WHERE SEARCHED_BY=? ORDER BY {} {};""".format(col,time),("keyword",))
                log_data = cursor.fetchall()
                connection.commit()
            return log_data
        elif self.log_options_search_var.get() == "Channels":
            with DatabaseConnection("DataBase.db") as connection:
                cursor = connection.cursor()
                cursor.execute("""SELECT * from log WHERE SEARCHED_BY=? ORDER BY {} {};""".format(col,time),("channel",))
                log_data = cursor.fetchall()
                connection.commit()
            return log_data
        elif self.log_options_search_var.get() == "Urls":
            with DatabaseConnection("DataBase.db") as connection:
                cursor = connection.cursor()
                cursor.execute("""SELECT * from log WHERE SEARCHED_BY=? ORDER BY {} {};""".format(col,time),("url",))
                log_data = cursor.fetchall()
                connection.commit()
            return log_data

    def show_log_func(self):
        for widget in self.Frame_5.winfo_children():
            widget.destroy()
        log_data = self.get_data()
        self.table_entry = []
        self.run_btns = []
        self.save_btns = []
        self.Working_on_Frame_5()
        Label(self.second_frame,text = "LastRun",bg = "#d2f1fc",font = ("helvatica",8,"bold")).grid(row = 0,column = 1)
        Label(self.second_frame,text = "Searched\nPhrase",bg = "#d2f1fc",font = ("helvatica",8,"bold")).grid(row = 0,column = 2)
        Label(self.second_frame,text = "Schedule",bg = "#d2f1fc",font = ("helvatica",8,"bold")).grid(row = 0,column = 3)
        Label(self.second_frame,text = "NextRun",bg = "#d2f1fc",font = ("helvatica",8,"bold")).grid(row = 0,column = 4)
        Label(self.second_frame,text = "MaxResult",bg = "#d2f1fc",font = ("helvatica",8,"bold")).grid(row = 0,column = 5)
        self.second_frame.config(bg = "#d2f1fc")
        self.Canvas_Frame_5.config(bg = "#d2f1fc")
        if log_data == []:
            self.add_data(1)
        for i in range(len(log_data)):
            self.table_en = []
            for j in range(5):
                self.table_var = StringVar()
                self.table_var.set(log_data[i][j+1])
                self.table_en.append(self.table_var)
                self.table_e = Entry(self.second_frame,textvariable = self.table_en[j],width = 12,font = ("helvatica",8),borderwidth=2)
                self.table_e.grid(row = i+1,column = j+1)
            
            self.del_in_log = Button(self.second_frame,bg = "#2eb9d9",text = "X",width=1,activebackground ="#96ebff",
                                                command =lambda x=i: self.delete_data(x))
            self.del_in_log.grid(row = i+1,column = 6)

            self.save_in_log = Button(self.second_frame,bg = "#2eb9d9",text = "Save",width=3,activebackground ="#96ebff",
                                                command =lambda x=i: self.save_edit(x))
            self.save_in_log.grid(row = i+1,column = 7)
            
            Label(self.second_frame,text = "{}.".format(i+1),bg = "#d2f1fc").grid(row=i+1,column = 0)
           
            self.run_btns.append(Button(self.second_frame,text = "Run",bg ="#2eb9d9",width=3,activebackground ="#96ebff",
                                                        command =lambda x=i: self.run_from_log(x)))
            self.run_btns[i].grid(row = i+1,column = 8)
            
            self.table_entry.append(self.table_en)
        if self.log_options_search_var.get() != "All":
            self.add_button = Button(self.second_frame,text = "Add",activebackground ="#96ebff",
                                    bg ="#2eb9d9" ,command =lambda x =len(log_data)+1: self.add_data(x))
            self.add_button.grid(row =len(log_data)+1, column =7)


    def delete_data(self,button_id):
        data = self.get_run_data(button_id)
        with DatabaseConnection("DataBase.db") as connection:
            cursor = connection.cursor()
            cursor.execute("""DELETE FROM LOG WHERE ID =?""",(data[0],))
            connection.commit()
        self.show_log_func()


    def add_data(self,id):
        self.add_table = []
        try:
            self.add_button.grid_forget()
        except:
            pass
        Label(self.second_frame,text = "{}.".format(id),bg = "#d2f1fc").grid(row=id,column = 0)
        for i in range(0,5):
            self.add_table_var = StringVar()
            self.add_table.append(self.add_table_var)
            self.table_add = Entry(self.second_frame,textvariable = self.add_table[i],width = 12,font = ("helvatica",8),borderwidth=2)
            self.table_add.grid(row = id,column =i+1)
        Button(self.second_frame,bg = "#2eb9d9",text = "X",width=1,activebackground ="#96ebff",
                                        command = lambda : self.show_log_func()).grid(row = id,column = 6)
        Button(self.second_frame,bg = "#2eb9d9",text = "Save",width=3,activebackground ="#96ebff",
                                        command =self.save_add_func).grid(row = id,column = 7)
        Button(self.second_frame,text = "Run",bg ="#2eb9d9",width=3,activebackground ="#96ebff",
                                        command =self.run_add).grid(row = id,column = 8)
    
    def run_add(self):
        if self.add_table[1].get()!="" and self.add_table[4].get()!="":
            if self.log_options_search_var.get() == "Keywords":
                self.Clear_Frame_5()
                self.show_log()
                self.Use_CheckBtn.set(1)
                self.Keyword_Var.set(self.add_table[1].get())
                self.Max_Result.set(self.add_table[4].get())
                if self.add_table[2].get():
                    self.Schedule_var.set(self.add_table[2].get())
                self.Thread_Start()
            if self.log_options_search_var.get() == "Channels":
                self.Clear_Frame_5()
                self.show_log()
                self.Use_CheckBtn.set(2)
                self.Channel_Var.set(self.add_table[1].get())
                self.Max_Result.set(self.add_table[4].get())
                if self.add_table[2].get():
                    self.Schedule_var.set(self.add_table[2].get())
                self.Thread_Start()
            if self.log_options_search_var.get() == "Urls":
                self.Clear_Frame_5()
                self.show_log()
                self.Use_CheckBtn.set(3)
                self.URL_Var.set(self.add_table[1].get())
                self.Max_Result.set(self.add_table[4].get())
                if self.add_table[2].get():
                    self.Schedule_var.set(self.add_table[2].get())
                self.Thread_Start()
        else:
            self.Max_Result_error_Label.config(text = "At least Insert Seached Phrase and\nMax result.",fg = "red",justify = "left")

    def save_add_func(self):
        if self.add_table[0].get()!=None and self.add_table[1].get()!="" and self.add_table[2].get()!="" and self.add_table[3].get()!=None and self.add_table[4].get()!="":
            if self.log_options_search_var.get() == "Keywords":
                key = "keyword"
            elif self.log_options_search_var.get() == "Channels":
                key = "channel"
            elif self.log_options_search_var.get() == "Urls":
                key = "url"
            with DatabaseConnection("DataBase.db") as connection:
                cursor = connection.cursor()
                cursor.execute("""select * from log where searched_phrase = ? """,(self.add_table[1].get(),))
                chk = cursor.fetchone()
                connection.commit()
            if chk == None:
                try:
                    with DatabaseConnection("DataBase.db") as connection:
                        cursor = connection.cursor()
                        cursor.execute("""INSERT INTO LOG(last_run,searched_phrase,schedule,next_run,max_result,searched_by) 
                                            VALUES(?,?,?,?,?,?)""",(datetime.datetime.strptime(self.add_table[0].get(),"%Y-%m-%d %H:%M:%S"),self.add_table[1].get(),self.add_table[2].get(),self.add_table[3].get(),self.add_table[4].get(),key))
                        connection.commit()
                except:
                    self.Max_Result_error_Label.config(text = "Wrong Input!",fg = "red")
            elif chk != None:
                with DatabaseConnection("DataBase.db") as connection:
                    cursor = connection.cursor()
                    cursor.execute("""UPDATE LOG SET last_run=?,
                                            searched_phrase=?,
                                            schedule =?,
                                            next_run=?,
                                            max_result = ?,
                                            searched_by=?
                                    where searched_phrase = ?""",(datetime.datetime.strptime(self.add_table[0].get(),"%Y-%m-%d %H:%M:%S"),self.add_table[1].get(),self.add_table[2].get(),self.add_table[3].get(),self.add_table[4].get(),key,self.add_table[1].get()))
                    connection.commit()
            self.show_log_func()
        else:
            self.Max_Result_error_Label.config(text = "Invalid input!",justify = "left",fg = "red")



    # this function is used when stop button is clicked
    def stop(self):
        self.Start_Button.config(state = NORMAL)
        self.Max_Result_error_Label.config(text = "Stoped!", fg = "red")
        self.stp = 1
        if (self.In_Use == 1):
            self.Use_Channels.config(state = NORMAL)
            self.Use_URLs.config(state = NORMAL)
        
            self.Choose_Keywords_Button.config(state = NORMAL)
            self.Keyword_Entry.config(state = NORMAL)

        if(self.In_Use == 2):
            self.Use_Keywords.config(state = NORMAL)
            self.Use_URLs.config(state = NORMAL)

            self.Choose_Channels_Button.config(state = NORMAL)
            self.Channel_Entry.config(state = NORMAL)

        if(self.In_Use == 3):
            self.Use_Keywords.config(state = NORMAL)
            self.Use_Channels.config(state = NORMAL)

            self.Choose_URLs_Button.config(state = NORMAL)
            self.URL_Entry.config(state = NORMAL)
        if self.rerun_videos != []:
            self.run()
            self.rerun()
            self.Rerun_Button.config(state = NORMAL)
        self.stp = 1
        self.Stop_Button.config(state = DISABLED)
        
    
    #this function convert fetch button to start button
    def Convert_to_Start(self):
        self.Start_Button.configure(text = "Start",fg = "white", 
                                        relief = "raised",bg = "#0c8f00",bd = 3,
                                        font =("helvetica",13,"bold"),width = 10,
                                        activeforeground = "#0c8f00", activebackground = "#15ff00",
                                        command = self.Thread_Start)

    #this function converts start button to fetch button
    def Convert_to_Fetch(self):
        self.Start_Button.configure(text = "Fetch",fg = "white",bg = "black",
                                activebackground = "grey",activeforeground = "black",
                                font =("helvetica",12,"bold"),
                                command = self.Fetch_Details)
    
    #this function is run when fetch button is clicked 
    def Fetch_Details(self):
        try:
            if(self.Max_Result.get() and self.Use_CheckBtn.get() != 0):
                self.Max_Result_error_Label.config(text ="Error Box.",fg = "black")
                try:
                    if(self.Use_CheckBtn.get() == 1):
                        if (self.Choose_Text_File == "" and self.Keyword_Var.get() != ""):
                            self.Start_Disable_1()
                            self.Keywords_show_manual()
                            self.Start_Disable_2()
                        elif(self.Choose_Text_File != ""):
                            self.Start_Disable_1()
                            self.Keywords_show_manual()
                            self.Start_Disable_2()
                        elif(self.Choose_Text_File == "" and self.Keyword_Var.get() == ""):
                            raise Exception("Enter some keyword")
                except :
                    self.Max_Result_error_Label.config(text = "You didn\'t Enter any Keyword!",fg = "red",
                                                justify = "left",
                                                font =("helvetica",9))
                try:
                    if(self.Use_CheckBtn.get() == 2):
                        if (self.Choose_Text_File == "" and self.Channel_Var.get() != ""):
                            self.Start_Disable_1()
                            self.channel_show_manual()
                            self.Start_Disable_2()
                        elif(self.Choose_Text_File != ""):
                            self.Start_Disable_1()
                            self.channel_show_manual()
                            self.Start_Disable_2()
                        elif(self.Choose_Text_File == "" and self.Channel_Var.get() == ""):
                            raise Exception("Enter some Channel")
                except :
                    self.Max_Result_error_Label.config(text = "You didn\'t Enter any Channel\nName!",fg = "red",
                                                justify = "left",
                                                font =("helvetica",9))
                try:
                    if(self.Use_CheckBtn.get() == 3):
                        if (self.Choose_Text_File == "" and self.URL_Var.get() != ""):
                            self.Start_Disable_1()
                            self.url_show_manual()
                            self.Start_Disable_2()
                        elif(self.Choose_Text_File != ""):
                            self.Start_Disable_1()
                            self.url_show_manual()
                            self.Start_Disable_2()
                        elif(self.Choose_Text_File == "" and self.URL_Var.get() == ""):
                            raise Exception("Enter some URL")
                except :
                    self.Max_Result_error_Label.config(text = "You didn\'t Enter any URL!",fg = "red",
                                                justify = "left",
                                                font =("helvetica",9))
            else:
                raise Exception()
        except:
            self.Max_Result_error_Label.config(text = "You didn\'t select any options,\nor didn\'t enter the max result\nor both.",fg = "red",
                                                justify = "left",
                                                font =("helvetica",9))
        
    #this disable the button when another button is enable accordingly
    def disable(self):
        self.last_run_radio.config(state = NORMAL)
        self.next_run_radio.config(state = NORMAL)
        self.log_options_search.config(state = NORMAL)
        self.log_options_time.config(state =NORMAL)
        self.log_button.config(state =NORMAL)
        self.In_Use = self.Use_CheckBtn.get()
        self.Keyword_Var.set("")
        self.Channel_Var.set("")
        self.URL_Var.set("")
        self.Keywords_File_Name_Label.config(text = "")
        self.Channels_File_Name_Label.config(text = "")
        self.URLs_File_Name_Label.config(text = "")
        self.Choose_Text_File = ""
        if (self.Use_CheckBtn.get() == 1):
            self.Max_Result_error_Label.config(text = "Error Box.",fg = "black")
            self.Max_Result.set("")
            self.show_captured.config(state = NORMAL)
            self.show_skipped.config(state = NORMAL)
            
            self.Sort_By.config(state = NORMAL)
            self.Video_Duration.config(state = NORMAL)
        
            self.Max_Result_Entry.config(state = NORMAL)
            self.Start_Button.config(state = NORMAL)
           
            self.Use_Keywords.config(state = DISABLED)
            self.Use_Channels.config(state = NORMAL)
            self.Use_URLs.config(state = NORMAL)

            self.Choose_Keywords_Button.config(state = NORMAL)
            self.Choose_Channels_Button.config(state = DISABLED)
            self.Choose_URLs_Button.config(state = DISABLED)

            self.Keyword_Entry.config(state = NORMAL)
            self.Channel_Entry.config(state = DISABLED)
            self.URL_Entry.config(state = DISABLED)
        elif (self.Use_CheckBtn.get() == 2):
            self.Max_Result_error_Label.config(text = "Error Box.",fg ="black")
            self.Max_Result.set("")
            self.show_captured.config(state = NORMAL)
            self.show_skipped.config(state = NORMAL)

            self.Sort_By.config(state = NORMAL)
            self.Video_Duration.config(state = NORMAL)

            self.Max_Result_Entry.config(state = NORMAL)
            self.Start_Button.config(state = NORMAL)

            self.Use_Keywords.config(state = NORMAL)
            self.Use_Channels.config(state = DISABLED)
            self.Use_URLs.config(state = NORMAL)

            self.Choose_Keywords_Button.config(state = DISABLED)
            self.Choose_Channels_Button.config(state = NORMAL)
            self.Choose_URLs_Button.config(state = DISABLED)

            self.Keyword_Entry.config(state = DISABLED)
            self.Channel_Entry.config(state = NORMAL)
            self.URL_Entry.config(state = DISABLED)
        elif (self.Use_CheckBtn.get() == 3):
            self.Max_Result_error_Label.config(text = "Error Box.",fg="black")
            self.Max_Result.set(1)
            self.Max_Result_Entry.config(state = DISABLED)

            self.show_captured.config(state = NORMAL)
            self.show_skipped.config(state = NORMAL)

            self.Sort_By.config(state = DISABLED)
            self.Video_Duration.config(state = DISABLED)

            self.Start_Button.config(state = NORMAL)

            self.Use_Keywords.config(state = NORMAL)
            self.Use_Channels.config(state = NORMAL)
            self.Use_URLs.config(state = DISABLED)

            self.Choose_Keywords_Button.config(state = DISABLED)
            self.Choose_Channels_Button.config(state = DISABLED)
            self.Choose_URLs_Button.config(state = NORMAL)

            self.Keyword_Entry.config(state = DISABLED)
            self.Channel_Entry.config(state = DISABLED)
            self.URL_Entry.config(state = NORMAL)


    #this function is used to buil choose file button
    def choosefile(self):
        global Choose_Text_File
        self.Choose_Text_File = filedialog.askopenfilename(initialdir =path.join(environ['USERPROFILE'],'Desktop'),
                                                                title = "Select a Text File",
                                                                filetypes = [("Text File","*.txt")])
        
        if (self.Use_CheckBtn.get() == 1):
            if (self.Choose_Text_File != ""):
                self.Keywords_File_Name_Label.config(text = self.Choose_Text_File.split('/')[-1],fg = "red")
                self.Keyword_Entry.config(state = DISABLED)
            else:
                self.Keywords_File_Name_Label.config(text = "")
                self.Keyword_Entry.config(state = NORMAL)

        elif (self.Use_CheckBtn.get() == 2):
            if(self.Choose_Text_File != ""):
                self.Channels_File_Name_Label.config(text = self.Choose_Text_File.split('/')[-1],fg = "red")
                self.Channel_Entry.config(state = DISABLED)
            else:
                self.Channels_File_Name_Label.config(text = "")
                self.Channel_Entry.config(state = NORMAL)
        elif(self.Use_CheckBtn.get() == 3):
            if(self.Choose_Text_File != ""):    
                self.URLs_File_Name_Label.config(text = self.Choose_Text_File.split('/')[-1],fg = "red")
                self.URL_Entry.config(state = DISABLED)
            else:
                self.URLs_File_Name_Label.config(text = "")
                self.URL_Entry.config(state = NORMAL)

    #this runs at the startin of the program
    def When_Check_Button_is_Zero(self): 
        if (self.Use_CheckBtn.get() == 0):
            self.last_run_radio.config(state = DISABLED)
            self.next_run_radio.config(state = DISABLED)
            self.log_options_search.config(state =  DISABLED)
            self.log_options_time.config(state =  DISABLED)
            self.log_button.config(state = DISABLED)
            self.show_skipped.config(state = DISABLED)
            self.show_captured.config(state = DISABLED)

            self.Sort_By.config(state = DISABLED)
            self.Video_Duration.config(state = DISABLED)

            self.Max_Result_Entry.config(state = DISABLED)
            self.Start_Button.config(state = DISABLED)

            self.Choose_Keywords_Button.config(state = DISABLED)
            self.Choose_Channels_Button.config(state = DISABLED)
            self.Choose_URLs_Button.config(state = DISABLED)

            self.Keyword_Entry.config(state = DISABLED)
            self.Channel_Entry.config(state = DISABLED)
            self.URL_Entry.config(state = DISABLED)
    
    #declaring frame 1
    def Frame_1_Func(self):
        self.Frame_1 = Frame(self.Frame_8,borderwidth = 4 , relief = "sunken",width = 160)
        self.Frame_1.pack(side="left",fill = "y", padx = 5,pady = 5)
        self.Frame_1.pack_propagate(0)

    #declaring frame 2
    def Frame_2_Func(self):
        self.Frame_2 = Frame(self.Frame_8,borderwidth = 4 , relief = "sunken",width = 160)
        self.Frame_2.pack(side="left",fill = "y",padx =5,  pady = 5)
        self.Frame_2.pack_propagate(0)

    #declaring frame 3
    def Frame_3_Func(self):
        self.Frame_3 = Frame(self.Frame_8,borderwidth = 4 , relief = "sunken",width = 160)
        self.Frame_3.pack(side="left",fill = "y",padx = 5,pady = 5)
        self.Frame_3.pack_propagate(0)

    #declaring frame 4
    def Frame_4_Func(self):
        self.Frame_4 = Frame(self.Frame_8,borderwidth = 4 , relief = "sunken",width = 275)
        self.Frame_4.pack(side="left",fill = "y",padx = 5,pady = 5)
        self.Frame_4.pack_propagate(0)

    #declaring frame 5
    def Frame_5_Func(self):
        self.Frame_5 = Frame(self.Frame_9,borderwidth = 4 , relief = "sunken")
        self.Frame_5.pack(side="left",expand = 1,fill = "both",padx = 5,pady = 5)
        self.Frame_5.pack_propagate(0)

    #declaring frame 6
    def Frame_6_Func(self):
        self.Frame_6 = Frame(self.Frame_4,borderwidth = 4 , relief = "sunken",width = 275,height = 70)
        self.Frame_6.pack(padx = 5)
        self.Frame_6.pack_propagate(0)

    #declaring frame 7
    def Frame_7_Func(self):
        self.Frame_7 = Frame(self.Frame_9,borderwidth = 4 , relief = "sunken",width = 210)
        self.Frame_7.pack(side ="left",fill = "y",padx = 5,pady = 5)
        self.Frame_7.pack_propagate(0)

    #declaring frame 8
    def Frame_8_Func(self):
        self.Frame_8 = Frame(self,height = 325)
        self.Frame_8.pack(fill = "x")
        self.Frame_8.pack_propagate(0)

    #declaring frame 9
    def Frame_9_Func(self):
        self.Frame_9 = Frame(self,height = 325)
        self.Frame_9.pack(fill = "x")
        self.Frame_9.pack_propagate(0)

    #declaring start button
    def Start_Button_Func(self):
        self.Start_Button = Button(self.Frame_4, text = "Start",fg = "white", 
                                        relief = "raised",bg = "#0c8f00",bd = 3,
                                        font =("helvetica",13,"bold"),width = 10,
                                        activeforeground = "#0c8f00", activebackground = "#15ff00",
                                        command = self.Thread_Start)
        self.Start_Button.pack(side = "bottom", padx = 10, pady = 10,fill = "x")

    #declaring stop button
    def Stop_Button_Func(self):
        self.Stop_Button = Button(self.Frame_4, text = "Stop",fg = "white", 
                                relief = "raised",bg = "#b50000",bd = 3,
                                font =("helvetica",13,"bold"),width = 10,
                                activeforeground = "#b50000", activebackground = "red",
                                state = DISABLED,command = self.Thread_Stop)
        self.Stop_Button.pack(side = "bottom", padx = 10, pady = 10, fill = "x")

    #threading start function
    def Thread_Start(self):
        self.stp  =0
        self.thread_start = Thread(target=self.start)
        self.thread_start.start()
    def Thread_Stop(self):
        self.thread_stop = Thread(target=self.stop)
        self.thread_stop.start()

    #declaring max result entry and label
    def Max_Result_Func(self):
        self.Max_Result = IntVar(value="")

        self.Max_Result_Label = Label(self.Frame_4,text = "Enter Max Result:")
        self.Max_Result_Label.pack()

        self.Max_Result_Entry = Entry(self.Frame_4,textvariable = self.Max_Result)
        self.Max_Result_Entry.pack(fill = "x" ,padx = 10)

        self.Empty_Label = Label(self.Frame_4,text = "")
        self.Empty_Label.pack(side = "top")

    #error box declaring
    def Error_Box(self):
        self.Max_Result_error_Label = Label(self.Frame_6,text = "Error Box.")
        self.Max_Result_error_Label.pack(side = "left",anchor = "nw")

    #as name suggest
    def Working_on_Frame_1(self):
        self.Use_CheckBtn = IntVar()
        self.Use_CheckBtn.set(0)

        self.Empty_Label = Label(self.Frame_1,text = "")
        self.Empty_Label.pack()

        self.Use_Keywords = Radiobutton(self.Frame_1,text = "Use keywords",value = 1,variable = self.Use_CheckBtn,
                                        command = self.disable)
        self.Use_Keywords.pack()

        self.Empty_Label = Label(self.Frame_1,text = "")
        self.Empty_Label.pack()

        self.Empty_Label = Label(self.Frame_1,text = "")
        self.Empty_Label.pack()

        self.Keyword_Label = Label(self.Frame_1,text = "Enter Keyword:")
        self.Keyword_Label.pack()

        self.Keyword_Var = StringVar()
        self.Keyword_Var.set("")

        self.Keyword_Entry = Entry(self.Frame_1,textvariable = self.Keyword_Var,bd = 3)
        self.Keyword_Entry.pack()

        self.Empty_Label = Label(self.Frame_1,text = "")
        self.Empty_Label.pack()

        self.Empty_Label = Label(self.Frame_1,text = "")
        self.Empty_Label.pack()

        self.Choose_Label = Label(self.Frame_1,text = "Enter Multiple Keywords:")
        self.Choose_Label.pack() 

        self.Choose_Keywords_Button = Button(self.Frame_1,text = "Choose File",command = self.choosefile,
                                        bd = 3,relief = "raised", font = ("helvetica",10,"bold"),
                                        fg = "white" , bg = "#254666",activeforeground ="#254666",activebackground =  "#5d99d4")
        self.Choose_Keywords_Button.pack()

        self.Keywords_File_Name_Label = Label(self.Frame_1,text = "")
        self.Keywords_File_Name_Label.pack()

    #as name suggest
    def Working_on_Frame_2(self):
        self.Empty_Label = Label(self.Frame_2,text = "")
        self.Empty_Label.pack()

        self.Use_Channels = Radiobutton(self.Frame_2,text = "Use Channels Name",value = 2,variable = self.Use_CheckBtn,
                                            command = self.disable)
        self.Use_Channels.pack()

        self.Empty_Label = Label(self.Frame_2,text = "")
        self.Empty_Label.pack()

        self.Empty_Label = Label(self.Frame_2,text = "")
        self.Empty_Label.pack()

        self.Channel_Label = Label(self.Frame_2,text = "Enter Channel Name:")
        self.Channel_Label.pack()

        self.Channel_Var = StringVar()
        self.Channel_Var.set("")

        self.Channel_Entry = Entry(self.Frame_2,textvariable = self.Channel_Var,bd = 3)
        self.Channel_Entry.pack()

        self.Empty_Label = Label(self.Frame_2,text = "")
        self.Empty_Label.pack()

        self.Empty_Label = Label(self.Frame_2,text = "")
        self.Empty_Label.pack()

        self.Choose_Label = Label(self.Frame_2,text = "Enter Multiple Channels:")
        self.Choose_Label.pack() 

        self.Choose_Channels_Button = Button(self.Frame_2,text = "Choose File",command = self.choosefile,
                                        bd = 3,relief = "raised", font = ("helvetica",10,"bold"),
                                        fg = "white" , bg = "#254666",activeforeground ="#254666",activebackground =  "#5d99d4")
        self.Choose_Channels_Button.pack()

        self.Channels_File_Name_Label = Label(self.Frame_2,text = "")
        self.Channels_File_Name_Label.pack()
        
        self.radio = IntVar()
        self.radio.set(1)
        self.log_options_time_var = StringVar()
        self.log_options_time_var.set("Oldest First")
        self.log_options_search_var =StringVar()
        self.log_options_search_var.set("All")

        self.Frame_log = Frame(self.Frame_2)
        self.Frame_log_1 = Frame(self.Frame_1)
        self.log_button = Button(self.Frame_log,text = "Log",command = self.show_log_func,bd= 2,relief ="raised",fg = "white" , bg = "#254666",activeforeground ="#254666",activebackground =  "#5d99d4")
        self.log_options_time = OptionMenu(self.Frame_log,self.log_options_time_var,"Newest First","Oldest First")
        self.log_options_search = OptionMenu(self.Frame_log,self.log_options_search_var,"All","Keywords","Channels","Urls")
        self.last_run_radio = Radiobutton(self.Frame_log_1,text = "LastRun",value = 1,variable = self.radio)
        self.next_run_radio = Radiobutton(self.Frame_log_1,text = "NextRun",value =2,variable = self.radio)
        self.Frame_log.pack(fill = "x",expand = 1)
        self.Frame_log_1.pack(fill = "x",expand = 1)
        self.log_button.grid(row = 0,column=1,sticky = "nsew")
        self.log_options_time.grid(padx = 3,row = 0,column=0,sticky="nsew")
        self.log_options_search.grid(padx = 3,row = 1,column=0,sticky="nsew")
        self.last_run_radio.grid(row = 0,column = 0)
        self.next_run_radio.grid(row = 0,column = 1)
    #as name suggest
    def Working_on_Frame_3(self):
        self.Empty_Label = Label(self.Frame_3,text = "")
        self.Empty_Label.pack()

        self.Use_URLs = Radiobutton(self.Frame_3,text = "Use URLs",value = 3,variable = self.Use_CheckBtn,
                                    command = self.disable)
        self.Use_URLs.pack()

        self.Empty_Label = Label(self.Frame_3,text = "")
        self.Empty_Label.pack()

        self.Empty_Label = Label(self.Frame_3,text = "")
        self.Empty_Label.pack()

        self.URL_Label = Label(self.Frame_3,text = "Enter URL:")
        self.URL_Label.pack()

        self.URL_Var = StringVar()
        self.URL_Var.set("")

        self.URL_Entry = Entry(self.Frame_3,textvariable = self.URL_Var,bd = 3)
        self.URL_Entry.pack()

        self.Empty_Label = Label(self.Frame_3,text = "")
        self.Empty_Label.pack()

        self.Empty_Label = Label(self.Frame_3,text = "")
        self.Empty_Label.pack()

        self.Choose_Label = Label(self.Frame_3,text = "Enter Multiple URLs:")
        self.Choose_Label.pack() 

        self.Choose_URLs_Button = Button(self.Frame_3,text = "Choose File",command = self.choosefile,
                                        bd = 3,relief = "raised", font = ("helvetica",10,"bold"),
                                        fg = "white" , bg = "#254666",activeforeground ="#254666",
                                        activebackground =  "#5d99d4")
        self.Choose_URLs_Button.pack()

        self.URLs_File_Name_Label = Label(self.Frame_3,text = "")
        self.URLs_File_Name_Label.pack()

    # scrollbar making
    def Config_second_frame(self,event):
        size = (self.second_frame.winfo_reqwidth(), self.second_frame.winfo_reqheight())
        self.Canvas_Frame_5.config(scrollregion="0 0 %s %s" % size)
        if self.second_frame.winfo_reqwidth() != self.second_frame.winfo_width():
            self.Canvas_Frame_5.config(width=self.second_frame.winfo_reqwidth())

    # scrollbar making
    def Config_Canvas(self,event):
        if self.second_frame.winfo_reqwidth() != self.Canvas_Frame_5.winfo_width():
             # update the inner frame's width to fill the canvas
            self.Canvas_Frame_5.itemconfigure(self.second_frame_id, width=self.Canvas_Frame_5.winfo_width())
        
    #as name suggest
    def Working_on_Frame_5(self):
        for widget in self.Frame_5.winfo_children():
            widget.destroy()
        self.Scrollbar_Frame_5 = Scrollbar(self.Frame_5,orient = "vertical")
        self.Scrollbar_Frame_5.pack(side = "right" , fill ="y",expand = 0)

        self.Canvas_Frame_5 = Canvas(self.Frame_5, bd=0, highlightthickness=0,
                        yscrollcommand=self.Scrollbar_Frame_5.set)
        self.Canvas_Frame_5.pack(side = "left",fill = "both",expand = 1)
        self.Scrollbar_Frame_5.configure(command = self.Canvas_Frame_5.yview)

        self.Canvas_Frame_5.xview_moveto(0)
        self.Canvas_Frame_5.yview_moveto(0)
        
        self.second_frame = Frame(self.Canvas_Frame_5)
        self.second_frame_id =self.Canvas_Frame_5.create_window(0,0, window = self.second_frame,anchor = "nw")
        self.second_frame.bind('<Configure>', self.Config_second_frame)
        self.Canvas_Frame_5.bind('<Configure>',self.Config_Canvas)

    #as name suggest
    def Working_on_Frame_7(self):
        self.Max_Result_label = Label(self.Frame_7,text = "Max Result:",justify = "left",font =("helvetica",9,"bold"))
        self.Max_Result_label.pack(anchor = "w")

        self.Skipped_label = Label(self.Frame_7,text = "Skipped:",justify = "left",font =("helvetica",9,"bold"))
        self.Skipped_label.pack(anchor = "w")

        self.Captured_label = Label(self.Frame_7,text = "Captured:",justify = "left",font =("helvetica",9,"bold"))
        self.Captured_label.pack(anchor = "w")
        self.Filter_func()
        
        self.Show_Frame = Frame(self.Frame_7,height =60)
        self.show_captured = Button(self.Show_Frame,text  ="Show Captured",relief = "raised",
                                                    bg = "#7d36f7",bd = 3,fg = 'white',
                                                    font =("helvetica",9,"bold"),
                                                    activeforeground = "#5e00ff", activebackground = "#976be3",command = self.Show_Captured_Func)
        self.show_skipped = Button(self.Show_Frame,text  ="Show Skipped",relief = "raised",
                                                    bg = "#7d36f7",bd = 3,fg = 'white',
                                                    font =("helvetica",9,"bold"),
                                                    activeforeground = "#5e00ff", activebackground = "#976be3",command = self.Show_Skipped_Func)
        self.Show_Frame.pack(fill = "both")
        self.show_captured.pack(side = "left",padx = 2)
        self.show_skipped.pack(side = "right",padx = 2)

        self.Schedule_Option = OptionMenu(self.Frame_7,self.Schedule_var,"None","1","3","7","14","21").pack(side ="bottom",fill = "x")
        Label(self.Frame_7,text = "Set Schedule:",justify = "left").pack(side ="bottom",anchor = "w")
        
        self.api_key_var = StringVar()

        with open("Mains/set_api_key.txt","r") as file:
            v = file.read().strip()
        self.api_key_var.set(v)

        with open("Mains/api_keys.txt","r") as file:
            options = file.read().split(",")
            options =[option.strip() for option in options]

        self.api_keys_option = OptionMenu(self.Frame_7,self.api_key_var,*options,command = self.select_api_key).pack(side ="bottom",fill = "x")
        self.Manually_var = IntVar()
        self.Manually_var.set(0)
        self.Manually_Check = Checkbutton(self.Frame_7,text = "Manually Select Videos?",variable = self.Manually_var,command = self.Convert_Buttons).pack(side = "bottom")
    def select_api_key(self,value):
        with open("Mains/set_api_key.txt","w") as file:
            file.write(value.strip())


    def show_log(self):
        self.log = scrolledtext.ScrolledText(self.Frame_5,font = ("Courier New",8))
        self.log.pack(fill = "both",expand =1)
        

    #convert the start and fetch buttons by manual check button
    def Convert_Buttons(self):
        if self.Use_CheckBtn.get() == 1:
            if self.Manually_var.get()==1:
                self.Convert_to_Fetch()
                for widget in self.Frame_5.winfo_children():
                    widget.destroy()
            elif self.Manually_var.get()==0:
                self.Convert_to_Start()
                for widget in self.Frame_5.winfo_children():
                    widget.destroy()
        elif self.Use_CheckBtn.get()==2:
            if self.Manually_var.get() == 1:
                self.Convert_to_Fetch()
                for widget in self.Frame_5.winfo_children():
                    widget.destroy()
            elif self.Manually_var.get() == 0:
                self.Convert_to_Start()
                for widget in self.Frame_5.winfo_children():
                    widget.destroy()
        elif self.Use_CheckBtn.get()==3:
            if self.Manually_var.get() == 1:
                self.Convert_to_Fetch()
                for widget in self.Frame_5.winfo_children():
                    widget.destroy()
            elif self.Manually_var.get() == 0:
                self.Convert_to_Start()
                for widget in self.Frame_5.winfo_children():
                    widget.destroy()

#main() function
if __name__ == "__main__":
    window = GUI()
    window.Frame_8_Func()
    window.Frame_9_Func()
    window.Frame_1_Func()
    window.Frame_2_Func()
    window.Frame_3_Func()
    window.Frame_4_Func()
    window.Frame_5_Func()
    window.Frame_7_Func()
    window.Stop_Button_Func()
    window.Start_Button_Func()
    window.Max_Result_Func()
    window.Frame_6_Func()
    window.Error_Box()
    window.Working_on_Frame_1()
    window.Working_on_Frame_2()
    window.Working_on_Frame_3()
    window.Working_on_Frame_7()
    window.Schedule()
    window.When_Check_Button_is_Zero()
    window.mainloop()    