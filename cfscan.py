import dns.resolver
import socket
from urllib.parse import urlparse
import argparse
import requests
from prettytable import PrettyTable

def print_banner():
    banner = """
 .d8888b.  8888888888 .d8888b.                            
d88P  Y88b 888       d88P  Y88b                           
888    888 888       Y88b.                                
888        8888888    "Y888b.    .d8888b  8888b.  88888b. 
888        888           "Y88b. d88P"        "88b 888 "88b
888    888 888             "888 888      .d888888 888  888
Y88b  d88P 888       Y88b  d88P Y88b.    888  888 888  888
 "Y8888P"  888        "Y8888P"   "Y8888P "Y888888 888  888
"""
    author = "Author: Raleigh Guevarra"
    version = "Version: 1.0"
    print(banner)
    print(author)
    print(version)
    print("\n")

def fetch_cloudflare_ips():
    urls = [
        "https://www.cloudflare.com/ips-v4",
        "https://www.cloudflare.com/ips-v6"
    ]
    ip_ranges = []
    for url in urls:
        response = requests.get(url)
        if response.status_code == 200:
            ip_ranges.extend(response.text.splitlines())
    return ip_ranges

def is_cloudflare_nameserver(ns):
    return "cloudflare" in ns.lower()

def is_behind_cloudflare(url, ip_ranges):
    try:
        parsed_url = urlparse(url)
        hostname = parsed_url.netloc or parsed_url.path

        answers = dns.resolver.resolve(hostname, 'A')
        for rdata in answers:
            ip = rdata.to_text()
            if ip in ip_ranges:
                return True, "Resolved IP belongs to Cloudflare"

        ns_answers = dns.resolver.resolve(hostname, 'NS')
        for rdata in ns_answers:
            ns = rdata.to_text()
            if is_cloudflare_nameserver(ns):
                return True, "Uses Cloudflare NS"

    except Exception as e:
        return False, str(e)
    return False, "Not behind Cloudflare"

def check_single_url(url, ip_ranges):
    table = PrettyTable()
    table.field_names = ["URL", "Status", "Detail"]
    result, detail = is_behind_cloudflare(url, ip_ranges)
    status = "Behind Cloudflare" if result else "Not behind Cloudflare"
    table.add_row([url, status, detail])
    print(table)

def process_urls_from_file(file_path, ip_ranges):
    table = PrettyTable()
    table.field_names = ["URL", "Status", "Detail"]
    with open(file_path, 'r') as file:
        for line in file:
            url = line.strip()
            if url:
                result, detail = is_behind_cloudflare(url, ip_ranges)
                status = "Behind Cloudflare" if result else "Not behind Cloudflare"
                table.add_row([url, status, detail])
    print(table)

def main():
    print_banner()

    parser = argparse.ArgumentParser(description="Check if a website is behind Cloudflare.")
    parser.add_argument("-u", "--url", help="URL to check.")
    parser.add_argument("-f", "--file", help="File containing URLs to check.")
    args = parser.parse_args()

    ip_ranges = fetch_cloudflare_ips()

    if args.url:
        check_single_url(args.url, ip_ranges)
    elif args.file:
        process_urls_from_file(args.file, ip_ranges)
    else:
        print("No URL or file provided. Use -u for a single URL or -f for a file.")
        print("Example syntax for a single URL: python script.py -u http://example.com")
        print("Example syntax for a file: python script.py -f urls.txt")

if __name__ == "__main__":
    main()