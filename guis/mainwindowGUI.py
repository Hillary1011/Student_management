import PySimpleGUI as sg
from datetime import date
from backend.db_sql import StudentManagement as SM
from backend.students_utility import display_notification as notification

############################################################## VERIFY TABLE WINDOW #############################################################
def verify_table_window(state, data):
    headings = ["Name", "Surname", "ID", "Major", "Age"]
    if state == "IDfetch":
        layout =[[sg.Push(), sg.Text("Student Information", justification="center"), sg.Push()],
                 [
                     sg.Table(values=data, headings=headings, auto_size_columns=True,
                            display_row_numbers=True,
                            justification='center',
                            num_rows=1,
                            key='-VERIFYTABLE-',
                            selected_row_colors='White on Green',
                            enable_events=False,
                            expand_x=True,
                            expand_y=True,
                            )
                 ],
                 [sg.Push(), sg.Button("OK", key="-EXIT-"), sg.Push()]
                ]

    if state == "Single":
        layout =[[sg.Push(), sg.Text("Student registration information", justification="center"), sg.Push()],
                 [
                     sg.Table(values=data, headings=headings, auto_size_columns=True,
                            display_row_numbers=True,
                            justification='center',
                            num_rows=1,
                            key='-VERIFYTABLE-',
                            selected_row_colors='White on Green',
                            enable_events=False,
                            expand_x=True,
                            expand_y=True,
                            )
                 ],
                 [sg.Button("Cancel", key="-EXIT-"), sg.Button("Submit", key="-SUBMIT-")]
                ]
    if state == "Multiple":
        pass

    window = sg.Window("Verify Window", layout=layout,  resizable=True, finalize=True)
    window.set_min_size(window.size)

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, "-EXIT-"):
            break
        
        if event == "-SUBMIT-":
            # print("Send data to database")
            db_object = SM()
            flag, msg =db_object.add_student(data[0][0], data[0][1], data[0][3], data[0][4])
            if flag == "Success":
                notification("Added Successfully", msg, flag, 2500, use_fade_in=True)
                window.close()
                return flag
            elif flag == "Fail":
                notification("Add student Failed", msg, flag, 2500, use_fade_in=True)
                window.close()
                return flag
            # print(data)
    window.close()

