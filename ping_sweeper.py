import os
import platform

def ping_host(host):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    response = os.system(f"ping {param} 1 {host} > /dev/null 2>&1")
    return response == 0

if __name__ == "__main__":
    base_ip = input("Enter base IP (e.g., 192.168.1): ")
    for i in range(1, 255):
        ip = f"{base_ip}.{i}"
        if ping_host(ip):
            print(f"{ip} is online")
