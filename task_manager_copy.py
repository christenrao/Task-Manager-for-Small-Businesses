# This program will help members of a small business manage their tasks.
# It reads and writes users and tasks to user.txt
# and task.txt files respectively.

# Import datetime module.
from datetime import datetime


# Define required functions.
# Create a dictionary to load current users from user.txt.
def user_check():
    """This function reads the user.txt file
    and checks for existing users.
    """
    users = {}
    with open("user.txt", "r+") as file:
        for lines in file:
            username, password = lines.strip().split(", ")
            users[username] = password
    return users


# Function to remove blank lines from tasks.txt.
def remove_blank_lines():
    """This function removes blank lines from the 'tasks.txt' file
    and writes non-blank lines back to the file.
    """
    with open("tasks.txt", "r") as tasks_file:
        lines = tasks_file.readlines()
    non_blank_lines = [line.strip() for line in lines if line.strip()]
    with open("tasks.txt", "w") as tasks_file:
        tasks_file.write('\n'.join(non_blank_lines))


# Login section for users.
def login():
    """This function handles the login process for the
    Business Task Manager.

    It prompts the user to enter their username
    and password, checks if the credentials are valid, and if so,
    calls the main menu function.
    """
    print("""Business Task Manager
      Welcome!\n""")

    while True:
        global username
        username = input("Please enter your username: ").lower()
        password = input("Please enter your password: ").lower()
        if username not in user_check():
            print("\nUsername not found! Please try again.\n")
        elif password != user_check()[username]:
            print("\nPassword does not match! Please try again.\n")
        else:
            print("\nSuccessful Login!\n")
            menu()
            return username


# Main Menu for users.
def menu():
    """This function handles the main menu of the program.

    It displays a list of options for the user and calls the
    corresponding functions based on the user's input.
    """
    while True:
        menu = input("""Select one of the following options:
r - register a user
a - add task
va - view all tasks
vm - view my tasks
gr - generate reports (admin only)
ds - display statistics (admin only)
e - exit
: """).lower()
        if menu == "r":
            reg_user()
        elif menu == "a":
            add_task()
        elif menu == "va":
            view_all()
        elif menu == "vm":
            view_mine()
        elif menu == "gr" and username == "admin":
            generate_report()
        elif menu == "ds" and username == "admin":
            display_statistics()
        elif menu == "e":
            print("\nGoodbye!!!\n")
            exit()
        else:
            print("\nYou have entered an invalid input OR you are not the admin. Please try again\n")


# Register a new user.
def reg_user():
    """This function handles the registration of new users.

    It prompts the user to enter a new username and password,
    checks if the username is unique, and if the passwords match.
    If all conditions are met, it writes the new user's details
    to the user.txt file.
    """
    while True:
        new_username = input("\nPlease enter in a new username: ").lower()
        if new_username not in user_check():
            new_password = input("\nPlease enter in a new password: ").lower()
            confirm_password = input("\nPlease enter in your password again: ").lower()
            if new_password == confirm_password:
                with open("user.txt", "a+") as file:
                    file.write("\n" + new_username + ", " + new_password)
                    print("\nNew user registered successfully.\n")
                    break
            else:
                print("\nYour passwords do not match. Please try again.\n")
        else:
            print("\nThis username is already taken. Please try again.\n")


# Add a new task.
def add_task():
    """This function handles the addition of new tasks.

    It prompts the user to enter a username, task title,
    task description, and due date. It checks if the username exists
    in the user_check() function. If the username exists, it writes the
    task details to the tasks.txt file. If the username does not exist,
    it prints an appropriate error message.
    """
    task_username = input("\nPlease enter the username of the person you want to assign the task to: ").lower()
    if task_username in user_check():
        task_title = input("\nPlease enter the title of the task: ")
        task_description = input("\nPlease enter a description of the task: ")
        time = datetime.today().strftime("%d %b %Y")
        try:
            task_due_date = input("\nPlease enter the due date of the task (YYYY-MM-DD): ")
            task_due_date = datetime.strptime(task_due_date, "%Y-%m-%d").strftime("%d %b %Y")
        except ValueError:
            print("\nInvalid date format. Please try again.\n")
            task_due_date = input("\nPlease enter the due date of the task (YYYY-MM-DD): ")
            task_due_date = datetime.strptime(task_due_date, "%Y-%m-%d").strftime("%d %b %Y")
        task_complete = "No"
        with open("tasks.txt", "a") as tasks_file:
            tasks_file.write(f"\n{task_username}, {task_title}, {task_description}, {time}, {task_due_date}, {task_complete}")
            print(f"\nTask: {task_title} has been successfully added.\n")
            remove_blank_lines()
    else:
        print("""\nThis user does not exist. Please register a new user to continue.
OR
This user has been recently added. Please exit and login again to add a task to the new user.\n""")


