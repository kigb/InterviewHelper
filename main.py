import whisper
from utils.speech2text import speech2text
from utils.translation import translate_cn_to_en
from transformers import AutoTokenizer, AutoModelForCausalLM, TextIteratorStreamer
import transformers
import torch

# prepare log file
log_file = "tmp/result.md"

def log_message(message, is_code=False):
    with open(log_file, "a") as log:
        if is_code:
            log.write(f"```\n{message}\n```\n")
        else:
            log.write(message + "\n\n")

# prepare the model
log_message("# Loading models...")
api_key = "3cda741a-a328-4ebd-a687-05462dd804b4:fx"
tokenizer = AutoTokenizer.from_pretrained("Nan-Do/LeetCodeWizard_7B_V1.1")
model = AutoModelForCausalLM.from_pretrained("Nan-Do/LeetCodeWizard_7B_V1.1").to("cuda:1")
speech_model = whisper.load_model("turbo")

# prepare the pipeline
pipeline = transformers.pipeline(
    "text-generation",
    model=model,
    torch_dtype=torch.float16,
    device="cuda:0",
    tokenizer=tokenizer,
)

log_message("## Models loaded. Waiting for user input...")

while True:
    input("Press Enter to process the next speech input...")

    # recognize the speech
    log_message("### Recognizing speech...")
    question = speech2text("recordings/reverse_list.m4a", speech_model)

    # translate the question
    log_message("### Translating the question...")
    chinese_text = question
    english_translation = translate_cn_to_en(chinese_text, api_key)
    log_message("#### Translated question: " + english_translation)

    # generate the code
    log_message("### Generating answer...")
    instruction = english_translation
    prompt = f"Below is an instruction that describes a task. Write a **code** and **algorithm** for response that appropriately completes the request.\n\n### Instruction:\n{instruction}\n\n### Response:"

    # Streaming code generation
    streamer = TextIteratorStreamer(tokenizer, skip_special_tokens=True)

    generation = model.generate(
        tokenizer(prompt, return_tensors="pt").input_ids.to("cuda:0"),
        streamer=streamer,
        do_sample=False,
        eos_token_id=tokenizer.eos_token_id,
        max_length=500,
    )

    log_message("#### Answer:")
    with open(log_file, "a") as log:
        # log.write("```\n")
        for token in streamer:
            log.write(token)
            print(token, end="", flush=True)
        # log.write("\n```\n")