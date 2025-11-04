# NOTE
# sometimes the format can cause some errors, bitmap are preferred in such cases
# lp uses cups underneath
# alternative to lp is pycups which has some nice feature to control the print flow (we dont need this features)
# both have a way to determine the additional settings of the printer
# for lp is : lpoptions -p name_printer -l
# to know the printer name: lpstat -p
# then we use the flag StpiShrinkOutput=Shrink to make the image use all the paper
# *Shrink Crop Expand
# the precedent flag is present in the gutenprint set (gutenprint is not installed in minimal distro), otherwise similar ones are:
# fit-to-page / scaling=X / fitplot
# it is possible to check if the printer is supported by gutenprint here: https://gimp-print.sourceforge.io/p_Supported_Printers.php
# warning: if the printer is supported by gutenprint it does not mean that has the flag StpiShrinkOutput=Shrink
import subprocess


class Printer:

    def __init__(self, printer_name, user_options=None):

        self.printer_name = printer_name
        if user_options is None:
            self._filling_command = ""
        else:
            self._filling_command += " ".join(f"-o {key}={value}" for key, value in user_options.items()) + " "

    def prepare(self)-> None:

        if self._filling_command == "":
            # here we check which command execute to fill the corner
            # check for
            possible_printer_options = {
                "StpiShrinkOutput": ["Shrink", "Crop", "Expand"],  # Opzione Gutenprint (se disponibile)
                "fit-to-page": [True, False],  # Opzione CUPS standard
                "scaling": list(range(1, 201)),  # Percentuale di ridimensionamento (1-200)
                "ImageableArea": ["Auto", "Custom"],  # Area stampabile
                "fitplot": [True, False],  # Adattamento immagine alla pagina
                "crop-to-fit": [True, False],  # Ritaglio immagine per adattarla alla pagina
                "page-border": ["None", "Single", "Double", "Thick"],  # Aggiunta di bordi
            }

            best_option_value =  {
                "StpiShrinkOutput": "Shrink",
                "fit-to-page": True,  # Opzione CUPS standard
                "scaling": 100,  # Percentuale di ridimensionamento (1-200)
                "ImageableArea": "Auto",  # Area stampabile
                "fitplot": True,  # Adattamento immagine alla pagina
                "crop-to-fit": False,  # Ritaglio immagine per adattarla alla pagina
                "page-border": "None",  # Aggiunta di bordi
            }

            supported_options = self.get_printer_options(self.printer_name)


            for possible_option in possible_printer_options.keys():
                if possible_option in supported_options:
                    self._filling_command += f"-o {possible_option}={best_option_value[possible_option]} "
                    break

    def get_printer_options(self, printer_name):
        try:
            # Esegue il comando lpoptions -p <stampante> -l e ottiene l'output
            result = subprocess.run(
                ["lpoptions", "-p", printer_name, "-l"],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            return f"Errore: {e}"

    def print_image(self, file_path):
        """
        command = [
            'lp', '-d', self.printer_name,
            # '-o', 'media=4x6',
            # '-o', 'PageSize=4x6',
            # '-o', 'fit-to-page',  # Adatta l'immagine alla pagina
            '-o', 'StpiShrinkOutput=Shrink',
            file_path]
        """
        """
        command = [
                'lp', '-d', self.printer_name,
                self._filling_command.split(),
                file_path]
        """

        command = [
            'lp', '-d', self.printer_name
        ] + self._filling_command.split() + [file_path]

        try:
            subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while printing: {e}")
        except FileNotFoundError:
            print("The 'lp' command was not found. Ensure CUPS is installed.")


# DEBUG SECTION
# printer = Printer(printer_name="Dai-Nippon-Printing-DS40")
# printer.prepare()
# printer.print_image("/home/gape01/Desktop/PROGETTI/photobooth/Assets/test.jpg")