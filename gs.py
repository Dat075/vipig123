import json
import requests, os, sys, re
from time import sleep
from datetime import datetime
import random
import time
import shutil
import traceback

# Thông tin phiên bản của tool
VERSION = "1.0.1"
GITHUB_RAW_URL = "https://raw.githubusercontent.com/Dat075/vipig123/refs/heads/main/gs.py"
GITHUB_VERSION_URL = "https://raw.githubusercontent.com/Dat075/vipig123/refs/heads/main/version.txt"
# Hệ thống kiểm tra cập nhật
def check_for_updates():
    """Kiểm tra phiên bản mới"""
    try:
        print("\033[1;33mĐang kiểm tra cập nhật...")
        response = requests.get(GITHUB_VERSION_URL, timeout=10)
        if response.status_code == 200:
            latest_version = response.text.strip()
            if latest_version != VERSION:
                return latest_version
        return None
    except Exception as e:
        print(f"\033[1;31mLỗi khi kiểm tra cập nhật: {e}")
        return None

def update_script():
    """Tải và cập nhật script"""
    try:
        print("\033[1;33mĐang tải phiên bản mới...")
        response = requests.get(GITHUB_RAW_URL, timeout=15)
        if response.status_code == 200:
            # Tạo backup của file cũ
            script_path = os.path.abspath(__file__)
            backup_path = script_path + ".bak"
            shutil.copy2(script_path, backup_path)
            
            # Ghi file mới
            with open(script_path, 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            print("\033[1;32mCập nhật thành công! Khởi động lại tool để áp dụng thay đổi.")
            return True
        else:
            print(f"\033[1;31mKhông thể tải phiên bản mới. Mã lỗi: {response.status_code}")
            return False
    except Exception as e:
        print(f"\033[1;31mLỗi trong quá trình cập nhật: {e}")
        return False

# Kiểm tra cập nhật khi khởi động
def check_update_on_startup():
    latest_version = check_for_updates()
    if latest_version:
        print(f"\033[1;33mCó phiên bản mới: {latest_version} (Phiên bản hiện tại: {VERSION})")
        choice = input("\033[1;97m[\033[1;91m❣\033[1;97m] \033[1;36m✈  \033[1;32mBạn có muốn cập nhật không? (y/n): \033[1;33m").lower()
        if choice == 'y':
            if update_script():
                print("\033[1;32mVui lòng khởi động lại tool để sử dụng phiên bản mới.")
                sys.exit(0)
        else:
            print("\033[1;33mTiếp tục sử dụng phiên bản cũ.")
    else:
        print(f"\033[1;32mBạn đang sử dụng phiên bản mới nhất: {VERSION}")

# Hệ thống quản lý cookie die
def mark_cookie_as_die(cookie):
    """Đánh dấu cookie là die để bỏ qua trong các lần chạy sau"""
    try:
        # Đọc file danh sách cookie die
        die_cookies = []
        if os.path.exists('cookie_die.txt'):
            with open('cookie_die.txt', 'r', encoding='utf-8') as f:
                die_cookies = [line.strip() for line in f.readlines() if line.strip()]
        
        # Kiểm tra xem cookie đã có trong danh sách chưa
        if cookie not in die_cookies:
            # Thêm cookie mới vào danh sách
            with open('cookie_die.txt', 'a', encoding='utf-8') as f:
                f.write(cookie + '\n')
            
            # Cập nhật file cookie chính bằng cách loại bỏ cookie die
            if os.path.exists('ck.txt'):
                with open('ck.txt', 'r', encoding='utf-8') as f:
                    live_cookies = [line.strip() for line in f.readlines() if line.strip() and line.strip() != cookie]
                
                with open('ck.txt', 'w', encoding='utf-8') as f:
                    for c in live_cookies:
                        f.write(c + '\n')
            
            print(f"\033[1;31mĐã đánh dấu cookie là die và loại bỏ khỏi danh sách")
            return True
    except Exception as e:
        print(f"\033[1;31mLỗi khi đánh dấu cookie die: {e}")
    return False

def is_cookie_die(cookie):
    """Kiểm tra xem cookie đã bị đánh dấu là die chưa"""
    try:
        if os.path.exists('cookie_die.txt'):
            with open('cookie_die.txt', 'r', encoding='utf-8') as f:
                die_cookies = [line.strip() for line in f.readlines()]
                return cookie in die_cookies
    except Exception as e:
        print(f"\033[1;31mLỗi khi kiểm tra cookie die: {e}")
    return False

# Menu quản lý cookie
def show_cookie_menu():
    print("\033[97m════════════════════════════════════════════════")
    print(f"{lam}QUẢN LÝ COOKIE{trang}")
    print(f"{luc}1. Xem danh sách cookie live")
    print(f"{luc}2. Xem danh sách cookie die")
    print(f"{luc}3. Xóa tất cả cookie die")
    print(f"{luc}4. Quay lại")
    print("\033[97m════════════════════════════════════════════════")
    
    choice = input('\033[1;97m[\033[1;91m❣\033[1;97m] \033[1;36m✈  \033[1;32mNhập lựa chọn của bạn:\033[1;33m ')
    
    if choice == '1':
        # Hiển thị danh sách cookie live
        if os.path.exists('ck.txt'):
            with open('ck.txt', 'r', encoding='utf-8') as f:
                cookies = f.read().splitlines()
            print(f"\033[1;32mCó {len(cookies)} cookie live:")
            for i, c in enumerate(cookies):
                print(f"{i+1}. {c[:30]}...")
        else:
            print("\033[1;31mKhông có file cookie!")
    
    elif choice == '2':
        # Hiển thị danh sách cookie die
        if os.path.exists('cookie_die.txt'):
            with open('cookie_die.txt', 'r', encoding='utf-8') as f:
                cookies = f.read().splitlines()
            print(f"\033[1;31mCó {len(cookies)} cookie die:")
            for i, c in enumerate(cookies):
                print(f"{i+1}. {c[:30]}...")
        else:
            print("\033[1;32mKhông có cookie die!")
    
    elif choice == '3':
        # Xóa tất cả cookie die
        if os.path.exists('cookie_die.txt'):
            os.remove('cookie_die.txt')
            print('\033[1;32mĐã xóa tất cả cookie die!')
        else:
            print("\033[1;32mKhông có file cookie die!")
    
    return

def banner():
    print("\033[97m════════════════════════════════════════════════")
    print(f"{lam}VipIG Tool{trang} - {cam}Phiên bản {VERSION}{trang}")
    print(f"{luc}Tự động nhiệm vụ Instagram thông qua VipIG{trang}")
    print("\033[97m════════════════════════════════════════════════")

den = '\x1b[1;90m'
luc = '\x1b[1;32m'
trang = '\x1b[1;37m'
red = '\x1b[1;31m'
vang = '\x1b[1;33m'
tim = '\x1b[1;35m'
lamd = '\x1b[1;34m'
lam = '\x1b[1;36m'
cam = '\x1b[38;5;208m'  # Thêm màu cam
hong = '\x1b[1;95m'
thanh_xau="\033[1;97m[\033[1;91m❣\033[1;97m] \033[1;36m✈  \033[1;32m"
thanh_dep="\033[1;97m[\033[1;91m❣\033[1;97m] \033[1;36m✈  \033[1;32m"

dem = 0

# Enhanced error handling for coin retrieval
def coin(ckvp):
    try:
        h_xu = {'user-agent':'Mozilla/5.0 (Linux; Android 11; Live 4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.28 Mobile Safari/537.36','cookie':ckvp}
        x = requests.post('https://vipig.net/home.php', headers=h_xu, timeout=10).text
        if '"soduchinh">' in x:
            xu = x.split('"soduchinh">')[1].split('<')[0]
            return xu
        return "0"
    except Exception as e:
        print(f"\033[1;31mLỗi khi lấy số xu: {e}")
        return "0"

# Improved cookie handling
def cookie(token):
    try:
        ck = requests.post('https://vipig.net/logintoken.php',headers={'Content-type':'application/x-www-form-urlencoded',},data={'access_token':token}, timeout=10)
        if ck.cookies and 'PHPSESSID' in ck.cookies:
            cookie = 'PHPSESSID='+(ck.cookies)['PHPSESSID']
            return cookie
        print("\033[1;31mKhông thể lấy cookie từ token")
        return None
    except Exception as e:
        print(f"\033[1;31mLỗi khi lấy cookie: {e}")
        return None

# Improved task retrieval with error handling
def get_nv(type, ckvp):
    try:
        headers={'content-type':'text/html; charset=UTF-8','accept':'application/json, text/javascript, */*; q=0.01','accept-language':'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5','referer':'https://vipig.net/kiemtien/','x-requested-with':'XMLHttpRequest','sec-ch-ua-mobile':'?1','user-agent':'Mozilla/5.0 (Linux; Android 11; vivo 1904) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Mobile Safari/537.36','sec-ch-ua-platform':'"Android"','sec-fetch-site':'same-origin','sec-fetch-mode':'cors','sec-fetch-dest':'empty','cookie':ckvp}
        response = requests.post(f'https://vipig.net/kiemtien{type}/getpost.php', headers=headers, timeout=15).json()
        return response
    except Exception as e:
        print(f"\033[1;31mLỗi khi lấy nhiệm vụ {type}: {e}")
        return []

# Improved reward claiming with error handling
def nhan_tien(list, ckvp, type):
    try:
        data_xu='id='+str(list)
        data_nhan=str(len(data_xu))
        headers={'content-length':data_nhan,'sec-ch-ua':'"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"','content-type':'application/x-www-form-urlencoded; charset=UTF-8','accept':'*/*','user-agent':'Mozilla/5.0 (Linux; Android 11; vivo 1904) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Mobile Safari/537.36','sec-ch-ua-mobile':'?1','x-requested-with':'XMLHttpRequest','sec-fetch-site':'same-origin','origin':'https://vipig.net','sec-ch-ua-platform':'"Android"','sec-fetch-mode':'cors','sec-fetch-dest':'empty','referer':'https://vipig.net/kiemtien'+type+'/','accept-language':'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5','cookie':ckvp}
        a = requests.post(f'https://vipig.net/kiemtien{type}/nhantien.php',headers=headers,data=data_xu, timeout=15).text
        return a
    except Exception as e:
        print(f"\033[1;31mLỗi khi nhận tiền: {e}")
        return "error"

# Improved subscription reward claiming
def nhan_sub(list, ckvp):
    try:
        data_xu='id='+str(list[0:len(list)-1])
        data_nhan=str(len(data_xu))
        headers={'content-length':data_nhan,'sec-ch-ua':'"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"','content-type':'application/x-www-form-urlencoded; charset=UTF-8','accept':'*/*','user-agent':'Mozilla/5.0 (Linux; Android 11; vivo 1904) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Mobile Safari/537.36','sec-ch-ua-mobile':'?1','x-requested-with':'XMLHttpRequest','sec-fetch-site':'same-origin','origin':'https://vipig.net','sec-ch-ua-platform':'"Android"','sec-fetch-mode':'cors','sec-fetch-dest':'empty','referer':'https://vipig.net/kiemtien/subcheo','accept-language':'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5','cookie':ckvp}
        response = requests.post('https://vipig.net/kiemtien/subcheo/nhantien2.php',headers=headers,data=data_xu, timeout=15)
        if response.status_code == 200:
            try:
                return response.json()
            except:
                print("\033[1;31mLỗi khi xử lý phản hồi JSON")
                return {"error": "Invalid JSON"}
        else:
            print(f"\033[1;31mLỗi HTTP: {response.status_code}")
            return {"error": f"HTTP error {response.status_code}"}
    except Exception as e:
        print(f"\033[1;31mLỗi khi nhận sub: {e}")
        return {"error": str(e)}

# Enhanced delay function with reduced time
def delay(dl):
    try:
        # Giảm thời gian delay xuống một nửa để tăng tốc độ làm nhiệm vụ
        actual_delay = max(1, int(dl/2))
        for i in range(actual_delay, -1, -1):
            print('[AN ORIN]['+str(i)+' Giây]           ',end='\r')
            sleep(0.8)  # Giảm thời gian sleep giữa mỗi lần đếm
    except KeyboardInterrupt:
        print("\n\033[1;31mĐã dừng delay bởi người dùng")
    except Exception as e:
        print(f"\n\033[1;31mLỗi trong quá trình delay: {e}")
        sleep(actual_delay)
        print(actual_delay,end='\r')

# Better adaptive delay with backoff
def delay_with_backoff(attempts, base_delay=5):
    try:
        # Giảm thời gian backoff xuống để tăng tốc độ
        delay_time = base_delay * (1.3 ** min(attempts, 5))
        delay_time = min(delay_time, 30)  # Giảm cap xuống 30 giây
        for i in range(int(delay_time), -1, -1):
            print(f'[AN ORIN][Đang nghỉ {i} Giây để tránh block]           ',end='\r')
            sleep(0.8)
    except KeyboardInterrupt:
        print("\n\033[1;31mĐã dừng delay bởi người dùng")
    except Exception as e:
        print(f"\n\033[1;31mLỗi trong quá trình adaptive delay: {e}")
        sleep(base_delay)

# Improved cookie info saving
def save_cookie_info(cookie_info):
    try:
        file_path = 'cookie_storage.json'
        data = []
        
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except json.JSONDecodeError:
                data = []
                print("\033[1;31mFile JSON lỗi, tạo mới danh sách cookie")
        
        # Check if cookie already exists
        for i, item in enumerate(data):
            if item.get('cookie') == cookie_info.get('cookie'):
                data[i] = cookie_info
                break
        else:
            data.append(cookie_info)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
        return True
    except Exception as e:
        print(f"\033[1;31mLỗi khi lưu thông tin cookie: {e}")
        return False

# Improved Instagram username retrieval with proper retries and error handling
def name(cookie, retries=3):
    # Kiểm tra trước xem cookie đã bị đánh dấu là die chưa
    if is_cookie_die(cookie):
        print(f"\033[1;31mCookie đã bị đánh dấu là die từ trước")
        return 'die', 'die'
    
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
    
    # Xử lý useragent trong cookie an toàn hơn
    if 'useragent=' in cookie:
        try:
            parts = cookie.split('useragent=')
            if len(parts) > 1:
                ua_parts = parts[1].split(';')
                if ua_parts:
                    user_agent = ua_parts[0]
        except Exception:
            pass
    
    # Xử lý user_id trong cookie an toàn hơn
    try:
        parts = cookie.split('ds_user_id=')
        if len(parts) < 2:
            print("\033[1;31mKhông tìm thấy ds_user_id trong cookie")
            mark_cookie_as_die(cookie)
            return 'die', 'die'
        
        id_parts = parts[1].split(';')
        if not id_parts:
            print("\033[1;31mKhông thể trích xuất ds_user_id từ cookie")
            mark_cookie_as_die(cookie)
            return 'die', 'die'
            
        user_id = id_parts[0]
        if not user_id:
            print("\033[1;31mds_user_id trống")
            mark_cookie_as_die(cookie)
            return 'die', 'die'
    except Exception as e:
        print(f"\033[1;31mLỗi khi lấy user_id từ cookie: {e}")
        mark_cookie_as_die(cookie)
        return 'die', 'die'
    
    # Xử lý csrftoken trong cookie an toàn hơn
    csrf_token = ""
    if 'csrftoken=' in cookie:
        try:
            parts = cookie.split('csrftoken=')
            if len(parts) > 1:
                csrf_parts = parts[1].split(';')
                if csrf_parts:
                    csrf_token = csrf_parts[0]
        except Exception:
            pass
    
    headers = {
        'Host': 'i.instagram.com',
        'User-Agent': user_agent,
        'Accept': 'application/json',
        'X-IG-App-ID': '1217981644879628',
        'X-CSRFToken': csrf_token,
    }
    
    for attempt in range(retries):
        try:
            response = requests.get(f'https://i.instagram.com/api/v1/users/{user_id}/info/', 
                                   headers=headers, 
                                   cookies={'Cookie': cookie}, 
                                   timeout=15)
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if 'user' in data and 'username' in data['user'] and 'pk' in data['user']:
                        user = data['user']['username']
                        id = data['user']['pk']
                        
                        cookie_info = {
                            'cookie': cookie,
                            'username': user,
                            'user_id': id,
                            'status': 'live',
                            'last_checked': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        }
                        
                        save_cookie_info(cookie_info)
                        return user, id
                    else:
                        print("\033[1;31mPhản hồi thiếu thông tin user/username/pk")
                        mark_cookie_as_die(cookie)
                except json.JSONDecodeError:
                    print(f"\033[1;31mLỗi phân tích JSON: {response.text[:100]}...")
                    mark_cookie_as_die(cookie)
            
            elif response.status_code == 429:  # Too Many Requests
                print(f'\033[1;31m[429] Quá nhiều yêu cầu, thử lại sau {5 * (attempt + 1)} giây...')
                sleep(5 * (attempt + 1))
                continue
            else:
                print(f'\033[1;31m[Error] Status code: {response.status_code} - {response.text[:50]}...')
                mark_cookie_as_die(cookie)
        
        except requests.exceptions.RequestException as e:
            print(f'\033[1;31m[Lỗi mạng] {str(e)}, thử lại lần {attempt + 1}/{retries}...')
            if attempt < retries - 1:
                sleep(5)  # Delay trước khi thử lại
                continue
    
    # Nếu hết số lần thử mà vẫn lỗi
    cookie_info = {
        'cookie': cookie,
        'username': None,
        'user_id': None,
        'status': 'die',
        'last_checked': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    save_cookie_info(cookie_info)
    mark_cookie_as_die(cookie)
    return 'die', 'die'

# Improved file operations
def save_cookie_to_txt(cookie):
    try:
        # Kiểm tra xem cookie đã bị đánh dấu là die chưa
        if is_cookie_die(cookie):
            print(f"\033[1;31mKhông lưu cookie đã die")
            return False
            
        with open('ck.txt', 'a', encoding='utf-8') as f:
            f.write(cookie + '\n')
        return True
    except Exception as e:
        print(f"\033[1;31mLỗi khi lưu cookie vào file: {e}")
        return False

def clear_cookie_file():
    try:
        with open('ck.txt', 'w', encoding='utf-8') as f:
            f.write('')
        return True
    except Exception as e:
        print(f"\033[1;31mLỗi khi xóa file cookie: {e}")
        return False

def load_cookies_from_txt():
    live_cookies = []
    try:
        if os.path.exists('ck.txt'):
            with open('ck.txt', 'r', encoding='utf-8') as f:
                cookies = f.read().splitlines()
                
            for cookie in cookies:
                if cookie.strip():
                    # Kiểm tra xem cookie đã bị đánh dấu là die chưa
                    if is_cookie_die(cookie):
                        print(f'Cookie đã bị đánh dấu là die từ trước, bỏ qua')
                        continue
                    
                    try:
                        ten = name(cookie)
                        if ten[0] != 'die':
                            live_cookies.append(cookie)
                            print(f'User Instagram: {cam}{ten[0]}{trang} - Live')
                        else:
                            print(f'Cookie: {cookie[:20]}... - Die')
                            # Đánh dấu cookie là die
                            mark_cookie_as_die(cookie)
                    except Exception as e:
                        print(f"\033[1;31mLỗi khi kiểm tra cookie: {e}")
                        
            print(f'\033[1;97m[\033[1;91m❣\033[1;97m] \033[1;36m✈  \033[1;32mSố cookie còn live: \033[1;33m{len(live_cookies)}')
        return live_cookies
    except Exception as e:
        print(f"\033[1;31mLỗi khi đọc file cookie: {e}")
        return []

# Improved console formatting
def bongoc(so):
    try:
        a= "────"*so
        for i in range(len(a)):
            sys.stdout.write(a[i])
            sys.stdout.flush()
            sleep(0.003)
        print()
    except Exception as e:
        print(f"\033[1;31mLỗi khi in đường gạch ngang: {e}")
        print("────"*so)

# Improved Instagram interactions with better error handling
def like(id, cookie):
    try:
        # Kiểm tra xem cookie đã bị đánh dấu là die chưa
        if is_cookie_die(cookie):
            print(f"\033[1;31mKhông thể sử dụng cookie đã die")
            return '1'
            
        headers = {
            "x-ig-app-id": "1217981644879628",
            "x-asbd-id": "198387",
            "x-instagram-ajax": "c161aac700f",
            "accept": "*/*",
            "content-length": "0",
            "content-type": "application/x-www-form-urlencoded",
            "user-agent": "Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03S) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Safari/535.19",
            "x-csrftoken": cookie.split('csrftoken=')[1].split(';')[0] if 'csrftoken=' in cookie else "",
            "x-requested-with": "XMLHttpRequest",
            "cookie": cookie
        }
        
        response = requests.post(f'https://www.instagram.com/web/likes/{id}/like/', headers=headers, timeout=15)
        
        if response.status_code == 200:
            like_data = response.text
            if 'ok' not in like_data.lower():
                return '1'
            else:
                return '2'
        else:
            print(f"\033[1;31mLỗi khi like: HTTP {response.status_code}")
            return '1'
    except Exception as e:
        print(f"\033[1;31mLỗi trong quá trình like: {e}")
        return '1'

# Improved post ID extraction with safe parsing
def get_id(link, cookie):
    try:
        # Kiểm tra xem cookie đã bị đánh dấu là die chưa
        if is_cookie_die(cookie):
            print(f"\033[1;31mKhông thể sử dụng cookie đã die")
            return False
            
        headers = {
            "x-ig-app-id": "1217981644879628",
            "x-asbd-id": "198387",
            "x-instagram-ajax": "c161aac700f",
            "accept": "*/*",
            "content-length": "0",
            "content-type": "application/x-www-form-urlencoded",
            "user-agent": "Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03S) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Safari/535.19",
            "x-csrftoken": cookie.split('csrftoken=')[1].split(';')[0] if 'csrftoken=' in cookie else "",
            "x-requested-with": "XMLHttpRequest",
            "cookie": cookie
        }
        
        response = requests.get(link, headers=headers, timeout=15)
        
        if response.status_code == 200:
            a = response.text
            
            # Xử lý an toàn khi tìm ID
            if 'media?id=' not in a:
                print("\033[1;31mKhông tìm thấy ID trong phản hồi")
                return False
                
            try:
                parts = a.split('media?id=')
                if len(parts) < 2:
                    print("\033[1;31mKhông thể phân tích ID từ phản hồi")
                    return False
                    
                id_parts = parts[1].split('"')
                if not id_parts:
                    print("\033[1;31mKhông thể trích xuất ID từ phản hồi")
                    return False
                    
                id = id_parts[0]
                if not id:
                    print("\033[1;31mID trống")
                    return False
                    
                return id
            except Exception as e:
                print(f"\033[1;31mLỗi khi phân tích ID từ phản hồi: {e}")
                return False
        else:
            print(f"\033[1;31mLỗi khi lấy ID: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"\033[1;31mLỗi trong quá trình lấy ID: {e}")
        return False

# Improved follow function
def follow(id, cookie):
    try:
        # Kiểm tra xem cookie đã bị đánh dấu là die chưa
        if is_cookie_die(cookie):
            print(f"\033[1;31mKhông thể sử dụng cookie đã die")
            return '1'
            
        headers = {
            "x-ig-app-id": "1217981644879628",
            "x-asbd-id": "198387",
            "x-instagram-ajax": "c161aac700f",
            "accept": "*/*",
            "content-length": "0",
            "content-type": "application/x-www-form-urlencoded",
            "user-agent": "Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03S) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Safari/535.19",
            "x-csrftoken": cookie.split('csrftoken=')[1].split(';')[0] if 'csrftoken=' in cookie else "",
            "x-requested-with": "XMLHttpRequest",
            "cookie": cookie
        }
        
        response = requests.post(f"https://i.instagram.com/web/friendships/{id}/follow/", headers=headers, timeout=15)
        
        if response.status_code == 200:
            fl = response.text
            if 'ok' not in fl.lower():
                return '1'
            else:
                return fl
        else:
            print(f"\033[1;31mLỗi khi follow: HTTP {response.status_code}")
            return '1'
    except Exception as e:
        print(f"\033[1;31mLỗi trong quá trình follow: {e}")
        return '1'

# Improved comment function with better error handling
def cmt(msg, id, cookie):
    try:
        # Kiểm tra xem cookie đã bị đánh dấu là die chưa
        if is_cookie_die(cookie):
            print(f"\033[1;31mKhông thể sử dụng cookie đã die")
            return '1'
            
        headers = {
            "x-ig-app-id": "1217981644879628",
            "x-asbd-id": "198387",
            "x-instagram-ajax": "c161aac700f",
            "accept": "*/*",
            "content-type": "application/x-www-form-urlencoded",
            "user-agent": "Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03S) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Safari/535.19",
            "x-csrftoken": cookie.split('csrftoken=')[1].split(';')[0] if 'csrftoken=' in cookie else "",
            "x-requested-with": "XMLHttpRequest",
            "cookie": cookie
        }
        
        response = requests.post(f'https://i.instagram.com/api/v1/web/comments/{id}/add/', 
                               headers=headers, 
                               data={'comment_text': msg}, 
                               timeout=15)
        
        if response.status_code == 200:
            try:
                cmt_data = response.json()
                if 'status' in cmt_data and cmt_data['status'] == 'ok':
                    return 'ok'
                else:
                    print(f"\033[1;31mComment không thành công: {json.dumps(cmt_data)[:100]}...")
                    return cmt_data
            except json.JSONDecodeError:
                print(f"\033[1;31mLỗi phân tích JSON từ comment: {response.text[:100]}...")
                return '1'
        else:
            print(f"\033[1;31mLỗi khi comment: HTTP {response.status_code}")
            return '1'
    except Exception as e:
        print(f"\033[1;31mLỗi trong quá trình comment: {e}")
        return '1'

# Improved Instagram account configuration
def cau_hinh(id_ig, ckvp):
    try:
        headers={'content-length':'23','sec-ch-ua':'"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"','accept':'*/*','content-type':'application/x-www-form-urlencoded; charset=UTF-8','x-requested-with':'XMLHttpRequest','sec-ch-ua-mobile':'?1','user-agent':'Mozilla/5.0 (Linux; Android 11; vivo 1904) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Mobile Safari/537.36','sec-ch-ua-platform':'"Android"','sec-fetch-site':'same-origin','sec-fetch-mode':'cors','sec-fetch-dest':'empty','referer':'https://vipig.net/cauhinh/datnick.php','accept-language':'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5','cookie':ckvp}
        
        response = requests.post('https://vipig.net/cauhinh/datnick.php', 
                               headers=headers, 
                               data={'iddat[]': id_ig},
                               timeout=15)
        
        if response.status_code == 200:
            return response.text
        else:
            print(f"\033[1;31mLỗi khi cấu hình: HTTP {response.status_code}")
            return "error"
    except Exception as e:
        print(f"\033[1;31mLỗi trong quá trình cấu hình: {e}")
        return "error"

# Improved logging function
def log_action(action_type, id, status, message=""):
    try:
        tg = datetime.now().strftime('%H:%M:%S')
        log_entry = f"[{tg}] | {action_type} | {id} | {status}"
        if message:
            log_entry += f" | {message}"
        
        print(log_entry)
        
        # Optionally write to a log file
        with open("vipig_log.txt", "a", encoding="utf-8") as f:
            f.write(log_entry + "\n")
    except Exception as e:
        print(f"\033[1;31mLỗi khi ghi log: {e}")

# Function to check if cookie is valid
def check_cookie_valid(cookie):
    try:
        # Kiểm tra xem cookie đã bị đánh dấu là die chưa
        if is_cookie_die(cookie):
            return False
            
        user, id = name(cookie)
        if user == 'die' or id == 'die':
            return False
        return True
    except:
        return False

# Function to get total follow count - Thêm mới để đếm tổng số follow đã thực hiện
def get_follow_count(id_ig):
    try:
        if os.path.exists(f"{id_ig}_follow_count.txt"):
            with open(f"{id_ig}_follow_count.txt", "r") as f:
                count = f.read().strip()
                return int(count) if count.isdigit() else 0
        return 0
    except Exception as e:
        print(f"\033[1;31mLỗi khi đọc số lượng follow: {e}")
        return 0

# Function to update follow count - Thêm mới để cập nhật tổng số follow
def update_follow_count(id_ig, count):
    try:
        with open(f"{id_ig}_follow_count.txt", "w") as f:
            f.write(str(count))
        return True
    except Exception as e:
        print(f"\033[1;31mLỗi khi cập nhật số lượng follow: {e}")
        return False

# Main execution with improved error handling
try:
    # Xóa màn hình và hiển thị banner
    os.system("cls" if os.name == "nt" else "clear")
    banner()
    
    # Kiểm tra cập nhật trước khi thực hiện các chức năng khác
    check_update_on_startup()
    
    # Hiển thị menu quản lý cookie
    cookie_menu_option = input('\033[1;97m[\033[1;91m❣\033[1;97m] \033[1;36m✈  \033[1;32mBạn muốn quản lý cookie không? (y/n):\033[1;33m ').lower()
    if cookie_menu_option == 'y':
        show_cookie_menu()
    
    # Khởi tạo danh sách cookie
    list_cookie = []
    
    # Main login loop with error handling
    while True:
        token = input('\033[1;97m[\033[1;91m❣\033[1;97m] \033[1;36m✈  \033[1;32mNhập Access_Token Vipig:\033[1;33m ')
        
        try:
            log = requests.post('https://vipig.net/logintoken.php', 
                              headers={'Content-type':'application/x-www-form-urlencoded'}, 
                              data={'access_token':token},
                              timeout=15).json()
            
            if log.get('status') == 'success':
                user = log['data']['user']
                xu = log['data']['sodu']
                ckvp = cookie(token)
                
                if ckvp:
                    print('\033[1;97m[\033[1;91m❣\033[1;97m] \033[1;36m✈  \033[1;32mĐăng Nhập Thành Công')
                    break
                else:
                    print('\033[1;31mKhông thể lấy cookie từ token, vui lòng thử lại')
            elif log.get('status') == 'fail':
                print(log.get('mess', 'Đăng nhập thất bại'))
            else:
                print('\033[1;31mPhản hồi không hợp lệ từ server')
        except Exception as e:
            print(f'\033[1;31mLỗi khi đăng nhập: {e}')
    
    bongoc(14)
    
    # Cookie management section with improved error handling
    list_cookie = []
    choice = input('\033[1;97m[\033[1;91m❣\033[1;97m] \033[1;36m✈  \033[1;32mBạn có muốn dùng lại các cookie cũ không? (y/n):\033[1;33m ').lower()
    
    if choice == 'n':
        clear_cookie_file()
        x = 0
        print('[LƯU Ý] Muốn Dừng Thì Nhấn Enter')
        
        while True:
            try:
                x = x + 1
                cookie = input(f'\033[1;97m[\033[1;91m❣\033[1;97m] \033[1;36m✈  \033[1;32mNhập Cookie Instagram Thứ {x}:\033[1;33m ')
                
                if cookie == '' and x > 1:
                    break
                
                # Kiểm tra cookie đã die chưa
                if is_cookie_die(cookie):
                    print(f'\033[1;31mCookie này đã bị đánh dấu là die từ trước, bỏ qua')
                    x = x - 1
                    continue
                    
                ten = name(cookie)
                if ten[0] != 'die':
                    print(f'User Instagram: {cam}{ten[0]}{trang} ')
                    list_cookie.append(cookie)
                    save_cookie_to_txt(cookie)
                    bongoc(14)
                    sleep(1)  # Giảm delay để nhập cookie nhanh hơn
                else:
                    print('\033[1;31mCookie Instagram Sai ! Vui Lòng Nhập Lại ! ! ! ')
                    x = x - 1
                    bongoc(14)
            except Exception as e:
                print(f'\033[1;31mLỗi khi xử lý cookie: {e}')
                x = x - 1
                bongoc(14)
    
    elif choice == 'y':
        list_cookie = load_cookies_from_txt()
        
        if not list_cookie:
            print('\033[1;31mKhông có cookie live nào trong file ck.txt! Vui lòng nhập cookie mới.')
            choice = input('\033[1;97m[\033[1;91m❣\033[1;97m] \033[1;36m✈  \033[1;32mBạn có muốn xóa tất cả cookie die không? (y/n):\033[1;33m ').lower()
            if choice == 'y':
                if os.path.exists('cookie_die.txt'):
                    os.remove('cookie_die.txt')
                    print('\033[1;32mĐã xóa tất cả cookie die!')
                    
            clear_cookie_file()
            x = 0
            print('[LƯU Ý] Muốn Dừng Thì Nhấn Enter')
            
            while True:
                try:
                    x = x + 1
                    cookie = input(f'\033[1;97m[\033[1;91m❣\033[1;97m] \033[1;36m✈  \033[1;32mNhập Cookie Instagram Thứ {x}:\033[1;33m ')
                    
                    if cookie == '' and x > 1:
                        break
                    
                    # Kiểm tra cookie đã die chưa
                    if is_cookie_die(cookie):
                        print(f'\033[1;31mCookie này đã bị đánh dấu là die từ trước, bỏ qua')
                        x = x - 1
                        continue
                        
                    ten = name(cookie)
                    if ten[0] != 'die':
                        print(f'User Instagram: {cam}{ten[0]}{trang} ')
                        list_cookie.append(cookie)
                        save_cookie_to_txt(cookie)
                        bongoc(14)
                        sleep(1)  # Giảm delay để nhập cookie nhanh hơn
                    else:
                        print('\033[1;31mCookie Instagram Sai ! Vui Lòng Nhập Lại ! ! ! ')
                        x = x - 1
                        bongoc(14)
                except Exception as e:
                    print(f'\033[1;31mLỗi khi xử lý cookie: {e}')
                    x = x - 1
                    bongoc(14)
    
    else:
        print('\033[1;31mLựa chọn không hợp lệ! Thoát chương trình.')
        sys.exit()
    
    # Clear screen and show banner
    os.system("cls" if os.name == "nt" else "clear")
    banner()
    
    # Display account info
    print(f"""\033[1;97m[\033[1;91m❣\033[1;97m] \033[1;36m✈  \033[1;32mTên Tài Khoản: \033[1;33m{user}
\033[1;97m[\033[1;91m❣\033[1;97m] \033[1;36m✈  \033[1;32mXu Hiện Tại: \033[1;33m{xu}
\033[1;97m[\033[1;91m❣\033[1;97m] \033[1;36m✈  \033[1;32mSố Cookie: \033[1;33m{len(list_cookie)}""")
    
    bongoc(14)
    
    # Task selection
    print("""\033[1;97m[\033[1;91m❣\033[1;97m] \033[1;36m✈  \033[1;32mNhập [1] Để Chạy Nhiệm Vụ Like
\033[1;97m[\033[1;91m❣\033[1;97m] \033[1;36m✈  \033[1;32mNhập [2] Để Chạy Nhiệm Vụ Follow
\033[1;97m[\033[1;91m❣\033[1;97m] \033[1;36m✈  \033[1;32mNhập [3] Để Chạy Nhiệm Vụ Comment
\033[1;97m[\033[1;91m❣\033[1;97m] \033[1;36m✈  \033[1;32mCó Thể Chọn Nhiều Nhiệm Vụ \033[1;33m(Ví Dụ 123)""")
    
    chon = input('\033[1;97m[\033[1;91m❣\033[1;97m] \033[1;36m✈  \033[1;32mNhập Số Để Chạy Nhiệm Vụ:\033[1;33m ')
    
    bongoc(14)
    
    # Configuration settings
    dl = int(input('\033[1;97m[\033[1;91m❣\033[1;97m] \033[1;36m✈  \033[1;32mNhập Delay:\033[1;33m '))
    
    print('Sau ____ Nhiệm Vụ Thì Kích Hoạt Chống Block. ',end='\r')
    chong_block = int(input('Sau '))
    
    print(f'Sau {chong_block} Nhiệm Vụ Nghỉ Ngơi ____ Giây       ',end='\r')
    delay_block = int(input(f'Sau {chong_block} Nhiệm Vụ Nghỉ Ngơi '))
    
    doi_acc = int(input('\033[1;97m[\033[1;91m❣\033[1;97m] \033[1;36m✈  \033[1;32mSau Bao Nhiêu Nhiệm Vụ Thì Đổi Nick:\033[1;33m '))
    
    # Main task loop with improved error handling
    while True:
        try:
            x = 0
            anorin = 0
            
            # Check if cookies are available
            if len(list_cookie) == 0:
                print('\033[1;31mToàn Bộ Cookie Đã Out Vui Lòng Nhập Lại ! !')
                
                # Xóa tất cả cookie die và yêu cầu nhập lại
                if os.path.exists('cookie_die.txt'):
                    choice = input('\033[1;97m[\033[1;91m❣\033[1;97m] \033[1;36m✈  \033[1;32mBạn có muốn xóa tất cả cookie die không? (y/n):\033[1;33m ').lower()
                    if choice == 'y':
                        os.remove('cookie_die.txt')
                        print('\033[1;32mĐã xóa tất cả cookie die!')
                
                clear_cookie_file()
                
                while True:
                    try:
                        x = x + 1
                        cookie = input(f'\033[1;97m[\033[1;91m❣\033[1;97m] \033[1;36m✈  \033[1;32mNhập Cookie Instagram Thứ {x}:\033[1;33m ')
                        
                        if cookie == '' and x > 1:
                            break
                        
                        # Kiểm tra cookie đã die chưa
                        if is_cookie_die(cookie):
                            print(f'\033[1;31mCookie này đã bị đánh dấu là die từ trước, bỏ qua')
                            x = x - 1
                            continue
                            
                        ten = name(cookie)
                        if ten[0] != 'die':
                            print(f'User Instagram: {cam}{ten[0]}{trang} ')
                            list_cookie.append(cookie)
                            save_cookie_to_txt(cookie)
                            bongoc(14)
                            sleep(1)
                        else:
                            print('\033[1;31mCookie Instagram Sai ! Vui Lòng Nhập Lại ! ! ! ')
                            x = x - 1
                            bongoc(14)
                    except Exception as e:
                        print(f'\033[1;31mLỗi khi xử lý cookie: {e}')
                        x = x - 1
                        bongoc(14)
            
            # Process each cookie safely, with index check to avoid list index out of range
            for i in range(len(list_cookie)):
                # Ensure index is within range (list might have changed)
                if i >= len(list_cookie):
                    print(f"\033[1;31mChỉ số cookie vượt quá số lượng hiện có")
                    break
                    
                if anorin == 2:
                    break
                
                loi_like = 0
                loi_cmt = 0
                cookie = list_cookie[i]
                
                # Kiểm tra cookie trước khi sử dụng
                if is_cookie_die(cookie):
                    print(f'\033[1;31mCookie này đã bị đánh dấu là die, bỏ qua')
                    if cookie in list_cookie:
                        list_cookie.remove(cookie)
                    continue
                
                # Get user info and verify cookie
                try:
                    user = name(cookie)
                    id_ig = user[1]
                    
                    if user[0] == 'die':
                        print('\033[1;31mCookie Instagram Die ! ! !! ')
                        mark_cookie_as_die(cookie)
                        if cookie in list_cookie:
                            list_cookie.remove(cookie)
                        continue
                except Exception as e:
                    print(f'\033[1;31mLỗi khi lấy thông tin user: {e}')
                    mark_cookie_as_die(cookie)
                    if cookie in list_cookie:
                        list_cookie.remove(cookie)
                    continue
                
                # Configure account
                try:
                    ngoc = cau_hinh(id_ig, ckvp)
                    if ngoc == '1':
                        bongoc(14)
                        print(f'Đang Cấu Hình ID: {id_ig} | User: {cam}{user[0]}{trang}')
                        bongoc(14)
                    else:
                        print(f'Cấu Hình Thất Bại ID: {id_ig} | User: {cam}{user[0]}{trang} ')
                        delay(2)
                        if cookie in list_cookie:
                            list_cookie.remove(cookie)
                        continue
                except Exception as e:
                    print(f'\033[1;31mLỗi khi cấu hình tài khoản: {e}')
                    delay(2)
                    if cookie in list_cookie:
                        list_cookie.remove(cookie)
                    continue
                
                # Lấy số lượng follow đã thực hiện từ trước
                follow_count = get_follow_count(id_ig)
                
                anorin = 0
                
                # Main task execution loop
                while True:
                    try:
                        if anorin == 1 or anorin == 2:
                            break
                        
                        # Like tasks
                        if '1' in chon:
                            try:
                                get_like = get_nv('', ckvp)
                                
                                if not isinstance(get_like, list):
                                    print('\033[1;31mPhản hồi từ API không phải danh sách nhiệm vụ')
                                    continue
                                
                                if len(get_like) == 0:
                                    print('Tạm Thời Hết Nhiệm Vụ Like','     ',end='\r')
                                
                                if len(get_like) != 0:
                                    print(f'Tìm Thấy {len(get_like)} Nhiệm Vụ Like','     ',end='\r')
                                    
                                    for x in get_like:
                                        try:
                                            # Kiểm tra xem phản hồi có chứa đúng dữ liệu hay không
                                            if not isinstance(x, dict):
                                                print('\033[1;31mDữ liệu nhiệm vụ không hợp lệ')
                                                continue
                                                
                                            if 'link' not in x or 'idpost' not in x:
                                                print('\033[1;31mThiếu dữ liệu trong nhiệm vụ')
                                                continue
                                                
                                            link = x['link']
                                            uid = x['idpost']
                                            
                                            id = get_id(link, cookie)
                                            if id == False:
                                                continue
                                            
                                            lam = like(id, cookie)
                                            
                                            if lam == '1':
                                                user = name(cookie)
                                                if user[0] == 'die':
                                                    print('Cookie Instagram Die ! ! !! ')
                                                    mark_cookie_as_die(cookie)
                                                    if cookie in list_cookie:
                                                        list_cookie.remove(cookie)
                                                    anorin = 2
                                                    break
                                                else:
                                                    print(f'Tài Khoản {cam}{user[0]}{trang} Đã Bị Chặn Tương Tác {lam}')
                                                    mark_cookie_as_die(cookie)
                                                    if cookie in list_cookie:
                                                        list_cookie.remove(cookie)
                                                    anorin = 2
                                                    break
                                            elif loi_like >= 4:
                                                print(f'Tài Khoản {cam}{user[0]}{trang} Đã Bị Chặn Tương Tác')
                                                mark_cookie_as_die(cookie)
                                                if cookie in list_cookie:
                                                    list_cookie.remove(cookie)
                                                anorin = 2
                                                break
                                            elif lam == '2':
                                                nhan = nhan_tien(uid, ckvp, '')
                                                
                                                if 'mess' in nhan:
                                                    xu = coin(ckvp)
                                                    dem = dem + 1
                                                    tg = datetime.now().strftime('%H:%M')
                                                    print(f'[{dem}] | {tg} | LIKE | {id} | +300 | {xu} | {cam}{user[0]}{trang}')
                                                    loi_like = 0
                                                    
                                                    if dem % chong_block == 0:
                                                        delay(delay_block)
                                                    else:
                                                        delay(dl)
                                                    
                                                    if dem % doi_acc == 0:
                                                        anorin = 1
                                                        break
                                                else:
                                                    tg = datetime.now().strftime('%H:%M')
                                                    print(f'[X] | {tg} | LIKE | {id} | ERROR | {cam}{user[0]}{trang}')
                                                    loi_like += 1
                                                    delay(dl)
                                        except Exception as e:
                                            print(f'\033[1;31mLỗi trong nhiệm vụ like: {e}')
                                            delay(dl)
                            except Exception as e:
                                print(f'\033[1;31mLỗi khi lấy nhiệm vụ like: {e}')
                                delay(2)
                        
                        if anorin == 1 or anorin == 2:
                            break
                        
                        # Follow tasks
                        if '2' in chon:
                            try:
                                get_sub = get_nv('/subcheo', ckvp)
                                
                                if not isinstance(get_sub, list):
                                    print('\033[1;31mPhản hồi từ API không phải danh sách nhiệm vụ')
                                    continue
                                
                                if len(get_sub) == 0:
                                    print('Tạm Thời Hết Nhiệm Vụ Follow','     ',end='\r')
                                
                                if len(get_sub) != 0:
                                    print(f'Tìm Thấy {len(get_sub)} Nhiệm Vụ Follow','     ',end='\r')
                                    
                                    for x in get_sub:
                                        try:
                                            # Kiểm tra dữ liệu nhiệm vụ
                                            if not isinstance(x, dict) or 'soID' not in x:
                                                print('\033[1;31mDữ liệu nhiệm vụ không hợp lệ')
                                                continue
                                                
                                            id = x['soID']
                                            
                                            lam = follow(id, cookie)
                                            
                                            if lam == '1':
                                                if user[0] == 'die':
                                                    print(f'Cookie Instagram Die ! ! !!  ')
                                                    mark_cookie_as_die(cookie)
                                                    if cookie in list_cookie:
                                                        list_cookie.remove(cookie)
                                                else:
                                                    print(f'Tài Khoản {cam}{user[0]}{trang} Đã Bị Chặn Tương Tác {lam}')
                                                    mark_cookie_as_die(cookie)
                                                    if cookie in list_cookie:
                                                        list_cookie.remove(cookie)
                                                
                                                anorin = 2
                                                break
                                            
                                            # Tăng số lượng follow và lưu lại
                                            follow_count += 1
                                            update_follow_count(id_ig, follow_count)
                                            
                                            # Lưu ID vào file để nhận tiền
                                            with open(f"{id_ig}.txt", "a+") as data_id:
                                                data_id.write(str(id) + ',')
                                            
                                            dem = dem + 1
                                            tg = datetime.now().strftime('%H:%M')
                                            print(f'[{dem}] | {tg} | FOLLOW | {id} | SUCCESS | {cam}{user[0]}{trang} | Tổng: {follow_count}')
                                            
                                            # Nếu đủ 6 job follow thì nhận tiền
                                            if follow_count % 6 == 0:
                                                try:
                                                    # Kiểm tra file trước khi đọc
                                                    if not os.path.exists(f"{id_ig}.txt"):
                                                        print(f"\033[1;31mFile {id_ig}.txt không tồn tại")
                                                        with open(f"{id_ig}.txt", "w") as f:
                                                            f.write('')
                                                        continue
                                                        
                                                    # Đọc an toàn
                                                    with open(f"{id_ig}.txt", "r") as data_id:
                                                        list_data = data_id.read()
                                                        
                                                    if not list_data.strip():
                                                        print(f"\033[1;31mFile {id_ig}.txt trống")
                                                        continue
                                                        
                                                    nhan = nhan_sub(list_data, ckvp)
                                                    
                                                    if 'error' not in nhan:
                                                        xu_them = nhan.get('sodu', 0)
                                                        job = xu_them // 600
                                                        xu = coin(ckvp)
                                                        print(f'Nhận Thành Công {job} Nhiệm Vụ Follow | +{xu_them} | {xu} | {cam}{user[0]}{trang}')
                                                        
                                                        # Reset file ID đã follow sau khi nhận tiền
                                                        os.remove(f"{id_ig}.txt")
                                                        with open(f"{id_ig}.txt", "w") as f:
                                                            f.write('')
                                                    else:
                                                        print(f"\033[1;31mLỗi khi nhận tiền follow: {nhan}")
                                                except Exception as e:
                                                    print(f"\033[1;31mLỗi khi xử lý nhận tiền follow: {e}")
                                            
                                            if dem % chong_block == 0:
                                                delay(delay_block)
                                            else:
                                                delay(dl)
                                            
                                            if dem % doi_acc == 0:
                                                anorin = 1
                                                break
                                        except Exception as e:
                                            print(f'\033[1;31mLỗi trong nhiệm vụ follow: {e}')
                                            delay(dl)
                            except Exception as e:
                                print(f'\033[1;31mLỗi khi lấy nhiệm vụ follow: {e}')
                                delay(2)
                        
                        if anorin == 1 or anorin == 2:
                            break
                        
                        # Comment tasks
                        if '3' in chon:
                            try:
                                get_cmt = get_nv('/cmtcheo', ckvp)
                                
                                if not isinstance(get_cmt, list):
                                    print('\033[1;31mPhản hồi từ API không phải danh sách nhiệm vụ')
                                    continue
                                
                                if len(get_cmt) == 0:
                                    print('Tạm Thời Hết Nhiệm Vụ Comment','     ',end='\r')
                                
                                if len(get_cmt) != 0:
                                    print(f'Tìm Thấy {len(get_cmt)} Nhiệm Vụ Comment','     ',end='\r')
                                    
                                    for x in get_cmt:
                                        try:
                                            # Kiểm tra dữ liệu nhiệm vụ
                                            if not isinstance(x, dict) or 'link' not in x or 'idpost' not in x or 'nd' not in x:
                                                print('\033[1;31mThiếu dữ liệu trong nhiệm vụ comment')
                                                continue
                                                
                                            link = x['link']
                                            uid = x['idpost']
                                            
                                            try:
                                                msg = random.choice(json.loads(x['nd']))
                                            except:
                                                print('\033[1;31mLỗi khi parse nội dung comment')
                                                continue
                                            
                                            id = get_id(link, cookie)
                                            if id == False:
                                                continue
                                            
                                            lam = cmt(msg, id, cookie)
                                            
                                            if lam == '1':
                                                user = name(cookie)
                                                if user[0] == 'die':
                                                    print('Cookie Instagram Die ! ! !! ')
                                                    mark_cookie_as_die(cookie)
                                                    if cookie in list_cookie:
                                                        list_cookie.remove(cookie)
                                                    anorin = 2
                                                    break
                                                else:
                                                    print(f'Tài Khoản {cam}{user[0]}{trang} Đã Bị Chặn Tương Tác ')
                                                    mark_cookie_as_die(cookie)
                                                    if cookie in list_cookie:
                                                        list_cookie.remove(cookie)
                                                    anorin = 2
                                                    break
                                            elif loi_cmt >= 4:
                                                print(f'Tài Khoản {cam}{user[0]}{trang} Đã Bị Chặn Tương Tác')
                                                mark_cookie_as_die(cookie)
                                                if cookie in list_cookie:
                                                    list_cookie.remove(cookie)
                                                anorin = 2
                                                break
                                            elif lam == 'ok':
                                                nhan = nhan_tien(uid, ckvp, '/cmtcheo')
                                                
                                                if 'mess' in nhan:
                                                    xu = coin(ckvp)
                                                    dem = dem + 1
                                                    tg = datetime.now().strftime('%H:%M')
                                                    print(f'[{dem}] | {tg} | COMMENT | {id} | {msg} | +600 | {xu} | {cam}{user[0]}{trang}')
                                                    loi_cmt = 0
                                                    
                                                    if dem % chong_block == 0:
                                                        delay(delay_block)
                                                    else:
                                                        delay(dl)
                                                    
                                                    if dem % doi_acc == 0:
                                                        anorin = 1
                                                        break
                                                else:
                                                    tg = datetime.now().strftime('%H:%M')
                                                    print(f'[X] | {tg} | COMMENT | {id} | ERROR | {cam}{user[0]}{trang}')
                                                    loi_cmt += 1
                                                    delay(dl)
                                            else:
                                                tg = datetime.now().strftime('%H:%M')
                                                print(f'[X] | {tg} | COMMENT | {id} | ERROR | {cam}{user[0]}{trang}')
                                                loi_cmt += 1
                                                delay(dl)
                                        except Exception as e:
                                            print(f'\033[1;31mLỗi trong nhiệm vụ comment: {e}')
                                            delay(dl)
                            except Exception as e:
                                print(f'\033[1;31mLỗi khi lấy nhiệm vụ comment: {e}')
                                delay(2)
                    except IndexError as e:
                        print(f"\033[1;31mLỗi index out of range: {e}")
                        print("\033[1;33mĐang cố gắng khôi phục...")
                        traceback.print_exc()
                        delay(3)
                    except Exception as e:
                        print(f'\033[1;31mLỗi trong vòng lặp chính: {e}')
                        traceback.print_exc()
                        delay(3)
        except KeyboardInterrupt:
            print("\n\033[1;31mĐã dừng chương trình theo yêu cầu người dùng")
            break
        except Exception as e:
            print(f'\033[1;31mLỗi không mong muốn: {e}')
            traceback.print_exc()
            delay(3)  # Giảm delay khi có lỗi

except Exception as e:
    print(f"\033[1;31mLỗi chương trình nghiêm trọng: {e}")
    traceback.print_exc()
