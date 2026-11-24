
def search4letters(phrase: str, letters: str = 'ATCG') -> set:
    """
    Return the set of target letters found in a supplied phrase.
    """
    return set(letters).intersection(set(phrase))



print("TASK 1: DNA MARKER SEARCH")

print("Positional Arguments:",
      search4letters('TGGACC', 'GC'))

print("Keyword Arguments:",
      search4letters(letters='CG', phrase='TGGACC'))

print("Default Arguments:",
      search4letters('TGGACC'))




def analyze_sequence(sequence_list, marker):

    print("\nInside Function (Start) - ID:",
          id(sequence_list), "| Data:", sequence_list)

    
    sequence_list.append(marker)

    print("Inside Function (End) - ID:",
          id(sequence_list), "| Data:", sequence_list)



print("\nTASK 2: MEMORY REFERENCES")

dna_database = ['AATCCG', 'TGGCTA']

print("Global Scope (Before) - ID:",
      id(dna_database), "| Data:", dna_database)

analyze_sequence(dna_database, 'CGAT')

print("Global Scope (After) - ID:",
      id(dna_database), "| Data:", dna_database)


# TASK 3: Slice Experiment

print("\nTASK 3: SLICE EXPERIMENT")

dna_database = ['AATCCG', 'TGGCTA']

print("Global Scope (Before) - ID:",
      id(dna_database), "| Data:", dna_database)

analyze_sequence(dna_database[:], 'CGAT')

print("Global Scope (After) - ID:",
      id(dna_database), "| Data:", dna_database)




def analyze_sequence_rebind(sequence_list, marker):

    print("\nInside (Start) - ID:", id(sequence_list))

   
    sequence_list = sequence_list + [marker]

    print("Inside (End) - ID:",
          id(sequence_list), "| Data:", sequence_list)


print("\nTASK 4: REASSIGNMENT")

dna_database = ['AATCCG', 'TGGCTA']

print("Global Scope (Before) - ID:",
      id(dna_database), "| Data:", dna_database)

analyze_sequence_rebind(dna_database, 'CGAT')

print("Global Scope (After) - ID:",
      id(dna_database), "| Data:", dna_database)




print("\nTASK 5: EDGE CASES")


print("Empty Phrase:", search4letters(''))


print("Mixed Arguments:",
      search4letters('TGGACC', letters='GC'))


dna_database = ['AATCCG', 'TGGCTA']

analyze_sequence(dna_database[:], 'CGAT')
analyze_sequence(dna_database[:], 'ATCG')

print("Original Database After Repeated Slices:",
      dna_database)
