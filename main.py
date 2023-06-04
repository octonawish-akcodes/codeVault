import os
import json
import subprocess
import bcrypt
from tqdm import tqdm
from colorama import init, Fore, Style
import readline
from prettytable import PrettyTable


init()


USERS_FILE_PATH = "users.json"
SNIPPETS_FILE_PATH = "snippets.json"

# Function to register a new user
def register_user():
    username = input("Enter a username: ")
    password = input("Enter a password: ")

    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    # Load existing users
    users = load_users()

    # Check if the username is already taken
    if any(user["username"] == username for user in users):
        print(Fore.RED + "Username already exists." + Style.RESET_ALL)
        return

    # Add the new user
    user = {
        "username": username,
        "password": hashed_password.decode()
    }
    users.append(user)

    # Save the updated users
    save_users(users)

    print(Fore.GREEN + "User registered successfully!" + Style.RESET_ALL)


# Function to load existing users from the file
def load_users():
    users = []

    if os.path.exists(USERS_FILE_PATH):
        with open(USERS_FILE_PATH, "r") as file:
            try:
                users = json.load(file)
            except json.JSONDecodeError:
                print("Error: Invalid JSON format in the users file.")
                return users

    return users

# Function to save users to the file
def save_users(users):
    with open(USERS_FILE_PATH, "w") as file:
        json.dump(users, file, indent=4)

# Function to authenticate a user
def authenticate_user(username, password):
    users = load_users()

    for user in users:
        if user["username"] == username:
            hashed_password = user["password"].encode()
            if bcrypt.checkpw(password.encode(), hashed_password):
                return True

    return False

# User login function
def login():
    username = input(Fore.CYAN + "Enter your username: " + Style.RESET_ALL)
    password = input(Fore.CYAN + "Enter your password: " + Style.RESET_ALL)

    if authenticate_user(username, password):
        print("Login successful!")
        return True
    else:
        print(Fore.RED + "Invalid username or password." + Style.RESET_ALL)
        return False

# Decorator function for user authentication
def require_authentication(func):
    def wrapper():
        if not login():
            return

        func()

    return wrapper

# Function to create a new snippet
@require_authentication
def create_snippet():
    title = input(Fore.CYAN + "Enter the title of the snippet: " + Style.RESET_ALL)
    description = input(Fore.CYAN + "Enter a description for the snippet: " + Style.RESET_ALL)
    language = input(Fore.CYAN + "Enter the programming language of the snippet: " + Style.RESET_ALL)

    # Open system editor for code input
    code = get_code_from_editor()

    snippet = {
        "title": title,
        "description": description,
        "language": language,
        "code": code
    }

    # Load existing snippets
    snippets = load_snippets()

    # Add the new snippet
    snippets.append(snippet)

    # Save the updated snippets
    save_snippets(snippets)

    # Create directory for the programming language
    language_directory = create_language_directory(language)

    # Save code to a file within the language directory
    language_extensions = {
        "python": "py",
    }
    extension = language_extensions.get(language)
    if extension:
        filename = f"{title}.{extension}"
        file_path = os.path.join(language_directory, filename)
        with open(file_path, "w") as file:
            file.write(code)

        # Update the snippet with the file path
        snippet["file_path"] = file_path

        # Save the updated snippets with file paths
        save_snippets(snippets)

    print(Fore.YELLOW + "Snippet created successfully!" + Style.RESET_ALL)


def completer(text, state):
    options = ['register_user', 'login', 'create_snippet', 'execute_snippet', 'exit']
    matches = [opt for opt in options if opt.startswith(text)]
    return matches[state]

readline.set_completer(completer)
readline.parse_and_bind("tab: complete")


# Function to load existing snippets from the file
def load_snippets():
    snippets = []

    if os.path.exists(SNIPPETS_FILE_PATH):
        with open(SNIPPETS_FILE_PATH, "r") as file:
            try:
                snippets = json.load(file)
            except json.JSONDecodeError:
                print("Error: Invalid JSON format in the snippets file.")
                return snippets

    return snippets

# Function to save snippets to the file
def save_snippets(snippets):
    with open(SNIPPETS_FILE_PATH, "w") as file:
        json.dump(snippets, file, indent=4)

def create_language_directory(language):
    directory = f"{language}_snippets"

    if not os.path.exists(directory):
        os.makedirs(directory)

    return directory

# Function to execute a Python code snippet
def execute_snippet(snippet):
    try:
        with tqdm(total=100, desc="Executing snippet") as pbar:
            exec(snippet["code"])
            pbar.update(100)
    except Exception as e:
        print(Fore.RED + "Error executing snippet: {e}" + Style.RESET_ALL)

# Function to open the system editor for code input
def get_code_from_editor():
    editor = os.environ.get("EDITOR") or "nano"  # Use "nano" as the default editor if the environment variable is not set
    temp_file = "temp_code.py"

    # Open the system editor for code input
    subprocess.run([editor, temp_file])

    # Read the code from the temporary file
    with open(temp_file, "r") as file:
        code = file.read()

    # Remove the temporary file
    os.remove(temp_file)

    return code

