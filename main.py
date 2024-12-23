# from absl.testing import absltest
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted
from model_utils import get_model_baseline
import torch

import re
import json
import argparse
import random
import time
from google.api_core.exceptions import ResourceExhausted
from llm import get_response_baseline

import openai
from openai import OpenAI
from similarity import argmax_cosine_sim
import os
from prompts import merge_prompt, extract_feature_prompt, extract_features_with_global_list_prompt, extract_characters_prompt

# client = None




data = [
    {"Title": "Harry Potter and the Philosopher's Stone (film)", "Plot": "Late one night, Albus Dumbledore and Minerva McGonagall, professors at Hogwarts School of Witchcraft and Wizardry, along with groundskeeper Rubeus Hagrid, deliver an orphaned infant wizard named Harry Potter to his Muggle aunt and uncle, Petunia and Vernon Dursley, his only living relatives.\n\nTen years later, just before Harry's eleventh birthday, owls begin delivering letters addressed to him. When the abusive Dursleys adamantly refuse to allow Harry to open any and flee to an island hut, Hagrid arrives to personally deliver Harry's letter of acceptance to Hogwarts. Hagrid also reveals that Harry's late parents, James and Lily, were killed by a dark wizard named Lord Voldemort. The killing curse that Voldemort had cast towards Harry rebounded, destroying Voldemort's body and giving Harry the lightning-bolt scar on his forehead. Hagrid then takes Harry to Diagon Alley for school supplies and gives him a pet snowy owl whom he names Hedwig. Harry buys a wand that is connected to Voldemort's own wand.\n\nAt King's Cross, Harry boards the Hogwarts Express train, and meets fellow first-years Ron Weasley and Hermione Granger during the journey. Arriving at Hogwarts, Harry also meets Draco Malfoy, who is from a wealthy wizard family; the two immediately form a rivalry. The students assemble in the Great Hall where the Sorting Hat sorts the first-years into four respective houses: Gryffindor, Hufflepuff, Ravenclaw, and Slytherin. Harry is placed into Gryffindor alongside Ron and Hermione, while Draco is placed into Slytherin, a house noted for dark wizards.\n\nAs he studies magic, Harry learns more about his parents and Voldemort, and his innate talent for broomstick flying gets him recruited for the Gryffindor Quidditch team as the youngest Seeker in a century. While returning to the Gryffindor common room, the staircases change paths, leading Harry, Ron and Hermione to the third floor, which is forbidden to students. There they discover a giant three-headed dog named Fluffy. On Halloween, Ron insults Hermione after she shows off in Charms class. Upset, she spends the entire afternoon crying in the girls' bathroom. That evening, a giant marauding troll enters it but Harry and Ron save Hermione; they make up and become close friends after Hermione takes the blame for the incident by saying she went looking for the troll.\n\nThe trio discover that Fluffy is guarding the philosopher's stone, a magical object that can turn metal into gold and produce an immortality elixir. Harry suspects that Severus Snape, the Potions teacher and head of Slytherin, wants the stone to return Voldemort to physical form. When Hagrid accidentally reveals that music puts Fluffy to sleep, Harry, Ron and Hermione decide to find the stone before Snape. Fluffy is already asleep, but the trio face other barriers, including a deadly plant called Devil's Snare, a room filled with aggressive flying keys, and a giant chess game that knocks out Ron.\n\nAfter overcoming the barriers, Harry encounters Defence Against the Dark Arts teacher Quirinus Quirrell, who wants the stone; Snape had figured this out and had been protecting Harry. Quirrell removes his turban to reveal a weakened Voldemort living on the back of his head. Dumbledore's protective enchantment places the stone in Harry's possession. Voldemort attempts to bargain the stone from Harry in exchange for resurrecting his parents, but Harry sees through his trick and refuses. Quirrell attempts to kill Harry. When Harry touches Quirrell's skin, it burns Quirrell, reducing him to ashes. Voldemort's soul rises from the pile and escapes, knocking out Harry as it passes through him.\n\nHarry recovers in the school infirmary. Dumbledore tells him the stone has been destroyed to prevent misuse, and that Ron and Hermione are safe. He also reveals how Harry defeated Quirrell: when Lily died to save Harry, a love-based protection against Voldemort was placed on him. At the end-of-school-year feast, Harry, Ron, and Hermione are rewarded extra house points for their heroism, tying Gryffindor for first place with Slytherin; Dumbledore then awards ten points to their housemate Neville Longbottom for having had the courage to stand up to the trio, granting Gryffindor the House Cup. Harry returns to the Dursleys for the summer, happy to finally have a real home at Hogwarts.", "Characters": ["a baby.[10]", "the casting team asked for a meeting with him.[9]", "Hermione Granger: Harry's other best friend and the trio's brains. Watson's Oxford theatre teacher passed her name on to the casting agents and she had to do over five interviews before she got the part.[11] Watson took her audition seriously, but \"never really thought [she] had any chance of getting the role.\"[9] The producers were impressed by Watson's self-confidence and she outperformed the thousands of other girls who had applied.[12]", "Nearly Headless Nick: The ghost of Gryffindor House.[13]", "McGonagall.[14][15] Coltrane, who was already a fan of the books, prepared for the role by discussing Hagrid's past and future with Rowling.[16][17]", "Filius Flitwick: The Charms Master and head of Ravenclaw House.[18] Davis also plays two other roles in the film: the Goblin Head Teller at Gringotts,[19] and dubs the voice of Griphook, who is embodied by Verne Troyer.[20]", "Vernon Dursley: Harry's Muggle uncle.[19]", "Albus Dumbledore: Hogwarts' Headmaster and one of the most famous and powerful wizards of all time. Harris initially rejected the role, only to reverse his decision after his granddaughter stated she would never speak to him again if he did not take it.[21][22][23]", "a hooded figure during a flashback.[24][25]", "Mr. Ollivander: a highly regarded wandmaker and the owner of Ollivanders.[19]", "Severus Snape: The Potions Master and head of Slytherin House.", "Petunia Dursley: Harry's Muggle aunt.[19]", "Hagrid.[14]", "Molly Weasley: Ron's mother. She shows Harry how to get to Platform 9+3\u20444.[26]"]},
    {"Title":"A New Hope","Plot":"Amid a galactic civil war, Rebel Alliance spies have stolen plans to the Death Star, a colossal space station built by the Galactic Empire that is capable of destroying entire planets. Princess Leia Organa of Alderaan, secretly a Rebel leader, has obtained the schematics, but her ship is intercepted and boarded by Imperial forces under the command of Darth Vader. Leia is taken prisoner, but the droids R2-D2 and C-3PO escape with the plans, crashing on the nearby planet of Tatooine.The droids are captured by Jawa traders, who sell them to the moisture farmers Owen and Beru Lars and their nephew, Luke Skywalker. While Luke is cleaning R2-D2, he discovers a recording of Leia requesting help from a former ally named Obi-Wan Kenobi. R2-D2 goes missing, and while searching for him, Luke is attacked by Sand People. He is rescued by the elderly hermit Ben Kenobi, who soon reveals himself to be Obi-Wan. He tells Luke about his past as one of the Jedi Knights, former peacekeepers of the Galactic Republic, who drew mystical abilities from the Force but were hunted to near-extinction by the Empire. Luke learns that his father, also a Jedi, fought alongside Obi-Wan during the Clone Wars until Vader, Obi-Wan's former pupil, turned to the dark side of the Force and murdered him. Obi-Wan gives Luke his father's lightsaber, the signature weapon of the Jedi. R2-D2 plays Leia's full message, in which she begs Obi-Wan to take the Death Star plans to Alderaan and give them to her father, a fellow veteran, for analysis. Luke initially declines Obi-Wan's offer to accompany him to Alderaan and learn the ways of the Force, but he is left with no choice after Imperial stormtroopers murder his family while searching for the droids. Seeking a way off the planet, Luke and Obi-Wan travel to the city of Mos Eisley and hire Han Solo and Chewbacca, pilots of the starship Millennium Falcon. Before the Falcon reaches Alderaan, the Death Star commander Grand Moff Tarkin has the planet obliterated by the station's superlaser.[5] Upon arrival, the Falcon is captured by the Death Star's tractor beam, but the passengers avoid detection and infiltrate the station. As Obi-Wan leaves to deactivate the tractor beam, Luke persuades Han and Chewbacca to help him rescue Leia, who is scheduled for execution after refusing to reveal the location of the Rebel base. After disabling the tractor beam, Obi-Wan sacrifices himself in a lightsaber duel against Vader, which allows the rest of the group to escape. Using a tracking device placed on the Falcon, the Empire locates the Rebel base on the moon Yavin 4. Analysis of the Death Star schematics reveals a weakness in a small exhaust port leading directly to the station's reactor. Luke joins the Rebellion's X-wing squadron in a desperate attack against the Death Star, while Han and Chewbacca leave to pay off a debt to the crime lord Jabba the Hutt. In the ensuing battle, Vader leads a squadron of TIE fighters and destroys several Rebel ships. Han and Chewbacca unexpectedly return in the Falcon, knocking Vader's ship off course before he can shoot Luke down. Guided by the voice of Obi-Wan's spirit, Luke uses the Force to aim his torpedoes into the exhaust port, causing the Death Star to explode moments before it can fire on the Rebel base. In a triumphant ceremony, Leia awards Luke and Han medals for their heroism.","Characters": []},
    {"Title":"The Lord of the Rings: The Fellowship of the Ring","Plot":"In the Second Age of Middle-earth, the lords of Elves, Dwarves, and Men are given Rings of Power. Unbeknownst to them, the Dark Lord Sauron forges the One Ring in Mount Doom, instilling into it a great part of his power to dominate the other Rings and conquer Middle-earth. A final alliance of Men and Elves battles Sauron's forces in Mordor. Isildur of Gondor severs Sauron's finger and the Ring with it, thereby vanquishing Sauron and returning him to spirit form. With Sauron's first defeat, the Third Age of Middle-earth begins. The Ring's influence corrupts Isildur, who takes it for himself and is later killed by Orcs. The Ring is lost in a river for 2,500 years until it is found by Gollum, who owns it for over four and a half centuries. The Ring abandons Gollum and is subsequently found by a hobbit named Bilbo Baggins, who is unaware of its history. Sixty years later, Bilbo celebrates his 111th birthday in the Shire, reuniting with his old friend, the wizard Gandalf the Grey. Bilbo departs the Shire for one last adventure and leaves his inheritance, including the Ring, to his nephew Frodo. Gandalf investigates the Ring, discovers its true nature, and learns that Gollum was captured and tortured by Sauron's Orcs, revealing two words during his interrogation: 'Shire' and 'Baggins.' Gandalf returns and warns Frodo to leave the Shire. As Frodo departs with his friend, gardener Samwise Gamgee, Gandalf rides to Isengard to meet with the wizard Saruman but discovers his betrayal and alliance with Sauron, who has dispatched his nine undead Nazgûl servants to find Frodo. Frodo and Sam are joined by fellow hobbits Merry and Pippin, and they evade the Nazgûl before arriving in Bree, where they are meant to meet Gandalf at the Inn of The Prancing Pony. However, Gandalf never arrives, having been taken prisoner by Saruman. The hobbits are then aided by a Ranger named Strider, who promises to escort them to Rivendell; however, they are ambushed by the Nazgûl on Weathertop, and their leader, the Witch-King, stabs Frodo with a Morgul blade. Arwen, an Elf and Strider's beloved, locates Strider and rescues Frodo, summoning flood-waters that sweep the Nazgûl away. She takes him to Rivendell, where he is healed by the Elves. Frodo meets with Gandalf, who escaped Isengard on a Great Eagle. That night, Strider reunites with Arwen, and they affirm their love for each other. Learning of Saruman's betrayal from Gandalf and now realising that they are facing threats from both Sauron and Saruman, Arwen's father, Lord Elrond, decides against keeping the Ring in Rivendell. He holds a council of Elves, Men, and Dwarves, also attended by Frodo and Gandalf, that decides the Ring must be destroyed in the fires of Mount Doom. Frodo volunteers to take the Ring, accompanied by Gandalf, Sam, Merry, Pippin, the Elf Legolas, the Dwarf Gimli, Boromir of Gondor, and Strider—who is actually Aragorn, Isildur's heir and the rightful King of Gondor. Bilbo, now living in Rivendell, gives Frodo his sword Sting, and a chainmail shirt made of mithril. The Company of the Ring makes for the Gap of Rohan, but discover it is being watched by Saruman's spies. They instead set off over the mountain pass of Caradhras, but Saruman summons a storm that forces them to travel through the Mines of Moria, where a tentacled water beast blocks off the entrance with the Company inside, giving them no choice but to journey to the exit on the other end. After finding the Dwarves of Moria dead, the Company is attacked by Orcs and a cave troll. They hold them off but are confronted by Durin's Bane: a Balrog residing within the mines. While the others escape, Gandalf fends off the Balrog and casts it into a vast chasm, but the Balrog drags Gandalf down into the darkness with him. The devastated Company reaches Lothlórien, ruled by the Elf-queen Galadriel, who privately informs Frodo that only he can complete the quest and that one of the Company will try to take the Ring. She also shows him a vision of the future in which Sauron succeeds in enslaving Middle-earth, including the Shire. Meanwhile, Saruman creates an army of Uruk-hai in Isengard to find and destroy the Company. The Company travels by river to Parth Galen. Frodo wanders off and is confronted by Boromir, who, as Lady Galadriel had warned, tries to take the Ring. Uruk-hai scouts then ambush the Company, attempting to abduct the Hobbits. Boromir breaks free of the Ring's power and protects Merry and Pippin, but the Uruk-Hai leader, Lurtz, mortally wounds Boromir as they abduct the Hobbits. Aragorn arrives and kills Lurtz before comforting Boromir as he dies, promising to help the people of Gondor in the coming conflict. Fearing the Ring will corrupt his friends, Frodo decides to travel to Mordor alone, but allows Sam to come along, recalling his promise to Gandalf to look after him. As Aragorn, Legolas, and Gimli set out to rescue Merry and Pippin, Frodo and Sam make their way down the pass of Emyn Muil, journeying on to Mordor.","Characters":[]},
    {"Title": "The Matrix", "Plot": "At an abandoned hotel, a police squad corners Trinity, who overpowers them with superhuman abilities. She flees, pursued by the police and a group of suited Agents capable of similar superhuman feats. She answers a ringing public telephone and vanishes.\n\nComputer programmer Thomas Anderson, known by his hacking alias \'Neo\', is puzzled by repeated online encounters with the phrase \'the Matrix\'. Trinity contacts him and tells him a man named Morpheus has the answers Neo seeks. A team of Agents and police, led by Agent Smith, arrives at Neo's workplace in search of Neo. Though Morpheus attempts to guide Neo to safety, Neo surrenders rather than risk a dangerous escape. The Agents offer to erase Neo's criminal record in exchange for his help with locating Morpheus, who they claim is a terrorist. When Neo refuses to cooperate, they fuse his mouth shut, pin him down, and implant a robotic \'bug\' in his abdomen. Neo wakes up from what he believes to be a nightmare. Soon after, Trinity takes Neo to meet Morpheus, and she removes the bug from Neo.\n\nMorpheus offers Neo a choice between two pills: red to reveal the truth about the Matrix or blue to make Neo forget everything and return to his former life. Neo takes the red pill, and his reality begins to distort until he awakens in a liquid-filled pod among countless other pods, containing other humans. He is then brought aboard Morpheus's flying ship, the Nebuchadnezzar. As Neo recuperates from a lifetime of physical inactivity in the pod, Morpheus explains the history: in the early 21st century, humanity had developed intelligent machines before war broke out between the two sides. After humans blocked the machines' access to solar energy, the machines responded by enslaving humankind and harvesting their bioelectric power while keeping their minds pacified in the Matrix, a shared simulated reality modeled on the world as it was in 1999. In the years following, the remaining free humans took refuge in the underground city of Zion.\n\nMorpheus and his crew are a group of rebels who hack into the Matrix to \'unplug\' enslaved humans and recruit them; their understanding of the Matrix's simulated nature allows them to bend its physical laws. Morpheus warns Neo that death within the Matrix kills the physical body too and explains that the Agents are sentient programs that eliminate threats to the system, while machines called Sentinels eliminate rebels in the real world. Neo's prowess during virtual training cements Morpheus's belief that Neo is \'the One\', a human prophesied to free humankind. The group enters the Matrix to visit the Oracle, a prophet-like program who predicted that the One would emerge. She implies to Neo that he is not the One and warns that he will have to choose between Morpheus's life and his own. Before they can leave the Matrix, Agents and police ambush the group, tipped off by Cypher, a disgruntled crew member who has betrayed Morpheus in exchange for a deal to be plugged back into the Matrix to live a comfortable life.\n\nTo buy time for the others, Morpheus fights Smith and is captured. Cypher exits the Matrix, murders three crew members, and severely wounds a fourth, Tank. Before he can kill Neo and Trinity, Tank regains consciousness and kills him before pulling Neo and Trinity from the Matrix. The Agents interrogate Morpheus to learn his access codes to the mainframe computer in Zion, which would allow them to destroy it. Neo resolves to return to the Matrix to rescue Morpheus, as the Oracle prophesied; Trinity insists on accompanying him. While rescuing Morpheus, Neo gains confidence in his abilities, performing feats comparable to those of the Agents.\n\nAfter Morpheus and Trinity safely exit the Matrix, Smith ambushes and appears to kill Neo. While a group of Sentinels attack the Nebuchadnezzar, Trinity confesses her love for Neo and says the Oracle told her she would fall in love with the One. Neo is revived, with newfound abilities to perceive and control the Matrix; he easily defeats Smith, prompting the other Agents to flee, and he leaves the Matrix just as the ship's electromagnetic pulse disables the Sentinels. Back in the Matrix, Neo makes a telephone call, promising the machines that he will show their prisoners \'a world where anything is possible\', before he hangs up and flies away.", "Characters": ["a female.[23]", "Morpheus: A human freed from the Matrix and captain of the Nebuchadnezzar. Fishburne stated that once he read the script, he did not understand why other people found it confusing. However, he doubted if the movie would ever be made, because it was \"so smart\".[16] The Wachowskis instructed Fishburne to base his performance on the character Morpheus in Neil Gaiman's Sandman comics.[24] Gary Oldman, Samuel L. Jackson and Val Kilmer were also considered for the part.[22]", "described in the script. She also doubted how the Wachowskis would get to direct a movie with a budget so large, but after spending an hour with them going through the storyboard, she understood why some people would trust them.[16] Moss mentioned that she underwent a three-hour physical test during casting, so she knew what to expect subsequently.[25] The role made Moss, who later said, \"I had no career before. None.\"[26] Janet Jackson was initially approached for the role but scheduling conflicts prevented her from accepting it.[27][28] In an interview, she stated that turning down the role was difficult for her, so she later referenced The Matrix in the 'Intro' and 'Outro' interludes on her tenth studio album Discipline.[29] Sandra Bullock, who was previously approached for the role of Neo, was also offered the role of Trinity, but she turned it down.[30] Rosie Perez, Salma Hayek and Jada Pinkett Smith (who would later play Niobe in the sequels) auditioned for the role.[31][32][33]", "Agent Smith: A sentient \"Agent\" program of the Matrix whose purpose is to destroy Zion and stop humans from getting out of the Matrix. Unlike other Agents, he has ambitions to free himself from his duties. Weaving stated that he found the character amusing and enjoyable to play. He developed a neutral accent but with more specific character for the role. He wanted Smith to sound neither robotic nor human, and also said that the Wachowskis' voices had influenced his voice in the film. When filming began, Weaving mentioned that he was excited to be a part of something that would extend him.[34] Jean Reno was offered the role, but declined, unwilling to move to Australia for the production.[35]", "Cypher: Another human freed by Morpheus, and a crewmember of the Nebuchadnezzar, but one who regrets taking the red pill and seeks to be returned to the Matrix, later betraying the rebels to Agent Smith. Pantoliano had worked with the Wachowskis prior to appearing in The Matrix, starring in their 1996 film Bound.", "Tank: The \"operator\" of the Nebuchadnezzar and Dozer's brother; they are both \"natural\" (as opposed to bred) humans, born outside of the Matrix.", "Mouse: A freed human and a programmer on the Nebuchadnezzar.", "The Spoon Boy, a young prophet who has learnt how to manipulate the world of the Matrix. Seemingly wise beyond his years, he teaches Neo how to develop his powers and provides him with wisdom and motivation across the films and graphic novels.", "The Oracle: A prophet who still resides in the Matrix, helping the freed humans with her foresight and wisdom.", "Dozer: Pilot of the Nebuchadnezzar. He is Tank's brother, and like him was born outside of the Matrix.", "Apoc: A freed human and a crew member on the Nebuchadnezzar.", "Switch: A human freed by Morpheus, and a crew member of the Nebuchadnezzar.", "Agent Brown: One of two sentient \"Agent\" programs in the Matrix, who works with Agent Smith to destroy Zion and stop humans from escaping the system.", "Agent Jones: One of two sentient \"Agent\" programs in the Matrix who works with Agent Smith to destroy Zion and stop humans from escaping the system.", "DuJour: A reference to the White Rabbit in Alice's Adventures in Wonderland."]},
    {"Title":"X-Men","Plot":"In 1944 Nazi-occupied Poland, fourteen-year-old Erik Lehnsherr is separated from his parents upon entering the Auschwitz concentration camp. While attempting to reach them, he causes a set of metal gates to bend toward him because of his mutant ability to generate magnetic fields, but is knocked out by guards. In the present day, U.S. Senator Robert Kelly attempts to pass a 'Mutant Registration Act' in Congress, which would force mutants to reveal their identities and abilities. Nearby, telepathic mutant Charles Xavier sees Lehnsherr, who now goes by the name 'Magneto', in attendance and is concerned with how he will respond to the Registration Act. In Meridian, Mississippi, seventeen-year-old Marie accidentally puts her boyfriend into a coma after kissing him, because of her mutant ability to absorb the power and life force of others. Adopting the name 'Rogue', she flees to Alberta and meets Logan, also known as 'Wolverine', a mutant with superhuman healing abilities and metal claws that protrude from between his knuckles. Sabretooth, a member of Magneto's Brotherhood of Mutants, attacks them on the road, but two members of Xavier's X-Men, Cyclops and Storm, save them. Logan and Rogue are brought to Xavier's school for mutants in Westchester County, New York. Believing that Magneto is interested in capturing Logan, Xavier asks him to stay while he investigates the matter. Meanwhile, Rogue enrolls in the school as a new pupil and develops a crush on cryokinetic mutant Bobby Drake. Brotherhood members Toad and Mystique abduct Senator Kelly, bringing him to their hideout on the uncharted island of Genosha. Magneto uses Kelly as a test subject for a machine powered by his magnetic abilities that generates a field of radiation, which induces mutations in normal humans. Taking advantage of his newfound mutation, Kelly later escapes. Rogue visits Logan during the night while he is having a nightmare. Startled, he accidentally stabs her, but she manages to absorb his healing ability and recover. Mystique, disguised as Drake, later convinces Rogue that Xavier is angry with her and that she must leave the school. Xavier uses his mutant-locating machine Cerebro to find Rogue at a train station, and the X-Men go to retrieve her. Meanwhile, Mystique enters Cerebro and sabotages it. Having left ahead of Storm and Cyclops, Logan finds Rogue on a train and convinces her to return. Before they can leave, Magneto arrives, incapacitates Logan and subdues Rogue, revealing it was her whom he wants rather than Logan. Although Xavier attempts to stop him by mentally controlling Sabretooth, he is forced to release his hold when Magneto threatens the police who have converged on the station, allowing the Brotherhood to escape with Rogue. Kelly arrives at the school, and Xavier reads his mind to learn about Magneto's machine. Realizing the strain of powering it nearly killed him, the X-Men deduce he intends to transfer his powers to Rogue and use her to power it at the cost of her life. Kelly's body rejects his mutation, and his body dissolves into liquid. Xavier attempts to locate Rogue using Cerebro, but Mystique's sabotage incapacitates him, and he falls into a coma. Fellow telepath and telekinetic Jean Grey fixes Cerebro and uses it, learning that the Brotherhood plans to place their machine on Liberty Island and use it to 'mutate' the world leaders meeting at a summit on nearby Ellis Island. The X-Men scale the Statue of Liberty, battling and overpowering the Brotherhood while Magneto transfers his powers to Rogue and activates the machine. As Logan confronts and distracts Magneto, Cyclops blasts him away, allowing Logan to destroy the machine. He transfers his powers to Rogue, rejuvenating her while incapacitating himself. Xavier and Logan recover from their comas. The group also learns that Mystique escaped the island battle and is impersonating Kelly. Xavier gives Logan a lead to his past at an abandoned military installation in Canada before visiting Magneto, now imprisoned in a complex constructed of polycarbonate. Magneto warns him that he intends to escape one day and continue the fight; Xavier replies that he will always be there to stop him.","Characters":[]}
    ]










