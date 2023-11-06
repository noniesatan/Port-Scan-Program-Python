# Port-Scan-Program-Python
To check what is your port open 
Mac User----------------------
1.Open Terminal 
2.run this line:      lsof -i -P | grep LISTEN | grep :$PORT
3.check the ip and port on first line 
4.Add the port number in the first line into "ports.txt"
5.Run the program

Windows User----------------------
1.Open cmd
2.run ipconfig and netstat -a
3.check the ip and port on first line 
4.Add the port number in the first line into "ports.txt"
5.Run the program
