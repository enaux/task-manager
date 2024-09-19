# -------------------------------- task_manager.py --------------------------------------

"""
This is a Task Manager Program.

It can manage multiple tasks for multiple members of a team.

The key functions offered within the program are:
    - registering new users
    - adding new tasks (and assigning these to team members)
    - viewing all tasks
    - viewing the user's tasks
    - generating reports (i.e. detailed information regarding current task management
      status)
    - displaying statistics (e.g. current number of users, current number of tasks).

The user must login before using the program.

The following username and passord give admin rights if entered:
    username - admin
    password - password

All tasks managed by the program are stored in "tasks.txt", which the program will create
if the file does not already exist.
All registered users are listed in "users.txt", which the program will create if the file
does not already exist.
"""







# -------------------------------- Importing libraries. ---------------------------------

import os

from datetime import datetime, date
DATETIME_STRING_FORMAT = "%Y-%m-%d"







# --------------------------------- Defining exceptions. --------------------------------

class NotInListError(Exception):
    """
    This exception is raised if the user tries to edit a task number that is not within
    their own list of tasks.

    It takes the "error_type" as a parameter.
    It then returns a custom message for each "error_type":

        > if the user attempts to select another user's task, they are informed that only
          the person assigned to the task may edit the task.
          (error_type = "in_range")

        > if the user enters a value that is completely out of range of the master list
          of tasks, then they are informed that their choice is not recognised.
          (error_type = "out_of_range")
    """

    def __init__(self, error_type):

        self.error_type = error_type

        if self.error_type == "in_range":
            self.message = ("\n\t** That task is not assigned to you. Only the assignee may edit. **")

        elif self.error_type == "out_of_range":
            self.message = ("\n\t** That choice is not recognised. **")
    
    def __str__(self):
        return self.message



class TaskAlreadyComplete(Exception):
    """
    This exception is raised if the user attempts to edit a task that has already been
    marked as complete.

    Only incomplete tasks may be edited.
    """

    def __init__(self):
        self.message = ("\n\t** Error: This task has already been marked as complete and can no longer be edited. **\n")
    
    def __str__(self):
        return self.message







# ---------------------------------- Defining functions. --------------------------------


def reg_user():
    """
    This function registers a new user to the Task Manager.
    
    The function is called when the user selects 'r' at the Main Menu.

    The new user is added to the "users.txt" file.
    The new user is also added to the "username_password" dictionary which stores all
    current users.
    """

    """ ------------------------ Display section title. ----------------------------- """

    print("-"*100)
    print("REGISTER A NEW USER\n")


    """ ---------------------------- Get username. ---------------------------------- """

    # Request input of a username for the new user.
    new_username = input("Enter a username:\t\t")

    # If the chosen username is already registered, show an error message.
    while new_username in username_password:
        print("\n\t** Sorry, that username is already taken. **\n")
        # Ask the user to choose another username.
        new_username = input("Choose another username:\t")


    """ ---------------------------- Get password. ---------------------------------- """

    # Request input of a password for the new user.
    new_password = input("\nChoose your password:\t\t")

    # Request input of the password again to confirm.
    confirm_password = input("Confirm password:\t\t")       

    # While the "new_password" and "confirm_password" inputs don't match:
    while new_password != confirm_password:

        # Show an error message.
        print("\n\t **Passwords do not match. Please try again. **\n")

        # Request input of a password for the new user.
        new_password = input("Choose your password:\t\t")

        # Request input of the password again to confirm.
        confirm_password = input("Confirm password:\t\t")


    """ ------------------------------ Add user.  ----------------------------------- """

    # Add the new user to the "username_password" dictionary.
    username_password[new_username] = new_password
    
    # Add the new user to the "users.txt" file.
    with open("users.txt", 'w', encoding="utf-8") as file_to_update:

        # Declare "temp_user_list" to store user data in the correct format for writing.
        temp_user_list = []

        # For each user in the "username_password" dictionary:
        for name, passw in username_password.items():
            # Concatenate a string of username, ';', and password.
            user_str = name + ';' + passw
            # Append the formatted string to the "temp_user_list".
            temp_user_list.append(user_str)

        # Write the users in "temp_user_list" to the "users.txt" file.
        file_to_update.write("\n".join(temp_user_list))

    # Display a confirmation message for the user.
    print(f"\nNew user \"{new_username}\" added successfully.")