# View all the tasks.
def view_all():
    """This function reads all tasks from the tasks.txt file
    and prints them in a formatted manner.
    """
    with open("tasks.txt", "r") as tasks_file:
        for i, lines in enumerate(tasks_file):
            if lines.strip():
                task_username, task_title, task_description, time, task_due_date, task_complete = lines.strip().split(", ")
                print(f"\n{str(i + 1)}.Task:         ", task_title)
                print("Assigned to:    ", task_username)
                print("Date assigned:  ", time)
                print("Due Date:       ", task_due_date)
                print("Task Complete?  ", task_complete)
                print("Task Description:\n", task_description + "\n")


# View only the user's tasks.
def view_mine():
    """This function reads the tasks assigned to the logged-in user from
    the tasks.txt file and prints them in a formatted manner.

    It also calls the edit_task function to allow editing of the tasks.

    Returns:
    my_tasks (list): A list of tasks assigned to the logged-in user.
    """
    global my_tasks, user_tasks
    my_tasks = []
    assign_task = False
    
    with open("tasks.txt", "r") as tasks_file:
        for i, lines in enumerate(tasks_file, start=1):
            if lines.strip():
                task_username, task_title, task_description, time, task_due_date, task_complete = lines.strip().split(", ")
                user_tasks = lines.strip().split(",")
                my_tasks.append(user_tasks)
                if task_username == username:
                    assign_task = True
                    print(f"\n{str(i)}.Task:         ", task_title)
                    print("Assigned to:    ", task_username)
                    print("Date assigned:  ", time)
                    print("Due Date:       ", task_due_date)
                    print("Task Complete?  ", task_complete)
                    print("Task Description:\n", task_description + "\n")
    if assign_task:
        edit_task()
    else:
        print("\nYou have no tasks assigned to you.\n")

    return my_tasks


# Edit task choices.
def edit_task():
    """This function allows the user to edit a task.

    The user can either mark a task as complete,
    or edit the username or due date of the task.
    The function reads the tasks from the tasks.txt file,
    and writes the updated tasks back to the file.
    """
    try:
        task_selection = int(input("\nPlease select a task number to edit or -1 to exit: "))
        if task_selection == -1:
            menu()
        elif 1 <= task_selection <= len(my_tasks):
            task = my_tasks[task_selection - 1]
            if task[5] == " No":
                try:
                    edit_task_choice = int(input("\nEnter 1 to mark the task complete or 2 to edit the task: "))
                    if edit_task_choice == 1:
                        if task in my_tasks:
                            newer_task = my_tasks[task_selection - 1]
                            newer_task[5] = " Yes"
                            my_tasks[task_selection - 1] = newer_task
                            with open("tasks.txt", "w") as tasks_file:
                                for task in my_tasks:
                                    tasks_file.write(','.join(task)+'\n')
                                    remove_blank_lines()
                            print("\nYour task has been marked as complete.\n")
                        else:
                            print("\n You have entered invalid input. Please try again.")
                    elif edit_task_choice == 2:
                        try:
                            username_or_date = int(input("\nEnter 1 to edit the username of this task or 2 to edit the due date of the task: "))
                            if username_or_date == 1:
                                task_username = input("\nPlease enter your username: ").lower()
                                new_task_username = input("\nPlease enter the new username of the user the task belongs to: ").lower()
                                if new_task_username and task_username in user_check():
                                    if task in my_tasks:
                                        newer_task = my_tasks[task_selection - 1]
                                        newer_task[0] = str(new_task_username)
                                        my_tasks[task_selection - 1] = newer_task
                                        with open("tasks.txt", "w") as tasks_file:
                                            for task in my_tasks:
                                                tasks_file.write(','.join(task) + '\n')
                                                remove_blank_lines()
                                        print("\nThe username has been edited.\n")
                                    else:
                                        print("\n You have entered invalid input. Please try again.")
                                else:
                                    print("\nThis user does not exist. Please try again.")
                            elif username_or_date == 2:
                                try:
                                    new_due_date = input("Please enter the new due date of the task (YYYY-MM-DD): ")
                                    new_due_date = datetime.strptime(new_due_date, "%Y-%m-%d").strftime("%d %b %Y")
                                except ValueError:
                                    print("\nInvalid date format. Please try again.\n")
                                    new_due_date = input("Please enter the new due date of the task (YYYY-MM-DD): ")
                                    new_due_date = datetime.strptime(new_due_date, "%Y-%m-%d").strftime("%d %b %Y")
                                if task in my_tasks:
                                    newer_task = my_tasks[task_selection - 1]
                                    newer_task[4] = str(" " + new_due_date)
                                    my_tasks[task_selection - 1] = newer_task
                                    with open("tasks.txt", "w") as tasks_file:
                                        for task in my_tasks:
                                            tasks_file.write(','.join(task)+'\n')
                                            remove_blank_lines()
                                    print("\nThe due date has been edited.\n")
                                else:
                                    print("\n You have entered invalid input. Please try again.\n")
                            else:
                                print("\nYou have entered an invalid input. Please try again\n")
                        except ValueError:
                            print("\nYou have entered an invalid input. Please try again.\n")
                    else:
                        print("\nYou have entered an invalid input. Please try again\n")
                except ValueError:
                    print("\nYou have entered an invalid input. Please try again\n")
            else:
                print("\nThis task is already complete. You cannot not edit it.\n")
        else:
            print("\nYou have entered an invalid input. Please try again\n")
    except ValueError:
        print("\nYou have entered an invalid input. Please try again\n")


