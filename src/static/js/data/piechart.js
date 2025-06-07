// Funktion zum Erstellen und Aktualisieren des Diagramms
function createOrUpdatePieChart(data) {
    const {
        labels,
        values
    } = data;

    if (labels.length === 0) {
        document.getElementById("piechart-container").innerHTML =
            "<div class='text-white'>Keine Daten verfügbar</div>";
        return;
    }

    // 📊 Sicherstellen, dass alle Labels auch angezeigt werden
    const allLabels = ["Neu", "Aktiv", "Gemeistert"]; // Hier alle gewünschten Labels hinzufügen

    // Sicherstellen, dass wir Werte für jedes Label haben
    const counts = {};
    values.forEach((value, index) => {
        counts[labels[index]] = value;
    });

    // Generiere die vollständige Liste der Werte (inkl. 0 für nicht vorhandene Daten)
    const completeValues = allLabels.map(label => counts[label] || 0);

    const isDarkMode = document.documentElement.classList.contains("dark");
    const total = Object.values(completeValues).reduce((a, b) => a + b, 0);
    // 📊 Trace und Layout für Plotly
    const trace = {
        labels: allLabels,
        values: completeValues,
        type: 'pie',
        textposition:
            Object.values(completeValues).map((value) =>
                (value / total) * 100 > 4 ? "inside" : "none"  // Only show if segment > 4%
            ) ?? "none",
        textinfo: "percent",
        texttemplate: "%{percent:.1%}", // Prozentwerte auf eine Dezimalstelle runden
        textfont: {
            size: 14,
            color: isDarkMode ? "#FFFFFF" : "#000000",
        },
        hovertemplate: "%{label}: %{value} Karten (%{percent})<extra></extra>",
        marker: {
            colors: ["#0c93ec", "#e73e66", "#43c483"]
        },
    };

    const layout = {
        height: 160,
        width: 300,
        margin: {
            l: 0,
            r: 0,
            t: 30,
            b: 15
        },
        paper_bgcolor: isDarkMode ? "#333C49" : "#FFFFFF",
        plot_bgcolor: isDarkMode ? "#333C49" : "#FFFFFF",
        font: {
            color: isDarkMode ? "#FFFFFF" : "#000000"
        },
        showlegend: true,
        legend: {
            x: 1.2, // Platzierung rechts vom Diagramm
            y: 0.5,
            font: {
                size: 14,
                color: isDarkMode ? "#FFFFFF" : "#000000"
            }
        }
    };

    // Diagramm erstellen oder aktualisieren
    Plotly.newPlot('piechart-container', [trace], layout, {
        displayModeBar: false
    });

    // Ladeindikator entfernen
    const loadingIndicator = document.querySelector('#piechart-container .loading-indicator');
    if (loadingIndicator) {
        loadingIndicator.remove();
    }
}

// Funktion zum Abrufen der Daten und Erstellen des Diagramms
document.addEventListener("DOMContentLoaded", async function () {
    try {
        // 📊 JSON-Daten per Fetch laden
        const response = await fetch(piechartDataUrl);
        const data = await response.json();

        // Diagramm erstellen oder aktualisieren
        createOrUpdatePieChart(data);

    } catch (error) {
        console.error("Fehler beim Laden der Daten:", error);
        document.getElementById("piechart-container").innerHTML =
            "<div class='text-white'>Fehler beim Laden der Daten</div>";
    }
});

function rerender() {
    const isDarkMode = document.documentElement.classList.contains("dark");

    const newLayout = {
        paper_bgcolor: isDarkMode ? "#333C49" : "#FFFFFF",
        plot_bgcolor: isDarkMode ? "#333C49" : "#FFFFFF",
        font: {
            color: isDarkMode ? "#FFFFFF" : "#000000"
        },
        legend: {
            font: {
                color: isDarkMode ? "#FFFFFF" : "#000000"
            }
        }
    };

    const newTextFont = {
        "textfont.color": isDarkMode ? "#FFFFFF" : "#000000"
    };

    Plotly.update('piechart-container', [], newLayout, {
        displayModeBar: false
    });

    Plotly.restyle("piechart-container", newTextFont);

}

document.getElementById("toggle-color-mode").addEventListener("click", () => {
    rerender();
});


const radioButtons = document.getElementsByName("course");
radioButtons.forEach(button => {
    button.addEventListener("change", async function () {
        const courseId = document.querySelector('input[name="course"]:checked').value; // Ausgewählte Kurs-ID
        // URL mit dem entsprechenden Kurs-Filter
        const url = courseId ? `${piechartDataUrl}?course=${courseId}` : `${piechartDataUrl}`;

        try {
            // Daten per Fetch abrufen
            const response = await fetch(url);
            const data = await response.json();
            // Diagramm mit neuen Daten erstellen oder aktualisieren
            createOrUpdatePieChart(data);

        } catch (error) {
            console.error("Fehler beim Abrufen der Daten:", error);
            document.getElementById("piechart-container").innerHTML =
                "<div class='text-white'>Fehler beim Laden der Daten</div>";
        }
    });
});