class UnitTests:
    def test_text_gen_text_only_prompt(self, prompt: str):
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        MAX_RETRIES = 9  # Set a maximum number of retries
        SLEEP_TIME = 4   # Initial sleep time in seconds

        for attempt in range(MAX_RETRIES):
            try:
                response = model.generate_content(prompt)
                # Extract the text from the response
                if response._done and response._result and response._result.candidates:
                    text = response._result.candidates[0].content.parts[0].text
                    return text
                else:
                    raise ValueError("Response is not complete or lacks expected structure.")
            except ResourceExhausted as exc:
                if attempt < MAX_RETRIES - 1:
                    print(f"Resource exhausted. Retrying in {SLEEP_TIME} seconds...")
                    time.sleep(SLEEP_TIME)  # Wait before retrying
                    SLEEP_TIME *= 2  # Exponential backoff
                else:
                    print("Max retries reached. Please check your API usage.")
                    raise exc  
            except Exception as e:
                print(f"An error occurred: {e}")
                break  
import re



def generate_text_gpt(prompt, model, max_tokens=100, temperature=0.7,client=None):
    # print(prompt)
    try:
        # generated_text=""
        # while generated_text=="":
        #     time.sleep(2)
        # Set your OpenAI API Key
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

        response = client.completions.create(
            model=model,
            prompt = prompt,
            temperature=0,
            max_tokens=350
        )

        
        
        generated_text = response.choices[0].text.strip()
        print(f"generate text is :\n{generated_text}")
        return generated_text
    except Exception as e:
        print(f"Error generating text: {e}")
        return None



