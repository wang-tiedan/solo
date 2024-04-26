## Design
This Django application provides an intuitive platform for users to browse and purchase products with ease. Built on the Bootstrap framework, the design is responsive and ensures a seamless shopping experience across all devices. The application inherits from a base.html template across all pages, promoting consistency and DRY (Don't Repeat Yourself) principles.

## Development
Leveraging Django's MTV (Model-Template-View) architecture, the project includes models representing core entities such as Products, Users, Shopping Carts, and Orders. Views process the business logic, and templates render the data to the end user in a clean and structured format.


## Implementation
The application features pages like product_detail.html for showcasing individual product details and view_cart.html for reviewing items in the shopping cart. Charts and user interaction elements are rendered using JavaScript and AJAX for a dynamic user experience.

## Installation
**To install and deploy**

1. Visit PythonAnywhere and create a new app: https://www.pythonanywhere.com/

2. Follow this deployment guide: https://help.pythonanywhere.com/pages/DeployExistingDjangoProject

3. Project URL:

**Creat the basic**

 ```bash
    pyenv local 3.10.7 # this sets the local version of python to 3.10.7
    python3 -m venv .venv # this creates the virtual environment for you
    source .venv/bin/activate # this activates the virtual environment
    pip install --upgrade pip [ this is optional]  # this installs pip, and upgrades it if required.
```
We will use Django (https://www.djangoproject.com) as our web framework for the application. We install that with

```bash
    pip install Django
```
   

**Project Configuration**
```bash
python manage.py migrate # Migrate databases
python manage.py createsuperuser # Create an admin user
python manage.py createsuperuser # Create an administrative user
```

**Data Import**
1. Place product CSV files in the designated import directory
2. Use the custom management command python manage.py import_products --path [CSV file path]

**Run the server**
```bash
    python manage.py runserver
```
Interact with the application at http://127.0.0.1:8000/product_detail/
Admin Interface: http://127.0.0.1:8000/admin with the superuser account


## Functionality Introduction
This e-commerce application features product listings with advanced filtering options, shopping cart management, order processing, and user authentication. There is also an administrative interface for site management and a CSV import utility for product data.

1. Product Navigation: The homepage showcases product categories and allows users to navigate to different sections, such as "Shopping Cart" or "Login."
2. Product Checkout: Clicking the shopping cart on the product interface will prompt you to log in. After logging in, you can add the shopping cart function to this interface, and click the shopping cart again to proceed with settlement. You can also add or remove items in the shopping cart interface.
3. Login: Administrators and users log in through their corresponding buttons. To log out of the account, click logout on the product interface. If the visitor cannot log in, click the return interface button.
4. Page access rights: After the administrator logs in, he jumps to the modification interface (this interface is associated with the creator-related information interface and the modified management-related information interface). This button will report an error when the user logs in; after the user logs in (the user login button administrator can also log in for settlement) Jump to the shopping cart interface. After settlement, it will show that the payment was successful. If the payment is canceled, it will jump back to the main interface.
5. The product interface has a powerful search function. It can search for the results expected by users through price filtering, keyword search, interval filtering, etc., and has a line chart for visualization.
6. Administrators can view order details after successful payment.
   

## Instruction

For smooth operation:

Start the Server: In the project directory, run python manage.py runserver and visit http://127.0.0.1:8000/product_detail to interact with the platform.
Run Tests: Execute python manage.py test to ensure all components are functioning correctly.
Install Libraries: Dependencies can be installed using pip install -r requirements.txt.
URL Deployment: In settings.py, configure the ALLOWED_HOSTS for production, and set DEBUG to False. Securely manage secrets and passwords using environment variables.

user account
name: u3, u4, u5 ...， u100
password: u12345678

administrator account
name: admin
password: admin123456