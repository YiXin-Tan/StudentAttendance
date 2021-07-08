from studentid_handler import StudentIDHandler
from email_handler import send_mail
import datetime

cur_time = datetime.datetime.today()

t1_start = datetime.datetime(2021, 7, 3, hour=15, minute=10)

student_id_handler = StudentIDHandler(t1_start)
t2_cur = datetime.datetime.now()
a = student_id_handler.modify_record('WAN0070', t2_cur)  # valid id
b = student_id_handler.modify_record('TES0001', t2_cur)  # wrong class
c = student_id_handler.modify_record('TES0002', t2_cur)  # id not found

attendance_filepath = student_id_handler.generate_attendance_csv()
send_mail(t1_start, attendance_filepath)
