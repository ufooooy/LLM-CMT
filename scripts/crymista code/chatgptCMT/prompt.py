from show import *
from utils import format_list, read_file

DIMENSION_PROMPT = [
    {
        'terms_file': 'terms/generic-causes.json',
        'dimension': 'This taxonomy classifies different generic causes of cryptographic API misuses according to the '
                     'terms:   "Compromising Client and Server Secrecy",  "Compromising Secrecy of Cipher Text",  '
                     '"Compromising Randomness",  "Compromising Secret Keys",  "Compromising Integrity through '
                     'Improper Checksum Use",  "Compromising Non-Repudiation",  "Compromising Communication Secrecy '
                     'with Intended Receiver",  with sub-categories representing corresponding typical types. ',
        'define': 'their generic causes. Each term should succinctly and exactly summarize a key cause of misuse.',
    },
    {
        'terms_file': 'terms/components.json',
        'dimension': 'This taxonomy classifies different cryptosystem components of cryptographic API misuses '
                     'according to the terms:     "Cryptographic Keys", "Passwords in Password-based Encryption", '
                     '"Passwords in KeyStore", "Credentials in String", "Hostname Verifier", "Certificate '
                     'Validation", "SSL Sockets", "Hypertext Transfer Protocol", "Pseudorandom Number Generator ('
                     'PRNG)", "Seeds in Pseudorandom Number Generator (PRNG)", "Salts in Password-based encryption ('
                     'PBE)", "Mode of Operation", "Initialization Vector (IV)", "Iteration Count in Password-based '
                     'Encryption (PBE)", "Symmetric Ciphers",  "Asymmetric Ciphers", "Cryptographic Hash Functions", '
                     '"Cryptographic MAC",  with sub-categories representing corresponding typical types.',
        'define': 'their related components of cryptosystems. Each term should succinctly indicate a component of '
                  'cyptosystems that the misuses may involved.',

    },
    {
        'terms_file': 'terms/security-properties.json',
        'dimension': 'This taxonomy classifies different security properties compromised by cryptographic API misuses '
                     'according to the terms: "Breach of Confidentiality", "Breach of Integrity", "Breach of '
                     'Availability", "Breach of Authentication", "Breach of non-repudiation",  with subcategories '
                     'representing corresponding typical types.',
        'define': 'security properties that may be violated by them. Each term should indicate a security property or '
                  'goal that the misuses may breach.',
    }
]


def knowledge_prompt(code, knowledge):
    return [
        {
            "role": "system",
            "content": "You are a cryptography expert. "
        },
        {
            "role": "user",
            "content": "You will be given a code snippet along with knowledge about unsafe practices, please identify "
                       "all cryptographic API misuses in the this snippet and export the causes of these misuses, "
                       "according to the security properties they breach and/or other cryptography principles they "
                       "violate, based on the following requirements: 1) You should decide cryptographic API misuses "
                       "based on relevant international or national standards, guidelines, recommendations, "
                       "CVE vulnerabilities, and other official information, to the extent possible. 2) You should "
                       "export all the identified misuses as a list of JSON objects in the format of ```json[{"
                       "'abstract':"",'files':["",],'detail':""},]```, where each JSON object describes one "
                       "cryptographic API misuse, its 'abstract' field is a brief description of the misuse, "
                       "'files' is the list of code files in which the misuse is identified, and 'detail' is the "
                       "detailed description of the misuse. 3) Each cryptographic API misuse must be documented as a "
                       "separate JSON object to maintain the atomicity of misuses. This means that if multiple "
                       "misuses are identified within a single code snippet or across the provided code snippets, "
                       "each misuse should be represented by its own JSON object. This approach ensures that the "
                       "causes, breached security properties, and violated cryptography principles of each misuse are "
                       "clearly and independently documented, facilitating a more granular analysis and understanding "
                       "of the misuses."
        },
        {
            "role": "assistant",
            "content": f"What is the content of the code?"
        },
        {
            "role": "user",
            "content": f"{code}"
        },
        {
            "role": "assistant",
            "content": "What is the content of the knowledge about unsafe practices?"
        },
        {
            "role": "user",
            "content": f"{knowledge}"
        },
    ]


