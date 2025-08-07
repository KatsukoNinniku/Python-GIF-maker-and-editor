from customtkinter import filedialog    
def selectfile():
        filename = filedialog.askdirectory()
        print(filename)

selectfile()