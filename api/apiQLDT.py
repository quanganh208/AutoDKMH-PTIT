import requests
import json
from datetime import datetime, timedelta
from colorama import Fore, init
from api.model import *


class ApiQLDT:
    def __init__(self, username, password):
        init(autoreset=True)
        self.host = 'https://qldt.ptit.edu.vn/api'
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded'})
        self.username = username
        self.password = password

        self.listCourse = []
        self.listCourseRegistration = []

    def initCourseRegistration(self):
        print(f"{Fore.LIGHTCYAN_EX}Đang khởi tạo...                    ", end='\r')
        try:
            self.session.headers.update({'Content-Type': 'application/json'})
            self.session.post(
                self.host + '/dkmh/w-checkvaliddangkymonhoc', timeout=60)
            data = {"ma_sv": self.username}
            self.session.post(
                self.host + '/sms/w-locketquaduyetsinhvien', json=data, timeout=60)
            data = {"ma_sinh_vien": self.username, "is_cam_xem_dkmh": True}
            self.session.post(
                self.host + 'srm/w-kiemtrasettinghoanthanhdg', json=data, timeout=60)
            self.session.post(
                self.host + '/api/dkmh/w-locdsdieukienloc', timeout=60)
            print(f"{Fore.GREEN}Khởi tạo thành công")
            return True
        except Exception:
            print(f"{Fore.RED}Khởi tạo thất bại, tiến hành thử lại", end='\r')
            return False

    def login(self):
        dataLogin = {
            'username': self.username,
            'password': self.password,
            'grant_type': 'password'
        }
        print(f"{Fore.LIGHTCYAN_EX}Đang đăng nhập", end='\r')
        response = self.session.post(
            self.host + '/auth/login', data=dataLogin, timeout=60).json()
        try:
            if response['code'] == '200':
                self.session.headers.update({
                    'Authorization': 'Bearer ' + response['access_token'],
                    'Idpc': response['idpc'], })
                print(f"{Fore.GREEN}Đăng nhập thành công")
                print(
                    f"Xin chào {Fore.BLUE}{response['name']}{Fore.RESET}. Mã sinh viên: {Fore.BLUE}{response['userName']}{Fore.RESET}")
                return True
            else:
                print(f"{Fore.RED}Đăng nhập thất bại")
                print(f"{Fore.LIGHTYELLOW_EX}Thông báo: {response['message']}")
        except Exception as e:
            writeLog(e, response)
        return False

    def registerCourse(self, id_to_hoc):
        data = {
            "filter": {
                "id_to_hoc": id_to_hoc,
                "is_checked": True,
                "sv_nganh": 1
            }
        }
        self.session.headers.update({'Content-Type': 'application/json'})
        try:
            response = self.session.post(
                self.host + '/dkmh/w-xulydkmhsinhvien', json=data, timeout=60).json()
            try:
                if self.checkExpired(response):
                    return False
                if response['code'] == 200:
                    time = datetime.now().strftime("%H:%M:%S")
                    print(time, end=' ')
                    if response['data']['is_thanh_cong']:
                        dt_object = datetime.fromisoformat(
                            response['data']['ket_qua_dang_ky']['ngay_dang_ky'])
                        dt_object_utc = dt_object - dt_object.utcoffset() + timedelta(hours=7)
                        formatted_time = dt_object_utc.strftime(
                            "%d/%m/%Y %H:%M:%S")
                        print(
                            f"{Fore.GREEN}Đăng ký môn thành công. Thời gian đăng ký: {formatted_time}")
                    else:
                        print(f"{Fore.LIGHTRED_EX}Đăng ký môn thất bại")
                        print(
                            f"{Fore.LIGHTYELLOW_EX}Thông báo: {response['data']['thong_bao_loi']}")
            except Exception as e:
                writeLog(e, response)
            return True
        except Exception:
            return False

    def getCourseRegistration(self, index):
        while self.initCourseRegistration():
            break
        print(f"[{index}] {Fore.LIGHTCYAN_EX}Đang lấy danh sách môn học", end='\r')
        data = {
            "is_CVHT": False,
            "additional": {
                "paging": {
                    "limit": 8000,
                    "page": 1
                },
                "ordering": [{"name": "", "order_type": ""}]
            }
        }

        self.session.headers.update({'Content-Type': 'application/json'})
        response = self.session.post(
            self.host + '/dkmh/w-locdsnhomto', json=data, timeout=60).json()
        if self.checkExpired(response):
            return False
        if response['code'] == 200:
            return response['data']
        return False

    def handleCourseRegistration(self, index):
        data = self.getCourseRegistration(index)

        if data == False:
            return False

        ds_mon_hoc = data['ds_mon_hoc']
        ds_nhom_to = data['ds_nhom_to']

        for nhom_to in ds_nhom_to:
            id_to_hoc = nhom_to['id_to_hoc']
            idCourse = nhom_to['ma_mon']
            className = nhom_to['lop']
            group = nhom_to['nhom_to']
            team = nhom_to['to']
            remainingAmount = nhom_to['sl_cl']
            nameCourse = ''

            for mon_hoc in ds_mon_hoc:
                if mon_hoc['ma'] == idCourse:
                    nameCourse = mon_hoc['ten']
                    break

            self.listCourse.append(
                Course(id_to_hoc, idCourse, nameCourse, group, team, className, remainingAmount))
        return True

    def getCourseRegistrationSuccess(self, index):
        print(
            f"[{index}] {Fore.LIGHTCYAN_EX}Đang lấy danh sách môn học đăng ký thành công", end='\r')
        data = {
            'is_CVHT': False,
            'is_Clear': False
        }
        self.session.headers.update({'Content-Type': 'application/json'})
        try:
            response = self.session.post(
                self.host + '/dkmh/w-locdskqdkmhsinhvien', json=data, timeout=60).json()
            if self.checkExpired(response):
                return False
            if response['code'] == 200:
                return response['data']
            return False
        except Exception as e:
            writeLog(e, response)
        return False

    def handleCourseRegistrationSuccess(self, index):
        data = self.getCourseRegistrationSuccess(index)
        if data == False:
            return False

        totalSubject = data['total_items']
        totalTC = 0
        maxLenIDSubject, maxLenNameSubject, maxLenClassName = 0, 0, 0
        for subject in data['ds_kqdkmh']:
            totalTC += int(subject['to_hoc']['so_tc'])
            maxLenIDSubject = max(maxLenIDSubject, len(
                subject['to_hoc']['ma_mon']))
            maxLenNameSubject = max(
                maxLenNameSubject, len(subject['to_hoc']['ten_mon']))
            maxLenClassName = max(
                maxLenClassName, len(subject['to_hoc']['lop']))
        spaceIDSubject = maxLenIDSubject - 5
        spaceNameSubject = maxLenNameSubject - 11
        spaceClassName = maxLenClassName - 4
        print("Danh sách môn học đã đăng ký:",
              totalSubject, "môn,", totalTC, "tín chỉ       ")
        print("Mã MH", " "*spaceIDSubject, "|", "Tên môn học", " "*spaceNameSubject, "|", "Nhóm tổ", "|", "Số TC",
              "|", "Lớp", " "*spaceClassName, "|", "Ngày đăng ký       ", "|", "Trạng Thái")
        for subject in data['ds_kqdkmh']:
            to_hoc = subject['to_hoc']
            datetime_obj = datetime.fromisoformat(subject['ngay_dang_ky'])
            formatted_time = datetime_obj.strftime("%d/%m/%Y %H:%M:%S")
            print(to_hoc['ma_mon'], " "*(maxLenIDSubject - len(to_hoc['ma_mon'])), "|", to_hoc['ten_mon'], " "*(maxLenNameSubject - len(to_hoc['ten_mon'])),
                  "|   ", to_hoc['nhom_to'], "  |  ", to_hoc['so_tc'], "  |", to_hoc['lop'], "|", formatted_time, "|", subject['dien_giai_enable_xoa'])
        return True

    def checkExpired(self, response):
        try:
            if response['message'] == 'expired' or response['message'] == 'loggedoff':
                print(
                    f"{Fore.LIGHTRED_EX}Phiên đăng nhập hết hạn, đang đăng nhập lại...")
                self.login()
                return True
        except Exception:
            pass


def writeLog(e, response):
    with open('log.txt', 'a+') as file:
        file.write(f"{datetime.now()} - {e}\n")
        try:
            data_string = json.dumps(response, sort_keys=True, indent=2)
            with open('log.json', 'a+') as f:
                f.write(data_string)
        except Exception:
            pass