################################################################## TAB 1 ADD STUDENTS ###########################################################
def main_function_window(admin, id):
    ############################################################## LEFT COLUMN AND TAB GROUP ####################################################
    available_programs = ["Accounting",  "Applied Mathematics", "Applied Physics","Automation", "Business Administration", "Civil Engineering", "Computer Science and Technology", "Economics", "Electronic Business", "Electronic and Information Engineering", "Engineering Mechanics", "English", "Environmental Engineering", "Financial Management", "Human Resources Management", "Industrial Design", "International Economics and Trade", "Law", "Marketing", "Transportation Engineering", "Wind Energy and Power Engineering"]

    add_student_tab = [[sg.Text('Name'), sg.Input(size=(25, 1), key="-STUDENTNAME-")],
                       [sg.Text('surname'), sg.Input(size=(25, 1), key="-STUDENTSURNAME-")],
                       [sg.Text('Major'), sg.Input(size=(25, 1), key="-STUDENTMAJOR-",disabled=True)],
                       [sg.Text('Age'), sg.Input(size=(25, 1), key="-STUDENTAGE-")],
                       [sg.Push(),sg.B("Verify", key="-VERIFY1-"), sg.Push()],
                    #    [sg.Push(),sg.B("Submit"), sg.Push(), sg.B("Cancel"), sg.Push()]
                      ]
    excel_layout = sg.Col([
                            [sg.Text('Excel File'), sg.Input(size=(15, 1)), sg.B("Browse")],
                            [sg.Push(), sg.B("Verify"), sg.Push()]
                         ])

    col4 = sg.Col([[sg.Frame("Select Major", 
                            [ 
                            # [sg.Input(size=(20, 1), enable_events=True, key='-MAJORINPUT-'), sg.Push(), sg.B("SELECT", key =   "-MAJORSELECT-")],
                            [sg.Listbox(available_programs, size=(31, 15), enable_events=True, key='-MAJORLIST-', horizontal_scroll=True)]
                            ]
                            # [sg.Image(data=db_image, expand_x=True, expand_y=True)],
                            )
                  ]], key='-COL4-')
    
    add_frame = [
                    [sg.Frame("", add_student_tab, element_justification="right")], 
                    [sg.Pane([col4, sg.Col([[excel_layout]])], orientation='v', expand_x=True, expand_y=True, k='-PANE-', show_handle=True, border_width=0)]
                ]

    fetch =    [
                    [sg.Radio('Display All',"Radio1", default =True, size=(10,1), k='-R1-'), sg.Radio('Student Count', "Radio1", default=False, size=(10,1), k='-R2-')],
                    [sg.Radio('Student Count per Major',"Radio1", default =False, size=(18,1), k='-R3-'), sg.B("Fetch", key="-ORDFETCH-")],
                ]
    
    fetch_by =  [
                    [sg.Radio('Credentials',"Radio2", default =True, size=(10,1), k='-R11-'), sg.Radio('Student ID', "Radio2", default=False,  size=(10,1), k='-R22-')],
                    [sg.Text("ID"), sg.Input(size=(16, 1), key="-IDFETCH-"), sg.Push(), sg.B("Fetch", key="-FETCHBY-")]
                 ]
    
    fetch_by_major =  [   
                            [sg.Input(size=(20, 1), enable_events=True, key='-INPUT-'), sg.Push(), sg.B("Fetch", key = "-FETCHBYMAJOR-")],
                            [sg.Listbox(available_programs, size=(30, 5), enable_events=True, key='-LIST-', text_color="green",horizontal_scroll=True)],
                            # [sg.Button('Chrome', key='c'), sg.Button('Exit')]
                    
                        ]

    retrieve = [
                    [sg.Frame("Fetch", fetch, element_justification="left")],
                    [sg.Frame("Fetch By", fetch_by, element_justification="left")],
                    [sg.Frame("Fetch By Major", fetch_by_major, element_justification="left")],
                    [sg.Text("Enrollment Stats")],
                    [sg.Multiline(key="-TEXTBOX-", size=(32, 7), enable_events=True, enter_submits=False, disabled=True)],
                    [sg.Push(), sg.B("Clear", key="-CLEAR-"), sg.Push()]
               ]


    action_tab = [[sg.Text('Action')],
                    [sg.Text('Put your layout in here')],
                    [sg.B("Click me")]]

    tab_groups_layout = [
                    [sg.Tab("Add Students", layout=add_frame, expand_x=False)],
                    [sg.Tab("Retrieve Info", layout=retrieve)],
                    [sg.Tab("Action", layout=action_tab)]
                    ] 

    left_col = sg.Column([[sg.Text(f"Admin logged: {admin} ({id})")],
                        [sg.TabGroup(tab_groups_layout, enable_events=True, key='-TABGROUP-', selected_background_color="Green", tab_background_color="gray", border_width=1, expand_x=True, expand_y=True)]
                        #   [sg.Button('Run'), sg.B('Edit'), sg.B('Clear'), sg.B('Open Folder'), sg.B('Copy Path')],
                        ], element_justification='l', expand_x=True, expand_y=True,) # May need to remove element justification


    ############################################################## RIGHT COLUMN AND TABLE ####################################################
    # Experimenting with tables
            # def word():
            #     return ''.join(random.choice(string.ascii_lowercase) for i in range(10))
            # def number(max_val=1000):
            #     return random.randint(0, max_val)

            # def make_table(num_rows, num_cols):
            #     data = [[j for j in range(num_cols)] for i in range(num_rows)]
            #     data[0] = [word() for __ in range(num_cols)]
            #     for i in range(1, num_rows):
            #         data[i] = [word(), *[number() for i in range(num_cols - 1)]]
            #     return data
            # data = make_table(num_rows=5, num_cols=5)
            # headings = [str(data[0][x])+' ..' for x in range(len(data[0]))]

    #################################################################### ACCESS DATABASE ########################################################
    headings = ["Name", "Surname", "ID", "Major", "Age"]
    data = [[]]

    table_layout =   [sg.Table(values=data[1:][:], headings=headings, max_col_width=25,
                            display_row_numbers=True,
                            justification='center',
                            num_rows=20, 
                            alternating_row_color='lightblue',
                            key='-TABLE-',
                            selected_row_colors='White on Green',
                            enable_events=True,
                            expand_x=True,
                            expand_y=True,
                            vertical_scroll_only=False,
                            enable_click_events=True, 
                            background_color="white",
                            text_color="Black"
                            )

                    ]
                
    # DATE IN RIGHT PANNEL
    right_col = sg.Column([[sg.Input("", key="-DISYPLAYUNIT-", justification="center", enable_events=False, size=(50, 1),disabled=True),sg.Push(), sg.Text(f"Today's Date is: {date.today()}")], table_layout], element_justification='l', expand_x=True, expand_y=True)
                    

    layout = [
            [sg.Push(), sg.Text('HOHAI University Student Management System', font='Any 20', justification="center"), sg.Push()],
            [sg.Pane([sg.Column([[left_col]], element_justification='l',  expand_x=True, expand_y=True), sg.Column([[right_col]], element_justification='c', expand_x=True, expand_y=True)], orientation='h', relief=sg.RELIEF_SUNKEN, expand_x=True, expand_y=True, k='-PANE-')],
            [sg.Sizegrip()]
            ]

    window = sg.Window('Student management system', layout, finalize=True,  resizable=True, right_click_menu=sg.MENU_RIGHT_CLICK_EDITME_VER_EXIT)
    window.set_min_size((1010, 650))

    data_ = [] # Focollecting added students so to visualize on the table in real time
    db_object = SM()
    while True:
        event, values = window.read()
        # print(event, values)
        if event in (sg.WIN_CLOSED, "Cancel"):
            break
        
        #           Submitting single student
        if event == "-VERIFY1-": 
            ################################### DB access point 1 ###################################
            generated_id = db_object.id_gen(values["-STUDENTMAJOR-"], values["-STUDENTAGE-"])
            
            current_student = [values["-STUDENTNAME-"], values["-STUDENTSURNAME-"], generated_id, values["-STUDENTMAJOR-"], values["-STUDENTAGE-"]]
   
            flag = verify_table_window("Single", data=[current_student])
            # Update the main table only if the student can be added into database i.e does not already exist
            if flag == "Success":
                data_.append(current_student)
                window["-TABLE-"].update(values=data_)
            # print(window["-TABLE-"].ge)
            # print(values["-TABLE-"])
        ############################################### RETRIEVE TAB EVENTS ###############################
        if event == "-ORDFETCH-":
            # print(values["-R1-"], values["-R2-"])
            if values["-R1-"]:
                enrolled_students = db_object.display_all() # Case when database is ready but eith no students
                if len(enrolled_students) == 0:
                    window["-DISYPLAYUNIT-"].update("No students have been enrolled")
                else:
                    # print(enrolled_students)
                    data_ = [list(i) for i in enrolled_students]
                    window["-DISYPLAYUNIT-"].update(f"Enrolled students: {len(data_)}")
                    window["-TABLE-"].update(values=data_)
            if values["-R2-"]:
                db_object = SM()
                st_count = db_object.get_students_count()
                # print(f"Get the count...{st_count}")
                # Display to the DISYPLAY UNIT
                window["-DISYPLAYUNIT-"].update(f"Enrolled students: {st_count}")
               
        #            Fetch by Major Text suggesion ######
        if values["-INPUT-"] !=  "":
            search = values['-INPUT-']
            sugessted_program = [x for x in available_programs if search in x]
            window["-LIST-"].update(sugessted_program)

        else:
            window["-LIST-"].update(available_programs)
            # window["-MAJORLIST-"].update(available_programs)

        # if values["-STUDENTMAJOR-"] !=  "":                                  IMPLEMENTATION Text SUGGESION
        #     search_ = values['-STUDENTMAJOR-']
        #     sugessted_program_ = [y for y in available_programs if search_ in y]
        #     window["-MAJORLIST-"].update(sugessted_program_)
        #     # print(sugessted_program_)
        #     # print(values["-STUDENTMAJOR-"])
        # else:
        #     window["-MAJORLIST-"].update(available_programs)
        
        # if event == '-MAJORLIST-' and len(values['-MAJORLIST-']):
        #     window["-STUDENTMAJOR-"].update(str(values["-MAJORLIST-"]).strip("[]'"))

        #            Fetch by Major Click Listbox and obtain text ######
        if event == '-LIST-' and len(values['-LIST-']):
            window["-INPUT-"].update(str(values["-LIST-"]).strip("[]'"))

         #           Major Selection     
        if event == '-MAJORLIST-' and len(values['-MAJORLIST-']):
            window["-STUDENTMAJOR-"].update(str(values["-MAJORLIST-"]).strip("[]'"))

        #            Fetch by major ######
        if event == '-FETCHBYMAJOR-':
            # print("Fetch Pressed")
            # print(values["-INPUT-"])
            
            if len(values["-INPUT-"]) and values["-INPUT-"] in available_programs:
                # print(f"Searching for {values['-INPUT-']}")
                subject_students = db_object.major(values["-INPUT-"])
                data_ = [list(i) for i in subject_students]
                window["-DISYPLAYUNIT-"].update(f"Enrolled students: {len(data_)}")
                window["-TABLE-"].update(values=data_)
                ####### WORKING HERE ON  FETCH BY MAJOR
            elif len(values["-INPUT-"]) == 0: # No subject entered 
                pass
            else: # subject entered is not in availabe_programs
                window["-DISYPLAYUNIT-"].update(f"{values['-INPUT-']} is currently unavailable!")
        if event == "-CLEAR-":
            window["-TEXTBOX-"].update("")


        #            Fetch student counts per major ######
        if event == "-ORDFETCH-":
            if values["-R3-"]:
                data_ = db_object.display_major_counts()
                major_counts = ""
                if len(data_) > 0: # If there are some records in the database
                    # major_counts.join(str(i[0]+"\t"+str(i[1])+"\n" for i in data_))
                    for i in data_:
                        major_counts = major_counts + i[0] + "\t\t"+ str(i[1])+ "\n" # .zfill(3)
                    window["-TEXTBOX-"].update(major_counts)

                else:
                    pass

        #           Fetch by Student ID
        if event == "-FETCHBY-" and values["-R22-"]:
            id = values["-IDFETCH-"]
            # print(id)
            student = db_object.get_student_by_id(id)
            if student and len(id)>0:
                data_ = [student[0], student[1], student[2], student[3], student[4]]
                print(student)
                #  current_student = [values["-STUDENTNAME-"], values["-STUDENTSURNAME-"], generated_id, values["-STUDENTMAJOR-"], values["-STUDENTAGE-"]]
                verify_table_window("IDfetch", [data_])
            elif not student:
                sg.popup_ok(f"Student Not Found!")
            else:
                pass

# Returns the current local date
# today = date.today()
# print("Today date is: ", today)
# name = "Hillary"
# id = "H75343"
# main_function_window(name, id)