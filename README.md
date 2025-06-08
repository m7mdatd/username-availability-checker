# Username Availability Checker

██╗   ██╗███████╗███████╗██████╗ ███╗   ██╗ █████╗ ███╗   ███╗███████╗
██║   ██║██╔════╝██╔════╝██╔══██╗████╗  ██║██╔══██╗████╗ ████║██╔════╝
██║   ██║███████╗█████╗  ██████╔╝██╔██╗ ██║███████║██╔████╔██║█████╗  
██║   ██║╚════██║██╔══╝  ██╔══██╗██║╚██╗██║██╔══██║██║╚██╔╝██║██╔══╝  
╚██████╔╝███████║███████╗██║  ██║██║ ╚████║██║  ██║██║ ╚═╝ ██║███████╗
 ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝
                                                                        
 █████╗ ██╗   ██╗ █████╗ ██╗██╗      █████╗ ██████╗ ██╗██╗     ██╗████████╗██╗   ██╗
██╔══██╗██║   ██║██╔══██╗██║██║     ██╔══██╗██╔══██╗██║██║     ██║╚══██╔══╝╚██╗ ██╔╝
███████║██║   ██║███████║██║██║     ███████║██████╔╝██║██║     ██║   ██║    ╚████╔╝ 
██╔══██║╚██╗ ██╔╝██╔══██║██║██║     ██╔══██║██╔══██╗██║██║     ██║   ██║     ╚██╔╝  
██║  ██║ ╚████╔╝ ██║  ██║██║███████╗██║  ██║██████╔╝██║███████╗██║   ██║      ██║   
╚═╝  ╚═╝  ╚═══╝  ╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝╚═════╝ ╚═╝╚══════╝╚═╝   ╚═╝      ╚═╝   
                                                                                      
 ██████╗██╗  ██╗███████╗ ██████╗██╗  ██╗███████╗██████╗ 
██╔════╝██║  ██║██╔════╝██╔════╝██║ ██╔╝██╔════╝██╔══██╗
██║     ███████║█████╗  ██║     █████╔╝ █████╗  ██████╔╝
██║     ██╔══██║██╔══╝  ██║     ██╔═██╗ ██╔══╝  ██╔══██╗
╚██████╗██║  ██║███████╗╚██████╗██║  ██╗███████╗██║  ██║
 ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝

A fast and efficient tool to check username availability across multiple social media platforms simultaneously. Perfect for digital investigations, OSINT, penetration testing, and personal branding.

## 🚀 Features

- **Multi-Platform Support**: Check availability across 12+ popular platforms
- **Concurrent Processing**: Fast parallel checking using threading
- **Multiple Input Methods**: Single username, file input, or interactive mode
- **Colored Output**: Easy-to-read results with color-coded status
- **JSON Export**: Save results for further analysis
- **Error Handling**: Robust handling of network issues and timeouts
- **Customizable Timeout**: Adjustable connection timeout settings

## 🎯 Supported Platforms

- **GitHub** - Code repositories and developer profiles
- **Twitter/X** - Social networking and microblogging
- **Instagram** - Photo and video sharing
- **LinkedIn** - Professional networking
- **YouTube** - Video sharing platform
- **TikTok** - Short-form video content
- **Reddit** - Social news aggregation
- **Medium** - Publishing platform
- **Telegram** - Messaging platform
- **Discord** - Gaming and community chat
- **Pinterest** - Visual discovery platform
- **Snapchat** - Multimedia messaging

## 📋 Requirements

- Python 3.6 or higher
- `requests` library

## 🔧 Installation

### Quick Install (Kali Linux / Debian / Ubuntu)

# Method 1: Using apt (Recommended)
sudo apt update
sudo apt install python3-requests

# Method 2: Using virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Method 3: Using pipx
sudo apt install pipx
pipx install requests

### Manual Installation

```bash
# Install Python dependencies
pip3 install requests

# Download the script
wget https://raw.githubusercontent.com/m7mdatd/username-availability-checker/main/username_checker.py

# Make executable
chmod +x username_checker.py
```

## 🚀 Usage

### Basic Usage

