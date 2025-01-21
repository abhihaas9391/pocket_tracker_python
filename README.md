# Pocket Tracker (Python Version)

A simple command-line-based expense tracker built with Python. This application allows users to record, manage, and review their expenses using a `.data` file for storage.

## Features
- Add expenses with categories
- View total expenses
- Search expenses by category
- Persistent storage using a `.data` file
- Simple command-line interface

## Installation

1. Clone this repository:
   ```sh
   git clone https://github.com/abhihaas9391/pocket_tracker_python.git
   cd pocket-tracker-python
   ```


## Usage

Run the script:
```sh
python demo.py
```

### Commands
- **Add an expense**: Enter the amount, category, and description.
- **View expenses**: Display all recorded transactions.
- **Search by category**: Filter transactions based on category.
- **Exit**: Save data and close the application.

## Data Storage
All transactions are stored in `expenses.data` in a structured format. The program automatically reads and writes to this file.

## Example
```sh
Welcome to Pocket Tracker!
1. Add Expense
2. View Expenses
3. Search by Category
4. Exit
Enter your choice: 1
Enter amount: 500
Enter category: Food
Enter description: Lunch at cafe
Expense added successfully!
```



