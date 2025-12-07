class Staff:
    staff_id = ""
    name = ""
    staff_role = ""
    password = ""
    status = "active"

    def __init__(self, staff_id, name, staff_role, password, status):
        self.staff_id = staff_id
        self.name = name
        self.staff_role = staff_role
        self.password = password
        self.status = status

    def getStaffId(self):
        return self.staff_id

    def setStaffId(self, staff_id):
        self.staff_id = staff_id



    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name



    def getStaffRole(self):
        return self.staff_role

    def setStaffRole(self, staff_role):
        self.staff_role = staff_role



    def getPassword(self):
        return self.password

    def setPassword(self, password):
        self.password = password



    def getStatus(self):
        return self.status

    def setStatus(self, status):
        self.status = status