```bash
# Check single username
python3 username_checker.py john_doe

# Interactive mode
python3 username_checker.py -i

# Check multiple usernames
python3 username_checker.py -u user1,user2,user3

# Check usernames from file
python3 username_checker.py -f usernames.txt
```

### Advanced Options

```bash
# Save results automatically
python3 username_checker.py john_doe --save

# Custom timeout (default: 10 seconds)
python3 username_checker.py john_doe --timeout 15

# Help and options
python3 username_checker.py --help
```

### Input File Format

Create a text file with usernames (one per line):

```
john_doe
test_user
admin123
social_media_user
```

## 📊 Output Examples

### Single Username Check
```
[+] Checking username: john_doe
==================================================
[✓] GitHub       : Available
[✗] Twitter      : Taken
[✓] Instagram    : Available
[⚠] LinkedIn     : Connection Error
[✓] YouTube      : Available
[✗] TikTok       : Taken
...

Summary:
Available: 8
Taken: 3
Errors: 1
```

### Result Status Indicators

- ✅ **Available** - Username is not taken
- ❌ **Taken** - Username is already in use
- ⚠️ **Error** - Connection issue or platform unavailable
- ❓ **Unknown** - Unclear response from platform

## 🔍 Use Cases

### Security & Investigation
- **OSINT (Open Source Intelligence)**: Gather information from public sources
- **Digital Forensics**: Link accounts across platforms during investigations
- **Penetration Testing**: Understanding target's digital footprint
- **Threat Intelligence**: Tracking suspicious accounts

### Personal & Business
- **Brand Protection**: Ensure consistent username across platforms
- **Identity Management**: Check for impersonation or unauthorized use
- **Social Media Strategy**: Secure usernames before launching campaigns
- **Personal Branding**: Find available usernames for professional use

## 📁 Output Files

The tool can save results in JSON format:

```json
{
  "username": "john_doe",
  "timestamp": "2025-06-08 14:30:25",
  "results": {
    "GitHub": "Available",
    "Twitter": "Taken",
    "Instagram": "Available",
    ...
  }
}
```

## ⚡ Performance
- **Speed**: Checks 12+ platforms in under 30 seconds
- **Efficiency**: Concurrent requests using threading
- **Reliability**: Built-in error handling and retry mechanisms
- **Scalability**: Supports batch processing of multiple usernames

## 🛠️ Configuration

### Custom Timeout
```bash
python3 username_checker.py username --timeout 20
```

### Platform Selection
Edit the `platforms` dictionary in the script to add/remove platforms or modify checking logic.

## 🔐 Privacy & Ethics

- **Public Information Only**: Only checks publicly available information
- **Rate Limiting**: Built-in delays to respect platform policies
- **No Authentication**: Does not require login credentials
- **Responsible Use**: Intended for legitimate security and research purposes

## 🐛 Troubleshooting

### Common Issues

**Connection Timeouts:**
```bash
# Increase timeout value
python3 username_checker.py username --timeout 20
```

**Permission Denied:**
```bash
# Make script executable
chmod +x username_checker.py
```

**Module Not Found:**
```bash
# Install required dependencies
pip3 install requests
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup

```bash
# Fork the repository
git clone https://github.com/m7mdatd/username-availability-checker.git
cd username-availability-checker

# Create a feature branch
git checkout -b feature/new-platform

# Make your changes and test
python3 username_checker.py test_user

# Commit and push
git add .
git commit -m "Add new platform support"
git push origin feature/new-platform
```

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool is intended for educational, research, and legitimate security testing purposes only. Users are responsible for complying with applicable laws and platform terms of service. The authors are not responsible for any misuse or damage caused by this tool.

## 📞 Contact
- **Twitter/X**: [@m7mdatd](https://x.com/m7mdatd)
- **Email**: [m@twal.sa](mailto:m@twal.sa)
- **Issues**: [Report issues here](https://github.com/m7mdatd/username-availability-checker/issues)

## 🙏 Acknowledgments

- Thanks to all the open-source contributors
- Inspired by the cybersecurity and OSINT community
- Built for the Kali Linux ecosystem

---

**⭐ If you find this tool useful, please consider giving it a star!**