def add_task():
    """
    This function adds a new task to the Task Manager.

    The function is called when the user selects 'a' at the Main Menu.

    To add a task, a user must enter:
        - the name of the person assigned to the task,
        - a task title,
        - a task description,
        - a task due date.
    
    The function also automatically records the date the task was assigned, and sets a
    completion status for the new task. (All new tasks are initially set to incomplete.)
    
    The new task is added to the "tasks.txt" file.
    The new task is also added to the "master_task_list" which stores all current tasks.
    """

    """ ------------------------ Display section title. ----------------------------- """

    print("-"*100)
    print("ADD A NEW TASK\n")



    """ ----------------- Gather information about the new task. -------------------- """


    """ Assigned user.
    """
    # Request input of the "assigned_user" for the new task.
    assigned_user = input("Please enter the username of person assigned to this task:\t\t")
    
    # While the input for "assigned_user" is not a registered username:
    while assigned_user not in username_password.keys():
        # Show an error message.
        print("\n\t**User not recognised. **\n")
        # Ask the user to input another username until a registered user is chosen.
        assigned_user = input("Please enter the username of person assigned to this task:\t\t")


    """ Task title.
    """
    # Request input of the "task_title" for the new task.
    task_title = input("\nPlease enter a Task Title:\t\t\t\t\t\t")


    """ Task decription.
    """
    # Request input of the "task_description" for the new task.
    task_description = input("\nPlease enter a Task Description:\t\t\t\t\t")


    """ Date assigned.
    """
    # Store the current date, which is the date the task was assigned.
    date_assigned = date.today()


    """ Due date.
    """
    # Request input of the "due_date" for the new task.
    while True:
        # Perform input validation with try-except block.
        try:
            input_date = input("\nPlease enter the Due Date of the task (Format: YYYY-MM-DD):\t\t")

            # Store the date in the correct format in "due_date".
            due_date = datetime.strptime(input_date, DATETIME_STRING_FORMAT)

            # Break the parent while-loop when a valid date is entered.
            break

        # If a date is entered in an incorrect format, show an error message.
        except ValueError:
            print("\n\t** Invalid date-time format. Please use the format specified. **")



    """ ----------------- Store task information for the new task. ------------------ """

    # Create an "add_task" dictionary and store the new task information gathered above.
    add_task = {
        "username": assigned_user,
        "title": task_title,
        "description": task_description,
        "assigned_date": date_assigned,
        "due_date": due_date,
        # New tasks are automatically set to incomplete upon creation.
        "completed": False,
        "new_line": "\n"
    }

    # Update the "master_task_list" with the new task.
    master_task_list.append(add_task)


    """ ---------------- Write the new task to the "tasks.txt" file. ---------------- """

    # Convert the new task information into a string in the correct format.
    task_string = "\n"
    task_string += add_task["username"] + ';'
    task_string += add_task["title"] + ';'
    task_string += add_task["description"] + ';'
    task_string += add_task["assigned_date"].strftime(DATETIME_STRING_FORMAT) + ';'
    task_string += add_task["due_date"].strftime(DATETIME_STRING_FORMAT) + ';'
    task_string += "No"
    task_string += "\n"

    # Append the "task_string" to the "tasks.txt" file.
    with open("tasks.txt", 'a', encoding="utf-8") as file:
        file.write(task_string)

    # Display a confirmation message for the user.
    print(f"\nTask \"{task_title}\" successfully added.")




def write_tasks_to_file(updated_list):
    """
    This function overwrites an updated list of tasks to the "tasks.txt" file.

    The function is called within the program whenever a list of tasks has been updated
    so the updated version of the list can be viewed immediately in the "tasks.txt" file.

    """

    """ -------------- Create a starting task list from "tasks.txt". ---------------- """

    # Read the current list of tasks from the data in "tasks.txt".
    with open("tasks.txt", 'r', encoding="utf-8") as file:

        # Store this in new list variable called "overwrite_list".
        overwrite_list = file.read().split("\n")


        """ ----- Check for any updates, and replace these in "overwrite_list". ----- """

        # For each task in the "updated_list" of tasks:
        for pos, task in enumerate(updated_list):

            # If the task has been marked "updated" since last writing:
            if "updated" in task.keys():
                if task["updated"] == True:
                    # Store the updated task values in an "updated_task" list.
                    updated_task = [
                        task["username"],
                        task["title"],
                        task["description"],
                        task["assigned_date"].strftime(DATETIME_STRING_FORMAT),
                        task["due_date"].strftime(DATETIME_STRING_FORMAT),
                        "Yes" if task["completed"] else "No",
                        task["updated_date"],
                    ]
                
                    # Replace the "updated_task" at the correct position in "overwrite_list".
                    overwrite_list[pos] = (";".join(updated_task))


                    """ -------- Reset the "updated" status. ------------------------ """

                    # When processing of updates is complete, delete the ["updated"] key.
                    del updated_list[pos]["updated"]
                

            """ ------ Format the "overwrite_list" prior to writing to file. -------- """
            
            # Remove any empty lines from "overwrite_list".
            overwrite_list = [task_entry for task_entry in overwrite_list if task_entry != '']


        """ ------------- Overwrite "overwrite_list" to "tasks.txt". ---------------- """

        # Write all of the tasks in "overwrite_list" to the "tasks.txt" file.
        with open("tasks.txt", 'w', encoding="utf-8") as overwrite_file:

            # Separate each string in the "overwrite_list" with a new line.
            overwrite_file.write("\n".join(overwrite_list))




def view_all(master_list):
    """
    This function displays all of the tasks listed in the "tasks.txt" file.

    The function is called when the user selects "va" at the Main Menu.

    All tasks are printed to the console in a readable format.
    Each task is displayed with a corresponding number to identify the task.
    """

    """ ------------------------ Display section title. ----------------------------- """

    print("-"*100)
    print("VIEW ALL TASKS\n")


    """ ---------------------------- Display tasks. --------------------------------- """

    display_task_list("va", master_list, "number sublist not required")


    """ -------- Allow the "admin" user to edit all tasks from this view. ----------- """

    if login_username == "admin":
        # Create a list of task numbers to give as argument to the edit_task() function.
        task_numbers = [pos+1 for pos,value in enumerate(master_task_list)]
        # Allow the user to edit tasks if desired.
        edit_task(master_task_list, master_task_list, task_numbers)




