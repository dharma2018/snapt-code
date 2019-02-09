import sys, os
from mitie import *
sample = ner_training_instance(["I", "am", "looking", "for", "some", "cheap", "Mexican", "food", "."])

sample.add_entity(xrange(5,6), "pricerange")
sample.add_entity(xrange(6,7), "cuisine")

# And we add another training example
sample2 = ner_training_instance(["show", "me", "indian", "restaurants", "in", "the", "centre", "."])
sample2.add_entity(xrange(2,3), "cuisine")
sample2.add_entity(xrange(6,7), "area")


trainer = ner_trainer("/path/to/total_word_feature_extractor.dat")

trainer.add(sample)
trainer.add(sample2)

trainer.num_threads = 4

ner = trainer.train()

ner.save_to_disk("new_ner_model.dat")


# Now let's make up a test sentence and ask the ner object to find the entities.
tokens = ["I", "want", "expensive", "korean", "food"]
entities = ner.extract_entities(tokens)


print "\nEntities found:", entities
print "\nNumber of entities detected:", len(entities)
for e in entities:
    range = e[0]
    tag = e[1]
    entity_text = " ".join(tokens[i] for i in range)
    print "    " + tag + ": " + entity_text
    
# output 
# >>> Number of entities detected: 2
# >>>     pricerange: expensive
# >>>     cuisine: korean
