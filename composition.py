from salary import Salary


class Employee:
    def __init__(self, pay, bonus, salary):
        self.pay = pay
        self.bonus = bonus
        self.obj_salary = salary

    def annual_salary(self):
        return "Total: " + str(self.obj_salary.get_total() + self.bonus)


sal = Salary(600)
obj_emp = Employee(600, 500, sal)
print(obj_emp.annual_salary())