# Main program
def main():
    register_option = input(Fore.CYAN + "Do you want to register a new user? (yes/no): " + Style.RESET_ALL)
    if register_option.lower() == "yes":
        register_user()

    create_snippet()

    execute_option = input(Fore.CYAN + "Do you want to execute the snippet? (yes/no): " + Style.RESET_ALL)
    if execute_option.lower() == "yes":
        snippets = load_snippets()
        if snippets:
            for i, snippet in enumerate(snippets):
                print(f"{i+1}. {snippet['title']} ({snippet['language']})")

            snippet_index = input(Fore.CYAN + "Enter the index of the snippet to execute: " + Style.RESET_ALL)
            try:
                snippet_index = int(snippet_index)
                if 1 <= snippet_index <= len(snippets):
                    snippet = snippets[snippet_index - 1]
                    if snippet["language"].lower() == "python":
                        execute_snippet(snippet)
                    else:
                        print(Fore.RED + "Code execution is only supported for Python snippets." + Style.RESET_ALL)
                else:
                    print(Fore.RED + "Invalid snippet index." + Style.RESET_ALL)
            except ValueError:
                print(Fore.RED + "Invalid input." + Style.RESET_ALL)
    else:
        print(Fore.YELLOW + "Snippet created successfully!" + Style.RESET_ALL)

    visualize_option = input(Fore.CYAN + "Do you want to visualize your profile and portfolio? (yes/no): " + Style.RESET_ALL)
    if visualize_option.lower() == "yes":
        visualize_profile()
        visualize_portfolio()
        
    search_option = input(Fore.CYAN + "Do you want to perform a search? (yes/no): " + Style.RESET_ALL)
    if search_option.lower() == "yes":
        perform_search()
        
    reset_option = input(Fore.CYAN + "Do you want to reset your password? (yes/no): " + Style.RESET_ALL)
    if reset_option.lower() == "yes":
        reset_password()
        
def perform_search():
    search_query = input(Fore.CYAN + "Enter your search query: " + Style.RESET_ALL)
    snippets = load_snippets()
    if snippets:
        search_results = []
        for snippet in snippets:
            # Check if the search query matches the snippet title, language, or description
            if search_query.lower() in snippet["title"].lower() or search_query.lower() in snippet["language"].lower() or search_query.lower() in snippet["description"].lower():
                search_results.append(snippet)

        if search_results:
            print(Fore.GREEN + "Search Results" + Style.RESET_ALL)
            table_data = []
            for i, snippet in enumerate(search_results):
                table_data.append([i + 1, snippet["title"], snippet["language"], snippet["description"]])
            table = PrettyTable()
            table.field_names = ["Index", "Title", "Language", "Description"]
            table.add_rows(table_data)
            print(table)
        else:
            print(Fore.YELLOW + "No search results found." + Style.RESET_ALL)
    else:
        print(Fore.YELLOW + "No snippets found in the portfolio." + Style.RESET_ALL)

# Function to reset a user's password
def reset_password():
    username = input("Enter your username: ")
    current_password = input("Enter your current password: ")

    # Check if the user exists and authenticate the current password
    users = load_users()
    user_exists = False
    for user in users:
        if user["username"] == username:
            user_exists = True
            hashed_password = user["password"].encode()
            if bcrypt.checkpw(current_password.encode(), hashed_password):
                new_password = input("Enter your new password: ")
                confirm_password = input("Confirm your new password: ")
                if new_password == confirm_password:
                    hashed_password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
                    user["password"] = hashed_password.decode()
                    save_users(users)
                    print(Fore.GREEN + "Password reset successful!" + Style.RESET_ALL)
                else:
                    print(Fore.RED + "New passwords do not match." + Style.RESET_ALL)
            else:
                print(Fore.RED + "Incorrect current password." + Style.RESET_ALL)
    
    if not user_exists:
        print(Fore.RED + "User does not exist." + Style.RESET_ALL)



def visualize_profile():
    print(Fore.GREEN + "Profile Visualization" + Style.RESET_ALL)
    users = load_users()
    if users:
        user = users[-1]  # Assuming the last registered user is the current user
        table = PrettyTable()
        table.field_names = ["Field", "Value"]
        table.add_row(["Username", user["username"]])
        # Add more fields as needed (e.g., name, contact details, bio)
        print(table)
    else:
        print(Fore.YELLOW + "No user profiles found." + Style.RESET_ALL)


def visualize_portfolio():
    print(Fore.GREEN + "Portfolio Visualization" + Style.RESET_ALL)
    snippets = load_snippets()
    if snippets:
        table_data = []
        for i, snippet in enumerate(snippets):
            table_data.append([i + 1, snippet["title"], snippet["language"], snippet["description"]])
        table = PrettyTable()
        table.field_names = ["Index", "Title", "Language", "Description"]
        table.add_rows(table_data)
        print(table)
    else:
        print(Fore.YELLOW + "No snippets found in the portfolio." + Style.RESET_ALL)


if __name__ == "__main__":
    main()
