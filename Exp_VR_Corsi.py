import tkinter, time, ast, pyautogui #TKinter - GUI, PyAutoGui - Mouse Control
from tkinter import Button #Button config for Mac (replace w/ tkinter if using Windows)
import tkinter.font
from HelperFunctions import * #Sequence generating functions
from functools import partial #Creates partial inputs of the same defintion w/ different inputs
from threading import Timer #Timer to set time limit and display squares/ numbers
import speech_recognition as sr #Speech recogntion for number input
from PIL import Image, ImageTk, ImageOps

""" Constants for the program defined """
HEIGHT = 800 #APP Window Height
WIDTH = 1050 #APP Window Width
SQUARES = ROWS * COLUMNS #Total squares (ROWS and COLUMNS defined HelperFunctions)
LEVELLIMITS = {1:16, 2:9, 3:24, 4:25} #Specific limits for each sequence for a 5x5 grid (manual calculations)
VRDIS = 274-22
VRSIZE = 1
BEGINHDIS = 30

""" Intiates TK Window """
main = tkinter.Tk() #Main TK window for application
main.geometry(str(main.winfo_screenwidth()) + "x" + str(main.winfo_screenheight())) #Main set to computer screen size
main.configure(bg = "#000000") #Colors the main window gray
root = tkinter.Canvas(main, height = HEIGHT, width = WIDTH, background = "#000000", highlightthickness = 0) #Creates window for the APP that has a gray background with specificed height and width above
root.place(x = (main.winfo_screenwidth() / 2) - (WIDTH / 2), y = (main.winfo_screenheight() / 2) - HEIGHT/2) #Places APP in the middle of the main screen

""" Importing Calibration Image """

#img = Image.open(r"C:\Users\HP\GitHub\CorsiTest\NewDesign\checkerboard.jpg")

"""
tkimage = ImageTk.PhotoImage(img)
CalImg1 = tkinter.Label(root, image=tkimage)
CalImg1.image = tkimage
CalImg2 = tkinter.Label(root, image=tkimage)
CalImg2.image = tkimage
"""
CalImg2 = tkinter.Canvas(root, bg="white", highlightthickness=5, highlightbackground="red")

CalImg1 = tkinter.Canvas(root, bg="white", highlightthickness=5, highlightbackground="blue")
""" Importing Calibration-Size Image """

#img_size = Image.open(r"C:\Users\HP\GitHub\CorsiTest\NewDesign\circle2-outlineCrop.png")
img_size = Image.open("circle2-outlineCrop.png")
img_size = img_size.resize((int(252/2),504))
save_img_size = img_size
tkimage = ImageTk.PhotoImage(img_size)
CalImg3 = tkinter.Label(root, image=tkimage)
CalImg3.image = tkimage
CalImg4 = tkinter.Label(root, image=tkimage)
CalImg4.image = tkimage

""" Initates integer TKinter variables """
sequence = tkinter.StringVar() #Current sequence
copy_sequence = tkinter.StringVar() #Copy of sequence for display/ editing
user_response = tkinter.StringVar() #Response of the user during answering
trial_data = tkinter.StringVar() #Trail data for specific object, task, and sequence
time_cons_var = tkinter.StringVar() #Time constant for the trial set by user

result = tkinter.IntVar() #Result of trial (0 = Failure, 1 = Success)
task_level = tkinter.IntVar() #Sequence type (1-4 : specified in HelperFunctions)
objects = tkinter.IntVar() #Number of objects
tasks_objects = []
highest_object = 5
lowest_object = 5
task_type = tkinter.IntVar() #Current task (1-5)
completed_trials = tkinter.IntVar() #Number of completed trial for a task
NumObjectRef = tkinter.IntVar() #Temp variable for recording TK object reference
NumObjectRef.set(0) 

""" Variables for data collection """
patient_id = tkinter.StringVar() #Patient ID
LastTime = tkinter.IntVar() #Time of last button click
TrialNumber = tkinter.IntVar() #Current trial number
TrialSequence = [] #The sequence at which the trials will be presented (list containing 1-4 only)
AliveTrials = [] #Sequnce types that have not ended for the task
UserSequence = {} #User response of current trial (+ values for additions to response and - values for removal)
CompleteData = {} #All the data of the current task

""" Set recorder for speech recognition """
Recorder = sr.Recognizer()
Recorder.pause_threshold = 1.5 #Time which the user stops talking before phrase is marked as done


task_order = [1,6,3,5,4,2]

#task_order =[3,5,2,1,4]
#random.shuffle(task_order)

""" Wipes grid by setting all squares to white """
def ClearGrid():
   global SQUARES
   for square in range(1, SQUARES + 1):
      exec("sq" + str(square) + ".config(bg = 'black', text = '')")
      exec("sq" + str(square) + "_2.config(bg = 'black', text = '')")

""" Takes button click and updates grid + user response """
def ButtonClick(button_num):
   global LimitTimer, UserSequence
   clicktime = time.time_ns()
   seq = user_response.get()
   seq = list(ast.literal_eval(seq))
   if LimitTimer.is_alive():
      LimitTimer.cancel()
      og_seq = sequence.get()
      og_seq = list(ast.literal_eval(og_seq))
      for item in og_seq:
         if task_type.get() != 5:
            exec("sq" + str(item) + ".config(bg = 'white', text = '')" )
            exec("sq" + str(item) + "_2.config(bg = 'white', text = '')" )
         else:
            exec("sq" + str(item) + ".config(bg = 'black', text = '')" )
            exec("sq" + str(item) + "_2.config(bg = 'black', text = '')" )
   if str(button_num) not in seq:
      #exec("sq" + str(button_num) + ".config(bg = 'black')")
      seq.append(str(button_num))
      UserSequence.update({button_num: clicktime - LastTime.get()})
      LastTime.set(clicktime)
   else:
      #exec("sq" + str(button_num) + ".config(bg = 'black')")
      seq.remove(str(button_num))
      UserSequence.update({button_num*-1: clicktime - LastTime.get()})
      LastTime.set(clicktime)
      if len(seq) == 0:
         seq.append("")

   user_response.set(seq)

""" 
Intiates all of the partial functions - pairs square with respective number 
36 buttons intiated to allow for up to 6x6 grid
"""
Sq1 = partial(ButtonClick, 1)
Sq2 = partial(ButtonClick, 2)
Sq3 = partial(ButtonClick, 3)
Sq4 = partial(ButtonClick, 4)
Sq5 = partial(ButtonClick, 5)
Sq6 = partial(ButtonClick, 6)
Sq7 = partial(ButtonClick, 7)
Sq8 = partial(ButtonClick, 8)
Sq9 = partial(ButtonClick, 9)
Sq10 = partial(ButtonClick, 10)
Sq11 = partial(ButtonClick, 11)
Sq12 = partial(ButtonClick, 12)
Sq13 = partial(ButtonClick, 13)
Sq14 = partial(ButtonClick, 14)
Sq15 = partial(ButtonClick, 15)
Sq16 = partial(ButtonClick, 16)
Sq17 = partial(ButtonClick, 17)
Sq18 = partial(ButtonClick, 18)
Sq19 = partial(ButtonClick, 19)
Sq20 = partial(ButtonClick, 20)
Sq21 = partial(ButtonClick, 21)
Sq22 = partial(ButtonClick, 22)
Sq23 = partial(ButtonClick, 23)
Sq24 = partial(ButtonClick, 24)
Sq25 = partial(ButtonClick, 25)
Sq26 = partial(ButtonClick, 26)
Sq27 = partial(ButtonClick, 27)
Sq28 = partial(ButtonClick, 28)
Sq29 = partial(ButtonClick, 29)
Sq30 = partial(ButtonClick, 30)
Sq31 = partial(ButtonClick, 31)
Sq32 = partial(ButtonClick, 32)
Sq33 = partial(ButtonClick, 33)
Sq34 = partial(ButtonClick, 34)
Sq35 = partial(ButtonClick, 35)
Sq36 = partial(ButtonClick, 36)

