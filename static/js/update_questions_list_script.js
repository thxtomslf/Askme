window.onclick = (event) => {
    let idCounter = 0;
    let baseName = 'like_dislike_button_';
    let likeDislikeGroups = document.querySelectorAll(".like_dislike_buttons_group");

    // Set their ids
    for (let i = 0; i < likeDislikeGroups.length; i++) {
        let inputs = likeDislikeGroups[i].querySelectorAll("input");
        inputs[0].name = baseName + i;
        inputs[1].name = baseName + i;

        inputs[0].id = baseName + idCounter;
        idCounter++;
        inputs[1].id = baseName + idCounter;
        idCounter++;

        const attribute0 = document.createAttribute("for");
        attribute0.value = inputs[0].id;
        const attribute1 = document.createAttribute("for");
        attribute1.value = inputs[1].id;

        let labels = likeDislikeGroups[i].querySelectorAll("label");
        document.createAttribute("for")
        labels[0].setAttributeNode(attribute0);

        labels[1].setAttributeNode(attribute1);

    }
};