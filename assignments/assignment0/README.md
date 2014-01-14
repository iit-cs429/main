## Assignment 0: Indexing

1. Learn Python by complete the online Python training course at <http://www.codecademy.com/tracks/python>.

2. Learn git by completing the online training course at <http://try.github.io>.

3. Install the Python/SciPy stack on your computer (if you haven't already) by follwing the instructions here: <http://continuum.io/downloads>.

4. Install Git
  - Windows: Download the installer from <http://msysgit.github.io/> and run it
  - Mac/Linux: Check if git is already installed by running `which git`
    - To install on Linux: `sudo apt-get install git` (Ubuntu) or `yum install git-core` (Fedora)
    - To install on Mac: <http://sourceforge.net/projects/git-osx-installer/>

5. Clone your private class repository
```
git clone https://github.com/iit-cs429/[iit-username].git
```
E.g., for me this would be:
  ```
   git clone https://github.com/iit-cs429/aculotta.git
  ```
  - You should have read/write (pull/push) access to your private repository.
  - This is where you will submit assignments.

6. Update your private repository with `git pull`
  - I will add files to your repository for each assignment.

7. Modify the README.md file in your repository to list your name.
  - Checkin this change with:

```
git add README.md 
git commit -m 'my first commit'
git push
```
