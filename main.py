import os
from api.apiQLDT import *


def findCourse(idCourse, group, team, className):
    for course in apiQLDT.listCourse:
        if course.idCourse == idCourse and course.group == group and course.team == team and course.className == className:
            return course
    return False


def checkCourse():
    with open('danh_sach_mon_hoc.txt') as file:
        for line in file:
            course = line.split('|')
            idCourse = course[0].strip()
            group = course[1].strip()
            team = course[2].strip()
            className = course[3].strip()
            course = findCourse(idCourse, group, team, className)
            if course == False:
                print(
                    f"{Fore.LIGHTRED_EX}Không tìm thấy môn học:{Fore.RESET} {idCourse} - {group} - {team} - {className}")
                continue
            print(
                f"{Fore.LIGHTGREEN_EX}Tìm thấy môn học:{Fore.RESET} {idCourse} - {group} - {team} - {className}")
            apiQLDT.listCourseRegistration.append(course)


def registerCourse():
    input("Nhấn [Enter] để bắt đầu đăng ký môn học: ")
    count = 1
    for course in apiQLDT.listCourseRegistration:
        print(
            f"[{count}] {Fore.LIGHTCYAN_EX}Đang đăng ký môn học: {course.nameCourse}")
        for index in range(5):
            print(f"{Fore.LIGHTMAGENTA_EX}Đăng ký lần [{index + 1}]", end='\r')
            if apiQLDT.registerCourse(course.id_to_hoc):
                break
        count += 1


def main():
    title = 'Auto đăng ký môn học PTIT by Quanh v1.0.0'
    os.system('cls' if os.name == 'nt' else 'clear')
    os.system(f'title {title}' if os.name ==
              'nt' else 'gnome-terminal --title="{title}"')
    if apiQLDT.login() == False:
        input("Nhấn [Enter] để thoát chương trình: ")
        return
    for index in range(5):
        if apiQLDT.handleCourseRegistration(index + 1):
            break
    checkCourse()
    registerCourse()
    input("Nhấn [Enter] xem danh sách môn học đã đăng ký thành công: ")
    for index in range(5):
        if apiQLDT.handleCourseRegistrationSuccess(index + 1):
            break
    input("Nhấn [Enter] để thoát chương trình: ")


if __name__ == '__main__':
    with open('account.json') as file:
        account = json.load(file)
        username = account['username']
        password = account['password']
    apiQLDT = ApiQLDT(username, password)
    main()
