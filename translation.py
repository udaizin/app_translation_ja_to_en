import re

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from functools import partial
from transformers import pipeline
from transformers.trainer_utils import set_seed


set_seed(42)

# load model and tokenizer
model_name = 'udaizin/sonoisa_t5_base_ja_en_translator_jsec_kftt'
tokenizer = AutoTokenizer.from_pretrained(model_name, keep_accents=True)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# create translation pipeline
fixed_model_pipeline = partial(
    pipeline,
    task='translation',
    model=model,
    tokenizer=tokenizer
)

'''
Translate text from Japanese to English.
:param text: Japanese text
:return: List of English translations
'''
def translate(text):
    translate_pipeline = fixed_model_pipeline(
        num_beams=3,
        num_return_sequences=3,
        do_sample=True,
        temperature=0.6,
        top_k=10,
        max_length=300,
    )
    results = [result['translation_text'] for result in translate_pipeline(text)]
    postprocess(results)

    return results

'''
postprocess the translation results
'''
def postprocess(results):
    # replace 'i' with 'I'
    itoI_dict = {'i': 'I', 
                 "i'm": "I'm", 
                 "i've": "I've", 
                 "i'll": "I'll", 
                 "i'd": "I'd"
                 }
    for i, result in enumerate(results):
        for key, value in itoI_dict.items():
            results[i] = re.sub(r'\b' + key + r'\b', value, results[i])
    
    # change the beginning of a sentence to uppercase
    beginning_sentence_pattern = r'^([a-z])|(?<=\.)\s+([a-z])'
    for i, result in enumerate(results):
        results[i] = re.sub(beginning_sentence_pattern, lambda x: x.group().upper(), results[i])



