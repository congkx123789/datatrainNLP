import os
import json
import torch
from torch.utils.data import Dataset
from transformers import (
    AutoTokenizer, 
    AutoModelForSeq2SeqLM, 
    Seq2SeqTrainingArguments, 
    Seq2SeqTrainer,
    DataCollatorForSeq2Seq
)

# Constants
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
PROCESSED_DIR = os.path.join(DATA_DIR, 'processed')
OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'models', 'constrained_mt_model'))

class ConstrainedTranslationDataset(Dataset):
    def __init__(self, filepath, tokenizer, max_length=128):
        self.data = []
        self.tokenizer = tokenizer
        self.max_length = max_length
        
        # Load dataset
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Dataset file not found at {filepath}")
            
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                item = json.loads(line)
                # We use the zh_tagged sentence as input and vi as output target
                self.data.append((item['zh_tagged'], item['vi']))
                
    def __len__(self):
        return len(self.data)
        
    def __getitem__(self, idx):
        src_text, trg_text = self.data[idx]
        
        # Tokenize source
        model_inputs = self.tokenizer(
            src_text, 
            max_length=self.max_length, 
            truncation=True, 
            padding=False
        )
        
        # Tokenize target
        labels = self.tokenizer(
            text_target=trg_text, 
            max_length=self.max_length, 
            truncation=True, 
            padding=False
        )
        
        model_inputs["labels"] = labels["input_ids"]
        return model_inputs

def main():
    model_name = "Helsinki-NLP/opus-mt-zh-vi"
    print(f"Loading base model and tokenizer: {model_name}...")
    
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    
    # Add special tokens for constraints mapping
    # Register both source POS placeholders and target index placeholders
    special_tokens = [
        "<1|nr>", "<2|nr>", "<1|ns>", "<2|ns>", "<3|d>", "<4|a>", "<5|n>", "<1|nt>", "<2|n>", "<1|n>",
        "<1>", "<2>", "<3>", "<4>", "<5>", "<6>", "<7>", "<8>", "<9>", "<10>"
    ]
    num_added_toks = tokenizer.add_tokens(special_tokens)
    print(f"Added {num_added_toks} special tokens to the tokenizer.")
    
    # Resize the model embeddings matrix to fit the new tokens
    model.resize_token_embeddings(len(tokenizer))
    
    # Load processed data
    dataset_path = os.path.join(PROCESSED_DIR, "train_constrained.jsonl")
    print(f"Loading dataset from {dataset_path}...")
    
    # For training validation, we'll split the dataset
    full_dataset = ConstrainedTranslationDataset(dataset_path, tokenizer)
    
    # If the dataset is small (like our 9-sentence prototype), we train on all of it.
    # In a real run, split 90/10 for train/eval.
    train_size = int(0.9 * len(full_dataset))
    eval_size = len(full_dataset) - train_size
    
    if eval_size > 0:
        train_dataset, eval_dataset = torch.utils.data.random_split(
            full_dataset, [train_size, eval_size]
        )
    else:
        train_dataset = full_dataset
        eval_dataset = full_dataset
        
    print(f"Dataset loaded. Train size: {len(train_dataset)}, Eval size: {len(eval_dataset)}")
    
    # Collator handles padding dynamically for batch processing
    data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)
    
    # Training Arguments (Optimized for Colab GPU T4)
    training_args = Seq2SeqTrainingArguments(
        output_dir=OUTPUT_DIR,
        eval_strategy="epoch" if eval_size > 0 else "no",
        learning_rate=3e-5,                  # Fine-tuning learning rate
        per_device_train_batch_size=16,       # Batch size per device
        per_device_eval_batch_size=16,
        weight_decay=0.01,
        save_total_limit=2,
        num_train_epochs=30,                  # Train for 30 epochs on CPU for quick demo
        predict_with_generate=True,
        fp16=torch.cuda.is_available(),      # Enable half-precision (FP16) training if GPU is present
        logging_steps=10,
        save_strategy="no",                  # Don't save checkpoints during overfit run
        report_to="none"                     # Disable wandb logging to keep it simple
    )
    
    # Initialize Trainer
    trainer = Seq2SeqTrainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        data_collator=data_collator,
        processing_class=tokenizer
    )
    
    print("\n--- Starting Model Training / Fine-tuning ---")
    trainer.train()
    
    print(f"\nTraining completed! Saving model and tokenizer to {OUTPUT_DIR}...")
    trainer.save_model(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)
    print("Save complete! Ready for local execution.")

if __name__ == "__main__":
    main()
