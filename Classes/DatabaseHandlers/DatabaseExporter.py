import os
import shutil
import sys
import wx
import wx.grid
from typing import Optional
from Classes.DatabaseHandlers.DatabaseEventHandlers import DatabaseConnector, logging


class TableData:
    def __init__(self, name: str, export: bool = False):
        """
        Represents data for a table.

        Parameters:
        - name (str): The name of the table.
        - export (bool): A flag indicating whether the table should be exported.
        """
        self.name = name
        self.export = export


class DatabaseExporter(wx.Frame):
    def __init__(self, parent, title, database_file: Optional[str] = "",
                 config_file: str = "./databases/config.ini"):
        """
        Initialize a DatabaseExporter instance.

        Parameters:
        - parent: The parent window.
        - title (str): The title of the window.
        - database_file (Optional[str]): The path to the SQLite database file.
        - config_file (str): The path to the configuration file.
        """
        super(DatabaseExporter, self).__init__(parent, title=title, size=(500, 300))

        self.db_events = DatabaseConnector(database_file)

        self.panel = wx.Panel(self)
        self.tables_grid = wx.grid.Grid(self.panel)

        self.tables_grid.CreateGrid(0, 2)
        self.tables_grid.SetColLabelValue(0, "Export")
        self.tables_grid.SetColLabelValue(1, "Table Name")

        """ INFO: load test example database for testing """
        self.load_tables(database_file)

        self.save_btn = wx.Button(self.panel, label="Save", size=(60, 40))
        self.save_btn.Bind(wx.EVT_BUTTON, self.on_save)

        self.import_btn = wx.Button(self.panel, label="Import", size=(60, 40))
        self.import_btn.Bind(wx.EVT_BUTTON, self.on_import)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.tables_grid, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.save_btn, 0, wx.ALIGN_RIGHT | wx.ALL, 5)
        sizer.Add(self.import_btn, 0, wx.ALIGN_RIGHT | wx.ALL, 5)

        self.panel.SetSizer(sizer)
        self.Centre()
        self.Show(True)

    def import_database(self, file_path: str) -> None:
        """
        Import a database file.

        Parameters:
        - file_path (str): The path to the database file.
        """
        try:
            base_name = os.path.basename(file_path)
            file_name, file_extension = os.path.splitext(base_name)
            new_file_path = f'{sys.path[1]}\\databases\\{file_name}{file_extension}'

            shutil.copy(file_path, new_file_path)

            try:
                self.tables_grid.DeleteRows(0, self.tables_grid.GetNumberRows())
            except Exception as e:
                logging.error(f"Error deleting table rows, wx: {e}")

            self.db_events.database_file = new_file_path
            self.load_tables(new_file_path)

            logging.info(f"Imported database file: {file_path}")
            wx.MessageBox("Database imported successfully!",
                          "Import Successful", wx.OK | wx.ICON_INFORMATION)
        except Exception as e:
            logging.error(f"Error importing database: {e}")
            wx.LogError(f"Error importing database: {e}")

    def on_import(self, event: wx.Event) -> None:
        """
        Event handler for the import button.
        """
        wildcard = "SQLite Database (*.db)|*.db|All files (*.*)|*.*"

        dialog = wx.FileDialog(
            self,
            message="Choose a database file to import",
            defaultDir=wx.GetHomeDir(),
            defaultFile="",
            wildcard=wildcard,
            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST,
        )

        if dialog.ShowModal() == wx.ID_OK:
            selected_file = dialog.GetPath()
            dialog.Destroy()

            try:
                self.import_database(selected_file)
            except Exception as e:
                logging.error(f"Error importing database: {e}")
                wx.LogError(f"Error importing database: {e}")
        else:
            dialog.Destroy()

    def on_save(self, event: wx.Event) -> None:
        """
        Event handler for the save button.
        """
        for i in range(self.tables_grid.GetNumberRows()):
            if self.tables_grid.GetCellValue(i, 0) == '1':
                table_name = self.tables_grid.GetCellValue(i, 1)
                try:
                    self.db_events.export_table_to_csv(table_name)
                    wx.MessageBox(f"{table_name} exported successfully!", "Export Successful",
                                  wx.OK | wx.ICON_INFORMATION)
                except Exception as e:
                    logging.error(f"Error exporting {table_name} to CSV: {e}")

    def load_tables(self, database_file: str) -> None:
        """
        Load tables from the database.

        Parameters:
        - database_file (str): The path to the SQLite database file.
        """
        try:
            sql_conn = self.db_events.connect()
            cursor = sql_conn.cursor()

            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()

            self.db_events.close_connection()

            table_data = [TableData(table[0]) for table in tables]

            self.tables_grid.AppendRows(len(table_data))

            for row, table in enumerate(table_data):
                self.tables_grid.SetCellEditor(row, 0, wx.grid.GridCellBoolEditor())
                self.tables_grid.SetCellRenderer(row, 0, wx.grid.GridCellBoolRenderer())
                self.tables_grid.SetCellEditor(row, 0, wx.grid.GridCellBoolEditor())
                self.tables_grid.SetCellValue(row, 1, table.name)
                self.tables_grid.SetReadOnly(row, 1)
        except Exception as e:
            logging.error(f"Error loading tables: {e}")
