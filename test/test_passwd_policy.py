#!/usr/bin/env python
import boto3
#import moto
#from moto import mock_iam
import yaml
import time
import io
import csv
from datetime import datetime, timedelta

def yamlfmt(obj):
    """Convert a dictionary object into a yaml formated string"""
    if isinstance(obj, str):
        return obj
    return yaml.dump(obj, default_flow_style=False)


def get_passwd_policy():
    client = boto3.client('iam')
    try:
        return client.get_account_password_policy()['PasswordPolicy']
    except client.exceptions.NoSuchEntityException:
        return "password policy not implemented"

def set_passwd_policy():
    client = boto3.client('iam')
    client.update_account_password_policy(
        MinimumPasswordLength=8,
        RequireSymbols=True,
        RequireNumbers=True,
        RequireUppercaseCharacters=True,
        RequireLowercaseCharacters=True,
        AllowUsersToChangePassword=True,
        MaxPasswordAge=180,
        PasswordReusePrevention=6,
        #HardExpiry=True|False
    )
    return

def delete_passwd_policy():
    client = boto3.client('iam')
    client.delete_account_password_policy()
    return 



def iam_credentials_report():
    """
    IAM Credential report in an account
    Returns list of per-user credential info dictionaries
    """
    client = boto3.client('iam')
    try:
        response = client.get_credential_report()
    except client.exceptions.CredentialReportNotPresentException as e:
        client.generate_credential_report()
        time.sleep(60)
        response = client.get_credential_report()

    report_file_object = io.StringIO(response['Content'].decode())
    reader = csv.DictReader(report_file_object)
    user_info = []
    for row in reader:
        user = dict()
        for key in reader.fieldnames:
            user[key] = row[key]
        user_info.append(user)
    return user_info


def list_users_with_aged_out_passwords(credentials_report, age_in_days):
    aged_out_users = []
    now = datetime.utcnow()
    datetime_pattern = "%Y-%m-%dT%H:%M:%S"
    password_last_changed_map = {
        x['user']: x['password_last_changed'] for x in credentials_report
    }
    for user_name, last_change in password_last_changed_map.items():
        # strip off tz suffix:
        # '2017-11-17T00:50:20+00:00' => '2017-11-17T00:50:20'
        last_change = last_change.partition('+')[0]
        try:
            then = datetime.strptime(last_change, datetime_pattern)
            if now - then > timedelta(days=age_in_days):
                aged_out_users.append(user_name)
        except ValueError:
            pass
    return aged_out_users

def list_users_who_never_changed_their_password(credentials_report):
    return [x['user'] for x in credentials_report if x['password_last_changed'] == 'N/A']

def list_users_with_no_mfa_device(credentials_report):
    return [x['user'] for x in credentials_report if x['mfa_active'] == 'false']





######### Tests ##########

#@mock_iam
#def test_get_passwd_policy():
#    response = get_passwd_policy()
#    print(yamlfmt(response))
#    assert False


if __name__ == '__main__':
    #response = set_passwd_policy()
    #response = get_passwd_policy()
    #print(yamlfmt(response))
    #response = delete_passwd_policy()
    #response = get_passwd_policy()
    #print(yamlfmt(response))

    credentials_report = iam_credentials_report()
    #print(yamlfmt(credentials_report))
    response = list_users_with_aged_out_passwords(credentials_report, 180)
    print(yamlfmt(response))
    response = list_users_who_never_changed_their_password(credentials_report)
    print(yamlfmt(response))
    response = list_users_with_no_mfa_device(credentials_report)
    print(yamlfmt(response))
    
