import pytest
from datetime import datetime
from click.testing import CliRunner
from habit import Habit
import pymysql

conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", password="MDBPassword", db="htdb")
cursor = conn.cursor()


@pytest.fixture
def habit_entry0():                                         #this fixture is used to get the first habit from the database.
    #start attribute of habit
    start_query = f"SELECT Start FROM habit"
    cursor.execute(start_query)
    start = cursor.fetchone()[0]
    #name attribute of habit
    name_query = f"SELECT Task FROM habit"
    cursor.execute(name_query)
    name = cursor.fetchone()[0]
    #period attribute of habit
    period_query = f"SELECT Duration FROM habit"
    cursor.execute(period_query)
    period = cursor.fetchone()[0]
    #streak attribute of habit
    streak_query = "SELECT Streak FROM habit"
    cursor.execute(streak_query)
    streaks = cursor.fetchone()[0]
    #ID attribute of habit
    ID_query = "SELECT HabitID FROM habit"
    cursor.execute(ID_query)
    ID = cursor.fetchone()[0]
    return Habit(start, name, period, streaks, ID)

@pytest.fixture
def habit_entry1():                                         #this fixture is used to enter create and delete a new habit.
    start: datetime = datetime.now()
    name: str = "Crafts"
    period: float = 2.5
    streaks: int = 0
    ID = 10
    return Habit(start, name, period, streaks, ID)

def test_habit(habit_entry0):                               #this test tests the habit 'habit_entry0' created above.
    assert habit_entry0 is not None                         #specifically it tests whether all elements retrieved from
    assert type(habit_entry0) is Habit                      #the database can be worked with and are not zero.
    assert habit_entry0.start is not None                   #The habit 'habit_entry1' does not need to be tested as all
    assert type(habit_entry0.start) is datetime             #datatypes were declared in the definition of the fixture
    assert habit_entry0.name is not None
    assert type(habit_entry0.name) is str
    assert habit_entry0.period is not None
    assert type(habit_entry0.period) is float
    assert habit_entry0.streaks is not None
    assert type(habit_entry0.streaks) is int
    assert habit_entry0.ID is not None
    assert type(habit_entry0.ID) is int

#CREATION/DELETION TEST
def test_create(habit_entry1):                              #this test tests how the create() function works with input.
   print("Function: Habit.create")                          #using a CliRunner, the functions click option can be invoked and
   create_runner = CliRunner()                              #parameters passed, such as here --self and --period with the values.
   creation = create_runner.invoke(Habit.create, f'--self {habit_entry1.name} --period {habit_entry1.period}')
   assert creation.exit_code == 0                           #if the exit code is 0, the test was executed okay.
   assert creation.output is not None                       #an output should be the result, else the function was not invoked correctly.
   print(creation)                                          #here the status of the execution is printed
   print(creation.output)                                   #here the execution result is printed
   assert creation.output.__contains__(habit_entry1.name)   #this function asserts that the created habit has the passed name.
   assert creation.output.__contains__(str(habit_entry1.period))    #asserts that the created habit has the passed period.

def test_delete(habit_entry1):                              #this test tests if the delete() function works with input.
    print("Function: Habit.delete")                         #Namely, this test is supposed to delete the previousely
    delete_runner = CliRunner()                             #created habit with the create() function
    deletion = delete_runner.invoke(Habit.delete, f'--self {habit_entry1.name} --progress no')
    assert deletion.exit_code == 0                          #if exit code is 0, the test was executed okay.
    assert deletion.output is not None                      #an output should be the result, else the function was not invoked correctly.
    print(deletion)                                         #prints the status of the execution
    print(deletion.output)                                  #prints the result of the execution

#EDITING TESTS
def test_edit(habit_entry0):                                #the test tests if the edit() function works with input.
    print("Function: Habit.edit")                           #Tests, if the first database entry can be edited.
    edit_runner = CliRunner()                               #Here, the new name and period are the same as before
    new_name = habit_entry0.name                            #the variable new_name can be passed as a param and searched for in the last step
    editing = edit_runner.invoke(Habit.edit, f'--self {habit_entry0.name} --name {new_name} --period {habit_entry0.period}')
    assert editing.exit_code == 0                           #if the exit code is 0, the test was executed without problem.
    assert editing.output is not None                       #an output should be produced, else the function ws invoked wrong
    print(editing)                                          #print status of test execution
    print(editing.output)                                   #print result of test execution
    assert editing.output.__contains__(new_name)            #asserts that the edited habit contains the new name

def test_complete(habit_entry0):                            #the test tests if the complete() function works with the input.
    print("Function: Habit.complete")                       #Tests if the passed habit name returns the habit as
    complete_runner = CliRunner()                           #successfully/unsuccessfully completed.
    completion = complete_runner.invoke(Habit.complete, ['--self', habit_entry0.name])
    assert completion.exit_code == 0                        #if exit code is 0, the test was executed without problem.
    assert completion.output is not None                    #the output should not be none, else the function was invoked wrong
    print(completion)                                       #print the status of the test execution
    print(completion.output)                                #print the result of the test execution
    assert completion.output.__contains__(habit_entry0.name)#asserts that the completed habit is the habit with the param name.

