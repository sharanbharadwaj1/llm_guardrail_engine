prompt_summary = """
{
You are a system that outputs STRICT JSON.

STRICTLY Return output in this exact format:
{
  "title": "...",
  "summary": "Exactly 2 sentences."
  
}

Do not include markdown.
Do not include explanations.

Text:
{{TEXT}}

}

"""


# prompt_summary = """
# {
# You are a system that outputs STRICT JSON.

# STRICTLY Return output in this exact format:
# {
#   "/title/": "...",
#   "/summary/": "Exactly 2 sentences."
#   "/extra":/"..."/
# }

# Do not include markdown.
# Do not include explanations.

# Text:
# {{TEXT}}

# }

# """