from customtkinter import filedialog    

def selectfile():
    filename = filedialog.askopenfilename(
        filetypes=[("MP4 files", "*.mp4")]
    )
    print(filename)

selectfile()