#ANALYTICS TESTS
def test_view():                                            #the test tests if the view() function works with the database.
    print("Function: Habit.view")                           #Tests if all habits are shown as a list and their
    view_runner1 = CliRunner()                              #course in a graph. (param 'yes' enables plotting the graph)
    view = view_runner1.invoke(Habit.view, ['--self', 'yes'])
    assert view.exit_code == 0                              #if exit code is 0, the test was executed without problem.
    assert view.output is not None                          #the output should not be none, else the function was wrong
    print(view)                                             #print the status of the test
    print(view.output)                                      #print the result of the test

def test_extreme():                                         #the test tests if the extreme() function with the database.
    print("Function: Habit.extreme")                        #Tests if the habit with the longest streak run and
    extreme_runner = CliRunner()                            #the longest habit are found in the database.
    extreme_result = extreme_runner.invoke(Habit.extreme, '--self yes --longest yes')
    assert extreme_result.exit_code == 0                    #if exit code is 0, the test was executed with no problem.
    assert extreme_result.output is not None                #output should not be none, else the function was invoked wrong.
    print(extreme_result)                                   #print the status of the test
    print(extreme_result.output)                            #print the result of the test

def test_analysis(habit_entry0):                            #the test tests if the analysis() function works with input.
    print("Function: Habit.analysis")                       #Tests if number of streakbreaks, startdate, completions
    analysis_runner = CliRunner()                           #and a graph with the course can be found for the entered habit name.
    analysis = analysis_runner.invoke(Habit.analysis, ['--self', habit_entry0.name])
    assert analysis.exit_code == 0                          #if exit code is 0, the test was executed with no problem.
    assert analysis.output is not None                      #output should not be none, else the function was invoked wrong
    print(analysis)                                         #print the status of the test
    print(analysis.output)                                  #print the result of the test
    assert analysis.output.__contains__(habit_entry0.name) and analysis.output.__contains__(str(habit_entry0.start))#assert the result contains the passed params

def test_run(habit_entry0):                                 #the test tests if the run() function works with input.
    print("Function: Habit.run")                            #Tests if all habits with the same streak run as the entered param
    run_runner = CliRunner()                                #are returned from the database.
    result = run_runner.invoke(Habit.run, ['--self', habit_entry0.streaks])
    assert result.exit_code == 0                            #if the exit code is 0, the test was executed with no problem
    assert result.output is not None                        #output should exist, else the function was invoked wrong
    print(result)                                           #print the status of the test
    print(result.output)                                    #print the result of the test
    assert result.output.__contains__(str(habit_entry0.streaks))#assert that the result includes the entered streak number

def test_period(habit_entry0):                              #the test tests if the period() function works with input.
    print("Function: Habit.period")                         #Tests if all habits with the same periodicity as the entered param
    period_runner = CliRunner()                             #are returned from the database.
    period_result = period_runner.invoke(Habit.period, ['--self', habit_entry0.period])
    assert period_result.exit_code == 0                     #if exit code is 0, then the test was executed without problem
    assert period_result.output is not None                 #output should exist, else the function was invoked wrong.
    print(period_result)                                    #print the status of the test
    print(period_result.output)                             #print the result of the test
    assert period_result.output.__contains__(str(habit_entry0.period))#assert that the result contains the passed period param

def test_exists(habit_entry0):                              #the test tests if the exists() function works with input.
    print("Function: Habit.exists")                         #Tests if the habit name can be found in the database.
    exists_result = Habit.exists(habit_entry0.name)         #function does not implement click, thus no CliRunner needed.
    print(exists_result)                                    #print status of the test, which equals result of the function.
    assert exists_result is not None                        #Execution result should exist, should thus be not none.
    assert exists_result is True                            #assert that habit name from database is found in database

def test_has(habit_entry0):                                 #the test tests if the has() function works with input.
    print("Function: Habit.has")                            #Tests if the habit streak can be found in the database.
    has_result = Habit.has(habit_entry0.streaks)            #function does not implement click, thus no CliRunner needed.
    print(has_result)                                       #print status of the test, which equals result of the function.
    assert has_result is not None                           #Execution result should exist, should thus be not none.
    assert has_result is True                               #assert that habit streak from database is found in database

def test_occurs(habit_entry0):                              #the test tests if the occurs() function works with input.
    print("Function: Habit.occurs")                         #Tests if the habit period can be found in the database.
    occurs_result = Habit.occurs(habit_entry0.period)       #function does not implement click, thus no CliRunner needed.
    print(occurs_result)                                    #print status of the test, which equals result of the function.
    assert occurs_result is not None                        #Execution result should exist, should thus be not none.
    assert occurs_result is True                            #assert that habit period from database is found in database