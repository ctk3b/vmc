ref = "TCTCAGCAGCATCT"

# T|C|T|C|A|G|C|A|G|C|A|T|C|T
#  |---| ⇒ A 

def trim_left(alleles):
    """remove common prefix from left of all alleles, returning
    [number_trimmed, new_alleles]

    >>> trim_left(["","AA"])
    (0, ['', 'AA'])
    >>> trim_left(["A","AA"])
    (1, ['', 'A'])
    >>> trim_left(["AT","AA"])
    (1, ['T', 'A'])
    >>> trim_left(["AA","AA"])
    (2, ['', ''])

    """
    trimmed = 0
    while all(len(a) > 0 for a in alleles):
        a0 = alleles[0]
        for a in alleles[1:]:
            if a0[0] != a[0]:
                return trimmed, alleles
        alleles = [a[1:] for a in alleles]
        trimmed += 1
    return trimmed, alleles

def print_seq(seq):
    p = "{:15s}".format("")
    print(p + "|" + "|".join(list(seq)) + "|")

def print_allele(pos, allele):
    start, end = pos
    pfx = "[{:2d},{:2d})".format(start,end)
    p = "{:15s}".format(pfx)
    pos_str = p + "  "*(start) + "|"
    if end > start:
        pos_str += "—" + "——"*(end-start-1) + "|"
    print(pos_str + " ⇒ " + allele)
    
def normalize(ref, pos, allele):
    """
    
    >>> normalize(ref, (3,3), "CAG")
    ((11, 11), 'GCA')
    >>> normalize(ref, (4,4), "AGC")
    ((11, 11), 'GCA')
    >>> normalize(ref, (3,6), "")
    ((8, 11), '')
    >>> normalize(ref, (3,7), "C")
    ((8, 11), '')
    >>> normalize(ref, (3,8), "CA")
    ((8, 11), '')

    """
    start, end = pos
    ref_allele = ref[start:end]

    print_seq(ref)
    print_allele(pos, allele)
    
    # remove common prefix and advance start
    trimmed, alleles = trim_left([ref_allele, allele])
    ref_allele, allele = alleles
    start += trimmed
    
    while True:
        print_allele((start, end), allele)
        #print(start,end, [ref_allele, allele])
        if end == len(ref):
            break
        next_residue = ref[end:end+1]
        trimmed, alleles = trim_left([ref_allele + next_residue, allele + next_residue])
        #print(trimmed, alleles)
        if trimmed == 0:
            break
        allele_len_change = len(allele)
        ref_allele, allele = alleles
        start += trimmed
        end += trimmed
    return ((start, end), allele)


if __name__ == "__main__":
    tests = [
        ((3,3), "CAG"),
        ((4,4), "AGC"),
        ((3,6), ""),
        ((3,7), "C"),
        ((3,8), "CA"),
    ]
    for t in tests:
        print("* " + str(t))
        print(normalize(ref, *t))
    