def generate_character_prompt(short_story):
    """Generate the character identification prompt."""
    # return f"Identify the significant characters in the following story:\n{short_story}"
    # return f"Identify only the main significant characters in the following story and return only their names in a list format, without any additional text or description:\n{short_story}"
    return extract_characters_prompt.format(short_story=short_story)

def extract_characters(ut, short_story, model, pipe,client,temperature):
    """Extract characters from the story based on the model."""
    character_prompt = generate_character_prompt(short_story)
    
    if model == "gemini":
        character_response = ut.test_text_gen_text_only_prompt(character_prompt)
    elif model == "llama3":
        character_response = get_response_baseline(character_prompt, pipe, "")
        characters = [x.split(":")[0][2:] for x in character_response.split("\n")][2:]
    elif "gpt" in model:
        character_response = generate_text_gpt(character_prompt, model,client, temperature=temperature)
        # print(character_response)
        # Step 1: Extract names and remove the bullet points (the '-')
        # Regular expression that works for both formats
        characters = re.findall(r"^\d+\.\s*(.+)$|^\-\s*(.+)$", character_response, re.MULTILINE)
        
        # The regular expression will return tuples, so we flatten them to get the names.
        characters = [char for group in characters for char in group if char]

        # Step 2: Remove duplicates by converting the list to a set
        unique_names = list(set(characters))

        # Step 3: Optionally, sort the names if needed
        unique_names.sort()
        characters = unique_names
    
    if character_response:
        if model == "gemini":
            return re.findall(r"\*\s+\*\*(.*?):\*\*", character_response)
        else:
            return characters
    return []

