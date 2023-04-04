import tkinter as tk
from PIL import ImageTk, Image, ImageOps
import json
import cv2

class MyVideoCapture:
    def __init__(self, video_source=0):
         # Open the video source
         self.vid = cv2.VideoCapture(video_source)
         if not self.vid.isOpened():
             raise ValueError("Unable to open video source", video_source)
 
         # Get video source width and height
         self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
         self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
         self.length = self.vid.get(cv2.CAP_PROP_FRAME_COUNT)
         self.fps = self.vid.get(cv2.CAP_PROP_FPS) 
         self.isEmpty = False
 
     # Release the video source when the object is destroyed
    def clear(self):
         if self.vid.isOpened():
            self.isEmpty = True
            self.vid.release()

    def get_frame(self):
         if self.vid.isOpened():
             ret, frame = self.vid.read()
             if ret:
                 # Return a boolean success flag and the current frame converted to BGR
                 return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
             else:
                print("None 1")
                return (ret, None)
         else:
            print("None 2")
            return (None, None)     

class App(tk.Tk):

    def is_horizontal(self,image):
        width, height = image.size
        if(width>height):
            return True
        else:
            return False    

    def resize_image(self,path,canvas):
        image = Image.open(path)
        image = ImageOps.exif_transpose(image)
        print(image.size)
        if(self.is_horizontal(image)):
            screen_width = max(canvas.winfo_width(),1520)
            multip = screen_width / image.size[0]
            image = image.resize((int(image.size[0]*multip), int(image.size[1]*multip)), Image.LANCZOS)
        else:
            screen_height = max(canvas.winfo_height(),868)
           
            multip = screen_height / image.size[1]
            image = image.resize((int(image.size[0]*multip), int(image.size[1]*multip)), Image.LANCZOS)

        return ImageTk.PhotoImage(image)

    def resize_video(self,image,canvas):
        #image = ImageOps.exif_transpose(image)
        print(image.size)
        if(self.is_horizontal(image)):
            screen_width = max(canvas.winfo_width(),1520)
            multip = screen_width / image.size[0]
            image = image.resize((int(image.size[0]*multip), int(image.size[1]*multip)), Image.LANCZOS)
        else:
            screen_height = max(canvas.winfo_height(),868)
           
            multip = screen_height / image.size[1]
            image = image.resize((int(image.size[0]*multip), int(image.size[1]*multip)), Image.LANCZOS)

        return ImageTk.PhotoImage(image)

    def get_image(self,canvas):
        if(self.pictures["list"][self.pictures["current"]["number"]]["type"]=="image"):
            next_pic =  {
                    "file":self.resize_image(self.image_path+self.pictures["list"][self.pictures["current"]["number"]]["file"],canvas),
                    "date":self.pictures["list"][self.pictures["current"]["number"]]["date"],
                    "type":"image"
                }
            if(self.video != None):
                self.video.clear();
            print(self.pictures["list"][self.pictures["current"]["number"]])
            return next_pic
        elif(self.pictures["list"][self.pictures["current"]["number"]]["type"]=="video"):
            self.video = MyVideoCapture(self.image_path+self.pictures["list"][self.pictures["current"]["number"]]["file"])
            next_pic =  {
                    "file":self.video,
                    "date":self.pictures["list"][self.pictures["current"]["number"]]["date"],
                    "type":"video"
                }
            self.videoCounter = 0  
            self.isLastFrame = False  
            return next_pic    

    def show_image(self):
        #display next item in iterator
        image_object = self.pictures["current"]["obj"]["file"]
        image_date = self.pictures["current"]["obj"]["date"]
        print("Show: " + image_date)
        #display the images with title after specified time
        self.canvas.delete("all")
        width, height = max(self.canvas.winfo_width(),1520), max(self.canvas.winfo_height(),868)
        self.canvas.create_image(width/2,height/2, anchor=tk.CENTER,image=image_object)

    def show_frame(self):
        #display next item in iterator
        
        if(self.isLastFrame):
            image_object = Image.open(self.blankImage)
            image_object = ImageTk.PhotoImage(image_object)
        else:
            _,image_frame = self.video.get_frame()
            image_object = Image.fromarray(image_frame)
            image_object = self.resize_video(image_object,canvas=self.canvas)
        image_date = self.pictures["current"]["obj"]["date"]
        print("Show: " + image_date)
        #display the images with title after specified time
        self.canvas.delete("all")
        width, height = max(self.canvas.winfo_width(),1520), max(self.canvas.winfo_height(),868)
        self.canvas.create_image(width/2,height/2, anchor=tk.CENTER,image=image_object)

    def next_button(self):
        stop = False
        self.pictures["prev"] = self.pictures["current"]["obj"]
        self.pictures["current"]["obj"] = self.pictures["next"]
        if( self.pictures["current"]["number"] >= len( self.pictures["list"])-1):
            stop = True
        else:
            self.pictures["current"]["number"] = self.pictures["current"]["number"] + 1
            self.pictures["next"] = self.get_image(self.canvas)
        print("Next en: "+str(self.pictures["current"]["number"] ))
        self.before_next = 0
        self.show_image()
        
        if(stop):
            self.right_button.state=tk.DISABLED 
        else:
            self.right_button.state=tk.NORMAL  


    def prev_button(self):
        stop = False
        self.pictures["next"] = self.pictures["current"]["obj"]
        self.pictures["current"]["obj"] = self.pictures["prev"]
        self.pictures["current"]["number"] = self.pictures["current"]["number"] - 1
        if( self.pictures["current"]["number"] <= 0):
            self.pictures["current"]["number"] = 0
            stop = True
        else:
            self.pictures["prev"] = self.get_image(self.canvas)
        print("Prev en: "+str(self.pictures["current"]["number"] ))
        self.before_next = 0
        self.show_image()
        
        if(stop):
            self.left_button.state=tk.DISABLED 
        else:
            self.left_button.state=tk.NORMAL  

    def pause_button(self):
        self.paused = not self.paused;
        if(self.paused):
            self.pause_button.config(text="▷")
        else:
           self.pause_button.config(text="||")

    '''constructor to initialize and define'''
    def __init__(self,image_files,json_path,image_path,blankImage):
        #form a Tkinter window
        tk.Tk.__init__(self)


        #assign customized geometry
        #self.geometry(f'{x}x{y}')
        self.attributes('-fullscreen', True)
        self.config(bg="black")
        self.blankImage = blankImage
        self.paused = False;

        left_frame = tk.Frame(self, width=15, height=self.winfo_screenheight(), bg='grey',name = "leftframe")
        left_frame.grid(row=0, column=0)
        right_frame = tk.Frame(self, width=self.winfo_screenwidth()-15, height=self.winfo_screenheight(), bg='grey')
        right_frame.grid(row=0, column=1)
        #create lable to display pictures
        self.canvas = tk.Canvas(right_frame,bg="yellow", width=self.winfo_screenwidth()-15, height=self.winfo_screenheight())
        self.canvas.grid(row=0,column=0)

        self.slider = tk.Scale(
        left_frame,
        from_=1,
        to=10,
        orient='vertical',
        showvalue=0,
        length=500,
        width = 15,
        resolution = 0.1,
        name = "myslider"
        )
        self.slider.set(5)
        self.slider.grid(row=1, column=0) 
        self.right_button = tk.Button( left_frame, text =">",command = self.next_button)
        self.right_button.grid(row=2, column=0) 
        self.left_button = tk.Button( left_frame, text ="<",command= self.prev_button)
        self.left_button.grid(row=3, column=0) 
        self.pause_button = tk.Button( left_frame, text ="▷",command= self.pause_button)
        self.pause_button.grid(row=4, column=0) 
       

        self.before_next = int(self.slider.get()*1000)
        self.video = None
        self.videoCounter = 0
        self.isLastFrame = False

        #create pictures
        self.pictures = {}
        self.image_path = image_path;
        self.pictures["list"] = json.load(open(json_path))
        self.pictures["current"] = {}
        self.pictures["current"]["obj"] = None
        self.pictures["current"]["number"] = 0
        self.pictures["prev"] = None
        self.pictures["next"] = self.get_image(self.canvas)

       

    '''function to display the slides'''
    def show_slides(self):
        if( self.pictures["current"]["number"] >= len( self.pictures["list"])-1):
            self.before_next = 0
        if(self.video == None or self.video.isEmpty):
             if(self.before_next>=int(self.slider.get()*1000)):
                self.next_button()
        else:
            if(self.before_next>=self.video.length*self.video.fps):
                self.next_button()
        if(not self.paused):
            self.before_next = self.before_next + 1        
        if(self.video != None and not self.video.isEmpty):
            if(self.before_next >= (self.video.length-2)*self.video.fps):
                self.isLastFrame = True
            if(self.videoCounter>=self.video.fps):
                self.videoCounter = 0
                self.show_frame()
            self.videoCounter = self.videoCounter + 1;    
        self.after(1,self.show_slides)
    
    '''function to run the window'''
    def run(self):
        self.mainloop()

'''main function''' 

config = json.load(open('config.json'))


#image files name
image_files = [
        '1.jpg',
        '2.jpg',
        '3.jpg',
        '4.jpg',
        '5.jpg']



jsonPath = config["jsonPath"]

#call the App
app = App(image_files,jsonPath,config["imagePath"],config["blankImage"])
app.show_slides()
app.run()