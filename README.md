# multiple_renaming

*Multiple Renaming application in priority for MacOS.*

## Todo:
- Menu "Quitter" accelerator "command-w" sur Windows
- Mettre en place un système de **substitution** de texte :

    [n] - text = nom du fichier - text.py

### Treeview:
Ajouter les colonnes suivantes :
* [ ] Modifié le
* [ ] Crée le
* [ ] Emplacement

### Backup code

```python
def display_treeview(self):
        # Delete Treeview
        self.treeview.tree.delete(
                *self.treeview.tree.get_children())

        for f in self.filenames:
            old_name = os.path.basename(f)
            new_name = old_name
            
            # FIXME Make a greater converter
            size = f"{os.path.getsize(f)/1024:.2f} Mo"
            self.treeview.tree.insert(
                "", "end", text=old_name,
                values=(new_name, size))

        # NOTE For testing
        # cur = self.treeview.tree.get_children()
        # print(cur) # ('I001', 'I002', 'I003')
        # print(self.treeview.tree.item(cur[0]))
        # return dict:
        # {'text': 'statusbar.py', 'image': '', 'values': ['statusbar.py', '0.48 Mo'], 'open': 0, 'tags': ''}
```

```python
    def is_valid(self, d, i, P):
        # print(d, i, P)

        # if "[c]" in P:
        #     print(self.notebook.sbox_start.get())

        if "[n]" not in P:
            self.changed_filenames = [""] * len(self.initial_filenames)
            self.display_treeview()
        else:
            self.changed_filenames = self.initial_filenames[:]
            self.display_treeview(self.notebook.cbox_arguments.current())

        return True
```