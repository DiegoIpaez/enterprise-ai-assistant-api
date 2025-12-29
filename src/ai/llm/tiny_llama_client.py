import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


class TinyLlamaClient:
    """
    LLM mínimo para RAG estable en Mac M1.
    """

    _instance = None
    _model = None
    _tokenizer = None

    _model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def initialize(self):
        if self._model is not None:
            return

        torch.set_num_threads(2)

        self._tokenizer = AutoTokenizer.from_pretrained(self._model_name)

        if self._tokenizer.pad_token is None:
            self._tokenizer.pad_token = self._tokenizer.eos_token

        self._model = AutoModelForCausalLM.from_pretrained(
            self._model_name,
            torch_dtype=torch.float32,
            low_cpu_mem_usage=True,
        )

        self._model.eval()

    def generate(self, prompt: str, max_new_tokens: int = 64) -> str:
        inputs = self._tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=384,
        )

        with torch.no_grad():
            output = self._model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=False,
                use_cache=False,
                pad_token_id=self._tokenizer.eos_token_id,
            )

        return self._tokenizer.decode(
            output[0][inputs["input_ids"].shape[1]:],
            skip_special_tokens=True,
        ).strip()
