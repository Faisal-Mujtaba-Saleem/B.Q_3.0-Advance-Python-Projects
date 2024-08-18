import pandas as pd
import os


class CSVEditor:
    def __init__(self, csv_file_path=None):
        self._csv = pd.DataFrame()
        self._csv_file_path = None
        if csv_file_path:
            self.load_csv(csv_file_path)

    def load_csv(self, csv_file_path):
        """Load an existing CSV file."""
        if not csv_file_path.endswith('.csv'):
            csv_file_path += '.csv'
        if not os.path.exists(csv_file_path):
            raise FileNotFoundError(f"File '{csv_file_path}' not found.")
        self._csv = pd.read_csv(csv_file_path)
        if self._csv.empty:
            raise ValueError(f"The CSV file '{csv_file_path}' is empty.")
        self._csv_file_path = csv_file_path

    def save_csv(self, new_csv_file_path=None):
        """Save the current _csv to a CSV file."""
        path_to_save = new_csv_file_path or self._csv_file_path
        if not path_to_save:
            raise ValueError("CSV file path is not set.")
        self._csv.to_csv(path_to_save, index=False)
        self._csv_file_path = path_to_save

    def add_row(self, values=None):
        """Add a new row to the CSV."""
        if values and len(values) != len(self._csv.columns):
            raise ValueError(
                f"Expected {len(self._csv.columns)} values, got {len(values)}.")
        new_row = pd.Series(values, index=self._csv.columns)
        self._csv = self._csv.append(new_row, ignore_index=True)
        return len(self._csv) - 1

    def drop_row(self, row_index):
        """Drop a row from the CSV."""
        if row_index not in self._csv.index:
            raise IndexError(f"Row index {row_index} is out of bounds.")
        self._csv.drop(row_index, inplace=True)
        self._csv.reset_index(drop=True, inplace=True)

    def edit_row(self, row_index, new_values, column_names=None):
        """Edit a specific row in the CSV."""
        if column_names:
            if isinstance(column_names, str):
                column_names = [column_names]
            if not set(column_names).issubset(self._csv.columns):
                raise ValueError(f"Invalid column names: {column_names}")
            self._csv.loc[row_index, column_names] = new_values
        else:
            if len(new_values) != len(self._csv.columns):
                raise ValueError(f"Expected {len(self._csv.columns)} values, got {
                                 len(new_values)}.")
            self._csv.iloc[row_index] = new_values

    def add_column(self, column_name=None, default_value=None):
        """Add a new column to the CSV."""
        if column_name is None:
            column_name = f'column_{len(self._csv.columns)}'
        if column_name in self._csv.columns:
            raise ValueError(f"Column '{column_name}' already exists.")
        self._csv[column_name] = default_value

    def drop_column(self, column_name):
        """Drop a column from the CSV."""
        if column_name not in self._csv.columns:
            raise ValueError(f"Column '{column_name}' does not exist.")
        self._csv.drop(column_name, axis=1, inplace=True)

    def edit_column(self, column_name, new_values):
        """Edit the values of a specific column in the CSV."""
        if column_name not in self._csv.columns:
            raise ValueError(f"Column '{column_name}' does not exist.")
        if len(new_values) != len(self._csv):
            raise ValueError(f"Expected {len(self._csv)} values, got {
                             len(new_values)}.")
        self._csv[column_name] = new_values

    def get_csv(self):
        """Get the entire CSV."""
        return self._csv

    def get_indices(self):
        """Get the indices of the CSV."""
        return self._csv.index

    def get_cols(self):
        """Get the columns of the CSV."""
        return self._csv.columns

    def get_row(self, row_index):
        """Get a specific row from the CSV."""
        if row_index not in self._csv.index:
            raise IndexError(f"Row index {row_index} is out of bounds.")
        return self._csv.iloc[[row_index]]

    def set_row(self, row_index, new_row):
        """Edit a specific row in the CSV."""
        if len(new_row) != len(self._csv.columns):
            raise ValueError(
                f"Expected {len(self._csv.columns)} values, got {len(new_row)}.")
        self._csv.iloc[row_index] = new_row

    def get_column(self, column_name):
        """Get a specific column from the CSV."""
        if column_name not in self._csv.columns:
            raise ValueError(f"Column '{column_name}' does not exist.")
        return self._csv[column_name]

    def set_column(self, column_name, new_column):
        """Set a specific column in the CSV."""
        if len(new_column) != len(self._csv):
            raise ValueError(f"Expected {len(self._csv)} values, got {
                             len(new_column)}.")
        self._csv[column_name] = new_column

    def get_cell(self, row_index, column):
        """Get a specific cell from the CSV."""
        if row_index not in self._csv.index:
            raise IndexError(f"Row index {row_index} is out of bounds.")
        if column not in self._csv.columns:
            raise ValueError(f"Column '{column}' does not exist.")
        return self._csv.loc[row_index, column]

    def set_cell(self, row_index, column, new_value):
        """Set a specific cell in the CSV."""
        if row_index not in self._csv.index:
            raise IndexError(f"Row index {row_index} is out of bounds.")
        if column not in self._csv.columns:
            raise ValueError(f"Column '{column}' does not exist.")
        self._csv.loc[row_index, column] = new_value
        return self._csv.loc[row_index, column]

    @property
    def csv_file_path(self):
        """Get the file path of the CSV."""
        return self._csv_file_path

    @csv_file_path.setter
    def csv_file_path(self, new_file_path):
        """Set the file path of the CSV."""
        self._csv_file_path = new_file_path


class CreateCSV(CSVEditor):
    def __init__(self, csv_filename):
        """Create a new CSV file with the given headers."""
        super().__init__()

        if not csv_filename.endswith('.csv'):
            csv_filename += '.csv'

        self.save_csv(csv_filename)


class EditCSV(CSVEditor):
    def __init__(self, csv_file_path):
        """Load an existing CSV file."""
        super().__init__()

        if not csv_file_path.endswith('.csv'):
            csv_file_path += '.csv'

        self.load_csv(csv_file_path)
