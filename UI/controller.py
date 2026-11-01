import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model


    def handleCreaGrafo(self, e):
        self._view._txt_result.controls.clear()




        # 3. grafo
        self._model.buildGraph()

        if self._model.getNumNodi() == 0:
            self._errore("Nessun genere acquistato dai clienti di questo paese.")
            return

        # 4. stampo
        self._view._txt_result.controls.append(ft.Text("Grafo creato correttamente!", color="green"))
        self._view._txt_result.controls.append(ft.Text(f"Numero di nodi: {self._model.getNumNodi()}"))
        self._view._txt_result.controls.append(ft.Text(f"Numero di archi: {self._model.getNumArchi()}"))
        self._view._ddAlbum.options.clear()
        self._view._ddAlbum.value = None
        for a in self._model.getNodiOrdinati():
            self._view._ddAlbum.options.append(ft.dropdown.Option(key=str(a.id), text=str(a)))
        self._view.update_page()

    def handleStampaInfo(self, e):
        self._view._txt_result.controls.clear()

        if self._model.getNumNodi() == 0:
            self._errore("Crea prima il grafo!")
            return

        res = self._view._txt_result.controls

        # artista con grado maggiore

        # componenti connesse
        nComp, dimMax = self._model.getComponenti()
        res.append(ft.Text(f"Numero di componenti connesse: {nComp}"))
        res.append(ft.Text(f"Dimensione della componente più grande: {dimMax}"))
        # 10 archi di peso maggiore
        res.append(ft.Text("I 10 archi di peso maggiore:"))
        for a,b  in self._model.getInfoComponentePiuGrande():
            res.append(ft.Text(f"     {a} : {b} brani"))
        self._view.update_page()

    def handleSelezione(self, e):
        self._view._txt_result.controls.clear()

        # 1. grafo creato?
        if self._model.getNumNodi() == 0:
            self._view._txt_result.controls.append(ft.Text("Crea prima il grafo!", color="red"))
            self._view.update_page()
            return

        # 2. album di partenza
        if self._view._ddAlbum.value is None:
            self._view._txt_result.controls.append(ft.Text("Seleziona un album di partenza!", color="red"))
            self._view.update_page()
            return
        partenza = self._model.getAlbum(int(self._view._ddAlbum.value))
        if partenza is None:
            self._view._txt_result.controls.append(ft.Text("Album non presente nel grafo!", color="red"))
            self._view.update_page()
            return

        # 3. N
        try:
            N = int(self._view._txtInN.value)
        except (ValueError, TypeError):
            self._view._txt_result.controls.append(ft.Text("N deve essere un numero intero!", color="red"))
            self._view.update_page()
            return
        nComp = self._model.getNumComponenti()
        if N < 1 or N > nComp:
            self._view._txt_result.controls.append(
                ft.Text(f"N deve essere compreso tra 1 e {nComp} (numero di componenti)!", color="red"))
            self._view.update_page()
            return

        # 4. ricorsione
        selezione, totBrani = self._model.getSelezione(partenza, N)

        if len(selezione) == 0:
            self._view._txt_result.controls.append(ft.Text("Nessuna selezione trovata."))
            self._view.update_page()
            return

        # 5. stampo
        self._view._txt_result.controls.append(ft.Text(f"Selezione a partire da {partenza}:", color="green"))
        for a in sorted(selezione, key=lambda x: x.title):
            self._view._txt_result.controls.append(
                ft.Text(f"     {a.title} – genere {a.generi} – {len(a.brani)} brani"))
        self._view._txt_result.controls.append(ft.Text(f"Numero totale di album: {len(selezione)}"))
        self._view._txt_result.controls.append(ft.Text(f"Numero complessivo di brani: {totBrani}"))

        self._view.update_page()

    def _errore(self, messaggio):
            self._view._txt_result.controls.append(ft.Text(messaggio, color="red"))
            self._view.update_page()