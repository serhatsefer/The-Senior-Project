import face_recognition
import pickle
import glob,os
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["EthereumFace"]
table_face = mydb["faceinfos"]


def start(file = None , walletAddress=""):

    known_face_encodings = []
    known_face_names = []
    all_files = []
    all_wallets = []
    check_file_is_none = 0
    check_database = 0
    first_face_encoding = []
    name = ""
    if (file == None):
        os.chdir("Person")
        globs = glob.glob("*.jpg")
        for file in globs:
            all_files.append("Person/" + file)
            all_wallets.append(str(input("Please Enter The Wallet Address For {}\n".format(file))))
        os.chdir("..")
        check_file_is_none= 1

    elif ( file != None ):
        all_files.append(file)
    print("Pictures Will Be Modelled = "+ str(all_files) + "\n")
    for file_ in all_files:
        try:
            result = []
            first_image = face_recognition.load_image_file(file_)
            name = file_.replace('Person/', '')
            name = name.replace('.jpg','')
            first_face_encoding = face_recognition.face_encodings(first_image)[0]
            if(check_file_is_none == 1):
                walletAddress = all_wallets[all_files.index(file_)]
            print("{} Has Been Modelled Successfully!".format(file_))
        except:
            print("Error! Cannot Find File {} Or There Is No Face In The Picture.".format(file_))


        #findquery = {"$or":[ {"Name":{"$eq":name}} , {"Wallet":{"$eq":walletAddress}} ]}
        findquery1 = {"Name":{"$eq":name}}
        mydoc1 = table_face.find(findquery1)
        for doc in mydoc1:
            result += doc

        findquery2 = {"Wallet": {"$eq": walletAddress}}
        mydoc2 = table_face.find(findquery2)
        for doc in mydoc2:
            result += doc

        if(len(result) == 0):
            mydict = {"FaceID": list(first_face_encoding) , "Name": name, "Wallet":   walletAddress}
            table_face.insert_one(mydict)
            print("\nFace Model Have Been Written To Database Successfully!")
            check_database = 1
        else:
            print("\nError! This Name Or Wallet Address Were Added Before.\nSo,This Face Was Not Added To Database!")
            check_database = 0
    return check_database

def clear():
    table_face.delete_many({})
    print("Database Was Cleared!")


