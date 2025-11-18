from SinhVien import SinhVien

class QuanLySinhVien:
    list_sinh_vien = []

    # Hàm hỗ trợ tìm sinh viên (BẠN BỊ THIẾU HÀM NÀY)
    def timSinhVien(self, ma_sv):
        for sv in self.list_sinh_vien:
            if sv.ma_sv == ma_sv:
                return sv
        return None

    def generate_id(self):
        maxID = 1
        if (self.SoluongSinhVien() > 0):
            maxID = self.list_sinh_vien[0].ma_sv
            for sv in self.list_sinh_vien:
                if (sv.ma_sv > maxID):
                    maxID = sv.ma_sv
            maxID += 1
        return maxID

    def SoluongSinhVien(self):
        return self.list_sinh_vien.__len__()

    def nhap_sinh_vien(self):
        ma_sv = self.generate_id()
        ho_ten = input("Nhập họ tên sinh viên: ")
        sex = input("Nhập giới tính sinh viên: ")
        major = input("Nhập chuyên ngành sinh viên: ")
        while True:
            try:
                diem_tb = float(input("Nhập điểm trung bình sinh viên: "))
                if 0 <= diem_tb <= 10: break
                else: print("Điểm phải từ 0 đến 10.")
            except ValueError:
                print("Vui lòng nhập số.")
        
        sv = SinhVien(ma_sv, ho_ten, sex, major, diem_tb)
        self.xeploaihocluc(sv) # Tính học lực ngay khi nhập
        self.list_sinh_vien.append(sv)
        print(f"Đã thêm sinh viên ID {ma_sv} thành công!")

    def updateSinhVien(self, ma_sv):
        sv = self.timSinhVien(ma_sv) # Đã có hàm timSinhVien để gọi
        if sv is not None:
            print(f"Đang cập nhật cho sinh viên: {sv.ho_ten}")
            ho_ten = input("Nhập họ tên mới (Enter để giữ nguyên): ")
            if ho_ten: sv.ho_ten = ho_ten
            
            sex = input("Nhập giới tính mới (Enter để giữ nguyên): ")
            if sex: sv.sex = sex
            
            major = input("Nhập chuyên ngành mới (Enter để giữ nguyên): ")
            if major: sv.major = major
            
            diem_input = input("Nhập điểm TB mới (Enter để giữ nguyên): ")
            if diem_input:
                sv.diem_tb = float(diem_input)
            
            self.xeploaihocluc(sv) # Cập nhật lại học lực
            print("Cập nhật thành công!")
        else:
            print("Không tìm thấy sinh viên với mã số đã cho.")

    def sortByID(self):
        self.list_sinh_vien.sort(key=lambda sv: sv.ma_sv, reverse=False)

    def sortByName(self):
        self.list_sinh_vien.sort(key=lambda sv: sv.ho_ten, reverse=False)

    def sortByDiemTB(self):
        self.list_sinh_vien.sort(key=lambda sv: sv.diem_tb, reverse=False)

    def findByName(self, name):
        ketqua = []
        if self.SoluongSinhVien() > 0:
            for sv in self.list_sinh_vien:
                if name.lower() in sv.ho_ten.lower():
                    ketqua.append(sv)
        return ketqua

    def deleteByID(self, ma_sv):
        sv = self.timSinhVien(ma_sv)
        if sv is not None:
            self.list_sinh_vien.remove(sv)
            return True
        return False

    def xeploaihocluc(self, sv: SinhVien):
        if sv.diem_tb >= 9:
            sv.hocluc = "Xuất sắc"
        elif sv.diem_tb >= 8:
            sv.hocluc = "Giỏi"
        elif sv.diem_tb >= 6.5: # Đã sửa từ 76.5 thành 6.5
            sv.hocluc = "Khá"
        elif sv.diem_tb >= 5:
            sv.hocluc = "Trung bình"
        else:
            sv.hocluc = "Yếu"

    def showSinhVien(self, list_sv):
        print("{:<10} {:<25} {:<10} {:<20} {:<10} {:<15}".format("Mã SV", "Họ Tên", "Giới Tính", "Chuyên Ngành", "Điểm TB", "Học Lực"))
        print("-" * 90)
        if(len(list_sv) > 0):
            for sv in list_sv:
                print("{:<10} {:<25} {:<10} {:<20} {:<10} {:<15}".format(sv.ma_sv, sv.ho_ten, sv.sex, sv.major, sv.diem_tb, sv.hocluc))
        else:
            print("Danh sách trống!")
        print("\n")

    def getlistSinhVien(self):
        return self.list_sinh_vien



from QuanLySinhVien import QuanLySinhVien
qlsv = QuanLySinhVien()
while True:
    print("----- CHƯƠNG TRÌNH QUẢN LÝ SINH VIÊN -----")
    print("1. Thêm sinh viên")
    print("2. Cập nhật sinh viên")
    print("3. Hiển thị danh sách sinh viên")
    print("4. Sắp xếp sinh viên theo ID")
    print("5. Tìm kiếm sinh viên theo tên")
    print("6. Xóa sinh viên theo ID")
    print("7. Thoát")
    
    choice = input("Chọn chức năng (1-7): ")
    
    if (choice == '1'):
        qlsv.nhap_sinh_vien()
        
    elif (choice == '2'):
        try:
            ma_sv = int(input("Nhập mã số sinh viên cần cập nhật: "))
            qlsv.updateSinhVien(ma_sv)
        except ValueError:
            print("Mã sinh viên phải là số!")

    elif (choice == '3'):
        # Sử dụng hàm showSinhVien có sẵn thay vì viết lại vòng lặp print
        qlsv.showSinhVien(qlsv.list_sinh_vien)

    elif (choice == '4'):
        qlsv.sortByID()
        print("\n-> Danh sách sinh viên đã được sắp xếp theo ID.")
        qlsv.showSinhVien(qlsv.list_sinh_vien)

    elif (choice == '5'):
        name = input("Nhập tên sinh viên cần tìm kiếm: ")
        ketqua = qlsv.findByName(name)
        print(f"\n-> Tìm thấy {len(ketqua)} sinh viên:")
        qlsv.showSinhVien(ketqua)

    elif (choice == '6'):
        try:
            ma_sv = int(input("Nhập mã số sinh viên cần xóa: "))
            isdeleted = qlsv.deleteByID(ma_sv)
            if isdeleted:
                print("-> Xóa sinh viên thành công.")
            else:
                print("-> Không tìm thấy sinh viên với mã số đã cho.")
        except ValueError:
            print("Mã sinh viên phải là số!")

    elif (choice == '7'):
        print("Thoát chương trình.")
        break
    else:
        print("Lựa chọn không hợp lệ. Vui lòng chọn lại.")