def cot_prompt(name, code, answer1, count):
    base = [
        {
            "role": "system",
            "content": "You are a cryptography expert. "
        },
        {
            "role": "user",
            "content": f"You will be given a code snippet: {name}, please point out the "
                       "cryptography-related information in this code, such as the usage of cryptography API or "
                       "cryptographic algorithm, protocol implementation, etc. If there is no cryptography-related "
                       "information, please indicate the functions implemented by the code and other information. "
                       "And, please normalize the output and use `json{'Cryptography-Related Information':'', "
                       "'Implementation Information':''}` to represent the output."
        },
        {
            "role": "assistant",
            "content": f"What is the content of the code {name}?"
        },
        {
            "role": "user",
            "content": f"{code}"
        }
    ]
    if count == 1:
        return base
    elif count == 1:
        base += [
            {
                "role": "assistant",
                "content": f"{answer1}"
            },
            {
                "role": "user",
                "content": "Based on the cryptography-related information or implementation information of the code, "
                           "please list the possible insecure phenomena of cryptography usage, or do you recommend "
                           "more secure cryptography-related best practices to replace this implementation? And, "
                           "please normalize the output and use `json[{'Cryptographic Insecure Practices': ''}]` to "
                           "represent the output."
            }
        ]


def merge2_prompt(misuse1, misuse2):
    return [
        {
            "role": "system",
            "content": "You are a cryptography expert. "
        },
        {
            "role": "user",
            "content": "You will be given two cryptographic API misuses in the JSON format, in which each entry "
                       "represents a cryptographic API misuse with the \"abstract\" field specifying a brief "
                       "description of the misuse and \"explanation\" summarizing the causes of the misuse, "
                       "the security properties it breaches, and/or other security issues it violates. You need to "
                       "determine whether the two cases essentially refer to the same cryptographic misuse, "
                       "based on a good understanding of the \"abstract\" and \"explanation\" fields of each "
                       "cryptographic API misuse, answer \"YES\" otherwise answer \"NO\"."
        },
        {
            "role": "assistant",
            "content": "What is the content of the first cryptographic API misuse?"
        },
        {
            "role": "user",
            "content": f"{misuse1}"
        },
        {
            "role": "assistant",
            "content": "What is the content of the second cryptographic API misuse?"
        },
        {
            "role": "user",
            "content": f"{misuse2}"
        }
    ]


def tune_prompt(dimension, taxonomy, missing):
    return [
        {
            "role": "system",
            "content": "You are a cryptography expert. "
        },
        {
            "role": "user",
            "content": "You will be given a preliminary cryptography API misuse taxonomy and a list of cryptographic "
                       "API misuse cases where the \"abstract\" field of the entry is a summary of the misuse case "
                       "and \"explanation\" is its detailed description. "
                       f"This taxonomy classifies different {dimension} of cryptographic API misuses, with "
                       "sub-categories representing corresponding typical types.\nYou should integrate the misuse "
                       "into the existing taxonomy to make a more comprehensive one based on the understanding of its "
                       "\"abstract\" and \"explanation\" and following the requirements below:\n1) Add cases to "
                       "existing categories/subcategories or new branches or even adjust the categories of the "
                       "original taxonomy system so that the taxonomy system integrating new cases is more reasonable "
                       "and scientific.\n2) Please output the new part in the format consistently with the original "
                       "taxonomy structure. Use \"***\" to indicate the beginning and end of the taxonomy."
        },
        {
            "role": "assistant",
            "content": "What is the content of taxonomy?"
        },
        {
            "role": "user",
            "content": f"{taxonomy}"
        },
        {
            "role": "assistant",
            "content": "What is the content of the list of cryptographic API misuse cases?"
        },
        {
            "role": "user",
            "content": f"{missing}"
        }
    ]