""" Intializes grid buttons """
sqFont = tkinter.font.Font( family = "Calibri", size = 20, weight = "bold")
sq1 = Button(root, command=Sq1, anchor="center", bg='black', font = sqFont)
sq2 = Button(root, command=Sq2, anchor="center", bg='black', font = sqFont)
sq3 = Button(root, command=Sq3, anchor="center", bg='black', font = sqFont)
sq4 = Button(root, command=Sq4, anchor="center", bg='black', font = sqFont)
sq5 = Button(root, command=Sq5, anchor="center", bg='black', font = sqFont)
sq6 = Button(root, command=Sq6, anchor="center", bg='black', font = sqFont)
sq7 = Button(root, command=Sq7, anchor="center", bg='black', font = sqFont)
sq8 = Button(root, command=Sq8, anchor="center", bg='black', font = sqFont)
sq9 = Button(root, command=Sq9, anchor="center", bg='black', font = sqFont)
sq10 = Button(root, command=Sq10, anchor="center", bg='black', font = sqFont)
sq11 = Button(root, command=Sq11, anchor="center", bg='black', font = sqFont)
sq12 = Button(root, command=Sq12, anchor="center", bg='black', font = sqFont)
sq13 = Button(root, command=Sq13, anchor="center", bg='black', font = sqFont)
sq14 = Button(root, command=Sq14, anchor="center", bg='black', font = sqFont)
sq15 = Button(root, command=Sq15, anchor="center", bg='black', font = sqFont)
sq16 = Button(root, command=Sq16, anchor="center", bg='black', font = sqFont)
sq17 = Button(root, command=Sq17, anchor="center", bg='black', font = sqFont)
sq18 = Button(root, command=Sq18, anchor="center", bg='black', font = sqFont)
sq19 = Button(root, command=Sq19, anchor="center", bg='black', font = sqFont)
sq20 = Button(root, command=Sq20, anchor="center", bg='black', font = sqFont)
sq21 = Button(root, command=Sq21, anchor="center", bg='black', font = sqFont)
sq22 = Button(root, command=Sq22, anchor="center", bg='black', font = sqFont)
sq23 = Button(root, command=Sq23, anchor="center", bg='black', font = sqFont)
sq24 = Button(root, command=Sq24, anchor="center", bg='black', font = sqFont)
sq25 = Button(root, command=Sq25, anchor="center", bg='black', font = sqFont)
sq26 = Button(root, command=Sq26, anchor="center", bg='black', font = sqFont)
sq27 = Button(root, command=Sq27, anchor="center", bg='black', font = sqFont)
sq28 = Button(root, command=Sq28, anchor="center", bg='black', font = sqFont)
sq29 = Button(root, command=Sq29, anchor="center", bg='black', font = sqFont)
sq30 = Button(root, command=Sq30, anchor="center", bg='black', font = sqFont)
sq31 = Button(root, command=Sq31, anchor="center", bg='black', font = sqFont)
sq32 = Button(root, command=Sq32, anchor="center", bg='black', font = sqFont)
sq33 = Button(root, command=Sq33, anchor="center", bg='black', font = sqFont)
sq34 = Button(root, command=Sq34, anchor="center", bg='black', font = sqFont)
sq35 = Button(root, command=Sq35, anchor="center", bg='black', font = sqFont)
sq36 = Button(root, command=Sq36, anchor="center", bg='black', font = sqFont)

sq1_2 = Button(root, command=Sq1, anchor="center", bg='black', font = sqFont)
sq2_2 = Button(root, command=Sq2, anchor="center", bg='black', font = sqFont)
sq3_2 = Button(root, command=Sq3, anchor="center", bg='black', font = sqFont)
sq4_2 = Button(root, command=Sq4, anchor="center", bg='black', font = sqFont)
sq5_2 = Button(root, command=Sq5, anchor="center", bg='black', font = sqFont)
sq6_2 = Button(root, command=Sq6, anchor="center", bg='black', font = sqFont)
sq7_2 = Button(root, command=Sq7, anchor="center", bg='black', font = sqFont)
sq8_2 = Button(root, command=Sq8, anchor="center", bg='black', font = sqFont)
sq9_2 = Button(root, command=Sq9, anchor="center", bg='black', font = sqFont)
sq10_2 = Button(root, command=Sq10, anchor="center", bg='black', font = sqFont)
sq11_2 = Button(root, command=Sq11, anchor="center", bg='black', font = sqFont)
sq12_2 = Button(root, command=Sq12, anchor="center", bg='black', font = sqFont)
sq13_2 = Button(root, command=Sq13, anchor="center", bg='black', font = sqFont)
sq14_2 = Button(root, command=Sq14, anchor="center", bg='black', font = sqFont)
sq15_2 = Button(root, command=Sq15, anchor="center", bg='black', font = sqFont)
sq16_2 = Button(root, command=Sq16, anchor="center", bg='black', font = sqFont)
sq17_2 = Button(root, command=Sq17, anchor="center", bg='black', font = sqFont)
sq18_2 = Button(root, command=Sq18, anchor="center", bg='black', font = sqFont)
sq19_2 = Button(root, command=Sq19, anchor="center", bg='black', font = sqFont)
sq20_2 = Button(root, command=Sq20, anchor="center", bg='black', font = sqFont)
sq21_2 = Button(root, command=Sq21, anchor="center", bg='black', font = sqFont)
sq22_2 = Button(root, command=Sq22, anchor="center", bg='black', font = sqFont)
sq23_2 = Button(root, command=Sq23, anchor="center", bg='black', font = sqFont)
sq24_2 = Button(root, command=Sq24, anchor="center", bg='black', font = sqFont)
sq25_2 = Button(root, command=Sq25, anchor="center", bg='black', font = sqFont)
sq26_2 = Button(root, command=Sq26, anchor="center", bg='black', font = sqFont)
sq27_2 = Button(root, command=Sq27, anchor="center", bg='black', font = sqFont)
sq28_2 = Button(root, command=Sq28, anchor="center", bg='black', font = sqFont)
sq29_2 = Button(root, command=Sq29, anchor="center", bg='black', font = sqFont)
sq30_2 = Button(root, command=Sq30, anchor="center", bg='black', font = sqFont)
sq31_2 = Button(root, command=Sq31, anchor="center", bg='black', font = sqFont)
sq32_2 = Button(root, command=Sq32, anchor="center", bg='black', font = sqFont)
sq33_2 = Button(root, command=Sq33, anchor="center", bg='black', font = sqFont)
sq34_2 = Button(root, command=Sq34, anchor="center", bg='black', font = sqFont)
sq35_2 = Button(root, command=Sq35, anchor="center", bg='black', font = sqFont)
sq36_2 = Button(root, command=Sq36, anchor="center", bg='black', font = sqFont)

