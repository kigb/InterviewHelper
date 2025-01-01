import whisper
from utils.speech2text import speech2text
from utils.translation import translate_cn_to_en
from transformers import AutoTokenizer, AutoModelForCausalLM
import transformers
import torch

# prepare log file
log_file = "tmp/result.log"

def log_message(message):
    with open(log_file, "a") as log:
        log.write(message + "\n")

# prepare the model
log_message("Loading models...")
api_key = "3cda741a-a328-4ebd-a687-05462dd804b4:fx"
tokenizer = AutoTokenizer.from_pretrained("Nan-Do/LeetCodeWizard_7B_V1.1")
model = AutoModelForCausalLM.from_pretrained("Nan-Do/LeetCodeWizard_7B_V1.1").to("cuda:1")
speech_model = whisper.load_model("turbo")

# recognize the speech
log_message("Recognizing speech...")
question = speech2text("recordings/reverse_list.m4a", speech_model)

# translate the question
log_message("Translating the question...")
chinese_text = question
english_translation = translate_cn_to_en(chinese_text, api_key)
log_message("Translated question: " + english_translation)

# generate the code
log_message("Generating answer...")
instruction = english_translation
prompt = f"Below is an instruction that describes a task. Write a **code** and **algorithm** for response that appropriately completes the request.\n\n### Instruction:\n{instruction}\n\n### Response:"
pipeline = transformers.pipeline(
    "text-generation",
    model=model,
    torch_dtype=torch.float16,
    device="cuda:0",
    tokenizer=tokenizer,
)

sequences = pipeline(
    prompt,
    do_sample=False,
    num_return_sequences=1,
    eos_token_id=tokenizer.eos_token_id,
    max_length=500,
)
for seq in sequences:
    log_message(f"Answer:")
    log_message(f"{seq['generated_text'][len(prompt):]}")