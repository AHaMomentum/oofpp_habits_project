import click
import habit as h

@click.group()                                                      #click group combines the click commands from habit.py
def cli():                                                          #to one function def cli() by adding all commands to a group.
    """
    To navigate to a function, type 'python todo.py [command]!'
    You can find a list of all commands and their results below.
    """
    pass                                                            #This is an informative text that is displayed when invoking todo.py

cli.add_command(h.Habit.create)                                     #Through the add_command function, multiple click commands can
cli.add_command(h.Habit.extreme)                                    #be accessed from one function, here cli(), to enable easier access
cli.add_command(h.Habit.complete)
cli.add_command(h.Habit.edit)
cli.add_command(h.Habit.delete)
cli.add_command(h.Habit.view)
cli.add_command(h.Habit.analysis)
cli.add_command(h.Habit.run)
cli.add_command(h.Habit.period)

if __name__ == '__main__':                                         #as always, this invokes the cli() main function.
    cli()