""" Threshold determination function """
def TaskPass():
   global UserSequence, SQUARES, TrialSequence, AliveTrials, LEVELLIMITS, tasks_objects, highest_object, lowest_object
   
   completed_trials.set(completed_trials.get() + 1)
   finished = False
   record_seq = sequence.get()
   record_seq = tuple(ast.literal_eval(record_seq))
   if task_type.get() == 1:
      CompleteData.update({(task_type.get(), objects.get(), task_level.get(), result.get(), TrialNumber.get()):{record_seq: ast.literal_eval(str(UserSequence))}})
   else:
      CompleteData.update({(task_type.get(), tasks_objects[task_level.get() - 1], task_level.get(), result.get(), TrialNumber.get()):{record_seq: ast.literal_eval(str(UserSequence))}})
   data = ast.literal_eval(trial_data.get())
   if task_type.get() == 1:
      if result.get() == 2:
         finished = True
      elif result.get() == 1:
         objects.set(objects.get() + 1)
      elif result.get() == 0:
         data[objects.get()][0][0] += 1
         if data[objects.get()][0][0] > 1:
            finished = True
         objects.set(objects.get() - 1)
      try:
         data[objects.get()]
      except Exception:
         data[objects.get()] = [[0,0],[0,0],[0,0],[0,0]]
   else:
      data[tasks_objects[task_level.get() - 1]][task_level.get() - 1][1] += 1
      if result.get() == 1:
         data[tasks_objects[task_level.get() - 1]][task_level.get() - 1][0] += 1
         if data[tasks_objects[task_level.get() - 1]][task_level.get() - 1][0] == 1 and tasks_objects[task_level.get() - 1] < LEVELLIMITS[task_level.get()] and tasks_objects[task_level.get() - 1] >= 5:
            TrialSequence = [value for value in TrialSequence if value != task_level.get()]
            AliveTrials.append(task_level.get())
         if tasks_objects[task_level.get() - 1] < 5:
            TrialSequence = [value for value in TrialSequence if value != task_level.get()]
      elif result.get() == 2:
         finished = True
      if len(TrialSequence) == 0:
         if task_type.get() != 1:
            for i in range (0,4):
               if data[tasks_objects[i]][i][0] == 0 and tasks_objects[i] <= 5 and tasks_objects[i] >= 1:
                  tasks_objects[i] -= 1
                  if lowest_object > tasks_objects[i]:
                     lowest_object -= 1
                     data[lowest_object] = [[0,0],[0,0],[0,0],[0,0]]
                  AliveTrials.append(i + 1)
               elif data[tasks_objects[i]][i][0] >= 1 and tasks_objects[i] >= 5:
                  tasks_objects[i] += 1
                  if tasks_objects[i] > highest_object:
                     highest_object = tasks_objects[i]
                     data[highest_object] = [[0,0],[0,0],[0,0],[0,0]]
         if len(AliveTrials) > 0:
            RandTrialOrder()
            task_level.set(TrialSequence[0])
            TrialSequence.pop(0)
            if task_type == 1:
               objects.set(objects.get() + 1)
               data[objects.get()] = [[0,0],[0,0],[0,0],[0,0]]
            
         else:
            finished = True
      else:
         task_level.set(TrialSequence[0])
         if len(TrialSequence) != 0:
            TrialSequence.pop(0)
            
   trial_data.set(data)
   UserSequence.clear()
   if finished == False:
      TrialNumber.set(TrialNumber.get() + 1)
      submitbutton.place_forget()
      submitbutton2.place_forget()
      if task_type.get() == 1:
         sequence.set(simple_random_num_set_gen(objects.get()))
         HideNums()
      else:
         ClearGrid()
         seq = random_sequence_gen(tasks_objects[task_level.get() - 1], SQUARES, task_level.get())
         while (0 in seq):
            seq = random_sequence_gen(tasks_objects[task_level.get() - 1], SQUARES, task_level.get())
         sequence.set(seq)
      exec("Task" + str(task_type.get()) + "Main()")
      
   elif finished == True:
      try:
         print(CompleteData)
         with open(patient_id.get() + "_data.json", "a+") as outfile:
            outfile.write(str(CompleteData) + '\n')
            CompleteData.clear()
         outfile.close()
      except Exception:
         print(CompleteData)
         with open(patient_id.get() + "_data.json", "w") as outfile:
            outfile.write(str(CompleteData) + '\n')
            CompleteData.clear()
         outfile.close()
      submitbutton.place_forget()
      submitbutton2.place_forget()
      if task_type.get() == 1:
         HideNums()
      else:
         ClearGrid()
         HideGrid()
      time_cons_var.set("")
      task_order.pop(0)
      instruct_text.config(text = ChooseText(task_order[0]))
      instruct_text2.config(text = ChooseText(task_order[0]))
      instruct_text.place(x = WIDTH / 2 - 100 - VRDIS, y = HEIGHT / 2 - 130, height = 200 , width = 200)
      instruct_text2.place(x = WIDTH / 2 - 100 +  VRDIS, y = HEIGHT / 2 - 130, height = 200 , width = 200)
      beginbutton.config(command = NextTask, text = "Begin Next Trial")
      beginbutton2.config(command = NextTask, text = "Begin Next Trial")
      beginbutton.place(x = WIDTH / 2 - 100 - VRDIS, y = HEIGHT / 2 + 70, width = 200, height = 60)
      beginbutton2.place(x = WIDTH / 2 - 100 + VRDIS, y = HEIGHT / 2 + 70, width = 200, height = 60)

""" Checks if the user response matches the sequence """
def CheckSequence():
   global LimitTimer
   if LimitTimer.is_alive():
      LimitTimer.cancel()
   result.set(1)
   seq = sequence.get()
   seq = list(ast.literal_eval(seq))
   ans = user_response.get()
   ans = list(ast.literal_eval(ans))
   if "" in ans:
      ans.remove("")
   if task_type.get() == 2 or task_type.get() == 5:
      if len(ans) != len(seq):
         result.set(0)
      if result.get() == 1:
         for vals in range(0, len(ans)):
            if int(ans[vals]) not in seq:
               result.set(0)
   else:
      if len(seq) != len(ans):
         result.set(0)
      if result.get() == 1:
         for vals in range(0, len(ans)):
            if int(ans[vals]) != seq[vals]:
               result.set(0)
   TaskPass()

""" Activates grid for clicking """
def ActivateGrid():
   global SQUARES
   for square in range(1,SQUARES + 1):
      code = "sq" + str(square) + ".config(command = Sq" + str(square) + ")" + "\nsq" + str(square) + "_2.config(command = Sq" + str(square) + ")"
      exec(code)

""" Displays square on the screen w/ number if applicable """
def AddSquare():
   seq = sequence.get()
   seq = list(ast.literal_eval(seq))
   cpy_seq = copy_sequence.get()
   cpy_seq = list(ast.literal_eval(cpy_seq))
   counter = ""
   if task_type.get() == 4:
      counter = str(len(seq) - len(cpy_seq) + 1)
   code = "sq" + str(cpy_seq[0]) + ".config(bg = 'white', text = '" + counter + "')\nsq" + str(cpy_seq[0]) + "_2.config(bg = 'white', text = '" + counter + "')"  
   exec(code)

""" Removes square from display along with number after showing """
def RemoveSquare():
   seq = copy_sequence.get()
   seq = list(ast.literal_eval(seq))
   code = "sq" + str(seq[0]) + ".config(bg = 'black', text = '')" + "\nsq" + str(seq[0]) + "_2.config(bg = 'black', text = '')"
   seq.pop(0)
   if len(seq) == 0:
      submitbutton.place(x = int(root['width']) / 2 - int(50*VRSIZE*0.864) - VRDIS, y = HEIGHT/2 - 40*2.5*VRSIZE*0.864 - 20*2*VRSIZE*0.864 - 15*VRSIZE*0.864 - 50*VRSIZE*0.864, width = 100*VRSIZE*0.864, height = 50*VRSIZE*0.864)
      submitbutton2.place(x = int(root['width']) / 2 - int(50*VRSIZE*0.864) + VRDIS, y = HEIGHT/2 - 40*2.5*VRSIZE*0.864 - 20*2*VRSIZE*0.864 - 15*VRSIZE*0.864 - 50*VRSIZE*0.864, width = 100*VRSIZE*0.864, height = 50*VRSIZE*0.864)
   copy_sequence.set(seq)
   exec(code)

""" Moves mouse to specified location """
def MoveMouse():
   global VRDIS
   pyautogui.moveTo(main.winfo_screenwidth()/2 - VRDIS, (main.winfo_screenheight()/2), duration = 0)

def ShowMouse():
   main.config(cursor="arrow")

def tksleep(t):
    'emulating time.sleep(seconds)'
    ms = int(t*1000)
    sle = tkinter._get_default_root('sleep')
    var = tkinter.IntVar(sle)
    sle.after(ms, var.set, 1)
    sle.wait_variable(var)

""" Shows flashing sequence w/ the specified time delay """
def ShowSequence():
   main.config(cursor="none")
   beginbutton.place_forget()
   beginbutton2.place_forget()
   seq = sequence.get()
   seq = ast.literal_eval(seq)
   
   for item in seq:
      AddSquare()
      tksleep(1)
      RemoveSquare()
   MoveMouse()
   ActivateGrid()
   ShowMouse()
   LastTime.set(time.time_ns())

""" Removes square grid from screen """
def HideGrid():
   global SQUARES
   for square in range(1, SQUARES + 1):
      code = "sq" + str(square) + ".place_forget()\nsq" + str(square) +"_2.place_forget()"
      exec(code)

""" Initalizes the submit and start buttons """
submitbutton = Button(root, text = "Submit", command = CheckSequence, font = ("calibri " + str(int(20*VRSIZE)) + " normal"), bg = "#38ff38")
submitbutton2 = Button(root, text = "Submit", command = CheckSequence, font = ("calibri " + str(int(20*VRSIZE)) + " normal"), bg = "#38ff38")

def NextTask():
    global task_order
    beginbutton.config(command = ShowSequence, text = "Start")
    beginbutton2.config(command = ShowSequence, text = "Start")
    beginbutton.place_forget()
    beginbutton2.place_forget()
    instruct_text.place_forget()
    instruct_text2.place_forget()
    MainFlow(task_order[0])

