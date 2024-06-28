repSetElement.contentEditable = "true";
repSetElement.addEventListener("input", function () {
    const newValue = repSetElement.textContent.trim(); // Get the trimmed content
    const [newSets, newReps] = newValue.split(' x ').map(val => parseInt(val, 10));

    // Check if both values are valid integers
    if (!isNaN(newSets) && !isNaN(newReps)) {
        updateRepSet(day, index, newSets, newReps);
    } else {
        // Handle invalid input, e.g., reset to previous valid values
        console.error("Invalid input for sets or reps:", newValue);
        // Optionally, provide user feedback or revert to previous values
    }
});