def dimension_prompt(previous_result):
    prompts = []
    for i in DIMENSION_PROMPT:
        dimension = i['dimension']
        define = i['define']
        terms = read_file(i['terms_file'])
        prompt = generalise_prompt(dimension, define, terms, previous_result)
        prompts.append(prompt)
    return prompts


def append_dimension_prompt(taxonomies, appends, one_taxonomy):
    prompts = []
    count = 0
    for i in DIMENSION_PROMPT:
        dimension = i['dimension']
        t = parse_taxonomy(taxonomies[count])
        taxonomy = trans_taxonomy(t)
        prompt = append_prompt(dimension, taxonomy, appends)
        if one_taxonomy:
            prompt = append_prompt(dimension, one_taxonomy, appends)
        prompts.append(prompt)
        count += 1
    return prompts


def append_prompt(dimension, taxonomy, appends):
    return [
        {
            "role": "system",
            "content": "You are a cryptography expert. "
        },
        {
            "role": "user",
            "content": "You will be given a preliminary cryptography API misuse taxonomy and a list of cryptographic "
                       "API misuse cases where the \"abstract\" field of the entry is a summary of the misuse case "
                       "and \"explanation\" is its detailed description. "
                       f"{dimension}\nYou should integrate the misuse into the existing taxonomy to make a more "
                       "comprehensive one based on the understanding of its \"abstract\" and \"explanation\" and "
                       "following the requirements below:\n1) You could add cases to existing "
                       "categories/subcategories or new branches or adjust the categories of the original taxonomy "
                       "system so that the taxonomy integrating new cases is more reasonable and scientific.\n2) "
                       "Please output the new part in the format consistently with the original taxonomy structure.  "
                       "Use \"***\" to indicate the beginning and end of the taxonomy. Use \"###\" followed by "
                       "\"1.\", \"2.\", etc.,"
                       "for first-level category titles. Use \"####\" followed by \"1.1\", \"1.2\", etc., "
                       "for subcategory titles within the first category (adjust numbering according to the "
                       "category). For listing specific misuse cases, use \"-\" and start with the misuse title in "
                       "bold, followed by a colon and its detailed explanation. Ensure each case is preceded by its "
                       "title in bold, followed by a colon and its explanation. This format will facilitate the "
                       "extraction of first-level titles, sub-titles, and cases from the answers, while also "
                       "maintaining a clear hierarchy and order."

        },
        {
            "role": "assistant",
            "content": "What is the content of taxonomy?"
        },
        {
            "role": "user",
            "content": f"{taxonomy}"
        },
        {
            "role": "assistant",
            "content": "What is the content of the case of cryptographic API misuse?"
        },
        {
            "role": "user",
            "content": f"{appends}"
        },
    ]


def generalise_prompt(dimension, define, terms, previous_result):
    return [
        {
            "role": "system",
            "content": "You are a cryptography expert. "
        },
        {
            "role": "user",
            "content": f"You'll receive a list of cryptographic API misuses and terms describing {define} Each list "
                       "entry represents a misuse, with the \"abstract\" summarizing the case and the \"explanation\" "
                       "detailing it. You should arrange all these misuses and construct a comprehensive, "
                       "hierarchy taxonomy of cryptography API misuses based on the following instructions:\n1) Group "
                       f"these misuses by {dimension} into categories, titling each to reflect the misuse nature "
                       "using given or new terms as needed.\n2) When a category encompasses a broad range of misuses "
                       "that can be further distinguished by specific characteristics or causes, divide it into "
                       "smaller, more focused subcategories. Generate titles for these subcategories that accurately "
                       "reflect the distinguishing features of the misuses they contain. If a subcategory itself "
                       "covers a broad range of misuses that can be further differentiated, continue to divide it "
                       "into even smaller categories, creating a multi-level hierarchy as necessary. \n3) Ensure that "
                       "each cryptographic API misuse provided in the list is categorized and included in the taxonomy."
                       " \n4) **Output Format Requirement**: Structure your taxonomy with clear, consistent "
                       "formatting, and include order numbers for categories and subcategories. For each category and "
                       "subcategory, provide a brief description that encapsulates the common theme or issue among "
                       "the misuses it contains. Use \"***\" to indicate the beginning and end of the taxonomy. Use "
                       "\"###\" followed by \"1.\", \"2.\", etc., for first-level category titles. Use \"####\" "
                       "followed by \"1.1\", \"1.2\", etc., for subcategory titles within the first category (adjust "
                       "numbering according to the category). For listing specific misuse cases, use \"-\" and start "
                       "with the misuse title in bold, followed by a colon and its detailed explanation. Ensure each "
                       "case is preceded by its title in bold, followed by a colon and its explanation. This format "
                       "will facilitate the extraction of first-level titles, sub-titles, and cases from the answers, "
                       "while also maintaining a clear hierarchy and order."
        },
        {
            "role": "assistant",
            "content": "What is the content of the terms?"
        },
        {
            "role": "user",
            "content": f"{terms}"
        },
        {
            "role": "assistant",
            "content": "What is the content of the cryptography API misuse JSON list?"
        },
        {
            "role": "user",
            "content": f"{previous_result}"
        }
    ]


