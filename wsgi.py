import click, pytest, sys
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import User
from App.main import create_app
from App.controllers import ( create_user, create_student,get_all_users_json, get_all_users, initialize, open_position, staff_shortlist_student, decide_shortlist, get_shortlist_by_student, get_shortlist_by_position, get_positions_by_employer)
from App.controllers.shortlist import *
# add create_student

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)

#working
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
@click.argument("email", default="rob@example.com")
@click.argument("phone_number", default="1234567890")
@click.argument("user_type", default="staff")
def create_user_command(username, password, email, phone_number, user_type):
    result = create_user(username, password, email, phone_number, user_type)
    if result:
        print(f'{username} created!')
    else:
        print("User creation failed")

# this command will be : flask user create bob bobpass

# @user_cli.command("list", help="Lists users in the database")
# @click.argument("format", default="string")
# def list_user_command(format):
#     if format == 'string':
#         print(get_all_users())
#     else:
#         print(get_all_users_json())


#working
@user_cli.command("add_position", help="Employer opens a position")
@click.argument("employer_id", default=1)
@click.argument("title", default="Software Engineer")
@click.argument("number_of_positions", default=10)
@click.argument("gpa_requirement",default=3.0)

def add_position_command(employer_id,title, number_of_positions, gpa_requirement):
    
    position = open_position(employer_id, title, number_of_positions, gpa_requirement)
    if position:
        print(f'Employer {position.employer} created {position.title} position with id {position.id}')
    else:
        print(f'Employer {employer_id} does not exist')


# added
@user_cli.command("create_student", help="Creates a student")
@click.argument("username", default="Maizee")
@click.argument("password", default="Mpass")
@click.argument("email", default="Maizee@example.com")
@click.argument("phone_number", default="1234567890")
@click.argument("degree", default="Computer Science")
@click.argument("resume", default="Enthusiastic and ready to learn")
@click.argument("dob", default="2001-05-11")
@click.argument("gpa", default=3.0)
def create_student_command(username, password, email, phone_number, degree,resume,dob,gpa):
    result = create_student(username, password, email, phone_number, degree,resume,dob,gpa)
    if result:
        print(f'{result.username} with ID {result.id} created!')
    else:
        print("User creation failed", result)


#needed updating
@user_cli.command("add_to_shortlist", help="Staff adds a student to a shortlist")
@click.argument("staff_id", default=2)
@click.argument("student_id", default=5)
@click.argument("position_id", default=3)

def add_to_shortlist_command(staff_id, student_id, position_id):

    test = staff_shortlist_student(staff_id, student_id, position_id)
    if test:

        print(f'\nStudent application ID is {test.application.id} ')
        print("\n\n__________________________________________________________________________\n\n")
    else:
        print('One of the following is the issue:')
        print(f'    An application for this student {student_id} was not found.')
        print(f'    Student {student_id} does not meet GPA requirements')
        print(f'    A shortlist already exist for student {student_id}')
        print("\n\n__________________________________________________________________________\n\n")

# needed updating
@user_cli.command("get_shortlist", help="Gets a shortlist for a student")
@click.argument("student_id", default=5)
def get_shortlist_command(student_id):
    list = get_shortlist_by_student(student_id)
    if list:
        for item in list:
            print(f'Student {item.student_id} is shortlisted for position {item.position_id}')

        print("\n\n__________________________________________________________________________\n\n")
    else:
        print(f'Student {student_id} has no shortlists')
        print("\n\n__________________________________________________________________________\n\n")

# required minor update in shortlist controller
@user_cli.command("get_shortlist_by_position", help="Gets a shortlist for a position")
@click.argument("position_id", default=3)
def get_shortlist_by_position_command(position_id):
    list = get_shortlist_by_position(position_id)
    if list:
        for item in list:
            print(f'Student {item.student_id} is shortlisted for id: {item.position_id}')  
            print("\n__________________________________________________________________________\n")

    else:
        print(f'Position {position_id} has no shortlists')
        print("\n\n__________________________________________________________________________\n\n")

@user_cli.command("get_positions_by_employer", help="Gets all positions for an employer")
@click.argument("employer_id", default=1)
def get_positions_by_employer_command(employer_id):
    list = get_positions_by_employer(employer_id)
    if list:
        for item in list:
            print(f'Position {item.id} is {item.status}')
            print(f'    Position {item.id} has {item.number_of_positions} slots')
            print(f'    Position {item.id} is for {item.title}')
            print("\n\n__________________________________________________________________________\n\n")
    else:
            print(f'Employer {employer_id} has no positions')
            print("\n\n__________________________________________________________________________\n\n")


# this required edits in application model
@user_cli.command("decide_shortlist", help="Decides a student's shortlist outcome")
@click.argument("student_id", default=5)
@click.argument("position_id", default=3)
@click.argument("decision", default="accept")
def decide_shortlist_command(student_id, position_id, decision):

    decision = decision.lower().strip()
    if decision not in ['accept', 'reject']:
        print("Invalid. Decision must be either 'accept' or 'reject'")
        print("\n\n__________________________________________________________________________\n\n")
        return
    
    result = decide_shortlist(student_id, position_id, decision)
    
    if result:
        print(f'Student {result.application.student_id} is {decision} for position {position_id}')
        print("\n\n__________________________________________________________________________\n\n")
    else:
        print(f'Student {student_id} not in shortlist for position {position_id}')
        print("\n\n__________________________________________________________________________\n\n")






@user_cli.command("withdraw_application", help="Withdraw an application")
def withdraw_application_command():
    app=Application.query.get(5)
    if not app:
        print(f'No application found')
        print("\n\n__________________________________________________________________________\n\n")
        return

    print(f'Application : {app.id}  Status: {app.getStatus()}')

    app.withdraw()
    print(f'Application : {app.id}  Status: {app.getStatus()}')
    print("\n\n__________________________________________________________________________\n\n")

            
app.cli.add_command(user_cli) # add the group to the cli

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)