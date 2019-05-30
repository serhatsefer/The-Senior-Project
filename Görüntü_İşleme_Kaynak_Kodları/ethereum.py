#                  ETHEREUM & SMART CONTRACT & SENSORS VALUE
#
#                          ~ 2019 Serhat SEFER ~
#
#
#                              | USAGE |
#
#


############################### IMPORTS #######################################
#################################################################################

import json
import sys
import argparse
import pymongo
from web3 import Web3, HTTPProvider
from web3.contract import ConciseContract
import requests
import threading

############################### VARIABLES #######################################
#################################################################################


# Set Ethereum URL
eth_URL = 'http://localhost:8545'

# Declaration Of Addresses
# senderAddress = '0x68cae41916deb63beca72ee0c272031a73cbac35'
contractAddress = '0x8b2f0388e57ac7a740931687c181999cd881c4a9'

#to = "0x60a716a961a173a8cdba3589e2119150b908a194"
to = ""
confirmed = 0
pay_money = 0
is_called_buy = 0
wallet_add = "0x3dfbbb16719ce30ee1b0fcb43791f7ec877c75f8"
private_key = "0xa60e7b8ad1f4944fd1a0d3614f3b22cedf80cec0899824812e4e15fb9a0ae1f2"
money = 0


############################### FUNCTIONS #######################################
#################################################################################

# Function To Setup Addresses
def SetParameter():
    global wallet_add, private_key, to, money
    ap = argparse.ArgumentParser()
    ap.add_argument("-w", "--wallet", required=True, type=str,
                    help="HTTP Provider URL")
    ap.add_argument("-p", "--private", required=True, type=str,
                    help="Contract Address")
    ap.add_argument("-t", "--to", required=True, type=str,
                    help="Sender Address")
    ap.add_argument("-m", "--money", required=True, type=int,
                    help="Sender Address")
    args = vars(ap.parse_args())
    wallet_add = args["wallet"]
    private_key = args["private"]
    to = args["to"]
    money = args["money"]


# Function To Initialize Ethereum Network
def InitEth(contractAddress,to_, ip_):
    try:
        global fContract, contractAdd, w3, eth_URL, mail, status_mail, ip,to
        w3 = Web3(HTTPProvider(eth_URL, request_kwargs={'timeout': 100}))
        # w3.eth.defaultAccount = w3.toChecksumAddress(senderAddress)
        contractAdd = w3.toChecksumAddress(contractAddress)
        ip = ip_
        to = to_
        with open('bank.abi', 'r') as abi_definition:
            abi = json.load(abi_definition)
        fContract = w3.eth.contract(address=contractAdd, abi=abi)
    except:
        print("Oops!", sys.exc_info()[0], " occured.")


def buy(wallet_add, private_key, money, a=threading.Event()):
    global to, pay_money, is_called_buy, status_mail, ip
    a.wait()
    is_called_buy = 1
    try:
        transaction = {
            'nonce': w3.eth.getTransactionCount(w3.toChecksumAddress(wallet_add)),
            'gasPrice': w3.eth.gasPrice,
            'gas': 100000,
            # to=w3.toChecksumAddress("0x6923174442be1530cd64656e802e0bb5ab207e4e"),
            # w3.toChecksumAddress('0x8748d1ff0eb974e3258134d52fe835d37698cad9'),
            'value': w3.toWei(money, 'ether')

        }

        # signed_txn = w3.eth.account.signTransaction(transaction,key)
        transact = fContract.functions.pay(w3.toChecksumAddress(to)).buildTransaction(transaction)
        signTransact = w3.eth.account.signTransaction(transact, private_key=private_key)
        w3.eth.sendRawTransaction(signTransact.rawTransaction)
        print("Sent Money!")
        pay_money = 1

        send_info(ip,wallet_add,private_key,money)

    except:
        print("Cannot Send Money! Please Check Your Balance Or Private Key.")
        send_error(ip)


