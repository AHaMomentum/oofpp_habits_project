# oofpp_habits_project
Welcome to this Object-Oriented and Functional Habit Tracker Project! In the following Manual you will see how to install and perform operations in the application.

<h2>Installation</h2>
Preconditions: An IDE supporting Python (VSCode, Pycharm) and a database with a hosting server (best: MariaDB)
<ul>
  <li>Download the folder</li>
  <li>In an IDE, import or open the folder of the project. Depending on the IDE, this will be done automatically and not require support or it will require a bit support.</li>
  <li>Ensure that the parameters of the database connector fit the database server and database.</li>
  <li>Open the terminal/command prompt and navigate to the now imported/opened folder of this project.</li>
</ul>

<h2>Performing Operations</h2>
<h4>The basic command to invoke this application is: python todo.py [command] <br> The following commands are available: </h4>
<table>
  <tr>
    <th>Command</th>
    <th>Result</th>
  </tr>
  <tr>
    <td>create</td>
    <td>Create a new habit with name and periodicity.</td>
  </tr>
  <tr>
    <td>delete</td>
    <td>Delete only the progress of an existing habit or completely delete an existing habit.</td>
  </tr>
  <tr>
    <td>edit</td>
    <td>Edit name and periodicity of an existing habit.</td>
  </tr>
  <tr>
    <td>complete</td>
    <td>Check of a task as completed.</td>
  </tr>
  <tr>
    <td>view</td>
    <td>View all listed habits and view a visualisation of their course in a graph.</td>
  </tr>
  <tr>
    <td>extreme</td>
    <td>Get the habit with the longest streak run and/or get the habit that has been practiced the longest.</td>
  </tr>
  <tr>
    <td>analysis</td>
    <td>Get the number of breaks in a streak run, start date, completions, and course in a graph of a habit.</td>
  </tr>
  <tr>
    <td>run</td>
    <td>Get all habits with a specific streak run.</td>
  </tr>
  <tr>
    <td>period</td>
    <td>Get all habits with a specific periodicity.</td>
  </tr>
</table>
(Please note that an overview of the commands can be found in the application when typing only python todo.py )