def view_mine():
    """
    This function displays all of the tasks assigned to the user who is currently logged
    in to the program.

    The function is called when the user selects "vm" at the Main Menu.

    Each task is displayed with a corresponding number to identify the task.
    The specific task numbers for each of the user's tasks are drawn directly from the
    "master_task_list" for better organisation and display of tasks. This avoids changing
    task numbers in different list displays which may result in user confusion when
    selecting task numbers to edit.

    The user can choose to edit their tasks if they wish.

    """

    """ ------------------------ Display section title. ----------------------------- """

    print("-"*100)
    print("VIEW MY TASKS\n")


    """ ------------------ Create a sublist of the user's tasks. -------------------- """

    # Store a list of the current user's tasks and store the corresponding "task_numbers".
    user_task_list, task_numbers = get_user_list(login_username)


    """ ------------------- For users without any assigned tasks. ------------------- """
    
    # Display a message to inform the user that they do not have any assigned tasks.
    if not user_task_list:
        print("\nYou do not currently have any assigned tasks.")
        
        # Exit the function, return to Main Menu.
        return
    

        """ ------------------ For users with assigned tasks. ----------------------- """

    else:
        # Display a list of the user's tasks for the user to review.
        display_task_list("vm", user_task_list, task_numbers)

        # Allow the user to edit their tasks if desired.
        edit_task(master_task_list, user_task_list, task_numbers)




def get_user_list(user):
    """
    This function generates a list of all tasks assigned to a user.

    The list retains the corresponding task numbers from the "master_task_list".

    The logic contained in the below for-loop ensures that the index of each task in the
    "user_task_list" and the index of the corresponding task number in "task_numbers" are
    the same index.
    """

    # Initialise a list to store the user's tasks.
    user_task_list = []
    # Initialise a list to store the corresponding task numbers of the user's tasks.
    task_numbers = []

    # Iterate through the "master_task_list".
    for pos, task in enumerate(master_task_list):

        # If a task belongs to the user:
        if task["username"] == user:
            # Append the task item to the "user_task_list".
            user_task_list.append(task)
            # Append the task number to the "task_numbers" list.
            task_numbers.append(pos+1)

    return user_task_list, task_numbers




def display_task_list(mode, list_to_display, corresponding_numbers):
    """
    This function displays a given list of tasks in a readable format.

    The function is called within the view_all() and view_mine() functions.

    Parameters:

        "mode" =                    the function calling display_task_list():
                                        - "va" = view_all()
                                        - "vm" = view_mine()

        "list_to_display" =         the list of tasks to be displayed

        "corresponding_numbers" =   the list of task numbers corresponding to the tasks
                                    within the "list_to_display"
    """


    """ -------------------- Mode "va" - VIEW ALL TASKS. ---------------------------- """

    # The "list_to_display" takes the "master_task_list" as an argument.
    # The "corresponding_numbers" are sourced by enumerating "master_task_list".

    if mode == "va":

        # Iterate through each task in the "list_to_display" ("master_task_list").
        for task_num, task in enumerate(list_to_display, 1):

            # Display the task and corresponding task number.
            display_task(task_num, task)


        """ ------------------ Mode "vm" - VIEW MY TASKS. --------------------------- """

        # The "list_to_display" takes the "user_task_list" as an argument.
        # The "corresponding_numbers" list receives the "task_numbers" list which contains
        # only the corresponding task numbers for the "user_task_list".
        # (The "task_numbers" list is generated by the get_user_list() function called
        # by the view_mine() function.)
        
    elif mode == "vm":
    
        # Declare a temporary dictionary to link task numbers as keys and tasks as items.
        temp_dictionary = {}
    
        # For each task in the "user_task_list":
        for pos, task in enumerate(list_to_display):
            # Store the task item as the value, and the corresponding task number as the key.
            temp_dictionary[f"{corresponding_numbers[pos]}"] = task

        # Display each task along with its corresponding task number.
        for task_number, task in temp_dictionary.items():
            display_task(task_number, task)




def display_task(task_number, task_to_display):
    """
    This function displays a single task in a readable format.

    The function is called within the display_task_list() function to display each task
    in a given list.

    Each "task_to_display" is printed with the corresponding "task_number".
    """

    """ ------------ Display a divider before the task for readability. ------------- """
    print("-"*40)


    """ -------------- Generate a string containing the task details. --------------- """

    # Task title.
    task_details = f"Task {task_number}: \t\t {task_to_display["title"]}\n"

    # Assigned person.
    task_details += f"Assigned to: \t\t {task_to_display["username"]}\n"

    # Date assigned.
    task_details += f"Date assigned: \t\t {task_to_display["assigned_date"].strftime(DATETIME_STRING_FORMAT)}\n"

    # Due date.
    task_details += f"Due Date: \t\t {task_to_display["due_date"].strftime(DATETIME_STRING_FORMAT)}\n"

    # Updated date - may not be present for all tasks.
    if "updated_date" in task_to_display.keys():
        task_details += f"Last updated: \t\t {task_to_display["updated_date"]}\n"
    else:
        pass

    # Current status.
    if task_to_display["completed"] == True:
        task_details += "Current status: \t Completed\n"
    elif task_to_display["completed"] == False:
        task_details += "Current status: \t Incomplete\n"

    # Task description.
    task_details += f"Task Description: \n {task_to_display["description"]}"


    """ ----------------------- Display the task details. --------------------------- """
    
    print(task_details)


    """ ------------ Display a divider after the task for readability. -------------- """
    print("-"*40)




