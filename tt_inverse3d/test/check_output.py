#!/usr/bin/env python

import os
import sys
from optparse import OptionParser

SMESH = "smesh"
REFL = "refl"
RAY = "ray"
TRES = "tres"
LOG = "log"

FORMATS = [SMESH, REFL, RAY,TRES, LOG ]

nb_errors=0
def diag(msg, force = False):
    global nb_errors
    if nb_errors > 0 or force:
        print msg
        nb_errors -= 1

def trace(t1, t2, status, out):
    if status:
        out.write("%s " % (abs(float(t2) - float(t1))))
    else:
        out.write("[%s(%s)] " % (float(t2), float(t1)))
        
def same_int(l1, l2, lnb, idx, out):
    i1 = l1.pop(0)
    i2 = l2.pop(0)
    status = False
    if int(i1) != int(i2):
        diag("value at pos %s of line %s are too different (%s vs %s)" % (idx, lnb, i1, i2))
    else:
        status = True
        trace(i1,i2,status,out)
    return status
            
def compare_floats(f1, f2, delta, lnb, idx, out, max_diff):
    status = False
    d = abs(float(f1) - float(f2))
    if d > delta:
        diag("value at pos %s of line %s are too different abs(%s-%s)==%s[>%s]" % (idx, lnb, 
                                                                                   f1, f2,
                                                                                   abs(float(f1)-float(f2)),
                                                                                   delta))
    else:
        status = True
    trace(f1,f2,status,out)
    if max_diff < d: max_diff = d
    return (status, max_diff)

def close_floats(l1, l2, delta, lnb, idx, out, max_diff):
    f1 = l1.pop(0)
    f2 = l2.pop(0)
    return compare_floats(f1, f2, delta, lnb, idx, out, max_diff)

def check_size(a1, a2, lnb, diff):
    if len(a1) != len(a2):
        diag("different number of token at line %s: %s instead of %s" % (lnb, len(a2), len(a1)))
        diff.writeln("%s token instead of %s" % (len(a2), len(a1)))
        return False;
    else:
        return True

def close_float_line(l1, l2, delta, lnb, diff, max_diff):
    a1 = l1.split()
    a2 = l2.split()
    status = False
    if check_size(a1,a2,lnb,diff):
        status = True
        nb = len(a1)
        for i in range(0, nb):
            s, max_diff = close_floats(a1,a2,delta,lnb,i,diff,max_diff)
            if not s:
                status = False
    diff.write('\n')
    return (status, max_diff)

def same_int_line(l1, l2, lnb, diff):
    a1 = l1.split()
    a2 = l2.split()
    status = False
    if check_size(a1,a2,lnb,diff):
        status = True
        nb = len(a1)
        for i in range(0, nb):
            if not same_int(a1,a2,lnb,i,diff):
                status = False
    diff.write('\n')
    return status

def get_pos_text(lpos, ipos):
    return "position %s of line %s" % (ipos,lpos)

def get_pos_text(lpos):
    return "position %s of line %s" % lpos

def compare_smesh(gold,test,trace,allowed=None):
    lineno = 0
    ghdr = gold.readline().split()
    thdr = test.readline().split()
    lineno += 1
    close_enough = True
    max_diff = 0.0

    if not check_size(ghdr, thdr, 0, diff):
        close_enough = False
    else:
        for i in range(0,3):
            if not same_int(ghdr, thdr, 0, i, diff):
                close_enough = False
        for i in range(3,5):
            s, max_diff = close_floats(ghdr, thdr, 0.05, 0, i, diff, max_diff)
            if not s:
                close_enough = False
        diff.write('\n')
        if not close_enough:
            diag("max in header: %s" % max_diff, True)
    max_diff = 0.0
    for i in range(0,2):
        s, max_diff = close_float_line(gold.readline(), test.readline(), 0, lineno, diff, max_diff)
        if not s:
            close_enough = False
        lineno += 1
    if not close_enough:
        diag("max in xy pos: %s" % max_diff, True)
    max_diff = 0.0
    if not allowed: allowed = 0.001
    for i in range(0,11):
        s, max_diff = close_float_line(gold.readline(), test.readline(), 0.001, lineno, diff, max_diff)
        if not s:
            close_enough = False
        lineno += 1
    if not close_enough:
        diag("max diff in top 11 lines: %s" % max_diff, True)

    glines = gold.readlines()
    tlines = test.readlines()
    if len(glines) != len(tlines):
        diag("Different number of lines", True)
        close_enough = False
    else:
        max_diff = 0.0
        for gline, tline in zip(glines,tlines):
            s, max_diff = close_float_line(gline, tline, 0.05, lineno, diff, max_diff)
            if not s:
                close_enough = False
            lineno += 1
        diag("max diff in end of file: %s" % max_diff, True)
    return close_enough

