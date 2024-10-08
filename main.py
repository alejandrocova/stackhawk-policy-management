#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
StackHawk Policy Management
Author: Alejandro Flores Covarrubias
Date: 2024-10-07
Description: StackHawk Policy Management is a small project that will help you manage scan policies for your applications in StackHawk using their API.
"""

import sys
import os
import logging
from argparse import ArgumentParser
from dotenv import load_dotenv
import requests
import json

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: [+] %(message)s')
logger = logging.getLogger(__name__)

def parse_arguments():
    """
    Parse command-line arguments
    """
    parser = ArgumentParser(description="A boilerplate Python script.")
    parser.add_argument('-v', '--verbose', action='store_true', help="Increase output verbosity")
    parser.add_argument('--input', type=str, required=True, help="Input file path")
    parser.add_argument('--output', type=str, required=False, help="Output file path")

    return parser.parse_args()

def load_json(file_path, message):
    logging.info(message)
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except json.JSONDecodeError:
        print(f"Error: The file '{file_path}' contains invalid JSON.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def login(key: str):
    logging.info("Authenticating into StackHawk...")
    url_login = "https://api.stackhawk.com/api/v1/auth/login"
    headers_login = {
        "accept": "application/json",
        "X-ApiKey": key
    }
    try:
        response = requests.get(url=url_login, headers=headers_login)
        response.raise_for_status()
        token = json.loads(response.text)['token']
        return token
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
        return None
    except requests.exceptions.ConnectionError as conn_err:
        logger.error(f"Connection error occurred: {conn_err}")
        return None
    except requests.exceptions.Timeout as timeout_err:
        logger.error(f"Timeout error occurred: {timeout_err}")
        return None
    except requests.exceptions.RequestException as req_err:
        logger.error(f"An error occurred: {req_err}")
        return None

def get_scan_policies():
    logging.info("Retrieving all StackHawk policies...")
    url_all_policies = "https://api.stackhawk.com/api/v1/policy/all"
    headers_all_policies = {
        "accept": "application/json",
        "authorization": f"Bearer {bearer_token}"
    }
    try:
        response = requests.get(url=url_all_policies, headers=headers_all_policies)
        response.raise_for_status()
        all_policies = json.loads(response.text)
        return all_policies
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
        return None
    except requests.exceptions.ConnectionError as conn_err:
        logger.error(f"Connection error occurred: {conn_err}")
        return None
    except requests.exceptions.Timeout as timeout_err:
        logger.error(f"Timeout error occurred: {timeout_err}")
        return None
    except requests.exceptions.RequestException as req_err:
        logger.error(f"An error occurred: {req_err}")
        return None
 
def get_all_org_apps():
    logging.info("Retrieving organization applications list...")
    list_of_apps = []
    url_list_apps = f"https://api.stackhawk.com/api/v1/app/{org_id}/list"
    headers_list = {
        "accept": "application/json",
        "authorization": f"Bearer {bearer_token}"
    }
    page_token_counter = 0
    page_token_total = int(json.loads(requests.get(url_list_apps, headers=headers_list).text)['totalCount'])
    #Persistent session to make requests faster
    s = requests.Session()

    while page_token_counter <= page_token_total:
        try: 
            if page_token_counter < 1:
                url = f"https://api.stackhawk.com/api/v1/app/{org_id}/list"
                response = s.get(url, headers=headers_list)
                response.raise_for_status()
                applications = json.loads(response.text)
            else:
                url = f"https://api.stackhawk.com/api/v1/app/{org_id}/list?pageToken={page_token_counter}"
                response = s.get(url, headers=headers_list)
                response.raise_for_status()
                applications = json.loads(response.text)

            page_token_counter = int(applications['nextPageToken'])

            for app in applications['applications']:
                list_of_apps.append(app)
            
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error occurred: {http_err}")
            return None
        except requests.exceptions.ConnectionError as conn_err:
            logger.error(f"Connection error occurred: {conn_err}")
            return None
        except requests.exceptions.Timeout as timeout_err:
            logger.error(f"Timeout error occurred: {timeout_err}")
            return None
        except requests.exceptions.RequestException as req_err:
            logger.error(f"An error occurred: {req_err}")
            return None
        
    return list_of_apps


def invalid_option():
    """
    Function for invalid option
    """
    logger.error("Invalid option selected")


def exit_program():
    """
    Function to exit the program
    """
    logger.info("Exiting program")
    sys.exit(0)


def list_all_apps():
    """
    Function for list apps in StackHawk Organization
    """
    for app in org_apps:
        print(f"[+] {app['name']}: {app['applicationId']}")


def assign_single_application(assignment_type: str):
    print(assignment_type)


def assign_multiple_applications(assignment_type: str):
    print(assignment_type)


def pattern_based_assignment(assignment_type: str):
    print(assignment_type)


def assign_built_in_policy_menu():
    """
    Function for assigning built in policy
    """
    print("\n====== Built-in Policy Assign Application Menu ======")
    print("1. Assign to a single applications")
    print("2. Assign to multiple applications")
    print("3. Assign to application based on patterns")
    print("4. Back")
    print("=======================")

def assign_built_in_policy():
    menu = True
    while menu:
        assign_built_in_policy_menu()
        choice_built_in = input("Enter your choice: ").strip()

        if choice_built_in == '1':
            result = assign_single_application(assignment_type="built-in")
        elif choice_built_in == '2':
            result = assign_multiple_applications(assignment_type="built-in")
        elif choice_built_in == '3':
            result = pattern_based_assignment(assignment_type="built-in")
        elif choice_built_in == '4':
            menu = False
        else:
            continue

def display_menu():
    """
    Function to display the menu options
    """
    print("\n====== Main Menu ======")
    print("1. List all applications in StackHawk organization")
    print("2. Assign Built-In Policy")
    print("3. Exit")
    print("=======================")

def menu_choice(choice):
    """
    Function to call the appropriate function based on the menu choice
    """
    options = {
        '1': list_all_apps,
        '2': assign_built_in_policy,
        '3': exit_program
    }
    return options.get(choice, invalid_option)

def main():
    """
    Main function that contains the program's logic
    """
    while True:
        display_menu()
        choice = input("Enter your choice: ").strip()
        # Execute the corresponding function
        menu_choice(choice)()
        

if __name__ == "__main__":
    global default_policies_names, bearer_token, all_policies, all_plugins, custom_policies, org_apps, org_id
    load_dotenv()
    try:
        stackhawk_api_key = os.getenv("STACKHAWK_API_KEY")
        org_id = os.getenv("ORG_ID")
    except KeyError:
        # Handle the case where the environment variable is not found
        logging.error(f"Environment variables are incorrectly set.")
        sys.exit(1)
    except Exception as e:
        # Handle any other unexpected errors
        logging.error(f"An unexpected error occurred: {e}")
        sys.exit(1)
    
    #args = parse_arguments()
    bearer_token = login(key=stackhawk_api_key)
    if bearer_token:
        all_policies = get_scan_policies()
        if all_policies:
            default_policies_names = [policy['name'] for policy in all_policies['scanPolicies']]
            all_plugins_path,custom_policies_path = 'plugins.json','custom.json'
            all_plugins = load_json(all_plugins_path, "Loading plugins file...")
            custom_policies = load_json(custom_policies_path, "Loading custom policies..." )
            org_apps = get_all_org_apps()
            main()
        else:
            logging.error("There is an error with your script configuration")
            sys.exit(1)
    else:
        logging.error("There is an error with your script configuration")
        sys.exit(1)