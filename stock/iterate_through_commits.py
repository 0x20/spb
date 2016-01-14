from datetime import date
import csv

from pygit2 import Repository

repo = Repository('.git')
diff = repo.diff

prev_commit = None

consolidate = True

if consolidate is True:
    matrix = {}
else:
    matrix = []

for commit in repo.walk(repo.head.target):
    print(commit.message)

    if prev_commit is not None:
        # get the diff info
        diff = repo.diff(commit, prev_commit)

        # Get the string with changed info and split it
        changes = diff.patch.split('\n')[5:]
        try:
            a = changes[3].split()
            b = changes[4].split()
        except:
            print("last one? and I am too lasy to dump that one so here we go")
            Exception
        else:
            try:
                person_a = a[0][1:]
                person_b = b[0][1:]
            except:
                print("new person")
                Exception
            else:
                if person_a != person_b:
                    print("Overschrijving (niet zelfde persoon)")

                else:
                    # person - amount(diff) - date
                    try:
                        change = float(b[1]) - float(a[1])



                        if change > 0:  # < for payments > for deposits

                            if consolidate is False: # output per line

                                date = date.fromtimestamp(commit.commit_time) # add timestamp of commit
                                row = [person_b, change, date]
                                matrix.append(row)

                            else: # consolidate per month

                                dt = date.fromtimestamp(commit.commit_time).strftime('%y%m') # add timestamp of commit
                                row = {dt: change}

                                if dt not in matrix:

                                    matrix[dt] = change
                                else:
                                    matrix[dt] += change

                        else:
                            print ("Value negative, discard")
                    except:
                        print ("not a valid row")

                        Exception

    prev_commit = commit

if consolidate is True:
    with open("output.csv", "w") as f:
        writer = csv.writer(f)

        for key, value in matrix.items():
            writer.writerow([key, value])

else:

    with open("output.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerows(matrix)