import wikipedia
import pickle

def get_topics():
	index_dict = "package/20topics_nmf_laspositas.sav"

	with open(index_dict, 'rb') as filehandle:
		indices = pickle.load(filehandle)
	indices.values.T.tolist()
	return [list(l) for l in zip(*indices.values)]

def get_definition(topic):
	try:
		results = wikipedia.search(topic)
		page = results[0]
		summary = wikipedia.summary(page, sentences = 1)
	except wikipedia.exceptions.DisambiguationError as e:
		print('here')
		return e.options
	return summary




topics = get_topics()[1:]
first_three = list(map(lambda x: x[:3], topics))

for topic in first_three:
	t = topic[0] + " " + topic[1] + " " + topic[2]
	print(t)
	print(get_definition(t))
	print('xxxxxxxxxxxxxxxxxxxxx')
	print('\n')
	print('\n')
	print('\n')
	# print(topic[0], ":     ", get_definition(topic[0]))
	# print(topic[1], ":     ", get_definition(topic[1]))
	# print(topic[2], ":     ", get_definition(topic[2]))
	# print('xxxxxxxxxxxxxxxxxxxxx')
	# print('\n')
	# print('\n')
	# print('\n')


