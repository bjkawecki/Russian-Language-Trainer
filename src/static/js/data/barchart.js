function removePrevButton(today, end_date) {
    if (today == end_date) {
        const nextButton = document.getElementById('nextButton');
        if (nextButton) {
            nextButton.classList.add("hidden");
        }
    }
    else {
        nextButton.classList.remove("hidden");
    }
}

function createOrUpdateBarChart(data) {
    const {
        dates,
        initial_cards,
        in_progress_cards,
        mastered_cards,
        today,
        end_date
    } = data;

    removePrevButton(today, end_date);

    const isDarkMode = document.documentElement.classList.contains("dark");


    const trace_initial_cards = {
        x: dates,
        y: initial_cards,
        type: 'bar',
        name: "Neu",
        marker: {
            color: '#0c93ec',
        },
    };
    const trace_in_progress_cards = {
        x: dates,
        y: in_progress_cards,
        type: 'bar',
        name: "Aktiv",
        marker: {
            color: '#E63F66',
        },
    };
    const trace_mastered_cards = {
        x: dates,
        y: mastered_cards,
        name: "Gemeistert",
        type: 'bar',
        marker: {
            color: '#43C483',
        },
    };

    const layout = {
        title: 'Karten pro Tag',
        height: 160,
        width: 768,
        margin: {
            l: 40,
            r: 30,
            t: 30,
            b: 40
        },
        barmode: 'group', // 'stack' für gestapelte Balken
        bargap: 0.05, // Weniger Abstand zwischen Balken = breitere Balken (Standard ist 0.2–0.3)
        bargroupgap: 0.1, // Weniger Abstand zwischen Gruppen
        showlegend: true,
        paper_bgcolor: isDarkMode ? "#333C49" : "#FFFFFF",
        plot_bgcolor: isDarkMode ? "#333C49" : "#FFFFFF",
        font: {
            color: isDarkMode ? "#FFFFFF" : "#000000"
        },
        legend: {
            font: {
                color: isDarkMode ? "#FFFFFF" : "#000000"
            }
        },
        xaxis: {
            linecolor: isDarkMode ? "#637b94" : "#333C49",
            tickformat: '%-d.%-m.', // Format: 01.03.2024
            tickmode: "auto",
            nticks: 15,
        },
        yaxis: {
            linecolor: isDarkMode ? "#637b94" : "#333C49",
        },
        dragmode: false,  // Deaktiviert das Ziehen (Pan & Zoom)
    };

    // Plotly-Diagramm in den Container einfügen
    Plotly.newPlot('barchart-container', [trace_initial_cards, trace_in_progress_cards, trace_mastered_cards], layout, {
        displayModeBar: false
    });

    // Ladeindikator entfernen
    const loadingIndicator = document.querySelector('#barchart-container .loading-indicator');
    if (loadingIndicator) {
        loadingIndicator.remove();
    }

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

        Plotly.update('barchart-container', [], newLayout, {
            displayModeBar: false
        });

    }

    document.getElementById("toggle-color-mode").addEventListener("click", () => {
        rerender();
        console.log("event");
    });


}

document.addEventListener("DOMContentLoaded", async function () {
    try {
        // 📊 JSON-Daten per Fetch laden
        const response = await fetch(barchartDataUrl);
        const data = await response.json();

        // Diagramm erstellen oder aktualisieren
        createOrUpdateBarChart(data);

    } catch (error) {
        console.error("Fehler beim Laden der Daten:", error);
        document.getElementById("barchart-container").innerHTML =
            "<div class='text-white'>Fehler beim Laden der Daten</div>";
    }
});


document.addEventListener('DOMContentLoaded', function () {
    const prevButton = document.getElementById('prevButton');
    const nextButton = document.getElementById('nextButton');

    let offset = 0;

    prevButton.addEventListener('click', function () {
        navigate(++offset);
    });
    if (nextButton) {
        nextButton.addEventListener('click', function () {
            navigate(--offset);
        });
    }

    function navigate(offset) {
        const url = offset ? `${barchartDataUrl}?offset=${offset}` : `${barchartDataUrl}`;
        fetch(url)
            .then(response => response.json())
            .then(data => {
                createOrUpdateBarChart(data);
                document.getElementById("barchart-data-month").innerHTML =
                    `${data.month[0]} bis ${data.month[1]}`;
            })
            .catch(error => {
                console.error('Error fetching data:', error);
            });
    }
});
