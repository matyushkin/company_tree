import random
import time
from decimal import Decimal

from company_tree.users.models import Department, Employee

departments_stable = list(Department.objects.all())
proto_file_names = ["name", "surname", "patronic"]
ffio, mfio = {}, {}

COMPANY_SIZE = 50000
DEP_ROOT_NUM = 5
DEP_LEVELS_NUM = 5
SALARY_MIN = 20000
SALARY_MAX = 1000000


for proto_name in proto_file_names:
    with open(f"names/f{proto_name}.txt") as f:
        data = f.read().splitlines()
        ffio[proto_name] = [line.strip() for line in data]
    with open(f"names/m{proto_name}.txt") as f:
        data = f.read().splitlines()
        mfio[proto_name] = [line.strip() for line in data]


def generate_departments_tree():
    for i in range(1, DEP_ROOT_NUM + 1):
        name = f"Департамент {i}"
        Department.objects.create(name=name)

    k = DEP_ROOT_NUM
    for level in range(DEP_ROOT_NUM - 1):
        for parent in Department.objects.filter(level=level):
            for i in range(DEP_ROOT_NUM):
                name = f"Подразделение {k}"
                Department.objects.create(name=name, parent=parent)
                k += 1

                if (k != 0) and (k % 100 == 0):
                    print(f"Added new {k} departments")


def generate_random_fio():
    d = {}
    r = random.random()

    if r > 0.5:
        d["last_name"] = random.choice(mfio["surname"])
        d["first_name"] = random.choice(mfio["name"])
        d["patronic_name"] = random.choice(mfio["patronic"])
    else:
        d["last_name"] = random.choice(ffio["surname"])
        d["first_name"] = random.choice(ffio["name"])
        d["patronic_name"] = random.choice(ffio["patronic"])

    return d


def generate_person_data():
    d = generate_random_fio()
    salary = random.uniform(SALARY_MIN, SALARY_MAX)
    d["salary"] = Decimal(salary).quantize(Decimal("1.00"))
    return d


def generate_employees():
    for i in range(COMPANY_SIZE):
        d = generate_person_data()
        e = Employee(**d)
        e.save()
        e.departments.add(random.choice(departments_stable))

        if (i != 0) and (i % 100 == 0):
            print(f"Added new {i} employees from {COMPANY_SIZE}")


def run():
    generate_departments_tree()
    print("Waiting untill department tree bulk processing will be finished...")
    time.sleep(60)
    generate_employees()
