import requests

def main(message):
    # Replace with your actual bot token
    TOKEN = "7338138917:AAH1XUdwaeos1bgjdbMaVav6NtY-x41E1c8"
    chat_id = "6000912808"  # Replace with the actual chat ID
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    response = requests.post(
        url, 
        data={
        'chat_id': chat_id,
        'text': message})

    print(response.json())