def makeFit(text):
   string = text.split()
   newtext = ""
   counter = 0 
   for item in string:
      counter = counter + len(item)
      if counter > 30 or item == "*":
         newtext += "\n" 
         counter = 0
      newtext += item + " "
   return newtext
      

def ChooseText(task):
   if task == 1:
      return "Number Task: \n* A sequence of #s will appear on the screen. \n* Remember the #s in the shown sequence. \n* After all numbers are shown, a box will appear. \n* Wait for the box to say 'Listening' \n* Verbalize the sequence in the order shown. \n* Compare your response with the numbers on the screen. \n* Inform the examiner of any discrepancies."
   if task == 2:
      return "Flashing Visuospatial (Unordered): \n* Squares appear on a grid one after another. \n* Remember the locations where squares light up. \n* When the green button appears, click the squares in ANY order. \n* After selecting all squares, hit the submit button. \n* To remove a wrongly selected square, click it again."
   if task == 3:
      return "Flashing Visuospatial (O): \n* Squares appear on a grid one after another. \n* Remember the locations where squares light up. \n* When the green button appears, click the squares in the EXACT order you saw. \n* After selecting all squares, hit the submit button. \n* To remove a wrongly selected square, click it again."
   if task == 4:
      return "Flashing Visuospatial (O,N): \n* Squares appear on a grid one after another. \n* Each square contains a number indicating its order. \n* Remember the locations where squares light up (turn white). \n* When the green button appears, click the squares in the EXACT order you saw. \n* After selecting all squares, remember to hit the submit button. \n* Click a square again to remove it."
   if task == 5:
      return "Sustained Visuospatial: \n* All squares appear on a grid at the same time. \n* Take time to memorize the shown squares within the time limit or start clicking on the lit squares as soon as they appear. \n* Once you click one square or the time limit is reached, the rest will disappear. \n* Hit submit after selecting all the squares you wish to. \n* To remove a wrongly selected square, click it again."
   if task == 6:
      return "Sustained Visuospatial Order: \n* Squares and #s appear together on a grid. \n* #s disappear after a set time. \n* Your task is to click the squares in the specified order indicated by the numbers. \n* Take time to memorize or respond immediately. \n* Clicking one square removes all numbers. \n* After selecting all squares, please click the submit button."

def ShowInstructs():
   global VRSIZE, VRVERT, VRHOZ
   VRSIZE = VRSIZE * int(verScale.get()) / 100 
   instruct_text.place(x = WIDTH / 2 - 100 - VRDIS, y = HEIGHT / 2 - 130, height = 200 , width = 200)
   instruct_text2.place(x = WIDTH / 2 - 100 +  VRDIS, y = HEIGHT / 2 - 130, height = 200 , width = 200)
   CalImg3.place_forget()
   CalImg4.place_forget()
   verScale.place_forget()
   verScale2.place_forget()
   #upbutton2.place_forget()
   #downbutton2.place_forget()
   #leftbutton2.place_forget()
   #rightbutton2.place_forget()
   submitbutton.config(font = ("calibri " + str(int(20*VRSIZE)) + " bold"))
   submitbutton2.config(font = ("calibri " + str(int(20*VRSIZE)) + " bold"))
   beginbutton.config(command = NextTask, text = "Begin Test")
   beginbutton2.config(command = NextTask, text = "Begin Test")
   beginbutton.place(x = WIDTH / 2 - int(100*VRSIZE) - VRDIS, y = HEIGHT / 2 + int(70*VRSIZE), width = int(200*VRSIZE), height = int(60*VRSIZE))
   beginbutton2.place(x = WIDTH / 2 - int(100*VRSIZE) + VRDIS, y = HEIGHT / 2 + int(70*VRSIZE), width = int(200*VRSIZE), height = int(60*VRSIZE))

VRVERT = 0
VRHOZ = 0

def VRAdjustment(option):
   global VRVERT, VRHOZ, VRSIZE
   root.delete(NumObjectRef.get())
   #root.delete(NumObjectRef.get() + 1)
   if option == 1:
      VRVERT -= 1
   elif option == 2:
      VRVERT += 1
   elif option == 3:
      VRHOZ -= 1
   elif option == 4:
      VRHOZ += 1
   NumObjectRef.set(root.create_text(int(root['width'])/2 - VRDIS + VRHOZ, int(root['height'])/2 + VRVERT, anchor = 'center', text = "+", fill = "white", font = ('calibri ' + str(int(30*VRSIZE)) + ' bold')))
   #root.create_text(root.winfo_width()/2 + VRDIS + VRHOZ, root.winfo_height()/2 + VRVERT, anchor = 'center', text = "+", fill = "white", font = ('calibri ' + str(int(30*VRSIZE)) + ' bold'))

up = partial(VRAdjustment,1)
down = partial(VRAdjustment,2)
left = partial(VRAdjustment,3)
right = partial(VRAdjustment,4)

upbutton = Button(root, text = "UP", font = ('calibri 20 bold'), command = up)
downbutton = Button(root, text = "DOWN", font = ('calibri 13 bold'), command = down)
leftbutton = Button(root, text = "<-", font = ('calibri 20 bold'), command = left)
rightbutton = Button(root, text = "->", font = ('calibri 20 bold'), command = right)

upbutton2 = Button(root, text = "UP", font = ('calibri 20 bold'), command = up)
downbutton2 = Button(root, text = "DOWN", font = ('calibri 13 bold'), command = down)
leftbutton2 = Button(root, text = "<-", font = ('calibri 20 bold'), command = left)
rightbutton2 = Button(root, text = "->", font = ('calibri 20 bold'), command = right)

def VRHeightSet():
   global VRSIZE
   NumObjectRef.set(root.create_text(root.winfo_width()/2 - VRDIS, root.winfo_height()/2, anchor = 'center', text = "+", fill = "white", font = ('calibri ' + str(int(30*VRSIZE)) + ' bold')))
   #root.create_text(root.winfo_width()/2 + VRDIS, root.winfo_height()/2, anchor = 'center', text = "+", fill = "white", font = ('calibri ' + str(int(30*VRSIZE)) + ' bold'))
   #upbutton2.place(x = root.winfo_width()/2 + VRDIS - 25 + 30, y = root.winfo_height()/2 + 50, width = 50, height = 50)
   #downbutton2.place(x = root.winfo_width()/2 + VRDIS - 25 + 30, y = root.winfo_height()/2 + 100, width = 50, height = 50)
   #leftbutton2.place(x = root.winfo_width()/2 + VRDIS - 75 + 30, y = root.winfo_height()/2 + 75, width = 50, height = 50)
   #rightbutton2.place(x = root.winfo_width()/2 + VRDIS + 25 + 30, y = root.winfo_height()/2 + 75, width = 50, height = 50)
   upbutton.place(x = root.winfo_width()/2 - VRDIS - 25 + 30, y = root.winfo_height()/2 + 50, width = 50, height = 50)
   downbutton.place(x = root.winfo_width()/2 - VRDIS - 25 + 30, y = root.winfo_height()/2 + 100, width = 50, height = 50)
   leftbutton.place(x = root.winfo_width()/2 - VRDIS - 75 + 30, y = root.winfo_height()/2 + 75, width = 50, height = 50)
   rightbutton.place(x = root.winfo_width()/2 - VRDIS + 25 + 30, y = root.winfo_height()/2 + 75, width = 50, height = 50)
   beginbutton.place(x = root.winfo_width()/2 - VRDIS - 45 - 50 - 5, y = root.winfo_height()/2 + 75, width = 50, height = 50)
   beginbutton.config(font = ('calibri 15 bold'))
   #beginbutton2.place(x = root.winfo_width()/2 + VRDIS - 45 - 50 - 5, y = root.winfo_height()/2 + 75, width = 50, height = 50)
   beginbutton2.config(font = ('calibri 15 bold'))

def updateSizeImage(scale):
   global CalImg3, CalImg4,img_size, tkimage
   adjustsize = 1 * int(scale) / 100 
   print(adjustsize)
   if int(verScale.get()) == int(scale):
      verScale2.set(int(scale))
   else:
      verScale2.set(int(scale))
   CalImg3.place_forget()
   CalImg4.place_forget()
   img_size = save_img_size.resize((int(252/2*adjustsize),int(504*adjustsize)))
   tkimage = ImageTk.PhotoImage(img_size)
   CalImg3 = tkinter.Label(image=tkimage)
   CalImg3.image = tkimage
   CalImg4 = tkinter.Label(image=tkimage)
   CalImg4.image = tkimage
   CalImg3.place(x = (root.winfo_screenwidth() / 2 - img_size.size[0]) - VRDIS + VRHOZ, y= root.winfo_height() / 2 - img_size.size[1]/2 + VRVERT)
   CalImg4.place(x = (root.winfo_screenwidth() / 2 - img_size.size[0]) + VRDIS + VRHOZ, y = root.winfo_height() / 2 - img_size.size[1]/2 + VRVERT)  
   
