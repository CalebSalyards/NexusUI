import json
from proxmoxer import ProxmoxAPI

# Function to connect to Proxmox API
def connect_to_proxmox(host, user, password, verify_ssl=False):
    return ProxmoxAPI(host, user=user, password=password, verify_ssl=verify_ssl)

# Function to create a user in Proxmox
def create_proxmox_user(proxmox, username, password, email):
    proxmox.access.users.create(
        userid=username,
        password=password,
        email=email,
        enable=True
    )

# Function to set user permissions (ACL)
def set_user_permissions(proxmox, username, path, role):
    proxmox.access.acl.create(
        path=path,
        roles=role,
        users=username
    )

# Example usage
def main():
    # Configuration
    proxmox_host = 'proxmox.example.com'
    admin_user = 'root@pam'
    admin_password = 'your_admin_password'
    verify_ssl = False  # Set to True if using a valid SSL certificate

    # Connect to Proxmox
    proxmox = connect_to_proxmox(proxmox_host, admin_user, admin_password, verify_ssl)

    # JSON data received from the HTML site
    json_data = '''
    {
        "users": [
            {
                "username": "johndoe@pve",
                "password": "securepassword123",
                "email": "johndoe@example.com",
                "resources": [
                    {
                        "path": "/vms/100",
                        "role": "PVEAdmin"
                    }
                ]
            }
        ]
    }
    '''

    # Parse JSON
    data = json.loads(json_data)
    
    # Configure users
    for user in data['users']:
        # Create user
        create_proxmox_user(proxmox, user['username'], user['password'], user['email'])

        # Set permissions for the resources
        for resource in user['resources']:
            set_user_permissions(proxmox, user['username'], resource['path'], resource['role'])

if __name__ == '__main__':
    main()
