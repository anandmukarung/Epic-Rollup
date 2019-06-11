# ****
# CT_Atlassian_Tools.py - This is a package of useful methods for connecting to JIRA and gathering/manipulating data.
# Every time this package is compiled, drop the new version in site-packages. On this system, that is located at:
#
# C:\Users\spease\AppData\Local\Programs\Python\Python37\Lib\site-packages
#
# ****

import json
import sys
import re
import requests
from jira import JIRA


II = {"Project Key": "II",
      "Project Name": "IT Infrastructure",
      "Project ID": 11200,
      "Board Name": "IT Infrastructure Board",
      "Board ID": 134,
      "Sprints": [{"Sprint Name": "IT 19A", "Sprint ID": 637},
                  {"Sprint Name": "IT 19B", "Sprint ID": 645},
                  {"Sprint Name": "IT 19C", "Sprint ID": 650},
                  {"Sprint Name": "IT 19D", "Sprint ID": 661},
                  {"Sprint Name": "IT 19F", "Sprint ID": 676}]
      }

JAN = {"Project Key": "JAN",
       "Project Name": "Janus",
       "Project ID": 11101,
       "Board Name": "Janus Scrum Board",
       "Board ID": 133,
       "Sprints": [{"Sprint Name": "Janus Sprint 19A", "Sprint ID": 631},
                   {"Sprint Name": "Janus Sprint 19B", "Sprint ID": 646},
                   {"Sprint Name": "Janus Sprint 19C", "Sprint ID": 652},
                   {"Sprint Name": "Janus Sprint 19D", "Sprint ID": 658},
                   {"Sprint Name": "Janus Sprint 19E", "Sprint ID": 663},
                   {"Sprint Name": "Janus Sprint 19F", "Sprint ID": 679},
                   {"Sprint Name": "Janus Sprint 19G", "Sprint ID": 682}]
       }

PHX = {"Project Key": "PHX",
       "Project Name": "Phoenix",
       "Project ID": 11003,
       "Board Name": "Phoenix Board",
       "Board ID": 118,
       "Sprints": [{"Sprint Name": "Phoenix Sprint 19A", "Sprint ID": 630},
                   {"Sprint Name": "Phoenix Sprint 19B", "Sprint ID": 641},
                   {"Sprint Name": "Phoenix Sprint 19C", "Sprint ID": 647},
                   {"Sprint Name": "Phoenix Sprint 19D", "Sprint ID": 654},
                   {"Sprint Name": "Phoenix Sprint 19D", "Sprint ID": 654},
                   {"Sprint Name": "Phoenix Sprint 19E", "Sprint ID": 660},
                   {"Sprint Name": "Phoenix Sprint 19F", "Sprint ID": 672},
                   {"Sprint Name": "Phoenix Sprint 19G", "Sprint ID": 680}]
       }

PM = {"Project Key": "PM",
      "Project Name": "Project Management",
      "Project ID": 10703,
      "Board Name": "Project Management Community",
      "Board ID": 136,
      "Sprints": [{"Sprint Name": "PM 19A", "Sprint ID": 639},
                  {"Sprint Name": "PM 19C", "Sprint ID": 653},
                  {"Sprint Name": "PM 19D", "Sprint ID": 662},
                  {"Sprint Name": "PM 19E", "Sprint ID": 668}]
      }

QC = {"Project Key": "QC",
      "Project Name": "QA Community",
      "Project ID": 11100,
      "Board Name": "QA Community",
      "Board ID": 135,
      "Sprints": [{"Sprint Name": "QA 19A", "Sprint ID": 635},
                  {"Sprint Name": "QA 19B", "Sprint ID": 636},
                  {"Sprint Name": "QA 19C", "Sprint ID": 655},
                  {"Sprint Name": "QA 19D", "Sprint ID": 659},
                  {"Sprint Name": "QA 19E", "Sprint ID": 670},
                  {"Sprint Name": "QA 19F", "Sprint ID": 677},
                  {"Sprint Name": "QA 19G", "Sprint ID": 683}]
      }

SENTINEL = {"Project Key": "SENTINEL",
            "Project Name": "Sentinel",
            "Project ID": 10203,
            "Board Name": "Sentinel",
            "Board ID": 88,
            "Sprints": [{"Sprint Name": "SEN 19A", "Sprint ID": 643},
                        {"Sprint Name": "SEN 19B", "Sprint ID": 649},
                        {"Sprint Name": "SEN 19C", "Sprint ID": 651},
                        {"Sprint Name": "SEN 19D", "Sprint ID": 657},
                        {"Sprint Name": "SEN 19E", "Sprint ID": 666},
                        {"Sprint Name": "SEN 19F", "Sprint ID": 675},
                        {"Sprint Name": "SEN 19G", "Sprint ID": 681},
                        {"Sprint Name": "SEN 19H", "Sprint ID": 684}]
            }

