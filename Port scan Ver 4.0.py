import socket
import os
import re
import sys
from datetime import datetime

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
    status = "Closed/Filtered or host is offline"
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.08)
            s.connect((ip, port))
            status = "Open"
    except (socket.timeout, ConnectionRefusedError):
        pass
    finally:
        # Get current time for logging
        current_time = datetime.now().strftime("%d-%b-%Y (%H:%M:%S)")
        log_entry = f"For IP:{ip}:{port} {status} at {current_time}"
        logs.append(f"{log_entry}")
        with open("ip_port_log.txt", "a") as log_file:
            log_file.write(f"{log_entry}\n")
        print(log_entry)

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