def confirm(wallet_add, private_key):
    global pay_money, confirmed, status_mail
    try:
        transaction = {
            'nonce': w3.eth.getTransactionCount(w3.toChecksumAddress(wallet_add)),
            'gasPrice': w3.eth.gasPrice,
            'gas': 100000,
            # to=w3.toChecksumAddress("0x6923174442be1530cd64656e802e0bb5ab207e4e"),
            # w3.toChecksumAddress('0x8748d1ff0eb974e3258134d52fe835d37698cad9'),
            #'value': w3.toWei(money, 'ether')

        }

        # signed_txn = w3.eth.account.signTransaction(transaction,key)
        transact = fContract.functions.confirm().buildTransaction(transaction)
        signTransact = w3.eth.account.signTransaction(transact, private_key=private_key)
        w3.eth.sendRawTransaction(signTransact.rawTransaction)
        confirmed = 1
        if (pay_money == 1):
            print("Confirmed!")
    except:
        print("Cannot Confirmed Money!")


def withdraw(wallet_add, private_key, money):
    try:
        transaction = {
            'nonce': w3.eth.getTransactionCount(w3.toChecksumAddress(wallet_add)),
            'gasPrice': w3.eth.gasPrice,
            'gas': 100000,
            # to=w3.toChecksumAddress("0x6923174442be1530cd64656e802e0bb5ab207e4e"),
            # w3.toChecksumAddress('0x8748d1ff0eb974e3258134d52fe835d37698cad9'),
            #'value': w3.toWei(money, 'ether')

        }

        # signed_txn = w3.eth.account.signTransaction(transaction,key)
        transact = fContract.functions.withdraw(w3.toWei(money, 'ether')).buildTransaction(transaction)
        signTransact = w3.eth.account.signTransaction(transact, private_key=private_key)
        w3.eth.sendRawTransaction(signTransact.rawTransaction)
        print("Refund Was Made!")
    except:
        print("Cannot Refund! Please Contact Your Seller!")


def send_info(ip,wallet_add,private_key,money):
    global confirmed, pay_money, is_called_buy
    while (True):

        if ((pay_money == 1)):
            try:
                send_inform = requests.get("http://" + ip + "/successful", timeout=10)
                print("Payment Has Been Successfull!")
                if (send_inform.status_code == 200):
                    print("[ESP8266] [" + str(send_inform.status_code) + "] Data Has Been Sent!(" + ip + ")")
                    confirm(wallet_add, private_key)
                else:
                    print("[ESP8266] [" + str(
                        send_inform.status_code) + "] An Error Occured During Sending Data To ESP8266! (" +
                          ip + ")")
                    withdraw(wallet_add, private_key, money)
                pay_money = 0
                confirmed = 0
                break
            except:
                print("[ESP8266] Can't Connect To IP Address! Please Check The Connection!")
                withdraw(wallet_add, private_key, money)
                break

def send_error(ip):
    global confirmed, pay_money, is_called_buy, wallet_add, private_key, money
    while True:
        try:
            send_inform = requests.get("http://" + ip + "/unsuccessful", timeout=10)
            print("Payment Has Been Unsuccessfull!")
            if (send_inform.status_code == 200):
                print("[ESP8266] [" + str(send_inform.status_code) + "] Data Has Been Sent!(" + ip + ")")
            else:
                print("[ESP8266] [" + str(
                    send_inform.status_code) + "] An Error Occured During Sending Data To ESP8266! (" +
                      ip + ")")
            break
        except:
            print("[ESP8266] Can't Connect To IP Address! Please Check The Connection!")
            break
################################## MAIN #########################################
#################################################################################


# InitEth(contractAddress)
# a = threading.Event()

# a.set()
# while True:
#    buy(wallet_add,private_key,money,a)
#    send_info("google.com")

#    print(pay_money)
#    print(confirmed)
#    send_info("google.com")

