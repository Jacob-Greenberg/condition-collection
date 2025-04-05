import translate
import json
import os


def translate_json(file_name: str, lang: str):
    with open(os.path.join("./conditions", file_name)) as file:
        json_file = json.load(file)
    translator = translate.Translator(to_lang=lang)
    json_file['condition'] = translator.translate(json_file['condition'])
    json_file['description'] = translator.translate(json_file['description'])
    
    for i in range(0, len(json_file['symptoms'])):
        json_file['symptoms'][i] = translator.translate(json_file['symptoms'][i])
    
    for i in range(0, len(json_file['treatment'])):
        json_file['treatment'][i] = translator.translate(json_file['treatment'][i])

    for i in range(0, len(json_file['lifestyle'])):
        json_file['lifestyle'][i] = translator.translate(json_file['lifestyle'][i])
    

    for i in range(0, len(json_file['medications'])):
        json_file['medications'][i]['note'] = translator.translate(json_file['medications'][i]['note'])
        json_file['medications'][i]['description'] = translator.translate(json_file['medications'][i]['description'])

        for j in range(0, len(json_file['medications'][i]['side_effects'])):
            json_file['medications'][i]['side_effects'][j] = translator.translate(json_file['medications'][i]['side_effects'][j])

        for j in range(0, len(json_file['medications'][i]['interactions'])):
            json_file['medications'][i]['interactions'][j] = translator.translate(json_file['medications'][i]['interactions'][j])

    json_file['medications'][i]['timeline'] = translator.translate(json_file['medications'][i]['timeline'])
        
    file_name = file_name.removeprefix("en_")
    with open(f'./conditions/{lang}_{file_name}', 'w') as f:
        json.dump(json_file, f)


def translate_all_files(lang: str):
    files = os.listdir("./conditions")
    for file in files:
        if file == "template.json":
            files.remove(file)
        elif file.startswith("en"):
            translate_json(file, lang)

print("es")
translate_all_files("es")
print("de")
translate_all_files("de")
print("dz")
translate_all_files("dz")
print("ne")
translate_all_files("ne")