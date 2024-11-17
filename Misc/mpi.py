'''
Notes:

mpiexec -n 2 --host nate-desktop,ubuntu python testing_mpi.py

'''

from mpi4py import MPI

comm = MPI.COMM_WORLD

rank = comm.Get_rank()

size = comm.Get_size()


if (rank == 0):

    data = [1,2,3,4,5]
    comm.send(data, dest=1, tag=11)
    print('From rank 0: \n' + str(data))

else:

    data = comm.recv(source=0, tag=11)
    print('From rank ' + str(rank) + ':\n' + str(data))
