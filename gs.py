import json
import requests, os, sys, re
from time import sleep
import random
import shutil
import traceback
import datetime

# Thông tin phiên bản của tool
VERSION = "1.5.4"
GITHUB_RAW_URL = "https://raw.githubusercontent.com/Dat075/vipig123/refs/heads/main/gs.py"
GITHUB_VERSION_URL = "https://raw.githubusercontent.com/Dat075/vipig123/refs/heads/main/version.txt"

# Danh sách User-Agent
USER_AGENTS = [
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_8 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.8 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0",
    "Mozilla/5.0 (X11; Linux i686; rv:102.0) Gecko/20100101 Firefox/102.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
]

# Hệ thống kiểm tra cập nhật
def check_for_updates():
    try:
        print("\033[1;33mĐang kiểm tra cập nhật...")
        response = requests.get(GITHUB_VERSION_URL, timeout=10)
        response.raise_for_status()
        latest_version = response.text.strip()
        return latest_version if latest_version != VERSION else None
    except Exception as e:
        print(f"\033[1;31mLỗi khi kiểm tra cập nhật: {e}")
        return None

def update_script():
    try:
        print("\033[1;33mĐang tải phiên bản mới...")
        response = requests.get(GITHUB_RAW_URL, timeout=15)
        response.raise_for_status()
        script_path = os.path.abspath(__file__)
        backup_path = script_path + ".bak"
        shutil.copy2(script_path, backup_path)
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(response.text)
        print("\033[1;32mCập nhật thành công! Khởi động lại tool để áp dụng thay đổi.")
        return True
    except Exception as e:
        print(f"\033[1;31mLỗi trong quá trình cập nhật: {e}")
        return False

def check_update_on_startup():
    latest_version = check_for_updates()
    if latest_version:
        print(f"\033[1;33mCó phiên bản mới: {latest_version} (Phiên bản hiện tại: {VERSION})")
        choice = input("\033[1;97m[\033[1;91m❣\033[1;97m] \033[1;36m✈  \033[1;32mBạn có muốn cập nhật không? (y/n): \033[1;33m").lower()
        if choice == 'y':
            if update_script():
                sys.exit(0)
        else:
            print("\033[1;33mTiếp tục sử dụng phiên bản cũ.")
    else:
        print(f"\033[1;32mBạn đang sử dụng phiên bản mới nhất: {VERSION}")

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
cam = '\x1b[38;5;208m'
hong = '\x1b[1;95m'
thanh_xau="\033[1;97m[\033[1;91m❣\033[1;97m] \033[1;36m✈  \033[1;32m"
thanh_dep="\033[1;97m[\033[1;91m❣\033[1;97m] \033[1;36m✈  \033[1;32m"

dem = 0

def coin(ckvp):
    try:
        headers = {'user-agent': random.choice(USER_AGENTS), 'cookie': ckvp}
        response = requests.get('https://vipig.net/home.php', headers=headers, timeout=10)
        response.raise_for_status()
        text = response.text
        if '"soduchinh">' in text:
            sodu = text.split('"soduchinh">')[1].split('<')[0]
            print(f"\033[1;33m[DEBUG] Số dư thực tế từ server: {sodu}")
            return sodu
        print("\033[1;31mKhông tìm thấy số dư trong HTML")
        return "0"
    except Exception as e:
        print(f"\033[1;31mLỗi khi lấy số xu: {e}")
        return "0"

def cookie(token):
    try:
        response = requests.post('https://vipig.net/logintoken.php', headers={'Content-type': 'application/x-www-form-urlencoded'}, data={'access_token': token}, timeout=10)
        response.raise_for_status()
        if 'PHPSESSID' in response.cookies:
            return f'PHPSESSID={response.cookies["PHPSESSID"]}'
        print("\033[1;31mKhông thể lấy cookie từ token")
        return None
    except Exception as e:
        print(f"\033[1;31mLỗi khi lấy cookie: {e}")
        return None

