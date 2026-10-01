from csv import reader


def carica_da_file(file_path):
    """Carica le foto dal file, creando un nuovo anno ogni volta che compare per la prima volta"""
    try:
        with open(file_path, "r", encoding="utf-8") as infile:
            csv_reader = reader(infile)
            album = {}
            for row in csv_reader:
                # Salta la prima riga di intestazione
                if row[0] == "codice":
                    continue
                else:
                    codice = row[0]
                    titolo = row[1]
                    autore = row[2]
                    mese = row[3]  # Convertito in intero per i controlli successivi
                    anno = row[4]

                    # Se l'anno non esiste nell'album, lo creiamo vuoto
                    if anno not in album:
                        album[anno] = {}
                    # Inseriamo i dati della foto usando il codice come chiave
                    album[anno][codice] = [titolo, autore, mese]
            print("album caricato")
            return album

    except FileNotFoundError:
        print("il file path non esiste")
        return None


def aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path):
    """Aggiunge una foto all'album, creando l'anno al volo se non è ancora presente"""
    #Controllo validità del mese (deve essere un intero da 1 a 12)
    mese = int(mese)
    if not (1 <= mese <= 12):
        return None

    #Controllo se il codice è già presente in tutto l'album
    for anno_esistente in album:
        if codice in album[anno_esistente]:
            return None

    #Aggiornamento del file
    try:
        with open(file_path, "a", encoding="utf-8") as outfile:
            nuova_riga = (f"{codice},{titolo},{autore},{mese},{anno}")
            outfile.write(nuova_riga)

    except FileNotFoundError:
        return None

    # Aggiornamento della struttura dati
    if anno not in album:
        album[anno] = {}
    # Creo la lista che rappresenta la foto
    foto_aggiunta = [titolo, autore, mese]
    # Inseriscola foto nel dizionario
    album[anno][codice] = foto_aggiunta
    # Ritorna il riferimento alla foto aggiunta
    return foto_aggiunta


def cerca_foto(album, codice):
    """Cerca una foto nell'album dato il codice"""
    for anno in album:
        foto = album[anno]
        if codice in foto:
            dati = foto[codice]
            titolo = dati[0]
            autore = dati[1]
            mese = dati[2]
            # Formattazione richiesta: "codice, titolo, autore, mese, anno"
            return f"{codice}, {titolo}, {autore}, {mese}, {anno}"
    return None


def elenco_foto_anno_per_titolo(album, anno):
    """Ordina i titoli delle foto di un dato anno in ordine alfabetico"""
    anno_str = str(anno)
    if anno_str not in album:
        return None

    # Recuperiamo il sotto-dizionario dell'anno
    foto_anno = album[anno_str]
    # Estraiamo il titolo da ciascuna foto
    titoli = []
    for codice in foto_anno:
        dati = foto_anno[codice]  # dati è la lista [titolo, autore, mese]
        titolo = dati[0]
        titoli.append(titolo)
    # Ordiniamo la lista in ordine alfabetico
    titoli.sort()
    return titoli


def main():
    album = []
    file_path = "album_fotografico.csv"

    while True:
        print("\n--- MENU ALBUM FOTOGRAFICO ---")
        print("1. Carica album da file")
        print("2. Aggiungi una nuova foto")
        print("3. Cerca una foto per codice")
        print("4. Elenco foto di un anno (ordinato per titolo)")
        print("5. Esci")

        scelta = input("Scegli un'opzione >> ").strip()

        if scelta == "1":
            while True:
                file_path = input("Inserisci il path del file da caricare: ").strip()
                album = carica_da_file(file_path)
                if album is not None:
                    break

        elif scelta == "2":
            if not album:
                print("Prima carica l'album da file.")
                continue

            codice = input("Codice della foto: ").strip()
            titolo = input("Titolo: ").strip()
            autore = input("Autore: ").strip()
            try:
                mese = int(input("Mese (1-12): ").strip())
                anno = int(input("Anno: ").strip())
            except ValueError:
                print("Errore: inserire valori numerici validi per mese e anno.")
                continue

            foto = aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path)
            if foto:
                print(f"Foto aggiunta con successo!")
            else:
                print("Non è stato possibile aggiungere la foto.")

        elif scelta == "3":
            if not album:
                print("L'album è vuoto.")
                continue

            codice = input("Inserisci il codice della foto da cercare: ").strip()
            risultato = cerca_foto(album, codice)
            if risultato:
                print(f"Foto trovata: {risultato}")
            else:
                print("Foto non trovata.")

        elif scelta == "4":
            if not album:
                print("L'album è vuoto.")
                continue

            try:
                anno = int(input("Inserisci l'anno da consultare: ").strip())
            except ValueError:
                print("Errore: inserire un valore numerico valido.")
                continue

            titoli = elenco_foto_anno_per_titolo(album, anno)
            if titoli is not None:
                print(f'\nFoto del {anno}:')
                print("\n".join([f"- {titolo}" for titolo in titoli]))
            else:
                print(f"Nessuna foto trovata per l'anno {anno}.")

        elif scelta == "5":
            print("Uscita dal programma...")
            break
        else:
            print("Opzione non valida. Riprova.")


if __name__ == "__main__":
    main()
