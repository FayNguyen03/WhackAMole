import tkinter as tk
from tkinter import PhotoImage
from tkinter import messagebox
import random

#Whack-a-mole
def main():
    #Create the entire GUI program
    program = WhackAMole()

    #Start the GUI event loop
    program.window.mainloop()

class WhackAMole():
    
    STATUS_BACKGROUND = "peachpuff"
    NUM_MOLE_ACROSS = 2
    MIN_TIME_DOWN = 1000
    MIN_TIME_UP = 3000
    MAX_TIME_DOWN = 5000
    MAX_TIME_UP = 7000

    def __init__ (self):
        
        self.window = tk.Tk()
        self.mole_frame, self.status_frame = self.create_frames()
        
        self.mole_photo = PhotoImage(file = "mole.png")
        self.mole_cover_photo = PhotoImage(file = "C:\\Users\\ntkha\\Documents\\CODING\\PYTHON\\PYTHON\\tkinter\\WhackAMole\\mole_cover.png")
        
        self.label_timers = {}
        self.mole_labels = self.create_moles()

        self.hit_counter, self.miss_counter, self.start_button, self.quit_button = self.create_status_widgets()
        
        self.set_callbacks()
        self.game_is_running = False
        
    def create_frames(self):
        
        mole_frame = tk.Frame(self.window, bg = "lightgreen", width = 300, height = 300)
        mole_frame.grid(row = 1, column = 1)

        status_frame = tk.Frame(self.window, bg = WhackAMole.STATUS_BACKGROUND, width = 100, height =300)
        status_frame.grid(row = 1, column = 2, sticky=tk.N + tk.S + tk.W + tk.W, ipadx = 2)
        return mole_frame, status_frame

    def create_moles(self):
        mole_buttons = []
        for r in range(WhackAMole.NUM_MOLE_ACROSS):
            row_of_buttons = []
            for c in range (WhackAMole.NUM_MOLE_ACROSS):
                mole_button = tk.Button(self.mole_frame, image = self.mole_photo)
                mole_button.grid(row = r, column = c, padx = 8, pady = 8)

                row_of_buttons.append(mole_button) # add the mole to the list

            mole_buttons.append(row_of_buttons) # add the row of moles into the total

        return mole_buttons 

    def create_status_widgets(self):
        spacer = tk.Label(self.status_frame, text = "", bg = WhackAMole.STATUS_BACKGROUND)
        spacer.pack(side = "top", fill = tk.Y, expand = True)

        hit_label = tk.Label(self.status_frame, text = "Number of Hits:", bg = WhackAMole.STATUS_BACKGROUND)
        hit_label.pack(side = "top", fill = tk.Y, expand = True)
 
        hit_counter = tk.Label(self.status_frame, text = "0", bg = WhackAMole.STATUS_BACKGROUND)
        hit_counter.pack(side = "top", fill = tk.Y, expand = True)

        spacer = tk.Label(self.status_frame, text = "", bg = WhackAMole.STATUS_BACKGROUND)
        spacer.pack(side = "top", fill = tk.Y, expand = True)

        miss_label = tk.Label(self.status_frame, text = "Number of Misses:", bg = WhackAMole.STATUS_BACKGROUND)
        miss_label.pack(side = "top", fill = tk.Y, expand = True)

        miss_counter = tk.Label(self.status_frame, text = "0", bg = WhackAMole.STATUS_BACKGROUND)
        miss_counter.pack(side = "top", fill = tk.Y, expand = True)

        spacer = tk.Label(self.status_frame, text="", bg=WhackAMole.STATUS_BACKGROUND)
        spacer.pack(side="top", fill=tk.Y, expand=True)

        start_button = tk.Button(self.status_frame, text="Start", bg = "peachpuff")
        start_button.pack(side="top", fill=tk.Y, expand=True, ipadx=10)

        spacer = tk.Label(self.status_frame, text="", bg=WhackAMole.STATUS_BACKGROUND)
        spacer.pack(side="top", fill=tk.Y, expand=True) # create distance between labels

        quit_button = tk.Button(self.status_frame, text="Quit", bg = "peachpuff")
        quit_button.pack(side="top", fill=tk.Y, expand=True, ipadx=10)

        spacer = tk.Label(self.status_frame, text="", bg=WhackAMole.STATUS_BACKGROUND)
        spacer.pack(side="top", fill=tk.Y, expand=True)
        
        return hit_counter, miss_counter, start_button, quit_button

    def set_callbacks(self):

        # set the same callback for each mole button
        for r in range(WhackAMole.NUM_MOLE_ACROSS):
            for c in range(WhackAMole.NUM_MOLE_ACROSS):
                self.mole_labels[r][c].bind("<ButtonPress-1>",self.mole_hit)

        self.start_button["command"] = self.start
        self.quit_button["command"] = self.quit

    def mole_hit(self,event):
        
        if self.game_is_running:
            hit_label = event.widget
            if hit_label["image"] == self.mole_cover_photo.name: # check whether the mole has been covered
                #Missed -> update the miss counter
                self.miss_counter["text"] = str(int(self.miss_counter["text"]) + 1)
                print("Missed.")
            
            else:
                #Hit -> update the hit counter
                self.hit_counter["text"] = str(int(self.hit_counter["text"]) + 1)
                #Remove the mole and don't upload the miss counter
                self.put_down_mole(hit_label, False)
                print("Hit")
            

    def start(self):
        
        if self.start_button["text"] == "Start":
            #Change all the mole images to a blank image
            #A random time for the moles to re-appear on each label
            for r in range(WhackAMole.NUM_MOLE_ACROSS):
                for c in range(WhackAMole.NUM_MOLE_ACROSS):
                    the_label = self.mole_labels[r][c]
                    the_label["image"] = self.mole_cover_photo
                    time_down = random.randrange(WhackAMole.MIN_TIME_DOWN, WhackAMole.MAX_TIME_DOWN)
                    timer_object = the_label.after(time_down, self.pop_up_mole, the_label)
                    self.label_timers[id(the_label)] = timer_object

            
            self.game_is_running = True
            self.start_button["text"] = "Stop"

            self.hit_counter["text"] == "0"
            self.miss_counter["text"] == "0"
        
        else:
            for r in range(WhackAMole.NUM_MOLE_ACROSS):
                for c in range(WhackAMole.NUM_MOLE_ACROSS):
                    self.mole_labels[r][c]["image"] = self.mole_photo
                    self.mole_labels[r][c].after_cancel(self.label_timers[id(self.mole_labels[r][c])])

            self.game_is_running = False
            self.start_button["text"] = "Start"


    def put_down_mole(self,the_label, timer_expired):

        if self.game_is_running:
            if timer_expired:
                #User can't click the mole on time -> update the miss counter
                self.miss_counter["text"] = str(int(self.miss_counter['text']) + 1)
            else:
                #The timer not expire, manually stop the timer
                the_label.after_cancel(self.label_timers[id(the_label)])

        #Make the mole invisible
        the_label["image"] = self.mole_cover_photo

        #call to pop up the mole in the future
        time_down = random.randrange(WhackAMole.MIN_TIME_DOWN,WhackAMole.MAX_TIME_DOWN)
        timer_object = the_label.after(time_down,self.pop_up_mole,the_label)

        #Remember the timer object so it can be canceled later
        self.label_timers[id(the_label)] = timer_object
    
    def pop_up_mole(self, the_label):
        #show mole on the screen
        the_label["image"] = self.mole_photo

        if self.game_is_running:
            #a call to make the mole disappear in the future
            timer_up = random.randrange(WhackAMole.MIN_TIME_UP,WhackAMole.MAX_TIME_UP)
            timer_object = the_label.after(timer_up, self.put_down_mole, the_label, True)
            self.label_timers[id(the_label)] = timer_object

    def quit(self):
        question = messagebox.askyesno("Quitting?","Do you want to quit?")
        if question:
            self.window.destroy()


        

if __name__ == "__main__":
    main()