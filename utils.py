import os
import re


def replacement_function(data, path):
    with open(f"{os.getcwd()}/{path}", "r") as file:
        prompt = file.read()

    def replacement_function(match):
        keys = match.group(1).split('"]["')
        value = data
        for key in keys:
            if not isinstance(value, dict) or key not in value:
                return ""
            value = value[key]
        return str(value)

    pattern = re.compile(r'{data\["(.*?)"\]}')
    compact_prompt = " ".join(prompt.split())
    compact_prompt = pattern.sub(replacement_function, compact_prompt)

    print(f"-----> {compact_prompt}")
    return compact_prompt
