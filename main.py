from studentid_handler import StudentIDHandler
from email_handler import send_mail
import datetime
from flask import Flask, request, render_template, url_for, redirect

t1_start = datetime.datetime(2021, 7, 10, hour=23, minute=20)

app = Flask(__name__)

student_id_handler = StudentIDHandler(t1_start)
t2_cur = datetime.datetime.now()
# a = student_id_handler.modify_record('WAN0070', t2_cur)  # valid id
# b = student_id_handler.modify_record('TES0001', t2_cur)  # wrong class
# c = student_id_handler.modify_record('TES0002', t2_cur)  # id not found


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
                           entry_record=None,
                           start_time=t1_start.strftime('%Y-%m-%d %I:%M %p'))

@app.route('/end')
def end():
    attendance_filepath = student_id_handler.generate_attendance_csv()
    send_mail(t1_start, attendance_filepath)
    return 'End of class, attendance email sent'


if __name__ == '__main__':
    app.run(debug=True)
