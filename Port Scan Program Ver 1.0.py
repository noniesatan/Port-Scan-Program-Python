
import socket




# Function to check if a given IP address is odd
def is_odd(ip):
    last_octet = int(ip.split('.')[-1])
    return last_octet % 2 != 0

# Function to validate subnet and return a list of valid IP addresses
def get_valid_ips(subnet):
    valid_ips = []
    for i in range(11, 254):
        ip = f"{subnet}.{i}"
        if is_odd(ip):
            valid_ips.append(ip)
    return valid_ips

# Function to check port status for a given IP address and port number
def check_port(ip, port):
    try:
        socket.setdefaulttimeout(1)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))
        s.close()
        return True
    except (socket.timeout, ConnectionRefusedError):
        return False

# Main function to read port numbers from ports.txt and perform port scanning
def main():
    try:
        with open("ports.txt", "r") as file:
            ports = file.read().splitlines()
    except FileNotFoundError:
        print("Error: ports.txt not found.")
        return

    unique_ports = list(set(ports))
    if len(unique_ports) != len(ports):
        print("Warning: Some ports are entered multiple times.")

    subnet = input("Enter the subnet (x.x.x): ")
    if not subnet.startswith("192.168.1"):
        print("Error: Invalid subnet. Only 192.168.1.x is allowed.")
        return

    valid_ips = get_valid_ips(subnet)
    if not valid_ips:
        print("Error: No valid IP addresses to scan.")
        return

    for port in unique_ports:
        for ip in valid_ips:
            if check_port(ip, int(port)):
                print(f"Port {port} is open on {ip}")
                # Log the result in the system log here
            else:
                print(f"Port {port} is closed on {ip}")

if __name__ == "__main__":
    main()
