import sys

if __name__ == '__main__':
    topic = '0.000*"paragraph" + 0.000*"stylecode" + 0.000*"rsq" + 0.000*"113883" + 0.000*"dose" + 0.000*"codesystem" + 0.000*"code" + 0.000*"00" + 0.000*"01380" + 0.000*"nov"'

    tmp = topic.split('+')
    for t in tmp:
        a = t.split('"') 
        print(a[0][:-1])
        print(a[1])

