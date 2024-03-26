import psycopg2

# Database connection parameters
host = "pgserver.mau.se"
database = "ao9145"
user = "ao9145"
password = "4wg0nyxw"
port = "5432"  # Default PostgreSQL port

# Establish a connection to the PostgreSQL server
try:
    connection = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password,
        port=port
    )

    # Create a cursor to interact with the database
    cursor = connection.cursor()

    # Commit the changes
    connection.commit()

except psycopg2.Error as e:
    print(f"Error: Unable to connect to the database\n{e}")

def main():
        while True:
            welcome()
            print_menu()
            print("Datan sparas när du trycker på avsluta: 3")
            user_choice = input("Val: ")
            if user_choice == "1":
                log_in()
            elif user_choice == "2":
                register()
            elif user_choice == "3":
                break
            else:
                print("Du valde inte ett giltigt alternativ, försök igen!")

def welcome():
    print("Hej och välkommen till HealHub")
    print("*"*20)
        
def print_menu():
    '''
    Skriver ut meny
    '''
    print("\nMeny")
    print("****")
    print("1) Logga In")
    print("2) Registrera")
    print("3) Avsluta programmet")

def log_in():
    '''funktionen som gör det möjligt för kunden att logga in med sin email'''
    global user_id  # Declare user_id as a global variable
    while True:
        email = input("Enter your email: ")
        cursor.execute("SELECT user_id FROM healhub.users WHERE email = %s;", (email,))
        user = cursor.fetchone()
        if user:
            user_id = user[0]  # Set user_id after successful login
            print("Login successful!")
            break
        else:
            print("Incorrect email. Please try again.")
def register():
    '''Funktionen som gör det möjligt för customers att registrera sig'''
    try:
        name = input("Namn: ")
        lastname = input("Efternamn: ")
        email = input("Email: ")
        adress = input("Adress: ")
        phonenumber = int(input("Telefonnummer: "))

        cursor.execute("INSERT INTO healhub.users (f_name, l_name, email, adress, t_number) VALUES (%s, %s, %s, %s, %s);",
                       (name, lastname, email, adress, phonenumber))
        print("Resultat tillagt!")
        connection.commit()
    
    except (psycopg2.Error, ValueError) as e:
        print(f"Något gick fel: {e}")
if __name__ == "__main__":
    main()