verScale = tkinter.Scale(root, from_=0, to=200, orient=tkinter.VERTICAL, command = updateSizeImage)
verScale2 = tkinter.Scale(root, from_=0, to=200, orient=tkinter.VERTICAL, command = updateSizeImage)

def VRSizeSet():
   global VRSIZE, VRDIS
   CalImg1.place_forget()
   CalImg2.place_forget()
   hozScale.place_forget()
   VRDIS = VRDIS - int(hozScale.get()) + 100
   beginbutton.config(command = ShowInstructs)
   beginbutton2.config(command = ShowInstructs)
   pyautogui.moveTo(main.winfo_screenwidth()/2 - VRDIS, (main.winfo_screenheight()/2), duration = 0)
   verScale.set(100)
   verScale.place(x = WIDTH/2 - VRDIS, y = main.winfo_height() / 2 - 100)
   verScale2.set(100)
   verScale2.place(x = WIDTH/2 + VRDIS, y = main.winfo_height() / 2 - 100)
   beginbutton.place(x = WIDTH / 2 - VRDIS, y = main.winfo_height() / 2, width = 80, height = 80)
   beginbutton2.place(x = WIDTH / 2 + VRDIS, y = main.winfo_height() / 2, width = 80, height = 80)
   
def updateImage(dist):
   global VRDIS
   adjustdist = VRDIS - int(dist) + 75
   CalImg1.place_forget()
   CalImg2.place_forget()
   CalImg2.place(x = root.winfo_screenwidth() / 2 - 200 + 50 + adjustdist, y = root.winfo_height() / 2 - 50, width=100, height=100)  
   CalImg1.place(x = root.winfo_screenwidth() / 2 - 95 - 50 - adjustdist, y = root.winfo_height() / 2 - 95/2, width=90, height=90)
    

hozScale = tkinter.Scale(root, from_=0, to=150, orient=tkinter.HORIZONTAL, command = updateImage)

def VRDistSet():
   global VRDIS
   root.place(x = (main.winfo_screenwidth() / 2) - (WIDTH / 2) + VRHOZ, y = (main.winfo_screenheight() / 2) - (HEIGHT / 2) + VRVERT)
   root.delete(NumObjectRef.get())
   #root.delete(NumObjectRef.get() + 1)
   beginbutton.config(command = VRSizeSet)
   upbutton.place_forget()
   downbutton.place_forget()
   leftbutton.place_forget()
   rightbutton.place_forget()
   pyautogui.moveTo(main.winfo_screenwidth()/2 - VRDIS, (main.winfo_screenheight()/2), duration = 0)
   hozScale.set(75)
   hozScale.place(x = root.winfo_screenwidth() / 2 - img.size[0]  - VRDIS, y = HEIGHT/2 + 50 , width = img.size[0])
   beginbutton.place(x = root.winfo_screenwidth() / 2 - img.size[0] - VRDIS, y = root.winfo_height() / 2 - img.size[1]/2  , width = img.size[0], height = 50)

id_entry = tkinter.Entry(root, textvariable = patient_id, font = ('calibri 30 bold'), borderwidth = 4, justify = "center")
id_entry2 = tkinter.Entry(root, textvariable = patient_id, font = ('calibri 30 bold'), borderwidth = 4, justify = "center")

def IDCollect():
   id_entry.place_forget()
   id_entry2.place_forget()
   id_sub_btn.place_forget()
   id_sub_btn2.place_forget()
   VRHeightSet()
   
id_sub_btn = Button(root, text = 'Submit Patient ID', command = IDCollect, bg = "#535353", fg = "white", font = ('calibri 25 bold'))
id_sub_btn2 = Button(root, text = 'Submit Patient ID', command = IDCollect, bg = "#535353", fg = "white", font = ('calibri 25 bold'))

id_entry.place(x = int(root['width']) / 2 - 150 - VRDIS, y = int(root['height']) / 2 - 60, width = 300, height = 60)
id_entry2.place(x = int(root['width']) / 2 - 150 + VRDIS, y = int(root['height']) / 2 - 60, width = 300, height = 60)
id_sub_btn.place(x = int(root['width']) / 2 - 150 - VRDIS, y = int(root['height']) / 2, width = 301.5, height = 80)
id_sub_btn2.place(x = int(root['width']) / 2 - 150 + VRDIS, y = int(root['height']) / 2, width = 301.5, height = 80)


instruct_text = Button(root, font = ("calibri 9 bold"), wraplength = 190, text = ChooseText(task_order[0]), justify = "left")
instruct_text2 = Button(root, font = ("calibri 9 bold"), wraplength = 190, text = ChooseText(task_order[0]), justify = "left")

beginbutton = Button(root, text = "Done", command = VRDistSet, font = ("calibri 20 bold"))
beginbutton2 = Button(root, text = "Done", command = VRDistSet, font = ("calibri 20 bold"))

def RestartTask():
    beginbutton.config(command = ShowSequence, text = "Start")
    beginbutton2.config(command = ShowSequence, text = "Start")
    beginbutton.place_forget()
    beginbutton2.place_forget()
    
    instruct_text.place_forget()
    instruct_text2.place_forget()
    exec("Task" + str(task_type.get()) + "Trigger()")

""" Generates a random order of trials from the alive sequences """
def RandTrialOrder():
   global TrialSequence, AliveTrials
   for item in AliveTrials:
      TrialSequence.append(item)
      TrialSequence.append(item)
   AliveTrials.clear()
   random.shuffle(TrialSequence)
      
""" Intialization of the current task and its paramters """
def TaskFlow(task):
   global SQUARES, AliveTrials, TrialSequence, lowest_object, highest_object, tasks_objects
   end_trial = {}
   tasks_objects = [5,5,5,5]
   end_trial[5] = [[0,0],[0,0],[0,0],[0,0]]
   trial_data.set(end_trial)
   TrialNumber.set(0)
   objects.set(5)
   lowest_object = 5
   highest_object = 5
   beginbutton.configure(font = ('calibri ' + str(int(20*VRSIZE)) + ' bold'))
   beginbutton2.configure(font = ('calibri ' + str(int(20*VRSIZE)) + ' bold'))
   if task  == 1:   
      task_level.set(0)
   else:
      AliveTrials = [1,2,3,4]
      RandTrialOrder()
      task_level.set(TrialSequence[0])
      TrialSequence.pop(0)
   task_type.set(task)
   completed_trials.set(0)
   if task == 1:
      sequence.set(simple_random_num_set_gen(objects.get()))
   else:
      seq = random_sequence_gen(tasks_objects[task_level.get() - 1], SQUARES, task_level.get())
      while (0 in seq):
         seq = random_sequence_gen(tasks_objects[task_level.get() - 1], SQUARES, task_level.get())
      sequence.set(seq)
   #exitbutton.place(x = int(root["width"]) - 200, y = 10, width = 90, height = 40)
   exec("Task" + str(task_type.get()) + "Main()")

""" Shows entry box for the time constraint """
time_entry = tkinter.Entry(root, textvariable = time_cons_var, font = ('calibri 30 bold'), borderwidth = 4, justify = "center")
time_entry2 = tkinter.Entry(root, textvariable = time_cons_var, font = ('calibri 30 bold'), borderwidth = 4, justify = "center")

def submit():
   time_entry.place_forget()
   time_entry2.place_forget()
   sub_btn.place_forget()
   sub_btn2.place_forget()
   TaskFlow(task_type.get())
sub_btn = Button(root, text = 'Submit Time Constraint', command = submit, bg = "#535353", fg = "white", font = ('calibri 15 bold'))
sub_btn2 = Button(root, text = 'Submit Time Constraint', command = submit, bg = "#535353", fg = "white", font = ('calibri 15 bold'))

""" Begins main flow through the submission of the time constraint"""
def MainFlow(task):
   task_type.set(task)
   TaskFlow(task)

""" 'Triggers' the selected task """
def Task1Trigger():
   MainFlow(1)
