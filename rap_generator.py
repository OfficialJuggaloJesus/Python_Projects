import requests

word = 'rhyme'
api_url = 'https://api.api-ninjas.com/v1/rhyme?word={}'.format(word)
response = requests.get(api_url, headers={'QEAgxaq3s3rFKhsV7lnDgqOkGujEApBmCCFDi2cI': 'QEAgxaq3s3rFKhsV7lnDgqOkGujEApBmCCFDi2cI'})
if response.status_code == requests.codes.ok:
    print(response.text)
else:
    print("Error:", response.status_code, response.text)