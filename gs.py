import json
import requests, os, sys, re
from time import sleep
import random
import shutil
import traceback
import datetime

# Thông tin phiên bản của tool
VERSION = "1.6"
GITHUB_RAW_URL = "https://raw.githubusercontent.com/Dat075/vipig123/refs/heads/main/gs.py"
GITHUB_VERSION_URL = "https://raw.githubusercontent.com/Dat075/vipig123/refs/heads/main/version.txt"

# Danh sách User-Agent (đã tắt random)
USER_AGENT = "Instagram 261.0.0.21.111 Android (30/11; 420dpi; 1080x2130; Samsung; SM-G973F; beyond1; qcom; en_US)"

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
        headers = {'user-agent': USER_AGENT, 'cookie': ckvp}
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
            'user-agent': USER_AGENT,
            'cookie': ckvp
        }
        response = requests.post(f'https://vipig.net/kiemtien{type}/getpost.php', headers=headers, timeout=15)
        response.raise_for_status()
        jobs = response.json()
        # Lọc job không hợp lệ
        valid_jobs = []
        for job in jobs:
            if isinstance(job, dict):
                if type == '' and 'link' in job and 'idpost' in job and job['link'] and job['idpost']:
                    valid_jobs.append(job)
                elif type == '/subcheo' and 'soID' in job and job['soID']:
                    valid_jobs.append(job)
        return valid_jobs
    except Exception as e:
        print(f"\033[1;31mLỗi khi lấy nhiệm vụ {type}: {e}")
        return []

def nhan_tien(list, ckvp, type, retries=3):
    data = f'id={list}'
    headers = {
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'accept': '*/*',
        'x-requested-with': 'XMLHttpRequest',
        'user-agent': USER_AGENT,
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
            if response.status_code == 404:
                return {'status': 'not_found', 'response': 'Job không tồn tại', 'attempt': attempt + 1}
            status = 'success' if 'thành công' in str(result).lower() else 'fail'
            return {'status': status, 'response': result, 'attempt': attempt + 1}
        except requests.exceptions.RequestException as e:
            if hasattr(e.response, 'status_code') and e.response.status_code == 429:
                print(f"\033[1;31m[429] Quá nhiều yêu cầu, nghỉ {5 * (attempt + 1)} giây...")
                sleep(5 * (attempt + 1))
            elif hasattr(e.response, 'status_code') and e.response.status_code == 404:
                return {'status': 'not_found', 'response': 'Job không tồn tại', 'attempt': attempt + 1}
            else:
                print(f"\033[1;31mLỗi khi nhận xu (lần {attempt + 1}/{retries}): {e}")
            if attempt < retries - 1:
                sleep(5 * (attempt + 1))
            else:
                return {'status': 'error', 'response': str(e), 'attempt': retries}

def nhan_sub(list, ckvp, retries=3):
    try:
        data = f'id={list.rstrip(",")}'
        headers = {
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'accept': '*/*',
            'x-requested-with': 'XMLHttpRequest',
            'user-agent': USER_AGENT,
            'cookie': ckvp
        }
        for attempt in range(retries):
            try:
                response = requests.post('https://vipig.net/kiemtien/subcheo/nhantien2.php', headers=headers, data=data, timeout=15)
                response.raise_for_status()
                result = response.json()
                if response.status_code == 404:
                    return {'status': 'not_found', 'response': 'Job không tồn tại', 'attempt': attempt + 1}
                return result
            except requests.exceptions.RequestException as e:
                if hasattr(e.response, 'status_code') and e.response.status_code == 429:
                    print(f"\033[1;31m[429] Quá nhiều yêu cầu, nghỉ {5 * (attempt + 1)} giây...")
                    sleep(5 * (attempt + 1))
                elif hasattr(e.response, 'status_code') and e.response.status_code == 404:
                    return {'status': 'not_found', 'response': 'Job không tồn tại', 'attempt': attempt + 1}
                else:
                    print(f"\033[1;31mLỗi khi nhận sub (lần {attempt + 1}/{retries}): {e}")
                if attempt < retries - 1:
                    sleep(5 * (attempt + 1))
                else:
                    return {"error": str(e), "attempt": retries}
    except Exception as e:
        print(f"\033[1;31mLỗi khi nhận sub: {e}")
        return {"error": str(e)}

def delay(dl):
    try:
        start_time = datetime.datetime.now()
        for i in range(int(dl), -1, -1):
            print(f'[AN ORIN][{i} Giây]           ', end='\r')
            sleep(1)
        elapsed = (datetime.datetime.now() - start_time).total_seconds()
        if abs(elapsed - dl) > 1:
            print(f"\n\033[1;33m[DEBUG] Delay thực tế: {elapsed:.2f} giây, mong muốn: {dl} giây")
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
    user_agent = USER_AGENT
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
        'Cookie': cookie
    }
    for attempt in range(retries):
        try:
            response = requests.get(
                f'https://i.instagram.com/api/v1/users/{user_id}/info/',
                headers=headers,
                timeout=15
            )
            response.raise_for_status()
            data = response.json()
            if 'user' in data and 'username' in data['user'] and 'pk' in data['user']:
                user = data['user']['username']
                id = data['user']['pk']
                return user, id
            print("\033[1;31mPhản hồi thiếu thông tin user/username/pk")
        except requests.exceptions.RequestException as e:
            if hasattr(e.response, 'status_code') and e.response.status_code == 429:
                print(f'\033[1;31m[429] Quá nhiều yêu cầu, thử lại sau {5 * (attempt + 1)} giây...')
                sleep(5 * (attempt + 1))
            else:
                print(f'\033[1;31m[Lỗi mạng] {str(e)}, thử lại lần {attempt + 1}/{retries}...')
                sleep(5)
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
    new_cookies = []
    ck_file = 'ck.txt'
    try:
        if not os.path.exists(ck_file):
            print(f"\033[1;31mKhông tìm thấy file {ck_file}")
            return []
        with open(ck_file, 'r', encoding='utf-8') as f:
            cookies = [line.strip() for line in f if line.strip()]
        for cookie in cookies:
            user, _ = name(cookie)
            if user != 'die':
                print(f'User Instagram: {cam}{user}{trang} - Live')
                live_cookies.append(cookie)
                new_cookies.append(cookie)
            else:
                print(f'Cookie: {cookie[:20]}... - Die (Đã loại bỏ)')
        if set(cookies) != set(new_cookies):
            with open(ck_file, 'w', encoding='utf-8') as f:
                for c in new_cookies:
                    f.write(c + '\n')
            print(f'\033[1;32mĐã cập nhật file ck.txt, chỉ còn {len(new_cookies)} cookie live.')
        else:
            print(f'\033[1;33mKhông có thay đổi trong file ck.txt.')
        return live_cookies
    except Exception as e:
        print(f"\033[1;31mLỗi khi xử lý file ck.txt: {e}")
        return []