def paraphrase_prompt(previous_result):
    return [
        {
            "role": "system",
            "content": "You are a cryptography expert."
        },
        {
            "role": "user",
            "content": "You will be given a list of cryptographic API misuses in the JSON format, in which each entry "
                       "represents a cryptographic API misuse with the \"abstract\" field specifying a brief "
                       "description of the misuse, \"files\" listing the files where the misuse is found, "
                       "and \"detail\" describing the misuse in detail. You should generate a paragraph of "
                       "explanation for each misuse based on the following requirements: \n1) Understand the "
                       "\"abstract\" and \"detail\" fields of each cryptographic API misuse and "
                       "generate a paragraph of explanation summarizing the causes of the misuse, the security "
                       "properties it breaches, and/or other security issues it violates. \n2) Export the results as "
                       "a list of JSON objects in the format of ```json[{\"abstract\":\"\",\"explanation\":\"\"},"
                       "]```, where one JSON object represents a cryptography API misuse with two fields: "
                       "\"abstract\" is the original brief description of the misuse and \"explanation\" is the "
                       "explanation you generate for it. When you output the result list, do not omit the 7-character "
                       "\"```json\" at the beginning and the 3-character \"```\" at the end."
        },
        {
            "role": "assistant",
            "content": "What is the content of the cryptography API misuse JSON list? "
        },
        {
            "role": "user",
            "content": f"{previous_result}"
        }
    ]


def merge_prompt(previous_result):
    return [
        {
            "role": "system",
            "content": " You are a cryptography expert. "
        },
        {
            "role": "user",
            "content": "You will be given a list of cryptographic API misuses in the JSON format, where one entry "
                       "represents a cryptography API misuse, its \"abstract\" field is a brief description of the "
                       "misuse, \"files\" is the list of code files in which the misuse is found, and \"detail\" is a "
                       "detailed description of the misuse. You should summarize this cryptographic API misuse list "
                       "and export the result based on the following requirements:\n1) You should merge different "
                       "entries in the list with the same meaning of cryptographic API misuses, based on \"abstract\" "
                       "and \"detail\". That is, if several cryptography API misuses have the same meaning, "
                       "summarize their \"abstract\" into a common \"abstract\", merge their \"files\" fields,  "
                       "and combine and summarize their \"detail\" fields.\n2) You should export the resulting list "
                       "of JSON objects using the same format as the original list and summarize the changes you make "
                       "to the original list. The format of the resulting list is  ```json[{\"abstract\":\"\","
                       "\"files\":[\"\",],\"detail\":\"\"},]```, where each JSON object describes one cryptographic "
                       "API misuse, its \"abstract\" field is a brief description of the misuse, \"files\" is the "
                       "list of code files in which the misuse is identified, and \"detail\" is the detailed "
                       "description of the misuse."
        },
        {
            "role": "assistant",
            "content": "What is the content of the cryptography API misuse JSON list? "
        },
        {
            "role": "user",
            "content": f"{previous_result}"

        }
    ]


