from datetime import datetime, timedelta
import click
import pymysql
import matplotlib.pyplot as plt

#initialising database objects, such as the connection and the cursor to be used later on
conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", password="MDBPassword", db="htdb")
cursor = conn.cursor()


class Habit:
#the Habit class. The habit class does not have getter and setter functions anymore, as they caused more harm than good. "Getting and Setting"
#is done through simple pymysql statements.

    @click.group() #this project uses click.group, in the click documentation the respective function cli() is described without parameters.
    def cli():                                                                              #click does not take arguments
        pass

    def __init__(self, datetime, str, float, int, ID):                                      #the __init__ Habit function, defining a Habit
        self.start = datetime
        self.name = str
        self.period = float
        self.streaks = int
        self.ID = ID


    #Creating a new task to establish a habit
    @click.command(help = "Add a new habit.")
    @click.option("--self", prompt = "Please enter the tasks name")
    @click.option("--period", prompt = "Please enter the reoccurrence in days (please use periods for punctuation)")
    def create(self, period):
        print("Creating a new Habit...")
        click.echo(f"Habit name: {self}")
        click.echo(f"Interval: {period}")
        if Habit.exists(self):                                                              #exists() checks if the habit is already in the database.
            print(f"Oops! Looks like the task already exists! Try looking for typos or edit the existing habit before trying again.")
            exit(1)                                                                         #If the habit is found in the DB, the function exits.
        else:
            new = Habit(datetime.now(), self, period, 0,0)                          #a new Habit with the passed parameters and default values is created.
            print("Starting at ", new.start, " the new habit ", new.name), " should be completed every ", new.period, " days."
            try:
                if (new.name == " ") or (new.period == " "):                                #If name or period are empty, the function is exited.
                    print("INVALID ACTION: Name and Duration cannot be empty!")
                    exit(1)
                else:
                    query = f"INSERT INTO habit (Task, Start, Duration, Streak) VALUES ('{new.name}', '{new.start}', '{new.period}', '{new.streaks}')"
                    cursor.execute(query)                                                   #The Habit is written into the table, except for the ID, which is created in the DB.
                    print(f"Hey, Congratulations! {cursor.rowcount} habit was successfully inserted in the database.")
                    conn.commit()
            except pymysql.err.OperationalError:
                print("Oops! We have an error creating the new habit. Please check if the Habit already exists or try again later.")

    #Delete a task or the progress from the database
    @click.command(help = "Reset your progress or delete a habit.")
    @click.option("--self", prompt = "Please enter the tasks name")
    @click.option("--progress", prompt = "Do you want to delete your progress only? Type yes or no")
    def delete(self, progress):
        print("Searching task in database...")
        if not Habit.exists(self):                                                          #exists() checks if the habit is in the DB, else the function exits.
            print(f"Oops! Looks like the task {self} does not exist! Try looking for typos or create the habit before trying again.")
            exit(1)
        else:
            if progress == "yes":                                                           #if progress is yes, only data from analysis table is deleted.
                progress_query = f"DELETE FROM analysis WHERE Task = '{self}'"              #Delete query for the analysis table in the database.
                cursor.execute(progress_query)
                conn.commit()
                print(f"Poof, just like magic! All progress for {self} was successfully deleted.")
            else:                                                                           #the habit is deleted, i.e., data from habit and analysis table are deleted.
                query_one = f"DELETE FROM analysis WHERE Task = '{self}'"                   #Delete query for the analysis table in the database.
                query_two = f"DELETE FROM habit WHERE Task='{self}'"                        #Delete query for the habit table in the database.
                cursor.execute(query_one)
                cursor.execute(query_two)
                conn.commit()
                print(f"All the good things must come to an end! {self} was successfully deleted.")


    #Edits an existing habit from the database
    @click.command(help = "Change an existing habit.")
    @click.option("--self", prompt = "Which task do you want to edit?")
    @click.option("--name", prompt = "Please enter the tasks new name")
    @click.option("--period", prompt = "Please enter the new reoccurrence in days (please use periods for punctuation)")
    def edit(self, name, period):                                                           #name and period can be overwritten with the same values again.
        click.echo(f"Searching for the habit {self} in database...")
        if not Habit.exists(self):                                                          #exists() checks if the task is listed in the DB, else the function is exited.
            print(f"Oops! Looks like the task {self} does not exist! Try looking for typos or create the habit before trying again.")
            exit(1)
        else:
            try:
                query_habit = f"UPDATE habit SET Task = '{name}', Duration = '{period}' WHERE Task = '{self}'"  #update name and duration in habit table
                query_analysis = f"UPDATE analysis SET Task = '{name}' WHERE Task = '{self}'"                   #update name in analysis table
                if (name == " ") or (period == " "):                                        #if name or period are empty, i.e.,
                    print("INVALID ACTION: Name and Duration cannot be empty!")             #are supposed to be overwritten with nothing
                    exit(1)
                else:                                                                       #if name and period are not empty:
                    cursor.execute(query_habit)                                             #execute the query in the habit table.
                    cursor.execute(query_analysis)                                          #execute the query in the analysis table.
                    conn.commit()
                    conn.commit()
                    print(f"Amazing! Your habit {name} was successfully updated!")
            except pymysql.err.OperationalError:
                print("Oops! Looks like we had a database error. Our apologies, please try again later.")


    #Checks of a task as complete by adding a streak number and if needed breaking the existing streak run.
    @click.command(help = "Check off a habit for today.")
    @click.option("--self", prompt = "Which task did you complete today?")      #self= task/habit name
    def complete(self):
        click.echo(f"Congratulations on completing {self} for today!")
        if not Habit.exists(self):                                                          #exists() checks if entered task is in DB, if not the function is exited
            print(f"Oops! Looks like the task {self} does not exist! Try looking for typos or create the habit before trying again.")
            exit(1)
        else:
            override_date = datetime.now()                                                  #at the moment's datetime is created to be used later
            read_habitID = f"SELECT HabitID FROM habit WHERE Task = '{self}'"
            cursor.execute(read_habitID)
            habitID = cursor.fetchone()[0]                                                  #HabitID is gotten from habit table in DB to be written to analysis
            read_streaks = f"SELECT Streak FROM habit WHERE Task = '{self}'"
            cursor.execute(read_streaks)
            streaks = cursor.fetchone()[0]                                                  #streaks are gotten from habit table in DB to be changed
            read_duration = f"SELECT Duration FROM habit WHERE Task = '{self}'"             #get the duration in which the task should be completed
            cursor.execute(read_duration)
            duration = cursor.fetchone()[0]
            minimum_time = timedelta(days = duration)                                       #minimum_time calculates the periodicity of the habit in passed time.
            print("Your set goal interval was ", minimum_time)
            try:                                                                            #CheckIn is the column for the date of the last task completions, therefore:
                read_checkin = f"SELECT CheckIn FROM habit WHERE Task = '{self}'"           #Get the latest date of task completion from DB
                cursor.execute(read_checkin)
                checkin = cursor.fetchone()[0]
                date_checkin = datetime(checkin.year, checkin.month, checkin.day)           #Calculate the Checkin date with only Year Month and Day, as such
                print("Next streak at: ", date_checkin + minimum_time)                      #The calculation awards streaks for respecting days, and not minutes or seconds
                compare_date = datetime(override_date.year, override_date.month, override_date.day)#The previously created current time is also stripped to year, month and day
            except:
                read_start = f"SELECT Start FROM habit WHERE Task = '{self}'"               #if there has not yet been a streak change, the column Start is used, as checkin is empty
                cursor.execute(read_start)                                                  #everything else is the same.
                start = cursor.fetchone()[0]
                date_checkin = datetime(start.year, start.month, start.day)
                print("Next streak at: ", date_checkin + minimum_time)
                compare_date = datetime(override_date.year, override_date.month, override_date.day)
            finally:
                if compare_date == (date_checkin + minimum_time):                           #If the current date is equal to the checkin date plus the periodicity of the habit
                    try:                                                                    #a streak is added
                        streakwrite = f"UPDATE habit SET Streak = Streak + 1, CheckIn='{override_date}' WHERE Task = '{self}'"
                        analysisquery = (f"INSERT INTO analysis (HabitID, Task, Streakdate, Streaknumber) VALUES ('{habitID}', '{self}', '{override_date}', '{streaks +1}')")
                        cursor.execute(streakwrite)                                         #table habit: Add a streak, change the checkIn date to today's date, and set the streakbreak to false.
                        cursor.execute(analysisquery)                                       #table analysis: Add a new row with the respective HabitID, the Task, today's date and current streaks
                        conn.commit()
                        print(f"Hooray! You increased your streak for {self}! Remember, consistency is the key...")
                    except pymysql.err.OperationalError:
                        print("Oops! Sorry, looks like we had a database error. Please try again in a few moments.")
                elif compare_date > (date_checkin + minimum_time):                          #If the current date is bigger than the checkin date plus the periodicity of the habit
                    try:                                                                    #no streak is added
                        write = f"UPDATE habit SET Streak = 0, CheckIn = '{override_date}' WHERE Task = '{self}'"
                        query = (f"INSERT INTO analysis (HabitID, Task, Streakdate, Streaknumber) VALUES ('{habitID}', '{self}', '{override_date}', '{streaks * 0}')")
                        cursor.execute(write)                                               #table habit: Set the streaks 0, change checkIn date to today's date and set the streakbreak to true.
                        cursor.execute(query)                                               #table analysis: Add new row with the respective HabitID, the Task, today's date and current streaks.
                        conn.commit()
                        print(f"Oh no! Your phenomenal streak for {self} was broken! But you know what they say about new beginnings...")
                    except pymysql.err.OperationalError:
                        print("Oops! Sorry, looks like we had a database error. Please try again in a few moments.")
                else:                                                                       #else the task was completed under the periodicity of the habit.
                    print("You accomplished this tasked under your set goal period! Sadly this does not earn you a streak.")


    #Shows all listed tasks in relation to their set duration
    @click.command(help = "Overview over all listed habits.")
    @click.option("--self", prompt = "Would you like to see a visualisation? Type yes or no")
    def view(self):                                                                         #view function shows all listed habits and their streak pattern
        task_list=[]                                                                        #required for for-loop output and as parameters for the graph
        read_task = f"SELECT Task FROM habit"                                               #get all tasks from the database
        cursor.execute(read_task)
        view_task = cursor.fetchall()
        for task in view_task:                                                              #for every element fetched from the database
            get_task = str(task)                                                            #convert the tuple into a string and
            gt = get_task.replace("('", '')                                     #remove unnecessary padding symbols
            str_task = gt.replace("',)", '')
            task_list.append(str_task)                                                      #the task fetched from database is added to the list.
            print(f"Listed Task: {str_task}")
        if self =="yes":                                                                    #if self == yes, visual output will be generated
            for task in task_list:                                                          #for every task that is in the task list
                get_date = f"SELECT Streakdate FROM analysis WHERE Task = '{task}'"         #select the streakdate from the database
                cursor.execute(get_date)                                                    #and select the streaknumber from the database
                date = cursor.fetchall()
                read_number = f"SELECT Streaknumber FROM analysis WHERE Task = '{task}'"
                cursor.execute(read_number)
                number = cursor.fetchall()
                                                                                            #Plot streakdate and srteaknumber and label it
                plt.plot(date, number, linestyle='solid' ,label= f"{task}")            #with the task name fetched earlier
            plt.xticks(rotation=90)
            plt.title("Task Overview")
            plt.ylabel("Streaks")
            plt.grid(True)
            plt.legend()
            plt.show()
        conn.commit()


    #Analysing extreme habits, i.e., habit with maximum streaks and longest habit
    @click.command(help = "Analyse extreme values of your habits.")
    @click.option("--self", prompt = "Would you like to see your longest streak run? Type yes or no")
    @click.option("--longest", prompt = "Would you like to see your longest habit? Type yes or no")
    def extreme(self, longest):
        if self == "yes":                                                                   #The MAX aggregate Function will
            read_highest = f"SELECT MAX(Streaknumber), Task FROM analysis"                  #return the task that has the
            cursor.execute(read_highest)                                                    #longest streakrun, i.e., the
            conn.commit()                                                                   #highest streaknumber in the DB
            highest_data = cursor.fetchall()
            for hd in highest_data:                                                         #With this for loop, data and
                str_ld = str(hd[0])                                                         #task name are assigned to variables
                str_th = str(hd[1])                                                         #after fetching from Database.
                print(f"Your longest streak run is at", str_ld, "for the habit", str_th)
        if longest == "yes":                                                                #The MIN aggregate Function will
            read_start = f"SELECT MIN(Start) FROM habit"                                    #return the task with the smallest
            cursor.execute(read_start)                                                      #start date in the database, i.e.,
            conn.commit()                                                                   #the longest habit
            longest_data = cursor.fetchone()
            time = longest_data[0]
            start_date = datetime.now() - time
            read_task = f"SELECT Task FROM habit WHERE (SELECT MIN(Start) FROM habit)"      #The second pymysql statement here
            cursor.execute(read_task)                                                       #selects only the name of the task
            task_data = cursor.fetchone()                                                   #the earliest start date was
            start_task = str(task_data[0])                                                  #fetched right at the beginning
            print(f"Your longest habit", start_task,"started", start_date, "ago")           #in a separate pymysql statement
        else:                                                                               #through the if-if-else structure, the
            exit(1)                                                                         #the function enables the user to
                                                                                            #explore as much or as little as they like

    #Analysing the streak properties of one habit, including maximum streaks, streak breaks and overall completions on the habit
    @click.command(help = "Analyse a habit of yours.")
    @click.option("--self", prompt = "Which task do you want to analyse?")
    def analysis(self):
        click.echo(f"Let us analyse the streaks of {self} ...")
        if not Habit.exists(self):                                                          #exists checks if task exists
            print(f"Oops! Looks like the task {self} does not exist! Try looking for typos or create the habit before trying again.")
            exit(1)                                                                         #if task does not exist, function
        else:                                                                               #is exited instead of throwing errors
            #STREAK BREAK ANALYSIS
            read_breaks = f"SELECT Streaknumber FROM analysis WHERE Task = '{self}' and Streaknumber = 0"
            cursor.execute(read_breaks)                                                     #Fetching all streaknumbers of the task
            breaks = cursor.fetchall()                                                      #that were 0, i.e., streakbreak
            i = 0
            for br in breaks:                                                               #the for-loop counts the number of
                i += 1                                                                      #streakbreaks.
            print("Streak breaks: ", i)
            #MAXIMUM STREAKS ANALYSIS
            read_max = f"SELECT MAX(Streaknumber) FROM analysis WHERE Task = '{self}'"      #Analysing the maximum streak with
            cursor.execute(read_max)                                                        #the classic sql MAX()
            result_max = cursor.fetchall()
            for m in result_max:                                                            #This for loop converts the one fetched
                str_max = str(m[0])                                                         #tuple object into a string.
            #START DATE ANALYSIS
            read_start = f"SELECT Start FROM habit WHERE Task = '{self}'"                   #Fetching the start date.
            cursor.execute(read_start)
            start = cursor.fetchall()
            for s in start:                                                                 #This for loop converts the one start
                time = s[0]                                                                 #date from a tuple into a string with
                str_start = time.strftime("%Y-%m-%d %H:%M:%S")                              #adequate date representation.
                print("Start date: ", str_start)
            #OVERALL CHECKINS
            read_completed = f"SELECT Task FROM analysis WHERE Task = '{self}'"             #Fetching all logged completions
            cursor.execute(read_completed)
            complete = cursor.fetchall()
            i = 0
            for c in complete:                                                              #This for loop again counts all results
                i += 1                                                                      #Here, every result is important, hence
            print("Overall completions: ", i)
            read_date = f"SELECT Streakdate FROM analysis WHERE Task = '{self}'"            # Select the X-axis values
            cursor.execute(read_date)
            date = cursor.fetchall()
            read_streaknumber = f"SELECT Streaknumber FROM analysis WHERE Task = '{self}'"  # Select the Y-axis values
            cursor.execute(read_streaknumber)
            streaknumber = cursor.fetchall()
            # creating a plot
            plt.plot(date, streaknumber)                                              # Plot X, Y, g
            plt.title(f"Activity of {self}")
            plt.xticks(rotation=90)
            plt.show()



    #Show habits with one specific streak run.
    @click.command(help = "Show all habits with a specific streak run")
    @click.option("--self", prompt = "Which streak run do you want to analyse? (Numeric input)")
    def run(self):                                                                          #self = number of streaks which
        click.echo(f"Let us analyse all tasks with a run of {self} ...")                    #should be searched for in DB
        if not Habit.has(self):                                                             #checks if the number of streaks exists
            print(f"Oops! Looks like a run of {self} does not exist! Maybe look for typos or try another streak run.")
            exit(1)                                                                         #exists the program instead of throwing an error
        else:
            try:
                streak_new = int(self)                                                      #This try-except block will catch all wrong inputs, such as text inputs
            except ValueError:                                                              #for numeric inputs. Upon entering a numeric value, the code is exited
                print('INVALID ACTION: Please enter a number:')                             #controlled instead of throwing an uncontrolled ValueError
                exit(1)
            read_run= f"SELECT Task FROM habit WHERE Streak = '{streak_new}'"               #From the Database, all Tasks with the corresponding
            cursor.execute(read_run)                                                        #Streaknumber are selected
            runner = cursor.fetchall()
            for rn in runner:                                                               #This for loop changes the retrieved object into a string
                str_run = str(rn[0])                                                        #to increase the User Experience
                print(f"Tasks with streak run of {self}: {str_run}")


    #Show habits of one periodicity
    @click.command(help = "Show all habits with a specific periodicity")
    @click.option("--self", prompt = "Which periodicity do you want to search for?")
    def period(self):
        click.echo(f"Searching for all tasks with periodicity {self} ...")
        if not Habit.occurs(self):                                                          #occurs() checks if the periodicity exists in the DB
            print(f"Oops! No task with the period {self} could be found! Try looking for typos or redo your entry.")
            exit(1)                                                                         #if the periodicity is not in the DB, the function exits
        else:                                                                               #if the period exists in DB:
            read_period= f"SELECT Task FROM habit WHERE Duration = '{self}'"                #get all Tasks from the table habit where the Duration equals
            cursor.execute(read_period)                                                     #the argument.
            result = cursor.fetchall()
            for res in result:                                                              #After retrieving from DB the elements are converted
                str_period = str(res[0])                                                    #from tuple to string for better output,
                print(f"Tasks with the periodicity {self}: {str_period}")                   #then printed


