document.addEventListener("DOMContentLoaded", async function () {
    try {
        // 📊 JSON-Daten per Fetch laden
        const response = await fetch(heatmapDataUrl);
        const data = await response.json();

        const {
            weeks,
            hovertext,
            start_date,
        } = data;

        var container = document.getElementById("heatmap-container");


        // 🗓️ Startdatum (vom Server)
        const firstDay = new Date(start_date);

        // 📆 Monatslabels & Positionen vorbereiten
        const monthLabels = ["Jan", "Feb", "Mär", "Apr", "Mai", "Jun", "Jul", "Aug", "Sep", "Okt", "Nov", "Dez"];
        const monthPositions = [];

        // Der aktuelle Monat (wir möchten bis zum aktuellen Monat und nicht weiter)
        let currentMonth = firstDay.getMonth(); // Get the current month (0-11)
        let nextMonth = (currentMonth + 1) % 12; // Nächster Monat (Zyklen von Januar bis Dezember)

        // Dynamisch die Monatslabels neu ordnen, sodass der aktuelle Monat an erster Stelle kommt
        const dynamicMonthLabels = [...monthLabels.slice(nextMonth), ...monthLabels.slice(0, nextMonth)];

        // Berechne die Monatspositionen (auch für die ersten Monate des Folgejahres)
        for (let i = 0; i < 12; i++) { // Gehe über 12 Monate hinaus (bis März des nächsten Jahres)
            let monthIndex = (nextMonth + i) % 12; // Berechne den Monatsindex mit Offset für den aktuellen Monat
            let firstOfMonth = new Date(firstDay.getFullYear(), monthIndex, 1);

            // Wenn der Monat über Dezember hinausgeht, berücksichtige das nächste Jahr
            if (monthIndex < nextMonth) {
                firstOfMonth.setFullYear(firstDay.getFullYear() + 1);
            }

            // Berechne die Differenz in Tagen
            let diffDays = Math.floor((firstOfMonth - firstDay) / (24 * 60 * 60 * 1000)); // Unterschied in Tagen

            // Berechne die Woche des Monats (Differenz in Tagen geteilt durch 7, dann +2)
            let monthPosition = Math.floor(diffDays / 7); // Jetzt nur noch den Index der Woche berechnen
            // Füge die berechnete Monatsposition hinzu
            monthPositions.push(monthPosition);
        }

        const isDarkMode = document.documentElement.classList.contains("dark");

        // 📊 Plotly-Diagramm erstellen
        const fig = {
            data: [{
                z: weeks,
                zmin: 0,
                zmax: 100,
                type: 'heatmap',
                colorscale: isDarkMode ? [
                    [null, 'rgb(51,61,72)'],
                    [0.0, "rgb(35,40,48)"],
                    [0.00000000001, "#d4efff"],
                    [0.1, "#b2e5ff"],
                    [0.2, "#7dd7ff"],
                    [0.3, "#40beff"],
                    [0.4, "#149cff"],
                    [0.5, "#007aff"],
                    [0.6, "#0062ff"],
                    [0.7, "#0052d6"],
                    [0.8, "#0846a0"],
                    [1.0, "#0a2b61"],
                ] : [
                    [null, 'white'],
                    [0.0, "#d4dbe3"],
                    [0.00000000001, "#d4efff"],
                    [0.1, "#b2e5ff"],
                    [0.2, "#7dd7ff"],
                    [0.3, "#40beff"],
                    [0.4, "#149cff"],
                    [0.5, "#007aff"],
                    [0.6, "#0062ff"],
                    [0.7, "#0052d6"],
                    [0.8, "#0846a0"],
                    [1.0, "#0a2b61"],
                ],
                showscale: true,
                xgap: 2,
                ygap: 2,
                hovertext: hovertext,
                hoverinfo: "text",
                colorbar: {
                    outlinewidth: 0,  // Entfernt den Rand
                    bgcolor: "rgba(0,0,0,0)",  // Transparenter Hintergrund
                }
            }],
            layout: {
                title: null,
                xaxis: {
                    tickmode: "array",
                    tickvals: monthPositions, // 🛠 Verwendet `monthPositions`
                    ticktext: dynamicMonthLabels,
                    showgrid: false,
                    zeroline: false,
                    showticklabels: true,
                },
                yaxis: {
                    tickmode: "array",
                    tickvals: [0, 1, 2, 3, 4, 5, 6],
                    ticktext: ["So", "Mo", "Di", "Mi", "Do", "Fr", "Sa"], // ✅ Sonntag als Start
                    showgrid: false,
                    zeroline: false,
                    showticklabels: true,
                    autorange: "reversed",
                },
                width: 768,
                height: 160,
                margin: {
                    l: 40,
                    r: 0,
                    t: 30,
                    b: 30
                },
                paper_bgcolor: isDarkMode ? "#333C49" : "#FFFFFF",
                plot_bgcolor: isDarkMode ? "#333C49" : "#FFFFFF",
                dragmode: false,  // Deaktiviert das Ziehen (Pan & Zoom)
                font: {
                    color: isDarkMode ? "#FFFFFF" : "#000000"
                },
                legend: {
                    frame: 0,
                    font: {
                        color: isDarkMode ? "#FFFFFF" : "#000000",
                    },
                    bordercolor: "rgba(0,0,0,0)", // Unsichtbarer Rand
                    bgcolor: "rgba(0,0,0,0)"
                }
            }
        };

        // 🎨 Plotly zeichnen
        Plotly.newPlot('heatmap-container', fig.data, fig.layout, {
            displayModeBar: false
        });

        // Ladeindikator entfernen
        const loadingIndicator = document.querySelector('#heatmap-container .loading-indicator');
        if (loadingIndicator) {
            loadingIndicator.remove();
        }
    } catch (error) {
        console.error("Fehler beim Laden der Daten:", error);
        document.getElementById("heatmap-container").innerHTML =
            "<div class='text-white'>Fehler beim Laden der Daten</div>";
    }



    function rerenderHeatmap() {
        const isDarkMode = document.documentElement.classList.contains("dark");

        const newLayout = {
            paper_bgcolor: isDarkMode ? "#333C49" : "#FFFFFF",
            plot_bgcolor: isDarkMode ? "#333C49" : "#FFFFFF",
            font: {
                color: isDarkMode ? "#FFFFFF" : "#000000"
            },
            legend: {
                font: {
                    color: isDarkMode ? "#FFFFFF" : "#000000",
                }
            }
        };

        Plotly.update('heatmap-container', [], newLayout, {
            displayModeBar: false
        });


        const newColorScale = isDarkMode ? [
            [null, 'rgb(51,61,72)'],
            [0.0, "rgb(35,40,48)"],
            [0.00000000001, "#d4efff"],
            [0.1, "#b2e5ff"],
            [0.2, "#7dd7ff"],
            [0.3, "#40beff"],
            [0.4, "#149cff"],
            [0.5, "#007aff"],
            [0.6, "#0062ff"],
            [0.7, "#0052d6"],
            [0.8, "#0846a0"],
            [1.0, "#0a2b61"],
        ] : [
            [null, 'white'],
            [0.0, "#d4dbe3"],
            [0.00000000001, "#d4efff"],
            [0.1, "#b2e5ff"],
            [0.2, "#7dd7ff"],
            [0.3, "#40beff"],
            [0.4, "#149cff"],
            [0.5, "#007aff"],
            [0.6, "#0062ff"],
            [0.7, "#0052d6"],
            [0.8, "#0846a0"],
            [1.0, "#0a2b61"],
        ];

        Plotly.restyle("heatmap-container", { colorscale: [newColorScale] });


    }


    document.getElementById("toggle-color-mode").addEventListener("click", () => {
        rerenderHeatmap();
    });




});
