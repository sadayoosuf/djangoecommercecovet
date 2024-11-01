
# covet

Covet is an e-commerce website built with Python and Django. It offers a seamless shopping experience, featuring a secure user authentication system, a comprehensive product catalog, and efficient order management. Designed for both buyers and sellers, Covet provides a modern, user-friendly marketplace for convenient online shopping.




## How to run locally

1.Clone the Repository:

```bash
 git clone https://github.com/sadayoosuf/djangoecommercecovet.git
 cd djangoecommercecovet
```
2.Create and Activate a Virtual Environment:
```bash
 python -m venv venv
 source venv/bin/activate  # On macOS/Linux
 venv\Scripts\activate     # On Windows
```
3.Install Dependencies:
```bash
pip install -r requirements.txt
```
  + For Payment Integration: Install Razorpay
  ```bash
pip install razorpay
```
 + For Image Handling: Install Pillow
  ```bash
pip install pillow
```
4.Set Up the Database:
```bash
python manage.py makemigrations
python manage.py migrate
```
5.Create a Superuser:
```bash
python manage.py createsuperuser
```
6.Run the Development Server:
```bash
python manage.py runserver
```
+ Visit http://127.0.0.1:8000 in your browser to see the website.
7.Access the Admin Panel:
+ Go to http://127.0.0.1:8000/admin and log in using the superuser credentials you created.

With these steps, you should be able to set up and run your Covet e-commerce website smoothly.

## Demo
### Registration and Login


  


    