def Task2Trigger():
   MainFlow(2)
def Task3Trigger():
   MainFlow(3)
def Task4Trigger():
   MainFlow(4)
def Task5Trigger():
   MainFlow(5)

""" Places the buttons of the grid """
def SetGrid():
   global WIDTH, HEIGHT, VRSIZE, VRDIS
   length = 40*VRSIZE*0.864
   spc = 20*VRSIZE*0.864
   ceiling = HEIGHT/2 - length * 2.5 - spc*2
   for row in range(1, ROWS + 1):
      for col in range(1, COLUMNS + 1):
        exec("sq" + str(grid_square(row, col)) + ".place( x = " + str(WIDTH/2 - length*(2 + 0.5*(COLUMNS - 2) - col) + spc*col - VRDIS - spc*(COLUMNS + 1)/2) + ", y = " + str(ceiling + length*(ROWS - row) - spc*(row - 1) + spc*(ROWS/2 + 1)) + ", width = " + str(length)+ ", height = " + str(length) + " )")
        exec("sq" + str(grid_square(row, col)) + "_2.place( x = " + str(WIDTH/2 - length*(2 + 0.5*(COLUMNS - 2) - col) + spc*col + VRDIS - spc*(COLUMNS + 1)/2) + ", y = " + str(ceiling + length*(ROWS - row) - spc*(row - 1) + spc*(ROWS/2 + 1)) + ", width = " + str(length)+ ", height = " + str(length) + " )")


""" Prevents grid from recieving input """
def PauseGrid():
   global SQUARES
   for square in range(1, SQUARES + 1):
      code = "sq" + str(square) + ".config(command = 0)" + "\nsq" + str(square) + "_2.config(command = 0)"
      exec(code)

def ClearSeqGrid():
   seq = sequence.get()
   seq = list(ast.literal_eval(seq))
   for square in seq:
      print(square)
      if task_type.get() == 5:
         exec("sq" + str(square) + ".config(bg = 'black', text = '')")
         exec("sq" + str(square) + "_2.config(bg = 'black', text = '')")
      else:
         exec("sq" + str(square) + ".config(text = '')")
         exec("sq" + str(square) + "_2.config(text = '')")

LimitTimer = Timer(0, ClearSeqGrid)

""" Displays sequence for theSustained task (5) """
def KeepSequence():
   global LimitTimer, tasks_objects, VRDIS
   beginbutton.place_forget()
   beginbutton2.place_forget()
   seq = sequence.get()
   seq = list(ast.literal_eval(seq))
   cpy_seq = copy_sequence.get()
   cpy_seq = list(ast.literal_eval(cpy_seq))
   counter = 1
   for item in seq:
      exec("sq" + str(cpy_seq[0]) + ".config(bg = 'white', text = '" + str(counter) + "')\nsq" + str(cpy_seq[0]) + "_2.config(bg = 'white', text = '" + str(counter) + "')" )
      cpy_seq.pop(0)
      counter += 1
   #LimitTimer = Timer(int(time_cons_var.get()) + tasks_objects[task_level.get() - 1] - 2, ClearSeqGrid)
   LimitTimer = Timer(60, ClearSeqGrid)
   LimitTimer.start()
   ActivateGrid()
   submitbutton.place(x = int(root['width']) / 2 - int(50*VRSIZE*0.864) - VRDIS, y = HEIGHT/2 - 40*2.5*VRSIZE*0.864 - 20*2*VRSIZE*0.864 - 15*VRSIZE*0.864 - 50*VRSIZE*0.864, width = 100*VRSIZE*0.864, height = 50*VRSIZE*0.864)
   submitbutton2.place(x = int(root['width']) / 2 - int(50*VRSIZE*0.864) + VRDIS, y = HEIGHT/2 - 40*2.5*VRSIZE*0.864 - 20*2*VRSIZE*0.864 - 15*VRSIZE*0.864 - 50*VRSIZE*0.864, width = 100*VRSIZE*0.864, height = 50*VRSIZE*0.864)
   pyautogui.moveTo(main.winfo_screenwidth()/2 - VRDIS, (main.winfo_screenheight()/2), duration = 0)

""" Removes number pad from the screen """
def HideNums():
   UserNumInputDisplay.place_forget()
   UserNumInputDisplay2.place_forget()
   
   UserNumInputDisplay.config(text = "Begin Speaking")
   UserNumInputDisplay2.config(text = "Begin Speaking")
   numclearbutton.place_forget()
   numdelbutton.place_forget()
   num0button.place_forget()
   num1button.place_forget()
   num2button.place_forget()
   num3button.place_forget()
   num4button.place_forget()
   num5button.place_forget()
   num6button.place_forget()
   num7button.place_forget()
   num8button.place_forget()
   num9button.place_forget()
   
   numclearbutton2.place_forget()
   numdelbutton2.place_forget()
   num0button2.place_forget()
   num1button2.place_forget()
   num2button2.place_forget()
   num3button2.place_forget()
   num4button2.place_forget()
   num5button2.place_forget()
   num6button2.place_forget()
   num7button2.place_forget()
   num8button2.place_forget()
   num9button2.place_forget()

""" Displays the number on the screen based on current object reference """
def DisplayNum():
   global VRDIS, VRSIZE
   main.config(cursor="none")
   seq = copy_sequence.get()
   seq = ast.literal_eval(seq)
   NumObjectRef.set(root.create_text(int(root['width'])/2 - VRDIS, int(root['height'])/2, anchor = 'center', text = str(seq[0]), fill = "white", font = ('calibri ' + str(int(300*VRSIZE)) + ' bold')))
   root.create_text(int(root['width'])/2 + VRDIS, int(root['height'])/2, anchor = 'center', text = str(seq[0]), fill = "white", font = ('calibri ' + str(int(300*VRSIZE)) + ' bold'))
UserNumInputDisplay = tkinter.Button(root, bg = "white", fg = "black", font = ('calibri 20 bold'), borderwidth = 0.1, text = "Begin Speaking")
UserNumInputDisplay2 = tkinter.Button(root, bg = "white", fg = "black", font = ('calibri 20 bold'), borderwidth = 0.1, text = "Begin Speaking")

""" Takes input of the number pad and updates user response and screen """
def NumPadInput(num):
   global UserSequence
   #timeclick = time.time_ns()
   seq = user_response.get()
   seq = list(ast.literal_eval(seq))
   seq = list(seq)
   if len(seq) == 1:
      UserNumInputDisplay.config(text = "")
      UserNumInputDisplay2.config(text = "")
   if num == -1:
      if len(seq) > 1:
         UserSequence.update({seq[len(seq) - 1]*-1: 0})
         seq.pop(len(seq) - 1)
      else:
         UserSequence.update({"DELETE_NONE": 0})
   elif num == -2:
      UserSequence.update({"CLEAR": 0})
      seq.clear()
      seq.append("")
   else:
      UserSequence.update({num: 0})
      seq.append(num)
   user_input = ""
   for item in seq:
      user_input += str(item) + " "
   #LastTime.set(timeclick)
   UserNumInputDisplay.config(text = (user_input))
   UserNumInputDisplay2.config(text = (user_input))
   user_response.set(seq)

""" Creates partial functions for number pad w/ respective numbers """
NumClear = partial(NumPadInput, -2)
NumDel = partial(NumPadInput, -1)
Num0 = partial(NumPadInput, 0)
Num1 = partial(NumPadInput, 1)
Num2 = partial(NumPadInput, 2)
Num3 = partial(NumPadInput, 3)
Num4 = partial(NumPadInput, 4)
Num5 = partial(NumPadInput, 5)
Num6 = partial(NumPadInput, 6)
Num7 = partial(NumPadInput, 7)
Num8 = partial(NumPadInput, 8)
Num9 = partial(NumPadInput, 9)

