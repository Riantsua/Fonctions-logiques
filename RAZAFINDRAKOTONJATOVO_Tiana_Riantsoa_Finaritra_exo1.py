def evaluer(fonc, var_dict):
	fonc = fonc.replace("+", " or ")
	fonc = fonc.replace(".", " and ")
	fonc = fonc.replace("!", " not ")

	for variable, value in var_dict.items():
		fonc = fonc.replace(variable, str(value))

	return eval(fonc)


def liste_variables(fonc):
	return sorted(set(filter(str.isalpha, fonc)))


def table_verite(fonc):
	fonc = fonc.upper()

	resultats = []
	var = liste_variables(fonc)
	var_count = len(var)
	print(" | ".join(var + ["" + fonc]))
	print("-" * (len(fonc) + 3 * (len(var) + 2)))

	tab = []
	for i in range(2 ** var_count):
		b = list(bin(i)[2:].zfill(var_count))
		tab.append(b)

	for values in tab:
		value_dict = dict(zip(var, values))
		result = evaluer(fonc, value_dict)
		resultats.append(result)
		value_str = " | ".join(str(v) for v in values)
		print(f" | ".join([value_str, str(int(result))]))

	return resultats, var


def forme_disjonctive(resultats, var):
	var_count = len(var)
	var = sorted(list(var))
	tab = []
	for i in range(2 ** var_count):
		b = list(bin(i)[2:].zfill(var_count))
		tab.append(b)
	tmp = str()
	dcf = str()

	for i in range(len(resultats)):
		if resultats[i]:
			for j in range(len(var)):
				tmp += str(tab[i][j])
				if j < len(var) - 1:
					tmp += "."

			if i < len(resultats) - 1:
				tmp += " + "

	tmp = tmp.split(" + ")
	for i in range(len(tmp)):
		t = tmp[i]
		tmp2 = "("
		tsize = len(t)
		for j in range(tsize):
			if t[j] == '1':
				tmp2 += var[(j >> 1)]
			elif t[j] == '0':
				tmp2 += "!" + var[(j >> 1)]
			else:
				tmp2 += "."
		dcf += tmp2 + ")"
		if i != len(tmp) - 1:
			dcf += " + "

	dcf = dcf.replace("+ ()", "")
	return dcf


def forme_conjonctive(resultats, var):
	var = sorted(list(var))
	var_count = len(var)
	tab = []
	for i in range(2 ** var_count):
		b = list(bin(i)[2:].zfill(var_count))
		tab.append(b)
	tmp = str()
	ccf = str()

	for i in range(len(resultats)):
		if resultats[i] == 0:
			for j in range(len(var)):
				tmp += str(tab[i][j])
				if j != len(var) - 1:
					tmp += "+"

			if i < len(resultats) - 1:
				tmp += " . "

	tmp = tmp.split(" . ")
	for i in range(len(tmp)):
		t = tmp[i]
		tmp2 = "("
		tsize = len(t)
		for j in range(tsize):
			if t[j] == '1':
				tmp2 += "!" + var[(j >> 1)]
			elif t[j] == '0':
				tmp2 += var[(j >> 1)]
			else:
				tmp2 += " + "
		ccf += tmp2 + ")"
		if i != len(tmp) - 1:
			ccf += "."

	ccf = ccf.replace(".()", "")
	return ccf


def main():
	fonc = input("Veuillez entrer une fonction logique (ex: A + !(B.C)): ")
	print("\nTable de verite")
	resultats, var = table_verite(fonc)

	print("\nPremière forme canonique:")
	print("\t", forme_disjonctive(resultats, var))
	print("\nDeuxième forme canonique:")
	print("\t", forme_conjonctive(resultats, var))


if __name__ == "__main__":
	main()