def save_token(token, user):
    try:
        file_path = 'tokens.json'
        tokens = []
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                tokens = json.load(f)
        if not isinstance(tokens, list):
            tokens = []
        if not any(t['token'] == token for t in tokens):
            tokens.append({'token': token, 'user': user})
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(tokens, f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(f"\033[1;31mLỗi khi lưu token: {e}")
        return False

def load_tokens():
    try:
        file_path = 'tokens.json'
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    except Exception as e:
        print(f"\033[1;31mLỗi khi đọc file token: {e}")
        return []

def get_nv(type, ckvp):
    try:
        headers = {
            'content-type': 'text/html; charset=UTF-8',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'x-requested-with': 'XMLHttpRequest',
            'user-agent': random.choice(USER_AGENTS),
            'cookie': ckvp
        }
        response = requests.post(f'https://vipig.net/kiemtien{type}/getpost.php', headers=headers, timeout=15)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"\033[1;31mLỗi khi lấy nhiệm vụ {type}: {e}")
        return []

def nhan_tien(list, ckvp, type, retries=3):
    data = f'id={list}'
    headers = {
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'accept': '*/*',
        'x-requested-with': 'XMLHttpRequest',
        'user-agent': random.choice(USER_AGENTS),
        'cookie': ckvp
    }
    for attempt in range(retries):
        try:
            response = requests.post(f'https://vipig.net/kiemtien{type}/nhantien.php', headers=headers, data=data, timeout=15)
            response.raise_for_status()
            try:
                result = response.json()
            except ValueError:
                result = response.text
            print(f"\033[1;33m[DEBUG] Phản hồi từ nhan_tien: {result}")
            status = 'success' if 'thành công' in str(result).lower() else 'fail'
            return {
                'status': status,
                'response': result,
                'attempt': attempt + 1
            }
        except requests.exceptions.RequestException as e:
            print(f"\033[1;31mLỗi khi nhận xu (lần {attempt + 1}/{retries}): {e}")
            if attempt < retries - 1:
                sleep(5 * (attempt + 1))
            else:
                return {
                    'status': 'error',
                    'response': str(e),
                    'attempt': retries
                }

def nhan_sub(list, ckvp):
    try:
        data = f'id={list.rstrip(",")}'
        headers = {
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'accept': '*/*',
            'x-requested-with': 'XMLHttpRequest',
            'user-agent': random.choice(USER_AGENTS),
            'cookie': ckvp
        }
        response = requests.post('https://vipig.net/kiemtien/subcheo/nhantien2.php', headers=headers, data=data, timeout=15)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"\033[1;31mLỗi khi nhận sub: {e}")
        return {"error": str(e)}

def delay(dl):
    try:
        for i in range(int(dl), -1, -1):
            print(f'[AN ORIN][{i} Giây]           ', end='\r')
            sleep(1)
    except KeyboardInterrupt:
        print("\n\033[1;31mĐã dừng delay bởi người dùng")
    except Exception as e:
        print(f"\n\033[1;31mLỗi trong quá trình delay: {e}")
        sleep(dl)

def delay_with_backoff(attempts, base_delay=5):
    try:
        delay_time = min(base_delay * (1.3 ** min(attempts, 5)), 30)
        for i in range(int(delay_time), -1, -1):
            print(f'[AN ORIN][Đang nghỉ {i} Giây để tránh block]           ', end='\r')
            sleep(1)
    except KeyboardInterrupt:
        print("\n\033[1;31mĐã dừng delay bởi người dùng")
    except Exception as e:
        print(f"\n\033[1;31mLỗi trong quá trình adaptive delay: {e}")
        sleep(base_delay)

def save_cookie_info(cookie_info):
    try:
        file_path = 'cookie_storage.json'
        data = []
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        if not isinstance(data, list):
            data = []
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

