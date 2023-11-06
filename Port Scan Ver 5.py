# Nont Sumate   date: 3 Nov 2023  Purpose : Port scan program
import socket
import os
import re
import sys
from datetime import datetime
#color
RESET = "\033[0m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"



# Global list variable to keep the logs
logs = []

# Function to check the validity of a subnet
def validate_subnet():
    while True:
        subnet = input("Enter the first three octets of the subnet (e.g., 192.168.1): ")
        if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}$', subnet):
            return subnet
        else:
            print("Invalid subnet format. Please try again.")

# Function to check port status and log the connection status
def check_port_status(ip, port):
    
    
    current_time = datetime.now().strftime("%d-%b-%Y (%H:%M:%S)")
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.settimeout(0.002)
    con = s.connect_ex((ip, port))
    with open('ip_port_log.txt','a') as log_file:
        if con == 0:
            log_file.write(f'For ip {ip} port {port} ------open-------- at {current_time}\n')
            print(f'{GREEN}For ip {ip} port {port} ------open-------- at {current_time}{RESET}')
        else:
            log_file.write(f'For ip {ip} port {port} close/Filtered or host is offline at {current_time}\n')
            print(f'For ip {ip} port {port} close/Filtered or host is offline at {current_time}')

        s.close()


        
# Function to write logs to event viewer
def write_to_event_viewer(logs):
    # Implementation for writing logs to event viewer can be added here
    pass




# Main function
def get_valid_port_numbers():
    port_numbers = set()
    while True:
        if os.path.exists("ports.txt"):
            if os.path.getsize("ports.txt") == 0:
                print("Error: ports.txt file is empty. Please put valid port numbers in ports.txt.")
            else:
                with open("ports.txt", "r") as port_file:
                    for line in port_file:
                        port = line.strip()
                        if port.isdigit():
                            port_numbers.add(int(port))
                if port_numbers:
                    break
                else:
                    print("Error: No valid port numbers found in ports.txt. or the file is empty")
        else:
            print("Error: ports.txt file not found. Please create a ports.txt file.")

        input("Please put valid port numbers in ports.txt and then press enter...")
        port_numbers.clear()
    return port_numbers


def main():
    try:
        # Get a valid subnet
        subnet = validate_subnet()

        # Generate list of IP addresses
        ip_addresses = [f"{subnet}.{i}" for i in range(11, 254, 2)]

        # Read unique port numbers from port.txt file
        port_numbers = get_valid_port_numbers()

        # Check port status for each IP address and port number
        for ip in ip_addresses:
            for port in port_numbers:
                check_port_status(ip, port)

        # Write logs to event viewer
        write_to_event_viewer(logs)

    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
if __name__ == "__main__":
    main()



