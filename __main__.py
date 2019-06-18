import ct_atlassian_tools as atl
from jira import JIRA


# connecting to Jira
def connect_to_jira():
    authentication = atl.get_authentication()
    jira_connection = atl.connect_to_jira(authentication)
    return jira_connection

# return list of projects specifically for Sand and Sentinel
def get_projects(jira_connection):

    projects_list = ["SAND", "SENTINEL"]
    projects = []
    for p in projects_list:
        j_p = jira_connection.project(p)
        projects.append(j_p)
    return projects


def get_epics(jira_connection, project):

    jql = "project= " + str(project) + " AND issuetype = Epic"
    epic_issues = []
    all_issues = jira_connection.search_issues(jql)
    # ---------------------------------------------------------------
    # searching for all issues in project and adding it to a list of epic issues

    for issue in all_issues:
        issue_type = str(issue.fields.issuetype)
        if issue_type == "Epic":
            epic_issues.append(issue)
    return epic_issues


def get_child_issues(jira_connection, epic):
    jql = '"Epic Link"=' + str(epic)
    child_issues = jira_connection.search_issues(jql)
    return child_issues


def get_aggregate_times(jira_connection, child_issues):
    # Summing up all the times for the child stories
    total_estimated_time = 0
    total_remaining_time = 0
    total_logged_time = 0
    print('Child Issues:**********************************************************')
    for story in child_issues:
        issue = jira_connection.issue(story.id)
        original_raw = issue.fields.aggregatetimeoriginalestimate
        remaining_raw = issue.fields.aggregatetimeestimate
        logged_raw = issue.fields.aggregatetimespent
        issue_type = issue.fields.issuetype
        print('{} Type: {}\t original: {}\t remaining: {}:\t logged: {}'.format(issue, issue_type, original_raw,
                                                                                remaining_raw, logged_raw))
        if remaining_raw is None:
            remaining_raw = 0
        if logged_raw is None:
            logged_raw = 0
        if original_raw is None:
            if remaining_raw is not None and logged_raw is not None:
                original_raw = int(remaining_raw) + int(logged_raw)
            else:
                original_raw = 0

        total_estimated_time += int(original_raw)
        total_remaining_time += int(remaining_raw)
        total_logged_time += int(logged_raw)
    print('End of Child Issues ****************************************************')
    time_stats = (total_estimated_time, total_remaining_time, total_logged_time)
    return time_stats


def main():
    jira_connection = connect_to_jira()
    # sandbox = jira_connection.project("SAND")
    projects = get_projects(jira_connection)
    for project in projects:
        print('**********************************************************************************************\n')
        print('PROJECT: {}'.format(project))
        epics = get_epics(jira_connection, project)
        for epic in epics:
            summary = epic.fields.summary
            print('Epic: {}\n Summary: {}\n'.format(epic, summary))
            child_issues = get_child_issues(jira_connection, epic)
            total_estimated_time, total_remaining_time, total_logged_time = get_aggregate_times(jira_connection,
                                                                                                child_issues)

            if total_estimated_time == 0:
                percent = 0
            else:
                percent = (1 - (total_remaining_time / total_estimated_time)) * 100
                percent = percent - (percent % 10)
            print('\nTotal Estimated: {}\nTotal Remaining: {}\nTotal Logged: '
                  '{}\nPercent Complete: {}%'.format(total_estimated_time,
                                                     total_remaining_time, total_logged_time, percent))


'''
    # 34710: id for Sand - 2  (Scott is doing stuff with other epics, only work with Sand-2)
    for epic_issue in epic_issues:
        print(epic_issue.id)
        print(str(epic_issue))
        if epic_issue.id == '34710':
            print('updating time for Sand-2')
            # Convert seconds to hours when setting the times
            epic_issue.update(timetracking={'originalEstimate': '{}h'.format(total_estimated_time / 3600),
                                   'remainingEstimate': '{}h'.format(total_remaining_time / 3600)})

        # e.update(fields={'description': "I just updated the description from Python"})
        # e.update(fields={'labels':['Imadethislabel', 'Thisonetoo']})
        # e.update(fields={'customfield_10803': {'value': '60%'}})         # Customfield_10803 = %Complete
        # e.update(fields={'timeoriginalestimate': {'value': int(12000)}})
        # e.update(timetracking={'originalEstimate': '20h'})
        # e.update(timetracking={'originalEstimate': '20h', 'remainingEstimate': '10h'})

'''
main()
