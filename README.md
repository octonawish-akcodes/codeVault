# CodeVault

![Screenshot from 2023-06-04 17-57-22](https://github.com/octonawish-akcodes/codeVault/assets/76171953/dd15d3f4-c9fc-4deb-9ff3-cc5333577bfe)

Introducing CodeVault, a powerful CLI tool for developers to securely store, manage, and execute code snippets. With CodeVault, you can effortlessly create, organize, and execute snippets in various programming languages, all from the command line. The application provides a seamless user experience, allowing you to register and authenticate users, create snippets with titles, descriptions, and code, and execute Python snippets with ease. CodeVault also offers features like profile and portfolio visualization, search functionality, and password reset. Simplify your coding workflow and boost productivity with CodeVault, the ultimate CLI Snippet Manager.

A command-line interface (CLI) application for managing and executing code snippets.

Table of Contents
[Installation](#installation)
[Usage](#usage)
[Authentication](#authentication)
[Profile and Portfolio Visualization](#profile-and-portfolio-visualization)
[Snippet Execution](#snippet-execution)
[Snippet Search](#snippet-search)
[Reset Password](#reset-password)
[Contributing](#contributing)
[License](#license)

1. Installation
     Clone the repository:

     ```git clone https://github.com/octonawish-akcodes/codeVault```
   
2. Change into the project directory:
   
     shell 
     ```cd codeVault```

3. Usage:

     Run the application:
     
     shell 
     ```python main.py```

Follow the on-screen instructions to navigate through the application and perform various actions.

4. Authentication

     Register a new user:

     When prompted, enter a unique username and a password.
     The user will be registered and stored in the users.json file.

     Login with an existing user:

     Enter your username and password when prompted.
     If the credentials are valid, you will be logged in and can proceed with other actions.

5. Profile and Portfolio Visualization

     Visualize your profile:

     Select the option to visualize your profile.
     Your username and other profile details will be displayed in a tabular format.

     Visualize your portfolio:
     Select the option to visualize your portfolio.
     All your snippets, including their titles, programming languages, and descriptions, will be displayed in a tabular          format.

6. Snippet Execution

     Create a new snippet:

     Select the option to create a new snippet.
     Provide a title, description, and programming language for the snippet.
     An editor will open for you to write the code.
     After saving, the snippet will be stored in the snippets.json file and in a separate directory based on the                programming language.

     Execute a snippet:

     Select the option to execute a snippet.
     Choose the snippet you want to execute from the list.
     If the snippet's language is supported (currently only Python), the code will be executed and the result will be            displayed.

7. Snippet Search

     Perform a search:
     Select the option to perform a search.
     Enter a search query with keywords, programming language, or description.
     The matching snippets will be displayed, including their indexes, titles, languages, and descriptions.

8. Reset Password

     Reset your password:
     Select the option to reset your password.
     Enter your username and current password.
     If the credentials are correct, enter and confirm your new password.
     Your password will be updated in the users.json file.

9. Contributing:

     Contributions are welcome! Here's how you can contribute:

     Fork the repository.
     Create a new branch: 
     ```git checkout -b feature/your-feature-name```

     Make your changes and commit them: 
     ```git commit -m 'Add some feature'```

     Push to the branch: ```git push origin feature/your-feature-name```

     Submit a pull request.

License: This project is licensed under the [MIT License](https://opensource.org/license/mit/).