TA = {"Project Key": "TA",
      "Project Name": "Test Automation",
      "Project ID": 11300,
      "Board Name": "Test Automation Board",
      "Board ID": 139,
      "Sprints": [{"Sprint Name": "Phoenix Sprint 19A", "Sprint ID": 630},
                  {"Sprint Name": "TA 19A", "Sprint ID": 640},
                  {"Sprint Name": "TA 19B", "Sprint ID": 648},
                  {"Sprint Name": "TA 19C", "Sprint ID": 656},
                  {"Sprint Name": "TA 19D", "Sprint ID": 664},
                  {"Sprint Name": "TA 19E", "Sprint ID": 669}]
      }



def filter_sprints_by_name(name):

    sprint_name = None
    # m = re.match(r'^[A-Za-z ]+(\d{2}\w{1}$)', s.name, re.M | re.I)
    m = re.match(r'^[A-Za-z ]+(19\w{1}$)', name, re.M | re.I)
    if m:
        sprint_name = m.group(1)

    return sprint_name


def get_authentication():

    # Get the command line arguments. There should be two: username and password
    arguments = sys.argv

    if len(arguments) == 3:
        return arguments[1], arguments[2]
    else:
        print('You must provide your JIRA username and password on the command line.')
        print('Example: {} username password'.format(arguments[0]))
        return 0


def connect_to_jira(auth):

    try:
        jira_server = {'server': 'https://jira.dev.countertack.com'}
        return JIRA(options=jira_server, basic_auth=auth)
    except BaseException as error:
        print(error)


def pprint(data):
    """Pretty prints json data."""

    print(json.dumps(
        data,
        sort_keys=True,
        indent=4,
        separators=(', ', ' : ')))


def get_page_json(auth, url, page_id, expand=False):
    """accesses and stores content of confluence page given page id """

    if expand:
        suffix = "?expand=body.storage"
    else:
        suffix = ""

    page = url + page_id + suffix
    response = requests.get(page, auth=auth)
    response.encoding = "utf8"
    return json.loads(response.text)


def set_page_json(auth, url, page_id, json_content):
    """Uses json content-type to dump new data to Confluence page given page id"""
    headers = {'Content-Type': 'application/json'}

    response = requests.put(url + page_id, headers=headers,
                            data=json.dumps(json_content), auth=auth)

    return response.text


def seconds_to_days_hours(seconds=0):

    result = None
    if seconds is not None:
        days = float(seconds) / 60 / 60 / 8
        hours = (days - int(days)) * 8
        result = '{}d {}h'.format(int(days), hours)

    return result


def seconds_to_days(seconds=0):
    return float(seconds) / 60 / 60 / 8


def seconds_to_hours(seconds=0):
    result = None
    if seconds is not None:
        hours = float(seconds) / 60 / 60
        result = '{} h'.format(hours)

    return result


def logged_time_per_issue(jira, issue):

    logs = jira.worklogs(issue.key)
    total_time = 0
    for wl in logs:
        # print('{}: {} = {}'. format(issue.key, wl.updateAuthor, secondsToDaysHours(wl.timeSpentSeconds)))
        total_time += wl.timeSpentSeconds

    return total_time


def dummy():
    print("Making Changes")


def main():

    dummy()

    # Authenticate the user and quit if this fails
    authentication = get_authentication()
    if authentication != 0:
        # Connect to Jira
        jira_connection = connect_to_jira(authentication)
    else:
        print('Could not authenticate the user. Exiting...')
        return 1

    print("### Projects ###")
    project = jira_connection.projects()
    for p in project:
        print('{key} = {{"Project Key": "{key}", "Project Name": "{name}", "Project ID": {id}}}'
              .format(key=p.key, name=p.name, id=p.id))
    print("")
    print("")

    # Print the list of Jira boards by name
    print("### Boards ###")
    boards = jira_connection.boards()
    for b in boards:
        print(', "Board Name": "{name}", "Board ID": {id}'.format(name=b.name, id=b.id))
    print("")
    print("")

    print("### Boards and Sprints ###")
    for b in boards:
        print(', "Board Name": "{name}", "Board ID": {id}'.format(name=b.name, id=b.id))
        sprints = jira_connection.sprints(b.id)
        print('"Sprints": [')
        for s in sprints:
            sprint_name = filter_sprints_by_name(s.name)
            if sprint_name is not None:
                print('{{"Sprint Name": "{name}", "Sprint ID": {id}}},'.format(name=s.name, id=s.id))
        print(']')
    print("")
    print("")


    issues = jira_connection.search_issues("Project in (Phoenix)")
    for i in issues:
        print(i)

    file = open('Projects Boards and Sprints Oh My.txt', 'w')
    file.write("Adding something to the file.")
    file.close()


if __name__ == '__main__':
    main()
