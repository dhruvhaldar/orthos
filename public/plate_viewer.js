async function solvePlate() {
    // In a real app, this would fetch from /api/plate/bending

    const a = 1.0;
    const b = 1.0;
    // Get load from input
    const loadInput = document.getElementById('plate-load');
    const load = loadInput ? parseFloat(loadInput.value) : 1000;

    const x = [];
    const y = [];
    const z = [];

    const steps = 50;
    for (let i = 0; i <= steps; i++) {
        x.push(i * a / steps);
        y.push(i * b / steps);
    }

    for (let j = 0; j <= steps; j++) {
        const row = [];
        for (let i = 0; i <= steps; i++) {
            const xi = i * a / steps;
            const yi = j * b / steps;

            // Simplified deflection for [0/90] plate (stiffer in x -> less curvature?)
            // Navier solution approximation (m=1, n=1 term)
            // w = W11 * sin(pi x / a) * sin(pi y / b)

            const w = (load / 10000) * Math.sin(Math.PI * xi / a) * Math.sin(Math.PI * yi / b);
            row.push(w);
        }
        z.push(row);
    }

    const data = [{
        x: x,
        y: y,
        z: z,
        type: 'surface',
        colorscale: 'Viridis'
    }];

    const layout = {
        title: `Plate Deflection (Load: ${load} Pa)`,
        scene: {
            xaxis: {title: 'Length (m)'},
            yaxis: {title: 'Width (m)'},
            zaxis: {title: 'Deflection (m)'}
        },
        autosize: true,
        height: 600
    };

    Plotly.newPlot('plate-plot', data, layout);
}
