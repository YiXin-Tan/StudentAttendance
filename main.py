from studentid_handler import StudentIDHandler
from email_handler import send_mail
import datetime
from flask import Flask, request, render_template, url_for, redirect, flash
import os

# too early: <5mins, too late: >10mins
t1_start = datetime.datetime(2021, 9, 7, hour=20, minute=54)


app = Flask(__name__)
app.config['SECRET_KEY'] = 'ff424301b28a53cf1185a9af'
os.environ['SMTP_SENDER_PWD'] = input('Enter SMTP_SENDER_PWD: ')

student_id_handler = StudentIDHandler(t1_start)
t2_cur = datetime.datetime.now()


@app.route('/', methods=['GET', 'POST'])
def enter_id():
    if request.method == 'POST':
        t_cur = datetime.datetime.now()
        std_id = request.form['std_id']
        entry_record = student_id_handler.modify_record(std_id, t_cur)
        return render_template('index.html',
                               entry_record=entry_record,
                               start_time=t1_start.strftime('%Y-%m-%d %I:%M %p'))
    return render_template('index.html',
                           title='Student Attendance',
                           entry_record=None,
                           start_time=t1_start.strftime('%Y-%m-%d %I:%M %p'))


@app.route('/end')
def end():
    attendance_filepath = student_id_handler.generate_attendance_csv()
    send_mail(t1_start, attendance_filepath)
    flash('End of class, attendance email has been sent to class teacher.', category='success')
    return render_template('daily-attendance-table.html',
                           title='End Of Class',
                           daily_attendance_list=student_id_handler.attendance_list)


if __name__ == '__main__':
    app.run(debug=True)
