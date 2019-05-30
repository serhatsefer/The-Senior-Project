# USAGE
# python3 main.py --prototxt deploy.prototxt --model res10_300x300_ssd_iter_140000.caffemodel -i "192.168.1.1"

# import the packages
from imutils.video import VideoStream

import face_recognition
import numpy as np
import imutils
from imutils.video import WebcamVideoStream
import time
import cv2
from datetime import datetime
import sys
import pymongo
import os
#import qrcode
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import threading
from threading import Thread
face_detect = 0
wallet_add = ""
mail = ""
def Init(ip_="",mail_=None):
    global num_det, status_mail, status_esp, face_names, \
        current_time,myclient,mydb,table_face,ip,mail,status_qr,name,face_detect,wallet_add

    try:
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["EthereumFace"]
        table_face = mydb["faceinfos"]
    except:
        print("Can't Connect Database!")


    # set detection number to 0
    num_det = "0"
    status_mail = 0
    status_esp  = 0
    face_names = []

    #status_qr = 0
    ip = ip_
    mail = mail_
    name = ""
    # load model from pc

    print("\n\n")
    print("******************************".center(80))
    print("Gebze Technical University".center(80))
    print("Department Of Electronics Engineering".center(80))
    print("The Final Project".center(80))
    print("2019".center(80))
    print("Serhat SEFER - 141024040".center(80))
    print("******************************\n\n".center(80))
    print("INFORMATIONS")
    print("____________\n")
    print("[INFO] IP/Domain : " + ip)
    print("[INFO] starting video stream...")
    print("-------------------------------\n\n")
    print("STATUSES")
    print("_______\n")
    # initialize the camera
    '''
    try:
        video_capture = cv2.VideoCapture(0)
    except:
        print("Cannot Open Camera!")
    '''

