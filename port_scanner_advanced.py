#!/usr/bin/env python3
"""
Advanced Port Scanner with Multi-threading
Author: cipherc4t
Purpose: Fast port scanning using concurrent threads
"""

import socket
import sys
import threading
from datetime import datetime
from queue import Queue

# Global lock for thread-safe printing
print_lock = threading.Lock()

class PortScanner:
    """Port scanner class with multi-threading support"""
    
    def __init__(self, host, start_port, end_port, num_threads=50):
        """
        Initialize scanner.
        
        Args:
            host: Target hostname/IP
            start_port: Starting port number
            end_port: Ending port number
            num_threads: Number of scanning threads
        """
        self.host = host
        self.start_port = start_port
        self.end_port = end_port
        self.num_threads = num_threads
        self.open_ports = []
        self.target_ip = None
    
    def resolve_host(self):
        """Resolve hostname to IP address"""
        try:
            self.target_ip = socket.gethostbyname(self.host)
            return True
        except socket.gaierror:
            print(f"[-] Cannot resolve hostname: {self.host}")
            return False
    
    def scan_port(self, port):
        """
        Scan a single port.
        
        Args:
            port: Port number to scan
        
        Returns:
            True if port is open, False otherwise
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.3)
            result = sock.connect_ex((self.target_ip, port))
            sock.close()
            return result == 0
        except:
            return False
    
    def worker(self, queue):
        """
        Worker thread that processes ports from queue.
        
        Args:
            queue: Queue containing port numbers
        """
        while True:
            port = queue.get()
            if port is None:
                break
            
            if self.scan_port(port):
                with print_lock:
                    print(f"[+] Port {port}: OPEN")
                self.open_ports.append(port)
            
            queue.task_done()
    
    def run(self):
        """Run the scanner"""
        if not self.resolve_host():
            return False
        
        # Print banner
        print("=" * 60)
        print(f"[*] Target: {self.host} ({self.target_ip})")
        print(f"[*] Port Range: {self.start_port}-{self.end_port}")
        print(f"[*] Threads: {self.num_threads}")
        print(f"[*] Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        # Create queue and add ports
        queue = Queue()
        for port in range(self.start_port, self.end_port + 1):
            queue.put(port)
        
        # Create and start threads
        threads = []
        for _ in range(self.num_threads):
            thread = threading.Thread(target=self.worker, args=(queue,))
            thread.daemon = True
            thread.start()
            threads.append(thread)
        
        # Wait for queue to be processed
        queue.join()
        
        # Stop workers
        for _ in range(self.num_threads):
            queue.put(None)
        
        for thread in threads:
            thread.join()
        
        # Print results
        print("=" * 60)
        if self.open_ports:
            print(f"[+] Found {len(self.open_ports)} open port(s):")
            for port in sorted(self.open_ports):
                print(f"    - Port {port}")
        else:
            print("[-] No open ports found")
        print(f"[*] Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        return True


def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage: python3 port_scanner_advanced.py <host> [start_port] [end_port] [threads]")
        print("Example: python3 port_scanner_advanced.py 127.0.0.1 1 1000 100")
        sys.exit(1)
    
    host = sys.argv[1]
    start_port = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    end_port = int(sys.argv[3]) if len(sys.argv) > 3 else 1000
    num_threads = int(sys.argv[4]) if len(sys.argv) > 4 else 50
    
    # Validate inputs
    if start_port < 1 or end_port > 65535 or start_port > end_port:
        print("[-] Invalid port range")
        sys.exit(1)
    
    # Create and run scanner
    scanner = PortScanner(host, start_port, end_port, num_threads)
    scanner.run()


if __name__ == "__main__":
    main()
