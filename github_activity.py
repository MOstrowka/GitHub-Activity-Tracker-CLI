#!/usr/bin/env python3

import argparse
import sys
import urllib.request
import json
from collections import defaultdict


def fetch_github_activity(username):
    url = f"https://api.github.com/users/{username}/events"
    try:
        with urllib.request.urlopen(url) as response:
            if response.status == 200:
                data = json.loads(response.read().decode())
                return data
            elif response.status == 404:
                print(f"Error: User '{username}' not found.")
                return None
            else:
                print(f"Error: Failed to fetch data, status code {response.status}")
                return None
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"Error: User '{username}' not found.")
        else:
            print(f"Error: Failed to fetch data, HTTP status code {e.code}")
        return None
    except urllib.error.URLError as e:
        print(f"Error: Failed to connect to GitHub API. {e.reason}")
        return None
    except json.JSONDecodeError:
        print("Error: Failed to parse response from GitHub API.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


def display_activity(events, event_type=None):
    if not events:
        print("No recent activity found.")
        return

    activity_summary = defaultdict(lambda: defaultdict(int))

    for event in events:
        if event_type and event['type'] != event_type:
            continue

        event_type_name = event['type']
        repo_name = event['repo']['name']

        if event_type_name == 'PushEvent':
            commit_count = len(event['payload']['commits'])
            activity_summary[repo_name]['PushEvent'] += commit_count
        elif event_type_name == 'IssuesEvent':
            action = event['payload']['action']
            activity_summary[repo_name][f"IssuesEvent-{action}"] += 1
        elif event_type_name == 'WatchEvent':
            activity_summary[repo_name]['WatchEvent'] += 1
        elif event_type_name == 'PullRequestEvent':
            action = event['payload']['action']
            activity_summary[repo_name][f"PullRequestEvent-{action}"] += 1
        elif event_type_name == 'CreateEvent':
            ref_type = event['payload']['ref_type']
            activity_summary[repo_name][f"CreateEvent-{ref_type}"] += 1
        elif event_type_name == 'PublicEvent':
            activity_summary[repo_name]['PublicEvent'] += 1

    for repo, actions in activity_summary.items():
        for action, count in actions.items():
            if action == 'PushEvent':
                print(f"Pushed {count} commit{'s' if count > 1 else ''} to {repo}")
            elif 'IssuesEvent' in action:
                action_type = action.split('-')[1]
                print(f"{action_type.capitalize()} {count} issue{'s' if count > 1 else ''} in {repo}")
            elif 'PullRequestEvent' in action:
                action_type = action.split('-')[1]
                print(f"{action_type.capitalize()} {count} pull request{'s' if count > 1 else ''} in {repo}")
            elif 'CreateEvent' in action:
                ref_type = action.split('-')[1]
                print(f"Created {count} new {ref_type}{'s' if count > 1 else ''} in {repo}")
            elif action == 'WatchEvent':
                print(f"Starred {repo}")
            elif action == 'PublicEvent':
                print(f"Made {repo} public")


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="GitHub Activity Tracker CLI")

    # Add argument for GitHub username or help
    parser.add_argument('username', nargs='?', help='GitHub username to fetch activity for or "help" to display help')
    parser.add_argument(
        '--event-type',
        help=(
            'Filter activities by event type. Available types: '
            'PushEvent, IssuesEvent, WatchEvent, PullRequestEvent, CreateEvent, PublicEvent'
        )
    )

    # Parse the arguments
    args = parser.parse_args()

    # Handle the help command
    if args.username == 'help' or args.username is None:
        parser.print_help()
        sys.exit(0)

    # Fetch GitHub activity
    print(f"Fetching activity for GitHub user: {args.username}")
    events = fetch_github_activity(args.username)

    # Only display activity if events are fetched successfully
    if events:
        display_activity(events, args.event_type)


if __name__ == '__main__':
    main()
