from node import Node

# Rules of the grammar 
L1 = {
    "S": [["NP", "VP"],["X1","VP"],["book"],["include"],["prefer"],["Verb","NP"],["X2","PP"],["Verb","PP"],["VP","PP"]],
    "NP": [["Det","Nominal"],["I"],["she"],["me"],["TWA"],["Houston"]],
    "Nominal": [["Nominal","Noun"],["Nominal","PP"],["book"],["flight"],["meal"],["money"],["morning"]],
    "VP": [["Verb","NP"],["Verb","PP"],["VP","PP"],["book"],["include"],["prefer"],["X2","PP"]],
    "PP": [["Preposition","NP"]],
    "X1": [["Aux","NP"]],
    "X2": [["Verb","NP"]],
    "Det": [["that"],["this"],["a"],["the"]],
    "Noun": [["book"],["flight"],["meal"],["money"],["morning"]],
    "Verb":[["book"],["include"],["prefer"]],
    "Aux": [["does"]],
    "Preposition": [["from"],["to"],["on"],["near"],["through"]]
}

Toy = {
    "S": [["NP", "VP"]],
    "VP": [["V","NP"],["VP","ADV"]],
    "V": [["ama"]],
    "NP":[["Paolo"],["Francesca"]],
    "ADV":[["dolcemente"]]
}

Dothraki = {
    "S": [["NP", "VP"],["X1","VP"],["VP","PP"], ["NP","NP"], ["NP","JJ"]],
    "X1": [["Aux","NP"]],
    "Aux": [["hash"]],
    "VP": [["VP","NP"],["VP","ADV"],["astoe"],["dothrak"],["zhilak"],["dothrae"],["VP","PP"],["ittesh"],["VP","Pron"],["nesak"]],
    "PP": [["Preposition","NP"]],
    "NP":[["anha"],["yera"],["yer"],["Dothraki"],["NP","ADV"],["mahrazh"],["mori"],["lajakis"],["NP","JJ"], ["lajak"]],
    "Preposition": [["ki"]],
    "ADV":[["chek"],["ADV","ADV"],["asshekh"]],
    "JJ":[["ivezhi"],["JJ,JJ"],["mori"],['gavork']],
    "Pron":[["haz"]]
}

s1 = ['Paolo','ama','Francesca','dolcemente']
s2 = ['book','the','flight','through','Houston']
s3 = ['does', 'she', 'prefer', 'a', 'morning', 'flight']
s4 = ['anha', 'zhilak', 'yera'] #I love you
s5 = ['hash', 'yer', 'astoe', 'ki', 'Dothraki'] #Do you speak Dothraki?
s6 = ['anha','gavork'] #I'm hungry
s7 = ['mahrazh','lajak'] #"The man is a warrior."
s8 = ['hash','yer','dothrae','chek','asshekh'] #Do you ride well today?
s9 = ['anha','dothrak','chek','asshekh'] #I fell well today
s10 = ['mori', 'ittesh', 'lajakis','ivezhi','mori'] #They tested their wild warriors.
s11 = ['anha', 'nesak', 'haz'] #I know that!


def parser(grammar,sentence):

    syntax_tree = CKY(grammar,sentence)
    printTrees(syntax_tree)


def CKY(R,s):

    n = len(s)
    table = [[set([]) for j in range(n + 1)] for i in range(n + 1)]
    nodes = [[set([]) for i in range(n + 1)] for j in range(n + 1)]

    for j in range(1, n + 1): 
            
        # Iterate over the rules 
        for left, rule in R.items(): 
            for right in rule: 
                
                if len(right) == 1 and right[0] == s[j - 1]:                                                ## { A -> words[j] in grammar}
                    table[j - 1][j].add(left)                                                               ## {table[j - 1, j] = A}
                    nodes[j - 1][j].add(Node(left, None, None, s[j - 1]))
                   
        for i in reversed(range(0, j - 1)):                
            for k in range(i + 1, j):      

                # Iterate over the rules 
                for left, rule in R.items(): 
                    for right in rule: 
                        
                                if len(right) == 2 and right[0] in table[i][k] and right[1] in table[k][j]:     ## {A | A -> BC, B in table[i,k], C in table [k,j]}        
                                    table[i][j].add(left)

                                
                                    for b in nodes[i][k]:
                                        for c in nodes[k][j]:
                                            if b.root == right[0] and c.root == right[1]:
                                                nodes[i][j].add(Node(left, b, c, None))
                                
                                
    print()                            
    for i in range(n):
        _str = ''.join(str(t) for t in (table[i]))
        _str_ = _str.replace("set()"," None ")
        print(_str_[5:])

    if (table[0][n]).__contains__('S'):
        print() 
        print("----------------------- True -----------------------")
        print() 
    else: 
        print("----------------------- False -----------------------") 

    return nodes[0][n]

def printTrees(nodes_back):
	check = False
	for node in nodes_back:
		if node.root == 'S':
			print(getParseTree(node, 3))
			print()
			check = True

	if not check:
		print('The given sentence is not valid according to the grammar.')

def getParseTree(root, indent):
	"""
	getParseTree() takes a root and constructs the tree in the form of a
	string. 
	"""
	if root.status:
		return '(' + root.root + ' ' + root.terminal + ')'

	# Calculates the new indent factors that we need to pass forward.
	new1 = indent + 2 + len(root.left.root) #len(tree[1][0])
	new2 = indent + 2 + len(root.right.root) #len(tree[2][0])
	left = getParseTree(root.left, new1)
	right = getParseTree(root.right, new2)
	return '(' + root.root + ' ' + left + '\n' \
			+ ' '*indent + right + ')'


if __name__ == '__main__':
   parser(L1,s3)


