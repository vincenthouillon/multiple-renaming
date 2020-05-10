# multiple_renaming

*Multiple Renaming application in priority for MacOS.*


## Todo:
- Ajouter support multilangues [FR/EN]
- Créer une page GitHubIo
- Menu :
    - Paramètres
    - A propos
    - Aide
- Mémorisation des paramètres
- Enregistrement de profil de renommage


### Treeview:
Ajouter les colonnes suivantes :
* [x] Modifié le
* [x] Crée le
* [x] Emplacement

```python
def input_filename(self, P):
    """Check the content of the input widget to verify that it is valid
    with the rules of the application.

    Arguments:
        P {str} -- Value of the entry if the edit is allowed

    Returns:
        str -- Output text processed by application rules
    """

    date_format = self.module.date_formatting(self.params.cbox_date.get())

    temp_filename = list()

    for fn in self.initial_filenames:
        temp_filename.append(os.path.splitext(os.path.basename(fn))[0])

    if "[n]" in P:
        for index, filename in enumerate(temp_filename):
            self.changed_filenames[index] = P.replace("[n]", filename)
    else:
        for index, dirname in enumerate(self.initial_filenames):
            filename, _ = os.path.splitext(os.path.basename(dirname))
            self.changed_filenames[index] = P

    # Option [nx]: Name from first character
    if re.findall(r"\[n\d+\]", P):
        re_findall = re.findall(r"\[n\d+\]", P)
        nx = re_findall[0][2:len(re_findall)-2]
        for index, filename in enumerate(temp_filename):
            self.changed_filenames[index] = P.replace(
                re_findall[0], filename[0:int(nx)])

    # Option [n-x]: Name from last character
    if re.findall(r"\[n-\d+\]", P):
        re_findall = re.findall(r"\[n-\d+\]", P)
        nx = re_findall[0][3:len(re_findall)-2]
        for index, filename in enumerate(temp_filename):
            if len(filename) >= int(nx):
                self.changed_filenames[index] = P.replace(
                    re_findall[0], filename[len(filename)-int(nx):])
            else:
                self.changed_filenames[index] = filename

    # Option [n,x]: Name from n character
    if re.findall(r"\[n,\d+\]", P):
        re_findall = re.findall(r"\[n,\d+\]", P)
        nx = re_findall[0][3:len(re_findall)-2]
        for index, filename in enumerate(temp_filename):
            if len(filename) >= int(nx):
                self.changed_filenames[index] = P.replace(
                    re_findall[0], filename[int(nx)-1:len(filename)])
            else:
                self.changed_filenames[index] = filename

    if "[c]" in P:
        counter = int(self.params.sbox_start.get())
        for index, filename in enumerate(self.changed_filenames):
            formated_counter = f"{counter:0{self.params.sbox_len.get()}}"
            self.changed_filenames[index] = filename.replace(
                "[c]", formated_counter)
            counter += int(self.params.sbox_step.get())

    if "[d]" in P:
        for index, filename in enumerate(self.changed_filenames):
            self.changed_filenames[index] = filename.replace(
                "[d]", date_format)

    self.display_treeview()
    return True

def display_treeview(self, argument=None):
    """Management of the display of the treeview.

    Keyword Arguments:
        argument {int} -- Key to the arguments, to transform text into
        capital letters for example. (default: {None})
    """
    # Delete treeview
    self.treeview.tree.delete(*self.treeview.tree.get_children())

    for initial, changed in zip(
            self.initial_filenames, self.changed_filenames):
        
        old_name = os.path.basename(initial)
        new_name = os.path.basename(changed)
        
        extension = os.path.splitext(old_name)[1]
        name_modified = new_name + extension

        name_modified = self.module.arguments_parsing(
            argument, new_name, extension
        )

        if platform.system() == "Windows":
            self.module.check_valid_characters_filename(name_modified)

        date_creation = datetime.fromtimestamp(os.path.getmtime(initial))
        date_creation_formated = datetime.strftime(
            date_creation, "%Y/%m/%d %H:%M:%S")

        date_modified = datetime.fromtimestamp(os.path.getctime(initial))
        date_modified_formated = datetime.strftime(
            date_modified, "%Y/%m/%d %H:%M:%S")

        location = os.path.abspath(initial)

        size = self.module.get_human_readable_size(
            os.path.getsize(initial))

        # Find duplicate files
        duplicate_files = set(
            [x for x in self.changed_filenames
                if self.changed_filenames.count(x) > 1])

        if os.path.splitext(name_modified)[0] in [x for x in duplicate_files]:
            self.treeview.tree.insert(
                "", "end",
                text=old_name,
                values=(name_modified, size, date_creation_formated,
                        date_modified_formated, location), tag="ERR")
            self.activate_button("disabled")
            continue
        else:
            self.treeview.tree.insert(
                "", "end",
                text=old_name,
                values=(name_modified, size, date_creation_formated,
                        date_modified_formated, location))
            self.activate_button("normal")
```


```python
self.prohibited_filename = ["CON", "PRN", "AUX", "NUL", "COM1", "COM2",
                            "COM3", "COM4", "COM5", "COM6", "COM7", "COM8",
                            "COM9", "LPT1", "LPT2", "LPT3", "LPT4", "LPT5",
                            "LPT6", "LPT7", "LPT8", "LPT9"]
```