def send_email(a = threading.Event()):
    a.wait()
    while (True):
        global status_mail,current_time,mail

        if(mail != None and status_mail == 1):
            try:


                fromaddr = "gtu.finalproject.serhatsefer@gmail.com"
                toaddr = mail

                msg = MIMEMultipart()

                msg['From'] = fromaddr
                msg['To'] = toaddr
                msg['Subject'] = "NOTIFICATION - Object Has Been Detected!"
                string = ""
                for names in face_names:
                    string = string + "," + str(names)

                body = "Detections: " + names + "\n" + \
                        "Time:"+ str(current_time) + "\n" +\
                       "You Can Find The Screenshot In The Attachment!\n" + \
                       "This message sent automatically by system!"

                msg.attach(MIMEText(body, 'plain'))

                filename = "ScreenShot.png"
                attachment = open("Screenshots/screenshot.jpg", "rb")

                part = MIMEBase('application', 'octet-stream')
                part.set_payload((attachment).read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

                msg.attach(part)

                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(fromaddr, "gtu_2019")
                text = msg.as_string()
                server.sendmail(fromaddr, toaddr, text)
                server.quit()
                print("[MAIL] E-Mail Has Been Sent!")
                status_mail = 0
                a.clear()
                break
            except:
                print("[MAIL] Error! E-Mail Has Not Been Sent!")
            

def detect(a = threading.Event(),b = threading.Event()):
    global status_esp,status_mail,face_names,current_time,status_qr,qr_enable,name,wallet_add,face_detect
    b.wait()
    print("Loading Database! Please Wait A Moment!")
    #video_capture = WebcamVideoStream(src=0).start()
    video_capture = cv2.VideoCapture(0)
    # Load a sample picture and learn how to recognize it.
    #obama_image = face_recognition.load_image_file("Person/qSerhat.jpg")
    #obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

    # Load a second sample picture and learn how to recognize it.
    #biden_image = face_recognition.load_image_file("Person/ilkay.jpg")
    #biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

    # Create arrays of known face encodings and their names
    #known_face_encodings = [
    #    obama_face_encoding,
    #    biden_face_encoding
    #]
    #with open("faces.txt", "rb") as fp:  # Unpickling
    #    known_face_encodings = pickle.load(fp)

    #with open("faces_names.txt", "rb") as fp:  # Unpickling
    #    known_face_names= pickle.load(fp)


    # Initialize some variables
    face_locations = []
    face_encodings = []
    before_names = []
    known_face_encodings=[]
    known_face_names = []
    findquery = {}
    wallet = []
    status_qr = 0
    try:
        mydoc = table_face.find(findquery)
        name =  table_face.find(findquery)
        for doc in mydoc:
            known_face_encodings.append(doc['FaceID'])
            known_face_names.append(doc['Name'])
    except:
        print("Cannot Read Database!")

    known_face_encodings = np.array(list(known_face_encodings))
    print("Faces In Database: " + str(known_face_names))

    process_this_frame = True

    while True:
        # Grab a single frame of video
        try:
            _,frame = video_capture.read()
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]
            before_names = face_names
            current_time = datetime.now()
            cv2.putText(frame, "Gebze Technical University", (40,20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (178, 166, 32), 2)
            cv2.putText(frame, "Department Of Electronics Engineering", (10,40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (178, 166, 32), 2)
            cv2.putText(frame, "Serhat SEFER", (500,20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (178, 166, 32), 2)
            cv2.putText(frame, "141024040", (500,40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (178, 166, 32), 2)
            cv2.putText(frame,'Time: '+ str(current_time), (10,450),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (178, 166, 32), 1)
        except:
            print("Cannot Read Frame From Camera!")

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            try:
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                face_names = []
            except:
                print("Cannot Encode Face!")

            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                try:
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    name = "Unknown"

                # # If a match was found in known_face_encodings, just use the first one.
                # if True in matches:
                #     first_match_index = matches.index(True)
                #     name = known_face_names[first_match_index]

                # Or instead, use the known face with the smallest distance to the new face
                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]
                    face_names.append(name)
                except:
                    print("Cannot Compare Faces! Please Check Database!")


        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        if ((before_names != face_names) and (face_names != [])) :
            try:
                cv2.imwrite("Screenshots/screenshot.jpg", frame)
                status_esp =  1
                status_mail = 1
                print("Detections = " + str(face_names))
                status_qr = 1

            except:
                print("Cannot Save Screenshot!")

        process_this_frame = not process_this_frame

        if(status_qr == 1):
            findquery={"Name":name}
            mydoc = table_face.find(findquery)
            for doc in mydoc:
                wallet = doc['Wallet']
            wallet_add = wallet
            #print(wallet_add)
            break

        #status = 0
        # Display the resulting image
        try:
            cv2.imshow('Serhat SEFER - 141024040', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        except:
            print("Cannot Show Frame!")
        # Hit 'q' on the keyboard to quit!




    # Release handle to the webcam
    #try:
    b.clear()
    #video_capture.stop()
    video_capture.release()
    cv2.destroyAllWindows()
    if(status_qr == 1):
        #    print("Founded Face!")
        face_detect = 1
        wallet_add = wallet
        time.sleep(1)
        a.set()
        #qrcode.QR_Read(1,"sd",wallet)




    #os._exit(1)
    #except:
    #print("Cannot Close Windows!")

'''
import qrcode
import ethereum

Init("121","serhattrworld@gmail.com")
ethereum.InitEth("0x8b2f0388e57ac7a740931687c181999cd881c4a9")

b = threading.Event()
a = threading.Event()
c = threading.Event()
#c = threading.Event()
#c.set()

#sendmail = Thread(target=send_email,args=(c,))
#sendmail.start()
#a.set()
#b.set()
a.clear()
c.clear()
b.set()
detect(a,b)
qrcode.QR_Read(1,"serhat",100,a,c)
ethereum.buy(wallet_add,qrcode.private_key,1,c)
'''
