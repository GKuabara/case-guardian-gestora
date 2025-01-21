# case-guardian-gestora
Case for open role of backend developer in Guardian Gestora company.

This project is a Django-based REST API for managing personal credit contracts and their parcels. It includes features for creating contracts, retrieving contract details, and summarizing contract data.

## Features
- Create contracts with optional parcel data.
- List contracts with filtering options (e.g., by contract ID, document number, issue_date, and state).
- Summarize contract data, including the total amount receivable, disbursed, number of contracts, and average contract rate.

## Instructions

### Installation

Follow the steps below to set up and run the project:

1. Clone repository or just download the folder

```bash
git clone https://github.com/GKuabara/case-guardian-gestora.git
cd case-guardian-gestora
```

2. Set Up a Virtual Environment
Install a Python virtual environment to isolate project dependencies:

```bash
python -m venv venv
source venv/bin/activate  # For Linux/Mac
venv\Scripts\activate     # For Windows
```

3. Install Dependencies
Install all required Python packages from the requirements.txt file:

```bash
pip install -r requirements.txt
```

4. Apply Database Migrations
Set up the database:

```bash
python manage.py migrate
```

5. Run the Server
Start the development server:

```bash
python manage.py runserver
```

Now you can use the API in (http://127.0.0.1:8000/) by making simple requests using your browser, code or any tool like Postman.

### API Endpoints
1. Create Contract
Method: POST
Endpoint: contracts/api/contracts/create/
Body Example:
```json
{
    "issue_date": "2025-01-01",
    "birth_date": "1990-05-15",
    "amount": 10000.00,
    "document_number": "12345678901",
    "country": "Brazil",
    "state": "SP",
    "city": "São Paulo",
    "phone_number": "123456789",
    "contract_rate": 3.5,
    "parcels": [
        {"parcel_number": 1, "parcel_amount": 2500.00, "due_date": "2025-02-01"},
        {"parcel_number": 2, "parcel_amount": 2500.00, "due_date": "2025-03-01"}
    ]
}
```

2. List Contracts
Method: GET\
Endpoint: contracts/api/contracts/list/\
Query Parameters:\
contract_id\
document_number\
issue_date\
state

3. Contract Summary
Method: GET\
Endpoint: contracts/api/contracts/summary/\
Query Parameters:\
contract_id\
document_number\
issue_date\
state


## Testing
This project includes a comprehensive suite of tests for views, filters, and data validation.

### Run All Tests
Run the tests using Django's test runner:

```bash
python manage.py test
```

### Expected Output
If all tests pass, you'll see something like:
```bash
Found 10 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
..........
----------------------------------------------------------------------
Ran 10 tests in 0.051s

OK
Destroying test database for alias 'default'...
```

### Customize Test Data
Tests are set up using Django's TestCase class and include setUp methods to generate test data. If you'd like to add or modify tests, edit the tests directory in the project.

## Contact
For questions or feedback, contact:

Email: gabrielalveskuabara@gmail.com\
LinkedIn: [LinkedIn Profile](https://www.linkedin.com/in/gkuabara/)