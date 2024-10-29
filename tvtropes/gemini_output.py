
from absl.testing import absltest
import google.generativeai as genai
import os
import pathlib
import re
import json


genai.configure(api_key=os.environ["GEMINI_API_KEY"])



class UnitTests(absltest.TestCase):
    def test_text_gen_text_only_prompt(self,prompt:str):
        # [START text_gen_text_only_prompt]
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        # print(response.text)
        return response.text
        # [END text_gen_text_only_prompt]

def find_archtypes(ut,text:str, prompt:str):
    jungian_archetypes = [
        "The Innocent",
        "The Orphan/Everyman",
        "The Hero",
        "The Caregiver",
        "The Explorer",
        "The Rebel",
        "The Lover",
        "The Creator",
        "The Jester",
        "The Sage",
        "The Magician",
        "The Ruler"
    ]
    c_prompt = prompt+f"\nPlease choose from this list of archtypes: {jungian_archetypes}"+"\nStory:\n"+short_story
    archtype_response = ut.test_text_gen_text_only_prompt(c_prompt)
    return archtype_response
    
    

if __name__ == "__main__":
    ut = UnitTests()
    with open('./archetype_analysis.jsonl', 'w') as jsonl_file:
        for i in range(10):
            prompt = "Write a short story about a typical day in someone's life."
            short_story = ut.test_text_gen_text_only_prompt(prompt)
            print(short_story)
            prompt = "Can you identify any Jungian archetypes present in this story?"
            archtype_response = find_archtypes(ut,short_story, prompt)
            print(archtype_response)
            archetype_pattern = r'\*\s+\*\*(.*?):\*\*'
            archetype_names = re.findall(archetype_pattern, archtype_response)
            print(archetype_names)
            
            # Creating a dictionary to hold the responses
            data = {
                "short_story": short_story,
                "archetype_response": archtype_response,
                "archetype_names": archetype_names
            }

            jsonl_file.write(json.dumps(data) + '\n')

    
    # absltest.main()