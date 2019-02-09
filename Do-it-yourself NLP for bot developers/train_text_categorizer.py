import sys, os
from mitie import *

trainer = text_categorizer_trainer("/path/to/total_word_feature_extractor.dat")

data = {} # same as before  - omitted for brevity

for label in training_examples.keys():
  for text in training_examples[label]["examples"]:
    tokens = tokenize(text)
    trainer.add_labeled_text(tokens,label)
    
trainer.num_threads = 4
cat = trainer.train()

cat.save_to_disk("my_text_categorizer.dat")

# we can then use the categorizer to predict on new text
tokens = tokenize("somewhere that serves chinese food")
predicted_label, _ = cat(tokens)
