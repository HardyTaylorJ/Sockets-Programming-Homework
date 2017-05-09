import argparse
import hashlib
import socket

#Sensor: Room100SE recorded: 68.2 time: Sep 13 00:47:48 sensorMin: 67.4 sensorAvg: 68.0 sensorMax: 69.1 allAvg: 66.1
def main():
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--server", help="IP address of the server")
    parser.add_argument("-p", "--port", help="Port number")
    parser.add_argument("-u", "--user", help="Username")
    parser.add_argument("-c", "--password", help="Password")
    parser.add_argument("-r", "--value", help="Sensor value")
    args = parser.parse_args()

    # Catch command line misuse
    if args.server is None:
        print("missing --server argument")
        print("all arguments are required, use --help or -h for more info")
        exit()
    if args.port is None:
        print("missing --port argument")
        print("all arguments are required, use --help or -h for more info")
        exit()
    if args.user is None:
        print("missing --user argument")
        print("all arguments are required, use --help or -h for more info")
        exit()
    if args.password is None:
        print("missing --password argument")
        print("all arguments are required, use --help or -h for more info")
        exit()
    if args.value is None:
        print("missing --value argument")
        print("all arguments are required, use --help or -h for more info")
        exit()

    try:
        int(args.port)
    except:
        print("Incorrect argument: --port argument must be an integer")
        exit()
    try:
        float(args.value)
    except:
        print("Incorrect argument: --value argument must be a number")
        exit()


    # Create TCP Socket
    clisock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clisock.settimeout(3.0)
    try:
        clisock.connect((args.server, int(args.port)))
    except:
        print("failed to connect. Make sure the server is running and the IP address and port number are correct")
        print("Exiting...")
        clisock.close()
        exit()
    # send a request for a challenge value (authentication request message)
    clisock.send("REQC\n")

    # receieve challenge value
    challenge = clisock.recv(256) #FIXME: use right value

    # compute a MD5 hash of the string formed by concatenating the username, password and  the random string sent by the server. Hash = MD5("username","password","challenge")
    chash = gen_chash(args.user, args.password, challenge)
    # send the clear text "username" and the resulting "Hash" to the server.
    clisock.send("AUTH\n"+args.user+"\n"+chash+"\n")

    result = clisock.recv(256) #FIXME: use right value


    if result.split("\n")[1] == "True":
        clisock.send("DATA\n"+args.value+"\n")
    else:
        print("failed to authenticate: check username and password and try again")
        exit()
    # else: #try one more time before blaming user #FIXME: server needs to accept a 2nd try
    #     clisock.send("AUTH\n" + args.user + "\n" + chash + "\n")
    #
    #     result = clisock.recv(256)  # FIXME: use right value
    #     if result.split("\n")[1] == "True":
    #         clisock.send("DATA\n" + args.value + "\n")
    #     else:
    #         print("failed to authenticate: check username and password and try again")
    #         exit()

    final = clisock.recv(256) #FIXME: use right value
    final = final.split("\n")
    print(
    "Sensor: " + final[1] + " recorded: " + final[2] + " time: "+final[3]+" sensorMin: " + final[4] +
    " sensorAvg: " + final[5] + " sensorMax: " + final[6] + " allAvg: " + final[7] + "")



def gen_chash(uname, pwd, challenge):
    return hashlib.md5(uname+pwd+challenge).digest()



if __name__ == "__main__":
    main()