def compare_refl(gold,test,trace):
    lineno = 0
    ghdr = gold.readline()
    thdr = test.readline()
    close_enough = True
    if not same_int_line(ghdr, thdr, lineno, trace):
        close_enough = False
    lineno += 1

    glines = gold.readlines()
    tlines = test.readlines()

    if len(glines) != len(tlines):
        diag("Different number of lines", True)
        close_enough = False
    else:
        max_diff = 0
        for gline, tline in zip(glines,tlines):
            s, max_diff = close_float_line(gline, tline, 0.002, lineno, diff, max_diff)
            if not s:
                close_enough = False
            lineno += 1
        diag("max diff: %s" % max_diff, True)
    return close_enough

def get_ray_line_sequence(f):
    line = f.readline()
    if not line:
        return None
    else:
        if line.startswith('>'): # first line
           return get_ray_line_sequence(f)
        else:
            s = []
            while True:
                l = f.readline()
                if not l: # last line
                    break
                elif l.startswith('>'): # end of seq
                    break
                else:
                    s.append(l)
            return s
    
def compare_ray(gold,test,trace):
    lineno = 1
    seqno = 0
    close_enough = True
    max_diff = 0.0
    while True:
        trace.write("> %s\n" % seqno)
        seqno += 1
        gseq = get_ray_line_sequence(gold)
        tseq = get_ray_line_sequence(test)
        if (not gseq) != (not tseq):
            diag("Different number of sequences", True)
            close_enough = False
        elif (not gseq) and (not tseq):
            break
        else:
            if len(gseq) != len(tseq):
                diag("Different number of lines", True)
                close_enough = False
            else:
                for gline, tline in zip(gseq,tseq):
                    s, max_diff = close_float_line(gline, tline, 0.001, lineno, diff, max_diff)
                    if not s:
                        close_enough = False
                    lineno += 1
        lineno += 1 # skip '>'
    diag("max diff: %s" % max_diff, True)
    return close_enough

def compare_tres(gold,test,trace,allowed=None):
    lineno = 0
    close_enough = True
    glines = gold.readlines()
    tlines = test.readlines()
    if not allowed:
        allowed=0.001
    if len(glines) != len(tlines):
        diag("Different number of lines", True)
        close_enough = False
    else:
        s, first_max_diff =  close_float_line(glines.pop(0), tlines.pop(0), allowed, lineno, diff, 0)
        if not s:
            close_enough = False
        max_diff = 0.0
        for gline, tline in zip(glines,tlines):
            s, max_diff = close_float_line(gline, tline, allowed, lineno, diff, max_diff)
            if not s:
                close_enough = False
            lineno += 1
    diag("max diff first line: %s\nmax diff rest of file: %s" % (first_max_diff,max_diff), True)
    return close_enough

