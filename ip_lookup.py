import requests

def get_ip_info(ip):
    response = requests.get(f"https://ipinfo.io/{ip}/json")
    return response.json()

if __name__ == "__main__":
    ip = input("Enter IP address: ")
    info = get_ip_info(ip)
    for key, value in info.items():
        print(f"{key}: {value}")
