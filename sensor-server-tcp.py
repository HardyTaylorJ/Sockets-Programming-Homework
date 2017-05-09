import argparse
import hashlib
import random
import string
import socket
import time

def main():
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", help="Port number")
    parser.add_argument("-f", "--file", help="Path to CSV file containing username-password set")
    parser.add_argument("-v", "--verbose", help="Verbose", action="store_true")
    args = parser.parse_args()
    if args.verbose:
        print("verbose mode turned on")

    # Catch command line misuse
    if args.port is None:
        print("missing --port argument")
        print("all arguments are required, use --help or -h for more info")
        exit()
    if args.file is None:
        print("missing --file argument")
        print("all arguments are required, use --help or -h for more info")
        exit()
    try:
        int(args.port)
    except:
        print("Incorrect argument: --port argument must be an integer")
        exit()

    # parse the passwords file into a dictionary
    users = {}
    try:
        with open(args.file) as f:
            for line in f:
                line = line.strip().split(",", 1)
                users[line[0]] = line[1]
    except:
        print("file invald")
        exit()

    # create TCP socket
    servesock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    servesock.bind((host, int(args.port)))
    servesock.listen(1)

    """Message types
    REQC: authentication request (REQuest Challenge)
    CHAL: CHALlenge value
    AUTH: AUTHentication information
    ARES: Authentication RESult
    DATA: sensor DATA
    FIND: FINal Data
    """
    # connections[addr] = [authenticated, challenge]
    connections = {}

    # data[username] = [values]
    data = {}
    for uname in users.keys():
        data[uname] = []
    # start listening
    if args.verbose: print("starting listening")
    while True:
        conn, addr = servesock.accept()
        while True:
            msg = conn.recv(256)

            if addr not in connections:
                connections[addr] = [0,gen_challenge()]

            type, msg = msg.split("\n",1)
            if args.verbose: print("Type: "+ type)

            if type == "REQC":
                if args.verbose: print("REQC received, Sending challenge")
                conn.send(connections[addr][1])
            elif type == "AUTH":
                if args.verbose: print("AUTH received, starting authentication")
                uname = msg.split("\n",1)[0]
                chash = msg.split("\n",1)[1].strip()
                result = auth(users,uname, chash, connections[addr][1])
                if args.verbose: print("Authentication complete:" + str(result))
                connections[addr][0] = result
                conn.send("ARES\n" + str(result))
                if not result:
                    print("User authorization failed for client: "+str(addr[0])+" port: "+str(args.port)+" user: "+uname)
                    break
            elif (type == "DATA") and (connections[addr][0] == True):
                data[uname].append(float(msg))
                allval = [i for j in data.values() for i in j]
                allavg = sum(allval)/len(allval)
                t = str(time.asctime( time.localtime(time.time())))[4:-5]
                print("Sensor: "+str(uname)+" recorded: "+msg.strip()+" time: "+t+" sensorMin: "+str(min(data[uname]))+
                      " sensorAvg: "+str(sum(data[uname])/len(data[uname]))+" sensorMax: "+str(max(data[uname]))+" allAvg: "+str(allavg)+"")
                conn.send("FIND\n"+uname+"\n"+msg.strip()+"\n"+t+"\n"+str(min(data[uname]))+"\n"+str(sum(data[uname])/len(data[uname]))+"\n"+str(max(data[uname]))+"\n"+str(allavg)+"\n")
                break



    # receive authentication request

    # respond with one time use, challenge value in the form of a random 64 character string. (You get to decide how this random string is generated.)
    #generate challenge string

    # receive username and hash from the client

    # compare client generated hash to server's hash
    # auth(users,uname,chash,challenge)

    #display information sent by client



def auth(users,uname,chash,challenge):
    """Returns True if the user can be authenticated, False if the user cannot be authenticated
    :param users: the dictionary of users and passwords from the file imported by the user
    :param uname: the username sent by the client
    :param chash: the hashed password sent by the client
    :param challenge: the callenge string that the user hashed their password with"""
    # finds password for username, returns false if user does not exist
    if uname in users:
        pwd = users[uname]
    else: return False

    # perform same md5 calculation as sensor
    md5r = hashlib.md5(uname+pwd+challenge).digest().strip()

    # check if md5s match
    if md5r == chash: return True
    return False


def gen_challenge():
    """Returns a 64 character string made of ASCII upper and lower case letters and punctuation (no whitespace characters)"""
    return ''.join(random.choice(string.lowercase + string.uppercase + string.punctuation) for c in range(64))


if __name__ == "__main__":
    main()