def generate_action_prompt(character, short_story, attribute_type, role_list):
    """Generate the action or trait prompt for a specific character and attribute."""
    if not role_list:
        # return f"""
        # Analyze the given short story and identify the character {character}'s primary {attribute_type}. 
        # Please provide exactly 5 concise {attribute_type} in a list format. Each {attribute_type} should be ONLY a single or double word, without any specific names, descriptions, or extra text.
       
        # **Short story:**
        # {short_story}
        
        
        # """
        return extract_feature_prompt.format(character=character,attribute_type=attribute_type,short_story=short_story)

    else:
        print(f"global list:{role_list}")
        # return f"""
        # Analyze the given short story and identify the character {character}'s primary {attribute_type}. 
        # Please provide exactly 5 concise attributes in a list format. Each attribute should be a single or double word, without any specific names, descriptions, or extra text.
        # Use the provided {attribute_type} list as a guide, but suggest a new {attribute_type} if it better fits the character's actions and motivations within the story.

        # **Short story:**
        # {short_story}

        # **{attribute_type} list:**
        # {role_list}
        # """
        return extract_features_with_global_list_prompt.format(character=character,attribute_type=attribute_type,short_story=short_story,role_list=role_list)


def generate_model_response(action_prompt, model, ut, pipe,client,temperature):
    """Generate the model's response based on the action prompt."""
    try:
        if model == "gemini":
            return ut.test_text_gen_text_only_prompt(action_prompt)
        elif model == "llama3":
            return get_response_baseline(action_prompt, pipe, "")
        elif "gpt" in model:
            return generate_text_gpt(action_prompt, model,client,temperature=temperature)
    except Exception as e:
        print(f"Error generating response: {e}")
        return None

