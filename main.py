import os
import time
import threading
import random
from datetime import datetime

# Bắt lỗi nếu không thể import được các thư viện cần thiết
try:
    from colorama import Style, Fore
    import tls_client
    from fake_useragent import UserAgent
    from Static.Methods import StaticMethods
    from Static.Values import StaticValues
    from Handler.ErrorHandler import Handler
except ImportError as e:
    print(f"Lỗi khi import thư viện: {e}")
    exit(1)  # Thoát chương trình nếu lỗi xảy ra


class StaticMethods:
    @staticmethod
    def kiem_tra_phien_ban(version):
        print(f"Kiểm tra phiên bản: {version}")

    @staticmethod
    def get_userData(username, info_type):
        # Hàm giả để lấy dữ liệu người dùng, bạn có thể thay thế bằng logic thực tế
        if username == "invalid":
            return "Không hợp lệ"
        return {"id": "123456", "nickname": "UserExample", "secUid": "ABC123456"}

    @staticmethod
    def _getpayload(timestamp, user_agent, rand1, rand2, user_data, report_type):
        # Tạo payload giả, thay thế bằng logic thật
        return {
            "timestamp": timestamp,
            "user_agent": user_agent,
            "rand1": rand1,
            "rand2": rand2,
            "user_data": user_data,
            "report_type": report_type
        }

    @staticmethod
    def vk():
        print("Thông tin về VK")

    @staticmethod
    def khi_chay_lan_dau():
        print("Chạy lần đầu")

    @staticmethod
    def hien_thi_thong_tin():
        print("Thông tin chương trình")


class StaticValues:
    WAITING = "[WAITING]"
    WARNING = "[WARNING]"
    SUCCESS = "[SUCCESS]"
    REPORT_TYPES = {1: ("Spam", "Spam content"), 2: ("Abuse", "Abusive content")}
    TONG_SO_YEU_CAU = 0
    SO_LUOT_BAO_CAO = 0
    COOLDOWN = False


class Handler:
    @staticmethod
    def integer_handler(prompt, min_value=1, max_value=10):
        while True:
            try:
                value = int(input(prompt))
                if min_value <= value <= max_value:
                    return value
                else:
                    print(f"Giá trị phải nằm trong khoảng {min_value} đến {max_value}.")
            except ValueError:
                print("Vui lòng nhập một số nguyên.")


class ChuongTrinh:
    def _xoa_man_hinh(self):
        # Xóa màn hình console
        os.system("cls") if os.name == 'nt' else os.system("clear")

    def main(self):
        self._xoa_man_hinh()
        while True:
            print(f"{StaticValues.WAITING}Nhập URL hoặc @ của nạn nhân ➤ ", end="")
            self.nan_nhan = input()
            self.nan_nhan = StaticMethods.get_userData(self.nan_nhan, "id")
            if "Không hợp lệ" in self.nan_nhan:
                print(f"{StaticValues.WARNING} URL hoặc @ không hợp lệ!")
            else:
                break

        self._xoa_man_hinh()
        print(f"{StaticValues.SUCCESS}Người dùng hợp lệ!")
        print(f"{StaticValues.WAITING}Đang thu thập dữ liệu người dùng...")

        # Lấy dữ liệu của nạn nhân
        self.du_lieu_nan_nhan = {
            "id": StaticMethods.get_userData(self.nan_nhan, "id"),
            "ten": StaticMethods.get_userData(self.nan_nhan, "nickname"),
            "secUid": StaticMethods.get_userData(self.nan_nhan, "secUid"),
        }

        print(f"{StaticValues.SUCCESS}Thành công!")
        self._xoa_man_hinh()

        # Hiển thị các tùy chọn báo cáo
        print(f"{StaticValues.WAITING}Chọn một tùy chọn để báo cáo nạn nhân.")
        for key, value in StaticValues.REPORT_TYPES.items():
            print(f"{key}: {value[1]}")

        while True:
            self.loai_bao_cao = Handler.integer_handler(f"{Fore.YELLOW}➤ {Fore.RESET}", 1, 15)
            if self.loai_bao_cao in StaticValues.REPORT_TYPES:
                break

        # Chuẩn bị payload cho báo cáo
        self.payload = StaticMethods._getpayload(
            datetime.now().timestamp(),
            UserAgent().random,
            random.randint(7000000000000000000, 9999999999999999999),
            random.randint(7000000000000000000, 9999999999999999999),
            self.du_lieu_nan_nhan,
            self.loai_bao_cao
        )

    def bao_cao(self):
        while True:
            session = tls_client.Session(client_identifier="chrome_106")
            response = session.get(
                "https://www.tiktok.com/aweme/v2/aweme/feedback/", params=self.payload
            )

            StaticValues.TONG_SO_YEU_CAU += 1
            if "Cảm ơn vì phản hồi của bạn" in response.text or response.status_code == 200:
                StaticValues.SO_LUOT_BAO_CAO += 1
                self._xoa_man_hinh()
                print(f"{StaticValues.SUCCESS}{self.du_lieu_nan_nhan['ten']} đã bị báo cáo "
                      f"{StaticValues.SO_LUOT_BAO_CAO} lần! (Tỷ lệ thành công: "
                      f"{(StaticValues.SO_LUOT_BAO_CAO / StaticValues.TONG_SO_YEU_CAU) * 100:.2f}%)")
            else:
                print(f"{StaticValues.WARNING}Lỗi! (Tỷ lệ thành công: "
                      f"{(StaticValues.SO_LUOT_BAO_CAO / StaticValues.TONG_SO_YEU_CAU) * 100:.2f}%)")
                StaticValues.COOLDOWN = True
                break


if __name__ == "__main__":
    danh_sach_luong = []

    # Kiểm tra phiên bản và hiển thị thông tin ban đầu
    StaticMethods.kiem_tra_phien_ban("0.0.3")
    os.system("cls") if os.name == 'nt' else os.system("clear")
    StaticMethods.vk()
    os.system("cls") if os.name == 'nt' else os.system("clear")
    StaticMethods.khi_chay_lan_dau()
    StaticMethods.hien_thi_thong_tin()

    # Nhập số lượng luồng để báo cáo
    so_luong_luong = Handler.integer_handler(f"{StaticValues.WAITING}SỐ LƯỢNG LUỒNG ➤ ")
    time.sleep(1)

    chuong_trinh = ChuongTrinh()
    chuong_trinh.main()

    # Tạo các luồng để thực hiện báo cáo
    for _ in range(so_luong_luong):
        luong = threading.Thread(target=chuong_trinh.bao_cao)
        danh_sach_luong.append(luong)
        luong.start()

    # Đồng bộ các luồng
    for luong in danh_sach_luong:
        if not StaticValues.COOLDOWN:
            luong.join()
        else:
            print(f"{StaticValues.WAITING}Phát hiện chế độ chờ. Đợi 10 giây...")
            time.sleep(10)
            StaticValues.COOLDOWN = False