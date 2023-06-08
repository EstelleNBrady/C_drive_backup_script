import os
import shutil
import logging
import subprocess
from concurrent.futures import ThreadPoolExecutor

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def backup_user_profile(username, backup_location):
    user_directory = f'C:\\Users\\{username}'
    destination_path = os.path.join(backup_location, username)

    try:
        # Using robocopy for faster copying and telling it not to retry on failures
        # Exclude directories that usually contain software and application data
        subprocess.run(['robocopy', user_directory, destination_path, '/E', '/XF', 'Downloads', '/R:0', '/W:0', '/XD', 'AppData', 'Program Files*', 'Windows'])
        logging.info(f"Backup of {username}'s profile has been completed.")
    except PermissionError:
        logging.error(f"Permission denied while backing up {username}'s profile. Skipping.")
    except Exception as e:
        logging.error(f"Error backing up {username}'s profile: {e}")


def select_users():
    users_directory = 'C:\\Users'
    users = [name for name in os.listdir(users_directory) if os.path.isdir(os.path.join(users_directory, name))]
    logging.info("Select users to back up (separate user numbers by commas):")
    for i, user in enumerate(users):
        logging.info(f"{i + 1}. {user}")
    selection = input("Enter the numbers corresponding to the users: ")
    selected_users = []
    for number in selection.split(','):
        if number.strip().isdigit() and 1 <= int(number) <= len(users):
            selected_users.append(users[int(number.strip()) - 1])
        else:
            logging.warning(f"Invalid selection for user number {number}. Skipping.")
    return selected_users


def main():
    backup_location = os.environ.get('BACKUP_LOCATION', 'C:\\Temp\\username_backup')

    if not os.path.exists(backup_location):
        os.makedirs(backup_location)

    selected_users = select_users()

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(backup_user_profile, user, backup_location) for user in selected_users]

        for future in futures:
            future.result()

    logging.info("All backups have been completed.")


if __name__ == '__main__':
    main()
