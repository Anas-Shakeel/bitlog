document.addEventListener("DOMContentLoaded", () => {
    // Get Elements
    const input = document.getElementById("tagsInput");
    const container = document.getElementById("tagsContainer");

    // Listen for Enter Keypresses on Input
    input.addEventListener("keypress", (event) => {
        if (event.key === "Enter" || event.key === " ") {
            event.preventDefault();
            const tag = input.value.trim();
            if (tag) {
                // Create the Tag
                createTag(container, tag);

                // Add a hidden input for form submission
                const hidden_input = document.createElement("input");
                hidden_input.type = "hidden";
                hidden_input.name = "all_tags";
                hidden_input.value = tag;
                document.getElementById("tagsForm").appendChild(hidden_input);
            }
            input.value = "";
        }
    });

    // Remove Event
    container.addEventListener("click", (event) => {
        if (event.target.classList.contains("tag")) {
            container.removeChild(event.target);
        }
    });
});

// For Custom File Upload Buttons
// It changes the innerHTML of id=filename element
function sub(obj) {
    let filename = obj.value.split("\\");
    document.getElementById("filename").innerHTML = filename[filename.length - 1];
    // document.myForm.submit();
    event.preventDefault();
}

// Function to create tag element
function createTag(container, tag) {
    const span = document.createElement("span");
    span.textContent = tag;
    span.className = "tag-pill";

    // Delete Button for Each Tag
    span.onclick = () => removeTag(tag, span);

    container.appendChild(span);
}

// Function to remove tag element
function removeTag(tag, tag_element) {
    // Remove visible tag
    tag_element.remove();
    // Remove hidden input tag
    document.querySelector(`input[name="all_tags"][value="${tag}"]`).remove();
}
