# Cloudflare Checker

This Python script checks if a website or websites listed in a file are behind the Cloudflare network by analyzing their DNS records and IP addresses. It allows for scanning a single URL or multiple URLs from a file.

## Features

- Fetches the latest Cloudflare IP ranges directly from Cloudflare.
- Identifies Cloudflare nameservers based on naming conventions.
- Supports checking a single URL or multiple URLs from a provided text file.
- Displays results in an ASCII table format for easy reading.

## Installation

Ensure you have Python 3.x installed and then follow these steps:

1. Clone this repository.
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Single URL

To check a single URL:

```bash
python cfscan.py -u https://example.com
```

### Multiple URLs

To check multiple URLs from a file:

```bash
python cfscan.py -f urls.txt
```

Ensure your `urls.txt` file contains one URL per line.

## Sample Output

### Single URL

```
+-------------------------+-----------------------+-------------------------------+
|           URL           |        Status         |             Detail            |
+-------------------------+-----------------------+-------------------------------+
| https://example.com     | Not behind Cloudflare | Not behind Cloudflare         |
+-------------------------+-----------------------+-------------------------------+
```

### Multiple URLs

```
+-------------------------+-----------------------+-------------------------------+
|           URL           |        Status         |             Detail            |
+-------------------------+-----------------------+-------------------------------+
| https://example.com     | Not behind Cloudflare | Not behind Cloudflare         |
| https://cloudflare.com  | Behind Cloudflare     | Uses Cloudflare NS            |
+-------------------------+-----------------------+-------------------------------+
```

## Author

Raleigh Guevarra

## Version

1.0

## License

This project is licensed under the MIT License.