def compare_log(gold,test,trace,nb_relaxed):
    glines = gold.readlines()
    tlines = test.readlines()
    close_enough = True
    lineno = 0
    
    for gline, tline in zip(glines, tlines):
        lineno += 1
        gtokens = gline.split()
        ttokens = tline.split()
        if gtokens[0] == ttokens[0] and gtokens[0][0] == '#':
            continue
        max_diff = 0.0
        if not compare_floats(gtokens[3],  ttokens[3],  0.001, lineno, 3, diff, max_diff)[0]:
            close_enough = False
        if not compare_floats(gtokens[4],  ttokens[4],  0.05, lineno, 4, diff, max_diff)[0]:
            close_enough = False
        if not compare_floats(gtokens[6],  ttokens[6],  0.001, lineno, 6, diff, max_diff)[0]:
            close_enough = False
        if not compare_floats(gtokens[7],  ttokens[7],  0.05, lineno, 7, diff, max_diff)[0]:
            close_enough = False
        if not compare_floats(gtokens[9], ttokens[9], 0.001, lineno, 9, diff, max_diff)[0]:
            close_enough = False
        if not compare_floats(gtokens[10], ttokens[10], 0.05, lineno, 10, diff, max_diff)[0]:
            close_enough = False
        diff.write('\n')
        if nb_relaxed > 0:
            nb_relaxed -= 1
            if not close_enough:
                print " Tolerated"
                close_enough = True
    return close_enough

usage = "%prog <gold path> <test path>"
parser = OptionParser(usage=usage)

print "Command line: ",
for w in sys.argv: print "%s " %w,
print

parser.add_option("-m", "--max-diff", dest="max_diff",
                  action="store", type="float", default=0.001,
                  help="The maximmun authorized difference")
parser.add_option("--format", dest="format",
                  action="store", type="str", metavar="FORMAT",
                  help="Compare according to format FORMAT (can be any of %s). If not provided, will try to extract from the name of the file" % repr(FORMATS) )
parser.add_option("--nb-errors", dest="nb_errors",
                  action="store", type="int", metavar="NB", default=200,
                  help="The maximum number of error to print, all of them if 0 (default: 200)")
parser.add_option("--nb-relaxed", dest="nb_relaxed",
                  action="store", type="int", metavar="NB", default=2,
                  help="Mismatch on the firt NB significant lines will be tolerated. (default 2)")
parser.add_option("--diff", dest="diff_path",
                  action="store", type="str", metavar="FILE",
                  help="Print the differences in file FILE (default: stdout).")

(options, args) = parser.parse_args()

if options.nb_errors > 0:
    nb_errors = options.nb_errors

if len(args) < 2:
    print parser.print_help()
    exit(1)

goldpath = os.path.abspath(args[0])
testpath = os.path.abspath(args[1])
    
if not os.path.isfile(goldpath):
    print "must be an existing file: ", args[0]
    exit(1)
if not os.path.isfile(testpath):
    print "must be an existing file: ", args[1]
    exit(1)

gold = open(goldpath, "r")
test = open(testpath, "r")
diff = sys.stdout
if options.diff_path:
    path = os.path.abspath(options.diff_path)
    diff = open(path, "w")
    if not diff:
        print "could not open '%s'" %path

close_enough = False

if not options.format:
    if args[0].find(SMESH)  != -1: options.format = SMESH
    elif args[0].find(REFL) != -1: options.format = REFL
    elif args[0].find(RAY)  != -1: options.format = RAY
    elif args[0].find(TRES) != -1: options.format = TRES
    elif args[0].endswith(LOG): options.format = LOG
    else:
        print "cannot determine format"
        exit(1)

if options.format == "smesh":
    close_enough = compare_smesh(gold,test,diff,options.max_diff)
elif options.format == "refl":
    close_enough = compare_refl(gold,test,diff)
elif options.format == "ray":
    close_enough = compare_ray(gold,test,diff)
elif options.format == "tres":
    close_enough = compare_tres(gold,test,diff,options.max_diff)
elif options.format == "log":
    close_enough = compare_log(gold,test,diff,options.nb_relaxed)
else:
    print "unsupported format '%s'" % options.format
    exit(1)

if close_enough:
    exit(0)
else:
    exit(1)