def extract_actions(model, action_response):
    """Extract actions from the model's response."""
    if model == "gemini":
        return re.findall(r"\*\s+\*\*(.*?):\*\*", action_response) if action_response else []
    elif model=="llama3":
        return [x[1:] for x in action_response.split("\n")[2:]] if action_response else []
    elif "gpt" in model:
        # Step 1: Extract the traits/roles by matching the text after the number
        actions = re.findall(r"\d+\.\s+([A-Za-z]+)", action_response)

        # Step 2: Remove extra spaces (if any) and ensure it's a clean list
        actions = [trait.strip() for trait in actions]

        return actions
def extract_characters_and_actions(ut, short_story, model, existing_functions,temperature, pipe=None, prompt=None,client=None):
    """Extract characters and actions from a short story."""
    # existing_functions = {'role': set(), 'action': set(), 'trait': set()} - for example - it can be different according to the prompt
    characters = extract_characters(ut, short_story, model, pipe,client,temperature=temperature)
    actions_dict = {}
    
    if characters:
        
        
        # Step 2: Find actions associated with each character
        for character in characters:
            # print(character)
            actions_dict[character] = {}
            
            for attribute_type in prompt:
                action_prompt = generate_action_prompt(character, short_story, attribute_type, list(existing_functions[attribute_type]))
                action_response = generate_model_response(action_prompt, model, ut, pipe,client,temperature=temperature)
                actions = extract_actions(model, action_response)
                
                if actions:
                    actions_dict[character][attribute_type] = actions  # Add to actions dictionary if actions were found
                    # print(f"{character}[{attribute_type}]:{actions_dict[character][attribute_type]}")
                    if attribute_type in existing_functions:
                        existing_functions[attribute_type].update(actions)
                   
    return characters, actions_dict, existing_functions
