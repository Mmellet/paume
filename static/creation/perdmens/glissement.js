
let letterCount = 1; // Commencez par supprimer 3 lettres

function removeRandomOneLetter() {
    const letters = document.querySelectorAll("p, h1, h2, span, div, style, summary, details"); // Sélectionnez les éléments où vous voulez supprimer des lettres
    if (letters.length > 0) {
        for (let i = 0; i < letterCount; i++) {
            const randomIndex = Math.floor(Math.random() * letters.length);
            const randomLetter = letters[randomIndex];
            if (randomLetter.textContent.length > 0) {
                randomLetter.textContent = randomLetter.textContent.slice(0, -1); // Supprimez la dernière lettre du contenu
            }
        }
    } 
}

// Démarrez le script après 20 secondes
setTimeout(function() {
    // Appelez la fonction pour supprimer des lettres toutes les 5 secondes (par exemple)
    setInterval(removeRandomOneLetter, 5000); // Supprimez des lettres toutes les 5 secondes (ajustez l'intervalle selon vos besoins)
}, 10000); // Attendre 10 secondes (20000 millisecondes) avant de lancer le script



function removeRandomElement() {
    const elements = document.querySelectorAll("*"); // Sélectionnez tous les éléments de la page
    if (elements.length > 0) {
        const randomIndex = Math.floor(Math.random() * elements.length); // Générez un index aléatoire
        const randomElement = elements[randomIndex]; // Sélectionnez l'élément à supprimer
        randomElement.remove(); // Supprimez l'élément
    }
}

// Démarrez le script après 20 secondes
setTimeout(function() {
    // Appelez la fonction pour supprimer un élément toutes les 5 secondes (par exemple)
    setInterval(removeRandomElement, 5000); // Supprimez un élément toutes les 5 secondes (ajustez l'intervalle selon vos besoins)
}, 60000); // Attendre 20 secondes (20000 millisecondes) avant de lancer le script
