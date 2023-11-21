# Database to CSV Converter

This project is a simple database to CSV converter application built using wxPython and SQLite. It allows users to import an SQLite database file, view tables, export selected tables to CSV files, and create a random example database for testing purposes.

# Note for the needs of the program
The upcoming update will involve the management of a MySQL connection through a secure tunnel using OpenVPN. Unfortunately, due to a shortage of time, health issues, and MySQL behaving conspicuously, it was detected like a printer that I intended to use at the last minute. I couldn't implement it as planned. Consequently, I had to improvise.

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features

- Import SQLite database files.
- View available tables in the database.
- Export selected tables to CSV files.
- Create a random example database for testing.

## Most prerequisites see more at [requirements.txt](requirements.txt)

- Python 3.9
- wxPython
- pandas
- SQLite3

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/schvincedv
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the application:

    ```bash
    python main.py
    ```

2. The main window will appear with options to import, export, and manage tables.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or create a pull request.

## License

This project is licensed under the [őHansága Studio © 2023](https://www.facebook.com/ohansaga).