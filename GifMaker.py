from customtkinter import CTkImage
from PIL import Image, ImageTk, ImageSequence
from configparser import ConfigParser
import customtkinter
import os
import cv2
import glob

tempval = 1



#Creating Config

if os.path.isfile("GIF_Maker_and_Editor_config.ini"):
    print("File exists!")
    Ustawienia = ConfigParser()
    Ustawienia.read('GIF_Maker_and_Editor_config.ini')

else:
    print("File does not exist.")
    Ustawienia = ConfigParser()

    Ustawienia["Default"] = {
        "Root_Path": "Enter directory",
        "Gifsicle_Path": "Enter directory",
        "Image_Sequence_Path": "Enter or create with root",
        "Videos_Directory": "Enter or create with root",
        "GIF_Edit_Directory": "Enter or create with root",
        "Temporary_Video_Directory": "Enter or create with root",
    }

    with open("GIF_Maker_and_Editor_config.ini","w") as f:
        Ustawienia.write(f)

#Functions to be defined

    #Creating a directory

def createfolder(parent_dir,new_folder_name):

    parent_folder = parent_dir
    new_directory_name = new_folder_name
    new_directory_path = os.path.join(parent_folder, new_directory_name)
    os.makedirs(new_directory_path, exist_ok=True)

    print(f"Directory created at: {new_directory_path}")
    
    #Changing config

def ChangeConfigValue(path_to_change,dir_to_change):
    Ustawienia.set("Default",path_to_change,dir_to_change)
    with open("GIF_Maker_and_Editor_config.ini", "w") as f:
        Ustawienia.write(f)

    #Checking if path is valid

def ispathvalid(path_to_read):
    if os.path.isdir(Ustawienia.get("Default",path_to_read)):
        return True
    else:
        return False

    #Read a path in the config

def readconfigpath(path_to_read):
    return Ustawienia.get("Default",path_to_read)

    #Check all config paths if valid

def CheckAllConfigPaths():
    invalid_paths = 0
    for key in Ustawienia["Default"]:
        if ispathvalid(key):
            print(f"{key}: Valid path")
        else:
            invalid_paths += 1
    if invalid_paths > 0:
        return False
    else:
        return True

print(os.path.join(readconfigpath("videos_directory"),".mp4"))

def czyszczenie_plikow_temp(dir_to_clean):
    dir_to_clean=os.path.join(dir_to_clean,"")
    usuwanie_plikow = glob.glob(dir_to_clean + "*")
    for f in usuwanie_plikow:
        os.remove(f)

def deleteafile(filewithdir):
    if os.path.exists(filewithdir):
        os.remove(filewithdir)
    else:
        print("The file does not exist") 

vid_name="BrB1Tru85anVx1oJ"
video_loaded = os.path.join(readconfigpath("videos_directory"),(vid_name+".mp4"))

def check_video_fps(video_file_fps):
    global check_frame_rate  # Declare the variable as global to modify it
    
    # Open the video file
    capfr = cv2.VideoCapture(video_file_fps)
    
    if not capfr.isOpened():
        print("Error: Could not open video.")
        return
    
    # Get the frame rate (frames per second) of the video
    check_frame_rate = capfr.get(cv2.CAP_PROP_FPS)
    
    if check_frame_rate == 0:
        print("Error: Could not retrieve frame rate.")
    else:
        print(f"Video frame rate: {check_frame_rate} FPS")
        return check_frame_rate  # Modify the global variable
    
    # Release the video capture object
    capfr.release()

def extract_frames_then_gif(video_file,vid_speed,temp_ms):
    vid_speed = 1/vid_speed
    check_video_fps(video_file)
    czyszczenie_plikow_temp(readconfigpath("temporary_video_directory"))

    cap = cv2.VideoCapture(video_file)
    
    frame_rate = check_video_fps(video_file) / vid_speed
    frame_count = 0
    
    
    while True:
        ret, frame = cap.read()
        
        if not ret:
            break
        
        frame_count += 1
        
        if frame_count % int(cap.get(5) / frame_rate) == 0:
            video_output_file = f"{readconfigpath("temporary_video_directory")}/{frame_count}.png"
            cv2.imwrite(video_output_file, frame)
    
    cap.release()
    cv2.destroyAllWindows()

    temp_file_path = os.path.join(readconfigpath("temporary_video_directory"), "temp_gif.gif")

    def make_temp_gif(frame_folder):
        frame_folder=os.path.join(frame_folder,"")
        temp_frames = [Image.open(image) for image in sorted(glob.glob(f"{frame_folder}/*.png"), key=lambda x: int(os.path.splitext(os.path.basename(x))[0]))]
        
        temp_frame_one = temp_frames[0]
        temp_frame_one.save(fp=temp_file_path, format="GIF", append_images=temp_frames[1:],
                            save_all=True, duration=temp_ms, loop=0)

    make_temp_gif(readconfigpath("temporary_video_directory"))

#GUI code

