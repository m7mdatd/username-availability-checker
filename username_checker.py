#!/usr/bin/env python3
"""
Username Availability Checker
أداة لفحص توفر أسماء المستخدمين عبر منصات متعددة

الاستخدام:
    python3 username_checker.py <username>
    python3 username_checker.py -f usernames.txt
    python3 username_checker.py -i  # للوضع التفاعلي

المؤلف: Kali Security Tools
الإصدار: 1.0
"""

import requests
import sys
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse
from urllib.parse import quote
import json

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

class UsernameChecker:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # قائمة المنصات مع معلومات الفحص
        self.platforms = {
            'GitHub': {
                'url': 'https://github.com/{}',
                'method': 'GET',
                'available_indicators': ['404'],
                'taken_indicators': ['200'],
                'error_indicators': ['429', '503']
            },
            'Twitter/X': {
                'url': 'https://twitter.com/{}',
                'method': 'GET',
                'available_indicators': ['This account doesn\'t exist'],
                'taken_indicators': ['200'],
                'error_indicators': ['429', '503']
            },
            'Instagram': {
                'url': 'https://www.instagram.com/{}/',
                'method': 'GET',
                'available_indicators': ['Sorry, this page isn\'t available'],
                'taken_indicators': ['200'],
                'error_indicators': ['429', '503']
            },
            'LinkedIn': {
                'url': 'https://www.linkedin.com/in/{}',
                'method': 'GET',
                'available_indicators': ['404'],
                'taken_indicators': ['200'],
                'error_indicators': ['429', '503']
            },
            'YouTube': {
                'url': 'https://www.youtube.com/@{}',
                'method': 'GET',
                'available_indicators': ['404'],
                'taken_indicators': ['200'],
                'error_indicators': ['429', '503']
            },
            'TikTok': {
                'url': 'https://www.tiktok.com/@{}',
                'method': 'GET',
                'available_indicators': ['Couldn\'t find this account'],
                'taken_indicators': ['200'],
                'error_indicators': ['429', '503']
            },
            'Reddit': {
                'url': 'https://www.reddit.com/user/{}',
                'method': 'GET',
                'available_indicators': ['404'],
                'taken_indicators': ['200'],
                'error_indicators': ['429', '503']
            },
            'Medium': {
                'url': 'https://medium.com/@{}',
                'method': 'GET',
                'available_indicators': ['404'],
                'taken_indicators': ['200'],
                'error_indicators': ['429', '503']
            },
            'Telegram': {
                'url': 'https://t.me/{}',
                'method': 'GET',
                'available_indicators': ['If you have <strong>Telegram</strong>'],
                'taken_indicators': ['200'],
                'error_indicators': ['429', '503']
            },
            'Discord': {
                'url': 'https://discord.com/users/{}',
                'method': 'GET',
                'available_indicators': ['404'],
                'taken_indicators': ['200'],
                'error_indicators': ['429', '503']
            },
            'Pinterest': {
                'url': 'https://www.pinterest.com/{}',
                'method': 'GET',
                'available_indicators': ['404'],
                'taken_indicators': ['200'],
                'error_indicators': ['429', '503']
            },
            'Snapchat': {
                'url': 'https://www.snapchat.com/add/{}',
                'method': 'GET',
                'available_indicators': ['404'],
                'taken_indicators': ['200'],
                'error_indicators': ['429', '503']
            }
        }
        
        self.results = {}
        self.timeout = 10

    def print_banner(self):
        banner = f"""
{Colors.CYAN}{Colors.BOLD}
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
{Colors.END}
{Colors.GREEN}╔════════════════════════════════════════════════════════════════════════════════╗
║                          🔍 USERNAME AVAILABILITY CHECKER 🔍                   ║
║                                                                                ║
║  {Colors.CYAN}Developer:{Colors.GREEN} @m7mdatd                    {Colors.CYAN}Email:{Colors.GREEN} m@twal.sa                      ║
║  {Colors.CYAN}GitHub:{Colors.GREEN} github.com/m7mdatd             {Colors.CYAN}Twitter:{Colors.GREEN} @m7mdatd                    ║
║                                                                                ║
║  {Colors.YELLOW}🎯 Multi-Platform Username Checker for Digital Investigation & OSINT{Colors.GREEN}        ║
╚════════════════════════════════════════════════════════════════════════════════╝{Colors.END}

{Colors.PURPLE}▶ {Colors.BOLD}Scanning {len(self.platforms)} platforms:{Colors.END} {Colors.WHITE}{', '.join(list(self.platforms.keys())[:6])}...{Colors.END}
{Colors.PURPLE}▶ {Colors.BOLD}Features:{Colors.END} {Colors.WHITE}Concurrent Processing | JSON Export | Interactive Mode{Colors.END}
{Colors.PURPLE}▶ {Colors.BOLD}Use Cases:{Colors.END} {Colors.WHITE}OSINT | Penetration Testing | Brand Protection{Colors.END}

{Colors.CYAN}{'='*80}{Colors.END}
"""
        print(banner)

    def check_platform(self, platform, username):
        """فحص توفر اسم المستخدم في منصة واحدة"""
        try:
            url = self.platforms[platform]['url'].format(quote(username))
            
            response = self.session.get(url, timeout=self.timeout, allow_redirects=True)
            status_code = str(response.status_code)
            content = response.text.lower()
            
            # فحص المؤشرات
            if any(indicator in content.lower() for indicator in self.platforms[platform]['available_indicators']) or status_code == '404':
                return 'متاح'
            elif status_code in self.platforms[platform]['error_indicators']:
                return 'خطأ'
            elif status_code == '200':
                return 'مأخوذ'
            else:
                return 'غير محدد'
                
        except requests.exceptions.Timeout:
            return 'انتهت المهلة'
        except requests.exceptions.RequestException:
            return 'خطأ في الاتصال'
        except Exception as e:
            return f'خطأ: {str(e)[:20]}'

    def check_username(self, username):
        """فحص اسم المستخدم عبر جميع المنصات"""
        print(f"\n{Colors.BOLD}[+] فحص اسم المستخدم: {Colors.CYAN}{username}{Colors.END}")
        print(f"{Colors.YELLOW}{'='*50}{Colors.END}")
        
        results = {}
        
        # استخدام threading لتسريع العملية
        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_platform = {
                executor.submit(self.check_platform, platform, username): platform 
                for platform in self.platforms
            }
            
            for future in as_completed(future_to_platform):
                platform = future_to_platform[future]
                try:
                    result = future.result()
                    results[platform] = result
                    
                    # طباعة النتيجة مع التلوين
                    if result == 'متاح':
                        color = Colors.GREEN
                        symbol = '✓'
                    elif result == 'مأخوذ':
                        color = Colors.RED
                        symbol = '✗'
                    elif result == 'خطأ' or 'خطأ' in result:
                        color = Colors.YELLOW
                        symbol = '⚠'
                    else:
                        color = Colors.PURPLE
                        symbol = '?'
                    
                    print(f"{color}[{symbol}] {platform:<12} : {result}{Colors.END}")
                    
                except Exception as e:
                    results[platform] = f'خطأ: {str(e)[:20]}'
                    print(f"{Colors.RED}[!] {platform:<12} : خطأ في الفحص{Colors.END}")
        
        return results

    def save_results(self, username, results):
        """حفظ النتائج في ملف JSON"""
        filename = f"username_check_{username}_{int(time.time())}.json"
        data = {
            'username': username,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'results': results
        }
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"\n{Colors.GREEN}[+] تم حفظ النتائج في: {filename}{Colors.END}")
        except Exception as e:
            print(f"{Colors.RED}[!] خطأ في حفظ الملف: {e}{Colors.END}")

    def print_summary(self, results):
        """طباعة ملخص النتائج"""
        available = sum(1 for r in results.values() if r == 'متاح')
        taken = sum(1 for r in results.values() if r == 'مأخوذ')
        errors = sum(1 for r in results.values() if 'خطأ' in r or r in ['انتهت المهلة', 'خطأ في الاتصال'])
        
        print(f"\n{Colors.BOLD}ملخص النتائج:{Colors.END}")
        print(f"{Colors.GREEN}متاح: {available}{Colors.END}")
        print(f"{Colors.RED}مأخوذ: {taken}{Colors.END}")
        print(f"{Colors.YELLOW}أخطاء: {errors}{Colors.END}")

    def check_multiple_usernames(self, usernames):
        """فحص عدة أسماء مستخدمين"""
        all_results = {}
        
        for username in usernames:
            if username.strip():
                results = self.check_username(username.strip())
                all_results[username.strip()] = results
                self.print_summary(results)
                time.sleep(1)  # تأخير بسيط بين الفحوصات
        
        return all_results

    def interactive_mode(self):
        """الوضع التفاعلي"""
        print(f"{Colors.CYAN}[INFO] الوضع التفاعلي - اكتب 'exit' للخروج{Colors.END}")
        
        while True:
            try:
                username = input(f"\n{Colors.BOLD}أدخل اسم المستخدم: {Colors.END}").strip()
                
                if username.lower() in ['exit', 'quit', 'خروج']:
                    print(f"{Colors.GREEN}[+] شكراً لاستخدام الأداة!{Colors.END}")
                    break
                
                if not username:
                    continue
                
                results = self.check_username(username)
                self.print_summary(results)
                
                save = input(f"\n{Colors.YELLOW}هل تريد حفظ النتائج؟ (y/n): {Colors.END}").strip().lower()
                if save in ['y', 'yes', 'نعم']:
                    self.save_results(username, results)
                    
            except KeyboardInterrupt:
                print(f"\n{Colors.RED}[!] تم إيقاف البرنامج{Colors.END}")
                break

