# Library Service Project

## Project Description:
There is a library in your city, where you can borrow books and pay for your borrowings using cash, depending on the days you read the book.
The problem is, that the system of tracking books, borrowings, users & payments in the library is outdated - everything is done manually and all tracking is performed on paper. There is no possibility to check the inventory of specific books in the library. Also, you are obliged to pay with cash (no credit card support). Library administration never knows, who returned the book in time, and who did not.

In this project, you will be fixing all these problems. And to do so, you’ll implement an online management system for book borrowings. The system will optimize the work of library administrators and will make the service much more user-friendly.


## Requirements:
### Functional (what the system should do):
<li>Web-based</li>
<li>Manage books inventory</li>
<li>Manage books borrowing</li>
<li>Manage customers</li>
<li>Display notifications</li>
<li>Handle payments</li>

### Non-functional (what the system should deal with):
<li>5 concurrent users</li>
<li>Up to 1000 books</li>
<li>50k borrowings/year</li>
<li>~30MB/year</li>



## Architecture:

![image](https://user-images.githubusercontent.com/72568844/204559703-690630e2-4bc4-4173-bbca-e26c197b3cdc.png)

## Resources:

#### 1. Book:
    Title: str
    Author: str
    Cover: Enum: HARD | SOFT
    Inventory: positive int
    Daily fee: decimal (in $USD)

#### 2. User (Customer):
    Email: str
    First name: str
    Last name: str
    Password: str
    Is staff: str

#### 3. Borrowing:
    Borrow date: date
    Expected return date: date
    Actual return date: date
    Book id: int
    User id: int
#### 4. Payment:
    Status: Enum: PENDING | PAID
    Type: Enum: PAYMENT | FINE
    Borrowing id: int
    Session url: Url  # url to stripe payment session
    Session id: str  # id of stripe payment session
    Money to pay: decimal (in $USD)  # calculated borrowing total price
## Components:
### Books Service:
#### Managing books amount (CRUD for Books)
    API:
    POST:           books/          - add new 
    GET:            books/          - get a list of books
    GET:            books/<id>/     - get book's detail info 
    PUT/PATCH:      books/<id>/     - update book (also manage inventory)
    DELETE:         books/<id>/     - delete book

### Users Service:
#### Managing authentication & user registration
    API:
    POST:           user/                  - register a new user 
    POST:           user/token/            - get JWT tokens 
    POST:           user/token/refresh/    - refresh JWT token 
    GET:            user/me/               - get my profile info 
    PUT/PATCH:      user/me/               - update profile info 

### Borrowings Service:

#### Managing users' borrowings of books
    API:
    POST:    borrowings/                       - add new borrowing (when borrow book - inventory should be made -= 1) 
    GET:     borrowings/?user_id=...&is_active=...  - get borrowings by user id and whether is borrowing still active or not.
    GET:     borrowings/<id>/        - get specific borrowing 
    POST:   borrowings/<id>/return/           - set actual return date (inventory should be made += 1)

### Notifications Service (Telegram):

Notifications about new borrowing created, borrowings overdue & successful payment
Asynchronous (using Django Q package)
Other services interact with it to send notifications to library administrators.
Usage of Telegram API, Telegram Chats & Bots.
### Payments Service (Stripe):

###### Perform payments for book borrowings through the platform.
###### Interact with Stripe API using the stripe package.
    API:
    GET:    success/  - check successful stripe payment
    GET:    cancel/   - return payment paused message 

#### Drf-spectacular docs
    API:
    GET:        doc/swagger/  - Swagger: API Documentation
    GET:        doc/redoc/    - Redoc: API documentation
    
View Service (Delegated to the Front-end Team):
Front-end interface for communication with Library API.
Will not be implemented here
    