#check if the task that is the input parameter is even in the database. Return False if not.
#Prevents unnecessary executions of functions when data is not even present.
    def exists(self):
        try:
            query = f"SELECT Task FROM habit WHERE Task = '{self}'"                         #get the all tasks from the table habit where the name equals
            cursor.execute(query)                                                           #the passed argument.
            result = cursor.fetchall()
            if len(result) == 0:                                                            #If the result has no length, there is no task to which
                return False                                                                #this condition applies.
            else:                                                                           #Otherwise there exists one or more task in the table habit
                return True                                                                 #and thus in the database.
        except pymysql.err.OperationalError or pymysql.err.ProgrammingError:
            print("Database error")
            return False

#check if the streak that is the input parameter is even in the database. Return False if not.
#Prevents unnecessary executions of functions when data is not even present.
    def has(self):
        try:
            query = f"SELECT Streak FROM habit WHERE Streak = '{self}'"                     #get all streaks from table habit where the streak count
            cursor.execute(query)                                                           #equals the passed number argument
            result = cursor.fetchall()
            if len(result) == 0:                                                            #If the result has no length, there are no streaks of this
                return False                                                                #length.
            else:                                                                           #Otherwise, one (or more) habit has this number of streaks
                return True                                                                 #in the table habit and thus in the database.
        except pymysql.err.OperationalError or pymysql.err.ProgrammingError:
            print("Database error")
            return False


#checks if the searched for input parameter period is in the database. Returns False if not.
#Prevents unnecessary execution of functions when data is not even present.
    def occurs(self):
        try:
            query = f"SELECT Task FROM habit WHERE Duration = '{self}'"                     #get all tasks from the table habit where the periodicity equals
            cursor.execute(query)                                                           #the passed number argument.
            result = cursor.fetchall()
            if len(result) == 0:                                                            #If the result has no length, there are no tasks that have this
                return False                                                                #periodicity.
            else:                                                                           #Otherwise, this periodicity occurs in one or more tasks in the
                return True                                                                 #table habit and thus in the database.
        except pymysql.err.OperationalError or pymysql.err.ProgrammingError:
            print("Database error")
            return False