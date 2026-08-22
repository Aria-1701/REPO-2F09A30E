import socket
# Code for Port Scanner implemented hereimport socket
import argparse
import sys
from datetime import datetime

def grab_banner(ip, port):
    """
    تحاول هذه الدالة سحب الـ Banner (معلومات الخدمة) من المنفذ المفتوح.
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        sock.connect((ip, port))
        
        # بعض الخدمات مثل الويب تحتاج لطلب مبدئي لترد
        if port in [80, 443, 8080]:
            sock.send(b"HEAD / HTTP/1.0\r\n\r\n")
            
        banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
        sock.close()
        
        # إرجاع أول السطور من الرد
        if banner:
            return banner.split('\n')[0][:60]
        return "Unknown Service"
    except:
        return "No Banner Grabbed"

def port_scanner(target_ip, ports):
    print("-" * 50)
    print(f"[*] Scanning Target: {target_ip}")
    print(f"[*] Scan Started At: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 50)
    
    open_ports_count = 0
    
    try:
        for port in ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1) # مهلة ثانية واحدة لتسريع الفحص
            result = sock.connect_ex((target_ip, port))
            
            if result == 0:
                open_ports_count += 1
                print(f"[+] Port {port}/tcp : OPEN")
                
                # استدعاء دالة تحديد الخدمة
                service_info = grab_banner(target_ip, port)
                print(f"    └─ Service: {service_info}")
                
            sock.close()
            
    except KeyboardInterrupt:
        print("\n[!] Scan stopped by user.")
        sys.exit()
    except socket.error:
        print("\n[-] Could not connect to server.")
        sys.exit()
        
    print("-" * 50)
    print(f"[*] Scan Completed. Found {open_ports_count} open ports.")

if __name__ == "__main__":
    # تجهيز الأداة لاستقبال المدخلات من الـ Terminal
    parser = argparse.ArgumentParser(description="Simple Network Port Scanner with Service Detection")
    parser.add_argument("-t", "--target", help="Target IP address", required=True)
    parser.add_argument("-p", "--ports", help="Ports to scan (comma separated, e.g., 21,22,80)", default="21,22,23,25,53,80,110,135,139,143,443,445,993,995,1723,3306,3389,5900,8080")
    
    args = parser.parse_args()
    
    target = args.target
    # تحويل البورتات المدخلة إلى قائمة أرقام
    ports_list = [int(p.strip()) for p in args.ports.split(',')]
    
    port_scanner(target, ports_list)