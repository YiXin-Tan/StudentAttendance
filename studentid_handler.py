import csv
import datetime
import os

class IdNotFound(Exception):
    """Raised when Student ID can't be found in 'HSC_students.csv'"""
    pass

# class StudentWrongClass(Exception):
#     """Raised when Student is not in CO111A"""
#     pass


class StudentIDHandler:
    def __init__(self, start_time):
        self.start_time = start_time
        self.HSC_students_csv = 'NameLists/HSC_students.csv'

        self.attendance_list = []
        with open('NameLists/CO011A_students.csv', mode='r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # pass 1st row
            for row in csv_reader:
                # Initial record: ['TAN0060', Yi Xin TAN, Absent]
                self.attendance_list.append([row[0], f'{row[1]} {row[2]}', 'Absent'])
            self.CO011A_students = [record[0] for record in self.attendance_list]

    def get_name(self, student_id):
        with open(self.HSC_students_csv, mode='r') as file:
            for row in csv.reader(file):
                if row[0] == student_id:
                    return f'{row[1]} {row[2]}'
            raise IdNotFound

    def modify_record(self, student_id, entry_time):
        delta_seconds = (entry_time - self.start_time).total_seconds()
        try:
            if student_id in self.CO011A_students: # check if student in CO011A
                if delta_seconds > 600:  # Late: entry_time >10mins
                    status = "Late"
                elif delta_seconds < -300:  # Too Early: entty_time <5 mins
                    status = "Too Early"
                else:
                    status = "On Time"
            else:
                name = self.get_name(student_id)
                status = "Wrong Class"
                self.attendance_list.append([student_id, name, status])
        except IdNotFound:
            name = 'N/A'
            status = 'Invalid Student ID'
            self.attendance_list.append([student_id, name, status])
        else:
            for record in self.attendance_list:
                if record[0] == student_id:
                    name = record[1]
                    record[2] = status
        finally:
            entry_record = {'status': status,
                            'student_id': student_id,
                            'name': name,
                            'entry_time': entry_time.strftime('%I:%M:%S %p')}
            print(f'{entry_record.get("entry_time")} {name}: {status}')
            return entry_record

    def generate_attendance_csv(self):
        class_datetime = self.start_time.strftime('%Y-%m-%d %H-%M')
        filepath = f'NameLists/{class_datetime}_CO011A_attendance.csv'
        with open(filepath, mode='w', newline='') as file:
            fieldnames = ['ID', 'Name', 'Status']
            csv_writer = csv.writer(file,  delimiter=',', quotechar="'", quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(fieldnames)
            for record in self.attendance_list:
                csv_writer.writerow(record)
        return filepath

def rename_fake_barcode_img():
    for file in os.listdir('./FakeStudentID'):
        # file: 3_EVA9999.gif
        # new_file: EVA9999.gif
        new_file = file[file.find('_') + 1:]
        os.rename(f'./FakeStudentID/{file}', f'./FakeStudentID/{new_file}')
