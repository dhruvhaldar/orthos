async function visualizeHoleStress() {
    // Visualize stress concentration around a hole (Sigma_y under Sigma_x tension)
    // Lekhnitskii / Isotropic approximation for visualization

    // Grid Setup
    const size = 100;
    const maxR = 3.0; // Plot up to 3*R
    const R = 1.0;

    const x = [];
    const y = [];
    const z = [];

    // Generate grid
    const axis = [];
    for (let i = 0; i < size; i++) {
        const val = -maxR + (2 * maxR * i) / (size - 1);
        axis.push(val);
    }

    // Calculate stress at each point
    for (let j = 0; j < size; j++) {
        const row = [];
        const yj = axis[j];

        for (let i = 0; i < size; i++) {
            const xi = axis[i];
            const r = Math.sqrt(xi*xi + yj*yj);

            if (r < R) {
                row.push(null); // Inside hole
            } else {
                // Polar coordinates
                const theta = Math.atan2(yj, xi); // -pi to pi

                // Stress Concentration Approximation
                // Hoop stress at boundary for Isotropic plate under Uniaxial Tension Sigma_inf = 1
                // Sigma_theta = 1 - 2*cos(2*theta)
                // At theta=90 (y-axis), sigma_theta = 3 (Tensile)
                // At theta=0 (x-axis), sigma_theta = -1 (Compressive)

                // Decay factor: (R/r)^2 approximation
                const decay = Math.pow(R/r, 2);
                const decay4 = Math.pow(R/r, 4);

                // Kirsch solution for Sigma_xx, Sigma_yy, Tau_xy
                // Here we just plot Sigma_yy (stress perpendicular to load direction at theta=90)
                // or just Von Mises / Max Principal.
                // Let's plot "Tangential Stress" Sigma_theta distribution mapped back?
                // Or simply the stress concentration factor roughly.

                // Simple visualization: Hoop stress projected
                const sigma_theta_boundary = 1 - 2 * Math.cos(2 * theta);
                const val = 1 + (sigma_theta_boundary - 1) * decay;

                row.push(val);
            }
        }
        z.push(row);
    }

    const data = [{
        z: z,
        x: axis,
        y: axis,
        type: 'heatmap',
        colorscale: 'Jet',
        zsmooth: 'best',
        colorbar: {title: 'Stress Concentration Factor'}
    }];

    const layout = {
        title: 'Stress Concentration (Isotropic Approx)',
        xaxis: {title: 'x / R', scaleanchor: 'y'},
        yaxis: {title: 'y / R'},
        autosize: true,
        height: 600
    };

    Plotly.newPlot('hole-plot', data, layout);
}
