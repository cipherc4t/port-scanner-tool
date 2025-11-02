#!/usr/bin/env python3
"""
Simple Port Scanner
Author: cipherc4t
Purpose: Educational port scanning tool for network reconnaissance
"""

import socket
import sys
from datetime import datetime

def scan_port(host, port):
    """
    Attempt to connect to a specific port on target host.
    
    Args:
        host: IP address or hostname to scan
        port: Port number to scan
    
    Returns:
        True if port is open, False otherwise
    """
    try:
        # Create a TCP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Set timeout to 0.5 seconds (prevents hanging)
        sock.settimeout(0.5)
        
        # Attempt to connect
        result = sock.connect_ex((host, port))
        
        # Close the socket
        sock.close()
        
        # If result is 0, connection was successful (port open)
        return result == 0
    
    except socket.gaierror:
        print(f"[-] Error: Cannot resolve hostname {host}")
        return False
    except socket.error:
        print(f"[-] Error: Cannot connect to {host}")
        return False


def main():
    """Main scanner function"""
    
    # Input validation
    if len(sys.argv) < 2:
        print("Usage: python3 port_scanner.py <host> [start_port] [end_port]")
        print("Example: python3 port_scanner.py 127.0.0.1 20 100")
        sys.exit(1)
    
    # Get host from command line
    host = sys.argv[1]
    
    # Get port range (default: 1-1000)
    start_port = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    end_port = int(sys.argv[3]) if len(sys.argv) > 3 else 1000
    
    # Validate port range
    if start_port < 1 or end_port > 65535 or start_port > end_port:
        print("[-] Invalid port range. Ports must be between 1 and 65535")
        sys.exit(1)
    
    # Resolve hostname to IP
    try:
        target_ip = socket.gethostbyname(host)
    except socket.gaierror:
        print(f"[-] Cannot resolve hostname: {host}")
        sys.exit(1)
    
    # Print banner
    print("=" * 60)
    print(f"[*] Scanning target: {host} ({target_ip})")
    print(f"[*] Port range: {start_port}-{end_port}")
    print(f"[*] Scan started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    open_ports = []
    
    # Scan each port
    for port in range(start_port, end_port + 1):
        if scan_port(target_ip, port):
            print(f"[+] Port {port}: OPEN")
            open_ports.append(port)
    
    # Print results summary
    print("=" * 60)
    if open_ports:
        print(f"[+] Found {len(open_ports)} open port(s):")
        for port in open_ports:
            print(f"    - Port {port}")
    else:
        print("[-] No open ports found")
    print(f"[*] Scan completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)


if __name__ == "__main__":
    main()
