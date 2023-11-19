# Nont Sumate   nont.sumate@studytafensw.edu.au as 'Copyright Red Opal Innovation'
# License 'Proprietary'
# date : 7 November 2023
# version 1.0.1
# Status: development

import socket
import os
import re
import sys
from datetime import datetime
import win32evtlogutil
import win32evtlog

# color
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
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.settimeout(0.002)
    con = s.connect_ex((ip, port))
    with open('ip_port_log.txt', 'a') as log_file:
        if con == 0:
            log_file.write(f'For ip {ip} port {port} ------open-------- at {current_time}\n')
            print(f'{GREEN}For ip {ip} port {port} ------open-------- at {current_time}{RESET}')
        else:
            log_file.write(f'For ip {ip} port {port} close/Filtered or host is offline at {current_time}\n')
            print(f'For ip {ip} port {port} close/Filtered or host is offline at {current_time}')

        s.close()


# Function to write logs to event viewer

def report_EV(mylists,eventtype):
    IP_EVT_APP_NAME = " CheckIPPort - IP-Port Scan Application"
    IP_EVT_ID = 7040
    IP_EVT_CATEG = 9876
    IP_EVT_TYPE = win32evtlog.EVENTLOG_WARNING_TYPE  # WARNING=2
    IP_EVT_ERR = win32evtlog.EVENTLOG_ERROR_TYPE  # ERROR=1
    IP_EVT_STRS = mylists
    IP_EVT_DATA = b"Scan IP Address Event Data"
    win32evtlogutil.ReportEvent(IP_EVT_APP_NAME, \
                                IP_EVT_ID, \
                                eventCategory=IP_EVT_CATEG, \
                                eventType=eventtype, \
                                strings=IP_EVT_STRS, \
                                data=IP_EVT_DATA)


# Main function
def get_valid_port_numbers():
    while True:
        port_numbers = set()
        if os.path.exists("ports.txt"):
            if os.path.getsize("ports.txt") == 0:
                print("Error: ports.txt file is empty. Please put valid port numbers in ports.txt.")
            else:
                with open("ports.txt", "r") as port_file:
                    for line in port_file:
                        port = line.strip()
                        if port.isdigit():
                            port = int(port)
                            if 1024 <= port <= 65535:
                                port_numbers.add(port)
                            else:
                                print(
                                    f"Error: Port {port} is not in the valid range (1024 to 65535). Please enter a valid port.")
                                break
                    else:
                        if port_numbers:
                            break
                        else:
                            print("Error: No valid port numbers found in ports.txt.")
        else:
            print("Error: ports.txt file not found. Please create a ports.txt file.")

        input("Please put valid port numbers in ports.txt and then press enter...")

    return port_numbers

def main():
    try:
        # Get a valid subnet
        subnet = validate_subnet()

        # Generate list of IP addresses
        ip_addresses = [f"{subnet}.{i}" for i in range(11, 254, 2)]
        mylists = []
        mylists.extend(ip_addresses)


        # Read unique port numbers from port.txt file
        port_numbers = get_valid_port_numbers()

        # Check port status for each IP address and port number
        for ip in ip_addresses:
            for port in port_numbers:
                check_port_status(ip, port)

        # Write logs to event viewer
        report_EV(ip_addresses, 2)

    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()



