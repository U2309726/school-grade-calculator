import tkinter
from tkinter import *
from tkinter import scrolledtext, messagebox
import smtplib
import json
import yagmail

# define functions
def save_data():
    """save the data entered into a Json file"""
    student_id = student_id_entry.get()
    student_name = student_name_entry.get()
    assignment_1 = Assignment_1_entry.get()
    assignment_2 = Assignment_2_entry.get()
    laboratories = Labs_entry.get()
    mid_semister_test = mid_semister_test_entry.get()
    final_exam = final_exam_entry.get()
    # use the json file format to save the data entered by the user
    new_data = {
        student_id: {
            "Student name": student_name,
            "Student ID": student_id,
            "Assignment 1": assignment_1,
            "Assignment 2": assignment_2,
            "Laboratories": laboratories,
            "Mid semester test": mid_semister_test,
            "Final Exam": final_exam
        } #{'contact_email':['']}
    }

    # use filedialog to get location and name of where/waht to save the file as.
    # save_name = filedialog.asksaveasfilename(initialdir="./",title="Save Note",
    # filetypes=(("Text Files", "*.txt"),("All Files", "*.*")))
    # use exception to catch possibilities of the user enters wrong data
    try:
        with open("data.json", 'r') as f:
            # read old data
            data = json.load(f)
    except FileNotFoundError:
        with open("data.json", "w") as f:
            json.dump(new_data, f, indent=4)

    else:
        # updating old data with new data
        data.update(new_data)
        with open("data.json", 'w') as f:
            # saving update data
            json.dump(data, f, indent=4)
    finally:
        # clear each entry widgets once the user click the save button
        student_name_entry.delete(0, END)
        student_id_entry.delete(0, END)
        Assignment_1_entry.delete(0, END)
        Assignment_2_entry.delete(0, END)
        Labs_entry.delete(0, END)
        mid_semister_test_entry.delete(0, END)
        final_exam_entry.delete(0, END)
    return new_data


def calc_grade():
    """calculate the final score"""
    # local variables
    assignment_1 = 0.0
    assignment_2 = 0.0
    labs = 0.0
    mid_sem_test = 0.0
    final_exam = 0.0
    # get the entries from the user
    assignment_1 = float(Assignment_1_entry.get())
    assignment_2 = float(Assignment_2_entry.get())
    labs = float(Labs_entry.get())
    mid_sem_test = float(mid_semister_test_entry.get())
    final_exam = float(final_exam_entry.get())
    # add the final score

    total_score = round(float(assignment_1 + assignment_2 + labs + mid_sem_test + final_exam), 2)
    final_score = float(assignment_1 + assignment_2 + labs + mid_sem_test + final_exam)
    if total_score >= 50:
        textbox.insert(2.0, f'\t\t\n{student_name_entry.get()} final score is {total_score}% '
                            f'with a alphabetic Grade of: ' + str(determine_grade(final_score)))
    else:
        textbox.insert(2.0, f'\t\t\n{student_name_entry.get()} final score is {total_score}% '
                            f'{student_name_entry.get()} has fail the course ' + str(determine_grade(final_score)))


def determine_grade(score):
    """Determine the score levels"""
    if 95 <= score <= 100:
        return 'A+'
    elif 85 <= score <= 94:
        return 'A'
    elif 75 <= score <= 85:
        return 'B+'
    elif 65 <= score <= 75:
        return 'B'
    elif 55 <= score <= 65:
        return 'C+'
    elif 50 <= score < 55:
        return 'C'
    else:
        return f' with a score of {score}%'


def open_data():
    """read the saved txt files"""
    try:
        with open('student_data', 'r') as f:
            for line in f:
                student_data.insert(END, line)

    except:
        return


def email_report():
    # email = yagmail.SMTP()
    # email = yagmail.SMTP(user="jackmount940@gmail.com", password="feyhkzxcjvxvztvs")
    # email.send(to=)
    pass


def clean_tex_box():
    textbox.delete(1.0, END)


