import os
import sys
import xml.etree.ElementTree as ET

class XMLCombiner:
    def __init__(self, input_dir, tag_name, output_file):
        self.input_dir = input_dir #initialisation avec les 3 elements dossier, tag(c'est la table) et le nom du fichier output
        self.tag_name = tag_name
        self.output_file = output_file + ".xml"
        

   

    def combine(self):
        files = [f for f in os.listdir(self.input_dir) #dictionnaire de tous les fichier dans le dossier selectionné
                if f.startswith(f"{self.output_file}_") and f.endswith(".xml")]   #doit commencer avec le nom du fichier deja saisi
        
        if not files:
            raise FileNotFoundError(f"Aucun fichier {self.output_file}_*.xml trouvé")

        with open(os.path.join(self.input_dir, self.output_file), 'w', encoding='utf-8') as out:    ##creation si le fichier n'existe pas il sera de la forme ouputfile.xml
            out.write('<xml>\n')
            
            # Prologue du premier fichier
            first_file = os.path.join(self.input_dir, files[0])
            tree = ET.parse(first_file)
            if tree.getroot() and tree.getroot().tag == 'script':
                out.write(ET.tostring(tree.getroot(), encoding='unicode') + '\n')
            
            # Contenu des fichiers
            for file in files:
                try:
                    tree = ET.parse(os.path.join(self.input_dir, file))
                    for element in tree.getroot():
                        if element.tag == self.tag_name:
                            out.write(ET.tostring(element, encoding='unicode'))
                except ET.ParseError as e:
                    print(f"Erreur dans {file} : {e}")
            
            out.write('\n</xml>')

        print(f"Fichier généré : {os.path.abspath(self.output_file)}")