import re

def merge_replace_or_add_output_parsing(text):
    
    # regex pattern
    pattern = r"Decision:\s*(?P<decision>.*?)\s*Rationale:\s*(?P<rationale>.*?)\s*Recommended Term:\s*(?P<recommended_term>.*)"

    # Perform the regex match
    match = re.search(pattern, text, re.DOTALL)

    # Extract the captured groups if there is a match
    if match:
        decision = match.group("decision")
        rationale = match.group("rationale")
        recommended_term = match.group("recommended_term")
        # Printing the structured output
        print("***********")
        print(f"Decision: {decision}")
        print(f"Rationale: {rationale}")
        print(f"Recommended Term: {recommended_term}")
    else:
        print("No match found.")
    
    return decision, rationale, recommended_term
    
def merge_replace_or_add(actions,attribute_type_existing_functions, attribute_type, model, client,temperature, changes_in_global_list={},merge_action_over_global=0, merge_global_over_action=0, merge_new=0, kept_separate=0,used_from_existing_functions=0):
    print("MERGE REPLACE OR ADD\n")
    all_dicisions=[]
    # print(f"ACTIONS:{actions}\n")
    potential=""
    for i, action in enumerate(actions):
        if action not in attribute_type_existing_functions:
            potential = argmax_cosine_sim(action,attribute_type_existing_functions)
            print(f"ACRION:{action}, POTENTIAL:{potential}\n")
