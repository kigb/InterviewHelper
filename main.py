import whisper
from utils.speech2text import speech2text
from transformers import pipeline
from transformers import AutoModelForCausalLM, AutoTokenizer, AutoConfig
speech_model = whisper.load_model("turbo")
question = speech2text("utils/test.mp3", speech_model)

device = "cuda:0" if torch.cuda.is_available() else "cpu"
tokenizer = AutoTokenizer.from_pretrained("codellama/CodeLlama-7b-Instruct-hf")
model = AutoModelForCausalLM.from_pretrained("codellama/CodeLlama-7b-Instruct-hf").to(device)
# Create a pipeline
code_generator = pipeline('text-generation', model=model, tokenizer=tokenizer)
# Generate code for an input string
input_string = f"[INST]{question}[/INST]"
generated_code = code_generator(input_string, max_length=100)[0]['generated_text']
print(generated_code)