def search():
    '''Show a tabulated report in a secound window'''
    global report
    # create second window relative to the root window
    report = Toplevel()
    report.title('Academic Report')
    report_button_frame = tkinter.Frame(report, bg="lightblue")
    report_button_frame.pack()
    report.geometry('700x250+' + str(root.winfo_x() + 200) + "+" + str(root.winfo_y() + 400))
    report.config(bg="lightblue")
    # call the display function that shows a tabulated layout of a particular student email
    # create input_text as a scrolledtext so you can scroll through the text field set default width and height to be
    # more than the window size so that on the smallest text size, the text field size is constant.
    input_text = tkinter.scrolledtext.ScrolledText(report, width=900, height=12)
    input_text.pack()

    student_id = student_id_entry.get()
    # check the input data from the user
    try:
        with open("data.json") as f:
            data = json.load(f)  # returns a dictionary
    # if data not in the saved json file give a error message
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No data file found", font=30, width=50, height=30)

    # if data is found get it and display within the second window

    else:
        if student_id in data:
            # use the key value pairs of the dictionary in line 28 and 29 to access the value and store it.
            # tap into the new_data dictionary in line 28 twice ([][]) to get the value student id...etc
            # repeat the process for the other entries
            student_id = data[student_id]["Student ID"]
            student_name = data[student_id]["Student name"]
            assignment_1 = data[student_id]["Assignment 1"]
            assignment_2 = data[student_id]["Assignment 2"]
            labs = data[student_id]["Laboratories"]
            mid_sem_test = data[student_id]["Mid semester test"]
            final_exam = data[student_id]["Final Exam"]
            # sum the scores
            score = float(assignment_1 ) + float(assignment_2) + float(labs) + float(mid_sem_test) + float(final_exam)
            # use a message box to display the result in the second window created in line 137 to 147
            input_text.insert(1.0, f'\t\tStudent ID :{student_id} \t\t\tStudent name :{student_name}\n\n'
                                   f'\t\tAssignment 1: {assignment_1} /10%\n\t\tAssignment 2 :{assignment_2} /10%\n'
                                   f'\t\tLaboratories : {labs}/10%\n'
                                   f'\t\tMid semister Test :{mid_sem_test}/20%\n'
                                   f'\t\tFinal Exam :{final_exam}/50%\n\n'
                                   f'\t\tfinal score is {score} % ')
        # displace message box asking the user to save the student data if its new
        else:

            if messagebox.showinfo(title="Error",
                                   message=f"No detail for {student_name_entry.get()} with ID  {student_id} is saved yet."
                                           f"please populate require inputs  then click Save button"):
                data.update(data)
                with open("data.json", 'w') as f:
                    # saving update data
                    json.dump(data, f, indent=4)
    # clear all entries once the user clicks the ok button on the message box window
    finally:
        student_name_entry.delete(0, END)
        student_id_entry.delete(0, END)
        Assignment_1_entry.delete(0, END)
        Assignment_2_entry.delete(0, END)
        Labs_entry.delete(0, END)
        mid_semister_test_entry.delete(0, END)
        final_exam_entry.delete(0, END)

    def clear_txt():
        input_text.delete(1.0, END)

    # create a email button in the second window
    email_label = Label(report_button_frame, text='Enter email address:')
    email_label_entry = Entry(report_button_frame, width=50)
    email_button = Button(report_button_frame, text='Send', command=email_report, width=20)
    clear_button = Button(report_button_frame, text='Clear', width=20, command=clear_txt)

    email_label.pack(side=LEFT, padx=5, pady=5)
    email_label_entry.pack(side=LEFT, padx=5, pady=5)
    email_button.pack(side=LEFT, padx=10, ipadx=8)
    clear_button.pack(side=LEFT, padx=10, ipadx=8)
    # disable the email button
    email_button.config(state=ACTIVE)





root = tkinter.Tk()
root.title('Academic Grade Calculator')
root.geometry('1000x700')
root.config(bg="lightblue")
# root.resizable(0, 0)

