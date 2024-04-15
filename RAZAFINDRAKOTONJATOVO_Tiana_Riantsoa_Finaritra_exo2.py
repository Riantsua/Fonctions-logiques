_parenthesize_variables = False


def implicant_premier(term_arr):
    return_arr = []
    for term1 in term_arr:
        for term2 in term_arr:
            if term1 != term2:
                similar_indexes = [idx for idx in range(len(term1)) if (term1[idx] == term2[idx])]
                if len(term1) - len(similar_indexes) <= 1:
                    tmp = combine(term1, term2)
                    if tmp not in return_arr:
                        return_arr.append(tmp)
    return return_arr


def combine(implicant1, implicant2):
    return_arr = []
    for idx in range(len(implicant1)):
        if implicant1[idx] == implicant2[idx]:
            return_arr.append(implicant1[idx])
        else:
            return_arr.append("-")
    return return_arr


def est_derive(a, b):
    for bit_idx in range(len(a)):
        if a[bit_idx] != b[bit_idx] and a[bit_idx] != "-":
            return False
    return True


def supp_redondance(term_arr):
    new_list = []
    for term1_idx in range(len(term_arr)):
        if term_arr[term1_idx] not in new_list:
            new_list.append(term_arr[term1_idx])
    indexes_to_remove = []
    for term1_idx in range(len(new_list)):
        for term2_idx in range(len(new_list)):
            if term1_idx != term2_idx and est_derive(new_list[term1_idx], new_list[term2_idx]):
                indexes_to_remove.append(term2_idx)
    indexes_to_remove = list(dict.fromkeys(indexes_to_remove))
    indexes_to_remove.sort()
    for idx in reversed(range(len(indexes_to_remove))):
        del new_list[indexes_to_remove[idx]]
    return new_list


def colonne(prime_implicant):
    if "-" not in prime_implicant:
        return [prime_implicant]
    col = []
    idx = prime_implicant.index("-")
    for bit in (['0', '1']):
        tmp = prime_implicant.copy()
        tmp[idx] = bit
        arr = colonne(tmp)
        for k in arr:
            col.append(k)
    return col


def tableau_redondance(minterms):
    chart = []
    for i in range(len(minterms)):
        chart.append(colonne(minterms[i]))
    return chart


def minterme_tableau(chart):
    all_minterms = []
    for row in chart:
        for item in row:
            if item not in all_minterms:
                all_minterms.append(item)
    return all_minterms


def convertir_string(minterms, var_list):
    output = ''
    for minterm in minterms:
        for bit_idx in range(len(minterm)):
            if minterm[bit_idx] != "-":
                output += '(' if _parenthesize_variables else ''
                output += "!" if minterm[bit_idx] == '0' else ''
                output += var_list[bit_idx]
                output += ')' if _parenthesize_variables else ''
                output += "."
        if "." == output[-len("."):]:
            output = output[:-len(".")]
        if minterm != minterms[-1]:
            output += " + "
    return output


def factoriser(minterms, var_list):
    common = ["-"] * len(minterms[0])
    if len(minterms) > 1:
        for bit in range(len(minterms[0])):
            for term in range(1, len(minterms)):
                if minterms[0][bit] != minterms[term][bit] or minterms[term][bit] == "-":
                    break
                elif term == len(minterms) - 1:
                    common[bit] = minterms[term][bit]
                    for k in range(len(minterms)):
                        minterms[k][bit] = "-"
    common = convertir_string([common], var_list)
    return common


def simplifier(minterms, var_list=[]):
    if len(minterms) == 0:
        raise Exception("Insufficient minterm count")
    var_count = len(bin(max(minterms))) - 2
    if len(var_list) == 0:
        var_list = list(map(chr, range(65, 65 + var_count)))
    elif len(var_list) >= var_count:
        var_count = len(var_list)
    else:
        raise Exception("Insufficient variable count")

    for i in range(len(minterms)):
        minterms[i] = list(bin(int(minterms[i]))[2:].zfill(var_count))

    prime_implicants = implicant_premier(minterms)
    while len(prime_implicants) != 0:
        for prime_implicant in prime_implicants:
            minterms.append(prime_implicant)
        prime_implicants = implicant_premier(prime_implicants)

    minterms = supp_redondance(minterms)

    chart = tableau_redondance(minterms)
    all_minterms = sorted(minterme_tableau(chart))

    redundant_indexes = []
    for i in range(len(chart)):
        tmp_chart = []
        for k in range(len(chart)):
            if (k != i) and (k not in redundant_indexes):
                 tmp_chart.append(chart[k])
        if sorted(minterme_tableau(tmp_chart)) == all_minterms:
            redundant_indexes.append(i)

    for idx in reversed(range(len(redundant_indexes))):
        del minterms[redundant_indexes[idx]]

    multiples = factoriser(minterms, var_list)

    output = convertir_string(minterms, var_list)

    if multiples != '()':
        output = multiples + "." + '(' + output + ')'
    return output


def evaluer(fonc, var_dict):
	fonc = fonc.replace("+", " or ")
	fonc = fonc.replace(".", " and ")
	fonc = fonc.replace("!", " not ")

	for variable, value in var_dict.items():
		fonc = fonc.replace(variable, str(value))

	return eval(fonc)


def liste_variables(fonc):
	return sorted(set(filter(str.isalpha, fonc)))


def mintermes(fonc):
	fonc = fonc.upper()

	resultats = []
	var = liste_variables(fonc)
	var_count = len(var)

	tab = []
	for i in range(2 ** var_count):
		b = list(bin(i)[2:].zfill(var_count))
		tab.append(b)

	for i in range(len(tab)):
		value_dict = dict(zip(var, tab[i]))
		result = evaluer(fonc, value_dict)
		if result:
			resultats.append(i)

	return resultats, var


def main():
	fonc = input("Veuillez entrer fonction à minimiser: ")
	resultats, var = mintermes(fonc)
	print("Fonction minimale:\n\t", simplifier(resultats, var))


if __name__ == "__main__":
	main()
