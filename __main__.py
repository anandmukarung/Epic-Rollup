import ct_atlassian_tools as atl
from jira import JIRA

# commit

def main():
    authentication = atl.get_authentication()
    jira_connection = atl.connect_to_jira(authentication)
    # connection = JIRA("https://jira.dev.countertack.com")
    projects = jira_connection.projects()
    # for p in projects:
    #   print(p)
    sandbox = jira_connection.project("SAND")
    jql = "project=" + str(sandbox)
    all_issues = jira_connection.search_issues(jql)
    epics = []

    for i in all_issues:
        iType = str(i.fields.issuetype)
        if iType == "Epic":
            epics.append(i)

    # Getting the child stories for the epic
    epic = "SAND-2"
    jql = '"Epic Link"=' + epic
    linked_stories = jira_connection.search_issues(jql)

    # Summing up all the times for the child stories
    total_estimated_time = 0
    total_remaining_time = 0
    for s in linked_stories:
        issue = jira_connection.issue(s.id)
        original_raw = issue.fields.aggregatetimeoriginalestimate
        remaining_raw = issue.fields.aggregatetimeestimate
        print('o = ' + str(original_raw))
        print('r = ' + str(remaining_raw))
        if original_raw is None:
            if remaining_raw is not None:
                original_raw = remaining_raw
            else:
                original_raw = 0
        if remaining_raw is None:
            remaining_raw = 0
        total_estimated_time += int(original_raw)
        total_remaining_time += int(remaining_raw)

    # The estimate and remaining are both given in seconds
    print('total estimate: {} seconds\t remaining: {} seconds'.format(total_estimated_time, total_remaining_time))

    # 34710: id for Sand - 2  (Scott is doing stuff with other epics, only work with Sand-2)
    for e in epics:
        print(e.id)
        print(str(e))
        if e.id == '34710':
            print('updating time for Sand-2')
            # Convert seconds to hours when setting the times
            e.update(timetracking={'originalEstimate': '{}h'.format(total_estimated_time / 3600),
                                   'remainingEstimate': '{}h'.format(total_remaining_time / 3600)})

        # e.update(fields={'description': "I just updated the description from Python"})
        # e.update(fields={'labels':['Imadethislabel', 'Thisonetoo']})
        # e.update(fields={'customfield_10803': {'value': '60%'}})         # Customfield_10803 = %Complete
        # e.update(fields={'timeoriginalestimate': {'value': int(12000)}})
        # e.update(timetracking={'originalEstimate': '20h'})
        # e.update(timetracking={'originalEstimate': '20h', 'remainingEstimate': '10h'})


main()