def main():
    parser = argparse.ArgumentParser(
        description='أداة فحص توفر أسماء المستخدمين عبر منصات متعددة',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
أمثلة على الاستخدام:
  python3 username_checker.py john_doe
  python3 username_checker.py -f usernames.txt
  python3 username_checker.py -i
  python3 username_checker.py -u user1,user2,user3
        """
    )
    
    parser.add_argument('username', nargs='?', help='اسم المستخدم المراد فحصه')
    parser.add_argument('-f', '--file', help='ملف يحتوي على قائمة أسماء المستخدمين')
    parser.add_argument('-u', '--usernames', help='قائمة أسماء المستخدمين مفصولة بفواصل')
    parser.add_argument('-i', '--interactive', action='store_true', help='الوضع التفاعلي')
    parser.add_argument('-s', '--save', action='store_true', help='حفظ النتائج تلقائياً')
    parser.add_argument('-t', '--timeout', type=int, default=10, help='مهلة الاتصال بالثواني (افتراضي: 10)')
    
    args = parser.parse_args()
    
    checker = UsernameChecker()
    checker.timeout = args.timeout
    checker.print_banner()
    
    try:
        if args.interactive:
            checker.interactive_mode()
        elif args.file:
            try:
                with open(args.file, 'r', encoding='utf-8') as f:
                    usernames = [line.strip() for line in f if line.strip()]
                
                if usernames:
                    results = checker.check_multiple_usernames(usernames)
                    if args.save:
                        for username, result in results.items():
                            checker.save_results(username, result)
                else:
                    print(f"{Colors.RED}[!] الملف فارغ أو لا يحتوي على أسماء مستخدمين صالحة{Colors.END}")
                    
            except FileNotFoundError:
                print(f"{Colors.RED}[!] لم يتم العثور على الملف: {args.file}{Colors.END}")
                sys.exit(1)
                
        elif args.usernames:
            usernames = [u.strip() for u in args.usernames.split(',') if u.strip()]
            results = checker.check_multiple_usernames(usernames)
            if args.save:
                for username, result in results.items():
                    checker.save_results(username, result)
                    
        elif args.username:
            results = checker.check_username(args.username)
            checker.print_summary(results)
            if args.save:
                checker.save_results(args.username, results)
        else:
            parser.print_help()
            
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}[!] تم إيقاف البرنامج بواسطة المستخدم{Colors.END}")
        sys.exit(1)

if __name__ == '__main__':
    main()