class MainMenu(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("GIF Maker and Editor")
        self.geometry("600x400")

        self.button_create = customtkinter.CTkButton(self,width = 250, height = 100, text="Create a GIF", command=self.GifCreation)
        self.button_edit = customtkinter.CTkButton(self,width = 250, height = 100, text="Edit a GIF", command=self.button_callback)
        self.button_exit = customtkinter.CTkButton(self,width = 150, height = 100, text="Exit", command=self.exitmainmenu)
        self.button_settings = customtkinter.CTkButton(self,width = 50, height = 50, text="settings", command=self.entersettings)
      
        self.button_create.place(x=25,y=25)
        self.button_edit.place(x=25,y=150)
        self.button_exit.place(x=25,y=275)
        self.button_settings.place(x=200,y=300)

        self.buttonplaceholderforart = customtkinter.CTkButton(self,width = 250, height = 250, text="", command=self.button_callback)
        self.buttonplaceholderforart.place(x=325,y=75)

    def button_callback(self):
        print("button clicked")
    def exitmainmenu(self):
        print("exiting")
        self.destroy()
    
    #Error messages for main menu

    def MainMenuerror(self,errortext):
        class MainMenuError(customtkinter.CTkToplevel):
            def __init__(self):
                super().__init__()
                self.geometry("300x200")
                self.title("Error")
                        
                self.error_label = customtkinter.CTkLabel(self, text=errortext, fg_color="transparent")
                self.error_label.pack (padx=10,pady=25)

                self.error_exit_button = customtkinter.CTkButton(self,width = 100,height = 50, text = "Okay",command=self.exiterror)
                self.error_exit_button.place(x=100,y=125)                        


            def exiterror(self):
                print("exiting")
                self.destroy()
        mainmenuerror = MainMenuError()
 
    #Entering settings

    def entersettings(self):
        class Settings(customtkinter.CTkToplevel):
            def __init__(self):
                super().__init__()
                self.geometry("600x400")
                self.title("Settings")



                self.label_root = customtkinter.CTkLabel(self, text="Root folder directory", fg_color="transparent")
                self.entry_root = customtkinter.CTkEntry(self,placeholder_text=readconfigpath("root_path"),width = 250, height = 50)
                
                self.label_imageseq = customtkinter.CTkLabel(self, text="Image sequence folder directory", fg_color="transparent")
                self.entry_imageseq = customtkinter.CTkEntry(self,placeholder_text=readconfigpath("image_sequence_path"),width = 175, height = 50)
                self.button_create1 = customtkinter.CTkButton(self,width = 50, height = 50, text="Create", command=self.createdir1)
                self.dir1_status = False

                self.label_gifedit = customtkinter.CTkLabel(self, text="Directory of GIFs to edit", fg_color="transparent")
                self.entry_gifedit = customtkinter.CTkEntry(self,placeholder_text=readconfigpath("gif_edit_directory"),width = 175, height = 50)
                self.button_create3 = customtkinter.CTkButton(self,width = 50, height = 50, text="Create", command=self.createdir3)
                self.dir3_status = False

                self.label_gifsicle = customtkinter.CTkLabel(self, text="Gifsicle directory", fg_color="transparent")
                self.entry_gifsicle = customtkinter.CTkEntry(self,placeholder_text=readconfigpath("gifsicle_path"),width = 250, height = 50)
               
                self.label_viddir = customtkinter.CTkLabel(self, text="Videos directory", fg_color="transparent")
                self.entry_viddir = customtkinter.CTkEntry(self,placeholder_text=readconfigpath("videos_directory"),width = 175, height = 50)
                self.button_create2 = customtkinter.CTkButton(self,width = 50, height = 50, text="Create", command=self.createdir2)
                self.dir2_status = False   

                self.label_tempvid = customtkinter.CTkLabel(self, text="Temporary video directory", fg_color="transparent")
                self.entry_tempvid = customtkinter.CTkEntry(self,placeholder_text=readconfigpath("temporary_video_directory"),width = 175, height = 50)
                self.button_create4 = customtkinter.CTkButton(self,width = 50, height = 50, text="Create", command=self.createdir4)
                
                self.label_apply = customtkinter.CTkLabel(self, text="",fg_color="transparent",justify="center")
                self.settings_apply_button = customtkinter.CTkButton(self,width = 100,height = 25, text = "Apply dirs",command=self.SubmitDirectoryChanges)
                self.settings_exit_button = customtkinter.CTkButton(self,width = 100,height = 25, text = "Exit",command=self.exitsettings)                
                
                
                self.label_root.place(x=25,y=25)        
                self.entry_root.place(x=25,y=50)
                
                self.label_imageseq.place(x=25,y=125)
                self.entry_imageseq.place(x=25,y=150)
                self.button_create1.place(x=225,y=150)
                
                self.label_gifedit.place(x=25,y=225)
                self.entry_gifedit.place(x=25,y=250)
                self.button_create3.place(x=225,y=250)

                self.label_gifsicle.place(x=325,y=25)   
                self.entry_gifsicle.place(x=325,y=50)
                
                self.label_viddir.place(x=325,y=125)   
                self.entry_viddir.place(x=325,y=150)
                self.button_create2.place(x=525,y=150)
                
                self.label_tempvid.place(x=325,y=225)   
                self.entry_tempvid.place(x=325,y=250)
                self.button_create4.place(x=525,y=250)

                self.label_apply.place(x=102,y=325)
                self.settings_apply_button.place(x=100,y=350)  
                self.settings_exit_button.place(x=400,y=350)
              

            def SubmitDirectoryChanges(self):
                self.aredirectioriesvalid()
                if len(self.invaliddirectories) == 0:
                    self.label_apply.configure(text="Changes Applied")
                else:
                    if len(self.invaliddirectories) ==1:
                        self.errormsg(f"{"".join(self.invaliddirectories)} directory path is invalid")
                    elif len(self.invaliddirectories) >3:
                        self.invaliddirectoriesline1 = self.invaliddirectories[:3]
                        self.invaliddirectoriesline2 = self.invaliddirectoriesline2  = [item for item in self.invaliddirectories if item not in self.invaliddirectoriesline1]
                        self.errormsg(f"These directories are invalid:\n{", ".join(self.invaliddirectoriesline1)},\n{", ".join(self.invaliddirectoriesline2)}.")
                    else:
                        self.errormsg(f"These directories are invalid:\n{", ".join(self.invaliddirectories)}.")

            def createdir1(self):

                if self.entry_root.get() == "":
                    if ispathvalid("root_path"):
                            print("config ma valid root")
                            createfolder(readconfigpath("root_path"),"ImageSequence")
                            self.dir1_path = os.path.join(readconfigpath("root_path"), "ImageSequence")
                            self.dir1_status = True
                            ChangeConfigValue("image_sequence_path",self.dir1_path)

                            self.entry_imageseq.destroy()
                            self.entry_imageseq = customtkinter.CTkEntry(self,placeholder_text=self.dir1_path,width = 175, height = 50)
                            self.entry_imageseq.place(x=25,y=150)                        
                    else:
                        self.errormsg("Fill out Root directory")

                else:
                    if os.path.isdir(self.entry_root.get()):
                        print("root = valid")  
                        createfolder(self.entry_root.get(),"ImageSequence")
                        self.dir1_path = os.path.join(self.entry_root.get(), "ImageSequence")
                        self.dir1_status = True
                        ChangeConfigValue("image_sequence_path",self.dir1_path)

                        self.entry_imageseq.destroy()
                        self.entry_imageseq = customtkinter.CTkEntry(self,placeholder_text=self.dir1_path,width = 175, height = 50)
                        self.entry_imageseq.place(x=25,y=150)
                    else:
                        print("root = invalid")
                        self.errormsg("Root entry is invalid")

            def createdir2(self):

                if self.entry_root.get() == "":
                    if ispathvalid("root_path"):
                            print("config ma valid root")
                            createfolder(readconfigpath("root_path"),"Videos")
                            self.dir2_path = os.path.join(readconfigpath("root_path"), "Videos")
                            self.dir2_status = True
                            ChangeConfigValue("videos_directory",self.dir1_path)

                            self.entry_viddir.destroy()
                            self.entry_viddir = customtkinter.CTkEntry(self,placeholder_text=self.dir2_path,width = 175, height = 50)
                            self.entry_viddir.place(x=325,y=150)                        
                    else:
                        self.errormsg("Fill out Root directory")

                else:
                    if os.path.isdir(self.entry_root.get()):
                        print("root = valid")  
                        createfolder(self.entry_root.get(),"Videos")
                        self.dir2_path = os.path.join(self.entry_root.get(), "Videos")
                        self.dir2_status = True
                        ChangeConfigValue("videos_directory",self.dir1_path)

                        self.entry_viddir.destroy()
                        self.entry_viddir = customtkinter.CTkEntry(self,placeholder_text=self.dir2_path,width = 175, height = 50)
                        self.entry_viddir.place(x=325,y=150)
                    else:
                        print("root = invalid")
                        self.errormsg("Root entry is invalid")

            def createdir3(self):

                if self.entry_root.get() == "":
                    if ispathvalid("root_path"):
                            print("config ma valid root")
                            createfolder(readconfigpath("root_path"),"GIFStoEdit")
                            self.dir3_path = os.path.join(readconfigpath("root_path"), "GIFStoEdit")
                            self.dir3_status = True
                            ChangeConfigValue("gif_edit_directory",self.dir1_path)

                            self.entry_gifedit.destroy()
                            self.entry_gifedit = customtkinter.CTkEntry(self,placeholder_text=self.dir3_path,width = 150, height = 50)
                            self.entry_gifedit.place(x=25,y=250)                        
                    else:
                        self.errormsg("Fill out Root directory")

                else:
                    if os.path.isdir(self.entry_root.get()):
                        print("root = valid")  
                        createfolder(self.entry_root.get(),"GIFStoEdit")
                        self.dir3_path = os.path.join(self.entry_root.get(), "GIFStoEdit")
                        self.dir3_status = True
                        ChangeConfigValue("gif_edit_directory",self.dir1_path)

                        self.entry_gifedit.destroy()
                        self.entry_gifedit = customtkinter.CTkEntry(self,placeholder_text=self.dir3_path,width = 150, height = 50)
                        self.entry_gifedit.place(x=25,y=250)
                    else:
                        print("root = invalid")
                        self.errormsg("Root entry is invalid")

            def createdir4(self):

                if self.entry_root.get() == "":
                    if ispathvalid("root_path"):
                            print("config ma valid root")
                            createfolder(readconfigpath("root_path"),"TemporaryVideoDir")
                            self.dir4_path = os.path.join(readconfigpath("root_path"), "TemporaryVideoDir")
                            self.dir4_status = True
                            ChangeConfigValue("temporary_video_directory",self.dir1_path)

                            self.entry_tempvid.destroy()
                            self.entry_tempvid = customtkinter.CTkEntry(self,placeholder_text=self.dir4_path,width = 150, height = 50)
                            self.entry_tempvid.place(x=325,y=250)                        
                    else:
                        self.errormsg("Fill out Root directory")

                else:
                    if os.path.isdir(self.entry_root.get()):
                        print("root = valid")  
                        createfolder(self.entry_root.get(),"TemporaryVideoDir")
                        self.dir4_path = os.path.join(self.entry_root.get(), "TemporaryVideoDir")
                        self.dir4_status = True
                        ChangeConfigValue("temporary_video_directory",self.dir1_path)

                        self.entry_tempvid.destroy()
                        self.entry_tempvid = customtkinter.CTkEntry(self,placeholder_text=self.dir4_path,width = 150, height = 50)
                        self.entry_tempvid.place(x=325,y=250)
                    else:
                        print("root = invalid")
                        self.errormsg("Root entry is invalid")


            def aredirectioriesvalid(self):
                self.invaliddirectories = []                                        # invalid directories list
                
                #root

                if self.entry_root.get() == "":
                    if ispathvalid("root_path"):
                        print("root_path is valid")
                    else:
                        self.invaliddirectories.append("Root")    
                else:
                    if os.path.isdir(self.entry_root.get()):
                        print("root = valid")
                        self.new_root_path = self.entry_root.get()
                        ChangeConfigValue("root_path",self.new_root_path)
                    else:
                        self.invaliddirectories.append("Root")
                
                #gifsicle

                if self.entry_gifsicle.get() == "":
                    if ispathvalid("gifsicle_path"):
                        print("gifsicle_path is valid")
                    else:
                        self.invaliddirectories.append("Gifsicle")    
                else:
                    if os.path.isdir(self.entry_gifsicle.get()):
                        print("gifsicle = valid")
                        self.new_gifsicle_path = self.entry_gifsicle.get()
                        ChangeConfigValue("gifsicle_path",self.new_gifsicle_path)
                    else:
                        self.invaliddirectories.append("Gifsicle")
                
                #Image Sequence

                if self.entry_imageseq.get() == "":
                    if ispathvalid("image_sequence_path"):
                        print("Imageseq correct config path")
                    else:
                        self.invaliddirectories.append("Image Sequence")
                else:
                    if os.path.isdir(self.entry_imageseq.get()):
                        print("imageseq correct entry path")
                    else:
                        self.invaliddirectories.append("Image Sequence")
                
                #video

                if self.entry_viddir.get() == "":
                    if ispathvalid("videos_directory"):
                        print("viddir correct config path")
                    else:
                        self.invaliddirectories.append("Video")
                else:
                    if os.path.isdir(self.entry_viddir.get()):
                        print("viddir correct entry path")
                    else:
                        self.invaliddirectories.append("Video")
                
                #gif edit
                
                if self.entry_gifedit.get() == "":
                    if ispathvalid("gif_edit_directory"):
                        print("gifedit correct config path")
                    else:
                        self.invaliddirectories.append("GIFS to edit")
                else:
                    if os.path.isdir(self.entry_gifedit.get()):
                        print("gifedit correct entry path")
                    else:
                        self.invaliddirectories.append("GIFS to edit")
                
                #temporary video

                if self.entry_tempvid.get() == "":
                    if ispathvalid("temporary_video_directory"):
                        print("tempvid correct config path")
                    else:
                        self.invaliddirectories.append("Temporary video")
                else:
                    if os.path.isdir(self.entry_tempvid.get()):
                        print("tempvid correct entry path")
                    else:
                        self.invaliddirectories.append("Temporary video")


            def exitsettings(self):
                print("exiting")
                self.destroy()

            def getentry(self):
                print(self.entry_root.get())


            def button_callback(self):
                print("button clicked")
   
            #Popup error message

            def errormsg(self,errortext):
                class ErrorMessage(customtkinter.CTkToplevel):
                    def __init__(self):
                        super().__init__()
                        self.geometry("300x200")
                        self.title("Error")
                        
                        self.error_label = customtkinter.CTkLabel(self, text=errortext, fg_color="transparent")
                        self.error_label.pack (padx=10,pady=25)

                        self.error_exit_button = customtkinter.CTkButton(self,width = 100,height = 50, text = "Okay",command=self.exiterror)
                        self.error_exit_button.place(x=100,y=125)                        


                    def exiterror(self):
                        print("exiting")
                        self.destroy()


                errormessage = ErrorMessage()            

        settings = Settings()

    #entering gif creation

    def GifCreation(self):
        if CheckAllConfigPaths():
            class GifCreation(customtkinter.CTkToplevel):
                def __init__(self):
                    super().__init__()
                    self.geometry("600x400")

                    self.button_firstloadlay1 = customtkinter.CTkButton(self,width = 550, height = 160, text="Convert Videos", command=self.layout1 )
                    self.button_firstloadlay1.place(x=25,y=25)
                    self.button_firstloadlay2 = customtkinter.CTkButton(self,width = 550, height = 160, text="Convert Image Sequences", command=self.layout2 )
                    self.button_firstloadlay2.place(x=25,y=215)                    

                # LAYOUT 1

                def layout1(self):

                    self.button_firstloadlay1.destroy()
                    self.button_firstloadlay2.destroy()

                    self.title("GIF creation")

                    self.label_name = customtkinter.CTkLabel(self, text="Video Name", fg_color="transparent")
                    self.label_percentage = customtkinter.CTkLabel(self, text=(r"% frames kept"), fg_color="transparent")
                    self.label_msvid = customtkinter.CTkLabel(self, text="Frame delay in ms", fg_color="transparent")
                    self.label_fpsframes = customtkinter.CTkLabel(self, text="", fg_color="transparent")
                    self.label_msframes = customtkinter.CTkLabel(self, text="", fg_color="transparent")
                    self.label_vidloaded = customtkinter.CTkLabel(self,text="",height=125,width=125,fg_color="gray20")                    
                    self.label_vidgif = customtkinter.CTkLabel(self,text="",height=125,width=125,fg_color="gray20",)

                    self.entry_percentage = customtkinter.CTkEntry(self,placeholder_text="0.1-1",width = 50, height = 50)
                    self.entry_msvid = customtkinter.CTkEntry(self,placeholder_text="ms",width = 50, height = 50)
                    self.entry_name = customtkinter.CTkEntry(self,placeholder_text="Enter the name of the video",width = 300, height = 50)

                    self.button_layout2 = customtkinter.CTkButton(self,width = 100, height = 50, text="Change Mode", command=self.switchtolay2)
                    self.button_convert = customtkinter.CTkButton(self,width = 100, height = 50, text="Convert", command=self.creategiffromvideo)
                    self.button_exitvid = customtkinter.CTkButton(self,width = 100, height = 50, text="Exit", command=self.exitcrt)
                    self.button_load = customtkinter.CTkButton(self,width = 75, height = 50, text="Load", command=self.start_video)                    

                    self.label_name.place(x=25,y=25)   
                    self.label_percentage.place(x=73,y=125)
                    self.label_msvid.place(x=182,y=125)
                    self.label_fpsframes.place(x=450,y=25)
                    self.label_msframes.place(x=450,y=225)
                    self.label_vidloaded.place(x=450,y=50)                    
                    self.label_vidgif.place(x=450,y=250)

                    self.entry_percentage.place(x=91,y=150)
                    self.entry_msvid.place(x=207,y=150)
                    self.entry_name.place(x=25,y=50)

                    self.button_convert.place(x=25,y=250)
                    self.button_load.place(x=350,y=50)
                    self.button_layout2.place(x=150,y=325)
                    self.button_exitvid.place(x=25,y=325)

                    


                    self.isvideoloaded = False
                    self.vidconvertvar = False
                    self.vidsavebuttons = False

 

                    self.cap = None
                    self.playing = False

                    self.gif_frames = []
                    self.current_frame = 0
                    self.gif_running = False

                def destroyvideogui(self):
                    self.stopgifvidplayback()
                    self.button_firstloadlay1.destroy()
                    self.label_name.destroy()
                    self.label_percentage.destroy()
                    self.label_msvid.destroy()
                    self.label_fpsframes.destroy()
                    self.label_msframes.destroy()
                    self.label_vidgif.destroy()
                    self.entry_percentage.destroy()
                    self.entry_msvid.destroy()
                    self.button_convert.destroy()
                    self.button_exitvid.destroy()
                    self.entry_name.destroy()
                    self.label_vidloaded.destroy()
                    self.button_load.destroy()
                    self.button_layout2.destroy()
                    if self.vidsavebuttons == True:
                        self.destroyvidsavebuttons

                def destroyisgui(self):
                    self.label_isext.destroy()
                    self.label_isms.destroy()
                    self.label_isloop.destroy()
                    self.label_isgifsaved.destroy()
                    self.label_isloadedgif.destroy()
                    self.entry_isext.destroy()
                    self.entry_isms.destroy()
                    self.button_exitis.destroy()
                    self.button_layout1.destroy()
                    self.button_isloopinf.destroy()
                    self.button_isloopamnt.destroy()
                    self.label_ismsframes.destroy()

                    if self.loopspressed == 1:
                        self.button_isgoback.destroy() 
                        self.button_isconvert.destroy()
                    if self.customloopsstate == True:
                        self.entry_isloopamount.destroy()
                    if self.isconverton == True:
                        self.entry_isgifname.destroy()
                        self.button_issave.destroy()

                def switchtolay2(self):
                    self.destroyvideogui()
                    self.layout2()

                def switchtolay1(self):
                    self.destroyisgui()
                    self.layout1()

                def start_video(self):
                    if self.entry_name.get() == "":
                        self.errormsgcrt("Input the video name")
                    elif os.path.exists(os.path.join(readconfigpath("videos_directory"),(self.entry_name.get()+".mp4"))):                                     
                        if self.vidconvertvar == True:
                            self.destroyvidsavebuttons()
                        self.label_msframes.configure(text="")
                        self.stopgifvidplayback()
                        print(os.path.join(readconfigpath("videos_directory"),(self.entry_name.get()+".mp4")))
                        self.cap = cv2.VideoCapture(os.path.join(readconfigpath("videos_directory"),(self.entry_name.get()+".mp4")))
                        self.playing = True
                        self.update_frame()
                        self.videogif_path = os.path.join(readconfigpath("videos_directory"),(self.entry_name.get()+".mp4"))
                        print(self.videogif_path)
                        self.isvideoloaded = True
                        self.loaded_vid_framerate = check_video_fps(os.path.join(readconfigpath("videos_directory"),(self.entry_name.get()+".mp4")))
                        self.label_fpsframes.configure(text=((f"FPS: {int(self.loaded_vid_framerate)}")))
                    else:
                        self.errormsgcrt("Input a valid video name")

                def update_frame(self):
                    if self.playing and self.cap is not None:
                        ret, frame = self.cap.read()
                        if ret:
                            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                            img = Image.fromarray(frame).convert("RGBA")
                            img.thumbnail((125, 125))
                            background = Image.new("RGBA", (125, 125), (0, 0, 0, 0))
                            x = (125 - img.width) // 2
                            y = (125 - img.height) // 2
                            background.paste(img, (x, y), img)
                            self.current_ctk_img = CTkImage(light_image=background, size=(125, 125))
                            self.label_vidloaded.configure(image=self.current_ctk_img)
                        else:
                            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                        self.after(33, self.update_frame)

                def button_callback(self):
                    print("button clicked")
                
                def arevidfieldsvalid(self):
                    if self.entry_msvid.get() == "" or self.entry_percentage.get() == "":
                        print(2)
                        return 2
                    elif 0< float(self.entry_percentage.get())<1 and int(self.entry_msvid.get())>0:
                        print(1)
                        return 1
                    elif float(self.entry_percentage.get()) < 0 or float(self.entry_percentage.get()) > 1:
                        print(3)
                        return 3
                    elif int(self.entry_msvid.get()) <=0:
                        print(4)
                        return 4
                    else:
                        print(5)
                        return 5

                def creategiffromvideo(self):
                    self.vidconvertvar = True
                    if self.isvideoloaded == False and self.arevidfieldsvalid() > 1:
                        self.errormsgcrt("Please load the video,\n then fill out the fields correctly")
                    elif self.isvideoloaded == False:
                        self.errormsgcrt("Please load the video first")
                    elif self.arevidfieldsvalid() == 2:
                        self.errormsgcrt("Please input values into the fields")
                    elif self.arevidfieldsvalid() >2:
                        self.errormsgcrt("Please fill out the fields correctly")
                    elif self.isvideoloaded == True and self.arevidfieldsvalid() == 1:
                        extract_frames_then_gif(self.videogif_path,float(self.entry_percentage.get()),int(self.entry_msvid.get()))
                        self.vidgifFrames = (len([name for name in os.listdir(readconfigpath("temporary_video_directory")) if os.path.isfile(os.path.join(readconfigpath("temporary_video_directory"), name))])) - 1
                        self.play_gif(os.path.join(readconfigpath("temporary_video_directory"),"temp_gif.gif"))
                        self.label_msframes.configure(text=(f"Frames: {self.vidgifFrames}, ms: {self.entry_msvid.get()}"))
                        self.entry_vidsavename = customtkinter.CTkEntry(self,placeholder_text="Enter Name",width = 100, height = 50)
                        self.button_savevid = customtkinter.CTkButton(self,width = 100, height = 50, text="Save", command=self.SavingVidGif)
                        self.label_vidsaved = customtkinter.CTkLabel(self, text="", fg_color="transparent")
                        self.entry_vidsavename.place(x=300,y=250)
                        self.button_savevid.place(x=300,y=325)
                        self.label_vidsaved.place(x=293,y=375)
                        self.vidsavebuttons = True
                    

                def play_gif(self, gif_path):
                    gif = Image.open(gif_path)
                    self.gif_frames = []
                    self.current_frame = 0
                    self.gif_running = True
                    self.gif_duration = gif.info.get("duration", 100)

                    for frame in ImageSequence.Iterator(gif):
                        frame = frame.convert("RGBA")
                        frame.thumbnail((125, 125))
                        background = Image.new("RGBA", (125, 125), (0, 0, 0, 0))
                        x = (125 - frame.width) // 2
                        y = (125 - frame.height) // 2
                        background.paste(frame, (x, y), frame)
                        self.gif_frames.append(ImageTk.PhotoImage(background))

                    def animate():                      
                        if self.gif_running and self.gif_frames:
                            self.label_vidgif.configure(image=self.gif_frames[self.current_frame])
                            self.current_frame = (self.current_frame + 1) % len(self.gif_frames)
                            self.after(self.gif_duration, animate)

                    animate()

                def stopgifvidplayback(self):
                    self.gif_running = False
                    self.label_vidgif.configure(image="")
                    self.playing = False
                    self.label_vidloaded.configure(image="")

                def SavingVidGif(self):
                    if self.entry_vidsavename.get() == "":
                        self.label_vidsaved.configure(text="Please input a name")
                    elif os.path.exists(os.path.join(readconfigpath("root_path"),(self.entry_vidsavename.get()+".gif"))):
                        print("Ten plik już istnieje")
                        
                        self.label_vidsaved.configure(text="GIF already exists")
                        
                    else:
                        os.rename(os.path.join(readconfigpath("temporary_video_directory"), "temp_gif.gif"),os.path.join(readconfigpath("root_path"), (self.entry_vidsavename.get()+".gif")))
                        czyszczenie_plikow_temp(readconfigpath("temporary_video_directory"))
                        self.destroyvidsavebuttons()
                        self.label_msframes.configure(text="")
                        self.label_fpsframes.configure(text="")
                        self.stopgifvidplayback()

                def destroyvidsavebuttons(self):
                        self.entry_vidsavename.destroy()
                        self.button_savevid.destroy()
                        self.label_vidsaved.destroy()

                # LAYOUT 2

                def layout2(self):

                    self.customloopsstate = False
                    self.loopspressed = 0
                    self.isconverton = False

                    self.button_firstloadlay1.destroy()
                    self.button_firstloadlay2.destroy()

                    self.label_isext = customtkinter.CTkLabel(self, text="File extension", fg_color="transparent")
                    self.label_isms = customtkinter.CTkLabel(self, text="Frame delay in ms", fg_color="transparent")
                    self.label_isloop = customtkinter.CTkLabel(self, text="Amount of loops", fg_color="transparent")
                    self.label_isgifsaved = customtkinter.CTkLabel(self, text="", fg_color="transparent")
                    self.label_ismsframes = customtkinter.CTkLabel(self, text="", fg_color="transparent")
                    self.label_isloadedgif = customtkinter.CTkLabel(self,text="",height=200,width=200,fg_color="gray20",)

                    self.entry_isext = customtkinter.CTkEntry(self,placeholder_text=".jpg/.jpeg/png",width = 100, height = 50)
                    self.entry_isms = customtkinter.CTkEntry(self,placeholder_text="ms",width = 50, height = 50)

                    self.button_exitis = customtkinter.CTkButton(self,width = 100, height = 50, text="Exit", command=self.exitcrt)
                    self.button_layout1 = customtkinter.CTkButton(self,width = 100, height = 50, text="Change Mode", command=self.switchtolay1)
                    self.button_isloopinf = customtkinter.CTkButton(self,width = 100, height = 25, text="∞", command=self.infiniteloops)
                    self.button_isloopamnt = customtkinter.CTkButton(self,width = 100, height = 25, text="Custom",state= "disabled", command=self.customloops)

                    self.label_isext.place(x=35,y=25)
                    self.label_isms.place(x=175,y=25)
                    self.label_isloop.place(x=100,y=125)
                    self.label_isloadedgif.place(x=375,y=25)
                    self.label_isgifsaved.place(x=425,y=375)
                    self.label_ismsframes.place(x=375,y=0)

                    self.entry_isext.place(x=25,y=50)
                    self.entry_isms.place(x=200,y=50)              

                    self.button_exitis.place(x=25,y=325)
                    self.button_layout1.place(x=150,y=325)
                    self.button_isloopinf.place(x=25,y=150)
                    self.button_isloopamnt.place(x=175,y=150)

                    self.cap = None
                    self.playing = False

                    self.gif_frames = []
                    self.current_frame = 0
                    self.gif_running = False
                
                def infiniteloops(self):

                    if self.iserrorcheck() == 1:
                        if self.hasfilewithextension(self.entry_isext.get()):
                            print("No custom loops!")
                            self.customloopsstate = False
                            self.loopspressed = 1

                            self.button_isloopinf.configure(state="disabled")
                            self.button_isloopamnt.configure(state="disabled")                   

                            self.button_isgoback = customtkinter.CTkButton(self,width = 100, height = 25, text="Go Back", command=self.goback)
                            self.button_isgoback.place(x=100,y=200)

                            self.button_isconvert = customtkinter.CTkButton(self,width = 100, height = 50, text="Convert", command=self.isconvertbutton)
                            self.button_isconvert.place(x=100,y=250)      
                        else:
                            self.errormsgcrt("There are no files with this extension\n in the Image Sequence directory")
                    elif self.iserrorcheck() == 2:
                        self.errormsgcrt("Please fill out both fields")
                    elif self.iserrorcheck() >2:
                        self.errormsgcrt("Please input valid values")                                  

                def customloops(self):
                    if self.iserrorcheck() == 1:
                        if self.hasfilewithextension(self.entry_isext.get()):
                            print("custom loops!")
                            self.customloopsstate = True
                            self.loopspressed = 1

                            self.button_isloopinf.configure(state="disabled")
                            self.button_isloopamnt.configure(state="disabled")


                            self.entry_isloopamount = customtkinter.CTkEntry(self,placeholder_text="Enter amount",width = 100, height = 25)
                            self.button_isgoback = customtkinter.CTkButton(self,width = 100, height = 25, text="Go Back", command=self.goback)

                            self.entry_isloopamount.place(x=175,y=200)
                            self.button_isgoback.place(x=25,y=200)

                            self.button_isconvert = customtkinter.CTkButton(self,width = 100, height = 50, text="Convert", command=self.isconvertbutton)
                            self.button_isconvert.place(x=100,y=250)
                        else:
                            self.errormsgcrt("There are no files with this extension\n in the Image Sequence directory")
                    elif self.iserrorcheck() == 2:
                        self.errormsgcrt("Please fill out both fields")
                    elif self.iserrorcheck() >2:
                        self.errormsgcrt("Please input valid values")


                def goback(self):
                    if self.customloopsstate == False:
                        self.button_isloopinf.configure(state="normal")
                        # self.button_isloopamnt.configure(state="normal")
                        self.button_isgoback.destroy()
                        self.button_isconvert.destroy()
                        self.stopisgifplayback()
                    elif self.customloopsstate == True:
                        self.button_isloopinf.configure(state="normal")
                        # self.button_isloopamnt.configure(state="normal")
                        self.button_isgoback.destroy()
                        self.entry_isloopamount.destroy()                        
                        self.button_isconvert.destroy()
                        self.stopisgifplayback()
                    if self.isconverton == True:
                        self.entry_isgifname.destroy()
                        self.button_issave.destroy()
                        self.stopisgifplayback()

                def isconvertbutton(self):
                    print("test")
                    print (f"loopy to :{self.customloopcheck()}")
                    if self.customloopcheck() in [1,11]:
                        if self.iserrorcheck() == 1:
                            if self.hasfilewithextension(self.entry_isext.get()):                              
                              
                              
                                if self.customloopsstate == False:
                                    self.entry_isloopamount = customtkinter.CTkEntry(self,placeholder_text="Enter amount",width = 100, height = 25)
                                self.isconverton = True
                                self.entry_isgifname = customtkinter.CTkEntry(self,placeholder_text="Enter the name",width = 200, height = 50)
                                self.button_issave = customtkinter.CTkButton(self,width = 100, height = 50, text="Save", command=self.SavingISGif)
                                self.entry_isgifname.place(x=375,y=250) 
                                self.button_issave.place(x=425,y=325)

                                self.isext = self.entry_isext.get()
                                self.isms = int(self.entry_isms.get())
                                self.ispath = readconfigpath("image_sequence_path")
                                self.isimageoutpath = os.path.join(readconfigpath("image_sequence_path"),"temp_gif.gif")
                                self.isloopamount = self.entry_isloopamount.get()
                                self.label_isloadedgif.configure(image="")
                                deleteafile(self.isimageoutpath)
                                print(f"ilość loopów{self.isloopamount}")
                                self.vidisFrames = (len([name for name in os.listdir(readconfigpath("image_sequence_path")) if os.path.isfile(os.path.join(readconfigpath("image_sequence_path"), name))]))
                                self.label_ismsframes.configure(text=(f"Frames: {self.vidisFrames}, ms: {self.entry_isms.get()}"))

                                if self.customloopsstate == False:
                                    self.make_isgif(self.ispath,self.isimageoutpath,self.isext,self.isms,0)
                                    self.isplay_gif(self.isimageoutpath)  
                                elif self.customloopsstate == True:
                                    self.make_isgif(self.ispath,self.isimageoutpath,self.isext,self.isms,self.entry_isloopamount.get())
                                    self.isplay_gif(self.isimageoutpath)                      
                            else:
                                self.errormsgcrt("There are no files with this extension\n in the Image Sequence directory")
                        elif self.iserrorcheck() == 2:
                            self.errormsgcrt("Please fill out both fields")
                        elif self.iserrorcheck() >2:
                            self.errormsgcrt("Please input valid values")   



                    elif self.iserrorcheck() == 2 or self.customloopcheck == 2:
                        self.errormsgcrt("Please input values into fields")

                def make_isgif(self,frame_folder,image_file_path,image_sequence_ext,delay_frame,loops):
                    frames = [Image.open(image) for image in glob.glob(f"{frame_folder}/*{image_sequence_ext}")]
                    frame_one = frames[0]
                    frame_one.save(fp = image_file_path, format="GIF", append_images=frames,
                            save_all=True, duration=delay_frame, loop=int(loops))

                def iserrorcheck(self):
                    if self.entry_isext.get() == "" or self.entry_isms.get() == "":
                        print(2)
                        return 2
                    elif self.entry_isext.get() not in [".jpg",".jpeg",".png"]:
                        print(3)
                        return 3
                    elif self.entry_isms.get().isnumeric() == False:
                        print(4)
                        return 4
                    elif self.entry_isext.get() in [".jpg",".jpeg",".png"] and self.entry_isms.get().isnumeric:
                        print(1)
                        return 1
                    else: 
                        print(5)
                        return 5
                
                def customloopcheck(self):
                    if self.customloopsstate == True:
                        if self.entry_isloopamount.get() == "":
                            print(2222)
                            return 2                            

                        elif self.entry_isloopamount.get().isnumeric() == False:
                            print(3)
                            return 3                        

                        elif self.entry_isloopamount.get().isnumeric():
                            print(1)
                            return 1
                    elif self.customloopsstate == False:
                        print(11)
                        return 11
                    
                def hasfilewithextension(self,does_exist_extension):

                    for root, dirs, files in os.walk(readconfigpath("image_sequence_path")):
                        for file in files:
                            if file.endswith(does_exist_extension):
                                return True
                    return False

                def isplay_gif(self, gif_path):
                    gif = Image.open(gif_path)
                    self.gif_frames = []
                    self.current_frame = 0
                    self.gif_running = True
                    self.gif_duration = gif.info.get("duration", 100)

                    for frame in ImageSequence.Iterator(gif):
                        frame = frame.convert("RGBA")
                        frame.thumbnail((200, 200))
                        background = Image.new("RGBA", (200, 200), (0, 0, 0, 0))
                        x = (200 - frame.width) // 2
                        y = (200 - frame.height) // 2
                        background.paste(frame, (x, y), frame)
                        self.gif_frames.append(ImageTk.PhotoImage(background))

                    def animate():                      
                        if self.gif_running and self.gif_frames:
                            self.label_isloadedgif.configure(image=self.gif_frames[self.current_frame])
                            self.current_frame = (self.current_frame + 1) % len(self.gif_frames)
                            self.after(self.gif_duration, animate)



                    animate()


                def SavingISGif(self):
                    if self.entry_isgifname.get() == "":
                        self.label_isgifsaved.configure(text="Please input a name")
                    elif os.path.exists(os.path.join(readconfigpath("root_path"),(self.entry_isgifname.get()+".gif"))):
                        print("Ten plik już istnieje")
                        self.label_isgifsaved.configure(text="GIF already exists")   
                    else:
                        os.rename(os.path.join(readconfigpath("image_sequence_path"), "temp_gif.gif"),os.path.join(readconfigpath("root_path"), (self.entry_isgifname.get()+".gif")))
                        czyszczenie_plikow_temp(readconfigpath("temporary_video_directory"))
                        self.destroyissavebuttons()
                        self.stopisgifplayback()

                def stopisgifplayback(self):
                    self.label_ismsframes.configure(text="")
                    self.gif_running = False
                    self.label_isloadedgif.configure(image="")

                def destroyissavebuttons(self):
                    self.entry_isgifname.destroy()
                    self.button_issave.destroy()
                    self.label_isgifsaved.destroy()

                # ERROR MESSAGE

                def errormsgcrt(self,errortext):
                    class ErrorMessageCrt(customtkinter.CTkToplevel):
                        def __init__(self):
                            super().__init__()
                            self.geometry("300x200")
                            self.title("Error")
                            
                            self.error_label = customtkinter.CTkLabel(self, text=errortext, fg_color="transparent")
                            self.error_label.pack (padx=10,pady=25)

                            self.error_exit_button = customtkinter.CTkButton(self,width = 100,height = 50, text = "Okay",command=self.exiterror)
                            self.error_exit_button.place(x=100,y=125)                        
                        def exiterror(self):
                            print("exiting")
                            self.destroy()
                    errormessagecrt = ErrorMessageCrt()  

                # EXIT BUTTON

                def exitcrt(self):
                    print("exiting")
                    self.destroy()                

            gifcreation = GifCreation()
        else:
            self.MainMenuerror("Please input valid directories\nin the settings.")
mainmenu = MainMenu()
mainmenu.mainloop()
