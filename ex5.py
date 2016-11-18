#!/usr/bin/env python
'''
    This is a demo logon interface
'''

# import some module
import hashlib
import sys
import getpass

# variable define
f_recoder = 'user.txt'


# file check. if recoder file not exist, create it first
try:
    open(f_recoder, 'r').close()
except:
    open(f_recoder, 'w').close()


# base layout
def layout(string, ch='*', length=40):
    '''layout(string[, ch[, length]]) -> None
    simple layout func, center the string only
    '''
    num = (length - len(string)) / 2
    if num <= 0:
        print string
    else:
        print ch * num + string + ch * num


def find_recoder(name):
    '''find_recoder(name) -> (line, pos)
    Return the recoder info
    '''
    fobj = open(f_recoder, 'r')
    pos = 0
    ret = None

    for line in fobj:
        if line[:len(name)] == name:
            ret = (line, pos)
            break
        pos += len(line)

    fobj.close()
    return ret


def parse_line(line, name_len):
    '''parse_line(line, name_len) -> (name, password, '[:-]')
    Parse the recoder line
    '''
    return (line[:name_len], line[name_len + 1:-1], line[name_len])


def get_info(name):
    '''get_info(name) -> (name, password, '[:-]')
    Return None when recoder not found
    '''
    recoder = find_recoder(name)
    if not recoder:
        return None
    return parse_line(recoder[0], len(name))


def append_recoder(line):
    '''append_recoder(line)
    Append one line to the file
    '''
    fobj = open(f_recoder, 'a')
    fobj.write(line)
    fobj.close()


def write_byte(pos, ch):
    '''write_byte(pos, ch)
    Rewite the char at the pos
    '''
    fobj = open(f_recoder, 'r+')
    fobj.seek(pos, 0)
    fobj.write(ch)
    fobj.close()


def modify_info(name):
    '''modify_info(name)
    Modify the user info
    '''
    recoder = find_recoder(name)
    write_byte(recoder[1] + len(name), '-')


def append_info(name, password):
    '''append_info(name, password)
    Appen user info to the user info file
    '''
    append_recoder(name + ':' + md5(password) + '\n')


# register a new user
def register():
    '''register()
    Register a new user
    '''
    layout('Register')

    while True:
        name = raw_input('User name: ')
        if get_info(name):
            print 'User name have been exist...'
        else:
            break

    while True:
        password1 = getpass.getpass('User password: ')
        if len(password1) <= 6:
            print 'Password length must more than 6 char...'
            continue
        password2 = getpass.getpass('Make sure password: ')
        if password1 == password2:
            break
        else:
            print 'Password not same, reinput...'

    append_info(name, password1)
    logon_new(name)


# new user logon interface
def logon_new(name):
    '''logon_new(name)
    New user's logon interface
    '''
    print 'Thank you for register.'
    logon(name)


# user logon interface
def logon(name):
    '''logon(name)
    User logon interface
    '''
    string = 'Hello ' + name
    layout(string)
    print 'Ctrl+C or q to quit'
    while True:
        if raw_input() == 'q':
            sys.exit()


# get md5
def md5(string):
    '''md5(string) -> string
    Return the md5 of the string
    '''
    m = hashlib.md5()
    m.update(string)
    return m.hexdigest()


# authentication user
def auth_user(name, password):
    '''auth_user(name, password) -> int
    Return 0: authentication successful
    Return 1: invalid password
    Return 2: invalid username
    Return 3: acount have been locked
    '''
    ret = 0
    info = get_info(name)
    if info:
        if info[2] == ':':
            if info[1] == md5(password):
                return 0
            else:
                return 1
        else:
            ret = 3
    else:
        ret = 2

    return ret


# lock a user
def lock_user(name):
    '''lock_user(name)
    Lock a user by changing  ':' to '-'
    '''
    modify_info(name)
    return


# main loop
def main():
    '''main loop
    As you see, this is the main function
    '''
    count = 2

    layout('User Logon Interface')
    while True:
        name = raw_input('Enter your name: ')
        password = getpass.getpass('Enter your password: ')

        ret = auth_user(name, password)
        if ret == 0:
            logon(name)
        elif ret == 1:
            count -= 1
            if count < 0:
                print 'Sorry, you have enter error password 3 times...'
                lock_user(name)
                return
            print 'Password error, check and retry...'
        elif ret == 2:
            print '[!] Invalid user name'
            while True:
                string = raw_input('''Do you want get one? (Y/N)''')
                if string in ('Y', 'y', 'yes', 'ye'):
                    register()
                    return
                if string in ('N', 'n', 'No', 'no'):
                    count -= 1
                    if count < 0:
                        return
                    else:
                        break
                else:
                    print '[*] Yes or No please...'
        elif ret == 3:
            print '[*] The acount have been locked...'
            sys.exit()


if __name__ == '__main__':
    main()
