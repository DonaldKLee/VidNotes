function copy_note_link() {
    link = document.getElementById("note_link");
    link.select();
    link.setSelectionRange(0, 100)
    document.execCommand("copy");
}