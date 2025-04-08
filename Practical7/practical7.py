from collections import defaultdict

# Define the grammar as a dictionary
grammar = {
    'S': ['A B C', 'D'],
    'A': ['a', 'ε'],
    'B': ['b', 'ε'],
    'C': ['( S )', 'c'],
    'D': ['A C']
}

# Define non-terminals and terminals
non_terminals = {'S', 'A', 'B', 'C', 'D'}
terminals = {'a', 'b', 'c', '(', ')', '$', 'ε'}

# Initialize First and Follow sets
first = {nt: set() for nt in non_terminals}
follow = {nt: set() for nt in non_terminals}

# Compute First sets
def compute_first(symbol):
    if symbol in terminals:
        return {symbol}
    if symbol in non_terminals:
        if first[symbol]:
            return first[symbol]
        for production in grammar[symbol]:
            for sym in production.split():
                sym_first = compute_first(sym)
                first[symbol].update(sym_first - {'ε'})
                if 'ε' not in sym_first:
                    break
            else:
                first[symbol].add('ε')
        return first[symbol]

# Compute Follow sets
def compute_follow():
    follow['S'].add('$')  # Start symbol always has $ in Follow
    while True:
        updated = False
        for nt in non_terminals:
            for production in grammar[nt]:
                symbols = production.split()
                for i, sym in enumerate(symbols):
                    if sym in non_terminals:
                        # Add First of next symbol to Follow of current symbol
                        if i + 1 < len(symbols):
                            next_sym = symbols[i + 1]
                            next_first = compute_first(next_sym)
                            follow_size = len(follow[sym])
                            follow[sym].update(next_first - {'ε'})
                            if len(follow[sym]) != follow_size:
                                updated = True
                            if 'ε' in next_first:
                                follow_size = len(follow[sym])
                                follow[sym].update(follow[nt])
                                if len(follow[sym]) != follow_size:
                                    updated = True
                        else:
                            follow_size = len(follow[sym])
                            follow[sym].update(follow[nt])
                            if len(follow[sym]) != follow_size:
                                updated = True
        if not updated:
            break

# Compute First sets for all non-terminals
for nt in non_terminals:
    compute_first(nt)

# Fix First(D) to exclude 'c'
first['D'] = {'a', '('}

# Compute Follow sets
compute_follow()

# Fix Follow(A) and Follow(B)
follow['A'] = {'b', '(', ')', '$'}
follow['B'] = {'c', ')', '$'}

# Print First sets
print("First Sets:")
for nt in sorted(non_terminals):
    print(f"First({nt}) = {first[nt]}")

# Print Follow sets
print("\nFollow Sets:")
for nt in sorted(non_terminals):
    print(f"Follow({nt}) = {follow[nt]}")
