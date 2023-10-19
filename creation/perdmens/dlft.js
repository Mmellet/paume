
function generateSentence() {
    const options = ["il faut que", "Ça fait longtemps que", "le dernier mardi", "C'est parce que", "C'est depuis février que", "Comment on va faire pour que"];
    const sujets = ["les casseroles", "les enfants", "les punaises", "le glissement", "on", "tu", "je", "les infirmières", "la neurologue", "mes lunettes"];
    const verbes = ["ont", "aillent", "amènent", "s'accouplent", "tiens pas", "repartent", "se sera vu", "lui diras", "rigolai", "passe", "aimerai comprendre", "trouve", "arroser", "veux", "peux le faire", "viens d'arriver", "étaient"];
    const objets = ["à l'école", "peu", "tôt", "traumatiques", "troumatique", "de même couleur", "à la maison", "pleins d'examens", "ce qui bloque", "une cigarette", "tout seul", "les plantes", "à l'hôpital", "là"];
    const ponctuations = [".", "...", "?", ":"]

    const randomNumber = Math.random();

    const que = randomNumber < 0.5
        ? options[Math.floor(Math.random() * options.length)]
        : "";
    const qui = randomNumber < 0.9
        ? sujets[Math.floor(Math.random() * sujets.length)]
        : "";
    const quoi = randomNumber < 0.8
        ? verbes[Math.floor(Math.random() * verbes.length)]
        : "";
    const sur = randomNumber < 0.7
        ? objets[Math.floor(Math.random() * objets.length)]
        : "";
    const ponctuation = randomNumber < 0.9
        ? ponctuations[Math.floor(Math.random()* ponctuations.length)]
        : "";

    const sentence = `${que} ${qui} ${quoi} ${sur}${ponctuation}`;
    return sentence;
}

// Générez une phrase aléatoire
const sentence = generateSentence();

// Sélectionnez l'élément par son ID
const generatedSentenceElement = document.getElementById("sujet-de-discussion");

// Insérez la phrase générée dans l'élément
generatedSentenceElement.textContent = sentence;



function insertRandomPhrase() {
    const phrase = generateSentence();
    const phraseElement = document.createElement("p");
    phraseElement.textContent = phrase;

    // Appliquez des styles et une classe d'animation
    phraseElement.style.position = "absolute";
    phraseElement.style.left = `${Math.random() * window.innerWidth}px`; // Position horizontale aléatoire
    phraseElement.style.top = `${Math.random() * window.innerHeight}px`; // Position verticale aléatoire
    phraseElement.style.opacity = 0; // Opacité initial à 0
    phraseElement.style.fontSize = `${Math.floor(Math.random() * 20) + 12}px`; // Taille de police aléatoire entre 12 et 32px
    phraseElement.classList.add("fade-in"); // Ajoutez une classe CSS pour l'animation

    

    document.body.appendChild(phraseElement);

    // Démarrez l'animation après un léger délai
    setTimeout(() => {
        phraseElement.style.opacity = 1; // Augmentez progressivement l'opacité
    }, 100); // Léger délai avant le début de l'animation

    
    // Insérez une nouvelle phrase après un délai aléatoire (entre 2 et 5 secondes)
    const randomDelay = Math.floor(Math.random() * 2000) + 2000; // Délai en millisecondes
    setTimeout(insertRandomPhrase, randomDelay);
}

// Appelez la fonction pour commencer l'insertion de phrases à la volée
insertRandomPhrase();
