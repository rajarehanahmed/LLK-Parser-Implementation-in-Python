def find_terminals_n_non_terminals():
    f = open('Example.txt', 'r')
    terminals = []
    non_terminals = []
    ch = f.read(1)
    while ch:
        if not ch.isupper() and not ch == '=' and not ch == '~' and not ch == '|' and not ch == '\n' and ch not in terminals:
            terminals.append(ch)
        ch = f.read(1)
    f.seek(0)
    lines = f.readlines()
    for line in lines:
        non_terminals.append(line[0])
    f.close()
    return terminals, non_terminals


def is_epsilon_present(line):
    for ch in line:
        if ch == '~':
            return True
    return False


def is_bar_present(line, start_index):
    i = start_index
    while i < len(line):
        if line[i] == '|':
            return i
        i = i + 1
    return -1


def is_symbol_present(line, start_index, symbol):
    i = start_index
    while i < len(line):
        if line[i] == symbol:
            return i
        i = i + 1
    return -1


def get_first_set(first_sets, symbol):
    first = []
    for line in first_sets:
        if line[0] == symbol:
            i = 2
            while i < len(line):
                first += line[i]
                i = i + 1
    return first


def get_follow_set(follow_sets, symbol):
    follow = []
    for line in follow_sets:
        if line[0] == symbol:
            i = 2
            while i < len(line):
                follow += line[i]
                i = i + 1
    return follow


def add_distinct(container, inp):
    for ch in inp:
        if ch not in container:
            container += ch
    return container

def calculate_first_sets(terminals, non_terminals):
    first_sets = []
    for terminal in terminals:
        first_sets.append(terminal + '=' + terminal)
    for symbl in non_terminals:
        string_set = ''
        first_of_symbl = first_set(symbl, terminals, non_terminals)
        for char in first_of_symbl:
            string_set += char
        first_sets.append(symbl + '=' + string_set)
    return first_sets


def first_set(symbol, terminals, non_terminals):
    f = open('Example.txt', 'r')
    lines = f.readlines()
    production = ''
    for line in lines:
        if line[0] == symbol:
            production = line
            break
    first_of_symbol = []
    if len(production) != 0:
        i = 2
        ch = production[i]
        while True:
            if ch in terminals or ch == '~':
                if ch not in first_of_symbol:
                    first_of_symbol += ch
                index_bar = is_bar_present(production, i)
                if index_bar == -1:
                    break
                else:
                    i = index_bar + 1
            elif ch in non_terminals:
                sub_first = first_set(ch, terminals, non_terminals)
                if not is_epsilon_present(sub_first):
                    first_of_symbol = add_distinct(first_of_symbol, sub_first)
                    # first_of_symbol += sub_first
                    index_bar = is_bar_present(production, i)
                    if index_bar == -1:
                        break
                    else:
                        i = index_bar + 1
                elif is_epsilon_present(sub_first):
                    sub_first.remove('~')
                    first_of_symbol = add_distinct(first_of_symbol, sub_first)
                    # first_of_symbol += sub_first
                    if production[i + 1] == '|':
                        i += 2
                    elif len(production) == i + 1:
                        break
                    else:
                        i = i + 1
            ch = production[i]
    f.close()
    return first_of_symbol


def calculate_follow_sets(first_sets, terminals, non_terminals):
    follow_sets = []
    for non_terminal in non_terminals:
        string_set = ''
        if non_terminal == non_terminals[0]:
            string_set += '$'
        follow_of_symbol = follow_set(non_terminal, first_sets, terminals, non_terminals)
        for char in follow_of_symbol:
            string_set += char
        # print(non_terminal + '=' + string_set)
        follow_sets.append(non_terminal + '=' + string_set)
    return follow_sets


