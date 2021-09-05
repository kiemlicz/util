# Hands-on commands
Checkout remote branch:  
`git checkout -b <name> origin/<name>`

Checkout directory to given changeset:  
`git checkout 3257289075289037592abcde253 -- path/to/the/folder/`

Multiple working trees sharing one repository:  
`git worktree add ../some/path/ branch`  
Checkouts `branch` under `../some/path/`

Compare file with branch:  
`git diff mybranch otherbranch -- somefile`

Transfer single commit between branches:  
```
git checkout desired_branch
git cherry-pick commit_to_be_transferred_here_by_hash

git checkout orig_branch
#rollback commit
git reset --hard HEAD^
```
# Branches
## Checkout
Remote to local:  
`git checkout -b <local_branch_name> <remote_name>/<remote_branch_name>`

## Delete
Remote:  
`git push <remote_name> --delete <branch_name>`

Locally:  
`git branch -d <local_branch_name>`

## Rename
First rename locally, then delete old branch on remote, finally push "new"
```
git branch -m old_branch new_branch   
git push origin :old_branch  
git push --set-upstream origin new_branch 
```

# Submodules
Project can depend on other projects. Root project is called **superproject**.  
Submodule is always a commit in other repostiory. In other words: submodule points to particular commit.

## Adding
`git submodule add https://repo.url... [path]` add submodule to project at _path_.  
If no _path_ is given then repo name is used.

## Deleting
1. `git submodule deinit <submodule>`
2. `git rm <submodule>`
3. `rm -rf .git/modules/asubmodule`

## Cloning
By default submodules are not cloned. In order to clone repository that contains submodules:

1. `git clone <repo url>`
2. `git submodule init`
3. `git submodule update`

## Upgrading
In order to "upgrade" the submodule (actually submodule's commit):

1. `cd submodule_dir`
2. `git checkout desired_branch`
3. `git pull`
4. `cd ..`
5. `git add submodule_dir && git commit -m "..."`

## Other
In order to change submodule's URL, edit _.gitmodules_ files and run `git submodule sync`

# Useful infographic
![](http://blog.podrezo.com/wp-content/uploads/2014/09/git-operations.png)

# References
 1. http://www.saintsjd.com/2011/01/what-is-a-bare-git-repository/
 2. http://gitolite.com/gcs.html#%281%29