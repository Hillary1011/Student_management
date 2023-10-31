import PySimpleGUI as sg
from backend.db_sql import StudentManagement as SM
from backend.students_utility import display_notification as notification
from guis.mainwindowGUI import main_function_window


################################################### PASWORD GUI ###################################################
def db_password(state):
    if state == "init":
        # layout on database set up
        layout1 = [[sg.Push(), sg.Text("Admin Setup"), sg.Push()]]
        layout_inputs = [[sg.Text("Name"), sg.Input(size=(25, 1), key="-NAME-")],
                        [sg.Text("Surname"), sg.Input(size=(25, 1), key="-SURNAME-")],
                        [sg.Text("Work ID"), sg.Input(size=(25, 1), key="-ID-")],
                        [sg.Text("Set Password"), sg.Input(size=(25, 1), password_char="*", key="-PASSWORD-")],
                        [sg.Text("Verify Password"), sg.Input(size=(25, 1), password_char="*", key="-PASSWORDVERIFICATION-")],
                        [sg.Button("Ok", key="-PASSWDINITOK-"), sg.Button("Cancel")]
                        
                        ]
        # into_frame_layout = [[layout1], [layout_inputs]]
        layout = [
                layout1,
                [sg.Frame("", layout_inputs, element_justification="right")],
                ]

    elif state == "login":
        layout1 = [[sg.Push(), sg.Text("Admin Login"), sg.Push()]]
        layout_inputs = [[sg.Text("Name"), sg.Input(size=(25, 1), key="-LOGINNAME-")],[sg.Text("Password"), sg.Input(size=(25, 1), password_char="*", key="-PASSWORD-")]]
        layout= [
                layout1,
                [sg.Frame("", layout_inputs, element_justification="right")],
                [sg.Push(), sg.Button("OK", key="-PASSWDLOGINOK-"), sg.Button("Cancel")]
                ]
    else:
        layout = [[sg.Text(f"Error...  {state} state is not defined on login")]]
    window = sg.Window("Loggin", layout=layout)

    while True:
        event, values = window.read()
        accessdb = True
        if event in (sg.WIN_CLOSED, "Cancel"):
            break
        if event == "-PASSWDINITOK-":
            # print(values["-NAME-"])
            for key in values:   # Checking if all inputs have values 
                if len(values[key].strip()) != 0:
                    continue

                else:
                    accessdb = False
                    print(f"{key} value cannot be empty")
                    sg.popup(f"{key.replace('-', '').capitalize()} value cannot be empty")
                    break
                                  
            if accessdb:
                # Password Verification
                if values["-PASSWORD-"] == values["-PASSWORDVERIFICATION-"]:
                    ############################# DATA BASE ACCESSS 1 ###############################
                    # print(f"{accessdb} Access database")
                    # print(values["-NAME-"], values["-SURNAME-"], "Admin-"+values["-ID-"], values["-PASSWORD-"])
                    stdb = SM()
                    stdb.add_student(values["-NAME-"].strip(), values["-SURNAME-"].strip(), "Admin-"+values["-ID-"].strip(), values["-PASSWORD-"].strip())
                    # Procceed with notification and then terminate admin setup window
                    # title = "Admin setup successfully"
                    # message = "Database created with admin as Hillary Mapondera"
                    # flag = "success"
                    notification("Admin setup successfully", f"Database created with admin as {values['-NAME-']} {values['-SURNAME-']}", "Success", 1500, use_fade_in=True)
                    window.close()
                    return values['-NAME-'].strip(), values["-ID-"].strip()
                    # ing on adding the admin into the database using the add_student function: students counts should be 1 less
                    
                else:
                    sg.popup(f"Passwords do not Match")

        if event == "-PASSWDLOGINOK-":
            # print(values["-LOGINNAME-"].capitalize(),values["-PASSWORD-"])
            stdb = SM()           
            admin = stdb.get_admin(values["-LOGINNAME-"].capitalize(), values["-PASSWORD-"])
            if admin:
                window.close()
                return admin
            else:
                sg.popup_ok("Password or Name is incorrect\nPlease retry again...")
                print("Wrong password Login fail... ")
                
            # print(db_object.display_all())
            # notification("Success", "Loging in...", "success", 1000, use_fade_in=True)
            # Verify Password
    window.close()


################################################### MAINFRAME GUI ###################################################


# Check if db exist using getcount
db_object = SM()

if db_object.get_students_count() == -1: #data base is empty
    s = sg.popup_ok_cancel("Students database is empty consider setting it up ?")
    if s == "OK":
        admin_name, id_= db_password("init")
        main_function_window(admin_name, id_)
        # main frame
    else:
        pass
else:
    admin = db_password("login")
    # Main window should also show the admin logged in from admin varable as well as the day....
    # on login we should show admins available.
    if admin:
        notification("Success", "Logging in...", "Success", 200, use_fade_in=True)
        # AdminName: admin[0], AdminID: admin[2][6:]
        # print(admin[0], admin[2][6:])
        main_function_window(admin[0], admin[2][6:])
    else:
        print("No login, Cancelling program...")
    # main frame
