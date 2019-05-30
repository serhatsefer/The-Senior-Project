import ethereum
import qrcode
import detection
import argparse
from threading import Thread
import threading


money = 20

def require():
    global  arg
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--ip", type=str, required=True,
                help="IP Address Of ESP8266")
    ap.add_argument("-e","--email",type=str,required=False,
                    help="If You Want To Get An Email About Detection,Enter Your E-Mail")
    ap.add_argument("-c","--contract",type=str,required=True,
                    help="Contract Address")
    ap.add_argument("-t","--to",type=str,required=True,
                    help="Target Wallet Address To Send Money")

    arg = vars(ap.parse_args())


def main():
    print("main")


if __name__ == "__main__":
    require()


    detection.Init(arg["ip"], arg["email"])
    ethereum.InitEth(arg["contract"],arg["to"],arg["ip"])
    while True:
        #http_info = Thread(target=ethereum.send_info, args=(arg["ip"],))
        #http_info.setDaemon(True)
        #a = threading.Event()
        b = threading.Event()
        b.set()
        #detect = Thread(target=detection.detect,args=(a,b,))
        #a.clear()
        #detect.setDaemon(True)

        sendmail = Thread(target=detection.send_email,args = (b,))
        #sendmail.setDaemon(True)
        #check = Thread(target=main)
        #check.setDaemon(True)

        #detect.start()
        #http_info.start()
        sendmail.start()
        #check.start()


      #  asd = Thread(target=qrcode.QR_Read, args=(1, "serhat", "123", a))
      #  asd.start()

        #http_info.join(10)
        #print("\n")
        #sendmail.join(20)



        b = threading.Event()
        a = threading.Event()
        c = threading.Event()
        # c = threading.Event()
        # c.set()

        # sendmail = Thread(target=send_email,args=(c,))
        # sendmail.start()
        # a.set()
        # b.set()
        a.clear()
        c.clear()
        b.set()
        detection.detect(a, b)
        qrcode.QR_Read(1, "serhat", a, c)
        ethereum.buy(detection.wallet_add, qrcode.private_key, money, c)