def identify_prompt(batches, files):
    return [
        {
            "role": "system",
            "content": "You are a cryptography expert."
        },
        {
            "role": "user",
            "content": f"You will be given {batches} code snippets: {format_list(files, ', ')}, "
                       "each of which "
                       "may contain zero, one or multiple cryptographic API misuses. You need to identify all "
                       "cryptographic API misuses in these snippets and export the causes of these misuses, "
                       "according to the security properties they breach and/or other cryptography principles they "
                       "violate, based on the following requirements: \n1) You should decide cryptographic API "
                       "misuses based on relevant international or national standards, guidelines, recommendations, "
                       "CVE vulnerabilities, and other official information, to the extent possible.\n2) You should "
                       "export all the identified misuses as a list of JSON objects in the format of ```json[{"
                       "\"abstract\":\"\",\"files\":[\"\",],\"detail\":\"\"},]```, where each JSON object describes "
                       "one cryptographic API misuse, its \"abstract\" field is a brief description of the misuse, "
                       "\"files\" is the list of code files in which the misuse is identified, and \"detail\" is the "
                       "detailed description of the misuse. "
                       "\n3) Each cryptographic API misuse must be "
                       "documented as a separate JSON object to maintain the atomicity of misuses. This means that if "
                       "multiple misuses are identified within a single code snippet or across the provided code "
                       "snippets, each misuse should be represented by its own JSON object. This approach ensures "
                       "that the causes, breached security properties, and violated cryptography principles of each "
                       "misuse are clearly and independently documented, facilitating a more granular analysis and "
                       "understanding of the misuses."
                       "\n4) If no cryptographic API misuse is identified within "
                       "a given code snippet, classify the code as \"no cryptographic API misuse\" using the "
                       "following JSON object format:```json[{\"abstract\":\"No cryptographic API misuse\","
                       "\"files\":[\"\"],\"detail\":\"Upon thorough analysis, no cryptographic API misuse was "
                       "identified in the provided code. The implementation adheres to best practices and guidelines "
                       "for secure cryptographic operations.\"},]```"
        }
    ]


def identify_add_rules_prompt(batches, files):
    prompt = identify_prompt(batches, files)

    prompt[1]["content"] += "\n4) You may need to refer to my knowledge to identify some cryptographic API misuse."
    rules = input(
        "Please enter the rules of cryptography API misuse you provided:")
    prompt += [
        {
            "role": "assistant",
            "content": "What are the knowledge of cryptography API misuses that I need to refer to?"
        },
        {
            "role": "user",
            "content": f"{rules}"
        }
    ]
    return prompt


def append_file_prompt(name, code):
    return [
        {
            "role": "assistant",
            "content": f"What is the content of the code {name}?"
        },
        {
            "role": "user",
            "content": f"{code}"
        }
    ]


def friendly_prompt(prompt):
    prompt_string = ''
    for i in range(0, len(prompt)):
        if i > 0 and i % 2 == 0:
            prompt_string += '\n- '
        if prompt[i - 1]['content'].find('What is the content of the code ') >= 0:
            index = prompt[i - 1]['content'].find('?')
            prompt_string += '@' + \
                             prompt[i -
                                    1]['content'][len('What is the content of the code '):index]
        elif prompt[i - 1]['content'].find('What is the content of the cryptography API misuse JSON list?') >= 0:
            prompt_string += '@' + 'identify-result.json'
        elif prompt[i - 1]['content'].find('What is the content of the list of cryptographic API misuse cases?') >= 0:
            prompt_string += '@' + 'missing.json'
        elif prompt[i - 1]['content'].find('What is the content of taxonomy?') >= 0:
            prompt_string += '@' + 'taxonomy.json'
        elif prompt[i - 1]['content'].find('What is the content of the case of cryptographic API misuse?') >= 0:
            prompt_string += '@' + 'append.json'
        else:
            prompt_string += prompt[i]['content'] + ' '
    return prompt_string
