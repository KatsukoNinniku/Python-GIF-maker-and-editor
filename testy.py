import customtkinter


    
class MyFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # add widgets onto the frame...
        self.button_optimize = customtkinter.CTkButton(self, width = 298,text = "Optimize",command = self.button_callback)
        self.button_optimize.grid(row=0, column=0, padx=0)
        self.button_accell = customtkinter.CTkButton(self, width = 298,text = "Change speed", command = self.button_callback)
        self.button_accell.grid(row=1, column=0, pady=6)
        self.button_text = customtkinter.CTkButton(self, width = 298,text = "Add text", command = self.button_callback)
        self.button_text.grid(row=2, column=0, padx=0)
        # self.button4 = customtkinter.CTkButton(self, width = 248)
        # self.button4.grid(row=3, column=0, pady=6)
        # self.button5 = customtkinter.CTkButton(self, width = 248)
        # self.button5.grid(row=4, column=0, padx=0)
        # self.button6 = customtkinter.CTkButton(self, width = 248)
        # self.button6.grid(row=5, column=0, pady=6)
    def button_callback(self):
        print("button clicked")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("900x400")
        
        self.label_loadedgifname = customtkinter.CTkLabel(self,text="Loaded GIF:",fg_color="transparent")
        self.label_outputgifname = customtkinter.CTkLabel(self,text="Output:",fg_color="transparent")
        self.label_loadedgif = customtkinter.CTkLabel(self,text="",height=160,width=160,fg_color="gray20")
        self.label_outputgif = customtkinter.CTkLabel(self,text="",height=160,width=160,fg_color="gray20")

        self.entry_name = customtkinter.CTkEntry(self,placeholder_text="Enter name or select it",width = 175, height = 50)


        self.button_filedialog = customtkinter.CTkButton(self,width = 122, height = 20, text="Select from disk", command=self.button_callback)
        self.button_load = customtkinter.CTkButton(self,width = 122, height = 20, text="Load from name", command=self.button_callback)
        
        self.my_frame = MyFrame(master=self, width=300, height=265)
        
        self.entry_name.place(x=25,y=25)

        self.label_loadedgifname.place(x=715,y=0)
        self.label_outputgifname.place(x=715,y=190)
        self.label_loadedgif.place(x=715,y=25)
        self.label_outputgif.place(x=715,y=215)
        
        
        self.button_filedialog.place(x=225,y=25)
        self.button_load.place(x=225,y=53)
        
        
        
        self.my_frame.place(x=25,y=100)

    def button_callback(self):
        print("button clicked")
app = App()
app.mainloop()