#             prompt = f"""
#             Task: Compare the terms "{action}" and "{potential}" within the context of {attribute_type}.  

# Evaluation:  
# 1. Are the terms distinct, overlapping, or synonymous?  
# 2. Should they be merged or kept separate?  

# Output:  
# - Decision: [Merge / Keep Separate]  
# - Rationale: Briefly explain your reasoning (1-2 sentences).  
# - Recommended Term: Recommend either one of the original terms or propose a new term that better encompasses both. If separate, state "None"  

# Keep the explanation concise and focused on clarity.  

#             """
            prompt = merge_prompt.format(action=action, potential=potential, attribute_type=attribute_type)


            # print(f"\n\nPROMPT:{prompt}\n")
            output = generate_text_gpt(prompt, model,client, temperature=temperature)
            decision, explanation, suggested_action  = merge_replace_or_add_output_parsing(output)
            print(f"\nOUTPUT:{output}\n")
            if decision.lower() == "merge":
                if suggested_action == potential:
                    merge_global_over_action+=1
                    actions[i] = potential
                elif suggested_action == action:
                    merge_action_over_global+=1
                    attribute_type_existing_functions = list(map(lambda x: x.replace(potential, suggested_action), attribute_type_existing_functions))
                    changes_in_global_list[potential]=suggested_action # at the end we can merge all the changes that are one after another, to one.
                else:
                    merge_new+=1
                    actions[i] = potential
                    attribute_type_existing_functions = list(map(lambda x: x.replace(potential, suggested_action), attribute_type_existing_functions))
                    changes_in_global_list[potential]=suggested_action # at the end we can merge all the changes that are one after another, to one.
            else:
                kept_separate+=1
        else:
            if len(attribute_type_existing_functions)>0:
                used_from_existing_functions+=1
                decision, explanation, suggested_action = f"{attribute_type} is already in existing list", f"{attribute_type} is already in existing list", f"{attribute_type} is already in existing list"
            else:
                kept_separate+=1
                decision, explanation, suggested_action = f"no existing list", f"no existing list", f"no existing list"
        all_dicisions.append(
            
            
            {
               "term":action,
               "potential":potential,
               "all existing list":list(attribute_type_existing_functions),
               "attribute type": attribute_type,
               "decision":  decision,
               "explanation": explanation,
               "suggested term": suggested_action
                
                
            }
        )    
    return actions, attribute_type_existing_functions, changes_in_global_list, decision, explanation, suggested_action, merge_action_over_global, merge_global_over_action, merge_new, kept_separate, used_from_existing_functions, all_dicisions
                
            
  
    
def extract_characters_and_actions_with_merging(ut, short_story, model, existing_functions,temperature, pipe=None, prompt=None,client=None,merge_action_over_global=0, merge_global_over_action=0, merge_new=0, kept_separate=0, used_from_existing_functions=0):
    """Extract characters and actions from a short story."""
    # existing_functions = {'role': set(), 'action': set(), 'trait': set()} - for example - it can be different according to the prompt
    characters = extract_characters(ut, short_story, model, pipe,client,temperature=temperature)
    actions_dict = {}
    all_dicisions, turn = {},{}
    changes_in_global_list = {}
    # merge_action_over_global, merge_global_over_action, merge_new, kept_separate, used_from_existing_functions = 0, 0, 0, 0, 0
    all_changes_as_variables_in_a_list = []
    if characters:
        
        
        # Step 2: Find actions associated with each character
        for i,character in enumerate(characters):
            print(f"character:{character}")
            actions_dict[character] = {}
            
            for attribute_type in prompt:
                action_prompt = generate_action_prompt(character, short_story, attribute_type, list(existing_functions[attribute_type]))
                action_response = generate_model_response(action_prompt, model, ut, pipe,client,temperature=temperature)
                actions = extract_actions(model, action_response)
                turn = {"turn":i,"merge_action_over_global":merge_action_over_global, "merge_global_over_action":merge_global_over_action, "merge_new":merge_new, "kept_separate":kept_separate,"used_from_existing_functions":used_from_existing_functions}
                
                if len(existing_functions[attribute_type])>0:
                    actions, existing_functions[attribute_type], changes_in_global_list, decision, explanation, suggested_action, merge_action_over_global, merge_global_over_action, merge_new, kept_separate,used_from_existing_functions, all_dicisions = merge_replace_or_add(actions,existing_functions[attribute_type],attribute_type, model,client,temperature,changes_in_global_list,merge_action_over_global, merge_global_over_action, merge_new, kept_separate,used_from_existing_functions)
                    turn = {"turn":i,"merge_action_over_global":merge_action_over_global, "merge_global_over_action":merge_global_over_action, "merge_new":merge_new, "kept_separate":kept_separate,"used_from_existing_functions":used_from_existing_functions}
                    all_changes_as_variables_in_a_list.append(turn)
                if actions:
                    if attribute_type not in actions_dict[character]:
                        actions_dict[character][attribute_type]={}
                    actions_dict[character][attribute_type]["values"] = actions  # Add to actions dictionary if actions were found
                    if len(existing_functions[attribute_type])>0:
                        actions_dict[character][attribute_type]["merging changes"] = all_dicisions
                        actions_dict[character][attribute_type]["numerical data"]= turn
                    else:
                        actions_dict[character][attribute_type]["merging changes"] = {}
                        actions_dict[character][attribute_type]["numerical data"]= turn
                    print(f"{character}[{attribute_type}]:{actions_dict[character][attribute_type]}")
                    if attribute_type in existing_functions:
                        existing_functions[attribute_type].update(actions)
                   
    return characters, actions_dict, existing_functions, changes_in_global_list, merge_action_over_global, merge_global_over_action, merge_new, kept_separate, used_from_existing_functions

        
    
