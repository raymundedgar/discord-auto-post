# -*- coding: utf-8 -*-

import threading as th
from cConnection import Connection
import os
import colorama
from colorama import Fore, Style, init
import random

init()

print(Fore.CYAN + """
░█████╗░██╗░░░██╗████████╗░█████╗░░██████╗░███╗░░░███╗
██╔══██╗██║░░░██║╚══██╔══╝██╔══██╗██╔════╝░████╗░████║
███████║██║░░░██║░░░██║░░░██║░░██║██║░░██╗░██╔████╔██║
██╔══██║██║░░░██║░░░██║░░░██║░░██║██║░░╚██╗██║╚██╔╝██║
██║░░██║╚██████╔╝░░░██║░░░╚█████╔╝╚██████╔╝██║░╚═╝░██║ By
╚═╝░░╚═╝░╚═════╝░░░░╚═╝░░░░╚════╝░░╚═════╝░╚═╝░░░░░╚═╝   [G7]AzaZlo""")
print(Style.RESET_ALL)
all_threads = {}


def get_all_threads_key():
    for key in all_threads.keys():
        print(key)


all_thread_names = []


def new_thread():
    global all_thread_names
    file_token = open('token.txt', 'r', encoding='utf-8')
    list_token = [line.strip() for line in file_token]
    token = list_token[0]
    channelid = input(
        "[X] Insert the channel ID where messages will be sent (the user must be on the server)\n >> ")
    message = input("[X] Enter the message to be sent in the chat\n >> ")
    timer = input("[X] Enter the sending interval in seconds\n >> ")
    name = input("[X] Enter a unique name for the process\n >> ")
    if name in all_thread_names:
        print(Fore.RED + '\nERROR: A process with this name already exists, please enter a different name')
        print(Style.RESET_ALL)
    else:
        new_con = Connection(token, channelid, message, timer, name)
        new_con.send_message()
        all_threads[new_con.name] = new_con
        all_thread_names.append(new_con.name)
        print(Fore.GREEN + 'Process started!\n')
        print(Style.RESET_ALL)


def table_thread():
    global all_thread_names
    file_token = open('token.txt', 'r', encoding='utf-8')
    list_token = [line.strip() for line in file_token]
    file_channel = open('channel.txt', 'r', encoding='utf-8')
    list_channel = [line.strip() for line in file_channel]
    message = input('Enter the message to be sent\n >> ')
    timer = input("[X] Enter the sending interval in seconds\n >> ")
    for token in list_token:
        for channelid in list_channel:
            name = f'{token}_{channelid}'
            if name in all_thread_names:
                print(Fore.RED + '\nERROR: A process with this name already exists')
                print(Style.RESET_ALL)
            else:
                new_con = Connection(token, channelid, message, timer, name)
                new_con.send_message()
                all_threads[new_con.name] = new_con
                all_thread_names.append(new_con.name)
                print(Fore.GREEN + 'Process started!\n')
                print(Style.RESET_ALL)


def random_message(choise):
    global all_thread_names
    token = input("[X] Insert the token of the user from which the sending will be performed\n >> ")
    channelid = input(
        "[X] Insert the channel ID where messages will be sent (the user must be on the server)\n >> ")
    timer = input("[X] Enter the sending interval in seconds\n >> ")
    name = input("[X] Enter a unique name for the process\n >> ")
    if name in all_thread_names:
        print(Fore.RED + '\nERROR: A process with this name already exists, please enter a different name')
        print(Style.RESET_ALL)
    else:
        message = None
        new_con = Connection(token, channelid, message, timer, name, random=choise)
        new_con.send_message()
        all_threads[new_con.name] = new_con
        all_thread_names.append(new_con.name)
        print(Fore.GREEN + 'Process started!\n')
        print(Style.RESET_ALL)


def main():
    global all_thread_names
    while True:
        print(
            '1) Create a new process\n2) Delete a process\n3) View process log\n4) List all processes\n5) Token x Channel ID batch process\n6) Send random messages\nq) Exit\n')
        switch = input(' >> ')
        if switch == '1':
            new_thread()
        elif switch == '2':
            name_thread = input("Enter the process name:\n >> ")
            try:
                all_threads[name_thread].stop_thread()
                del all_threads[name_thread]
                all_thread_names.remove(name_thread)
                print(Fore.GREEN + 'Process successfully deleted\n')
                print(Style.RESET_ALL)
            except KeyError:
                print(Fore.RED + '\nERROR: No such process exists')
                print(Style.RESET_ALL)
        elif switch == '3':
            name_thread = input("Enter the process name:\n >> ")
            try:
                logs = all_threads[name_thread].get_log()
                print(Fore.YELLOW + f"Logs for process {name_thread}:\n---------------------")
                print('\n'.join(logs))
                print('---------------------')
                print(Style.RESET_ALL)
            except KeyError:
                print(Fore.RED + '\nERROR: No such process exists')
                print(Style.RESET_ALL)
        elif switch == '4':
            print('All processes:\n---------------------')
            get_all_threads_key()
            print('---------------------')
        elif switch == '5':
            print('Batch process creation for multiple accounts and channels')
            print('In the file token.txt, specify the tokens for all accounts, one per line')
            print('In the file channel.txt, specify the IDs of all channels, one per line')
            if input("Type 'start' to begin once files are ready\n >> ").lower() == 'start':
                table_thread()
            else:
                print(Fore.RED + '\nERROR: Invalid command, please check your input')
                print(Style.RESET_ALL)
        elif switch == '6':
            print('Random message sending mode')
            print('Write the list of messages to message.txt, one per line')
            print(Fore.YELLOW + 'WARNING: Sending messages too frequently might result in a ban')
            print(Style.RESET_ALL)
            print('1) Use basic randomization\n2) Use smart randomization (no repeated messages until all are sent)')
            choice = input("\n >> ")
            if choice == '1':
                random_message(choise=1)
            elif choice == '2':
                random_message(choise=2)
            else:
                print(Fore.RED + '\nERROR: Invalid choice, please check your input')
                print(Style.RESET_ALL)
        elif switch == 'q':
            os.abort()
        else:
            print(Fore.RED + '\nERROR: Invalid action number\n')
            print(Style.RESET_ALL)


main()
