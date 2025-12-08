import bcrypt
from model.staff import Staff
from tools.file_handler import read_file
from tools.file_handler import save_file

class StaffController:
#password is [admin]
#Staff("admin","Bossku", "manager", b'$2b$12$fr1jy6nwyg4Yh3AHEfDbqOUATBxb8sz9gdFgUC.4uac4V3AbrUQdy', "active")
#password is [12345678]
#Staff("S001","Alice", "staff", b'$2b$12$irizjpBEUKYrPz/q6UD1Leq2tAgAB7Uiqdh.09hY6t.A5HiXm3iS2', "active")
#password is [abcdef]
#Staff("S002","Johnson", "staff", b'$2b$12$irizjpBEUKYrPz/q6UD1LekoAvMRFDSePzke8N9meEBKWhOpJGD5y', "resgined")
#Staff("S003","Duke", "staff", b'$2b$12$irizjpBEUKYrPz/q6UD1LekoAvMRFDSePzke8N9meEBKWhOpJGD5y', "active")

    staff_list = []
    def __init__(self):
        header, datas = read_file("staff", "csv")
        pw_index = -1
        try:
            pw_index = header.index("password")
        except ValueError:
            print("Password field not found.")
            return

        for staff_data in datas:
            #print(staff_data) #debug see only
            byte_pw = bytes(staff_data[pw_index].encode('utf-8'))
            staff = Staff(staff_data[0], staff_data[1], staff_data[2], byte_pw, staff_data[4])
            self.staff_list.append(staff)
        print("Staff controller init successful.")
        

    def login(self, _id, password):
        role = None
        logged_in = False
        for staff in self.staff_list:
            if staff.getStaffId() == _id and staff.getStatus() == "active":
                encoded_password = password.encode('utf-8')
                result = bcrypt.checkpw(encoded_password, staff.getPassword())
                if(result):
                    logged_in = True
                    role = staff.getStaffRole()
                    break
                else: #break also since the id is matched
                    break
        return role, logged_in

sc = StaffController()
staffRole, logged_in = sc.login("S003","abcdef")
print(staffRole, logged_in)
