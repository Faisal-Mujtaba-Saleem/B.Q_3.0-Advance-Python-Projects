from csv_editor import CSVEditor
from communicator import speak, recognize_speech_from_microphone as micInput
from utils import is_convertible_to_int, taking_setting_row_values_choice
import os


class CSV_Sub_Tasks:
    def __init__(self, csv_: CSVEditor, runSubCsvTasks):
        self.runSubCsvTasks = runSubCsvTasks
        self.csv_ = csv_
        self.added_rows = []
        self.added_cols = []

    def save_changes(self):
        speak("Here's the overview of the changes you made")
        df = self.csv_.get_csv()
        print(df)

        doSave = micInput(
            'Do you want to save the changes you made? Say "yes" to save the changes -or- "run sub csv tasks" to go back?'
        )
        if doSave == "run sub csv tasks":
            self.runSubCsvTasks(self.csv_)
        elif doSave == 'yes':
            speak(
                f"Type the filename/path where you want to save the changes -or- provide an empty input by directly pressing enter if you want to save your changes in the same CSV file, i.e., '{
                    self.csv_.csv_file_path}'"
            )
            csv_filename_path_toSave = input()

            if csv_filename_path_toSave == '':
                self.csv_.save_csv()
            else:
                self.csv_.save_csv(csv_filename_path_toSave)

            speak(
                f"Successfully saved the changes in the file {
                    csv_filename_path_toSave if csv_filename_path_toSave else self.csv_.csv_file_path}"
            )

            os.system(f'''start "{
                      csv_filename_path_toSave if csv_filename_path_toSave else self.csv_.csv_file_path}"''')

            self.runSubCsvTasks(self.csv_)
        else:
            speak("Your changes have not been saved. Any unsaved changes will be lost.")

    def load_csv(self):
        try:
            speak(
                'Please provide the file path of the CSV you want to load -or- say "run sub csv tasks" to go back.')
            csv_file_path = input()

            if csv_file_path == "run sub csv tasks":
                self.runSubCsvTasks(self.csv_)
            elif csv_file_path:
                self.csv_.load_csv(csv_file_path)
                speak(f"Successfully loaded the CSV file: {csv_file_path}")
            else:
                raise ValueError("No file path provided.")

            loaded_csv = self.csv_.get_csv()
            print(loaded_csv)

        except Exception as e:
            speak("An error occurred while loading the CSV file.")
            print(str(e))

    def addRow(self):
        try:
            speak(
                'How many rows do you want to add -or- say "run sub csv tasks"" to go back?')
            reply = input()

            if reply == "run sub csv tasks":
                self.runSubCsvTasks(self.csv_)
            else:
                no_of_rows_to_add = int(reply)

                for _ in range(no_of_rows_to_add):
                    row_index = self.csv_.add_row()
                    self.added_rows.append(row_index)

                if len(self.added_rows) == no_of_rows_to_add:
                    speak(f'Successfully added {
                          no_of_rows_to_add}/{len(self.added_rows)} rows!')
                    df = self.csv_.get_csv()
                    print(df)

                    for i, row_added in enumerate(self.added_rows):
                        speak(f'Row {row_added}:')
                        print(f'\n{self.csv_.get_row(row_added)}\n')

                        setting_row_values_choice = taking_setting_row_values_choice(
                            self.csv_, iteration_index=i
                        )

                        print(setting_row_values_choice)

                        if setting_row_values_choice is not None:
                            if setting_row_values_choice in {'one', '1'}:
                                values_to_set_in_row = micInput(
                                    'Say/Enter the comma separated row values'
                                ).split(', ')
                                values_to_set_in_row = [
                                    int(val) if is_convertible_to_int(
                                        val) else val
                                    for val in values_to_set_in_row
                                ]
                                self.csv_.set_row(
                                    row_added, values_to_set_in_row)
                                print(f'\n{self.csv_.get_row(row_added)}\n')

                            elif setting_row_values_choice in {'two', '2'}:
                                columns = self.csv_.get_csv().columns
                                for col in columns:
                                    value_to_set_in_col_of_row = micInput(
                                        f'Say the value for column \'{col}\''
                                    )
                                    if is_convertible_to_int(value_to_set_in_col_of_row):
                                        value_to_set_in_col_of_row = int(
                                            value_to_set_in_col_of_row)
                                    self.csv_.edit_row(
                                        value_to_set_in_col_of_row, row_added, col
                                    )
                                print(f'\n{self.csv_.get_row(row_added)}\n')

                            elif setting_row_values_choice in {'three', '3'}:
                                print(f'\n{self.csv_.get_row(row_added)}\n')

                            else:
                                raise ValueError(
                                    f'You must choose between 1, 2, -or- 3, but you entered {
                                        setting_row_values_choice}'
                                )

                        else:
                            speak(
                                "Set the row value -or- leave it empty by directly pressing 'enter'"
                            )
                            value_to_set_in_row = micInput('Say the row value')

                            if is_convertible_to_int(value_to_set_in_row):
                                value_to_set_in_row = int(value_to_set_in_row)

                            self.csv_.set_row(row_added, value_to_set_in_row)
                            print(f'\n{self.csv_.get_row(row_added)}\n')

                    self.save_changes()
                    self.addRow()

                else:
                    raise ValueError(
                        f'Failed to add the required {
                            no_of_rows_to_add}/{len(self.added_rows)} rows.'
                    )

        except Exception as e:
            speak("An error occurred while adding rows.")
            print(str(e))

            # Rollback the added rows in case of an error
            for row_added in reversed(self.added_rows):
                self.csv_.drop_row(row_added)
            self.added_rows.clear()

            # Retry adding rows
            self.addRow()

    def dropRow(self):
        try:
            speak(
                'Which row number do you want to drop -or- say "run sub csv tasks"" to go back?')
            reply_to_drop = input()

            if reply_to_drop == "run sub csv tasks":
                self.runSubCsvTasks(self.csv_)
            else:
                row_to_drop = int(reply_to_drop)
                if row_to_drop in self.csv_.get_csv().index:
                    self.csv_.drop_row(row_to_drop)
                    speak(f'Successfully dropped row {row_to_drop}')
                    df = self.csv_.get_csv()
                    print(df)
                    self.save_changes()
                    self.dropRow()
                else:
                    speak(f'Row {row_to_drop} does not exist.')
                    raise ValueError(f'Invalid row number: {row_to_drop}')

        except Exception as e:
            speak("An error occurred while dropping a row.")
            print(str(e))

    def editRow(self):
        try:
            speak(
                'Which row number do you want to edit -or- say "run sub csv tasks"" to go back?')
            reply = input()

            if reply == "run sub csv tasks":
                self.runSubCsvTasks(self.csv_)
            else:
                row_to_edit = int(reply)

                if row_to_edit in self.csv_.get_csv().index:
                    speak(f'Editing row {row_to_edit}')
                    columns = self.csv_.get_csv().columns
                    for col in columns:
                        value_to_set_in_col_of_row = micInput(
                            f'Say the value for column \'{col}\''
                        )
                        if is_convertible_to_int(value_to_set_in_col_of_row):
                            value_to_set_in_col_of_row = int(
                                value_to_set_in_col_of_row)
                        self.csv_.edit_row(
                            value_to_set_in_col_of_row, row_to_edit, col)

                    speak(f'Successfully edited row {row_to_edit}')
                    df = self.csv_.get_csv()
                    print(df)
                    self.save_changes()
                    self.editRow()

                else:
                    speak(f'Row {row_to_edit} does not exist.')
                    raise ValueError(f'Invalid row number: {row_to_edit}')

        except Exception as e:
            speak("An error occurred while editing a row.")
            print(str(e))

    def addColumn(self):
        try:
            column_name = micInput(
                'What is the name of the new column -or- say "run sub csv tasks"" to go back?')

            if column_name == "run sub csv tasks":
                self.runSubCsvTasks(self.csv_)
            elif column_name:
                self.csv_.add_column(column_name)
                speak(f'Successfully added column \'{column_name}\'')
                df = self.csv_.get_csv()
                print(df)
                self.save_changes()
                self.addColumn()
            else:
                raise ValueError("No column name provided.")

        except Exception as e:
            speak("An error occurred while adding a column.")
            print(str(e))

    def dropColumn(self):
        try:
            column_to_drop = micInput(
                'Which column do you want to drop -or- say "run sub csv tasks"" to go back?')

            if column_to_drop == "run sub csv tasks":
                self.runSubCsvTasks(self.csv_)
            elif column_to_drop in self.csv_.get_csv().columns:
                self.csv_.drop_column(column_to_drop)
                speak(f'Successfully dropped column \'{column_to_drop}\'')
                df = self.csv_.get_csv()
                print(df)
                self.save_changes()
                self.dropColumn()
            else:
                speak(f'Column \'{column_to_drop}\' does not exist.')
                raise ValueError(f'Invalid column name: {column_to_drop}')

        except Exception as e:
            speak("An error occurred while dropping a column.")
            print(str(e))

    def renameColumn(self):
        try:
            column_to_rename = micInput(
                'Which column do you want to rename -or- say "run sub csv tasks"" to go back?')

            if column_to_rename == "run sub csv tasks":
                self.runSubCsvTasks(self.csv_)
            elif column_to_rename in self.csv_.get_csv().columns:
                new_column_name = micInput(
                    'What is the new name of the column?')
                self.csv_.rename_column(column_to_rename, new_column_name)
                speak(f'Successfully renamed column \'{
                      column_to_rename}\' to \'{new_column_name}\'')

                self.save_changes()
                self.renameColumn()
            else:
                speak(f'Column \'{column_to_rename}\' does not exist.')
                raise ValueError(f'Invalid column name: {column_to_rename}')

        except Exception as e:
            speak("An error occurred while renaming a column.")
            print(str(e))

    def editColumn(self):
        try:
            column_to_edit = micInput(
                'Which column do you want to edit -or- say "run sub csv tasks"" to go back?')

            if column_to_edit == "run sub csv tasks":
                self.runSubCsvTasks(self.csv_)
            elif column_to_edit in self.csv_.get_csv().columns:
                if len(self.csv_.get_csv()[column_to_edit]) == 1:

                    value_to_set_in_col_of_row = micInput(
                        f'Say the value for the column "{column_to_edit}"')

                    if is_convertible_to_int(value_to_set_in_col_of_row):
                        value_to_set_in_col_of_row = int(
                            value_to_set_in_col_of_row)

                    self.csv_.set_cell(
                        0, column_to_edit, value_to_set_in_col_of_row
                    )
                else:
                    edit_choice = micInput(
                        f'Do you want to edit the whole column "{column_to_edit}" at once or cell by cell? Say "whole" or "cell".')

                    if edit_choice.lower() == "whole":
                        speak(f'Enter the new values for the whole column "{
                            column_to_edit}", separated by commas.')
                        new_column_values = input()

                        new_column_values = [val.strip()
                                             for val in new_column_values.split(',')]
                        self.csv_.set_column(column_to_edit, new_column_values)

                    elif edit_choice.lower() == "cell":
                        for row_index in self.csv_.get_csv().index:
                            value_to_set_in_row_of_col = micInput(
                                f'Say the value for row {row_index} in column "{column_to_edit}"')
                            if is_convertible_to_int(value_to_set_in_row_of_col):
                                value_to_set_in_row_of_col = int(
                                    value_to_set_in_row_of_col)
                            self.csv_.set_cell(
                                row_index, column_to_edit, value_to_set_in_row_of_col)

                    else:
                        speak(f'Invalid choice. Please say "whole" or "cell".')
                        raise ValueError(f'Invalid choice: {edit_choice}')

                    speak(f'Successfully edited column "{column_to_edit}"')

                self.save_changes()
                self.editColumn()

            else:
                speak(f'Column "{column_to_edit}" does not exist.')
                raise ValueError(f'Invalid column name: {column_to_edit}')

        except Exception as e:
            speak("An error occurred while editing a column.")
            print(str(e))

    def getRow(self):
        try:
            speak(
                'Which row number do you want to retrieve -or- say "run sub csv tasks"" to go back?')
            reply = input()

            if reply == "run sub csv tasks":
                self.runSubCsvTasks(self.csv_)
            else:
                row_to_get = int(reply)

                if row_to_get in self.csv_.get_csv().index:
                    row_data = self.csv_.get_row(row_to_get)
                    speak(f'Data in row {row_to_get}:')
                    print(row_data)
                    self.getRow()
                else:
                    speak(f'Row {row_to_get} does not exist.')
                    raise ValueError(f'Invalid row number: {row_to_get}')

        except Exception as e:
            speak("An error occurred while retrieving a row.")
            print(str(e))

    def getColumn(self):
        try:
            column_to_get = micInput(
                'Which column do you want to retrieve -or- say ""run sub csv tasks"" to go back?')

            if column_to_get == "run sub csv tasks":
                self.runSubCsvTasks(self.csv_)
            elif column_to_get in self.csv_.get_csv().columns:
                column_data = self.csv_.get_column(column_to_get)
                speak(f'Data in column \'{column_to_get}\':')
                print(column_data)
                self.getColumn()
            else:
                speak(f'Column \'{column_to_get}\' does not exist.')
                raise ValueError(f'Invalid column name: {column_to_get}')

        except Exception as e:
            speak("An error occurred while retrieving a column.")
            print(str(e))

    def getCSV(self):
        try:
            csv_data = self.csv_.get_csv()
            speak('Here is the CSV data:')
            print(csv_data)
            self.getCSV()

        except Exception as e:
            speak("An error occurred while retrieving the CSV data.")
            print(str(e))
