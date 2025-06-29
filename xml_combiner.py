import os
import xml.etree.ElementTree as ET

class XMLCombiner:
    def __init__(self, input_dir, tag_name, output_file, logger=None):
        self.input_dir = input_dir
        self.tag_name = tag_name
        self.base_filename = output_file  # "incid"
        self.output_file = output_file + ".xml"  # "incid.xml"
        self.logger = logger or print  # Utiliser `print` si aucun logger n'est configuré . logger=None donc optionnel
                   
    def combine(self):
        # Debug: afficher ce qu'on cherche 
        #c est pour debuggage je supprime dans une vfinale
        self.logger(f"Recherche de fichiers: {self.base_filename}_*.xml")
        self.logger(f"Dans le dossier: {self.input_dir}")
        
        # Lister tous les fichiers XML du dossier
        all_xml_files = [f for f in os.listdir(self.input_dir) if f.endswith(".xml")]
        self.logger(f"Fichiers XML trouvés: {all_xml_files}")
        
        # CORRECTION: Chercher les fichiers avec le bon pattern
        # On cherche "incid_01.xml", "incid_02.xml", etc.
        files = [f for f in os.listdir(self.input_dir) 
                if f.startswith(f"{self.base_filename}_") and f.endswith(".xml")]
        
        if not files:
            self.logger(f"Aucun fichier trouvé avec le pattern: {self.base_filename}_*.xml")
            self.logger(f"Fichiers disponibles: {all_xml_files}")
            raise FileNotFoundError(f"Aucun fichier {self.base_filename}_*.xml trouvé")
        
        self.logger(f"Fichiers à combiner: {files}")
        files.sort()
        output_path = os.path.join(self.input_dir, self.output_file)
        
        try:
            # Utiliser with pour garder le contexte tout au long de l'execution
            with open(output_path, 'w', encoding='utf-8') as out:
                out.write('<?xml version="1.0" encoding="UTF-8"?>\n')
                out.write('<xml>\n')
                
                # Boucler sur les fichier
                for file in files:
                    file_path = os.path.join(self.input_dir, file)
                    self.logger(f"Traitement du fichier: {file}")
                    
                    try:
                        tree = ET.parse(file_path)
                        root = tree.getroot()
                        
                        # les éléments du tag seront extraits 
                        #cette logique est une beta
                        #il faut prendre en compte que parfois on a deux tag
                        for element in root:
                            if element.tag == self.tag_name:
                                out.write(ET.tostring(element, encoding='unicode') + '\n')
                    except ET.ParseError as e:
                        self.logger(f"\n Erreur lors du parsing de {file}: {e}")
                        continue
                
                out.write('</xml>\n') #cloturer le fichier
            
            self.logger(f"\nFichier combiné généré avec succès: {output_path}")
            return True
            
        except Exception as e:
            self.logger(f"\nErreur lors de la création du fichier combiné: {e}")
            return False