# Generate two reports for the user logged in as admin.
def generate_report():
    """The first report, 'task_overview.txt', provides an overview of
    all tasks, including the total number of tasks, completed tasks,
    incomplete tasks, overdue tasks,
    and the percentages of incomplete and overdue tasks.

    The second report, 'user_overview.txt', provides an overview of
    all users, including the total number of users registered,
    total number of tasks, and the percentage of tasks assigned to each
    user, completed by each user, incomplete by each user,
    and overdue by each user.
    """
    task_count = 0
    completed_task_count = 0
    incomplete_task_count = 0
    overdue_count = 0
    user_task_count = {}
    user_completed_tasks = {}
    user_incomplete_tasks = {}
    user_overdue_tasks = {}
    all_tasks = []
    num_users = 0

    with open("tasks.txt", "r") as tasks_file:
        for line in tasks_file:
            items = line.strip().split(", ")
            all_tasks.append(items)

    for task in all_tasks:
        task_count += 1
        username = task[0]
        due_date = datetime.strptime(task[4].strip(), "%d %b %Y")
        if task[5].strip().lower() == "yes":
            completed_task_count += 1
            user_completed_tasks[username] = user_completed_tasks.get(username, 0) + 1
        else:
            incomplete_task_count += 1
            user_incomplete_tasks[username] = user_incomplete_tasks.get(username, 0) + 1
            if due_date < datetime.today():
                overdue_count += 1
                user_overdue_tasks[username] = user_overdue_tasks.get(username, 0) + 1

        user_task_count[username] = user_task_count.get(username, 0) + 1

    incomplete_percent = (incomplete_task_count / task_count) * 100 if task_count > 0 else 0
    overdue_percent = (overdue_count / incomplete_task_count) * 100 if incomplete_task_count > 0 else 0

    with open("task_overview.txt", "w") as task_overview_file:
        task_overview_file.write(f"""Task overview:
Total number of tasks: {task_count}
Completed tasks: {completed_task_count}
Incomplete tasks: {incomplete_task_count}
Overdue tasks: {overdue_count}
Percent incomplete tasks: {incomplete_percent:.2f}%
Percent overdue tasks: {overdue_percent:.2f}%""")

    with open("user.txt", "r") as user_file:
        for line in user_file:
            items = line.strip().split(",")
            num_users += 1

    with open("user_overview.txt", "w") as user_overview_file:
        user_overview_file.write(f"""User overview:\n
Total number of users registered: {num_users}
Total number of tasks: {task_count}\n""")
        for username, count in user_task_count.items():
            user_task_percentage = (count / task_count) * 100 if task_count > 0 else 0
            completed_task_percentage = (user_completed_tasks.get(username, 0) / count) * 100 if count > 0 else 0
            incomplete_task_percentage = (user_incomplete_tasks.get(username, 0) / count) * 100 if count > 0 else 0
            overdue_task_percentage = (user_overdue_tasks.get(username, 0) / count) * 100 if count > 0 else 0
            user_overview_file.write(f"""\nUsername: {username}
Tasks assigned: {count}
Percentage of total tasks assigned to {username}: {user_task_percentage:.2f}%
Percentage of {username}'s tasks completed: {completed_task_percentage:.2f}%
Percentage of {username}'s tasks incomplete: {incomplete_task_percentage:.2f}%
Percentage of {username}'s tasks overdue: {overdue_task_percentage:.2f}%\n""")

    print("""\n1. task_overview.txt has been successfully generated.
2. user_overview.txt has been successfully generated.\n""")


