import datetime, random, time, os, sys, json
from finalIndexing import *
from helper import Helper
from subprocess import Popen, PIPE

helper = Helper('I am the Ironman..!!')

GLOBALS = {
    'FORCE_PUSH': True,
    'DEFAULT_DAYS_INCREMENT': 7,
    'WRITER_FILE': 'writer.sh',
}

class User:
    def __init__(self):
        config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
        
        self._userName = config.get('GITHUB_USERNAME', 't1noo7')
        self._emailId = config.get('GITHUB_EMAIL', '2121030019@student.humg.edu.vn')
        self._profileName = config.get('GITHUB_PROFILENAME', 't1l0o_ch0co')

        print(f"Using GitHub username: {self._userName}")
        print(f"Using email ID: {self._emailId}")
        print(f"Using profile name: {self._profileName}")

        #self.__set_username__()
        #self.__set_emailid__()
        #self.__set_profile_name__()

    def getUserInfo(self, configInfo):
        command = 'git config {0} user.{1}'
        configLocations = ['--global', '--local', '--system']

        for location in configLocations:
            userConfig = command.format(location, configInfo)
            output = helper.getCommandOutput(userConfig)
            if len(output):
                return output.strip()
        return ''

    def __set_username__(self):
        print('Enter your github username: ', end='')

        info = self.getUserInfo('name')
        if len(info):
            self._userName = info
            print(f'\n<default: {info}>: ', end='')

        info = input()
        if len(info.strip()):
            self._userName = info

    def __set_emailid__(self):
        print('Enter your registered github emailId: ', end='')

        info = self.getUserInfo('email')
        if len(info):
            self._emailId = info
            print(f'\n<default: {info}>: ', end='')

        info = input()
        if len(info):
            self._emailId = info

    def __set_profile_name__(self):
        print('Enter the name that you want to write on your profile: ', end='')

        info = input()
        if len(info):
            self._profileName = info
        else:
            print('<InvalidName Error>')
            self.__set_profile_name__()

user = User()

class Date:
    def __init__(self):
        self.setDefaultDate()
        print('\nEnter the Base Date in the format (YY-MM-DD).')
        print('<(For more details or to know how to find Base Date, refer README.md)>')
        self.setBaseDate()

    def setDefaultDate(self):
        self.now = datetime.datetime.now()
        self.oldDate = self.now - datetime.timedelta(days=365-3*7)
        diffSunday = 6 - self.oldDate.weekday()
        self.defaultDate = self.oldDate + datetime.timedelta(days=diffSunday-1)
        self.year = self.defaultDate.year
        self.month = self.defaultDate.month
        self.day = self.defaultDate.day

    def setBaseDate(self):
        base_date_str = os.getenv('BASE_DATE', self.defaultDate.strftime('%Y-%m-%d'))
        print(f'\n<default: {self.defaultDate.strftime("%Y-%m-%d")}>: {base_date_str}')

        try:
            info = base_date_str.split('-')
            self.year = int(info[0])
            self.month = int(info[1])
            self.day = int(info[2])
            datetime.datetime(year=self.year, month=self.month, day=self.day)
        except Exception:
            print('Please enter a valid Base Date (leave blank for using Default Date)')
            self.setBaseDate()

    def getBaseDate(self):
        return {
            'year': self.year,
            'month': self.month,
            'day': self.day
        }

date = Date()
base_date = date.getBaseDate()

INFO = {
    'userName': user._userName,
    'emailId': user._emailId,
    'profileName': user._profileName,
    'no_of_commits': 5,
}

allowedChars = [' ']

commits_per_day = 5
info = input('Number of commits per day:\n<default: 5>: ')
if len(info):
    try:
        info = int(info)
        INFO['no_of_commits'] = info
    except Exception:
        pass

startingDate = datetime.datetime(base_date['year'], base_date['month'], base_date['day'])

for alphabet in INFO['profileName']:
    time.sleep(0.1)

    if (not alphabet.isalnum()) and (alphabet not in allowedChars):
        print(f'The character {str(alphabet)} is not yet released')
    elif alphabet != ' ':
        myArray = eval('arr' + alphabet.upper())
        increment = eval('increment' + alphabet.upper())

        print(alphabet, end='')
        sys.stdout.flush()

        for i in myArray:
            components = [None] * 3
            components[0] = 'echo ' + str(random.random()) + str(random.random()) + ' > testFile'
            components[1] = 'git add .'
            components[2] = f'git commit -m "blah blah" --amend --author="{INFO["userName"]} <{INFO["emailId"]}> " --date="{(startingDate + datetime.timedelta(days=i)).strftime("%A %B %d %Y")}"'
            finalCommand = ';'.join(components)

            if GLOBALS['FORCE_PUSH']:
                finalCommand += '; git push origin master --force'

            with open(GLOBALS['WRITER_FILE'], 'a') as f:
                f.write(f'for i in `seq 1 {INFO["no_of_commits"]}`;do {finalCommand}; done\n')
        startingDate += datetime.timedelta(days=increment * GLOBALS['DEFAULT_DAYS_INCREMENT'])
    else:
        print(' ', end='')
        startingDate += datetime.timedelta(days=GLOBALS['DEFAULT_DAYS_INCREMENT'])

print(f'\nNow go and execute the file {GLOBALS["WRITER_FILE"]} in your repository\nHave Fun :D')
