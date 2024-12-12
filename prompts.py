merge_prompt="""Task: Compare the terms "{action}" and "{potential}" within the context of {attribute_type}.  

If the terms overlap, are synonyms, or can be unified into a single concept, they should be merged. If they are distinct in meaning or usage, they should be kept separate.  

Output:  
- Decision: [Merge / Keep Separate]  
- Rationale: Briefly explain your reasoning (1-2 sentences). If they overlap or are synonymous, explain why they can be merged. If they are distinct, clarify why they should be kept separate.  
- Recommended Term: If merged, recommend the term that best represents both, either one of the original terms or a new term that encompasses both. If separate, state "None".
"""