def name(cookie, retries=3):
    user_agent = random.choice(USER_AGENTS)
    if 'useragent=' in cookie:
        user_agent = cookie.split('useragent=')[1].split(';')[0]
    try:
        user_id = cookie.split('ds_user_id=')[1].split(';')[0]
        if not user_id:
            raise ValueError("ds_user_id trống")
    except (IndexError, ValueError):
        print("\033[1;31mKhông tìm thấy ds_user_id trong cookie")
        return 'die', 'die'
    csrf_token = cookie.split('csrftoken=')[1].split(';')[0] if 'csrftoken=' in cookie else ""
    headers = {
        'Host': 'i.instagram.com',
        'User-Agent': user_agent,
        'Accept': 'application/json',
        'X-IG-App-ID': '1217981644879628',
        'X-CSRFToken': csrf_token,
    }
    for attempt in range(retries):
        try:
            response = requests.get(f'https://i.instagram.com/api/v1/users/{user_id}/info/', headers=headers, cookies={'Cookie': cookie}, timeout=15)
            response.raise_for_status()
            data = response.json()
            if 'user' in data and 'username' in data['user'] and 'pk' in data['user']:
                user = data['user']['username']
                id = data['user']['pk']
                save_cookie_info({
                    'cookie': cookie,
                    'username': user,
                    'user_id': id,
                    'status': 'live',
                    'last_checked': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })
                return user, id
            print("\033[1;31mPhản hồi thiếu thông tin user/username/pk")
        except requests.exceptions.RequestException as e:
            if response.status_code == 429:
                print(f'\033[1;31m[429] Quá nhiều yêu cầu, thử lại sau {5 * (attempt + 1)} giây...')
                sleep(5 * (attempt + 1))
            else:
                print(f'\033[1;31m[Lỗi mạng] {str(e)}, thử lại lần {attempt + 1}/{retries}...')
                sleep(5)
    save_cookie_info({
        'cookie': cookie,
        'username': None,
        'user_id': None,
        'status': 'die',
        'last_checked': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })
    return 'die', 'die'

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
        open('ck.txt', 'w', encoding='utf-8').close()
        return True
    except Exception as e:
        print(f"\033[1;31mLỗi khi xóa file cookie: {e}")
        return False

def load_cookies_from_txt():
    live_cookies = []
    try:
        if os.path.exists('ck.txt'):
            with open('ck.txt', 'r', encoding='utf-8') as f:
                cookies = [c.strip() for c in f.read().splitlines() if c.strip()]
            for cookie in cookies:
                ten = name(cookie)
                if ten[0] != 'die':
                    live_cookies.append(cookie)
                    print(f'User Instagram: {cam}{ten[0]}{trang} - Live')
                else:
                    print(f'Cookie: {cookie[:20]}... - Die')
            print(f'\033[1;97m[\033[1;91m❣\033[1;97m] \033[1;36m✈  \033[1;32mSố cookie còn live: \033[1;33m{len(live_cookies)}')
        return live_cookies
    except Exception as e:
        print(f"\033[1;31mLỗi khi đọc file cookie: {e}")
        return []

def bongoc(so):
    try:
        print("────" * so)
    except Exception as e:
        print(f"\033[1;31mLỗi khi in đường gạch ngang: {e}")

def like(id, cookie):
    try:
        endpoints = [
            "https://www.instagram.com/web/likes/{id}/like/",
            "https://i.instagram.com/api/v1/media/{id}/like/",
            "https://www.instagram.com/api/v1/web/likes/{id}/like/",
        ]
        headers = {
            "x-ig-app-id": "1217981644879628",
            "accept": "*/*",
            "content-type": "application/x-www-form-urlencoded",
            "user-agent": random.choice(USER_AGENTS),
            "x-csrftoken": cookie.split('csrftoken=')[1].split(';')[0] if 'csrftoken=' in cookie else "",
            "x-requested-with": "XMLHttpRequest",
            "cookie": cookie
        }
        for endpoint_template in endpoints:
            endpoint = endpoint_template.format(id=id)
            try:
                response = requests.post(endpoint, headers=headers, timeout=15)
                response.raise_for_status()
                if 'ok' in response.text.lower():
                    return '2'
                elif 'post_not_found' in response.text.lower() or response.status_code == 404:
                    return '0'
                print(f"\033[1;31mEndpoint {endpoint} lỗi: {response.text[:100]}... Thử endpoint tiếp theo.")
            except requests.exceptions.RequestException as e:
                if hasattr(e.response, 'status_code') and e.response.status_code == 404:
                    return '0'
                print(f"\033[1;31mLỗi với endpoint {endpoint}: {e}. Thử endpoint tiếp theo.")
                continue
        print(f"\033[1;31mĐã thử tất cả endpoint cho ID {id} nhưng vẫn lỗi. Bỏ qua job.")
        return '1'
    except Exception as e:
        print(f"\033[1;31mLỗi không xác định trong quá trình like: {e}")
        return '1'

