import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/drive']

def get_credentials():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
    return creds

def list_file_revisions(service, file_id):
    try:
        revisions = service.revisions().list(fileId=file_id, fields="revisions(id,modifiedTime,lastModifyingUser)").execute()
        return revisions.get('revisions', [])
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def get_file_icon_and_type(mime_type):
    mime_to_icon_and_type = {
        'application/vnd.google-apps.document': ('📝', '[Google Docs]'),
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ('📝', '[Word]'),
        'application/vnd.google-apps.spreadsheet': ('📊', '[Google Sheet]'),
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ('📊', '[Excel]'),
        'text/csv': ('📊', '[CSV]'),
        'application/vnd.google-apps.presentation': ('🖼', '[Google Slides]'),
        'application/vnd.openxmlformats-officedocument.presentationml.presentation': ('🖼', '[PowerPoint]'),
        'application/pdf': ('📄', '[PDF]'),
        'application/vnd.google-apps.form': ('✉', '[Google Form]'),
        'application/vnd.google-apps.drawing': ('🎨', '[Google Drawing]'),
    }
    return mime_to_icon_and_type.get(mime_type, ('❓', ''))

def generate_html_for_folder(service, folder_id='root', is_root=False):
    folder_name = 'ROOT' if is_root else service.files().get(fileId=folder_id).execute().get('name')
    folder_structure = f"<div class='folder'><div class='folder-header' onclick='toggleContent(this)'>📁 {folder_name}</div><div class='folder-content'>"
    
    results = service.files().list(q=f"'{folder_id}' in parents", pageSize=1000, fields="nextPageToken, files(id, name, mimeType)").execute()
    items = results.get('files', [])
    
    root_files = 0
    total_files = 0
    total_folders = 0
    total_revisions = 0

    for item in items:
        if item['mimeType'] != 'application/vnd.google-apps.folder':
            icon, file_type = get_file_icon_and_type(item['mimeType'])
            folder_structure += f"<div class='file'><div class='file-header'>{icon} {item['name']} {file_type}</div>"
            
            revisions = list_file_revisions(service, item['id'])
            for rev in revisions:
                modified_by = rev['lastModifyingUser']['displayName'] if 'lastModifyingUser' in rev else 'Unknown'
                folder_structure += f"<div class='revision'>Revision: {rev['id']} | Timestamp: {rev['modifiedTime']} | Modified by: {modified_by}</div>"
            folder_structure += "</div>"

            total_files += 1
            if is_root:
                root_files += 1
            total_revisions += len(revisions)
        else:
            total_folders += 1
            folder_html, folder_root_files, folder_total_files, folder_folders, folder_revisions = generate_html_for_folder(service, item['id'])
            folder_structure += folder_html
            root_files += folder_root_files
            total_files += folder_total_files
            total_folders += folder_folders
            total_revisions += folder_revisions
            
    folder_structure += "</div></div>"
    return folder_structure, root_files, total_files, total_folders, total_revisions

def main():
    creds = get_credentials()
    service = build('drive', 'v3', credentials=creds)
    
    folder_structure, root_files, total_files, total_folders, total_revisions = generate_html_for_folder(service, is_root=True)

    html_structure = """
    <html>
    <head>
        <title>Google Drive Structure</title>
        <style>
            .folder, .file {
                border: 1px solid black;
                margin: 10px;
                padding: 10px;
            }
            .folder-content, .file-content {
                display: none;
                margin-left: 20px;
            }
            .folder-header, .file-header {
                cursor: pointer;
            }
            .revision {
                margin-left: 10px;
            }
        </style>
        <script>
            function toggleContent(element) {
                let content = element.nextElementSibling;
                if(content.style.display === 'none' || content.style.display === '') {
                    content.style.display = 'block';
                } else {
                    content.style.display = 'none';
                }
            }
        </script>
    </head>
    <body>
    <h1 style='text-align:center'>Google Drive Revisions</h1>
    <h3 style='text-align:center'>- by Tina Vea</h3>
    <hr>
    """
    
    html_structure += f"<div><strong>Root files:</strong> {root_files}</div>"
    html_structure += f"<div><strong>Directories:</strong> {total_folders}</div>"
    html_structure += f"<div><strong>Files:</strong> {total_files}</div>"
    html_structure += f"<div><strong>Revisions:</strong> {total_revisions}</div>"
    html_structure += folder_structure
    html_structure += """
    </body>
    </html>
    """
    
    with open('Drive_Structure.html', 'w', encoding='utf-8') as f:
        f.write(html_structure)

if __name__ == '__main__':
    main()
