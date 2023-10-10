# GD_Revisions_HTML


![GD Rvisions HTML](https://media.makeameme.org/created/revisions-revisions-everywhere.jpg)

- Usage:

<font size=2>**Step 1:</font> 
Create a New Project in Google Developers Console
Go to Google Developers Console.
Click on the "Select a project" dropdown, then click on the "New Project" button.
Enter a name for your project and select a billing account (if you have one).
Click on the "Create" button.

Step 2: Enable Google Drive API
In your new project, navigate to the "Dashboard" on the left-hand side.
Click on the "+ ENABLE APIS AND SERVICES" button.
In the search bar, type "Google Drive" and select "Google Drive API".
Click the "Enable" button on the next page.

Step 3: Create OAuth 2.0 Credentials
Click on "Create credentials" and select "OAuth client ID".
Select "Desktop app" for the application type and enter a name for your OAuth client ID.
Click on "Create".
Click on the download icon (down arrow) next to your new credentials and save the file as "credentials.json".

Step 4: Install Required Python Packages
Open a terminal and navigate to the directory where you saved your "credentials.json" file.
Run the following commands to install the necessary packages:
pip install flask pandas google-api-python-client google-auth google-auth-oauthlib google-auth-httplib2 oauth2client

Step 5: Run the Python Script
In your terminal, navigate to the directory containing your "credentials.json" and "GDriveRevisions_html.py" files.
Run the script with the command: python GDriveRevisions_html
You will be prompted to authorize access your Google Drive. Follow the steps to grant permission.

Step 6: View the Generated HTML Page
After you've authorized access, the HTML will be generated as Drive_Structure.html in the same directory.
NB! If html is not created, after granting access terminate the script and restart. This should create the html in current directory.