# Displays the statistics for the user logged in as admin.
def display_statistics():
    """This function reads the generated reports and
    prints their content.

    It first calls the generate_report
    function to ensure the reports are up-to-date.
    """
    generate_report()
    with open("task_overview.txt", "r") as task_overview_file:
        print(task_overview_file.read())
        print()

    with open("user_overview.txt", "r") as user_overview_file:
        print(user_overview_file.read())


# Entry point of the program.
def main():
    """It calls the user_check(), login(),
    and menu() functions in sequence.
    """
    user_check()
    login()
    menu()


if __name__ == "__main__":
    main()


"""References:
https://stackoverflow.com/questions/74821620/editing-data-in-a-text-file-in-python-for-a-given-condition
https://stackoverflow.com/questions/32822473/how-to-access-function-variables-in-another-function
https://stackoverflow.com/questions/50177173/how-do-i-get-flake8-to-reliably-ignore-rules-in-vs-code
https://www.geeksforgeeks.org/python-program-to-replace-specific-line-in-file/
https://www.geeksforgeeks.org/how-to-search-and-replace-text-in-a-file-in-python/
https://stackoverflow.com/questions/42259166/python-3-valueerror-not-enough-values-to-unpack-expected-3-got-2
https://stackoverflow.com/questions/27642839/converting-23-oct-2014-to-2014-10-23-in-python
https://stackoverflow.com/questions/27642839/converting-23-oct-2014-to-2014-10-23-in-python
https://ioflood.com/blog/python-get-current-date/#:~:text=To%20get%20the%20current%20date%20in%20Python%2C%20you%20can%20use,%2DMM%2DDD'%20format.&text=In%20this%20example%2C%20we%20first,class%20from%20the%20datetime%20module.
https://www.w3schools.com/python/ref_dictionary_get.asp
https://github.com/JakJak90/task_manager/blob/master/task_manager.py
https://www.geeksforgeeks.org/personalized-task-manager-in-python/
https://www.studocu.com/en-gb/messages/question/2865842/use-the-task-managerpy-file-for-this-project-also-make-use-of-the-supporting-text-files-usertxt
https://www.chegg.com/homework-help/questions-and-answers/follow-steps-create-copy-previous-task-task-managerpy-save-dropbox-folder-project-also-cop-q116680317?autotype=mix&search=%3Cdiv%3E%3Cp%3EUse+the+task_manager.py+file+for+this+project.+Also%2C+make+use+of+the+supporting+text+files+%28user.txt+and+tasks.txt%3C%2Fp%3E%3C%2Fdiv%3E%3Cdiv%3E%3C%2Fdiv%3E&searchid=9e72a250-ace0-447c-983a-04d0dc397055&searchtype=button_submit&strackid=1dd90c18cb08&trackid=ae275431d207&fromSearch=true&resultrank=4&searchscore=0.60807
https://stackoverflow.com/questions/419163/what-does-if-name-main-do
https://stackoverflow.com/questions/4041238/why-use-def-main/4041718#4041718
https://www.chegg.com/homework-help/questions-and-answers/create-copy-previous-capstone-project-task-managerpy-save-dropbox-folder-project-also-copy-q115690197?autotype=paste&search=%3Cdiv%3E%3Cp%3EUse+the+task_manager.py+file+for+this+project.+Also%2C+make+use+of+the+supporting+text+files+%28user.txt+and+tasks.txt%29+that+accompany+this+Capstone+project+in+this+folder.+In+this+task+you+will+be+modifying+this+program.%3C%2Fp%3E%3C%2Fdiv%3E%3Cdiv%3E%3C%2Fdiv%3E&searchid=141868e2-b065-4f8c-b26c-761ffe0c22b1&searchtype=&strackid=14945e1b5741&trackid=e7bf15dadf9c&fromSearch=true&resultrank=3&searchscore=0.68031
https://www.reddit.com/r/Python/comments/csyoge/pep8_line_length_at_80_is_very_strange/
https://peps.python.org/pep-0008/#:~:text=spaces%20for%20indentation.-,Maximum%20Line%20Length,be%20limited%20to%2072%20characters.
https://peps.python.org/pep-0257/
"""