input_frame = tkinter.Frame(root, bg="lightblue")
output_frame = tkinter.Frame(root, bg="lightblue", width=10)
input_frame.grid()
output_frame.grid()
student_name_label = tkinter.Label(input_frame, text="Student Name:", width=20, bg="lightblue")
student_name_label.grid(row=0, column=0, padx=5, pady=(5, 20))
student_name_entry = tkinter.Entry(input_frame, borderwidth=3, width=30)
student_name_entry.grid(row=0, column=1, padx=2, pady=(5, 20))
student_id_label = tkinter.Label(input_frame, text="ID Number:", width=20, bg="lightblue", anchor='w')
student_id_label.grid(row=0, column=2, padx=2, pady=(5, 20))
student_id_entry = tkinter.Entry(input_frame, borderwidth=3, width=30)
student_id_entry.grid(row=0, column=3, padx=2, pady=(5, 20), columnspan=1)
# create the labels and entry widgets for the Assessments
Assignment_1_label = tkinter.Label(input_frame, text="Assignment 1 :", bg="lightblue")
Assignment_1_label.grid(row=1, column=0, padx=5)
Assignment_1_entry = tkinter.Entry(input_frame, width=20, borderwidth=3)
Assignment_1_entry.grid(row=1, column=1, padx=3, pady=5, sticky='W')
Assignment_1_label = tkinter.Label(input_frame, text="/ 10% ", bg="lightblue", width=5)
Assignment_1_label.grid(row=1, column=2, sticky='W')

Assignment_2_label = tkinter.Label(input_frame, text="Assignment 2 :", bg="lightblue")
Assignment_2_label.grid(row=2, column=0, padx=5)
Assignment_2_entry = tkinter.Entry(input_frame, width=20, borderwidth=3)
Assignment_2_entry.grid(row=2, column=1, padx=3, pady=5, sticky='W')
Assignment_2_label = tkinter.Label(input_frame, text="/ 10% ", bg="lightblue", width=5)
Assignment_2_label.grid(row=2, column=2, sticky='W')

Labs_label = tkinter.Label(input_frame, text="Laboratories :", bg="lightblue")
Labs_label.grid(row=3, column=0, padx=5)
Labs_entry = tkinter.Entry(input_frame, width=20, borderwidth=3)
Labs_entry.grid(row=3, column=1, padx=3, pady=5, sticky='W')
Labs_label = tkinter.Label(input_frame, text="/ 10% of the final grade", bg="lightblue")
Labs_label.grid(row=3, column=2, padx=5, sticky='W')

mid_semister_test_label = tkinter.Label(input_frame, text="Mid semister Test :", bg="lightblue")
mid_semister_test_label.grid(row=4, column=0, padx=5)
mid_semister_test_entry = tkinter.Entry(input_frame, width=20, borderwidth=3)
mid_semister_test_entry.grid(row=4, column=1, padx=3, pady=5, sticky='W')
mid_semister_test_label = tkinter.Label(input_frame, text="/ 20% of the final grade", bg="lightblue")
mid_semister_test_label.grid(row=4, column=2, padx=5, sticky='W')

final_exam_label = tkinter.Label(input_frame, text="Final Exam  :", bg="lightblue")
final_exam_label.grid(row=5, column=0, padx=5)
final_exam_entry = tkinter.Entry(input_frame, width=20, borderwidth=3)
final_exam_entry.grid(row=5, column=1, padx=3, pady=5, sticky='W')
final_exam_label = tkinter.Label(input_frame, text="/ 50% of the final grade ", bg="lightblue")
final_exam_label.grid(row=5, column=2, padx=5, sticky='W')

textbox = tkinter.Text(output_frame, width=160, height=50)
textbox.pack(side=BOTTOM)

# create the buttons

save_button = tkinter.Button(output_frame, text="Save", width=20, command=save_data)
save_button.pack(side=LEFT, pady=5)

search_button = tkinter.Button(output_frame, text="Search", width=20, command=search)
search_button.pack(side=LEFT, padx=3)

guide_button = tkinter.Button(output_frame, text="Clear", width=20, command=clean_tex_box)
guide_button.pack(side=LEFT, padx=3)

outline_button = tkinter.Button(output_frame, text="Calculate Grade", width=20, command=calc_grade)
outline_button.pack(pady=5)

cal_grade_button = tkinter.Button(output_frame, text="Guide", width=20)
cal_grade_button.pack(pady=5)

root.mainloop()
