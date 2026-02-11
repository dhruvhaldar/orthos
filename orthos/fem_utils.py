import numpy as np

def generate_rect_mesh(length, width, nx, ny):
    """
    Generates a structured quadrilateral mesh for a rectangular domain.
    Returns nodes and elements (connectivity).

    nodes: (N_nodes, 2) array of XY coordinates
    elements: (N_elements, 4) array of node indices (0-based)
    """
    x = np.linspace(0, length, nx+1)
    y = np.linspace(0, width, ny+1)
    X, Y = np.meshgrid(x, y)

    # Flatten in row-major order (default for numpy)?
    # meshgrid returns X where X[j, i] is x[i].
    # flatten() flattens row by row.
    # So index k corresponds to j=k//(nx+1), i=k%(nx+1)

    nodes = np.column_stack((X.flatten(), Y.flatten()))

    elements = []
    # Node indexing: i + j*(nx+1)
    for j in range(ny):
        for i in range(nx):
            n1 = i + j*(nx+1)
            n2 = (i+1) + j*(nx+1)
            n3 = (i+1) + (j+1)*(nx+1)
            n4 = i + (j+1)*(nx+1)
            elements.append([n1, n2, n3, n4])

    return nodes, np.array(elements)