def edit_task(full_list, display_list, task_numbers):
    """
    This function allows the user to edit the tasks that are assigned to them if desired.
    The user may select "-1" from within the Edit Task Menu to return to the Main Menu.

    When the user chooses to edit a task, they can choose to:
        - mark the task as complete,
        - amend the task (e.g. update assigned person, update due date).
    """

    # Allow the user to edit tasks until they choose to exit.
    while True:

        # Print a divider for ease-of-reading.
        print("-"*100)


        """ ------------- Ask the user if they wish to edit a task. ----------------- """

        # Until the user enters their choice, "awaiting_choice" remains True.
        awaiting_choice = True
        while awaiting_choice:

            # Request user input of choice to edit a task or to exit.
            continue_choice = input("Would you like to edit a task? (Enter 'y' or 'n'):\n\n").lower()

            # If the user selects a valid option, break while-loop.
            if continue_choice == 'y' or continue_choice == 'n':
                awaiting_choice = False
                break

            # If the user does not select a valid option, show an error message.
            print("\n\t** That choice is not a recognised option. **\n")


        """ --------------- If user does not wish to edit tasks. -------------------- """

        if continue_choice == 'n':
            # Return from the edit_task() function to the Main Menu.
            return
        

        """ ------------------ If user chooses to edit tasks. ----------------------- """

        # Only incomplete tasks within the user's task list may be edited by the user.
        # The "admin" user can edit tasks that are not assigned to them through the VIEW
        # ALL TASKS menu option.

        """ Ensure the user may only select an incomplete task.
        """ # Parent try-except block.
        while True:
            try:

                """ Ensure the user only selects a task number from their own list,
                    or "-1" to exit.
                """ # Nested try-except block.
                while True:
                    try:

                        # Request input of either a task number to edit, or "-1" to exit.
                        edit_choice = int(input("\nPlease select a task to edit (e.g. to select Task 1, enter '1') or enter '-1' to return to the Main Menu:\n\n"))
                        
                        # If user selects "-1", return from the function to the Main Menu.
                        if int(edit_choice) == -1:
                            return
                        
                        # If the user does not select one of their own tasks:
                        if int(edit_choice) not in task_numbers:

                            # If the choice is recognised in the "master_task_list":
                            if int(edit_choice)-1 in range(len(full_list)):
                                # Raise an "in_range" "NotInListError" Exception.
                                raise NotInListError("in_range")
                            
                            # If the choice is not recognised in the "master_task_list":
                            else:
                                # Raise an "out_of_range" "NotInListError" Exception.
                                raise NotInListError("out_of_range")
           
                        # Break the nested try-except when all conditions are satisfied.
                        break
                            
                    except ValueError:
                        print("\n\t** Please enter a number only. **")

                    except NotInListError as error:
                        # Print error message according to the type of the NotInListError.
                        print(error)


                # Find the list index of the selected task.
                index_of_choice = task_numbers.index(edit_choice)

                # If the chosen task is already complete:
                if display_list[index_of_choice]["completed"] == True:
                    # Raise a "TaskAlreadyComplete" Exception.
                    raise TaskAlreadyComplete
                
                # Break parent try-except when all conditions are satisfied.
                break

            except TaskAlreadyComplete as error:
                print(error)


        """ ------------------ Display EDIT TASK section heading. ------------------- """

        print("-"*100)
        print(f"EDIT TASK {edit_choice}\n")


        """ ------------ Store the current values for the selected task. ------------ """

        # Store the task to be edited in a temporary dictionary.
        edited_task = display_list[index_of_choice]

        # Store the index of the "edited_task" from the "master_task_list".
        editing_index = full_list.index(edited_task)


        """ --------------------- Display the selected task. ------------------------ """
        
        # Display the selected task for ease of user review.
        display_task(edit_choice, display_list[index_of_choice])


        """ ------------------- Present a menu of edit options. --------------------- """

        # Request input of a selected menu option by the user.
        option_selection = input(
            "Please select an option:\n"
                "\nmc - mark task as complete\n"
                "a - assign task to a different user\n"
                "d - update Due Date\n\n"
            ).lower()
        
        # Perform input validation.
        while option_selection not in ["mc", 'a', 'd']:

            # Show an error message if the "option_selection" is not "mc", 'a', or 'd'.
            print("\n\t** That choice is not a recognised option. **")

            # Request input of another option until the user chooses a correct option.
            option_selection = input(
                "\nPlease select an option:\n"
                    "\nmc - mark task as complete\n"
                    "a - assign task to a different user\n"
                    "d - update due date\n\n"
                ).lower()


        """ ---------------- Option "mc" - Mark a task as complete. ----------------- """

        if option_selection == "mc":

            # Change the value of "completed" to True in the "edited_task".
            edited_task["completed"] = True

            # Display an update message for the user.
            print("\nThis task has been marked as complete.")


            """ ---------------- Option 'a' - Re-assign a task. --------------------- """

        elif option_selection == 'a':

            """ Get the username of the "new_assignee".
            """
            # Request input of the username of the "new_assignee".
            new_assignee = input("\nPlease enter the username of the person you wish to assign to this task:\t")
            
            # Perform input validation to ensure the username is a registered user.
            while new_assignee not in username_password.keys():

                # Display an error message if the username is not registered.
                print("\n\t** User not recognised. **")

                # Ask the user to input a correct, registered username.
                new_assignee = input("\nPlease enter the username of the person you wish to assign to this task:\t")
    
            """ Re-assign the task.
            """
            # Assign the "new_assignee" to the "edited_task".
            edited_task["username"] = new_assignee

            # Display an update messagee for the user.
            print(f"\nThis task has been successfully assigned to {new_assignee}.")


            """ ---------- Option 'd' - Change the due date of a task. -------------- """

        elif option_selection == 'd':

            # Perform input validation using a try-except block.
            while True:
                try:

                    # Request input of a new due date for the task.
                    input_date = input("\nPlease enter a new Due Date for the task (Format: YYYY-MM-DD): ")

                    # Store the "new_due_date" in the correct format.
                    new_due_date = datetime.strptime(input_date, DATETIME_STRING_FORMAT)

                    # Break the try-except block once the date format is correct.
                    break

                except ValueError:
                    print("\n\t** Invalid date-time format. Please use the format specified. **")
            
            # Assign the "new_due_date" to the "edited_task".
            edited_task["due_date"] = new_due_date

            # Display an update message for the user.
            print(f"\nThis task is now due on {new_due_date.strftime(DATETIME_STRING_FORMAT)}.")


        """ --------- If a task has been updated, set an "updated" status. ---------- """

        # Set an "updated" key status for the "edited_task".
        edited_task["updated"] = True

        # Add an "updated_date" to the "edited_task" dictionary.
        edited_task["updated_date"] = date.today().strftime(DATETIME_STRING_FORMAT)


        """ ---------- Update the "master_task_list" and "user_task_list". ---------- """

        # Assign the "edited_task" dictionary to the appropriate index in both the
        # "full_list" and to the "display_list".

        # Updating the "full_list" updates the "master_task_list".
        full_list[editing_index] = edited_task

        # Updating the "display_list" updates the "user_task_list" if the Edit Task Menu
        # has been accessed through the view_mine() function.
        display_list[index_of_choice] = edited_task


        """ -------------- Write all updates to the "tasks.txt" file. --------------- """

        write_tasks_to_file(full_list)




