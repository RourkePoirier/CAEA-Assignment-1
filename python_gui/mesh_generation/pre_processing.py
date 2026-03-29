import numpy as np

# Bascially the same as the example matlab code
# Need to make everything private

class PreProcessing:
    def __init__(self, data):
        n_element = data.n_element
        n_nodes = data.n_nodes
        X = data.X
        Y = data.Y
        E = data.E
        t = data.t
        v = data.v
        F = np.array(data.F)
        dzero = data.dzero
        NDU = data.NDU
        ncon = [(data.ncon1[i], data.ncon2[i], data.ncon3[i]) for i in range(n_element)]

        K = np.zeros((2*n_nodes, 2*n_nodes))
        for i in range(n_element):
            nodes = list(ncon[i])
            coords = [[X[n-1], Y[n-1]] for n in nodes]

            # Calculate Elemental Stiffness matrix
            A = self._calc_triangle_area(coords)
            B = self._calc_strain_displacement_matrix(coords, A)
            D = self._calc_strain_stress_matrix(E, v)
            KE = t * A * (B.T @ D @ B)

            ROC = []
            for n in nodes:
                ROC.append(2*n-2)  # x DOF
                ROC.append(2*n-1)  # y DOF

            for ix in range(len(ROC)):
                for jx in range(len(ROC)):
                    K[ROC[ix], ROC[jx]] += KE[ix, jx]
        
        KM = self._apply_boundary_conditions(K, dzero, NDU)
        self.U = np.linalg.solve(KM, F)

        (self.Sx, self.Sy, self.Sxy) = self._calculate_element_stresses(n_element, ncon, X, Y, self.U, E, v)
    
    def get_U(self):
        return self.U

    def get_Sx(self):
        return self.Sx

    def get_Sy(self):
        return self.Sy

    def get_Sxy(self):
        return self.Sxy

    # Returns KM
    def _apply_boundary_conditions(self, K, dzero, NDU):
        KM = K.copy()

        for k in range(NDU):
            n = int(dzero[k]) - 1
            KM[n, :] = 0
            KM[:, n] = 0
            KM[n, n] = 1

        return KM

    # Returns (Sx, Sy, Sxy)
    def _calculate_element_stresses(self, n_element, ncon, X, Y, U, E, v) -> tuple:
        Sx, Sy, Sxy = [], [], []

        D = self._calc_strain_stress_matrix(E, v)

        for i in range(n_element):
            nodes = list(ncon[i])
            coords = [[X[n-1], Y[n-1]] for n in nodes]

            A  = self._calc_triangle_area(coords)
            B  = self._calc_strain_displacement_matrix(coords, A)

            # Local displacement vector (6 DOF)
            Ue = np.array([U[dof] for n in nodes for dof in (2*n-2, 2*n-1)])

            sigma = D @ B @ Ue

            Sx.append(sigma[0])
            Sy.append(sigma[1])
            Sxy.append(sigma[2])

        return (Sx, Sy, Sxy)

    def _calc_triangle_area(self, coords):
        n = len(coords)
        area = 0
        for i in range(n):
            j = (i + 1) % n
            area += coords[i][0] * coords[j][1]
            area -= coords[j][0] * coords[i][1]
        return abs(area) / 2

    def _calc_strain_displacement_matrix(self, coords, A):
        n = len(coords)  # number of nodes
    
        # Extract x and y
        x = [coords[i][0] for i in range(n)]
        y = [coords[i][1] for i in range(n)]

        # Compute b and c coefficients for each node
        # b_i = y_j - y_k, c_i = x_k - x_j (cyclic)
        b = []
        c = []
        for i in range(n):
            j = (i + 1) % n
            k = (i + 2) % n
            b.append(y[j] - y[k])
            c.append(x[k] - x[j])

        # Assemble B matrix (3 x 2n)
        s = 1 / (2 * A)
        B = np.zeros((3, 2*n))
        for i in range(n):
            B[0, 2*i]   = s * b[i]   # epsilon_x
            B[1, 2*i+1] = s * c[i]   # epsilon_y
            B[2, 2*i]   = s * c[i]   # gamma_xy
            B[2, 2*i+1] = s * b[i]   # gamma_xy

        return B

    def _calc_strain_stress_matrix(self, E, v):
        s = E / (1 - v**2)
        return np.array([
            [s*1,   s*v,          0],
            [s*v,   s*1,          0],
            [  0,     0, s*(1-v)/2],
        ])