def convert_sets_to_lists(obj):
    if isinstance(obj, set):
        # Convert set to list
        return list(obj)
    elif isinstance(obj, dict):
        # Recurse through dictionary values
        return {k: convert_sets_to_lists(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        # Recurse through list elements
        return [convert_sets_to_lists(item) for item in obj]
    else:
        # If it's neither a set, dict, nor list, return as is
        return obj


def main():
    parser = argparse.ArgumentParser(description="Process a corpus using a language model.")
    parser.add_argument("--model", required=False, help="Name of the language model (e.g., GPT-4, Claude, Gemini)")
    parser.add_argument("--corpus", required=False, help="Path to the corpus of story synopses")
    parser.add_argument("--prompt", required=False, default=["roles", "traits", "actions"], help="roles, traits, actions")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for deterministic traversal")
    parser.add_argument("--output_path", default="./output.jsonl", help="Path to save output data")
    parser.add_argument("--merge", default = False, action="store_true", help="if you want to merge extracted actions if similar.")
    parser.add_argument("--temperature",default=42, type=int, help="temperature of the model.")
    args = parser.parse_args()
    
    # print("CUDA available:", torch.cuda.is_available())
    # print("Number of GPUs:", torch.cuda.device_count())
    # if torch.cuda.is_available():
    #     print("Current GPU:", torch.cuda.get_device_name(1))

    random.seed(args.seed)
    # data = []
    if args.corpus:
        with open(args.corpus, 'r') as file:
            for line in file:
                data.append(json.loads(line))

    
    if "gpt" in args.model:
        openai.api_key = os.environ.get("OPENAI_API_KEY")
        # print(openai.api_key)
        client = OpenAI()
    ut = UnitTests()
    pipe = None
    if args.model == "llama3":
        pipe = get_model_baseline("meta-llama/Meta-Llama-3-8B-Instruct")
    if args.model=="gemini":
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    
        
    # existing_functions = set()
    existing_functions = {x:set() for x in args.prompt}
    merge_action_over_global, merge_global_over_action, merge_new, kept_separate, used_from_existing_functions = 0, 0, 0, 0, 0
    
    # with open(args.output_path.replace(".jsonl",f"_{args.seed}_.jsonl"), 'w') as jsonl_file:
    with open(args.output_path.replace(".jsonl", f"_{args.seed}_beautify.jsonl"), 'w') as jsonl_file, \
     open(args.output_path.replace(".jsonl", f"_{args.seed}_.jsonl"), 'w') as jsonl_fomatted_file:
        for i, movie in enumerate(random.sample(data, len(data))):
            short_story = movie["Plot"]
            title = movie["Title"]
            if args.merge == True:
                characters, actions_dict, existing_functions, changes_in_global_list,merge_action_over_global, merge_global_over_action, merge_new, kept_separate, used_from_existing_functions = extract_characters_and_actions_with_merging(ut, short_story,args.model, existing_functions,args.temperature, pipe, args.prompt,client,merge_action_over_global, merge_global_over_action, merge_new, kept_separate, used_from_existing_functions)
                if characters is not None and actions_dict!=[]:
                    # existing_functions.update([action for actions in actions_dict.values() for action in actions])
                    
                    extracted_output = {
                        "title": title,
                        "characters": characters,
                        "actions_dict": actions_dict,
                        "all_actions": {k: list(v) for k, v in existing_functions.items()},
                        "plot": short_story,
                        "changes_in_global_list": changes_in_global_list
                        
                    }
            else:
                characters, actions_dict, existing_functions = extract_characters_and_actions(ut, short_story,args.model, existing_functions,args.temperature, pipe, args.prompt,client)
                if characters is not None and actions_dict!=[]:
                    # existing_functions.update([action for actions in actions_dict.values() for action in actions])
                    
                    extracted_output = {
                        "title": title,
                        "characters": characters,
                        "actions_dict": actions_dict,
                        "all_actions": {k: list(v) for k, v in existing_functions.items()},
                        "plot": short_story,
                        
                    }
            
            jsonl_file.write(json.dumps(convert_sets_to_lists(extracted_output), indent=4, ensure_ascii=False) + '\n')
            jsonl_fomatted_file.write(json.dumps(convert_sets_to_lists(extracted_output)) + '\n')

            
    print(f"Processing complete. Output saved to {args.output_path}.")

if __name__ == "__main__":
    main()