def generate_reports():
    """
    This function generates reports on all of the tasks stored in the Task Manager.

    The function is called when the user selects "gr" at the Main Menu.

    The reports are printed in a user-friendly, readable manner and are separated into
    two sections:
        - Task Overview,
        - User Overview.
    
    The function also stores the reports separately within similarly named text files:
        - "task_overview.txt",
        - "user_overview.txt".

    Task Overview displays:
        - the total number of tasks that have been generated and tracked by the Task
          Manager,
        - the total number of completed tasks,
        - the total number of incomplete tasks,
        - the total number of tasks that are incomplete and overdue,
        - the percentage of all tasks that are incomplete,
        - the percentage of all tasks that are overdue.

    User Overview displays:
        - the total number of users that are registered in the Task Manager,
        - the total number of tasks that have been generated and tracked by the Task
          Manager,
        - a breakdown report for each user including:
            - the total number of tasks assigned to the user,
            - the percentage of total tasks assigned to the user,
            - the percentage of the user's tasks that are complete,
            - the percentage of the user's tasks that are incomplete,
            - the percentage of the user's tasks that are incomplete and overdue.
    """

    """ ------------------------ Display section title. ----------------------------- """

    print("-"*100)
    print("GENERATE REPORTS\n")



    """ -*-*-*-*-*-*-*-*-*-*-*-* Generate Task Overview. *-*-*-*-*-*-*-*-*-*-*-*-*-*- """

    """ Display sub-section heading.
    """
    print("-"*80)
    print("***** Task Overview *****\n")


    """ ------------------ Calculate the total number of tasks. --------------------- """

    total_num_tasks = len(master_task_list)


    """ ----------------- If there are tasks in the Task Manager. ------------------- """

    if total_num_tasks:

        """ Calculate the total number of completed tasks.
        """ # Count completed tasks in "master_task_list".
        completed_tasks = (
            count_occurrences(master_task_list, "completed", True)
        )

        """ Calculate the total number of incomplete tasks.
        """ # Count incomplete tasks in "master_task_list".
        incomplete_tasks = (
            count_occurrences(master_task_list, "completed", False)
        )

        """ Calculate the total number of overdue tasks and total number of tasks that
            are both incomplete and overdue.
        """
        # Initialise empty lists to count the relevant occurrences.
        overdue = []
        incomplete_overdue = []

        # Iterate through all of the tasks in the Task Manager.
        for task in master_task_list:
            
            # If a task is overdue, add a counter 'x' to the list "overdue".
            if (task["due_date"]).date() < (date.today()):
                overdue.append('x')

                # If the task is also incomplete, add a counter 'x' to the list "incomplete_overdue".
                if (task["completed"] == False):
                    incomplete_overdue.append('x')

        # Count the number of overdue tasks.
        overdue_tasks = len(overdue)

        # Count the number of tasks that are both incomplete and overdue.
        incomplete_overdue_tasks = len(incomplete_overdue)
        
        """ Calculate the percentage of tasks that are incomplete.
        """
        percent_incomplete = round((incomplete_tasks / total_num_tasks)*100, 2)

        """ Calculate the percentage of tasks that are overdue.
        """
        percent_overdue = round((overdue_tasks / total_num_tasks)*100, 2)


        """ ------------- If there no tasks found in the Task Manager. -------------- """

    else:
        # Set values for the required variables to avoid zero division errors.
        completed_tasks = 0
        incomplete_tasks = 0
        incomplete_overdue_tasks = 0
        percent_incomplete = 0
        percent_overdue = 0


    """ ------------------ Display the Task Overview for the user. ------------------ """

    # Store each statement within a "task_overview_list".
    task_overview_list = [

        # Total tasks.
        f"The total number of tasks that have been generated is: \t\t\t{total_num_tasks}",

        # Completed tasks.
        f"The total number of completed tasks is: \t\t\t\t{completed_tasks}",

        # Incomplete tasks.
        f"The total number of incomplete tasks is: \t\t\t\t{incomplete_tasks}",

        # Incomplete and overdue tasks.
        f"The total number of tasks that are incomplete and overdue is: \t\t{incomplete_overdue_tasks}",

        # Percentage incomplete.
        f"The percentage of tasks that are incomplete is: \t\t\t{percent_incomplete}%",

        # Percentage overdue.
        f"The percentage of tasks that are overdue is: \t\t\t\t{percent_overdue}%"
    ]

    # Display the Task Overview for the user.
    for statement in task_overview_list:
        print(statement)

    # Print a divider.
    print("-"*80 + "\n")


    """ --------- Write the Task Overview to the "task_overview.txt" file. ---------- """
    
    # Generate the "task_overview.txt" file and add a heading.
    with open("task_overview.txt", 'w',  encoding="utf-8") as file:
        file.write("-------------------------------- Task Overview --------------------------------\n\n")

    # Write the Task Overview into the "task_overview.txt" file.
    for statement in task_overview_list:
        with open("task_overview.txt", 'a',  encoding="utf-8") as file:
            file.write(statement)
            # End each statement with a new line character.
            file.write("\n")
    


    """ -*-*-*-*-*-*-*-*-*-*-*-* Generate User Overview. *-*-*-*-*-*-*-*-*-*-*-*-*-*- """

    """ Display sub-section heading.
    """
    print("-"*80)
    print("***** User Overview *****\n")


    """ -------------- Calculate the total number of registered users. -------------- """
    
    total_users = len(username_password)

  
    """ ---------------- Generate text to display in User Overview. ----------------- """
    
    # Store each statement within a "task_overview_list".
    user_overview_list = [

        # Total users.
        f"The total number of users that are registered in the Task Manager is:\t{total_users}",

        # Total tasks.
        f"The total number of tasks that have been generated is:\t\t\t{total_num_tasks}",

        "\n\n"
    ]
    

    """ ------------------------ For each registered user: -------------------------- """

    for user in username_password.keys():

        # Calculate the total number of assigned tasks.
        user_tasks, task_nums = get_user_list(user)
        assigned_tasks = len(user_tasks)

        """ ------------------- If the user has assigned tasks. --------------------- """

        if assigned_tasks:
            
            # Calculate the total number of completed tasks.
            tasks_complete = count_occurrences(user_tasks, "completed", True)

            # Calculate the total number of incomplete tasks.
            tasks_incomplete = count_occurrences(user_tasks, "completed", False)

            # Calculate the percentage of tasks assigned to the user.
            percent_of_total = round((assigned_tasks / total_num_tasks)*100, 2)

            # Calculate the percentage of the user's tasks which are complete.
            percent_complete = round((tasks_complete / assigned_tasks)*100, 2)

            # Calculate the percentage of the user's tasks which are incomplete.
            percent_incomplete_user = round((tasks_incomplete / assigned_tasks)*100, 2)

            # Calculate the number of tasks that are both incomplete and overdue.
            # Initialise a list to count the occurrences.
            incomplete_overdue_count = []
            # Iterate through all of the tasks assigned to the user.
            for task in user_tasks:
                # If a task is overdue, check if it's also incomplete.
                if (task["due_date"]).date() < (date.today()):
                    if (task["completed"] == False):
                        # If the task is both incomplete and overdue, add a counter 'x' to the list.
                        incomplete_overdue_count.append('x')
            # Count the number of tasks that are both incomplete and overdue.
            incomplete_overdue_user = len(incomplete_overdue_count)

            # Calculate the percentage of the user's tasks that are both incomplete and overdue.
            percent_incomplete_overdue = round((incomplete_overdue_user / assigned_tasks)*100, 2)
            

            """ -------------- If the user does not have any tasks. ----------------- """

        else:
            # Set values for the required variables to avoid zero division errors.
            assigned_tasks = 0
            tasks_complete = 0
            tasks_incomplete = 0
            percent_of_total = 0
            percent_complete = 0
            percent_incomplete_user = 0
            percent_incomplete_overdue = 0

        
        """ ----------------- Generate text to display for each user. --------------- """

        user_subheading = ("-"*15 + f" User Stats - {user} "+ "-"*15 + "\n")

        # Store each statement within a "user_sublist".
        user_sublist = [

            # Include a subheading for the user.
            user_subheading,

            # Assigned tasks.
            f"The total number of assigned tasks is: \t\t\t\t\t{assigned_tasks}",

            # Percentage of total tasks.
            f"As a percentage of all tasks this is: \t\t\t\t\t{percent_of_total}%",

            # Percentage of tasks complete.
            f"The percentage of tasks that are complete is: \t\t\t\t{percent_complete}%",

            # Percentage of tasks incomplete.
            f"The percentage of tasks that are incomplete is: \t\t\t{percent_incomplete_user}%",

            # Percentage of tasks that are incomplete and overdue.
            f"The percentage of tasks that are incomplete and overdue is: \t\t{percent_incomplete_overdue}%\n"
        ]

        # Append the "user_sublist" to the "user_overview_list".
        for statement in user_sublist:
            user_overview_list.append(statement)
        

    """ ------------------ Display the User Overview for the user. ------------------ """

    for statement in user_overview_list:
        print(statement)

    # Print a divider.
    print("-"*80)


    """ -------- Write the User Overview to the "user_overview.txt" file. ----------- """

    # Generate the "user_overview.txt" file and add a heading.
    with open("user_overview.txt", 'w',  encoding="utf-8") as file:
        file.write("-------------------------------- User Overview --------------------------------\n\n")

    # Write the User Overview into the "user_overview.txt" file.
    for statement in user_overview_list:
        with open("user_overview.txt", 'a',  encoding="utf-8") as file:
            file.write(statement)
            # End each statement with a new line character.
            file.write("\n")
    



