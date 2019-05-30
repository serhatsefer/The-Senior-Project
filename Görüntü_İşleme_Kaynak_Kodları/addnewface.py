# import the necessary packages
from tkinter import *
from PIL import Image
from PIL import ImageTk
from tkinter import filedialog
import cv2
from tkinter import messagebox
from imutils.video import VideoStream
import time
import numpy as np
import face_recognition
import model
import argparse
from tkinter.ttk import Frame, Label, Entry

ap = argparse.ArgumentParser()
ap.add_argument("-c", "--clear", type=int, required=False,
                help="clear all face data!")
ap.add_argument("-a", "--all", type=int, required=False,
                help="Add All Faces In Person Directory!")
args = vars(ap.parse_args())


detected_face = 0
E1 = ""
E2 = ""





def Video():
    global E1,E2
    if(E1.get() != "" and E2.get()!= ""):
        msg = "The Person Is " + E1.get()
        messagebox.showinfo("Info",msg)
        print(msg)
        msg2 = "The Wallet Address Is " + E2.get()
        messagebox.showinfo("Info",msg2)
        print(msg2)
        cam = cv2.VideoCapture(0)

        cv2.namedWindow(msg)

        img_counter = 0
        process_this_frame = True
        check = 1
        while check:
            ret, frame = cam.read()
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = small_frame[:, :, ::-1]
            detected_face = 0
            if process_this_frame:
                # Find all the faces and face encodings in the current frame of video
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)





            # Display the results
            for (top, right, bottom, left) in face_locations:
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Draw a box around the face
                #cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                detected_face = 1
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, "FACE FOUND! PLEASE PRESS SPACE TO SAVE PHOTO!", (70,20), font, 0.5 , (255, 255, 255), 1)

            cv2.imshow(msg, frame)
            if not ret:
                break
            k = cv2.waitKey(1)

            if k % 256 == 27:
            # ESC pressed
                print("Escape hit, closing...")
                break
            elif k % 256 == 32 and detected_face == 1:
            # SPACE pressed
                img_name = "Person/{}.jpg".format(E1.get())
                cv2.imwrite(img_name, frame)
                print("{} written!".format(img_name))
                #messagebox.showinfo("Info","{} written".format(img_name))
                check = 0
                cam.release()
                cv2.destroyAllWindows()

                if(model.start(img_name,E2.get()) == 1):
                    messagebox.showinfo("SUCCESSFUL!", "FACE WAS ADDED TO MODEL SUCCESSFULLY!")
                else:
                    messagebox.showinfo("ERROR!", "This Name Or Wallet Address Were Added Before.")


                img_counter += 1
            elif k % 256 == 32 and detected_face == 0:
                print("FACE NOT FOUND! PLEASE WAIT UNTIL FACE FOUND MESSAGE OF THE TOP OF THE WINDOW AND PRESS SPACE BUTTON TO SAVE! ")
            process_this_frame = not process_this_frame
        cam.release()

        cv2.destroyAllWindows()
    else:
        if(E1.get() == ""):
            messagebox.showinfo("Error!", "Please Enter The Name Of Person Who Will Be Taken Photo!")
            print("Please Enter The Name Of Person Who Will Be Taken Photo!")
        if(E2.get() == ""):
            messagebox.showinfo("Error!", "Please Enter The Wallet Address Of Person Who Will Be Taken Photo!")
            print("Please Enter The Wallet Address Of Person Who Will Be Taken Photo!")

def prints():
    global E1,E2

    print(E1.get())
    print(E2.get())
# initialize the window toolkit along with the two image panels

if(args["clear"] == 1):
    model.clear()

if(args["all"] == 1):
    model.start()
else:
    root = Tk()
    root.wm_title("Save New Person To Database")
    root.geometry("500x200")
    panelA = None
    panelB = None

    # create a button, then when pressed, will trigger a file chooser
    # dialog and allow the user to select an input image; then add the
    # button the GUI

    #self.master.title("Review")
    #self.pack(fill=BOTH, expand=True)
    frame0 = Frame()
    frame0.pack(fill=X)

    L1 = Label(frame0, text="Please Enter The Name Of Person Who Will Be Taken Photo!")
    L1.pack( side = "top")
    L2 = Label(frame0, text="Then Click Open Camera Button.")
    L2.pack( side = "top")
    L3 = Label(frame0, text="To Take Picture Press Space Button In The Camera Window")
    L3.pack( side = "top")

    frame1 = Frame()
    frame1.pack(fill=X)

    lbl1 = Label(frame1, text="Name:", width=15)
    lbl1.pack(side=LEFT, padx=5, pady=5)

    E1 = Entry(frame1)
    E1.pack(fill=X, padx=5)

    frame2 = Frame()
    frame2.pack(fill=X)

    lbl2 = Label(frame2, text="Wallet Address:", width=15)
    lbl2.pack(side=LEFT, padx=5, pady=5)

    E2 = Entry(frame2)
    E2.pack(fill=X, padx=5)

    frame3 = Frame()
    frame3.pack(fill=BOTH)

    btn1 = Button(frame3, text="Open Camera", command=Video,width=10,height=10)
    btn1.pack(side="bottom", fill="both",padx="10", pady="10")

    # kick off the GUI
    root.mainloop()

