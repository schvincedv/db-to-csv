from Classes.DatabaseHandlers import ImportRandomDB
from Classes.DatabaseHandlers.DatabaseExporter import DatabaseExporter
import wx


if __name__ == "__main__":
    db_path = ""
    db_path = ImportRandomDB.DatabaseCreator.create_random_db()  # Create random database first if it needs
    app = wx.App()
    DatabaseExporter(None, title="Database Exporter", database_file=db_path)
    app.MainLoop()
