import json
import requests, os, sys, re
from time import sleep
from datetime import datetime
import random
import time

def banner():
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

os.system("cls" if os.name == "nt" else "clear")
banner()
list_cookie = []

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
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
    
    if 'useragent=' in cookie:
        try:
            ua_encoded = cookie.split('useragent=')[1].split(';')[0]
            user_agent = ua_encoded
        except:
            pass
    
    try:
        user_id = cookie.split('ds_user_id=')[1].split(';')[0]
    except:
        print("\033[1;31mKhông thể lấy user_id từ cookie")
        return 'die', 'die'
    
    headers = {
        'Host': 'i.instagram.com',
        'User-Agent': user_agent,
        'Accept': 'application/json',
        'X-IG-App-ID': '1217981644879628',
        'X-CSRFToken': cookie.split('csrftoken=')[1].split(';')[0] if 'csrftoken=' in cookie else '',
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
                except json.JSONDecodeError:
                    print(f"\033[1;31mLỗi phân tích JSON: {response.text[:100]}...")
            
            elif response.status_code == 429:  # Too Many Requests
                print(f'\033[1;31m[429] Quá nhiều yêu cầu, thử lại sau {5 * (attempt + 1)} giây...')
                sleep(5 * (attempt + 1))
                continue
            else:
                print(f'\033[1;31m[Error] Status code: {response.status_code} - {response.text[:50]}...')
        
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
    return 'die', 'die'

# Improved file operations
def save_cookie_to_txt(cookie):
    try:
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
                    try:
                        ten = name(cookie)
                        if ten[0] != 'die':
                            live_cookies.append(cookie)
                            print(f'User Instagram: {cam}{ten[0]}{trang} - Live')
                        else:
                            print(f'Cookie: {cookie[:20]}... - Die')
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

# Improved post ID extraction
def get_id(link, cookie):
    try:
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
            if 'media?id=' in a:
                id = a.split('media?id=')[1].split('"')[0]
                return id
            else:
                print("\033[1;31mKhông tìm thấy ID trong phản hồi")
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
            clear_cookie_file()
            x = 0
            print('[LƯU Ý] Muốn Dừng Thì Nhấn Enter')
            
            while True:
                try:
                    x = x + 1
                    cookie = input(f'\033[1;97m[\033[1;91m❣\033[1;97m] \033[1;36m✈  \033[1;32mNhập Cookie Instagram Thứ {x}:\033[1;33m ')
                    
                    if cookie == '' and x > 1:
                        break
                    
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
                clear_cookie_file()
                
                while True:
                    try:
                        x = x + 1
                        cookie = input(f'\033[1;97m[\033[1;91m❣\033[1;97m] \033[1;36m✈  \033[1;32mNhập Cookie Instagram Thứ {x}:\033[1;33m ')
                        
                        if cookie == '' and x > 1:
                            break
                        
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
            
            # Process each cookie
            for i in range(len(list_cookie)):
                if anorin == 2:
                    break
                
                loi_like = a = 0
                loi_cmt = 0
                cookie = list_cookie[i]
                
                # Get user info and verify cookie
                try:
                    user = name(cookie)
                    id_ig = user[1]
                    
                    if user[0] == 'die':
                        print('\033[1;31mCookie Instagram Die ! ! !! ')
                        list_cookie.remove(cookie)
                        continue
                except Exception as e:
                    print(f'\033[1;31mLỗi khi lấy thông tin user: {e}')
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
                        list_cookie.remove(cookie)
                        continue
                except Exception as e:
                    print(f'\033[1;31mLỗi khi cấu hình tài khoản: {e}')
                    delay(2)
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
                                
                                if len(get_like) == 0:
                                    print('Tạm Thời Hết Nhiệm Vụ Like','     ',end='\r')
                                
                                if len(get_like) != 0:
                                    print(f'Tìm Thấy {len(get_like)} Nhiệm Vụ Like','     ',end='\r')
                                    
                                    for x in get_like:
                                        try:
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
                                                    list_cookie.remove(cookie)
                                                    anorin = 2
                                                    break
                                                else:
                                                    print(f'Tài Khoản {cam}{user[0]}{trang} Đã Bị Chặn Tương Tác {lam}')
                                                    list_cookie.remove(cookie)
                                                    anorin = 2
                                                    break
                                            elif loi_like >= 4:
                                                print(f'Tài Khoản {cam}{user[0]}{trang} Đã Bị Chặn Tương Tác')
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
                                
                                if len(get_sub) == 0:
                                    print('Tạm Thời Hết Nhiệm Vụ Follow','     ',end='\r')
                                
                                if len(get_sub) != 0:
                                    print(f'Tìm Thấy {len(get_sub)} Nhiệm Vụ Follow','     ',end='\r')
                                    
                                    for x in get_sub:
                                        try:
                                            id = x['soID']
                                            
                                            lam = follow(id, cookie)
                                            
                                            if lam == '1':
                                                if user[0] == 'die':
                                                    print(f'Cookie Instagram Die ! ! !!  ')
                                                    list_cookie.remove(cookie)
                                                else:
                                                    print(f'Tài Khoản {cam}{user[0]}{trang} Đã Bị Chặn Tương Tác {lam}')
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
                                                    # Đọc danh sách ID đã follow
                                                    with open(f"{id_ig}.txt", "r") as data_id:
                                                        list_data = data_id.read()
                                                        
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
                                
                                if len(get_cmt) == 0:
                                    print('Tạm Thời Hết Nhiệm Vụ Comment','     ',end='\r')
                                
                                if len(get_cmt) != 0:
                                    print(f'Tìm Thấy {len(get_cmt)} Nhiệm Vụ Comment','     ',end='\r')
                                    
                                    for x in get_cmt:
                                        try:
                                            link = x['link']
                                            uid = x['idpost']
                                            msg = random.choice(json.loads(x['nd']))
                                            
                                            id = get_id(link, cookie)
                                            if id == False:
                                                continue
                                            
                                            lam = cmt(msg, id, cookie)
                                            
                                            if lam == '1':
                                                user = name(cookie)
                                                if user[0] == 'die':
                                                    print('Cookie Instagram Die ! ! !! ')
                                                    list_cookie.remove(cookie)
                                                    anorin = 2
                                                    break
                                                else:
                                                    print(f'Tài Khoản {cam}{user[0]}{trang} Đã Bị Chặn Tương Tác ')
                                                    list_cookie.remove(cookie)
                                                    anorin = 2
                                                    break
                                            elif loi_cmt >= 4:
                                                print(f'Tài Khoản {cam}{user[0]}{trang} Đã Bị Chặn Tương Tác')
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
                    except Exception as e:
                        print(f'\033[1;31mLỗi trong vòng lặp chính: {e}')
                        delay(3)
        except KeyboardInterrupt:
            print("\n\033[1;31mĐã dừng chương trình theo yêu cầu người dùng")
            break
        except Exception as e:
            print(f'\033[1;31mLỗi không mong muốn: {e}')
            delay(3)  # Giảm delay khi có lỗi

except Exception as e:
    print(f"\033[1;31mLỗi chương trình nghiêm trọng: {e}")
