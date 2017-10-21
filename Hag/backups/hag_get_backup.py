import time,datetime,pandas,requests
from subprocess import call
from colorama import init,Fore,Back,Style
init()
polling=[]
times=[]
means={}
begin_time=time.time()
slots = [
    'testaut-1-stb-1',
    'testaut-1-stb-2',
    'testaut-1-stb-3',
    'testaut-1-stb-4',
]

def run_once(polling_interval):
    time.sleep(0.2)

    call(['clear'],shell=True)
    print 'BOX\t\t\tSTATUS'
    print '================================================'

    def restart(slot):
        requests.get('http://127.0.0.1:4000/fake-jenkins-do-something/START/'+slot)

    def slotchck(slot):
        resp=requests.get('http://127.0.0.1:4000/fake-jenkins-status/'+slot)
        return resp.text

    statii = {
        'testaut-1-stb-1': False,
        'testaut-1-stb-2': False,
        'testaut-1-stb-3': False,
        'testaut-1-stb-4': False
        }

    def slots_complete():
        return all(statii.values())

    while not slots_complete():
        time.sleep(polling_interval)

        for slot in slots:

            chck=slotchck(slot)
            if chck in ['FAILURE','unknown']:
                if chck =='unknown':
                    print slot+'\t\t'+Fore.YELLOW+chck+Style.RESET_ALL
                else:
                    print slot+'\t\t'+Fore.RED+chck+Style.RESET_ALL
                restart(slot)

            elif chck=='SUCCESS':
                statii[slot]=True
                print slot+'\t\t'+Fore.GREEN+chck+Style.RESET_ALL

    for slot in slots:
        requests.get('http://127.0.0.1:4000/fake-jenkins-do-something/RESTART/'+slot)

polling_intervals = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
means = []

for polling_interval in polling_intervals:
    times = []
    for i in range(15):
        start_time=time.time()
        run_once(polling_interval)
        end_time=time.time()-start_time
        times.append(end_time)
    means.append(round(sum(times)/len(times),2))


overall_time=time.time()-begin_time
call(['clear'],shell=True)
print Fore.YELLOW+'\n\n\n\t\ttimes:'
print '\t\t',times,'\n'
print'\t\tpolling intervals tested:'
print '\t\t',polling_intervals,'\n'
print '\t\tThese are the means for each test rounded to 2 decimal places:'
print '\t\t',means,'\n'
total_mean=sum(times)/len(times)
print '\t\tTotal mean:',total_mean
print '\t\tTotal rounded mean to 2 decimal places:',round(total_mean,2)
print '\t\tTotal time for test',overall_time,'seconds'
