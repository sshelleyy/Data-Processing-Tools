# github terminal commends

*bro i need to do calc i cant do this rn*

ok whatever

## set up (do once, before work)
`git config --global user.name "Your Name"`

`git config --global user.email "your@email.com"`
- tells git ur name and info

`git init`
- turns current folder to git repo, creating hidden .git folder
- dont touch .git

## saving work
`git status`
- see "status" of doc, which files modified, which are "staged for save"

`git add <file>`
- moves file to staging

`git add . ` or `folder_name/`
- adds everything in folder

`git commit -m "Your message"`
- commits all staged. msg should be shortish

`git restore .`
- restores current working directory to last successful save
- replace `.` with path if only specific

`git blame <filename>`
- shows every line of code with author and date
  - scary scary

## reviewing history
`git log`
- shows list of all prev commits, authors, dates

`git diff`
- shows exactly which lines of code changed since last save

## git hygiene
`git commit --amend --no-edit`
- squashes change to last commit for clean edits

`git stash`
- hides current work, restores to last commit

`git stash pop`
- reopens stash on stack. uses LIFO (open most recent)

## git ignore
`.gitignore`
- this file usually is in project root
- **all ignores are relative to the directory that .gitignore is in**

`*.file`
- ignore all files endings in `.log`

`directory/`
- ignore repository and it's contents. use path relative to project

- `directory/*.type` 
  - ignore `.type` files in `directory`
- `**/directory/`
  - ignore any `directory` regardless of location

`file-name.type`
- ignore file-name

`!file-name.type`
- tracks file-name.type even if it is in ignored directory

## branches
`git branch <name>`
- creates new branch

`git checkout <name>` 
* switch ur view to `<name>` branch

` git merge <name>`
- combine work from that branch into current one

`git push origin main` 
- push ur local commits to main branch of "origin" (think of as github hyperlink)
- add `--force` to overwrite any conflicting main branch updates w ur own