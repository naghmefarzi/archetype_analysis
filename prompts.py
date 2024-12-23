merge_prompt="""Task: Compare the terms "{action}" and "{potential}" within the context of {attribute_type}.  

If the terms overlap, are synonyms, or can be unified into a single concept, they should be merged. If they are distinct in meaning or usage, they should be kept separate.  

Output:  
- Decision: [Merge / Keep Separate]  
- Rationale: Briefly explain your reasoning (1-2 sentences). If they overlap or are synonymous, explain why they can be merged. If they are distinct, clarify why they should be kept separate.  
- Recommended Term: If merged, recommend the term that best represents both, either one of the original terms or a new term that encompasses both. If separate, state "None".
"""
extract_feature_prompt = """Analyze the given short story and identify the character "{character}"'s primary {attribute_type}. 
Please provide exactly 5 concise {attribute_type}s in a list format. Each {attribute_type} should be ONLY a single or double word, without any specific names, descriptions, or extra text.

**Short story:**
{short_story}

Output:
1. {attribute_type} 1
2. {attribute_type} 2
3. {attribute_type} 3
...
"""

extract_features_with_global_list_prompt = """Analyze the given short story and identify the character "{character}"'s primary {attribute_type}. 
Please provide exactly 5 concise attributes in a list format. Each attribute should be a single or double word, without any specific names, descriptions, or extra text.
Use the provided "{attribute_type}" list as a guide, but suggest a new "{attribute_type}" if it better fits the character's actions and motivations within the story.

**Short story:**
"{short_story}"

**"{attribute_type}" list:**
{role_list}


Output:
1. {attribute_type} 1
2. {attribute_type} 2
3. {attribute_type} 3
...
"""

extract_characters_prompt = """Identify only the main significant characters in the following story and return only their names in a list format, without any additional text or description:

{short_story}

Output:
- Character 1
- Character 2
- Character 3
...
"""

