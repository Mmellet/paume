package main

import (
    "strings"
    "regexp"
	"encoding/json"
    "html/template"
	"os"
)

func main() {
	// Définition du contenu du template HTML
	htmlTemplate := `
    {{ define "index" }}

    <h1>Index thématique</h1>

    {{/* Obtenez la liste de toutes les pages du site */}}
    {{ $pages := .Site.RegularPages }}


    {{/* Parcourez chaque page pour trouver les thématiques */}}
    {{ range $pages }}
        {{ $page := . }}
        {{ with .Params.themes }}
            {{ range . }}
                <p>Thématique : {{ . }}</p>
                {{/* Obtenez les paragraphes contenant cette thématique sur la page */}}
                {{ $paragraphs := $page.Plain | findThemeParagraphs . $themeUtils }}

                {{/* Affichez les paragraphes correspondants avec les liens vers la page */}}
                {{ range $paragraphs }}
                    <p>
                        <a href="{{ $page.RelPermalink }}">
                            {{ $page.Title }}
                        </a> - {{ . }}
                    </p>
                {{ end }}
            {{ end }}
        {{ end }}
    {{ end }} 
{{ end }}

	`

	// Définition des données pour le template
	data := struct {
		Title   string
		Heading string
		Content string
	}{
		Title:   "Mon premier fichier HTML généré en Go",
		Heading: "Bienvenue dans mon site",
		Content: "Ceci est un exemple de génération de contenu HTML en utilisant Go.",
	}

	// Création du template
	tmpl := template.Must(template.New("myTemplate").Parse(htmlTemplate))

	// Génération du contenu HTML en utilisant les données fournies
	err := tmpl.Execute(os.Stdout, data)
	if err != nil {
		panic(err)
	}
}

	
func fromString(data string) (map[string]interface{}, error) {
		var result map[string]interface{}
		err := json.Unmarshal([]byte(data), &result)
		if err != nil {
			return nil, err
		}
		return result, nil
	}
	
var themeRegex = regexp.MustCompile(`\[theme:(.*?)\]`)

func findThemeParagraphs(content string, theme string) []string {
    paragraphs := strings.Split(content, "\n\n")
    themeParagraphs := make([]string, 0)

    for _, paragraph := range paragraphs {
        if themeRegex.MatchString(paragraph) {
            themes := themeRegex.FindAllStringSubmatch(paragraph, -1)
            for _, t := range themes {
                if t[1] == theme {
                    themeParagraphs = append(themeParagraphs, paragraph)
                    break
                }
            }
        }
    }

    return themeParagraphs
}

