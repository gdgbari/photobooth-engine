import subprocess


def print_image(file_path):
    printer_name = 'Dai-Nippon-Printing-DS40'
    # printer_name = 'OLIVETTI_d_COPIA_6000MF'
    try:
        # Costruisci il comando di stampa
        command = [
            'lp', '-d', printer_name,
            # '-o', 'media=4x6',
            # '-o', 'PageSize=4x6',
            # '-o', 'fit-to-page',  # Adatta l'immagine alla pagina
            '-o', 'StpiShrinkOutput=Shrink',
            file_path]

        # Esegui il comando
        subprocess.run(command, check=True)

        print(f"Sent to printer '{printer_name}': {file_path}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while printing: {e}")
    except FileNotFoundError:
        print("The 'lp' command was not found. Ensure CUPS is installed.")


# Esempio di utilizzo

#file_to_print = '/home/gape01/Desktop/main/output/DEVFESTBA_0003_01-DEVFESTBA_0003_01_00.jpg'
#file_to_print =
# file_to_print = '/home/gape01/Desktop/main/output/test-test_00.jpg'

# print_image(file_to_print)