""" Intializes buttons for number pad """
numclearbutton = Button(root, borderwidth = 0.1, text = "clear", command = NumClear, font = ('calibri ' + str(int(10*VRSIZE)) + ' bold'))
numdelbutton = Button(root, borderwidth = 0.1, text = "delete", command = NumDel, font = ('calibri ' + str(int(10*VRSIZE)) + ' bold'))
num0button = Button(root, borderwidth = 1, text = "0", command = Num0, font = ('calibri ' + str(int(20*VRSIZE))+ ' bold'))
num1button = Button(root, borderwidth = 1, text = "1", command = Num1, font = ('calibri ' + str(int(20*VRSIZE))+ ' bold'))
num2button = Button(root, borderwidth = 1, text = "2", command = Num2, font = ('calibri ' + str(int(20*VRSIZE))+ ' bold'))
num3button = Button(root, borderwidth = 1, text = "3", command = Num3, font = ('calibri ' + str(int(20*VRSIZE))+ ' bold'))
num4button = Button(root, borderwidth = 1, text = "4", command = Num4, font = ('calibri ' + str(int(20*VRSIZE))+ ' bold'))
num5button = Button(root, borderwidth = 1, text = "5", command = Num5, font = ('calibri ' + str(int(20*VRSIZE))+ ' bold'))
num6button = Button(root, borderwidth = 1, text = "6", command = Num6, font = ('calibri ' + str(int(20*VRSIZE))+ ' bold'))
num7button = Button(root, borderwidth = 1, text = "7", command = Num7, font = ('calibri ' + str(int(20*VRSIZE))+ ' bold'))
num8button = Button(root, borderwidth = 1, text = "8", command = Num8, font = ('calibri ' + str(int(20*VRSIZE))+ ' bold'))
num9button = Button(root, borderwidth = 1, text = "9", command = Num9, font = ('calibri ' + str(int(20*VRSIZE))+ ' bold'))

numclearbutton2 = Button(root, borderwidth = 0.1, text = "clear", command = NumClear, font = ('calibri ' + str(int(10*VRSIZE)) + ' bold'))
numdelbutton2 = Button(root, borderwidth = 0.1, text = "delete", command = NumDel, font = ('calibri ' + str(int(10*VRSIZE)) + ' bold'))
num0button2 = Button(root, borderwidth = 1, text = "0", command = Num0, font = ('calibri ' + str(int(20*VRSIZE))+ ' bold'))
num1button2 = Button(root, borderwidth = 1, text = "1", command = Num1, font = ('calibri ' + str(int(20*VRSIZE))+ ' bold'))
num2button2 = Button(root, borderwidth = 1, text = "2", command = Num2, font = ('calibri ' + str(int(20*VRSIZE))+ ' bold'))
num3button2 = Button(root, borderwidth = 1, text = "3", command = Num3, font = ('calibri ' + str(int(20*VRSIZE))+ ' bold'))
num4button2 = Button(root, borderwidth = 1, text = "4", command = Num4, font = ('calibri ' + str(int(20*VRSIZE))+ ' bold'))
num5button2 = Button(root, borderwidth = 1, text = "5", command = Num5, font = ('calibri ' + str(int(20*VRSIZE))+ ' bold'))
num6button2 = Button(root, borderwidth = 1, text = "6", command = Num6, font = ('calibri ' + str(int(20*VRSIZE))+ ' bold'))
num7button2 = Button(root, borderwidth = 1, text = "7", command = Num7, font = ('calibri ' + str(int(20*VRSIZE))+ ' bold'))
num8button2 = Button(root, borderwidth = 1, text = "8", command = Num8, font = ('calibri ' + str(int(20*VRSIZE))+ ' bold'))
num9button2 = Button(root, borderwidth = 1, text = "9", command = Num9, font = ('calibri ' + str(int(20*VRSIZE))+ ' bold'))

""" Creates number pad on the screen """
def MakeNumPad():
   length = 40*VRSIZE
   ceiling = HEIGHT/2
   main.config(cursor="arrow")
   MoveMouse()
   numdelbutton.place(x = int(root['width'])/2 - length*1 - length/2 - VRDIS, y = ceiling - length*0, width = length, height = length)
   numclearbutton.place(x = int(root['width'])/2 - length*-1 - length/2 - VRDIS, y = ceiling - length*0, width = length, height = length)
   num0button.place(x = int(root['width'])/2 - length*0 - length/2 - VRDIS, y = ceiling - length*0, width = length, height = length)
   num7button.place(x = int(root['width'])/2 - length*1 - length/2 - VRDIS, y = ceiling - length*1, width = length, height = length)
   num8button.place(x = int(root['width'])/2 - length*0 - length/2 - VRDIS, y = ceiling - length*1, width = length, height = length)
   num9button.place(x = int(root['width'])/2 - length*-1 - length/2 - VRDIS, y = ceiling - length*1, width = length, height = length)
   num4button.place(x = int(root['width'])/2 - length*1 - length/2 - VRDIS, y = ceiling - length*2, width = length, height = length)
   num5button.place(x = int(root['width'])/2 - length*0 - length/2 - VRDIS, y = ceiling - length*2, width = length, height = length)
   num6button.place(x = int(root['width'])/2 - length*-1 - length/2 - VRDIS, y = ceiling - length*2, width = length, height = length)
   num1button.place(x = int(root['width'])/2 - length*1 - length/2 - VRDIS, y = ceiling - length*3, width = length, height = length)
   num2button.place(x = int(root['width'])/2 - length*0 - length/2 - VRDIS, y = ceiling - length*3, width = length, height = length)
   num3button.place(x = int(root['width'])/2 - length*-1 - length/2 - VRDIS, y = ceiling - length*3, width = length, height = length)
  
   numdelbutton2.place(x = int(root['width'])/2 - length*1 - length/2 + VRDIS, y = ceiling - length*0, width = length, height = length)
   numclearbutton2.place(x = int(root['width'])/2 - length*-1 - length/2 + VRDIS, y = ceiling - length*0, width = length, height = length)
   num0button2.place(x = int(root['width'])/2 - length*0 - length/2 + VRDIS, y = ceiling - length*0, width = length, height = length)
   num7button2.place(x = int(root['width'])/2 - length*1 - length/2 + VRDIS, y = ceiling - length*1, width = length, height = length)
   num8button2.place(x = int(root['width'])/2 - length*0 - length/2 + VRDIS, y = ceiling - length*1, width = length, height = length)
   num9button2.place(x = int(root['width'])/2 - length*-1 - length/2 + VRDIS, y = ceiling - length*1, width = length, height = length)
   num4button2.place(x = int(root['width'])/2 - length*1 - length/2 + VRDIS, y = ceiling - length*2, width = length, height = length)
   num5button2.place(x = int(root['width'])/2 - length*0 - length/2 + VRDIS, y = ceiling - length*2, width = length, height = length)
   num6button2.place(x = int(root['width'])/2 - length*-1 - length/2 + VRDIS, y = ceiling - length*2, width = length, height = length)
   num1button2.place(x = int(root['width'])/2 - length*1 - length/2 + VRDIS, y = ceiling - length*3, width = length, height = length)
   num2button2.place(x = int(root['width'])/2 - length*0 - length/2 + VRDIS, y = ceiling - length*3, width = length, height = length)
   num3button2.place(x = int(root['width'])/2 - length*-1 - length/2 + VRDIS, y = ceiling - length*3, width = length, height = length)

""" Speech recogntion - takes user speech and returns string """
def SpeechRec():
   global Recorder, HEIGHT, WIDTH
   with sr.Microphone() as source:
      #Recorder.adjust_for_ambient_noise(source)
      UserNumInputDisplay.config(text = "Listening...")
      UserNumInputDisplay2.config(text = "Listening...")
      audio = Recorder.listen(source, timeout = 10, phrase_time_limit = 20)
   try:
      UserNumInputDisplay.config(text = "Recognizing...")
      UserNumInputDisplay2.config(text = "Recognizing...")
      print("after")
      query = Recorder.recognize_google(audio,language = "en-US") #https://cloud.google.com/speech-to-text/docs/speech-to-text-supported-languages
      print("before")
   except Exception as e:
      UserNumInputDisplay.config(text = "Error, please enter...")
      UserNumInputDisplay2.config(text = "Error, please enter...")
      query = ""
   return query

""" Removes number from screen """
def RemoveNum():
   global VRDIS
   seq = copy_sequence.get()
   seq = ast.literal_eval(seq)
   seq = list(seq)
   seq.pop(0)
   copy_sequence.set(seq)
   root.delete(NumObjectRef.get())
   root.delete(NumObjectRef.get() + 1)

