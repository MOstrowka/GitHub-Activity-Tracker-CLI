
# GitHub Activity Tracker CLI

GitHub Activity Tracker CLI is a command-line tool designed to fetch and display the recent activity of a GitHub user. This project helps you practice working with APIs, handling JSON data, and building a simple CLI application.

## Features

- Fetch recent activity of a specified GitHub user.
- Display various types of GitHub events, such as commits, issues, and stars.
- Handle errors gracefully.

## Installation

1. **Clone the repository:**

   ```bash
   git clone Miniomamen/GitHub-Activity-Tracker-CLI
   cd GitHub-Activity-Tracker-CLI
   ```

2. **Ensure Python (3.x) is installed and accessible via the command line.**

## Usage

To use the GitHub Activity Tracker CLI application, open a terminal, navigate to the project directory, and use the following commands:

### Fetching a User's Activity

```bash
github-activity <username>
```

**Example:**

```bash
github-activity kamranahmedse
```

### Displaying Help

To display help information:

```bash
github-activity help
```

### Handling Errors

- If a user does not exist, the CLI will display: `Error: User '<username>' not found.`

## Examples

```bash
github-activity kamranahmedse
Fetching activity for GitHub user: kamranahmedse
Pushed 15 commits to kamranahmedse/developer-roadmap
Closed 15 pull requests in kamranahmedse/developer-roadmap

github-activity nonexistinguser
Fetching activity for GitHub user: nonexistinguser
Error: User 'nonexistinguser' not found.
```

## Project URL

For more details about this project, visit the [Github User Activity Project Page](https://roadmap.sh/projects/github-user-activity).
