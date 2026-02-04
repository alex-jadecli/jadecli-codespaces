# CLAUDE.md - GitHub Issues Guide Reference

## Quick Navigation

- [Issues](#issues)
- - [Projects](#projects)
  - - [Labels & Milestones](#labels--milestones)
    - - [Automation](#automation)
     
      - ---

      ## Issues

      ### [Quickstart for GitHub Issues](https://docs.github.com/en/issues/tracking-your-work-with-issues/learning-about-issues/quickstart)

      Interactive guide: create issues, add sub-issues, labels, types, milestones, assignees, projects. Use @mentions for collaboration, # to link related issues.

      ### [Creating an Issue](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/creating-an-issue)

      Methods: repository UI, GitHub CLI (`gh issue create`), from comments, code, discussions, projects, task lists, URL query params, Copilot. Supports templates via `ISSUE_TEMPLATE/`.

      ### [Adding Sub-issues](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/adding-sub-issues)

      Break work into hierarchical tasks. Max 100 sub-issues per parent, 8 nesting levels. Create new or add existing issues as sub-issues.

      ### [Creating Issue Dependencies](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/creating-issue-dependencies)

      Mark issues as "blocked by" or "blocking" other issues. Blocked issues show icon on project boards. Requires triage permissions.

      ### [Managing Issue Types](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/managing-issue-types-in-an-organization)

      Org-level classification (task, bug, feature). Max 25 types. Filter/search by type. Org owners manage via Settings > Planning > Issue types.

      ### [Filtering and Searching Issues](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/filtering-and-searching-issues-and-pull-requests)

      Boolean operators (`AND`, `OR`), nested queries with parentheses (5 levels). Key filters: `author:`, `assignee:`, `label:`, `type:`, `is:`, `state:`, `review:`. Share filters via URL.

      ### [Viewing All Issues and PRs](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/viewing-all-of-your-issues-and-pull-requests)

      Dashboard at top of any page. Create up to 25 saved views with custom queries.

      ---

      ## Projects

      ### [Quickstart for Projects](https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/quickstart-for-projects)

      Create org/user project. Add items via URL paste or search. Custom fields: iteration, priority, estimate. Views: table, board, roadmap. Built-in automation workflows.

      ### [Planning and Tracking Work](https://docs.github.com/en/issues/tracking-your-work-with-issues/learning-about-issues/planning-and-tracking-work-for-your-team-or-project)

      Repository types: product, project, team, personal. Use README.md, CONTRIBUTING.md. Issue templates for release tracking, initiatives, feature requests, bugs.

      ### [Best Practices for Projects](https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/best-practices-for-projects)

      Use @mentions, break large issues into sub-issues, leverage description/README/status updates, create custom views, use field types (date, number, single select, iteration), automate, create charts, use templates.

      ### [Creating a Project](https://docs.github.com/en/issues/planning-and-tracking-with-projects/creating-projects/creating-a-project)

      Org projects: profile > Organizations > Projects > New. User projects: profile > Projects > New. Choose Table/Roadmap/Board or use templates. Set description and README via Settings.

      ### [Understanding Fields](https://docs.github.com/en/issues/planning-and-tracking-with-projects/understanding-fields)

      Field types: text, number, date, single select, iteration (with breaks), parent/sub-issue progress, pull request, issue type. Rename/delete custom fields.

      ### [Customizing Views](https://docs.github.com/en/issues/planning-and-tracking-with-projects/customizing-views-in-your-project)

      Layouts: table, board, roadmap. Filter, group, sort, slice by assignee, show field sums, add column limits. Save and share views.

      ### [Creating Charts](https://docs.github.com/en/issues/planning-and-tracking-with-projects/viewing-insights-from-your-project/creating-charts)

      Access via project > Insights. Click "New chart", apply filters, configure grouping/layout/axes, save changes.

      ### [Managing Project Templates](https://docs.github.com/en/issues/planning-and-tracking-with-projects/managing-your-project/managing-project-templates-in-your-organization)

      Create templates or mark projects as templates. Templates copy views, fields, drafts, workflows (except auto-add), insights. Configure up to 6 recommended templates.

      ### [Adding Items to Your Project](https://docs.github.com/en/issues/planning-and-tracking-with-projects/managing-items-in-your-project/adding-items-to-your-project)

      Methods: paste URL, search (`#`), bulk add, from repo lists, command palette (Cmd/Ctrl+K). Create issues directly from project. Draft issues for quick capture. Max 50,000 items.

      ---

      ## Labels & Milestones

      ### [Managing Labels](https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/managing-labels)

      Categorize issues/PRs/discussions. Default labels: bug, documentation, duplicate, enhancement, good first issue, help wanted, invalid, question, wontfix. Create/edit/delete via Issues > Labels.

      ### [Creating and Editing Milestones](https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/creating-and-editing-milestones-for-issues-and-pull-requests)

      Track progress on issue/PR groups. Issues/PRs > Milestones > New Milestone. Set title, description, due date. Supports Markdown.

      ---

      ## Automation

      ### [Using Built-in Automations](https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/using-the-built-in-automations)

      Default workflows: set status to "Done" on close/merge. Configure via project menu > Workflows > Default workflows. Auto-archive and auto-add workflows available.

      ### [Using the API to Manage Projects](https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/using-the-api-to-manage-projects)

      GraphQL API for automation. Mutations: `addProjectV2ItemById`, `addProjectV2DraftIssue`, `updateProjectV2ItemFieldValue`, `deleteProjectV2Item`, `createProjectV2`. Use `read:project` (queries) or `project` (mutations) scope.

      ### [Automating Projects using Actions](https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/automating-projects-using-actions)

      Workflow on `pull_request: ready_for_review`. Auth via GitHub App (org projects) or PAT (user projects). Query project fields, add items, update Status/Date fields. Use `actions/add-to-project` action.

      ---

      ## See Also

      - [GitHub Issues Guides Index](https://docs.github.com/en/issues/guides)
      - - [About Issues](https://docs.github.com/en/issues/tracking-your-work-with-issues/learning-about-issues/about-issues)
        - - [About Projects](https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/about-projects)
         
          - ---

          ## Registry

          ### CLI Commands

          `gh issue create --title "TITLE" --body "BODY"` - Create issue via GitHub CLI
          `gh issue list` - List issues with optional filters
          `gh pr list` - List pull requests with optional filters
          `gh api graphql -f query='...'` - Execute GraphQL queries/mutations

          ### GraphQL Mutations

          `addProjectV2ItemById(input: {projectId, contentId})` - Add issue/PR to project
          `addProjectV2DraftIssue(input: {projectId, title, body})` - Add draft issue to project
          `updateProjectV2ItemFieldValue(input: {projectId, itemId, fieldId, value})` - Update field value
          `deleteProjectV2Item(input: {projectId, itemId})` - Remove item from project
          `createProjectV2(input: {ownerId, title})` - Create new project

          ### GraphQL Queries

          `organization(login:).projectV2(number:)` - Get org project by number
          `user(login:).projectV2(number:)` - Get user project by number
          `node(id:).fields(first:)` - Get project fields and options

          ### Search Qualifiers

          `is:issue` / `is:pr` / `is:open` / `is:closed` / `is:draft` / `is:merged`
          `author:USER` / `assignee:USER` / `involves:USER` / `review-requested:USER`
          `label:"LABEL"` / `milestone:"NAME"` / `project:ORG/NUM` / `type:"TYPE"`
          `linked:pr` / `linked:issue` / `no:assignee` / `no:label` / `no:project`
          `reason:completed` / `reason:"not planned"` - Closed issue reasons
          `review:none` / `review:required` / `review:approved` / `review:changes_requested`

          ### URL Query Parameters

          `?title=TITLE` - Pre-fill issue title
          `?body=BODY` - Pre-fill issue body
          `?labels=label1,label2` - Apply labels
          `?assignees=user1,user2` - Assign users
          `?milestone=NAME` - Set milestone
          `?projects=ORG/NUM` - Add to project
          `?template=filename.md` - Use issue template

          ### Field Types

          `ProjectV2Field` - Text/number fields
          `ProjectV2SingleSelectField` - Dropdown with options
          `ProjectV2IterationField` - Time-boxed iterations with breaks
          `ProjectV2ItemFieldTextValue` - Text field value
          `ProjectV2ItemFieldDateValue` - Date field value
          `ProjectV2ItemFieldSingleSelectValue` - Selected option value

          ### Built-in Workflows

          `Item added to project` - Set status when item added
          `Item closed` - Set status to Done on close
          `Item reopened` - Reset status on reopen
          `Pull request merged` - Set status to Done on merge
          `Auto-add to project` - Add items matching filter criteria
          `Auto-archive items` - Archive items meeting criteria

          ### Default Labels

          `bug` / `documentation` / `duplicate` / `enhancement` / `good first issue` / `help wanted` / `invalid` / `question` / `wontfix`

          ### Default Issue Types

          `task` / `bug` / `feature`

          ### Project Layouts

          `Table` - Spreadsheet view with sortable columns
          `Board` - Kanban columns by status/field
          `Roadmap` - Timeline view with date/iteration fields

          ### Actions

          `actions/create-github-app-token@v2` - Generate app installation token
          `actions/add-to-project` - Add current issue/PR to specified project

          ### Webhook Events

          `projects_v2_item` - Fires on project item changes

          ### Permissions

          `read:project` - Read-only project access (queries)
          `project` - Full project access (queries + mutations)
          `repo` - Repository access for issues/PRs

          ### Limits

          `50,000` - Max items per project (active + archived)
          `100` - Max sub-issues per parent issue
          `8` - Max sub-issue nesting levels
          `25` - Max issue types per organization
          `25` - Max saved views per dashboard
          `6` - Max recommended templates per org
          `20` - Max fields returned per query (paginate for more)
