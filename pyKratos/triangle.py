from __future__ import print_function, absolute_import, division 
import math
from numpy import *


class Triangle:

    def __init__(self, node_list):
        if(len(node_list) != 3):
            raise Exception("wrong number of nodes! should be 3!!")
        self.nodes = node_list

        for node in self.nodes:
            if(node.Id < 0):
                raise Exception("node with Id lesser than 0 found")

    # def Nodes(self):
        # return self.nodes

    def __getitem__(self, key):
        return self.nodes[key]
    
    def GetNumberOfNodes(self):
        return 3

    def ShapeFunctions(self, order=1):
        '''this function provides the shape function values, derivatives and integration_weight'''
        '''at the location of the gauss points. Order of integration is controlled'''
        '''by the optional parameter "order".'''
        '''N[gauss][i] contains the shape function of node i computed at the position of "gauss" '''
        '''derivatives[gauss][i,k] contains the derivative of node i, component k at the position of gauss '''
        '''weights[gauss] includes the integration weights, including the det of the jacobian, to be used '''
        '''at the gauss point'''
        derivatives = []
        weights = []
        Ncontainer = []

        x10 = self.nodes[1].coordinates[0] - self.nodes[0].coordinates[0]
        y10 = self.nodes[1].coordinates[1] - self.nodes[0].coordinates[1]

        x20 = self.nodes[2].coordinates[0] - self.nodes[0].coordinates[0]
        y20 = self.nodes[2].coordinates[1] - self.nodes[0].coordinates[1]

        detJ = x10 * y20 - y10 * x20

        DN_DX = zeros((3, 2), dtype=float)
        DN_DX[0, 0] = -y20 + y10
        DN_DX[0, 1] = x20 - x10
        DN_DX[1, 0] = y20
        DN_DX[1, 1] = -x20
        DN_DX[2, 0] = -y10
        DN_DX[2, 1] = x10

        DN_DX /= detJ

        if(order == 1):  # give back 1 single integration point
            one_third = 1.0 / 3.0
            Ncontainer = [array([one_third, one_third, one_third])]

            Area = 0.5 * detJ
            weights = [Area]
            derivatives = [DN_DX]

        elif(order == 2):  # gives back 3 integration points
            one_sixt = 1.0 / 6.0
            two_third = 2.0 / 3.0
            Ncontainer.append(array([one_sixt, one_sixt, two_third]))
            Ncontainer.append(array([one_sixt, two_third, one_sixt]))
            Ncontainer.append(array([two_third, one_sixt, one_sixt]))

            weights = [one_sixt * detJ, one_sixt * detJ, one_sixt * detJ]

            derivatives = [DN_DX, DN_DX, DN_DX]
        else:
            raise Exception("integration order not implemented")

        return [Ncontainer, derivatives, weights]
