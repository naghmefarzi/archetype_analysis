
def get_response_baseline(prompt: str,pipeline,system_message:str):
  messages = [
      {"role": "system", "content": system_message},
      {"role": "user", "content": prompt},
  ]
  
  
  # Check if the function has been called before
  if not hasattr(get_response_baseline, "called"):
  # Set the attribute to indicate the function has been called
    get_response_baseline.called = True
    # print(messages)

  prompt = pipeline.tokenizer.apply_chat_template(
          messages,
          tokenize=False,
          add_generation_prompt=True
  )

  terminators = [
      pipeline.tokenizer.eos_token_id,
      pipeline.tokenizer.convert_tokens_to_ids("<|eot_id|>")
  ]

  outputs = pipeline(
      prompt,
      max_new_tokens=1000,
      eos_token_id=terminators,
      pad_token_id=128009,
      do_sample=True,
      temperature=0.1,
      top_p=0.9,
  )

  return outputs[0]["generated_text"][len(prompt):]

