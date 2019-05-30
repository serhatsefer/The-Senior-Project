# import the necessary packages
from pyzbar import pyzbar
import argparse
import cv2
from imutils.video import WebcamVideoStream
import time
import ethereum
import imutils
import threading
# construct the argument parser and parse the arguments

qr_enable = 0

private_key=""

def QR_Read(isactive,name,a = threading.Event(),b=threading.Event()):
    global qr_enable,private_key
    a.wait()
    a.clear()
    if(isactive == 1):
        try:
            sender = "0x2cF1DAf65898c658C2732161100cA247384c689a"
            contract = "0x3329010478fe7bad89a4175fb2b45a4a507109a4"
            vs = WebcamVideoStream().start()
            time.sleep(2.0)
            check_qr = 0
        except:
            print("Can't Open Camera For Reading QR!")

        #ethereum.InitEth(sender, contract)
        while True:
            try:
                image = vs.read()
                #image = imutils.resize(image, width=400)

                small_image = cv2.resize(image, (0, 0), fx=0.25, fy=0.25)
            # load the input image
                #image = cv2.imread(frame)

                # find the barcodes in the image and decode each of the barcodes
                barcodes = pyzbar.decode(small_image)

                #cv2.imshow("sas",image)

                # loop over the detected barcodes
                for barcode in barcodes:
                    # extract the bounding box location of the barcode and draw the
                    # bounding box surrounding the barcode on the image
                    (x, y, w, h) = barcode.rect
                    x *= 4
                    y *= 4
                    w *= 4
                    h *= 4
                    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

                    # the barcode data is a bytes object so if we want to draw it on
                    # our output image we need to convert it to a string first
                    barcodeData = barcode.data.decode("utf-8")
                    barcodeType = barcode.type

                    # draw the barcode data and barcode type on the image
                    #text = "{} ({})".format(barcodeData, barcodeType)
                    #cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    #    0.5, (0, 0, 255), 2)

                    # print the barcode type and data to the terminal
                    #print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))
                    print("Recognized QR Code!")
                    check_qr = 1
                



            # show the output image
                cv2.namedWindow("QR CODE READER")
                cv2.imshow("QR CODE READER",image)
                #cv2.imshow("Private KEY Scanner For {}".format(name), image)
                #cv2.waitKey(1)
                if(cv2.waitKey(20) & 0xFF == ord("q")):
                    break


                #cv2.destroyAllWindows()
                # if the `q` key was pressed, break from the loop
                #if key == ord("q"):
                #    break

                if (check_qr == 1):
                    qr_enable = 1
                    private_key = barcodeData
                    #print(private_key)
                    b.set()
                    break
                #cv2.waitKey(0)
            except:
                print("Error While Reading QR Code!")


                if(cv2.waitKey(1) & 0XFF == ord("q")):
                    break
            #except:
            #   print("Error")
        a.clear()
        vs.stop()
        cv2.destroyAllWindows()

#a = threading.Event()
#a.set()
#QR_Read(1,"serhat",100,a)

