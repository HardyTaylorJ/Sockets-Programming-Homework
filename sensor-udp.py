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
    clisock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # clisock.connect((args.server, int(args.port)))
    reqout = 20 #todo: allow as arg
    clisock.settimeout(1.0) #todo: allow as arg
    server = (args.server, int(args.port))
    #try requout times to request a challenge before failure
    i = 0
    while True:
        try:
            # send a request for a challenge value (authentication request message)
            clisock.sendto("REQC\n", server)

            # receieve challenge value
            challenge, srv = clisock.recvfrom(256) #FIXME: use right value
            break
        except socket.error:
            i+=1
            if i>=reqout:
                print("tried to contact server "+str(reqout)+" times with no response. Make sure the server is running and the IP address and port number are correct")
                print("Exiting...")
                clisock.close()
                exit()



    # compute a MD5 hash of the string formed by concatenating the username, password and  the random string sent by the server. Hash = MD5("username","password","challenge")
    chash = gen_chash(args.user, args.password, challenge)

    # try requout times to send authentication information before failure
    i = 0
    while True:
        try:
            # send the clear text "username" and the resulting "Hash" to the server.
            clisock.sendto("AUTH\n"+args.user+"\n"+chash+"\n", server)

            result, srv = clisock.recvfrom(256) #FIXME: use right value
            break
        except socket.error:
            i+=1
            if i>=reqout:
                print("tried to contact server 20 times with no response. Exiting")
                clisock.close()
                exit()

    # try requout times to send data before failure
    i=0
    while True:
        try:
            if result.split("\n")[1] == "True":
                clisock.sendto("DATA\n"+args.value+"\n", server)
            else:
                print("failed to authenticate: check username and password and try again")
                exit()
             #FIXME: server needs to accept a 2nd try before blaming user in case of corrupt packet

            final, srv = clisock.recvfrom(256) #FIXME: use right value
            break
        except socket.error:
            i+=1
            if i>=reqout:
                print("tried to contact server "+str(reqout)+" times with no response. Exiting")
                clisock.close()
                exit()

    final = final.split("\n")
    print(
    "Sensor: " + final[1] + " recorded: " + final[2] + " time: "+final[3]+" sensorMin: " + final[4] +
    " sensorAvg: " + final[5] + " sensorMax: " + final[6] + " allAvg: " + final[7] + "")



def gen_chash(uname, pwd, challenge):
    return hashlib.md5(uname+pwd+challenge).digest()



if __name__ == "__main__":
    main()
