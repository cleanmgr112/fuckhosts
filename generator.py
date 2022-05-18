"""Blocklistt
"""
from typing import *
import os
from datetime import datetime as date
import re

now=date.now().strftime("%Y-%m-%d %H:%M:%S")

def generateIPV4Hosts(block_list: list):
    return sorter(block_list, 'hosts')

def generateAdblockList(block_list: list):
    return sorter(block_list, 'adblock')

def sorter(domains:list[str], mode):
    '''gets list of domains and returns sorted by domain in alphabetical order'''    
    already = l = []
    entries = f'\n'#{time}'

    for i in domains:
        if t := re.findall(r'\w+\.\w+$', i):
            print(i)
            l.append([i.split(t[0])[0], t[-1]])
        else:pass
    l = sorted(l, key = lambda x: x[::-1])

    for i in l:
        domain = i[-1]
        if domain not in already:
            ae=[j if j[-1] == domain else None for j in l]
            ae=list(filter(None, ae))

            so_ = sorted(ae, key = lambda x: x[::-1])

            if mode=='hosts':
                entries += f'\n# {domain}\n' + '\n'.join(['0.0.0.0 {}'.format(entry) for entry in [''.join(j) for j in so_]])+'\n'

            elif mode=='adblock':
                entries += f'\n# {domain}\n' +'\n'.join(['||{}^'.format(entry) for entry in [''.join(j) for j in so_]]) +'\n'

            already.append(domain)
    return entries


# All generators
generator_list: dict = {
    "hosts.txt": generateIPV4Hosts,
    "adblok.txt": generateAdblockList
}
file_list=[
    "wot.txt",
    "melcosoft.txt",
    "rom.txt",
    "tikkok.txt"
]

def main() -> int:
    # Load the block list to a newline-seperated list
    entries = []
    for i in file_list:
        with open(i, "r") as f:
            rr=f.read().split("\n")
            [entries.append(i) for i in rr]

    # Filter empty lines
    entries = list(filter(None, entries))

    # Create the output dir
    os.makedirs("output", exist_ok=True)

    # Run every generator
    for gen in generator_list:
        print(f"Running generator: {gen}")
        with open(f"output/{gen}", "w") as f:
            f.write(f"#{now}\n"+generator_list[gen](entries))


if __name__ == "__main__":
    main()