def follow_set(symbol, first_sets, terminals, non_terminals):
    f = open('Example.txt', 'r')
    lines = f.readlines()
    follow_of_symbol = []
    for line in lines:
        index_symbol = is_symbol_present(line, 2, symbol)
        if index_symbol != -1:
            i = index_symbol + 1
            # print(i)
            # print('line length:', end=' ')
            # print(len(line))
            # input('Press Enter to Continue')
            while True:
                # input('Press Enter to Continue')
                if i == len(line) - 1:
                    # print('i==len(line)')
                    if line[0] == non_terminals[0]:
                        follow_of_symbol += '$'
                    follow_of_symbol = add_distinct(follow_of_symbol,
                                                    follow_set(line[0], first_sets, terminals, non_terminals))
                    # follow_of_symbol += follow_set(line[0], first_sets, terminals, non_terminals)
                    # print(follow_of_symbol)
                    # input('Press Enter to Continue')
                    break
                elif line[i] == '|':
                    # print('line[i]==|')
                    follow_of_symbol = add_distinct(follow_of_symbol,
                                                    follow_set(line[0], first_sets, terminals, non_terminals))
                    # follow_of_symbol += follow_set(line[0], first_sets, terminals, non_terminals)
                    index_symbol = is_symbol_present(line, i + 1, symbol)
                    if index_symbol == -1:
                        break
                    else:
                        i = index_symbol + 1
                        # print(i)
                else:
                    sub_first = get_first_set(first_sets, line[i])
                    if not is_epsilon_present(sub_first):
                        # print('Epsilon Not Present')
                        follow_of_symbol = add_distinct(follow_of_symbol, sub_first)
                        # follow_of_symbol += sub_first
                        # print(follow_of_symbol)
                        # input('Press Enter to Continue')
                        index_bar = is_symbol_present(line, i + 1, '|')
                        if index_bar == -1:
                            break
                        else:
                            index_symbol = is_symbol_present(line, index_bar + 1, symbol)
                            if index_symbol == -1:
                                break
                            else:
                                i = index_symbol + 1
                                # print(i)
                    else:
                        # print('Epsilon Present')
                        sub_first.remove('~')
                        follow_of_symbol = add_distinct(follow_of_symbol, sub_first)
                        # follow_of_symbol += sub_first
                        # print(follow_of_symbol)
                        # input('Press Enter to Continue')
                    i = i + 1
    f.close()
    return follow_of_symbol


def individual_first_set(production, first_sets, terminals, non_terminals):
    first = []
    i = 0
    while True:
        if production[i] in terminals or production[i] == '~':
            first += production[i]
            break
        elif production[i] in non_terminals:
            sub_first = get_first_set(first_sets, production[i])
            # print(sub_first)
            if not is_epsilon_present(sub_first):
                first += sub_first
                break
            elif is_epsilon_present(sub_first):
                sub_first.remove('~')
                first += sub_first
                if i == len(production) - 1:
                    break
        i = i + 1
    # print(first)
    # input('Press Enter to Continue')
    return first


def make_m_table(first_sets, follow_sets, terminals, non_terminals):
    f = open('Example.txt', 'r')
    lines = f.readlines()
    table = [[-1 for i in range(len(terminals) + 1)] for j in range(len(non_terminals))]
    # for line in table:
    #     print(line)
    prod_count = 1  #Production Count
    line_count = 1  #Line Count
    for line in lines:
        i = 2
        prod = ''
        while True:
            if line[i] == '|':
                # print(prod_count)
                first = individual_first_set(prod, first_sets, terminals, non_terminals)
                # print(line_count - 1)
                if '~' in first:
                    first.remove('~')
                    for element in first:
                        # print(terminals.index(element), end=' ')
                        # print(element)
                        table[line_count - 1][terminals.index(element)] = prod_count
                    follow = get_follow_set(follow_sets, line[0])
                    for element in follow:
                        if element == '$':
                            table[line_count - 1][len(terminals)] = prod_count
                        else:
                            # print(terminals.index(element), end=' ')
                            # print(element)
                            table[line_count - 1][terminals.index(element)] = prod_count
                else:
                    for element in first:
                        # print(terminals.index(element), end=' ')
                        # print(element)
                        table[line_count - 1][terminals.index(element)] = prod_count
                prod_count = prod_count + 1
                prod = ''
            elif i == len(line) - 1:
                # print(prod_count)
                first = individual_first_set(prod, first_sets, terminals, non_terminals)
                # print(line_count - 1)
                if '~' in first:
                    first.remove('~')
                    for element in first:
                        # print(terminals.index(element), end=' ')
                        # print(element)
                        table[line_count - 1][terminals.index(element)] = prod_count
                    follow = get_follow_set(follow_sets, line[0])
                    for element in follow:
                        if element == '$':
                            table[line_count - 1][len(terminals)] = prod_count
                        else:
                            # print(terminals.index(element), end=' ')
                            # print(element)
                            table[line_count - 1][terminals.index(element)] = prod_count
                else:
                    for element in first:
                        # print(terminals.index(element), end=' ')
                        # print(element)
                        table[line_count - 1][terminals.index(element)] = prod_count
                prod_count = prod_count + 1
                break
            else:
                prod += line[i]
            i = i + 1
        line_count = line_count + 1
    f.close()
    return table


