from string import Template

prompt_template_string = """
# This is a template for the prompt to be sent to the LLM.
# The template contains placeholders that will be replaced with actual values.
# The placeholders are:
# {heading}: The heading of the listing.
# {body_dyn}: The dynamic body of the listing.
# {description}: The description of the listing.
# The template will be used to generate a prompt for the LLM to decide if the listing is a sublet or not.
"""

prompt_template_string = """
You are an assistant motivated to fulfill your task reliable.

Your task is: Check if the given listing is a sublet for a few months or not.:

The heading for the given listing is:

$heading

The body for the given listing is:
$body_dyn

The description for the given listing is:
$description

Keep in mind that you probably need multiple steps to get the required information. In that case, provide the commands one at a time and wait for answers in between.
"""

listing_content = {
  'heading': 'zentral und dennoch ruhig! 2 Zimmer Erstbezugswohnung mit Balkon ab sofort beziehbar!',
  'body_dyn': 'Liebe Wohnungssuchende, Wir freuen uns über Ihr Interesse an dem Projekt APOLLOGASSE18 und bieten\xa0 auf unserer Projekt-Homepage w w w . a p o l l o g a s s e 1 8 . a t www.apollogasse18.at einen Überblick über alle verfügbaren Wohneinheiten.\xa0 Ob Zwei-,...',
  'description': 'zentral und dennoch ruhig! 2 Zimmer Erstbezugswohnung mit Balkon ab sofort beziehbar!'
}

prompt_template = Template(prompt_template_string)
print(f"DEBUG: prompt_template_string:\n{prompt_template_string}")
print(f"DEBUG: listing_content:\n{listing_content}")