def bongoc(so):
    try:
        print("────" * so)
    except Exception as e:
        print(f"\033[1;31mLỗi khi in đường gạch ngang: {e}")

def check_media_exists(media_id, cookie):
    try:
        headers = {
            "x-ig-app-id": "1217981644879628",
            "accept": "application/json",
            "user-agent": USER_AGENT,
            "x-csrftoken": cookie.split('csrftoken=')[1].split(';')[0] if 'csrftoken=' in cookie else "",
            "cookie": cookie
        }
        response = requests.get(f"https://i.instagram.com/api/v1/media/{media_id}/info/", headers=headers, timeout=10)
        if response.status_code == 200 and response.json().get("status") == "ok":
            return True
        return False
    except Exception as e:
        print(f"\033[1;31mLỗi kiểm tra media {media_id}: {e}")
        return False

def check_user_exists(user_id, cookie):
    try:
        headers = {
            "x-ig-app-id": "1217981644879628",
            "accept": "application/json",
            "user-agent": USER_AGENT,
            "x-csrftoken": cookie.split('csrftoken=')[1].split(';')[0] if 'csrftoken=' in cookie else "",
            "cookie": cookie
        }
        response = requests.get(f"https://i.instagram.com/api/v1/users/{user_id}/info/", headers=headers, timeout=10)
        if response.status_code == 200 and response.json().get("status") == "ok":
            return True
        return False
    except Exception as e:
        print(f"\033[1;31mLỗi kiểm tra user {user_id}: {e}")
        return False

def log_job_error(job_id, job_type, error_message):
    try:
        with open('job_errors.log', 'a', encoding='utf-8') as f:
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f"[{timestamp}] {job_type} | ID: {job_id} | Error: {error_message}\n")
    except Exception as e:
        print(f"\033[1;31mLỗi khi ghi log: {e}")

