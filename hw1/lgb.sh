# Main
## Part 1
### 1
git commit
git commit
### 2
git checkout -b bugFix
### 3
git checkout -b bugFix
git commit
git checkout main
git commit
git merge bugFix
### 4
git checkout -b bugFix
git commit 
git checkout main 
git commit
git checkout bugFix
git rebase main
## Part 2
### 1
git checkout C4
### 2
git checkout C3
### 3
git branch -f bugFix HEAD~2
git branch -f main C6
git checkout HEAD^
### 4
git branch -f local HEAD^
git checkout pushed
git revert HEAD
## Part 3
### 1
git cherry-pick C3 C4 C7
### 2
git rebase -i C1
## Part 4
### 1
git checkout main
git cherry-pick C4
### 2
git rebase -i C1
git commit --amend
git rebase -i C1
git branch -f main
### 3
git checkout main
git cherry-pick C2
git commit --amend
git cherry-pick C3
### 4
git checkout C2
git tag v1
git tag v0 HEAD^
### 5
git describe # v1-2-gC6
git describe # v1-1-gC4
git commit
## Part 5
### 1
git rebase bugFix
git rebase bugFix side
git rebase side another
git branch -f main
### 2
git branch HEAD^^2^
### 3
git checkout one
git cherry-pick C4 C3 C2
git checkout two
git cherry-pick C5 C4 C3 C2
git branch -f three C2
# Remote
## Part 1
### 1
git clone
### 2
git commit
git checkout HEAD^
git commit
### 3
git fetch
### 4
git pull
### 5
git fakeTeamwork 2
git commit
git pull
### 6
git commit
git commit
git push
### 7
git clone
git fakeTeamwork
git commit
git pull --rebase
git push
### 8
git reset o/main
git checkout -b feature C2
git push
## Part 2
### 1
git rebase side1 side2
git rebase side2 side3
git pull --rebase
git push
### 2
git checkout main
git pull
git merge side1
git merge side2
git merge side3
git push
### 3
git checkout -b side o/main
git commit
git pull --rebase
git push
### 4
git push origin main
git push origin foo
### 5
git push origin main^:foo
git push origin foo:main
### 6
# Не получилось :(
### 7
git push origin :foo
git fetch origin :bar
### 8
git pull origin bar:foo
git pull origin main:side