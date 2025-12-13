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
        reader = read_file("staff", "csv")
        print(reader)
        for staff_data in reader:
            byte_pw = bytes(staff_data["password"].encode('utf-8'))
            staff = Staff(staff_data["staff_id"],
                          staff_data["name"],
                          staff_data["staff_role"],
                          byte_pw,
                          staff_data["status"])
            self.staff_list.append(staff)
        print("Staff controller init successful.")
        

    def login(self, _id, password):
        _staff = None
        role = None
        logged_in = False
        for staff in self.staff_list:
            if staff.getStaffId() == _id and staff.getStatus() == "active":
                encoded_password = password.encode('utf-8')
                result = bcrypt.checkpw(encoded_password, staff.getPassword())
                if(result):
                    logged_in = True
                    _staff = staff
                    role = staff.getStaffRole()
                    break
                else: #break also since the id is matched
                    break
        return role, logged_in
    
    def get_staff_by_id(self, _id):
        for staff in self.staff_list:
            if staff.getStaffId() == _id:
                return staff