def save_done_jobs(done_jobs):
    try:
        with open('done_jobs.json', 'w', encoding='utf-8') as f:
            json.dump({k: list(v) for k, v in done_jobs.items()}, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"\033[1;31mLỗi khi lưu done_jobs: {e}")

def load_done_jobs():
    try:
        if os.path.exists('done_jobs.json'):
            with open('done_jobs.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                return {k: set(v) for k, v in data.items()}
        return {}
    except Exception as e:
        print(f"\033[1;31mLỗi khi đọc done_jobs: {e}")
        return {}

def save_pending_like_jobs(pending_jobs):
    try:
        with open('pending_like_jobs.json', 'w', encoding='utf-8') as f:
            json.dump(pending_jobs, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"\033[1;31mLỗi khi lưu pending_like_jobs: {e}")

def load_pending_like_jobs():
    try:
        if os.path.exists('pending_like_jobs.json'):
            with open('pending_like_jobs.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                return {k: list(v) for k, v in data.items()}
        return {}
    except Exception as e:
        print(f"\033[1;31mLỗi khi đọc pending_like_jobs: {e}")
        return {}

def like(id, cookie):
    if not check_media_exists(id, cookie):
        log_job_error(id, "LIKE", "Bài viết không tồn tại hoặc đã bị xóa")
        return '0'
    try:
        endpoints = [
            #"https://i.instagram.com/api/v1/media/{id}/like/",
            "https://www.instagram.com/api/v1/web/likes/{id}/like/",
        ]
        headers = {
            "x-ig-app-id": "1217981644879628",
            "accept": "*/*",
            "content-type": "application/x-www-form-urlencoded",
            "user-agent": USER_AGENT,
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
                    log_job_error(id, "LIKE", "Bài viết không tồn tại")
                    return '0'
                print(f"\033[1;31mEndpoint {endpoint} lỗi: {response.text[:100]}... Thử endpoint tiếp theo.")
            except requests.exceptions.RequestException as e:
                if hasattr(e.response, 'status_code') and e.response.status_code == 404:
                    log_job_error(id, "LIKE", "Bài viết không tồn tại")
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
    if not check_user_exists(id, cookie):
        log_job_error(id, "FOLLOW", "Người dùng không tồn tại")
        return '0'
    try:
        user_ig, _ = name(cookie)
        if user_ig == 'die':
            print(f"\033[1;31mCookie đã hết hạn, bỏ qua: {cookie[:20]}...")
            return '1'
        
        # Kiểm tra trạng thái Follow
        check_endpoint = f"https://i.instagram.com/api/v1/friendships/show/{id}/"
        csrftoken = cookie.split('csrftoken=')[1].split(';')[0] if 'csrftoken=' in cookie else ""
        headers = {
            "accept": "application/json",
            "user-agent": USER_AGENT,
            "x-csrftoken": csrftoken,
            "x-ig-app-id": "1217981644879628",
            "cookie": cookie
        }
        response = requests.get(check_endpoint, headers=headers, timeout=15)
        if response.status_code == 200:
            json_response = response.json()
            if json_response.get("following") or json_response.get("is_private") and not json_response.get("followed_by"):
                print(f"\033[1;31m[DEBUG] Không thấy nút Follow cho user {id} (Đã follow hoặc tài khoản riêng tư)")
                log_job_error(id, "FOLLOW", "Không thấy nút Follow")
                return '0'
        else:
            print(f"\033[1;31m[DEBUG] Lỗi kiểm tra trạng thái Follow cho user {id}: {response.status_code}")
            log_job_error(id, "FOLLOW", f"Lỗi kiểm tra trạng thái: {response.status_code}")
            return '0'

        # Tiến hành follow nếu kiểm tra OK
        endpoints = [
            f"https://www.instagram.com/api/v1/friendships/create/{id}/",
            f"https://i.instagram.com/api/v1/friendships/create/{id}/",
            f"https://i.instagram.com/api/v1/friendships/follow/{id}/",
        ]
        headers = {
            "accept": "application/json",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "user-agent": USER_AGENT,
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
                    elif json_response.get("message") == " Analysis of the website failed. Please try again.":
                        log_job_error(id, "FOLLOW", "Người dùng không tồn tại")
                        print(f"\033[1;31m[DEBUG] {endpoint} - User không tồn tại")
                        return '0'
                    else:
                        print(f"\033[1;31m[DEBUG] {endpoint} lỗi: {json_response.get('message', 'Không rõ')}")
                elif response.status_code == 404:
                    log_job_error(id, "FOLLOW", "Job không tồn tại")
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
            'user-agent': USER_AGENT,
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
    doi_acc_sau = int(input('\033[1;97m[\033[1;91m❣\033[1;97m] \033[1;36m✈  \033[1;32mSau bao nhiêu nhiệm vụ thì đổi acc (khuyến nghị để mặc định):\033[1;33m '))
    chong_block = int(input('Sau bao nhiêu nhiệm vụ thì kích hoạt chống block: '))
    delay_block = int(input(f'Sau {chong_block} nhiệm vụ nghỉ ngơi bao nhiêu giây: '))
    
    done_jobs = load_done_jobs()
    success_counts = {}
    SUCCESS_THRESHOLD = 6  # Mặc định nhận xu sau 6 job
    pending_like_jobs = load_pending_like_jobs()  # Tải danh sách job Like đang chờ

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
            if id_ig not in pending_like_jobs:
                pending_like_jobs[id_ig] = []

            while True:
                if anorin in (1, 2):
                    save_pending_like_jobs(pending_like_jobs)
                    break
                
                if '1' in chon:
                    get_like = get_nv('', ckvp)
                    if not isinstance(get_like, list):
                        delay(2)
                        continue
                    if not get_like:
                        print('Tạm thời hết nhiệm vụ Like', '     ', end='\r')
                    else:
                        print(f'Tìm thấy {len(get_like)} nhiệm vụ Like', '     ', end='\r')

                    fail_count = 0
                    for x in get_like:
                        link = x.get('link')
                        uid = x.get('idpost')
                        if not link or not uid:
                            log_job_error(uid or "unknown", "LIKE", "Dữ liệu nhiệm vụ không hợp lệ")
                            fail_count += 1
                            if fail_count >= 2:
                                print(f'{red}Đã gặp 2 lỗi liên tiếp (Dữ liệu không hợp lệ). Chuyển cookie...')
                                anorin = 1
                                break
                            continue

                        id = get_id(link)
                        if not id:
                            log_job_error(uid, "LIKE", "Không lấy được media ID")
                            fail_count += 1
                            if fail_count >= 2:
                                print(f'{red}Đã gặp 2 lỗi liên tiếp (Không lấy được media ID). Chuyển cookie...')
                                anorin = 1
                                break
                            continue

                        if uid in done_jobs[id_ig]:
                            print(f'[{dem}] | LIKE | {id} | TRÙNG JOB')
                            fail_count += 1
                            if fail_count >= 2:
                                print(f'{red}Đã gặp 2 lỗi liên tiếp (Job trùng). Chuyển cookie...')
                                anorin = 1
                                break
                            continue

                        lam = like(id, cookie)
                        if lam == '2':
                            dem += 1
                            fail_count = 0
                            done_jobs[id_ig].add(uid)
                            save_done_jobs(done_jobs)
                            tg = datetime.datetime.now().strftime('%H:%M')
                            print(f'[{dem}] | {tg} | LIKE | {id} | +300')

                            success_counts[id_ig] += 1
                            pending_like_jobs[id_ig].append(uid)
                            if success_counts[id_ig] >= SUCCESS_THRESHOLD:
                                for job_id in pending_like_jobs[id_ig]:
                                    nhan = nhan_tien(job_id, ckvp, '')
                                    if nhan['status'] == 'success':
                                        xu = coin(ckvp)
                                        print(f'Đã hoàn thành {SUCCESS_THRESHOLD} nhiệm vụ LIKE | Tổng xu hiện tại: {xu}')
                                    else:
                                        print(f'| LIKE | {job_id} | ERROR NHẬN XU: {nhan["response"]}')
                                pending_like_jobs[id_ig] = []
                                success_counts[id_ig] = 0
                                save_pending_like_jobs(pending_like_jobs)
                                print(f'\033[1;36mHoàn thành 6 job LIKE thành công, chuyển cookie...')
                                anorin = 1
                                break

                            if dem % chong_block == 0:
                                delay(delay_block)
                            else:
                                delay(random.uniform(dl, dl + 2))
                        else:
                            fail_count += 1
                            if fail_count >= 2:
                                print(f'{red}Đã gặp 2 lỗi liên tiếp (Lỗi API Like). Chuyển cookie...')
                                anorin = 1
                                break
                            if lam == '1':
                                user_ig, _ = name(cookie)
                                if user_ig == 'die':
                                    print(f'\033[1;31mCookie đã die, xóa khỏi danh sách')
                                    anorin = 2
                                    break
                                print(f'\033[1;31mTài khoản {cam}{user_ig}{trang} bị chặn Like')
                                anorin = 2
                                break
                            delay(random.uniform(dl, dl + 2))

                if anorin in (1, 2):
                    save_pending_like_jobs(pending_like_jobs)
                    break
                
                if '2' in chon:
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
                        id = x.get('soID')
                        if not id:
                            log_job_error(id or "unknown", "FOLLOW", "Dữ liệu nhiệm vụ không hợp lệ")
                            fail_count += 1
                            if fail_count >= 2:
                                print(f'{red}Đã gặp 2 lỗi liên tiếp (Dữ liệu không hợp lệ). Chuyển cookie...')
                                anorin = 1
                                break
                            continue

                        if id in done_jobs[id_ig]:
                            print(f'[{dem}] | FOLLOW | {id} | TRÙNG JOB')
                            fail_count += 1
                            if fail_count >= 2:
                                print(f'{red}Đã gặp 2 lỗi liên tiếp (Job trùng). Chuyển cookie...')
                                anorin = 1
                                break
                            continue

                        lam = follow(id, cookie)
                        if lam == '2':
                            dem += 1
                            fail_count = 0
                            done_jobs[id_ig].add(id)
                            save_done_jobs(done_jobs)
                            print(f'[{dem}] | FOLLOW | {id} | SUCCESS | Thành công: {success_counts[id_ig] + 1}/{SUCCESS_THRESHOLD}')

                            with open(f"{id_ig}.txt", "a+", encoding='utf-8') as data_id:
                                data_id.write(f"{id},")

                            success_counts[id_ig] += 1
                            if success_counts[id_ig] >= SUCCESS_THRESHOLD:
                                with open(f"{id_ig}.txt", "r", encoding='utf-8') as data_id:
                                    list_data = data_id.read()
                                if list_data:
                                    nhan = nhan_sub(list_data, ckvp)
                                    if 'error' not in nhan and nhan.get('status') != 'not_found':
                                        xu_them = nhan.get('sodu', 0)
                                        job = xu_them // 600
                                        xu = coin(ckvp)
                                        print(f'Nhận thành công {job} nhiệm vụ Follow | +{xu_them} | Tổng xu: {xu}')
                                        os.remove(f"{id_ig}.txt")
                                        open(f"{id_ig}.txt", "w", encoding='utf-8').close()
                                        success_counts[id_ig] = 0
                                        print(f'\033[1;36mHoàn thành 6 job FOLLOW thành công, chuyển cookie...')
                                        anorin = 1
                                        break
                                    else:
                                        print(f'[{dem}] | FOLLOW | {id} | ERROR NHẬN XU: {nhan.get("error", "Job không tồn tại")}')
                                if dem % chong_block == 0:
                                    delay(delay_block)
                                else:
                                    delay(random.uniform(dl, dl + 2))
                        else:
                            fail_count += 1
                            if fail_count >= 2:
                                print(f'{red}Đã gặp 2 lỗi liên tiếp (Lỗi API Follow). Chuyển cookie...')
                                anorin = 1
                                break
                            if lam == '1':
                                user_ig, _ = name(cookie)
                                if user_ig == 'die':
                                    print(f'\033[1;31mCookie của {cam}{user_ig}{trang} đã die')
                                else:
                                    print(f'\033[1;31mTài khoản {cam}{user_ig}{trang} gặp vấn đề khi Follow')
                                anorin = 2
                                break
                            delay(random.uniform(dl, dl + 2))
            if anorin in (1, 2):
                i += 1

except KeyboardInterrupt:
    print("\n\033[1;31mĐã dừng chương trình theo yêu cầu người dùng")
except Exception as e:
    print(f"\033[1;31mLỗi chương trình nghiêm trọng: {e}")
    traceback.print_exc()