def count_occurrences(list_of_dictionaries, key, condition):
    """
    This function counts the occurrences of a given value within a list that contains
    list items in the form of dictionaries.

    Parameters:

        "condition" =               a dictionary value of which the occurrences are to be
                                    counted

        "key" =                     the corresponding dictionary key of the "condition"
                                    to be counted

        "list_of_dictionaries" =    the list to be searched for "condition" occurrences
    """

    # Initialise a list to count the occurrences of the given "condition".
    occurrences = []

    # Iterate through all sub-dictionaries in the "list_of_dictionaries".
    for dictionary in list_of_dictionaries:
        
        # If an instance of the "condition" is identified:
        if dictionary[key] == condition:
            # Append a counter 'x' to the list "occurrences".
            occurrences.append('x')
    
    # Calculate the total number of occurrences.
    occurrence_count = len(occurrences)

    # Return the result.
    return occurrence_count




def display_statistics():
    '''
    This function permits the "admin" user to display statistics about the number of
    users and tasks without generating full reports.

    The statistics that are generated are read from the "tasks.txt" and "users.txt" files
    as per the Project Instructions.
    These files are initialised when the program starts.
    '''
    
    """ Display a section heading.
    """
    print("-"*100)
    print("DISPLAY STATISTICS\n")


    """ ------------------ If the user is not the "admin" user. ----------------------"""

    if login_username != "admin":

        # Show an error message to the user.
        print("Sorry, you are not authorised to display statistics.")

        # Return to the Main Menu.
        return
    

        """ ---------------- If the user is the "admin" user. ------------------------"""

    elif login_username == "admin":

        # Calculate the total number of users from the number of lines in "users.txt".
        with open("users.txt", 'r', encoding="utf-8") as file:
            total_users = len(file.readlines())

        # Calculate the total number of tasks from the number of lines in "tasks.txt".
        with open("tasks.txt", 'r', encoding="utf-8") as file:
            total_tasks = len(file.readlines())

        # Display the statistics for the user in a readable format.
        print("------------------------------------")
        print(f"Total number of users: \t\t {total_users}")
        print(f"Total number of tasks: \t\t {total_tasks}")
        print("------------------------------------")  






