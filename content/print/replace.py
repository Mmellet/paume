import re
import fileinput

with fileinput.FileInput('5.md', inplace=True) as file:
    for line in file:
        #line_modifiee = re.sub(r'{{< cite "(.*)" (\d+-\d+) (.*?) >}}', r'[@\1, pp. \2 \3]', line)
        #line_modifiee = re.sub(r'{{< cite "(.*)" >}}', r'[@\1]', line) 
        #line_modifiee = re.sub(r'{{< cite "(.*)" (\d+) >}}', r'[@\1, p. \2]', line)
        line_modifiee = re.sub(r'<sup>(.*)</sup>', r'^\1^', line)
        print(line_modifiee, end='')

        #ajout replace balise strike
        #ajout replace balise theme
