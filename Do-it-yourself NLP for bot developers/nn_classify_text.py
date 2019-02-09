import numpy as np

def sum_vecs(embed,text):

    tokens = text.split(' ')
    vec = np.zeros(embed.W.shape[1])

    for idx, term in enumerate(tokens):
        if term in embed.vocab:
            vec = vec + embed.W[embed.vocab[term], :]
    return vec


def get_centroid(embed,examples):

    C = np.zeros((len(examples),embed.W.shape[1]))
    for idx, text in enumerate(examples):
        C[idx,:] = sum_vecs(embed,text)

    centroid = np.mean(C,axis=0)
    assert centroid.shape[0] == embed.W.shape[1]
    return centroid


def get_intent(embed,text):
    intents = ['deny', 'inform', 'greet']
    vec = sum_vecs(embed,text)
    scores = np.array([ np.linalg.norm(vec-data[label]["centroid"]) for label in intents ])
    return intents[np.argmin(scores)]


embed = Embedding('/path/to/vocab','/path/to/vectors')


data={
  "greet": {
    "examples" : ["hello","hey there","howdy","hello","hi","hey","hey ho"],
    "centroid" : None
  },
  "inform": {
    "examples" : [
      "i'd like something asian",
      "maybe korean",
      "what mexican options do i have",
      "what italian options do i have",
      "i want korean food",
      "i want german food",
      "i want vegetarian food",
      "i would like chinese food",
      "i would like indian food",
      "what japanese options do i have",
      "korean please",
      "what about indian",
      "i want some vegan food",
      "maybe thai",
      "i'd like something vegetarian",
      "show me french restaurants",
      "show me a cool malaysian spot"
    ],
    "centroid" : None
  },
  "deny": {
    "examples" : [
      "nah",
      "any other places ?",
      "anything else",
      "no thanks"
      "not that one",
      "i do not like that place",
      "something else please",
      "no please show other options"
    ],
    "centroid" : None
  }
}


for label in data.keys():
    data[label]["centroid"] = get_centroid(embed,data[label]["examples"])


for text in ["hey you","i am looking for chinese food","not for me"]:
    print "text : '{0}', predicted_label : '{1}'".format(text,get_intent(embed,text))

# output
# >>>text : 'hey you', predicted_label : 'greet'
# >>>text : 'i am looking for chinese food', predicted_label : 'inform'
# >>>text : 'not for me', predicted_label : 'deny'