# ----------------------------- Initialising task storage. ------------------------------
"""
The "tasks.txt" file stores all of the task-related information for the program. It is
structured similarly to a .csv file.
The "tasks.txt" file is initialised when the program starts.

If the file does not exist already from a previous use of the program, a new, empty
"tasks.txt" file is created. An existing "tasks.txt" file can be reopened by the program.

The current, complete list of tasks is also stored within a variable "master_task_list",
which is used by the program to display tasks, add tasks, modify tasks, and generate
reports on current task status.
"""


# Create "tasks.txt" if it doesn't already exist.
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", 'w', encoding="utf-8") as default_file:
        pass

# Read a list of "task_data" from the "tasks.txt" file for later use in the program.
with open("tasks.txt", 'r', encoding="utf-8") as task_file:
    
    # Store the "task_data" for all tasks as a list. Remove "\n".
    task_data = task_file.read().split("\n")

    # Remove any empty lines from the list.
    task_data = [line for line in task_data if line != '']

# Overwrite the "tasks.txt" file with all empty lines removed.
with open("tasks.txt", 'w', encoding="utf-8") as task_file:
    task_file.write("\n".join(task_data))


# Initialise a master list which will store dictionary items containing each individual task.
master_task_list = []


# Populate the "master_task_list" by iterating through the "task_data" list items.
for each_task in task_data:

    # Split "each_task" by ';' into a list of "task_components".
    task_components = each_task.split(';')

    # Initialise an empty dictionary to store the "task_components" for the "current_task".
    current_task = {}

    # Add each task component to the "current_task" dictionary.
    current_task["username"] = task_components[0]
    current_task["title"] = task_components[1]
    current_task["description"] = task_components[2]
    current_task["assigned_date"] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    current_task["due_date"] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    current_task["completed"] = True if task_components[5] == "Yes" else False
    # If a task has been previously updated, add this date as another task component.
    if (len(task_components) >= 7):
        current_task["updated_date"] = task_components[6]

    # Append each populated "current_task" dictionary to the "master_task_list".
    master_task_list.append(current_task)