""" Takes speech and converts to number only list that is displayed """
def BeginSpeechInput():
   global UserSequence
   UserNumInputDisplay.config(text = "Please wait...")
   UserNumInputDisplay2.config(text = "Please wait...")
   try:
      UserNumInputDisplay.place(x = int(root['width'])/2 - 100 - VRDIS, y = HEIGHT/2 - 160*VRSIZE, width = 200, height = 40)
      UserNumInputDisplay2.place(x = int(root['width'])/2 - 100 + VRDIS, y = HEIGHT/2 - 160*VRSIZE, width = 200, height = 40)
      query = SpeechRec()
      submitbutton.place(x = int(root['width']) / 2 - 60 - VRDIS, y = HEIGHT/2 + 40, width = 120, height = 50)
      submitbutton2.place(x = int(root['width']) / 2 - 60 + VRDIS, y = HEIGHT/2 + 40, width = 120, height = 50)
      word_num_dict = {'one': '1','two': '2','three': '3','four': '4','five': '5','six': '6','seven': '7','eight': '8','nine': '9','zero': '0', " ": ",","-":","}
      final = ""
      for key in word_num_dict:
         if key in query:
            query = query.replace(key, word_num_dict[key])
      for val in query.split(","):
         if val.isnumeric():
            final += val
      res = list(final)
      if query != "":
         UserNumInputDisplay.config(text = ' '.join(map(str, res)))
         UserNumInputDisplay2.config(text = ' '.join(map(str, res)))
      MakeNumPad()
      if len(res) == 0:
         res = [""]
      user_response.set(res)
      for val in res:
         UserSequence.update({int(val): 0})
   except Exception as e:
      MakeNumPad()
      submitbutton.place(x = int(root['width']) / 2 - 60 - VRDIS, y = HEIGHT/2 + 40, width = 120, height = 50)
      submitbutton2.place(x = int(root['width']) / 2 - 60 + VRDIS, y = HEIGHT/2 + 40, width = 120, height = 50)

""" Displays sequence for the Flashing-Numbers task (1) """
def ShowNumSequence():
   beginbutton.place_forget()
   beginbutton2.place_forget()
   seq = sequence.get()
   seq = ast.literal_eval(seq)
   copy_sequence.set(sequence.get())
   for item in range(0, len(seq)):
      DisplayNum()
      tksleep(1)
      RemoveNum()
   pyautogui.moveTo(main.winfo_screenwidth()/2 - VRDIS, (main.winfo_screenheight()/2), duration = 0)
   Timer(0,BeginSpeechInput).start()
      
""" Microphone adjustment for background noise """
def AdjustAmbientNoise():
   global Recorder, WIDTH, HEIGHT
   with sr.Microphone() as source:
      Recorder.adjust_for_ambient_noise(source)
      Recorder.energy_threshold *= 1.5
   noisebutton.place_forget()
   noisebutton2.place_forget()
   beginbutton.place(x = WIDTH / 2 - int(75*VRSIZE) - VRDIS, y = HEIGHT / 2 - int(40*VRSIZE) + BEGINHDIS, width = int(150*VRSIZE), height = int(80*VRSIZE))
   beginbutton2.place(x = WIDTH / 2 - int(75*VRSIZE) + VRDIS, y = HEIGHT / 2 - int(40*VRSIZE) + BEGINHDIS, width = int(150*VRSIZE), height = int(80*VRSIZE))
noisebutton = Button(root, borderwidth = 1, text = "Set Ambient Noise Level", command = AdjustAmbientNoise, font = ('calibri 20 bold'), justify = "center")
noisebutton2 = Button(root, borderwidth = 1, text = "Set Ambient Noise Level", command = AdjustAmbientNoise, font = ('calibri 20 bold'), justify = "center")

""" 
Task intializations:
   1: Flashing - Numbers
   2: Flashing - Unordered
   3: Flashing - Ordered
   4: Flashing - Ordered + Numbers
   5: Sustained
"""

def Task1Main():
   global WIDTH, HEIGHT
   time_cons_var.set(1)
   user_response.set("['']")
   UserNumInputDisplay.config(text = "")
   UserNumInputDisplay2.config(text = "")
   beginbutton.config(command = ShowNumSequence)
   beginbutton2.config(command = ShowNumSequence)
   if completed_trials.get() == 0:
      noisebutton.place(x = WIDTH / 2 - int(150*VRSIZE) - VRDIS, y = HEIGHT / 2 - int(40*VRSIZE), width = int(300*VRSIZE), height = int(80*VRSIZE))
      noisebutton2.place(x = WIDTH / 2 - int(150*VRSIZE) + VRDIS, y = HEIGHT / 2 - int(40*VRSIZE), width = int(300*VRSIZE), height = int(80*VRSIZE))
   else:
      beginbutton.place(x = WIDTH / 2 - int(75*VRSIZE) - VRDIS, y = HEIGHT / 2 - int(40*VRSIZE) + BEGINHDIS, width = int(150*VRSIZE), height = int(80*VRSIZE))
      beginbutton2.place(x = WIDTH / 2 - int(75*VRSIZE) + VRDIS, y = HEIGHT / 2 - int(40*VRSIZE) + BEGINHDIS, width = int(150*VRSIZE), height = int(80*VRSIZE))
"""
lis = [1,1,1,1,1,1,1,1,1,1,0,1,0,0,1,0,0,]
def Task1Main():
   time_cons_var.set(1)
   result.set(lis[0])
   lis.pop(0)
   print(objects.get(),lis)
   TaskPass()
"""

def Task2Main():
   for row in range(1, ROWS + 1):
         for col in range(1, COLUMNS + 1):
            exec("sq" + str(grid_square(row, col)) + ".config(borderwidth = 2)")
            exec("sq" + str(grid_square(row, col)) + "_2.config(borderwidth = 2)")
   time_cons_var.set(1)
   beginbutton.place(x = int(root['width']) / 2 - int(50*VRSIZE*0.864) - VRDIS, y = HEIGHT/2 - 40*2.5*VRSIZE*0.864 - 20*2*VRSIZE*0.864 - 15*VRSIZE*0.864 - 50*VRSIZE*0.864, width = 100*VRSIZE*0.864, height = 50*VRSIZE*0.864)
   beginbutton2.place(x = int(root['width']) / 2 - int(50*VRSIZE*0.864) + VRDIS, y = HEIGHT/2 - 40*2.5*VRSIZE*0.864 - 20*2*VRSIZE*0.864 - 15*VRSIZE*0.864 - 50*VRSIZE*0.864, width = 100*VRSIZE*0.864, height = 50*VRSIZE*0.864)
   beginbutton.config(command = ShowSequence)
   beginbutton2.config(command = ShowSequence)
   SetGrid()
   PauseGrid()
   copy_sequence.set(sequence.get())
   user_response.set("['']")

def Task3Main():
   Task2Main()
   
def Task4Main():
   Task2Main()

def Task5Main():
   if task_type.get() == 5:
      for row in range(1, ROWS + 1):
         for col in range(1, COLUMNS + 1):
            exec("sq" + str(grid_square(row, col)) + ".config(borderwidth = 2)")
            exec("sq" + str(grid_square(row, col)) + "_2.config(borderwidth = 2)")
   time_cons_var.set(2)
   beginbutton.place(x = int(root['width']) / 2 - int(50*VRSIZE*0.864) - VRDIS, y = HEIGHT/2 - 40*2.5*VRSIZE*0.864 - 20*2*VRSIZE*0.864 - 15*VRSIZE*0.864 - 50*VRSIZE*0.864, width = 100*VRSIZE*0.864, height = 50*VRSIZE*0.864)
   beginbutton2.place(x = int(root['width']) / 2 - int(50*VRSIZE*0.864) + VRDIS, y = HEIGHT/2 - 40*2.5*VRSIZE*0.864 - 20*2*VRSIZE*0.864 - 15*VRSIZE*0.864 - 50*VRSIZE*0.864, width = 100*VRSIZE*0.864, height = 50*VRSIZE*0.864)
   beginbutton.config(command = KeepSequence)
   beginbutton2.config(command = KeepSequence)
   SetGrid()
   PauseGrid()
   copy_sequence.set(sequence.get())
   user_response.set("['']")
   
def Task6Main():
   for row in range(1, ROWS + 1):
      for col in range(1, COLUMNS + 1):
        exec("sq" + str(grid_square(row, col)) + ".config(borderwidth = 0)")
        exec("sq" + str(grid_square(row, col)) + "_2.config(borderwidth = 0)")
   Task5Main()

def on_closing():
   main.config(cursor="arrow")
   main.destroy()

main.protocol("WM_DELETE_WINDOW", on_closing)
main.mainloop()
