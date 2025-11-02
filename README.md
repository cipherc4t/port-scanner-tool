# port-scanner-tool
python based port scanner

# Port Scanner Tool

## Description
A multi-threaded port scanner written in Python for network reconnaissance and security assessment.

## Features
- **Simple version**: Sequential port scanning (educational)
- **Advanced version**: Multi-threaded concurrent scanning (fast)
- **Hostname resolution**: Works with domain names and IPs
- **Customizable**: Port range and thread count configurable
- **Error handling**: Graceful handling of network errors

## Installation
No external dependencies required
Built-in socket module
python3 --version # Ensure Python 3.x installed

## Usage

### Simple Scanner
python3 port_scanner.py <target> [start_port] [end_port]

### Advanced Scanner (Recommended)
python3 port_scanner_advanced.py <target> [start_port] [end_port] [threads]
## Examples

Scan localhost, ports 1-100:
python3 port_scanner_advanced.py 127.0.0.1 1 100 50

Scan with 100 threads:
python3 port_scanner_advanced.py 192.168.1.1 1 1000 100


## How It Works

1. **Hostname Resolution**: Converts domain to IP
2. **Thread Pool Creation**: Creates N worker threads
3. **Port Distribution**: Assigns ports to queue
4. **Concurrent Scanning**: Each thread attempts connection
5. **Result Collection**: Open ports recorded and displayed

## Performance

| Version | Ports | Time | Speed |
|---------|-------|------|-------|
| Sequential | 500 | ~250s | 2 ports/sec |
| Multi-threaded (50) | 500 | ~10s | 50 ports/sec |
| Multi-threaded (100) | 500 | ~5s | 100 ports/sec |

**Result: 25-50x performance improvement with threading**

## Security Note

Only scan networks you own or have explicit permission to scan. Unauthorized port scanning may be illegal.

## Learning Outcomes

✓ TCP/IP protocol understanding
✓ Python socket programming
✓ Multi-threading concepts
✓ Network security fundamentals
✓ Performance optimization

---

Author: cipherc4t
Date: Nov 2, 2025
