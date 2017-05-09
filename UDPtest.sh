#!/bin/bash

#Change END variable to change how long the test is (iterates over 0 to END)
END=10

clear
echo "
=======   server info   =======
	port: 6666
	ip address: 172.17.0.4"
echo "
////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////
			Correct value test            
		Room100SE from 0 to $END      
		Room1408 from 0 to $((END*10))  
		Room80085 from 0 to $((END*-1)) 
////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////
"
for ((i=0;i<=END;i++)); do
	echo "$ python sensor-udp.py -s 172.17.0.4 -p 6666 -u Room100SE -c eyeheartsockets -r $i"
	python sensor-udp.py -s 172.17.0.4 -p 6666 -u Room100SE -c eyeheartsockets -r $i
	echo
	echo "$ python sensor-udp.py -s 172.17.0.4 -p 6666 -u Room1408 -c spooky -r $((i*10))"
	python sensor-udp.py -s 172.17.0.4 -p 6666 -u Room1408 -c spooky -r $((i*10))
	echo
	echo "$ python sensor-udp.py -s 172.17.0.4 -p 6666 -u Room80085 -c 2lewd -r $((i*-1))"
	python sensor-udp.py -s 172.17.0.4 -p 6666 -u Room80085 -c 2lewd -r $((i*-1))
	echo
done

echo "


////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////
			Incorrect password test 
////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////
"

echo "$ python sensor-udp.py -s 172.17.0.4 -p 6666 -u Room100SE -c eyesockets -r 80"
python sensor-udp.py -s 172.17.0.4 -p 6666 -u Room100SE -c eyesockets -r 80
echo
echo "$ python sensor-udp.py -s 172.17.0.4 -p 6666 -u Room1408 -c spoopy -r 72"
python sensor-udp.py -s 172.17.0.4 -p 6666 -u Room1408 -c spoopy -r 72
echo
echo "$ sensor-udp.py -s 172.17.0.4 -p 6666 -u Room80085 -c giggiohihigukules -r 80085"
python sensor-udp.py -s 172.17.0.4 -p 6666 -u Room80085 -c giggiohihigukules -r 80085

echo "


////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////
			Incorrect username test 
////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////
"
echo "$ python sensor-udp.py -s 172.17.0.4 -p 6666 -u Room10ufeie0SE -c eyeheartsockets -r 80"
python sensor-udp.py -s 172.17.0.4 -p 6666 -u Room10ufeie0SE -c eyeheartsockets -r 80
echo
echo "$ python sensor-udp.py -s 172.17.0.4 -p 6666 -u Room108 -c spooky -r 72"
python sensor-udp.py -s 172.17.0.4 -p 6666 -u Room108 -c spooky -r 72
echo
echo "$ python sensor-udp.py -s 172.17.0.4 -p 6666 -u Room8008135 -c 2lewd -r 80085"
python sensor-udp.py -s 172.17.0.4 -p 6666 -u Room8008135 -c 2lewd -r 80085


echo "


////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////
			Incorrect port test 
////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////
"
echo "$ python sensor-udp.py -s 172.17.0.4 -p 6666 -u Room100SE -c eyesockets -r 80"
python sensor-udp.py -s 172.17.0.4 -p 7777 -u Room100SE -c eyeheartsockets -r 80
echo "$ python sensor-udp.py -s 172.17.0.4 -p 6666 -u Room1408 -c spoopy -r 72"
python sensor-udp.py -s 172.17.0.4 -p 666 -u Room1408 -c spooky -r 72
echo "$ sensor-udp.py -s 172.17.0.4 -p aaaa -u Room80085 -c 2lewd -r 80085"
python sensor-udp.py -s 172.17.0.4 -p aaaa -u Room80085 -c 2lewd -r 80085




echo "


////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////
			Incorrect IP test 
////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////
"
echo "$ python sensor-udp.py -s 172.17.0.4 -p 6666 -u Room100SE -c eyesockets -r 80"
python sensor-udp.py -s 117.0.4 -p 6666 -u Room100SE -c eyeheartsockets -r 80
echo "$ python sensor-udp.py -s 172.17.0.4 -p 6666 -u Room1408 -c spoopy -r 72"
python sensor-udp.py -s 172.1.0.4 -p 6666 -u Room1408 -c spooky -r 72
echo "$ sensor-udp.py -s 172.17.0.4 -p 6666 -u Room80085 -c 2lewd -r 80085"
python sensor-udp.py -s www.google.com -p 6666 -u Room80085 -c 2lewd -r 80085



echo "


////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////
			Missing arguments test 
////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////
"
echo "$ python sensor-udp.py-p 6666 -u Room100SE -c eyesockets -r 80"
python sensor-udp.py -p 6666 -u Room100SE -c eyeheartsockets -r 80
echo
echo "$ python sensor-udp.py -s 172.17.0.4 -u Room1408 -c spoopy -r 72"
python sensor-udp.py -s 172.17.0.4 -u Room1408 -c spooky -r 72
echo
echo "$ sensor-udp.py -s 172.17.0.4 -p 6666 -c 2lewd -r 80085"
python sensor-udp.py -s 172.17.0.4 -p 6666 -c 2lewd -r 80085
echo
echo "$ sensor-udp.py -s 172.17.0.4 -p 6666 -u Room80085 -r 80085"
python sensor-udp.py -s 172.17.0.4 -p 6666 -u Room80085 -r 80085
echo
echo "$ sensor-udp.py -s 172.17.0.4 -p 6666 -u Room80085 -c 2lewd"
python sensor-udp.py -s 172.17.0.4 -p 6666 -u Room80085 -c 2lewd

echo "


////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////
			Incorrectly formated arguments test 
////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////
"
echo "$ python sensor-udp.py -s 172.17.0.4 -p aaa -u Room80085 -c 2lewd -r 80"
python sensor-udp.py -s 172.17.0.4 -p aaa -u Room80085 -c 2lewd -r 80
echo
echo "$ python sensor-udp.py -s 172.17.0.4 -p 6666 -u Room80085 -c 2lewd -r aaa"
python sensor-udp.py -s 172.17.0.4 -p 6666 -u Room80085 -c 2lewd -r aaa
echo