# ----------------------------- Requesting user login. ----------------------------------
'''
This code section controls user login.

First, if the file does not exist already from a previous use of the program, a new
"users.txt" file is created containing a default admin account.
An existing "users.txt" file can be reopened by the program.

Second, the user is requested to enter their "login_username" and "login_password". The
input is compared against the registered users in the "users.txt" file, and if the input
is recognised, the user is granted login. Otherwise, the user will be prompted to
re-enter the correct details.

This code block is included within the main body of the program, rather than contained
within a separate function, to ensure that the variable "login_username" remains
accessible throughout the program as a means of determining the current user's access
privileges.

Additionally, the "username_password" dictionary stores a current list of all users and
passwords, which is used later in the program.

'''

# If no "users.txt" file currently exists, write one with a default "admin" account.
if not os.path.exists("users.txt"):
    with open("users.txt", 'w', encoding="utf-8") as default_file:
        default_file.write("admin;password")


# Read a list of "user_data" from the "users.txt" file for later use within the program.
with open("users.txt", 'r', encoding="utf-8") as user_file:

    # Store "user_data" as a list containing linked usernames and passwords as strings.
    user_data = user_file.read().split("\n")

    # Remove any empty lines from the list.
    user_data = [user for user in user_data if user != '']

# Overwrite the "users.txt" file with any empty lines removed.
with open("users.txt", 'w', encoding="utf-8") as user_file:
    user_file.write("\n".join(user_data))


# Initialise a "username_password" dictionary to store paired usernames and passwords.
username_password = {}

# Populate the "username_password" dictionary by iterating through the "user_data" items.
for each_user in user_data:
    # Split "each_user" by ';' into "username" and "password".
    username, password = each_user.split(';')
    # Store the "username" and "password" as a key:value pair within "username_password".
    username_password[username] = password


# Initial login state is set to False.
logged_in = False

# Show LOGIN menu to user until successful login with recognised values.
while not logged_in:

    # Print a divider and menu message for readability.
    print("-"*100)
    print("LOGIN\n")

    # Ask the user to input their username.
    login_username = input("Username:\t")

    # If the username input is not found in the "users.txt" file, display error message.
    if login_username not in username_password.keys():
        print("\n\t** That user does not exist. **")
        # Proceed to display LOGIN menu again, and ask for re-input of username.
        continue

    # Ask the user to input their password.
    login_password = input("Password:\t")

    # If the password does not match the username, display an error message.
    if username_password[login_username] != login_password:
        print("\n\t** Incorrect password. **")
        # Proceed to LOGIN menu again, to ask for re-input of username and password.
        continue

    # Login is successful if the username and password are recognised as matching.
    else:
        print("\nLogin successful!")
        logged_in = True

# After login is confirmed, initialise "done" variable for later control of program exit.
done = False







# ------------------------------ Displaying Main Menu. ----------------------------------
"""
This block of code presents the Main Menu to the user.
The menu will continue to be presented until the user chooses option 'e' to exit.
"""

while not done:

    """ ----------------------- Request user menu choice. --------------------------- """

    print("-"*100)
    print("Welcome to the Main Menu!")

    # User input is converted to lowercase.
    menu_choice = input(
        "Please select one of the following options:\n"
            "\nr - registering a user\n"
            "a - adding a task\n"
            "va - view all tasks\n"
            "vm - view my tasks\n"
            "gr - generate reports\n"
            "ds - display statistics\n"
            "e - exit\n\n"
        ).lower()


    """ ---------------------- Option 'r' - add new user. --------------------------- """

    if menu_choice == 'r':
        reg_user()


        """ ------------------ Option 'a' - add new task. --------------------------- """

    elif menu_choice == 'a':
        add_task()


        """ ----------------- Option "va" - view all tasks. ------------------------- """

    elif menu_choice == 'va':
        view_all(master_task_list)
            

        """ ------------------ Option "vm" - view my tasks. ------------------------- """

    elif menu_choice == 'vm':
        view_mine()


        """ ----------------- Option "gr" - generate reports. ----------------------- """
    
    elif menu_choice == "gr":
        generate_reports()


        """ ---------------- Option "ds" - display statistics. ---------------------- """

    elif menu_choice == "ds":
        display_statistics()


        """ ------------------- Option 'e' - exit program. -------------------------- """

    elif menu_choice == 'e':

        # Display exit message.
        print('-'*100)
        print("Goodbye!\n")

        # Set "done" to True to exit the Main Menu while-loop and exit the program.
        done = True


        """ ----------------------- Input validation. ------------------------------- """

    else:
        # Display error message for invalid menu choices.
        print("\n\t** You have made an invalid choice. Please try again. **")