def parse(inp_string, table, terminals, non_terminals):
    f = open('Example.txt', 'r')
    lines = f.readlines()
    rules = []
    # Separating productions i.e. 1 production on each line
    for line in lines:
        if '|' not in line:
            rules.append(line.replace('\n', ''))
        else:
            i = 2
            rule = ''
            while True:
                if i == len(line) - 1:
                    rules.append(line[0] + '=' + rule)
                    break
                elif line[i] == '|':
                    rules.append(line[0] + '=' + rule)
                    i = i + 1
                    rule = ''
                else:
                    rule += line[i]
                    i = i + 1
    print(rules)
    stack = ['$']
    stack.append(non_terminals[0])
    inp_string += '$'
    X = stack[len(stack) - 1]
    print(inp_string)
    a = inp_string[0]

    while True:
        print('Input :', end=' ')
        print(inp_string)
        print('Stack :', end=' ')
        print(stack)
        input('Press Enter to Continue')
        if X == a == '$':
            print('Parsing Successful.')
            break
        elif X in terminals:
            if X == a:
                print('match', end=' ')
                print('X : ', end=' ')
                print(X, end=' ')
                print('a :', end=' ')
                print(a)
                inp_string = inp_string.replace(a, '', 1)
                a = inp_string[0]
                stack.pop()
                X = stack[len(stack) - 1]
            else:
                print('not matched: ', end=' ')
                print(X + a)
                print('Error...!')
                break
        elif X in non_terminals:
            if a == '$':
                rule_no = mTable[non_terminals.index(X)][len(terminals)]
            elif a in terminals:
                rule_no = mTable[non_terminals.index(X)][terminals.index(a)]
            else:
                print('Invalid Symbol : ', end=' ')
                print(a)
                break

            if rule_no == -1:
                print('Error at: ', end=' ')
                print('Stack :', end=' ')
                print(X, end=' ')
                print('Input :', end=' ')
                print(a)
                break
            else:
                stack.pop()
                rule = rules[rule_no - 1]
                print(rule)
                input('Press Enter to Continue')
                if '~' not in rule:
                    for i in range(len(rule) - 2):
                        stack.append(rule[len(rule) - 1 - i])
                X = stack[len(stack) - 1]
        else:
            print('Error...!')
            break
    f.close()


if __name__ == '__main__':
    file = open('Example.txt', 'r')
    terminals, nonTerminals = find_terminals_n_non_terminals()
    firstSets = calculate_first_sets(terminals, nonTerminals)
    followSets = calculate_follow_sets(firstSets, terminals, nonTerminals)
    mTable = make_m_table(firstSets, followSets, terminals, nonTerminals)
    while True:
        print('*_*_*_*_* LL(1) Parser *_*_*_*_*\n'
              '1. View the grammar.\n'
              '2. View the Terminals.\n'
              '3. View the Non Terminals.\n'
              '4. View the First Sets.\n'
              '5. View the Follow Sets.\n'
              '6. View the M Table.\n'
              '7. Parse a Sample String.\n'
              '8. Exit.\n'
              '--Please Enter your Choice: ')
        choice = input()
        if choice == '1':
            print(file.read())
        elif choice == '2':
            print('Terminals :', end=' ')
            for symbol in terminals:
                print(symbol, end=' ')
            print()
        elif choice == '3':
            print('Non Terminals :', end=' ')
            for symbol in nonTerminals:
                print(symbol, end=' ')
            print()
        elif choice == '4':
            print('First Sets:')
            for s in firstSets:
                print(s)
        elif choice == '5':
            print('Follow Sets:')
            for s in followSets:
                print(s)
        elif choice == '6':
            for line in mTable:
                print(line)
        elif choice == '7':
            sampleString = input('Enter the Sample String: ')
            parse(sampleString, mTable, terminals, nonTerminals)
        elif choice == '8':
            break
        else:
            print('Invalid Input...!')
    file.close()
