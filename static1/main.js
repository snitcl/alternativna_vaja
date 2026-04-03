function deleteNote(noteId) {
    fetch(`/delete/${noteId}`, { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            if(data.success){
                document.getElementById(`note-${noteId}`).remove();
            }
        })
        .catch(err => console.error("Napaka pri brisanju:", err));
}