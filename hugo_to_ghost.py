import os
import json
import yaml
import argparse
import time

def main(input_folder, output_file_name):
    data_template = {
        "db": [
            {
                "meta": {
                    "exported_on": int(time.time() * 1000),
                    "version": "5.41.0"
                },
                "data": {
                    "posts": []
                }
            }
        ]
    }

    def process_front_matter(front_matter):
        result = {
            "title": front_matter.get("title", ""),
            "slug": front_matter.get("slug", ""),
            "status": "published",
            "created_at": front_matter.get("date", ""),
            "updated_at": front_matter.get("lastmod", front_matter.get("date", "")),
            "tags": [{"name": tag.strip()} for tag in front_matter.get("tags", [])],
            "mobiledoc": ""
        }
        return result

    def markdown_to_mobiledoc(markdown_content):
        mobiledoc = {
            "version": "0.3.1",
            "markups": [],
            "atoms": [],
            "cards": [["markdown", {"cardName": "markdown", "markdown": markdown_content}]],
            "sections": [[10, 0]]
        }
        return json.dumps(mobiledoc)

    for file in os.listdir(input_folder):
        if file.endswith('.md'):
            input_file_path = os.path.join(input_folder, file)
            with open(input_file_path, 'r', encoding='utf-8') as input_file:
                input_content = input_file.read()
                split_content = input_content.split('---')
                yaml_content, markdown_content = split_content[1], '---'.join(split_content[2:])
                front_matter = yaml.safe_load(yaml_content)
                post_data = process_front_matter(front_matter)
                post_data['mobiledoc'] = markdown_to_mobiledoc(markdown_content.strip())
                data_template['db'][0]['data']['posts'].append(post_data)

    with open(output_file_name, 'w', encoding='utf-8') as output_file:
        json.dump(data_template, output_file, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert Hugo posts to Ghost JSON format.')
    parser.add_argument('input_folder', help='Path to the folder containing Hugo posts')
    parser.add_argument('output_file_name', help='Name of the output JSON file')

    args = parser.parse_args()
    main(args.input_folder, args.output_file_name)