def get_id(link, cookie=None):
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_'
    try:
        match = re.search(r'/p/([A-Za-z0-9_-]+)', link)
        if not match:
            print(f"\033[1;31mKhông tìm thấy shortcode trong URL: {link}")
            return False
        shortcode = match.group(1)
        media_id = 0
        for char in shortcode:
            if char not in alphabet:
                print(f"\033[1;31mKý tự không hợp lệ trong shortcode: {char} | URL: {link}")
                return False
            media_id = (media_id * 64) + alphabet.index(char)
        return str(media_id)
    except Exception as e:
        print(f"\033[1;31mLỗi khi trích xuất ID từ URL: {e} | URL: {link}")
        return False

def follow(id, cookie):
    try:
        user_ig, _ = name(cookie)
        if user_ig == 'die':
            print(f"\033[1;31mCookie đã hết hạn, bỏ qua: {cookie[:20]}...")
            return '1'
        endpoints = [
            f"https://www.instagram.com/api/v1/friendships/create/{id}/",
            f"https://i.instagram.com/api/v1/friendships/create/{id}/",
            f"https://i.instagram.com/api/v1/friendships/follow/{id}/",
        ]
        csrftoken = cookie.split('csrftoken=')[1].split(';')[0] if 'csrftoken=' in cookie else ""
        headers = {
            "accept": "application/json",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "user-agent": random.choice(USER_AGENTS),
            "x-csrftoken": csrftoken,
            "x-ig-app-id": "1217981644879628",
            "x-requested-with": "XMLHttpRequest",
            "x-ig-www-claim": "0",
            "x-instagram-ajax": "1000000000",
            "cookie": cookie,
            "origin": "https://www.instagram.com",
            "referer": "https://www.instagram.com/"
        }
        data = {
            "user_id": id,
            "radio_type": "wifi-none",
            "container_module": "profile",
            "_uid": cookie.split('ds_user_id=')[1].split(';')[0] if 'ds_user_id=' in cookie else "",
        }
        for endpoint in endpoints:
            if "i.instagram.com" in endpoint:
                headers["authority"] = "i.instagram.com"
            else:
                headers["authority"] = "www.instagram.com"
            try:
                response = requests.post(endpoint, headers=headers, data=data, timeout=15)
                if response.status_code == 200:
                    json_response = response.json()
                    if json_response.get("status") == "ok":
                        print(f"\033[1;32m[DEBUG] Sử dụng {endpoint} - Thành công")
                        return '2'
                    elif json_response.get("message") == "User not found":
                        print(f"\033[1;31m[DEBUG] {endpoint} - User không tồn tại")
                        return '0'
                    else:
                        print(f"\033[1;31m[DEBUG] {endpoint} lỗi: {json_response.get('message', 'Không rõ')}")
                elif response.status_code == 404:
                    print(f"\033[1;31m[DEBUG] {endpoint} - Job không tồn tại")
                    return '0'
                elif response.status_code == 429:
                    print(f"\033[1;31m[DEBUG] {endpoint} - [429] Quá nhiều yêu cầu")
                    delay_with_backoff(attempts=3, base_delay=30)
                else:
                    print(f"\033[1;31m[DEBUG] {endpoint} lỗi HTTP {response.status_code}: {response.text[:100]}...")
                print(f"\033[1;31mLỗi với endpoint {endpoint}. Thử endpoint tiếp theo.")
            except requests.exceptions.RequestException as e:
                print(f"\033[1;31mLỗi kết nối với {endpoint}: {str(e)}. Thử endpoint tiếp theo.")
                continue
        print(f"\033[1;31mĐã thử tất cả endpoint cho ID {id} nhưng vẫn lỗi. Bỏ qua job.")
        return '1'
    except Exception as e:
        print(f"\033[1;31mLỗi không xác định: {str(e)}")
        return '1'

