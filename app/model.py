from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch

model_id = "defog/sqlcoder-7b-2"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
).to(device)

generator = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    device=0 if torch.cuda.is_available() else -1,
    return_full_text=False,
    max_new_tokens=256
)

def generate_sql(prompt: str) -> str:
    output = generator(prompt, do_sample=False)[0]["generated_text"]
    return output.strip()
