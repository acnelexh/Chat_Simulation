from transformers import GPT2LMHeadModel, GPT2Tokenizer, Trainer, TrainingArguments

# Load pre-trained model and tokenizer
model = GPT2LMHeadModel.from_pretrained('gpt2')
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')

new_tokens = ['[A]', '[B]'] + ['[' + emotion + ']' for emotion in lookup]
tokenizer.add_tokens(new_tokens)

# Tokenize and encode your formatted data
encoded_dialogues = tokenizer('dd_examples_all.txt', return_tensors='pt', padding=True, truncation=True)

# Define training arguments
training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=3,
    per_device_train_batch_size=4,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir='./logs',
)

# Initialize the Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=encoded_dialogues,
)

# Train the model
trainer.train()

# Save the fine-tuned model
model.save_pretrained('./fine_tuned_model')