def cau_hinh(id_ig, ckvp):
    try:
        headers = {
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'accept': '*/*',
            'x-requested-with': 'XMLHttpRequest',
            'user-agent': random.choice(USER_AGENTS),
            'cookie': ckvp
        }
        response = requests.post('https://vipig.net/cauhinh/datnick.php', headers=headers, data={'iddat[]': id_ig}, timeout=15)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"\033[1;31mLỗi trong quá trình cấu hình: {e}")
        return "error"

try:
    os.system("cls" if os.name == "nt" else "clear")
    banner()
    check_update_on_startup()
    
    tokens = load_tokens()
    if tokens:
        print("\033[1;33mDanh sách token đã lưu:")
        for i, t in enumerate(tokens, 1):
            print(f"{i}. {t['user']} - {t['token'][:10]}...")
        choice = input('\033[1;97m[\033[1;91m❣\033[1;97m] \033[1;36m✈  \033[1;32mChọn token (nhập số) hoặc nhấn Enter để nhập token mới: \033[1;33m')
        if choice.isdigit() and 1 <= int(choice) <= len(tokens):
            token = tokens[int(choice) - 1]['token']
            user = tokens[int(choice) - 1]['user']
            xu = coin(cookie(token))
            ckvp = cookie(token)
            if ckvp:
                print('\033[1;97m[\033[1;91m❣\033[1;97m] \033[1;36m✈  \033[1;32mĐăng Nhập Thành Công')
            else:
                print('\033[1;31mKhông thể lấy cookie từ token, vui lòng thử lại')
                sys.exit()
        else:
            token = input('\033[1;97m[\033[1;91m❣\033[1;97m] \033[1;36m✈  \033[1;32mNhập Access_Token Vipig:\033[1;33m ')
            log = requests.post('https://vipig.net/logintoken.php', headers={'Content-type': 'application/x-www-form-urlencoded'}, data={'access_token': token}, timeout=15).json()
            if log.get('status') == 'success':
                user = log['data']['user']
                xu = log['data']['sodu']
                ckvp = cookie(token)
                if ckvp:
                    save_token(token, user)
                    print('\033[1;97m[\033[1;91m❣\033[1;97m] \033[1;36m✈  \033[1;32mĐăng Nhập Thành Công')
                else:
                    print('\033[1;31mKhông thể lấy cookie từ token')
                    sys.exit()
            else:
                print(log.get('mess', 'Đăng nhập thất bại'))
                sys.exit()
    else:
        token = input('\033[1;97m[\033[1;91m❣\033[1;97m] \033[1;36m✈  \033[1;32mNhập Access_Token Vipig:\033[1;33m ')
        log = requests.post('https://vipig.net/logintoken.php', headers={'Content-type': 'application/x-www-form-urlencoded'}, data={'access_token': token}, timeout=15).json()
        if log.get('status') == 'success':
            user = log['data']['user']
            xu = log['data']['sodu']
            ckvp = cookie(token)
            if ckvp:
                save_token(token, user)
                print('\033[1;97m[\033[1;91m❣\033[1;97m] \033[1;36m✈  \033[1;32mĐăng Nhập Thành Công')
            else:
                print('\033[1;31mKhông thể lấy cookie từ token')
                sys.exit()
        else:
            print(log.get('mess', 'Đăng nhập thất bại'))
            sys.exit()
    
    bongoc(14)
    list_cookie = []
    choice = input('\033[1;97m[\033[1;91m❣\033[1;97m] \033[1;36m✈  \033[1;32mBạn có muốn dùng lại các cookie cũ không? (y/n):\033[1;33m ').lower()
    
    if choice == 'n':
        clear_cookie_file()
        print('[LƯU Ý] Muốn Dừng Thì Nhấn Enter')
        x = 0
        while True:
            x += 1
            cookie_input = input(f'\033[1;97m[\033[1;91m❣\033[1;97m] \033[1;36m✈  \033[1;32mNhập Cookie Instagram Thứ {x}:\033[1;33m ')
            if not cookie_input and x > 1:
                break
            ten = name(cookie_input)
            if ten[0] != 'die':
                print(f'User Instagram: {cam}{ten[0]}{trang} ')
                list_cookie.append(cookie_input)
                save_cookie_to_txt(cookie_input)
                bongoc(14)
                sleep(1)
            else:
                print('\033[1;31mCookie Instagram Sai ! Vui Lòng Nhập Lại ! ! ! ')
                x -= 1
                bongoc(14)
    elif choice == 'y':
        list_cookie = load_cookies_from_txt()
        if not list_cookie:
            print('\033[1;31mKhông có cookie nào trong file ck.txt! Vui lòng nhập cookie mới.')
            clear_cookie_file()
            x = 0
            print('[LƯU Ý] Muốn Dừng Thì Nhấn Enter')
            while True:
                x += 1
                cookie_input = input(f'\033[1;97m[\033[1;91m❣\033[1;97m] \033[1;36m✈  \033[1;32mNhập Cookie Instagram Thứ {x}:\033[1;33m ')
                if not cookie_input and x > 1:
                    break
                ten = name(cookie_input)
                if ten[0] != 'die':
                    print(f'User Instagram: {cam}{ten[0]}{trang} ')
                    list_cookie.append(cookie_input)
                    save_cookie_to_txt(cookie_input)
                    bongoc(14)
                    sleep(1)
                else:
                    print('\033[1;31mCookie Instagram Sai ! Vui Lòng Nhập Lại ! ! ! ')
                    x -= 1
                    bongoc(14)
    else:
        print('\033[1;31mLựa chọn không hợp lệ! Thoát chương trình.')
        sys.exit()
    
    os.system("cls" if os.name == "nt" else "clear")
    banner()
    print(f"""\033[1;97m[\033[1;91m❣\033[1;97m] \033[1;36m✈  \033[1;32mTên Tài Khoản: \033[1;33m{user}
\033[1;97m[\033[1;91m❣\033[1;97m] \033[1;36m✈  \033[1;32mXu Hiện Tại: \033[1;33m{xu}
\033[1;97m[\033[1;91m❣\033[1;97m] \033[1;36m✈  \033[1;32mSố Cookie: \033[1;33m{len(list_cookie)}""")
    bongoc(14)
    print("""\033[1;97m[\033[1;91m❣\033[1;97m] \033[1;36m✈  \033[1;32mNhập [1] Để Chạy Nhiệm Vụ Like - đang lỗi
\033[1;97m[\033[1;91m❣\033[1;97m] \033[1;36m✈  \033[1;32mNhập [2] Để Chạy Nhiệm Vụ Follow
\033[1;97m[\033[1;91m❣\033[1;97m] \033[1;36m✈  \033[1;32mCó Thể Chọn Nhiều Nhiệm Vụ \033[1;33m(Ví Dụ 12)""")
    chon = input('\033[1;97m[\033[1;91m❣\033[1;97m] \033[1;36m✈  \033[1;32mNhập Số Để Chạy Nhiệm Vụ:\033[1;33m ')
    bongoc(14)
    dl = int(input('\033[1;97m[\033[1;91m❣\033[1;97m] \033[1;36m✈  \033[1;32mNhập Delay (giây):\033[1;33m '))
    chong_block = int(input('Sau bao nhiêu nhiệm vụ thì kích hoạt chống block: '))
    delay_block = int(input(f'Sau {chong_block} nhiệm vụ nghỉ ngơi bao nhiêu giây: '))
    
    done_jobs = {}
    success_counts = {}
    SUCCESS_THRESHOLD = 6

    while True:
        if not list_cookie:
            print('\033[1;31mToàn bộ cookie đã hết hạn! Vui lòng nhập lại.')
            clear_cookie_file()
            x = 0
            while True:
                x += 1
                cookie_input = input(f'\033[1;97m[\033[1;91m❣\033[1;97m] \033[1;36m✈  \033[1;32mNhập Cookie Instagram Thứ {x}:\033[1;33m ')
                if not cookie_input and x > 1:
                    break
                ten = name(cookie_input)
                if ten[0] != 'die':
                    print(f'User Instagram: {cam}{ten[0]}{trang} ')
                    list_cookie.append(cookie_input)
                    save_cookie_to_txt(cookie_input)
                    bongoc(14)
                    sleep(1)
                else:
                    print('\033[1;31mCookie Instagram Sai! Vui lòng nhập lại!')
                    x -= 1
                    bongoc(14)
        
        i = 0
        while i < len(list_cookie):
            cookie = list_cookie[i]
            anorin = 0
            user_ig, id_ig = name(cookie)
            if user_ig == 'die':
                print(f'\033[1;31mCookie {i+1} đã die, xóa khỏi danh sách')
                list_cookie.pop(i)
                continue
            ngoc = cau_hinh(id_ig, ckvp)
            if ngoc == '1':
                bongoc(14)
                print(f'Đang cấu hình ID: {id_ig} | User: {cam}{user_ig}{trang}')
                bongoc(14)
            else:
                print(f'Cấu hình thất bại ID: {id_ig} | User: {cam}{user_ig}{trang} ')
                delay(2)
                i += 1
                continue
            
            if id_ig not in done_jobs:
                done_jobs[id_ig] = set()
            if id_ig not in success_counts:
                success_counts[id_ig] = 0

            while True:
                if anorin in (1, 2):
                    break
                
                if '1' in chon:
                    get_like = get_nv('', ckvp)
                    if not isinstance(get_like, list):
                        print('\033[1;31mPhản hồi từ API không phải danh sách nhiệm vụ')
                        delay(2)
                        continue
                    if not get_like:
                        print('Tạm thời hết nhiệm vụ Like', '     ', end='\r')
                    else:
                        print(f'Tìm thấy {len(get_like)} nhiệm vụ Like', '     ', end='\r')
                    fail_count = 0
                    for x in get_like:
                        if not isinstance(x, dict) or 'link' not in x or 'idpost' not in x:
                            print('\033[1;31mDữ liệu nhiệm vụ không hợp lệ')
                            continue
                        link = x['link']
                        uid = x['idpost']
                        id = get_id(link)
                        if not id:
                            continue
                        if uid in done_jobs[id_ig]:
                            print(f'[{dem}] | LIKE | {id} | TRÙNG JOB')
                            fail_count += 1
                            if fail_count >= 6:
                                print(f'{red}Đã gặp lỗi {fail_count} lần liên tiếp. Đổi cookie...')
                                anorin = 1
                                break
                            continue
                        lam = like(id, cookie)
                        if lam == '2':
                            dem += 1
                            fail_count = 0
                            done_jobs[id_ig].add(uid)
                            print(f'[{dem}] | LIKE | {id} | SUCCESS')
                            xu_old = coin(ckvp)
                            nhan = nhan_tien(uid, ckvp, '')
                            if nhan['status'] == 'success':
                                sleep(2)
                                xu = coin(ckvp)
                                xu_old_int = int(xu_old) if xu_old.isdigit() else 0
                                xu_new_int = int(xu) if xu.isdigit() else 0
                                if xu_new_int > xu_old_int:
                                    print(f'| LIKE | Nhận xu thành công | Tổng xu: {xu} (+{xu_new_int - xu_old_int})')
                                else:
                                    print(f'| LIKE | Server báo thành công nhưng số xu không tăng | Tổng xu: {xu} | Kiểm tra web để xác nhận')
                            else:
                                print(f'| LIKE | {id} | ERROR NHẬN XU: {nhan["response"]} (Thử {nhan["attempt"]} lần)')
                            if dem % chong_block == 0:
                                delay(delay_block)
                            else:
                                delay(random.uniform(dl, dl + 2))
                        elif lam == '0':
                            print(f'[{dem}] | LIKE | {id} | JOB KHÔNG TỒN TẠI')
                            fail_count += 1
                            if fail_count >= 6:
                                print(f'{red}Đã gặp lỗi {fail_count} lần liên tiếp. Đổi cookie...')
                                anorin = 1
                                break
                            delay(random.uniform(dl, dl + 2))
                        elif lam == '1':
                            user_ig, _ = name(cookie)
                            if user_ig == 'die':
                                print(f'\033[1;31mCookie của {cam}{user_ig}{trang} đã die')
                                anorin = 2
                                break
                            print(f'\033[1;31mTài khoản {cam}{user_ig}{trang} bị chặn Like')
                            anorin = 2
                            break
                
                if anorin in (1, 2):
                    break
                
                if '2' in chon:
                    # Kiểm tra cookie trước khi chạy job Follow
                    user_ig, id_ig = name(cookie)
                    if user_ig == 'die':
                        print(f'\033[1;31mCookie {i+1} đã die trước khi chạy Follow, xóa khỏi danh sách')
                        list_cookie.pop(i)
                        break
                    print(f'\033[1;32mCookie {i+1} ({cam}{user_ig}{trang}) đang live, bắt đầu chạy job Follow')
                    
                    get_sub = get_nv('/subcheo', ckvp)
                    if not isinstance(get_sub, list):
                        print('\033[1;31mPhản hồi từ API không phải danh sách nhiệm vụ')
                        delay(2)
                        continue
                    if not get_sub:
                        print('Tạm thời hết nhiệm vụ Follow', '     ', end='\r')
                    else:
                        print(f'Tìm thấy {len(get_sub)} nhiệm vụ Follow', '     ', end='\r')
                    fail_count = 0
                    for x in get_sub:
                        if not isinstance(x, dict) or 'soID' not in x:
                            print('\033[1;31mDữ liệu nhiệm vụ không hợp lệ')
                            continue
                        id = x['soID']
                        if id in done_jobs[id_ig]:
                            print(f'[{dem}] | FOLLOW | {id} | TRÙNG JOB')
                            fail_count += 1
                            if fail_count >= 6:
                                print(f'{red}Đã gặp lỗi {fail_count} lần liên tiếp. Đổi cookie...')
                                anorin = 1
                                break
                            continue
                        lam = follow(id, cookie)
                        if lam == '2':
                            success_counts[id_ig] += 1
                            dem += 1
                            fail_count = 0
                            done_jobs[id_ig].add(id)
                            print(f'[{dem}] | FOLLOW | {id} | SUCCESS | Thành công: {success_counts[id_ig]}/{SUCCESS_THRESHOLD}')
                            with open(f"{id_ig}.txt", "a+") as data_id:
                                data_id.write(f"{id},")
                            if success_counts[id_ig] >= SUCCESS_THRESHOLD:
                                with open(f"{id_ig}.txt", "r") as data_id:
                                    list_data = data_id.read()
                                if list_data:
                                    nhan = nhan_sub(list_data, ckvp)
                                    if 'error' not in nhan:
                                        xu_them = nhan.get('sodu', 0)
                                        job = xu_them // 600
                                        xu = coin(ckvp)
                                        print(f'Nhận thành công {job} nhiệm vụ Follow | +{xu_them} | {xu}')
                                        os.remove(f"{id_ig}.txt")
                                        open(f"{id_ig}.txt", "w").close()
                                        success_counts[id_ig] = 0
                                        anorin = 1  # Đổi cookie sau khi nhận xu thành công
                                        break
                                    else:
                                        print(f'[{dem}] | FOLLOW | {id} | ERROR NHẬN XU')
                            if dem % chong_block == 0:
                                delay(delay_block)
                            else:
                                delay(random.uniform(dl, dl + 2))
                        elif lam == '0':
                            print(f'[{dem}] | FOLLOW | {id} | JOB KHÔNG TỒN TẠI')
                            fail_count += 1
                            if fail_count >= 6:
                                print(f'{red}Đã gặp lỗi {fail_count} lần liên tiếp. Đổi cookie...')
                                anorin = 1
                                break
                            delay(random.uniform(dl, dl + 2))
                        elif lam == '1':
                            user_ig, _ = name(cookie)
                            if user_ig == 'die':
                                print(f'\033[1;31mCookie của {cam}{user_ig}{trang} đã die')
                            else:
                                print(f'\033[1;31mTài khoản {cam}{user_ig}{trang} gặp vấn đề khi Follow')
                            anorin = 2
                            break
            if anorin in (1, 2):
                i += 1  # Chuyển sang cookie tiếp theo

except KeyboardInterrupt:
    print("\n\033[1;31mĐã dừng chương trình theo yêu cầu người dùng")
except Exception as e:
    print(f"\033[1;31mLỗi chương trình nghiêm trọng: {e}")
    traceback.print_exc()
