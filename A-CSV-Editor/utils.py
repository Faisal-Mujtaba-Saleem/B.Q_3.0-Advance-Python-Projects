from communicator import speak, recognize_speech_from_microphone as micInput
from csv_editor import CSVEditor
import shutil
# import sys


def centeralizing_width():
    size = shutil.get_terminal_size()
    width = size.columns
    return width


def is_convertible_to_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def print_commands(commands):
    for i, command_with_description in enumerate(commands):
        command, description = command_with_description
        print(f"{i}. {command} - {description}")


def seperate_commands(commands_with_description):
    return [cmd for cmd, desc, in commands_with_description]


def print_starting_messages(command_type, commands_to_print, csv_: CSVEditor = None):
    if command_type == 'main':
        speak(
            "Welcome to Commandline-CSV-Editor!".center(centeralizing_width()), dots=False)
        speak("Switch to typing by pressing \'shift\' on the keyboard. Say 'exit' at any time to leave the editor.".center(
            centeralizing_width()), dots=False)
        speak("Note: If you need to enter a digit -or- symbol, please switch to typing. Digits & symbols can't be saved or written using speech input.".center(centeralizing_width()), dots=False)
        speak(f"Here are the {
              command_type}-commands related to csv you can use:")

    if command_type == 'sub':
        speak(f'Here\'s the overview of {
              csv_.csv_file_path}')
        df = csv_.get_csv()
        print(df)

        speak(f"Here are the {
              command_type}-commands you can apply on your {csv_.csv_file_path}:")

    print_commands(commands_to_print)


def taking_setting_row_values_choice(csv_: CSVEditor, iteration_index=0):

    if len(csv_.get_cols()) > 1:
        if iteration_index == 0:
            speak("Please choose one of the following options:")
            speak(
                "1. Set all row values at once,\n2. Add them column by column,\n3. Keep the row empty")

        setting_row_values_choice = micInput(
            "Say/Type the number of your choice in 1-3")
        return setting_row_values_choice
    else:
        return None
