import re

NUM_RE = re.compile(r"(\d+)")

rules = {}
parsing_rules = True
words = []

with open("input.txt") as f:
    for line in f:
        line = line.strip()
        if not line:
            parsing_rules = False
        if parsing_rules:
            key, val = line.split(":")
            rules[key] = [r.strip() for r in val.split("|")]
        elif line:
            words.append(line)

rules["8"] = ["42", "42 8"]
rules["11"] = ["42 31", "42 11 31"]


from lark import Lark
grammar_text = ""
for (rule, reqs) in sorted(rules.items(), key=lambda x: x[0]):
    rule = NUM_RE.sub(r"rule\1", rule)
    reqs = [NUM_RE.sub(r"rule\1", req) for req in reqs]
    reqs = '\n\t| '.join(reqs)
    grammar_text += f"{rule} : {reqs}\n"

print(grammar_text)
parser = Lark(grammar_text, start="rule0")

count = 0
for word in words:
    try:
        if parser.parse(word):
            count += 1
    except Exception as e:
        pass

print(count)

# 305 too low
